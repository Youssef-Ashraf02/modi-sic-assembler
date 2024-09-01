import pandas as pd

# Opcode dictionaries for format 1 and 3
FORMAT_3_OPCODES = {
    "18":"ADD",
    "40":"AND",
    "28":"COMP",
    "24":"DIV",
    "3C":"J",
    "30":"JEQ",
    "34":"JGT",
    "38":"JLT",
    "48":"JSUB",
    "00":"LDA",
    "50":"LDCH",
    "08":"LDL",
    "04":"LDX",
    "20":"MUL",
    "44":"OR",
    "D8":"RD",
    "4C":"RSUB",
    "0C":"STA",
    "54":"STCH",
    "14":"STL",
    "E8":"STSW",
    "10":"STX",
    "1C":"SUB",
    "E0":"TD",
    "2C":"TIX",
    "DC":"WD",
}

FORMAT_1_OPCODES = {
    "C4":"FIX",
    "C0":"FLOAT",
    "F4":"HIO",
    "C8":"NORM",
    "F0":"SIO",
    "F8":"TIO"
}

ASCII = {chr(i): hex(i)[2:].upper() for i in range(65, 91)}  # ASCII values for A-Z


location_counter_list = []
symbol_table = {}
forward_reference_table = {}
object_code_list = []
dup_object_code_list = []
t_record_list = []
relocating_bits_table = {}
t_record_counter = 0
bytes_counter = 0
relocating_bits = ""
check_relocation = False
total_sum = 0  

def is_numeric(input_string):
    return input_string.isdigit()

def create_symbol_table():
    with open('symbolTable.txt', 'w') as file:
        file.write("SYMBOLTABLE \t REFERENCES\n")
        for key, value in symbol_table.items():
            file.write(f"{key} \t\t {value} \n")

def copy_file_with_relocation(source_file, destination_file):
    try:
        with open(source_file, 'r') as src, open(destination_file, 'w') as dest:
            content = src.readlines()
            for i in range(len(location_counter_list)):
                location = location_counter_list[i]
                relocation_bit = relocating_bits_table.get(location, "")
                line = content[i].strip() if i < len(content) else ""
                dest.write(f"{location}\t {line}\t\t\t\t\t\t {relocation_bit}\n")
        print("File copied successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def update_location_counter_list(hex_sum, current_instruction, current_reference):
    global t_record_counter, bytes_counter, dup_object_code_list, relocating_bits
    location_counter_list.append(hex_sum)

    sum_offset = 0

    if current_instruction == "RESB":
        sum_offset = int(current_reference)
    elif current_instruction == "RESW":
        sum_offset = int(current_reference) * 3
    elif current_instruction in FORMAT_3_OPCODES.values() or current_instruction in FORMAT_1_OPCODES.values():
        sum_offset = 3 if current_instruction in FORMAT_3_OPCODES.values() else 1
        relocating_bits += "1" if current_instruction in FORMAT_3_OPCODES.values() and current_instruction != "RSUB" else "0"
    elif current_instruction == "BYTE":
        byte_length = len(current_reference[2:-1])
        sum_offset = byte_length if current_reference.startswith("C") else byte_length // 2
        relocating_bits += "0"
    elif current_instruction == "WORD":
        sum_offset = 3
        relocating_bits += "0"

    update_sum_and_bytes(sum_offset, sum_offset)
    relocating_bits_table[hex_sum] = relocating_bits[-1] if relocating_bits else "0"

    t_record_counter += 1
    dup_object_code_list.append(object_code_list[-1] if object_code_list else "")

def update_sum_and_bytes(sum_offset, byte_offset):
    global total_sum, bytes_counter
    total_sum += sum_offset
    bytes_counter += byte_offset

def handle_forward_reference(hex_sum, i, df):
    global check_relocation, dup_object_code_list, t_record_counter, bytes_counter, relocating_bits
    if t_record_counter == 10 or (i + 1 < len(df) and df.at[i + 1, 'instruction'] == "END"):
        size = hex(bytes_counter)[2:].zfill(2).upper()
        relocating_bits = relocating_bits + "0" * (12 - len(relocating_bits))
        relocating_bits = hex(int(relocating_bits, 2))[2:].zfill(3).upper()

        start_address = location_counter_list[i - t_record_counter] if i - t_record_counter >= 0 else "000000"
        zaza = "T. " + start_address.zfill(6).upper() + " " + size + " " + relocating_bits + " " + ' '.join(dup_object_code_list)
        t_record_list.append(zaza)

        t_record_counter = 0
        bytes_counter = 0
        dup_object_code_list = []
        relocating_bits = ""

def parse_instruction(row, df, i):
    global check_relocation, total_sum, symbol_table, forward_reference_table, object_code_list
    try:
        current_instruction = row['instruction']
        current_label = row['label']
        current_reference = row['reference']

        is_immediate = current_reference and current_reference.startswith("#")
        if is_immediate:
            current_reference = current_reference[1:]

        object_code = None

        if current_instruction in FORMAT_3_OPCODES.values():
            key_for_value = next((key for key, val in FORMAT_3_OPCODES.items() if val == current_instruction), None)
            if key_for_value:
                object_code = format_instruction(key_for_value, current_reference, is_immediate, i)

        elif current_instruction in FORMAT_1_OPCODES.values():
            key_for_value = next((key for key, val in FORMAT_1_OPCODES.items() if val == current_instruction), None)
            if key_for_value:
                object_code = key_for_value

        elif current_instruction == "WORD":
            object_code = hex(int(current_reference))[2:].zfill(6).upper()

        elif current_instruction == "BYTE":
            object_code = format_byte(current_reference)

        elif current_instruction in ["RESB", "RESW"]:
            object_code = None

        if object_code:
            object_code_list.append(object_code)

        update_location_counter_list(hex(total_sum)[2:].zfill(4).upper(), current_instruction, current_reference)

        if current_label != "...":
            symbol_table[current_label] = hex(total_sum)[2:].zfill(4).upper()

        handle_forward_reference(hex(total_sum)[2:].zfill(4).upper(), i, df)
    
    except Exception as e:
        print(f"Error processing instruction at index {i}: {e}")

def format_instruction(key_for_value, current_reference, is_immediate, i):
    if is_immediate and is_numeric(current_reference):
        key_for_value = hex(int(key_for_value, 16) + 1)[2:].zfill(2)
        return key_for_value + hex(int(current_reference, 16))[2:].zfill(4).upper()
    else:
        value_for_label = symbol_table.get(current_reference, "")
        if not value_for_label:
            forward_reference_table[str(hex(int(location_counter_list[i], 16) + 1)[2:].upper())] = current_reference
        return key_for_value + value_for_label

def format_byte(current_reference):
    if current_reference.startswith("C"):
        return ''.join([ASCII[char] for char in current_reference[2:-1]])
    elif current_reference.startswith("X"):
        return current_reference[2:-1]

def generate_hte_records(df):
    last_ref = df.loc[df['instruction'] == "END", 'reference'].values[0] if not df[df['instruction'] == "END"].empty else "000000"
    start_address = hex(int(df.loc[0, 'reference'], 16))[2:].zfill(6).upper()
    program_length = hex(total_sum - int(start_address, 16))[2:].zfill(6).upper()

    h_record = f"H. {df.iloc[0, 0].ljust(6)} {start_address} {program_length}"
    e_record = f"E. {symbol_table.get(last_ref, '000000').zfill(6).upper()}"

    t_record_list.insert(0, h_record)
    t_record_list.append(e_record)

    with open('ObjectCode.txt', 'w') as file:
        file.write("\n".join(t_record_list))
    print("Object Code file created successfully.")

def main():
    global symbol_table, object_code_list, total_sum
    try:
        with open("Input.txt") as file:
            lines = file.readlines()
            data = [line.strip().split() for line in lines if line.strip()]
            columns = ['label', 'instruction', 'reference']
            df = pd.DataFrame(data, columns=columns)

            total_sum = int(df.loc[0, 'reference'], 16)

            for i, row in df.iterrows():
                parse_instruction(row, df, i)

            generate_hte_records(df)
            create_symbol_table()
            copy_file_with_relocation("InputUPDATED.txt", "InputFINAL.txt")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

# Assembler Program

This program is an implementation of an assembler, a tool used in assembly language programming to convert assembly code into machine code. It processes an input file containing assembly instructions and generates the corresponding object code, symbol table, and relocation information. The assembler handles both format 1 and format 3 opcodes, resolves forward references, and outputs the final machine code in a format suitable for loading into memory.

## Features

- **Opcode Dictionaries**: Contains opcode mappings for format 1 and format 3 instructions.
- **Symbol Table Generation**: Creates and stores a symbol table from the input assembly code.
- **Relocation Handling**: Manages relocation bits for instructions that require address adjustments during execution.
- **Forward Reference Resolution**: Handles cases where symbols are referenced before they are defined.
- **Object Code Generation**: Converts assembly instructions into corresponding machine code (object code).
- **HTE Record Generation**: Creates the H, T, and E records (header, text, and end) needed for the final object code file.
- **Relocation Information**: Copies and updates input files with relocation information.

## How to Use

1. **Input File**: The program reads an input file named `Input.txt` containing assembly code in the following format:

    ```assembly
    LABEL  INSTRUCTION  REFERENCE
    ```

    Example:

    ```assembly
    COPY   START   1000
           LDA     ALPHA
    ALPHA  RESW    1
    ```


2. **Output Files**:
- `ObjectCode.txt`: Contains the final machine code with HTE records.
- `symbolTable.txt`: Lists all labels and their addresses.
- `InputFINAL.txt`: A copy of the input file with location counters and relocation bits.

3. **Execution**: Run the script to process the input file. The program will:
- Parse each instruction.
- Update the location counter.
- Handle relocation and forward references.
- Generate the symbol table and object code.
- Create the final output files.

4. **Error Handling**: Includes basic error checking to handle issues during the assembly process.

## Code Overview

- **Global Variables**: Track the location counter, symbol table, object code, relocation bits, and more.
- **Functions**:
- `is_numeric()`: Checks if a string is numeric.
- `create_symbol_table()`: Writes the symbol table to `symbolTable.txt`.
- `copy_file_with_relocation()`: Copies `InputUPDATED.txt` to `InputFINAL.txt` with relocation bits.
- `update_location_counter_list()`: Updates the location counter and handles various instructions.
- `handle_forward_reference()`: Manages unresolved symbols and updates text records.
- `parse_instruction()`: Processes each instruction and generates machine code.
- `generate_hte_records()`: Creates the HTE records for the object code file.
- `main()`: Coordinates the assembly process from reading input to generating outputs.

## Example

Given an assembly input file (`Input.txt`), the assembler will produce:
- `ObjectCode.txt`: The final machine code with HTE records.
- `symbolTable.txt`: The symbol table with addresses.
- `InputFINAL.txt`: The updated input file with relocation information.

---


Assembler Program
This program is an implementation of an assembler, a tool used in assembly language programming to convert assembly code into machine code. It processes an input file containing assembly instructions and generates the corresponding object code, symbol table, and relocation information. The assembler handles both format 1 and format 3 opcodes, resolves forward references, and outputs the final machine code in a format suitable for loading into memory.

Features
Opcode Dictionaries: Contains opcode mappings for format 1 and format 3 instructions.
Symbol Table Generation: Creates and stores a symbol table from the input assembly code.
Relocation Handling: Manages relocation bits for instructions that require address adjustments during execution.
Forward Reference Resolution: Handles cases where symbols are referenced before they are defined.
Object Code Generation: Converts assembly instructions into corresponding machine code (object code).
HTE Record Generation: Creates the H, T, and E records (header, text, and end) needed for the final object code file.
Relocation Information: Copies and updates input files with relocation information.
How to Use
Input File: The program reads an input file named Input.txt containing assembly code in the following format:

css
Copy code
LABEL INSTRUCTION REFERENCE
Example:

sql
Copy code
COPY   START   1000
       LDA     ALPHA
ALPHA  RESW    1
Output Files:

ObjectCode.txt: Contains the final object code with HTE records.
symbolTable.txt: Contains the symbol table with references.
InputFINAL.txt: Contains the updated input file with location counters and relocation bits.
Run the Program: Simply execute the script. It will process the input file and generate the necessary outputs.

Error Handling: The program includes basic error handling to catch and display any issues that arise during the execution.

Code Structure
Global Variables: Store various states such as the location counter, symbol table, object code, relocation bits, etc.
Functions:
is_numeric: Checks if a string is numeric.
create_symbol_table: Writes the symbol table to a file.
copy_file_with_relocation: Copies the input file while adding relocation information.
update_location_counter_list: Updates the location counter based on the instruction.
update_sum_and_bytes: Updates the sum and byte counters.
handle_forward_reference: Manages forward references and updates the text records.
parse_instruction: Parses each assembly instruction and generates corresponding object code.
format_instruction: Formats instructions into machine code.
format_byte: Converts BYTE instructions into corresponding machine code.
generate_hte_records: Generates the HTE records for the final object code file.
main: The main function that orchestrates the entire assembly process.
Example
Given an assembly input file (Input.txt), the assembler will generate an object code file (ObjectCode.txt) that includes the HTE records, as well as the symbol table (symbolTable.txt) and the updated input file (InputFINAL.txt) with relocation information.

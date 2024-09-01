<h1 align="center"> Modi-SIC Disassembler </h1>
This project aims to disassemble High-Level Assembler (HTE) records, extracting data to create a SYMBOL table and generate the corresponding ASSEMBLY code. By analyzing HTE records, the system offers a thorough disassembly, improving both the clarity and utility of the SYMBOL table and ASSEMBLY code.
Symbol Table Management (symbolTable.py)
To explore the functionality of the symbolTable.py script, follow these steps:

Open Terminal/Command Prompt:

Access a terminal or command prompt on your system.
Execute the Script:

Run the script using the Python interpreter with:
bash
Copy code
python symbolTable.py
Design Considerations:
Purpose:

The script aims to set up references to memory addresses by inserting object codes into the SYMBOL table, facilitating the use of object codes tied to specific addresses.
Challenge:

A key aspect is the removal of entries from the SYMBOL table. This removal is crucial for maintaining an accurate table and depends on the successful execution of the assembly process.
Assembly Code Processing (assembly.py)
To see how the assembly.py script operates, follow these steps:

Open Terminal/Command Prompt:

Open a terminal or command prompt window.
Run the Script:

Execute the script with the Python interpreter using:
bash
Copy code
python assembly.py
Design Considerations:
Purpose:

The execution of the assembly code relies heavily on accurate references to memory addresses, which are carefully managed within the SYMBOL table.
Challenge:

The main design issue is the interdependence between the assembly code and the SYMBOL table. Effective assembly requires precise address references, necessitating coordination with the SYMBOL table.
Main Execution Program (main.py)
To understand the functionality of the main.py script, follow these instructions:

Open Terminal/Command Prompt:

Access your terminal or command prompt.
Run the Script:

Execute the script using:
bash
Copy code
python main.py
Design Considerations:
Object Code Management:

The initial inclusion of object codes in the SYMBOL table and the subsequent removal of entries can affect the table's accuracy.
Dependency on Address References:

The assembly code's reliance on address references from the SYMBOL table presents synchronization challenges, especially when the table is updated during execution.

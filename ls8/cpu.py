"""CPU functionality."""

import sys
from sys import argv

SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """ When the LS-8 CPU is booted, the following steps occur: """
        """
        ## Registers
        # 8 general-purpose 8-bit numeric registers R0-R7.

        * `R0`-`R6` are cleared to `0`.
        * `R7` is set to `0xF4`.
        * `PC` and `FL` registers are cleared to `0`.
        * RAM is cleared to `0`.

        # * R5 is reserved as the interrupt mask (IM)
        # * R6 is reserved as the interrupt status (IS)
        # * R7 is reserved as the stack pointer (SP)
        """
        self.registers = bytearray(8)


        """
        # total of 256 bytes of memory
        """
        self.memory = bytearray(256)


        """
        The SP points at the value at the top of the stack (most recently pushed), or at
        address `F4` if the stack is empty.
        
        The value of the key pressed is stored in address `0xF4`
        
        """
        self.registers[SP] = 0xF4


        """#`PC`: Program Counter, address of the currently executing instruction : internal register"""
        self.PC = 0

        """
        # `FL`: Flags, holds the current flags status
        # These flags can change based on the operands given to the `CMP` opcode.
        # If a particular bit is set, that flag is "true" : internal register
        """
        self.FL = 0


        """
        Some instructions set the PC directly. These are:
        * CALL : Calls a subroutine (function) at the address stored in the register.
        * INT : 
        * IRET
        * LDI : Set the value of a register to an integer.
        * JMP
        * JNE
        * JEQ
        * JGT
        * JGE
        * JLT
        * JLE
        * RET
        * HLT : Halt the CPU (and exit the emulator).
        * PRN : Print numeric value stored in the given register.
        * MUL : Multiply the values in two registers together and store the result in registerA.

        * CMP : Compare the values in two registers.
        """
        """ Not really all mutators rather register instructions.. but will likely store other and mutators here"""
        self.pc_mutators = {
            'PRN' : 0b01000111,
            'LDI' : 0b10000010,
            'HLT' : 0b00000001,
            'PUSH': 0b01000101,
            'POP' : 0b01000110
        }


        """ # *These are instructions handled by the ALU.* """
        self.alu_ops = {
            0b10100010: 'MUL',
            0b10100011: 'DIV',
            0b10100100: 'MOD',
            0b10100001: 'SUB',
            0b10100000: 'ADD',
            0b10101011: 'XOR',
            0b01101001: 'NOT',
            0b10101010: 'OR',
            0b01100101: 'INC',
            0b01100110: 'DEC',
            0b10100111: 'CMP',
            0b10101100: 'SHL',
            0b10101101: 'SHR',
            0b10101000: 'AND'

        }


    def load(self, program):

        """Load a program into memory. # Step 7: Un-hardcode the machine code """

        address = 0
        
        for instruction in program:
            if instruction:
                instruction = instruction.split()[0]
                if instruction[0] != '#':

                    # convert the binary strings to integer values to store in RAM. The built-in `int()` function
                    self.memory[address] = int(instruction, 2)
                    address += 1


    """ Step 2: Add RAM functions """

    """
     > Inside the CPU, there are two __internal registers__ used for memory operations:
     > the _Memory Address Register_ (MAR) and the _Memory Data Register_ (MDR). The
     > MAR contains the address that is being read or written to. The MDR contains
     > the data that was read or the data to write. You don't need to add the MAR or
     > MDR to your `CPU` class, but they would make handy parameter names for
     > `ram_read()` and `ram_write()`, if you wanted.
     
    """
    def ram_read(self, memory_address_register):
        """ should accept the address to read and return the value stored """

        # note: here we are using _operands_ : _opcode_
        memory_data_register = self.memory[memory_address_register]
        return memory_data_register


    def ram_write(self, memory_data_register, memory_address_register):
        """ should accept the value to write and the address to write to """

        # note: here we are using _opcode_ : _operands_ 
        self.memory[memory_address_register] = memory_data_register


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        
        elif op == "SUB":
            self.registers[reg_a] -= self.registers[reg_b]

        # Step 8: Implement a Multiply and Print the Result
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print(sys.argv)



    def run(self):
        """  Step 3: Implement the core of `CPU`'s `run()` method """

        """
        This is the workhorse function of the entire processor.

        It needs to read the memory address that's stored in register `PC`, and store
        that result in `IR`, the _Instruction Register_.


        Some instructions requires up to the next two bytes of data _after_ the `PC` in
        memory to perform operations on. Sometimes the byte value is a register number,
        other times it's a constant value (in the case of `LDI`).

        Using `ram_read()`,
        read the bytes at `PC+1` and `PC+2` from RAM into variables `operand_a` and
        `operand_b` in case the instruction needs them.
  
        """

        running = True

        """ `IR`: Instruction Register, contains a copy of the currently executing instruction"""
        while running:
            IR = self.ram_read(self.PC)

            """
             This is _currently_ `O(n)` It would be a lot better if it were an `O(1)` process..
            """
            # Step 4: Implement the `HLT` instruction handler
            if IR == self.pc_mutators['HLT']:
                sys.exit(0)


            # Step 5: Add the `LDI` instruction
            elif IR == self.pc_mutators['LDI']:
                #register_A : the Address
                register_a = self.ram_read(self.PC + 1)
                #register_B : the Value
                register_b = self.ram_read(self.PC + 2)
                self.registers[register_a] = register_b
                self.PC += 3
            

            # Step 6: Add the `PRN` instruction
            elif IR == self.pc_mutators['PRN']:
                register_a = self.memory[self.PC + 1]
                print(self.registers[register_a])
                self.PC += 2
            

            # Add the POP instruction
            elif IR == self.pc_mutators['POP']:
                register_a = self.memory[self.PC + 1]
                self.registers[register_a] = self.memory[self.registers[SP]]
                self.registers[SP] += 1
                self.PC += 2

            # Add the PUSH instruction
            elif IR == self.pc_mutators['PUSH']:
                register_a = self.memory[self.PC + 1]
                register_b = self.registers[register_a]
                self.registers[SP] -= 1
                self.memory[self.registers[SP]] = register_b
                self.PC += 2

            # Arithmetic (alu) Operations
            # Step 8: Implement a Multiply and Print the Result
            elif IR in self.alu_ops:
                register_a = self.memory[self.PC + 1]
                register_b = self.memory[self.PC + 2]
                self.alu(self.alu_ops[IR], register_a, register_b)
                self.PC += 3


            else:
                print(f'Unknown instruction at: {IR}')
                sys.exit(1)

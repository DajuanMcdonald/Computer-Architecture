"""CPU functionality."""

import sys
from sys import argv

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
        SP = 7
        self.registers[SP] = 0xF4


        """#`PC`: Program Counter, address of the currently executing instruction """
        self.PC = 0

        """# `IR`: Instruction Register, contains a copy of the currently executing instruction"""
        self.IR = 0

        """
        # `FL`: Flags, holds the current flags status
        # These flags can change based on the operands given to the `CMP` opcode.
        # If a particular bit is set, that flag is "true"
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
        self.INSTRUCTION_SET = {
            'CALL' : 0b01010000,
            'INT' : 0b01010010,
            'MUL' : 0b10100010,
            'PRN' : 0b01000111,
            'LDI' : 0b10000010,
            'HLT' : 0b00000001,

        }



        

    def load(self, program):

        """Load a program into memory."""
        # Step 7: Un-hardcode the machine code

        address = 0
        
        for instruction in program:
            if instruction:
                instruction = instruction.split()[0]
                if instruction[0] != '#':

                    # convert the binary strings to integer values to store in RAM. The built-in `int()` function
                    self.memory[address] = int(instruction, 2)
                    address += 1

    """
     Add RAM functions
    """
    def ram_read(self, memory_address_register):
        """ should accept the address to read and return the value stored """
        memory_data_register = self.memory[memory_address_register]
        return memory_data_register



    def ram_write(self, memory_data_register, memory_address_register):
        """ should accept the value to write and the address to write to """
        self.memory[memory_address_register] = memory_data_register


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        #elif op == "SUB": etc
        elif op == "SUB":
            self.registers[reg_a] -= self.registers[reg_b]
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
        """Run the CPU. Implement the core of `CPU`'s `run()` method """
        # _opcode = _operands
        IR = self.PC
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        # MUL = 0b10100010

        running = True

        while running:
            IR = self.ram_read(self.PC)
            # op_a = register_address
            # op_b = register_data

            #   Step 4: Implement the `HLT` instruction handler
            if IR == HLT:
                # running = False
                # self.PC += 1
                sys.exit(0)


            # Step 5: Add the `LDI` instruction
            elif IR == LDI:
                op_a = self.ram_read(self.PC + 1)
                op_b = self.ram_read(self.PC + 2)
                self.registers[op_a] = op_b
                self.PC += 3


            # Step 6: Add the `PRN` instruction
            elif IR == PRN:
                op_a = self.memory[self.PC + 1]
                print(self.registers[op_a])
                self.PC += 2

            # elif instruction == MUL:
            #     print(self.registers[op_a] * self.registers[op_b])


            else:
                print(f'Unknown instruction at: {IR}')
                # running = False
                sys.exit(1)

"""CPU functionality."""

import sys

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

        address = 0
        
        for instruction in program:
            if instruction:
                instruction = instruction.split()[0]
                if instruction[0] != '#':
                    self.memory[address] = int(instruction, 2)
                    address += 1

    def ram_read(self, memory_address_register):
        """ should accept the address to read and return the value stored """
        memory_data_register = self.memory[memory_address_register]
        return memory_data_register


    def ram_write(self, value, memory_address_register):
        """ should accept the value to write and the address to write to """
        self.memory[memory_address_register] = value


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
        """Run the CPU."""
        # _opcode = _operands
        IR = self.PC
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001

        running = True

        while running:
            instruction = self.ram_read(IR)
            op_a = self.ram_read(IR + 1)
            op_b = self.ram_read(IR + 2)

            if instruction == LDI:
                self.registers[op_a] == op_b
                IR += 3

            elif instruction == PRN:
                print(self.registers[op_a])
                IR += 2

            elif instruction == HLT:
                running = False
                IR += 1
                sys.exit(0)

            else:
                print(f'Unknown instruction at: {IR}')
                running = False
                sys.exit(1)

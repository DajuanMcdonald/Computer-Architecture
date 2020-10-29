"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.memory = bytearray(256)
        self.registers = bytearray(8)
        self.pc = 0
        

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000, # NOP
            0b00001000, # ?
            0b01000111, # PRN R0
            0b00000000, # NOP
            0b00000001, # HLT
        ]

        for instruction in program:
            self.memory[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        #elif op == "SUB": etc
        elif op == "SUB":
            self.registers[reg_a] -= self.registers[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.registers[i], end='')

        print()

    def ram_read(self, address):
        """ should accept the address to read and return the value stored """
        return self.memory[address]

    def ram_write(self, address, data):
        """ should accept the value to write and the address to write to """
        self.memory[address] = data


    def run(self):
        """Run the CPU."""
        IR = self.pc
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
                sys.exit(0)

            else:
                print(f'Unknown instruction at: {IR}')
                sys.exit(1)

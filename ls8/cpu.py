"""CPU functionality."""

import sys
from sys import argv

SP = 7
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
PRN = 0b01000111
LDI = 0b10000010
HLT = 0b00000001
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100
SUB = 0b10100001
ADD = 0b10100000
DEC = 0b01100110
INC = 0b01100101
PRA = 0b01001000



class CPU:
    """Main CPU class."""

    def __init__(self):
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
        # self.pc_mutators = {
        #     'PRN' : 0b01000111,
        #     'LDI' : 0b10000010,
        #     'HLT' : 0b00000001,
        #     'PUSH': 0b01000101,
        #     'POP' : 0b01000110,
        #     'CALL': 0b01010000,
        #     'RET' : 0b00010001,
        #     'JMP' : 0b01010100,
        #     'JNE' : 0b01010110,
        #     'JEQ' : 0b01010101,
        # }

        # Set up the branch table
        self.branchtable = {}
        self.branchtable[CMP] = self.handle_cmp
        self.branchtable[JMP] = self.handle_jmp
        self.branchtable[JEQ] = self.handle_jeq
        self.branchtable[JNE] = self.handle_jne
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[POP] = self.handle_pop
        self.branchtable[CALL] = self.handle_call
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[RET] = self.handle_ret
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[ADD] = self.handle_add
        self.branchtable[SUB] = self.handle_sub
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[DEC] = self.handle_dec
        self.branchtable[INC] = self.handle_inc
        self.branchtable[PRA] = self.handle_pra





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
        # memory_data_register = self.memory[memory_address_register]
        # return memory_data_register
        return self.memory[memory_address_register]


    def ram_write(self, memory_data_register, memory_address_register):
        """ should accept the value to write and the address to write to """

        # note: here we are using _opcode_ : _operands_ 
        self.memory[memory_address_register] = memory_data_register

    def handle_jmp(self):
        register_a = self.memory[self.PC + 1]
        self.PC = self.registers[register_a]

    def handle_jeq(self):
        if self.E == 1:
            self.handle_jmp()
        else:
            self.PC += 2

    def handle_jne(self):
        if self.E == self.FL:
            self.handle_jmp()
        else:
            self.PC += 2

    def handle_push(self):
        register_a = self.memory[self.PC + 1]
        register_b = self.registers[register_a]
        self.registers[SP] -= 1
        self.memory[self.registers[SP]] = register_b
        self.PC += 2

    def handle_pop(self):
        register_a = self.memory[self.PC + 1]
        self.registers[register_a] = self.memory[self.registers[SP]]
        self.registers[SP] += 1
        self.PC += 2

    def handle_call(self):
        self.registers[SP] -= 1
        self.memory[self.registers[SP]] = self.PC + 2
        register_a = self.memory[self.PC + 1]
        self.PC = self.registers[register_a]

    def handle_hlt(self):
        sys.exit(0)

    def handle_ret(self):
        self.PC = self.memory[self.registers[SP]]
        self.registers[SP] += 1

    def handle_ldi(self):
        register_a = self.ram_read(self.PC + 1)
        register_b = self.ram_read(self.PC + 2)
        self.registers[register_a] = register_b
        self.PC += 3

    def handle_prn(self):
        register_a = self.memory[self.PC + 1]
        print(self.registers[register_a])
        self.PC += 2

    def handle_pra(self):
        register_a = self.ram_read(self.PC + 1)
        register_b = self.ram_read(self.PC + 2)
        self.registers[register_a] = register_b
        self.PC += 3

        print(ascii(register_b))

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        
        elif op == "SUB":
            self.registers[reg_a] -= self.registers[reg_b]

        # Step 8: Implement a Multiply and Print the Result
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]

        elif op == "DEC":
            self.registers[reg_a] = self.registers[reg_b] - 1

        elif op == "INC":
            self.registers[reg_a] = self.registers[reg_b] + 1

        elif op == "CMP":
            if self.registers[reg_a] == self.registers[reg_b]:
                self.E = 1
                self.L = self.FL
                self.G = self.FL
            elif reg_a < reg_b:
                self.E = self.FL
                self.L = 1
                self.G = self.FL

            elif reg_a > reg_b:
                self.E = self.FL
                self.L = self.FL
                self.G = self.FL

        else:
            raise Exception("Unsupported ALU operation")

    """ *These are instructions handled by the ALU.* """

    def handle_cmp(self):
        register_a = self.ram_read(self.PC + 1)
        register_b = self.ram_read(self.PC + 2)
        self.alu('CMP', register_a, register_b)
        self.PC += 3


    def handle_add(self):
        register_a = self.ram_read(self.PC + 1)
        register_b = self.ram_read(self.PC + 2)
        self.alu('ADD', register_a, register_b)
        self.PC += 3

    def handle_sub(self):
        register_a = self.ram_read(self.PC + 1)
        register_b = self.ram_read(self.PC + 2)
        self.alu('SUB', register_a, register_b)
        self.PC += 3

    def handle_mul(self):
        register_a = self.ram_read(self.PC + 1)
        register_b = self.ram_read(self.PC + 2)
        self.alu('MUL', register_a, register_b)
        self.PC += 3

    def handle_dec(self):
        register_a = self.ram_read(self.PC + 1)
        register_b = self.ram_read(self.PC + 2)
        self.alu('DEC', register_a, register_b)
        self.PC += 3

    def handle_inc(self):
        register_a = self.ram_read(self.PC + 1)
        register_b = self.ram_read(self.PC + 2)
        self.alu('INC', register_a, register_b)
        self.PC += 3

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
            IR = self.PC
            INS = self.memory[IR]
            self.branchtable[INS]()

            """ 
             This is _currently_ `O(n)` It would be a lot better if it were an `O(1)` process..
            """
            # Step 4: Implement the `HLT` instruction handler
            # if IR == self.pc_mutators['HLT']:
            #     sys.exit(0)


            # # Step 5: Add the `LDI` instruction
            # elif IR == self.pc_mutators['LDI']:
            #     #register_A : the Address
            #     register_a = self.ram_read(self.PC + 1)
            #     #register_B : the Value
            #     register_b = self.ram_read(self.PC + 2)
            #     self.registers[register_a] = register_b
            #     self.PC += 3
            

            # # Step 6: Add the `PRN` instruction
            # elif IR == self.pc_mutators['PRN']:
            #     register_a = self.memory[self.PC + 1]
            #     print(self.registers[register_a])
            #     self.PC += 2
            

            # # Add the POP instruction
            # elif IR == self.pc_mutators['POP']:
            #     register_a = self.memory[self.PC + 1]
            #     self.registers[register_a] = self.memory[self.registers[SP]]
            #     self.registers[SP] += 1
            #     self.PC += 2


            # # Add the PUSH instruction
            # elif IR == self.pc_mutators['PUSH']:
            #     register_a = self.memory[self.PC + 1]
            #     register_b = self.registers[register_a]
            #     self.registers[SP] -= 1
            #     self.memory[self.registers[SP]] = register_b
            #     self.PC += 2

            # # Add the CALL instruction
            # elif IR == self.pc_mutators['CALL']:
            #     self.registers[SP] -= 1
            #     self.memory[self.registers[SP]] = self.PC + 2
            #     register_a = self.memory[self.PC + 1]
            #     self.PC = self.registers[register_a]

            # # Add the RET instruction
            # elif IR == self.pc_mutators['RET']:
            #     self.PC = self.memory[self.registers[SP]]
            #     self.registers[SP] += 1

            # # Add the JMP instruction
            # # Jump to the address stored in the given register.
            # # Set the `PC` to the address stored in the given register.

            # elif IR == self.pc_mutators['JMP']:
            #     register_a = self.ram_read(self.PC + 1)
            #     self.PC = self.registers[register_a]

            

            # # Add the JEQ instruction
            # elif IR == self.pc_mutators['JEQ']:
            #     register_a = self.ram_read(self.PC + 1)
            #     # register_a = self.memory[self.PC + 1]
            #     self.registers[self.FL] == 1
            #     self.PC = self.registers[register_a]
                


            # # Add the JNE instruction
            # elif IR == self.pc_mutators['JNE']:
            #     register_a = self.ram_read(self.PC + 1)
            #     # register_a = self.memory[self.PC + 1]
                
            #     self.registers[self.FL] == 1
            #     self.PC = self.registers[register_a]


            # # Arithmetic (alu) Operations
            # # Step 8: Implement a Multiply and Print the Result
            # if IR in self.alu_ops:
            #     register_a = self.memory[self.PC + 1]
            #     register_b = self.memory[self.PC + 2]
            #     self.alu(self.alu_ops[IR], register_a, register_b)
            #     self.PC += 3

            # if IR == self.alu_ops['CMP']:
            #     register_a = self.ram_read(self.PC + 1)
            #     register_b = self.ram_read(self.PC + 2)
            #     if self.registers[register_a] == self.registers[register_b]:
            #         self.registers[self.FL] = 1
            #     elif self.registers[register_a] > self.registers[register_b]:
            #         self.registers[self.FL] = 2

            # else:
            #     print(f'Unknown instruction at: {IR}')
            #     sys.exit(1)

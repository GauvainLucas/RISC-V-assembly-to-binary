# Python script to convert RISC-V RV32I assembly instructions to binary
#
# RISC-V table
# https://five-embeddev.com/riscv-user-isa-manual/Priv-v1.12/instr-table.html
#
# Table of correspondance between registers and their names
# https://en.wikichip.org/wiki/risc-v/registers
#
# Verify the results
# https://luplab.gitlab.io/rvcodecjs/
#
# Author: Lucas Gauvain
# © LAOB - UFABC 2024

import re

# Opcode map
opcode_map = {
    'lui'   : '0110111',
    'auipc' : '0010111',
    'jal'   : '1101111',
    'jalr'  : '1100111',
    'beq'   : '1100011',
    'bne'   : '1100011',
    'blt'   : '1100011',
    'bge'   : '1100011',
    'bltu'  : '1100011',
    'bgeu'  : '1100011',
    'lb'    : '0000011',
    'lh'    : '0000011',
    'lw'    : '0000011',
    'lbu'   : '0000011',
    'lhu'   : '0000011',
    'sb'    : '0100011',
    'sh'    : '0100011',
    'sw'    : '0100011',
    'addi'  : '0010011',
    'slti'  : '0010011',
    'sltiu' : '0010011',
    'xori'  : '0010011',
    'ori'   : '0010011',
    'andi'  : '0010011',
    'slli'  : '0010011',
    'srli'  : '0010011',
    'srai'  : '0010011',
    'add'   : '0110011',
    'sub'   : '0110011',
    'sll'   : '0110011',
    'slt'   : '0110011',
    'sltu'  : '0110011',
    'xor'   : '0110011',
    'srl'   : '0110011',
    'sra'   : '0110011',
    'or'    : '0110011',
    'and'   : '0110011'
}

# Funct3 map
funct3_map = {
    'add'   : '000', 
    'sub'   : '000', 
    'sll'   : '001', 
    'slt'   : '010', 
    'sltu'  : '011',
    'xor'   : '100', 
    'srl'   : '101', 
    'sra'   : '101', 
    'or'    : '110', 
    'and'   : '111',
    'addi'  : '000', 
    'slti'  : '010', 
    'sltiu' : '011', 
    'xori'  : '100', 
    'ori'   : '110',
    'andi'  : '111', 
    'slli'  : '001', 
    'srli'  : '101', 
    'srai'  : '101',
    'beq'   : '000', 
    'bne'   : '001', 
    'blt'   : '100', 
    'bge'   : '101', 
    'bltu'  : '110', 
    'bgeu'  : '111',
    'sb'    : '000', 
    'sh'    : '001', 
    'sw'    : '010', 
    'lb'    : '000', 
    'lh'    : '001', 
    'lw'    : '010',
    'lbu'   : '100', 
    'lhu'   : '101', 
    'jalr'  : '000'
}

# Funct7 map
funct7_map = {
    'add'  : '0000000', 
    'sub'  : '0100000', 
    'sll'  : '0000000', 
    'slt'  : '0000000',
    'sltu' : '0000000', 
    'xor'  : '0000000', 
    'srl'  : '0000000', 
    'sra'  : '0100000',
    'or'   : '0000000', 
    'and'  : '0000000', 
    'slli' : '0000000', 
    'srli' : '0000000', 
    'srai' : '0100000'
}

# Full instruction map
full_instruction_map = {
    'fence.tso' : '10000011001100000000000000001111',
    'pause'     : '00000001000000000000000000001111',
    'ecall'     : '00000000000000000000000001110011',
    'ebreak'    : '00000000000100000000000001110011'
}
# Register names map
register_map = {
    'zero' : 'x0',
    'ra'   : 'x1',
    'sp'   : 'x2',
    'gp'   : 'x3',
    'tp'   : 'x4',
    't0'   : 'x5',
    't1'   : 'x6',
    't2'   : 'x7',
    's0'   : 'x8',
    's1'   : 'x9',
    'a0'   : 'x10',
    'a1'   : 'x11',
    'a2'   : 'x12',
    'a3'   : 'x13',
    'a4'   : 'x14',
    'a5'   : 'x15',
    'a6'   : 'x16',
    'a7'   : 'x17',
    's2'   : 'x18',
    's3'   : 'x19',
    's4'   : 'x20',
    's5'   : 'x21',
    's6'   : 'x22',
    's7'   : 'x23',
    's8'   : 'x24',
    's9'   : 'x25',
    's10'  : 'x26', 
    's11'  : 'x27',  
    't3'   : 'x28',
    't4'   : 'x29',
    't5'   : 'x30',
    't6'   : 'x31',
}

# Secondary register names map
secondary_register_names = {
    'fp': 's0'
}

def decode_register(register):
    if register in register_map:
        return register_map[register]
    elif register in secondary_register_names: # au cas ou il y a un 2nd nom
        return register_map[secondary_register_names[register]]
    else:
        return register

def decode_instruction(instr):
    parts = re.split(r'(\W+)', instr)
    decoded_parts = [decode_register(part) for part in parts]
    return ''.join(decoded_parts)


def match_instruction(instr):
    match1 = re.match(r'(\w+)\s+x(\d+),\s*(-?\d+)\(x(\d+)\)', instr)
    match2 = re.match(r'(\w+)\s+x(\d+),\s*x(\d+),\s*x(\d+)', instr)
    if not match1 and not match2:
        raise ValueError(f"Instruction format not recognized: {instr}")
    

# Function to convert R-type instructions to binary
def r_type_to_bin(instr):
    decod_instr = decode_instruction(instr)
    parts = decod_instr.split()
    opcode = opcode_map[parts[0]]
    match = re.match(r'(\w+)\s+x(\d+),\s*x(\d+),\s*x(\d+)', decod_instr)
    if not match:
        raise ValueError(f"Instruction format not recognized: {instr}")
    rd = format(int(match.group(2)), '05b')
    rs1 = format(int(match.group(3)), '05b')
    rs2 = format(int(match.group(4)), '05b')
    funct3 = funct3_map[match.group(1)]
    funct7 = funct7_map.get(match.group(1), '0000000')
    return funct7 + " " + rs2 + " " + rs1 + " " + funct3 + " " + rd + " " + opcode

# Function to convert I-type instructions to binary
def i_type_to_bin(instr):
    decod_instr = decode_instruction(instr)
    parts = decod_instr.split()
    opcode = opcode_map[parts[0]]
    match = re.match(r'(\w+)\s+x(\d+),\s*(-?\d+)\(x(\d+)\)', decod_instr)
    if not match:
        raise ValueError(f"Instruction format not recognized: {decod_instr}")
    rd = format(int(parts[1][1:]), '05b')
    rs1 = format(int(parts[2][1:]), '05b')
    imm = format(int(parts[3]), '012b')
    funct3 = funct3_map[parts[0]]
    return imm + " " + rs1 + " " + funct3 + " " + rd + " " + opcode


# Function to convert I-type load instructions to binary
def i_type_load_to_bin(instr):
    decod_instr = decode_instruction(instr)
    parts = decod_instr.split()
    opcode = opcode_map[parts[0]]
    match = re.match(r'(\w+)\s+x(\d+),\s*(-?\d+)\(x(\d+)\)', decod_instr)
    if not match:
        raise ValueError(f"Instruction format not recognized: {decod_instr}")

    rd = format(int(match.group(2)), '05b')
    offset = int(match.group(3))
    rs1 = format(int(match.group(4)), '05b')
    imm = format(offset & 0xFFF, '012b') 
    funct3 = funct3_map[parts[0]]
    
    return imm + " " + rs1 + " " + funct3 + " " + rd + " " + opcode


# Function to convert I-type shift instructions to binary
def i_type_shift_to_bin(instr):
    decod_instr = decode_instruction(instr)
    parts = decod_instr.split()
    opcode = opcode_map[parts[0]]
    rd = format(int(parts[1][1:]), '05b')
    rs1 = format(int(parts[2][1:]), '05b')
    shamt = format(int(parts[3]), '05b')  
    funct3 = funct3_map[parts[0]]
    funct7 = funct7_map[parts[0]]
    
    return funct7 + " " + shamt + " " + rs1 + " " + funct3 + " " + rd + " " + opcode

# Function to convert S-type instructions to binary
def s_type_to_bin(instr):
    decod_instr = decode_instruction(instr)
    parts = decod_instr.split()
    opcode = opcode_map[parts[0]]
    match = re.match(r'(\w+)\s+x(\d+),\s*(-?\d+)\(x(\d+)\)', decod_instr)
    if not match:
        raise ValueError(f"Instruction format not recognized: {decod_instr}")
    
    rs2 = format(int(match.group(2)), '05b')
    offset = int(match.group(3))
    rs1 = format(int(match.group(4)), '05b')
    imm = format(offset & 0xFFF, '012b')  
    imm_11_5 = imm[:7]  
    imm_4_0 = imm[7:]  
    funct3 = funct3_map[parts[0]]
    return imm_11_5 + " " + rs2 + " " + rs1 + " " + funct3 + " " + imm_4_0 + " " + opcode

# Function to convert B-type instructions to binary
def b_type_to_bin(instr):
    decod_instr = decode_instruction(instr)
    parts = decod_instr.split()
    opcode = opcode_map[parts[0]]
    rs1 = format(int(parts[1][1:]), '05b')
    rs2 = format(int(parts[2][1:]), '05b')
    imm = format(int(parts[3]), '013b')
    imm_12 = imm[0]
    imm_10_5 = imm[2:8]
    imm_4_1 = imm[8:12]
    imm_11 = imm[12]
    funct3 = funct3_map[parts[0]]

    return imm_12 + " " + imm_10_5 + " " + rs2 + " " + rs1 + " " + funct3 + " " + imm_4_1 + " " + imm_11 + " " + opcode

# Function to convert U-type instructions to binary
def u_type_to_bin(instr):
    decod_instr = decode_instruction(instr)
    parts = decod_instr.split()
    opcode = opcode_map[parts[0]]
    rd = format(int(parts[1][1:]), '05b')
    imm = format(int(parts[2]), '020b')

    return imm + " " + rd + " " + opcode

# Function to convert J-type instructions to binary
def j_type_to_bin(instr):
    decod_instr = decode_instruction(instr)
    parts = decod_instr.split()
    opcode = opcode_map[parts[0]]
    rd = format(int(parts[1][1:]), '05b')
    imm = format(int(parts[2]), '021b')
    imm_20 = imm[0]
    imm_10_1 = imm[10:20]
    imm_11 = imm[9]
    imm_19_12 = imm[0:8]

    return imm_20 + " " + imm_10_1 + " " + imm_11 + " " + imm_19_12 + " " + rd + " " + opcode

def full_instruction_to_bin(instr):
    decod_instr = decode_instruction(instr)
    return full_instruction_map[decod_instr]
# Test instructions
instructions_r = [ 
    'add ra, x2, x3',     # R-type
    'sub x2, x3, x1',     # R-type
    'sll x3, x1, x2',     # R-type
    'slt x1, x3, x2',     # R-type
    'sltu x2, x1, x3',    # R-type
    'xor x3, x2, x1',     # R-type
    'srl x1, x2, x3',     # R-type
    'sra x2, x3, x1',     # R-type
    'or x3, x1, x2',      # R-type
    'and x1, x3, x2'      # R-type 
]

instructions_u = [ 
    'lui x1 1000',      # U-type
    'auipc x2 500',     # U-type
]

instructions_j = [ 
    'jal x1 2000',      # J-type
    'jal x1 1234',      # J-type
]

instructions_b = [ 
    'beq x1 x2 20',     # B-type
    'bne x2 x3 30',     # B-type
    'blt x1 x3 40',     # B-type
    'bge x2 x1 50',     # B-type
    'bltu x1 x2 60',    # B-type
    'bgeu x3 x1 70',    # B-type
]

instructions_i = [ 
    'addi x1 x2 10',    # I-type
    'slti x2 x3 20',    # I-type
    'sltiu x3 x1 30',   # I-type
    'xori x1 x2 40',    # I-type
    'ori x2 x3 50',     # I-type
    'andi x3 x1 60',    # I-type
]

instructions_i_type_load= [ 
    'jalr x3, 300(x1)', # I-type (jalr)
    'lb x1, 100(x2)',   # I-type-load
    'lh x2, 200(x3)',   # I-type-load
    'lw x3, 300(x1)',   # I-type-load
    'lbu x1, 400(x2)',  # I-type-load
    'lhu x2, 500(x3)',  # I-type-load
]

instructions_i_type_shift = [ 
    'slli x1 x2 1',     # I-type-shift
    'srli x2 x3 2',     # I-type-shift
    'srai x3 x1 3',     # I-type-shift
]

instructions_s = [ 
    'sb x3, 600(x1)',   # S-type
    'sh x1, 700(x2)',   # S-type
    'sw x2, 800(x3)',   # S-type
    'sb a3, 600(t0)',   # S-type
]

instructions_mix = [
    'slli ra sp 1',     # I-type (shift)
    'srli s1 t1 2',     # I-type (shift)
    'srai a1 zero 3',   # I-type (shift)
    'lw s0, 100(a0)',   # I-type (load)
    'sw t0, 200(gp)',   # S-type (store)
    'add fp, t1, t2',     # R-type
    'ecall',            # Full instruction
]

def get_bin(instr):
    parts = instr.split()
    instr_type = parts[0]
    if instr_type in ['lui', 'auipc']:
        return u_type_to_bin(instr)
    elif instr_type in ['jal']:
        return j_type_to_bin(instr)
    elif instr_type in ['addi', 'slti', 'sltiu', 'xori', 'ori', 'andi']:
        return i_type_to_bin(instr)
    elif instr_type in ['lb', 'lh', 'lw', 'lbu', 'lhu', 'jalr']:
        return i_type_load_to_bin(instr)
    elif instr_type in ['slli', 'srli', 'srai']:
        return i_type_shift_to_bin(instr)
    elif instr_type in ['beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu']:
        return b_type_to_bin(instr)
    elif instr_type in ['sb', 'sh', 'sw']:
        return s_type_to_bin(instr)
    elif instr_type in ['add', 'sub', 'sll', 'slt', 'sltu', 'xor', 'srl', 'sra', 'or', 'and']:
        return r_type_to_bin(instr)
    elif instr_type in full_instruction_map:
        return full_instruction_to_bin(instr)
    else:
        raise ValueError(f"Unknown instruction type: {instr}")


for instr in instructions_mix:
    print(f"{instr} -> {get_bin(instr)}")

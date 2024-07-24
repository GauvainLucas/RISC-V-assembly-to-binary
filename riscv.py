import re

# Define the opcode map and funct3/funct7 values
opcode_map = {
    'LUI'   : '0110111',
    'AUIPC' : '0010111',
    'JAL'   : '1101111',
    'JALR'  : '1100111',
    'BEQ'   : '1100011',
    'BNE'   : '1100011',
    'BLT'   : '1100011',
    'BGE'   : '1100011',
    'BLTU'  : '1100011',
    'BGEU'  : '1100011',
    'LB'    : '0000011',
    'LH'    : '0000011',
    'LW'    : '0000011',
    'LBU'   : '0000011',
    'LHU'   : '0000011',
    'SB'    : '0100011',
    'SH'    : '0100011',
    'SW'    : '0100011',
    'ADDI'  : '0010011',
    'SLTI'  : '0010011',
    'SLTIU' : '0010011',
    'XORI'  : '0010011',
    'ORI'   : '0010011',
    'ANDI'  : '0010011',
    'SLLI'  : '0010011',
    'SRLI'  : '0010011',
    'SRAI'  : '0010011',
    'ADD'   : '0110011',
    'SUB'   : '0110011',
    'SLL'   : '0110011',
    'SLT'   : '0110011',
    'SLTU'  : '0110011',
    'XOR'   : '0110011',
    'SRL'   : '0110011',
    'SRA'   : '0110011',
    'OR'    : '0110011',
    'AND'   : '0110011'
}

funct3_map = {
    'ADD' : '000', 'SUB' : '000', 'SLL'  : '001', 'SLT' : '010', 'SLTU': '011',
    'XOR' : '100', 'SRL' : '101', 'SRA'  : '101', 'OR'  : '110', 'AND' : '111',
    'ADDI': '000', 'SLTI': '010', 'SLTIU': '011', 'XORI': '100', 'ORI' : '110',
    'ANDI': '111', 'SLLI': '001', 'SRLI' : '101', 'SRAI': '101',
    'BEQ' : '000', 'BNE' : '001', 'BLT'  : '100', 'BGE' : '101', 'BLTU': '110', 'BGEU': '111',
    'SB'  : '000', 'SH'  : '001', 'SW'   : '010'
}

funct7_map = {
    'ADD' : '0000000', 'SUB': '0100000', 'SLL': '0000000', 'SLT': '0000000',
    'SLTU': '0000000', 'XOR': '0000000', 'SRL': '0000000', 'SRA': '0100000',
    'OR'  : '0000000', 'AND': '0000000'
}

# Function to convert R-type instructions to binary
def r_type_to_bin(instr):
    parts = instr.split()
    opcode = opcode_map[parts[0]]
    rd = format(int(parts[1][1:]), '05b')
    rs1 = format(int(parts[2][1:]), '05b')
    rs2 = format(int(parts[3][1:]), '05b')
    funct3 = funct3_map[parts[0]]
    funct7 = funct7_map.get(parts[0], '0000000')
    return funct7 + " " + rs2 + " " + rs1 + " " + funct3 + " " + rd + " " + opcode

# Function to convert I-type instructions to binary
def i_type_to_bin(instr):
    parts = instr.split()
    opcode = opcode_map[parts[0]]
    rd = format(int(parts[1][1:]), '05b')
    rs1 = format(int(parts[2][1:]), '05b')
    imm = format(int(parts[3]), '012b')
    funct3 = funct3_map[parts[0]]
    return imm + " " + rs1 + " " + funct3 + " " + rd + " " + opcode

# Function to convert S-type instructions to binary
def s_type_to_bin(instr):
    parts = instr.split()
    opcode = opcode_map[parts[0]]
    
    # Use regex to extract rs2, offset, and rs1
    match = re.match(r'(\w+)\s+x(\d+),\s*(-?\d+)\(x(\d+)\)', instr)
    if not match:
        raise ValueError(f"Instruction format not recognized: {instr}")
    
    rs2 = format(int(match.group(2)), '05b')
    offset = int(match.group(3))
    rs1 = format(int(match.group(4)), '05b')
    
    imm = format(offset & 0xFFF, '012b')  # 12-bit immediate
    imm_11_5 = imm[:7]  # bits [11:5]
    imm_4_0 = imm[7:]   # bits [4:0]
    funct3 = funct3_map[parts[0]]
    return imm_11_5 + " " + rs2 + " " + rs1 + " " + funct3 + " " + imm_4_0 + " " + opcode

# Function to convert B-type instructions to binary
def b_type_to_bin(instr):
    parts = instr.split()
    opcode = opcode_map[parts[0]]
    rs1 = format(int(parts[1][1:]), '05b')
    rs2 = format(int(parts[2][1:]), '05b')
    imm = format(int(parts[3]), '013b')
    imm_12 = imm[0]
    imm_10_5 = imm[1:7]
    imm_4_1 = imm[8:12]
    imm_11 = imm[12]
    funct3 = funct3_map[parts[0]]
    return imm_12 + " " + imm_10_5 + " " + rs2 + " " + rs1 + " " + funct3 + " " + imm_4_1 + " " + imm_11 + " " + opcode

# Function to convert U-type instructions to binary
def u_type_to_bin(instr):
    parts = instr.split()
    opcode = opcode_map[parts[0]]
    rd = format(int(parts[1][1:]), '05b')
    imm = format(int(parts[2]), '020b')
    return imm + " " + rd + " " + opcode

# Function to convert J-type instructions to binary
def j_type_to_bin(instr):
    parts = instr.split()
    opcode = opcode_map[parts[0]]
    rd = format(int(parts[1][1:]), '05b')
    imm = format(int(parts[2]), '021b')
    imm_20 = imm[0]
    imm_10_1 = imm[10:20]
    imm_11 = imm[10]
    imm_19_12 = imm[0:8]
    return imm_20 + " " + imm_10_1 + " " + imm_11 + " " + imm_19_12 + " " + rd + " " + opcode

# Example usage
instructions = [
    'ADD x1 x2 x3',
    'ADDI x1 x2 5',
    'SW x1, 10(x2)',
    'BEQ x1 x2 20',
    'LUI x1 1000',
    'JAL x1 500'
]

for instr in instructions:
    parts = instr.split()
    instr_type = parts[0]
    if instr_type in ['ADD', 'SUB', 'SLL', 'SLT', 'SLTU', 'XOR', 'SRL', 'SRA', 'OR', 'AND']:
        print(f"{instr} -> {r_type_to_bin(instr)}")
    elif instr_type in ['ADDI', 'SLTI', 'SLTIU', 'XORI', 'ORI', 'ANDI', 'SLLI', 'SRLI', 'SRAI']:
        print(f"{instr} -> {i_type_to_bin(instr)}")
    elif instr_type in ['SB', 'SH', 'SW']:
        print(f"{instr} -> {s_type_to_bin(instr)}")
    elif instr_type in ['BEQ', 'BNE', 'BLT', 'BGE', 'BLTU', 'BGEU']:
        print(f"{instr} -> {b_type_to_bin(instr)}")
    elif instr_type in ['LUI', 'AUIPC']:
        print(f"{instr} -> {u_type_to_bin(instr)}")
    elif instr_type in ['JAL', 'JALR']:
        print(f"{instr} -> {j_type_to_bin(instr)}")



 
import re

# Register map
register_map = {
    'zero': 'x0', 'ra': 'x1', 'sp': 'x2', 'gp': 'x3', 'tp': 'x4',
    't0': 'x5', 't1': 'x6', 't2': 'x7', 's0': 'x8', 'fp': 'x8', 's1': 'x9',
    'a0': 'x10', 'a1': 'x11', 'a2': 'x12', 'a3': 'x13', 'a4': 'x14', 'a5': 'x15',
    'a6': 'x16', 'a7': 'x17', 's2': 'x18', 's3': 'x19', 's4': 'x20', 's5': 'x21',
    's6': 'x22', 's7': 'x23', 's8': 'x24', 's9': 'x25', 's10': 'x26', 's11': 'x27',
    't3': 'x28', 't4': 'x29', 't5': 'x30', 't6': 'x31'
}

# Secondary names map
secondary_names = {
    'fp': 's0'
}

def decode_register(register):
    # Check if it's in the register map
    if register in register_map:
        return register_map[register]
    # Check if it's in the secondary names map
    elif register in secondary_names:
        return register_map[secondary_names[register]]
    else:
        return register

def decode_instruction(instr):
    # Split the instruction into parts
    parts = re.split(r'(\W+)', instr)
    
    # Decode each part
    decoded_parts = [decode_register(part) for part in parts]
    
    # Reassemble the instruction
    return ''.join(decoded_parts)

# Test the function with example instructions
instructions = [
    'SLLI ra sp 1',     # I-type (shift)
    'SRLI s1 t1 2',     # I-type (shift)
    'SRAI a1 zero 3',   # I-type (shift)
    'LW s0 100(a0)',    # I-type (load)
    'SW t0 200(gp)',    # S-type (store)
    'ADD fp t1 t2'      # R-type
]

for instr in instructions:
    print(f"{instr} -> {decode_instruction(instr)}")


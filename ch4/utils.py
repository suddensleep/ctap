def bin_str_to_int(bin_str):
    return int(bin_str, base=2)

def int_to_bin_str(i, places=None):
    bin_str = bin(i)[2:]
    while len(bin_str) % 4 != 0:
        bin_str = '0' + bin_str
    if places:
        bin_str = bin_str.zfill(places)
    return bin_str

def bin_str_to_hex_str(bin_str, places=None):
    hex_str = ''
    while len(bin_str) % 4 != 0:
        bin_str = '0' + bin_str
    for i in range(len(bin_str) // 4):
        hex_str += hex(bin_str_to_int(bin_str[4*i:4*i+4]))[-1]
    if places:
        hex_str = hex_str.zfill(places)
    return hex_str

def hex_str_to_bin_str(hex_str, places=None):
    bin_str = ''
    for i in range(len(hex_str)):
        bin_str += int_to_bin_str(int(hex_str[i], base=16))
    if places:
        bin_str = bin_str.zfill(places)
    return bin_str

def int_to_hex_str(i, places=None):
    hex_str = hex(i)[2:]
    if places:
        hex_str = hex_str.zfill(places)
    return hex_str

def hex_str_to_int(hex_str):
    return int(hex_str, base=16)

def xor_bin_str(bs):
    xor = bs[0]
    for i in range(1, len(bs)):
        xor = int_to_bin_str(
            bin_str_to_int(bs[i]) ^ bin_str_to_int(xor),
            places=len(bs[0])
        )
    return xor

def xor_hex_str(hs):
    xor = hs[0]
    for i in range(1, len(hs)):
        xor = int_to_hex_str(
            hex_str_to_int(hs[i]) ^ hex_str_to_int(xor),
            places=len(hs[0]))
    return xor


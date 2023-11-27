import random

from spn import SPN
from utils import *

s_box = {
    "0": "8", "1": "4", "2": "2", "3": "1",
    "4": "c", "5": "6", "6": "3", "7": "d",
    "8": "a", "9": "5", "a": "e", "b": "7",
    "c": "f", "d": "b", "e": "9", "f": "0"
}

p_box = {
    1: 1, 2: 5, 3: 9, 4: 13,
    5: 2, 6: 6, 7: 10, 8: 14,
    9: 3, 10: 7, 11: 11, 12: 15,
    13: 4, 14: 8, 15: 12, 16: 16
}

K = [
    int_to_bin_str(random.randint(0, 2**16 - 1), places=16),
    int_to_bin_str(random.randint(0, 2**16 - 1), places=16),
    int_to_bin_str(random.randint(0, 2**16 - 1), places=16),
    int_to_bin_str(random.randint(0, 2**16 - 1), places=16),
    int_to_bin_str(random.randint(0, 2**16 - 1), places=16)
]

s = SPN(s_box=s_box, p_box=p_box, K=K)

# get ~8K pt/ct pairs
T = []
for _ in range(1500):
    pt = int_to_hex_str(random.randint(0, 2**16 - 1), places=4)
    ct = s.encrypt(pt)
    T.append((pt, ct))

key_count = {int_to_hex_str(kk, places=2): 0 for kk in range(256)}

for (pt, ct) in T:
    x__4 = hex_str_to_bin_str(pt[3])
    x_16 = x__4[3]
    for kk in key_count:
        v_4__1 = xor_hex_str([kk[0], ct[0]])
        v_4__3 = xor_hex_str([kk[1], ct[2]])
        u_4__1 = hex_str_to_bin_str(s.s_box_inv[v_4__1])
        u_4__3 = hex_str_to_bin_str(s.s_box_inv[v_4__3])
        u_4_1 = u_4__1[0]
        u_4_9 = u_4__3[0]
        z = xor_bin_str([x_16, u_4_1, u_4_9])
        if bin_str_to_int(z) == 0:
            key_count[kk] += 1

max = -1
max_key = ''

for kk in key_count:
    key_count[kk] = abs(key_count[kk] - len(T) / 2)
    if key_count[kk] > max:
        max = key_count[kk]
        max_key = kk

print(max_key)
print(
    ''.join(
        [bin_str_to_hex_str(K[-1][0:4]), bin_str_to_hex_str(K[-1][8:12])]
    )
)

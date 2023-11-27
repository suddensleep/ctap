import random

from spn import SPN
from utils import *

s_box = {
    "0": "e", "1": "2", "2": "1", "3": "3",
    "4": "d", "5": "9", "6": "0", "7": "6",
    "8": "f", "9": "4", "a": "5", "b": "a",
    "c": "8", "d": "c", "e": "7", "f": "b"
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

# get ~1K pt/ct pair
x_prime = bin_str_to_hex_str("1001000000001001")
T = []
for _ in range(1000):
    x = int_to_hex_str(random.randint(0, 2**16 - 1), places=4)
    x_star = xor_hex_str([x, x_prime])
    y = s.encrypt(x)
    y_star = s.encrypt(x_star)
    T.append((x, y, x_star, y_star))

key_count = {int_to_hex_str(kk, places=2): 0 for kk in range(256)}

for (x, y, x_star, y_star) in T:
    if y[2] == y_star[2] and y[3] == y_star[3]:
        for kk in key_count:
            v_4__1 = xor_hex_str([kk[0], y[0]])
            v_4__1_star = xor_hex_str([kk[0], y_star[0]])
            v_4__2 = xor_hex_str([kk[1], y[1]])
            v_4__2_star = xor_hex_str([kk[1], y_star[1]])
            u_4__1 = hex_str_to_bin_str(s.s_box_inv[v_4__1])
            u_4__1_star = hex_str_to_bin_str(s.s_box_inv[v_4__1_star])
            u_4__2 = hex_str_to_bin_str(s.s_box_inv[v_4__2])
            u_4__2_star = hex_str_to_bin_str(s.s_box_inv[v_4__2_star])
            u_4__1_prime = xor_bin_str([u_4__1, u_4__1_star])
            u_4__2_prime = xor_bin_str([u_4__2, u_4__2_star])
            if u_4__1_prime == "0001" and u_4__2_prime == "0001":
                key_count[kk] += 1

max = -1
max_key = ''

for kk in key_count:
    if key_count[kk] > max:
        max = key_count[kk]
        max_key = kk

print(max_key)
print(
    ''.join(
        [bin_str_to_hex_str(K[-1][0:4]), bin_str_to_hex_str(K[-1][8:12])]
    )
)

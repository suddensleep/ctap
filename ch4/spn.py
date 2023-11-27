from utils import *

class SPN():
    def __init__(self, L=4, M=4, N=4, s_box=None, p_box=None, K=None):
        self.L = L
        self.M = M
        self.block_length = self.L * self.M
        self.N = N
        if s_box:
            self.s_box = s_box
        else:
            self.s_box = {int_to_hex_str(i): int_to_hex_str(i)
                          for i in range(2**self.L)}
        self.s_box_inv = {self.s_box[key]: key for key in self.s_box}
        if p_box:
            self.p_box = p_box
        else:
            self.p_box = {i: i for i in range(1, self.block_length + 1)}
        if K:
            self.K = K
        else:
            self.K = ["0" * self.block_length] * (self.N + 1)
        try:
            self.assert_validity()
        except:
            raise ValueError("Invalid parameters.")

    def assert_validity(self):
        assert self.L > 0
        assert self.M > 0
        assert self.N > 0
        assert self.s_box.keys() == self.s_box_inv.keys()
        assert (sorted(list(self.p_box.keys())) ==
                sorted(list(self.p_box.values())))
        assert len(self.K) == self.N + 1
        for K_i in self.K:
            assert(len(K_i) == self.block_length)

    def encrypt(self, plaintext):
        plaintext = hex_str_to_bin_str(plaintext)
        try:
            assert len(plaintext) == self.block_length
        except:
            raise ValueError("Plaintext block is wrong length.")

        W = [plaintext]
        U = ['0'*self.block_length]
        V = ['0'*self.block_length]
        for i in range(1, self.N):
            U.append(xor_bin_str([W[-1], self.K[i - 1]]))
            vi = ''
            for j in range(self.M):
                vi += hex_str_to_bin_str(
                    self.s_box[
                        bin_str_to_hex_str(
                            U[-1][self.L*j:self.L*(j+1)]
                        )
                    ]
                )
            V.append(vi)
            W.append(
                ''.join(
                    V[-1][self.p_box[i+1]-1]
                    for i in range(self.block_length)
                )
            )
        U.append(xor_bin_str([W[-1], self.K[-2]]))
        vi = ''
        for j in range(self.M):
            vi += hex_str_to_bin_str(
                self.s_box[
                    bin_str_to_hex_str(
                        U[-1][self.L*j:self.L*(j+1)]
                    )
                ]
            )
        V.append(vi)
        y = xor_bin_str([V[-1], self.K[-1]])

        return bin_str_to_hex_str(y)

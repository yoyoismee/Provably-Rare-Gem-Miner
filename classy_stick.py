# Provably Rare Gem Miner
# love ya alpha team. <3
# by yoyoismee.eth

from Crypto.Hash import keccak
from eth_abi.packed import encode_abi_packed
import random
import time


class StickTheMiner:
    def __init__(self, chain_id, entropy, gemAddr, senderAddr, kind, nonce, diff):
        self.task = [chain_id, entropy, gemAddr, senderAddr, kind, nonce]
        self.target = 2 ** 256 / diff

    @staticmethod
    def pack_mine(chain_id, entropy, gemAddr, senderAddr, kind, nonce, salt) -> bytes:
        return encode_abi_packed(['uint256', 'bytes32', 'address', 'address', 'uint', 'uint', 'uint'],
                                 (chain_id, entropy, gemAddr, senderAddr, kind, nonce, salt))

    @staticmethod
    def mine(packed) -> (str, int):
        k = keccak.new(digest_bits=256)
        k.update(packed)
        hx = k.hexdigest()
        return hx, int(hx, base=16)

    @staticmethod
    def get_salt() -> int:
        return random.randint(1, 2 ** 123)  # can probably go to 256 but 123 probably enough

    def run(self):
        i = 0
        st = time.time()
        while True:
            i += 1
            salt = self.get_salt()
            # salt = i
            hx, ix = self.mine(self.pack_mine(*self.task, salt))

            if ix < self.target:
                print("done! here's the salt - ", salt)
                return salt

            if i % 5000 == 0:
                print(f'iter {i}, {i / (time.time() - st)} avg iter per sec')

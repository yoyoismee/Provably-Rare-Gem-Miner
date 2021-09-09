# Provably Rare Gem Miner
# love ya alpha team. <3
# by yoyoismee.eth

from Crypto.Hash import keccak
from eth_abi.packed import encode_abi_packed
import random
import time
from datetime import datetime, timedelta
from line_notify import LineNotify


class BasicDiffCallback:
    def __init__(self, contract, gem):
        self.contract = contract
        self.gem = gem

    def get_diff(self):
        _, _, _, difficulty, _, _, _, _, _ = self.contract.functions.gems(self.gem).call()
        return difficulty


class StickTheMiner:
    def __init__(self, chain_id, entropy, gemAddr, senderAddr, kind, nonce, diff, diff_callback=None, line_notify=None):
        self.task = [chain_id, entropy, gemAddr, senderAddr, kind, nonce]
        self.target = 2 ** 256 / diff
        self.diff_callback = diff_callback
        self.diff = diff
        self.line_notify = line_notify
        self.last_check = 0

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
        # can probably go to 256 but 123 probably enough
        return random.randint(1, 2 ** 123)

    def run(self):
        i = 0
        st = time.time()
        while True:
            i += 1
            salt = self.get_salt()
            # salt = i
            hx, ix = self.mine(self.pack_mine(*self.task, salt))

            if ix < self.target:
                template = "done! here's the salt - " + str(salt) + "\n"
                template += f'Elapsed: {str(timedelta(seconds=(time.time() - st)))}\n' + f'found on: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'

                print(template)
                if self.line_notify is not None:
                    self.line_notify.send(template)
                return salt

            if i % 5000 == 0:
                if self.diff_callback is not None:
                    if time.time() - self.last_check > 120:
                        self.diff = self.diff_callback.get_diff()
                        self.target = 2 ** 256 / self.diff
                        self.last_check = time.time()
                avg_it_sec = i / (time.time() - st)
                print(
                    f'iter {i}, {avg_it_sec} avg iter per sec, current diff {self.diff}, est mining time - {self.diff / avg_it_sec / 60 / 60} hrs')

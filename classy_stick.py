# Provably Rare Gem Miner
# love ya alpha team. <3
# by yoyoismee.eth

from Crypto.Hash import keccak
from eth_abi.packed import encode_abi_packed
import random
import time
from datetime import datetime, timedelta

class BasicDiffCallback:
    def __init__(self, contract, gem):
        self.contract = contract
        self.gem = gem

    def get_diff(self):
        _, _, _, difficulty, _, _, _, _, _ = self.contract.functions.gems(self.gem).call()
        return difficulty

class BasicNonceCallback:
    def __init__(self, contract, address):
        self.contract = contract
        self.address = address

    def get_nonce(self):
        nonce = self.contract.functions.nonce(self.address).call()
        # print("nonce - ", nonce)
        return nonce

class StickTheMiner:
    def __init__(self, chain_id, entropy, gemAddr, senderAddr, kind, nonce,
                 diff, diff_callback=None, nonce_callback=None, line_notify=None):
        self.task = [chain_id, entropy, gemAddr, senderAddr, kind, nonce]
        self.target = 2 ** 256 / diff
        self.diff_callback = diff_callback
        self.nonce_callback = nonce_callback
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
        return random.randint(1, 2 ** 256)
    
    def run(self, processNumber, saltQueue, itrQueue):
        i = 0
        st = time.time()
        if self.nonce_callback is not None:
            self.task[5] = self.nonce_callback.get_nonce()
        while saltQueue.empty() is True:
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
                saltQueue.put(salt)

            if i % 5000 == 0:
                if time.time() - self.last_check > 60:
                    if self.diff_callback is not None:
                        self.diff = self.diff_callback.get_diff()
                        self.target = 2 ** 256 / self.diff
                        self.last_check = time.time()
                    if self.nonce_callback is not None:
                        self.task[5] = self.nonce_callback.get_nonce()
                itr = itrQueue.get()
                totalItr = itr + i
                itrQueue.put(totalItr)
                i = 0
                avg_it_sec = totalItr / (time.time() - st)
                print(
                    f'{processNumber} iter {totalItr}, {avg_it_sec} avg iter per sec, current diff {self.diff}, est mining time - {self.diff / avg_it_sec / 60 / 60} hrs, time spent mining - {(time.time() - st) / 60} mins')
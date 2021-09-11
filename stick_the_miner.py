# Provably Rare Gem Miner
# love ya alpha team. <3
# by yoyoismee.eth

from Crypto.Hash import keccak
from eth_abi.packed import encode_abi_packed
from sys import platform
import random
import time
import logging, colorlog
import psutil
import os

SALTCOLORLEVEL = 1
RESULTCOLORLEVEL = 2

chain_id = 1  # eth main net who mine others chain for god sake // nah JK I think you know how to do chain ID
entropy = 0x949f147e5fb733f43d887bd3f9455dad768029a75baa8c63ec2d749439935d59  # loot / main net
# entropy = 0xe562c6985e1e24ea9e1b39595afc64ac6cee3a06f6f4402694a85f49a7986ba8 # bloot / main net
gemAddr = '0xC67DED0eC78b849e17771b2E8a7e303B4dAd6dD4'  # gem address (yeah at this point you should know what it is)
userAddr = '0x6647a7858a0B3846AbD5511e7b797Fc0a0c63a4b'  # your address. this is my address (where you can donate lol)
kind = 0  # which gem ya want (Loot, Amethyst = 0 Topaz = 1 ... for Bloot Violet=10, Goldy Pebble =1 ...)
nonce = 0  # how greedy are you? JK (you can read from contract or FE)
diff = 1  # just read from the contract or front end

target = 2 ** 256 / diff

def setup_logger():
    logging.addLevelName(RESULTCOLORLEVEL, 'RESULT')
    logging.addLevelName(SALTCOLORLEVEL, 'SALT')

    formatter = colorlog.ColoredFormatter("%(log_color)s%(levelname)-8s%(reset)s %(message_log_color)s%(message)s",
    log_colors={'RESULT': 'cyan' ,'SALT': 'blue'},
    secondary_log_colors={
		'message': {
			'RESULT':    'cyan',
			'SALT':    'white,bg_blue',
		}
	})
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel('RESULT')
    logger.setLevel('SALT')

    return logger

def pack_mine(chain_id, entropy, gemAddr, senderAddr, kind, nonce, salt) -> bytes:
    return encode_abi_packed(['uint256', 'uint256', 'address', 'address', 'uint', 'uint', 'uint'],
                             (chain_id, entropy, gemAddr, senderAddr, kind, nonce, salt))


def mine(packed) -> (str, int):
    k = keccak.new(digest_bits=256)
    k.update(packed)
    hx = k.hexdigest()
    return hx, int(hx, base=16)

def get_salt() -> int:
    return random.randint(1, 2 ** 123)  # can probably go to 256 but 123 probably enough

core = psutil.Process(os.getpid())
if platform == "win32":
    core.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
elif platform == "darwin":
    core.nice(10)
logger = setup_logger()
i = 0
st = time.time()
while True:
    i += 1
    salt = get_salt()
    # salt = i
    hx, ix = mine(pack_mine(chain_id, entropy, gemAddr, userAddr, kind, nonce, salt))

    if ix < target:
        logger.log(RESULTCOLORLEVEL, "done! here's the salt")
        logger.log(SALTCOLORLEVEL,str(salt))
        break

    if i % 5000 == 0:
        print(f'iter {i}, {i / (time.time() - st)} avg iter per sec')

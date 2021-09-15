# Provably Rare Gem Miner
# love ya alpha team. <3
# by yoyoismee.eth

from Crypto.Hash import keccak
from eth_abi.packed import encode_abi_packed
import random
import time
import multiprocessing
import logging, colorlog
import psutil
import os

SALTCOLORLEVEL = 101
RESULTCOLORLEVEL = 102

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

chain_id = 250  # eth main net who mine others chain for god sake // nah JK I think you know how to do chain ID
entropy = 0x000085f6000009b52c33cc14d29bc7c7ce21664517b167ed086a8cbc272f435f  # loot / main net
# entropy = 0xe562c6985e1e24ea9e1b39595afc64ac6cee3a06f6f4402694a85f49a7986ba8 # bloot / main net
gemAddr = '0x342EbF0A5ceC4404CcFF73a40f9c30288Fc72611'  # gem address (yeah at this point you should know what it is)
userAddr = '0x6647a7858a0B3846AbD5511e7b797Fc0a0c63a4b'  # your address. this is my address (where you can donate lol)
kind = 5  # which gem ya want (Loot, Amethyst = 0 Topaz = 1 ... for Bloot Violet=10, Goldy Pebble =1 ...)
nonce = 13  # how greedy are you? JK (you can read from contract or FE)
diff = 158053436  # just read from the contract or front end

targetValue = 2 ** 256 / diff


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


def multiprocessing_gems(processNumber, saltQueue, itrQueue):
    logger = setup_logger()
    i = 0
    st = time.time()
    while saltQueue.empty() is True:
        i += 1
        salt = get_salt()
        hx, ix = mine(pack_mine(chain_id, entropy, gemAddr, userAddr, kind, nonce, salt))
        if ix < targetValue:
            # logger.critical("done! here's the salt - " )
            logger.log(RESULTCOLORLEVEL, "done! here's the salt")
            logger.log(SALTCOLORLEVEL,str(salt))

            
            print('That took {} seconds'.format(time.time() - st))
            saltQueue.put(salt)

        if i % 5000 == 0:
            itr = itrQueue.get()
            totalItr = itr + i
            itrQueue.put(totalItr)
            i = 0
            print(f'process {processNumber} iter {totalItr}, {totalItr / (time.time() - st)} avg iter per sec')
            if totalItr % 100000 == 0:
                logger.log(RESULTCOLORLEVEL, 'time elapsed {}'.format(time.time() - st))



if __name__ == '__main__':
    # st = time.time()
    processes = []
    saltQueue = multiprocessing.Queue()
    itrQueue = multiprocessing.Queue()
    itrQueue.put(0)
    coreNumber = 16
    for i in range(coreNumber):
        p = multiprocessing.Process(target=multiprocessing_gems, args=(i, saltQueue,itrQueue))
        core = psutil.Process(os.getpid())
        core.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    
        # salt = i
    
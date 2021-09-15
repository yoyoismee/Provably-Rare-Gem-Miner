# Provably Rare Gem Miner auto version
# love ya alpha team. <3
# by yoyoismee.eth
# use at your own risk
# only work with eth for now

import multiprocessing
import psutil
from web3 import Web3
import not_classy_stick
import os
from dotenv import load_dotenv
import requests
from add_log_color import LogColor

load_dotenv()

# change wallet here or in .env
WALLET_ADDRESS = os.getenv('WALLET_ADDRESS', 'DEFAULT_WALLET')
# change influra api key here or in .env
TARGET_GEM = int(os.getenv('TARGET_GEM', 1))  # change gem here or in .env

# config here
w3 = Web3(Web3.HTTPProvider('https://rpc.ftm.tools'))
your_address = WALLET_ADDRESS  # my address don't use it.
target_gem = TARGET_GEM  # gem type

# Line notification
NOTIFY_AUTH_TOKEN = os.getenv('NOTIFY_AUTH_TOKEN', '')
notify_url = 'https://notify-api.line.me/api/notify'
notify_headers = {'Authorization': 'Bearer ' + NOTIFY_AUTH_TOKEN}

# print('Your wallet', WALLET_ADDRESS)
# print('Gem', TARGET_GEM)

# glhf - no need to change
gem_addr = "0x342EbF0A5ceC4404CcFF73a40f9c30288Fc72611"  # fantom
gem_abi = """[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"kind","type":"uint256"}],"name":"Create","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"miner","type":"address"},{"indexed":true,"internalType":"uint256","name":"kind","type":"uint256"}],"name":"Mine","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"indexed":false,"internalType":"uint256[]","name":"values","type":"uint256[]"}],"name":"TransferBatch","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"TransferSingle","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"value","type":"string"},{"indexed":true,"internalType":"uint256","name":"id","type":"uint256"}],"name":"URI","type":"event"},{"inputs":[{"internalType":"uint256[]","name":"kinds","type":"uint256[]"}],"name":"acceptManager","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"accounts","type":"address[]"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"}],"name":"balanceOfBatch","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"kind","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"to","type":"address"}],"name":"craft","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"color","type":"string"},{"internalType":"uint256","name":"difficulty","type":"uint256"},{"internalType":"uint256","name":"gemsPerMine","type":"uint256"},{"internalType":"uint256","name":"multiplier","type":"uint256"},{"internalType":"address","name":"crafter","type":"address"},{"internalType":"address","name":"manager","type":"address"}],"name":"create","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"name":"exists","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"gemCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"gems","outputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"color","type":"string"},{"internalType":"bytes32","name":"entropy","type":"bytes32"},{"internalType":"uint256","name":"difficulty","type":"uint256"},{"internalType":"uint256","name":"gemsPerMine","type":"uint256"},{"internalType":"uint256","name":"multiplier","type":"uint256"},{"internalType":"address","name":"crafter","type":"address"},{"internalType":"address","name":"manager","type":"address"},{"internalType":"address","name":"pendingManager","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_maxGemCount","type":"uint256"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"kind","type":"uint256"},{"internalType":"uint256","name":"salt","type":"uint256"}],"name":"luck","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxGemCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"kind","type":"uint256"},{"internalType":"uint256","name":"salt","type":"uint256"}],"name":"mine","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonce","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"kinds","type":"uint256[]"}],"name":"renounceManager","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeBatchTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_maxGemCount","type":"uint256"}],"name":"setMaxGemCount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"kinds","type":"uint256[]"},{"internalType":"address","name":"to","type":"address"}],"name":"transferManager","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_owner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"kinds","type":"uint256[]"},{"internalType":"address","name":"crafter","type":"address"}],"name":"updateCrafter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"kind","type":"uint256"},{"internalType":"bytes32","name":"entropy","type":"bytes32"}],"name":"updateEntropy","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"kind","type":"uint256"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"color","type":"string"}],"name":"updateGemInfo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"kind","type":"uint256"},{"internalType":"uint256","name":"difficulty","type":"uint256"},{"internalType":"uint256","name":"multiplier","type":"uint256"},{"internalType":"uint256","name":"gemsPerMine","type":"uint256"}],"name":"updateMiningData","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"kind","type":"uint256"}],"name":"uri","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]"""
gem_contract = w3.eth.contract(address=gem_addr, abi=gem_abi )

name, color, entropy, difficulty, gemsPerMine, multiplier, crafter, manager, pendingManager = \
    gem_contract.functions.gems(target_gem).call()

nonce = gem_contract.functions.nonce(your_address).call()
chain_id = 250  # fantom

# gem_contract_dict = {}
coreNumber = 8

    
# for x in range (10):
#     gem_contract_dict["gem_contract_{num}".format(num=x)] = w3.eth.contract(address=gem_addr, abi=gem_abi )
# Start mining
# for j in range(len(gem_contract_dict)):
#     print(gem_contract_dict["gem_contract_{num}".format(num=j)])
def mine(coreNumber,saltQueue,itrQueue):
    diff_result = not_classy_stick.BasicDiffCallback(gem_contract, target_gem)
    nonce_result = not_classy_stick.BasicNonceCallback(contract=gem_contract, address=your_address)
    stick = not_classy_stick.StickTheMiner(chain_id, entropy, gem_addr,
                    your_address, target_gem, nonce, difficulty,
                    diff_callback=diff_result,
                    nonce_callback=nonce_result)
    stick.run(coreNumber,saltQueue,itrQueue)

if __name__ == '__main__':
    loggerOBJ = LogColor()
    logger = loggerOBJ.setup_logger()

    if NOTIFY_AUTH_TOKEN != '':
        body = {
            'message': '👷🏼‍♂️⛏Starting gem mining...'
                    + '\nkind: ' + str(target_gem)
                    + '\nwallet: ' + your_address
                    + '\nnonce: ' + str(nonce)
                    + '\ndifficulty: ' + str(difficulty)
        }

        res = requests.post(notify_url, data=body, headers=notify_headers)
        print("Start result notified:", res.text)

    diff_value = not_classy_stick.BasicDiffCallback(gem_contract, target_gem).get_diff()
    nonce_value = not_classy_stick.BasicNonceCallback(gem_contract, your_address).get_nonce()
    logger.log(loggerOBJ.get_diff(), str(diff_value))
    logger.log(loggerOBJ.get_nonce(), str(nonce_value))
   
    processes = []
    saltQueue = multiprocessing.Queue()
    itrQueue = multiprocessing.Queue()
    itrQueue.put(0)
   
    for i in range(coreNumber):
        p = multiprocessing.Process(target=mine,args=(i,saltQueue,itrQueue))
        core = psutil.Process(os.getpid())
        core.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    if NOTIFY_AUTH_TOKEN != '':
        body = {
            'message': '💎Gem found'
                    + '\nkind: ' + str(target_gem)
                    + '\nwallet: ' + your_address
                    + '\nnonce: ' + str(nonce)
                    + '\ndifficulty: ' + str(difficulty)
                    + '\nsalt: ' + str(saltQueue.get())
        }
        res = requests.post(notify_url, data=body, headers=notify_headers)
        print("End result notified:", res.text)

    """
    private_key = "" # use at your own risk
    gas = None # pick a number
    transaction = gem_contract.functions.mine(target_gem, salt).buildTransaction()
    transaction.update({'gas': gas})
    transaction.update({'nonce': w3.eth.get_transaction_count('Your_Wallet_Address')})
    signed_tx = w3.eth.account.sign_transaction(transaction, private_key)
    """

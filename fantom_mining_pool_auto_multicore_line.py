# Provably Rare Gem Miner auto version
# love ya alpha team. <3
# by yoyoismee.eth
# use at your own risk
# only work with eth for now

import multiprocessing
import not_classy_stick
import os
import requests
import psutil
import time
import atexit
from dotenv import load_dotenv
from add_log_color import LogColor
from sys import platform
from web3 import Web3

load_dotenv()
# config here
TARGET_GEM = int(os.getenv('TARGET_GEM', 1))  # change gem here or in .env

w3 = Web3(Web3.HTTPProvider('https://rpc.ftm.tools'))
target_gem = TARGET_GEM  # gem type
WALLET_ADDRESS = str(os.getenv('WALLET_ADDRESS', ''))
PRIVATE_KEY = str(os.getenv('PRIVATE_KEY', ''))
# your target diff level, will submit result to the pool if salt reach target quality. note that submit salt will cost gas.
difficulty = 50000000

pool_addr = "0x7558cF0c0Dfc21b30D5012586492aEA49fE1c27d"  # pool address
pool_abi = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[{"internalType":"uint256","name":"kind","type":"uint256"},{"internalType":"address","name":"wrapAddress","type":"address"},{"internalType":"string","name":"HPName","type":"string"},{"internalType":"string","name":"HPSymbol","type":"string"},{"internalType":"uint256","name":"bonus","type":"uint256"}],"name":"addGem","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"kind","type":"uint256"}],"name":"gems","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"bytes32","name":"","type":"bytes32"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"gemsMap","outputs":[{"internalType":"bool","name":"exist","type":"bool"},{"internalType":"uint256","name":"kind","type":"uint256"},{"internalType":"address","name":"wrapAddress","type":"address"},{"internalType":"contract HPToken","name":"hptoken","type":"address"},{"internalType":"uint256","name":"bonus","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"kind","type":"uint256"},{"internalType":"uint256","name":"salt","type":"uint256"}],"name":"mine","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"notInUse","type":"address"}],"name":"nonce","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"address","name":"from","type":"address"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"internalType":"uint256[]","name":"values","type":"uint256[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"onERC1155BatchReceived","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"address","name":"from","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"onERC1155Received","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"kind","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
pool_contract = w3.eth.contract(address=pool_addr, abi=pool_abi)

# Line notification
NOTIFY_AUTH_TOKEN = os.getenv('NOTIFY_AUTH_TOKEN', '')
notify_url = 'https://notify-api.line.me/api/notify'
notify_headers = {'Authorization': 'Bearer ' + NOTIFY_AUTH_TOKEN}

# glhf - no need to change
gem_addr = "0x342EbF0A5ceC4404CcFF73a40f9c30288Fc72611"  # fantom gem
gem_abi = """[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"kind","type":"uint256"}],"name":"Create","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"miner","type":"address"},{"indexed":true,"internalType":"uint256","name":"kind","type":"uint256"}],"name":"Mine","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"indexed":false,"internalType":"uint256[]","name":"values","type":"uint256[]"}],"name":"TransferBatch","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"id","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"TransferSingle","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"value","type":"string"},{"indexed":true,"internalType":"uint256","name":"id","type":"uint256"}],"name":"URI","type":"event"},{"inputs":[{"internalType":"uint256[]","name":"kinds","type":"uint256[]"}],"name":"acceptManager","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"accounts","type":"address[]"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"}],"name":"balanceOfBatch","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"kind","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"to","type":"address"}],"name":"craft","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"color","type":"string"},{"internalType":"uint256","name":"difficulty","type":"uint256"},{"internalType":"uint256","name":"gemsPerMine","type":"uint256"},{"internalType":"uint256","name":"multiplier","type":"uint256"},{"internalType":"address","name":"crafter","type":"address"},{"internalType":"address","name":"manager","type":"address"}],"name":"create","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"name":"exists","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"gemCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"gems","outputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"color","type":"string"},{"internalType":"bytes32","name":"entropy","type":"bytes32"},{"internalType":"uint256","name":"difficulty","type":"uint256"},{"internalType":"uint256","name":"gemsPerMine","type":"uint256"},{"internalType":"uint256","name":"multiplier","type":"uint256"},{"internalType":"address","name":"crafter","type":"address"},{"internalType":"address","name":"manager","type":"address"},{"internalType":"address","name":"pendingManager","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_maxGemCount","type":"uint256"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"kind","type":"uint256"},{"internalType":"uint256","name":"salt","type":"uint256"}],"name":"luck","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxGemCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"kind","type":"uint256"},{"internalType":"uint256","name":"salt","type":"uint256"}],"name":"mine","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonce","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"kinds","type":"uint256[]"}],"name":"renounceManager","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256[]","name":"ids","type":"uint256[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeBatchTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_maxGemCount","type":"uint256"}],"name":"setMaxGemCount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"kinds","type":"uint256[]"},{"internalType":"address","name":"to","type":"address"}],"name":"transferManager","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_owner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"kinds","type":"uint256[]"},{"internalType":"address","name":"crafter","type":"address"}],"name":"updateCrafter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"kind","type":"uint256"},{"internalType":"bytes32","name":"entropy","type":"bytes32"}],"name":"updateEntropy","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"kind","type":"uint256"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"color","type":"string"}],"name":"updateGemInfo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"kind","type":"uint256"},{"internalType":"uint256","name":"difficulty","type":"uint256"},{"internalType":"uint256","name":"multiplier","type":"uint256"},{"internalType":"uint256","name":"gemsPerMine","type":"uint256"}],"name":"updateMiningData","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"kind","type":"uint256"}],"name":"uri","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]"""
gem_contract = w3.eth.contract(address=gem_addr, abi=gem_abi)

name, color, entropy, _, gemsPerMine, multiplier, crafter, manager, pendingManager = \
    gem_contract.functions.gems(target_gem).call()
nonce = gem_contract.functions.nonce(pool_addr).call()

chain_id = 250  # ftm
#number of core for processing, the higher the faster, but shouldn't exceed ˜16 cores 
coreNumber = 8

def mine(coreNumber, saltQueue, itrQueue):
    # diff_result = not_classy_stick.BasicDiffCallback(gem_contract, TARGET_GEM)
    nonce_result = not_classy_stick.BasicNonceCallback(contract=gem_contract, address=pool_addr)
    stick = not_classy_stick.StickTheMiner(chain_id, entropy, gem_addr,
                            pool_addr, target_gem, nonce, difficulty,
                            nonce_callback=nonce_result)
    stick.run(coreNumber, saltQueue, itrQueue)

if __name__ == '__main__':

    #setting up logger for colored output
    loggerOBJ = LogColor()
    logger = loggerOBJ.setup_logger()

    if NOTIFY_AUTH_TOKEN != '':
        body = {
            'message': '🌊Gem pool mining👷🏼‍♂️👷🏼‍♀️⛏...'
                    + '\nkind: ' + str(target_gem)
                    + '\nwallet: ' + pool_addr
                    + '\nnonce: ' + str(nonce)
                    + '\ndifficulty: ' + str(difficulty)
        }

        res = requests.post(notify_url, data=body, headers=notify_headers)
        print("Start result notified:", res.text)
    
    print('Pool address ', pool_addr)
    print('Gem', TARGET_GEM)

    mining_itr = 0

    #send Line noti when exiting the program
    @atexit.register
    def terminate_program():
        if NOTIFY_AUTH_TOKEN != '':
            body = {
                'message': '❌Gem pool mining is closed....❌'
            }
            res = requests.post(notify_url, data=body, headers=notify_headers)
            print("❌Gem pool mining is closed...❌", res.text)

    while True:
        # Start mining
        st = time.time()
        processes = []
        saltQueue = multiprocessing.Queue()
        itrQueue = multiprocessing.Queue()
        itrQueue.put(0)

        for i in range(coreNumber):
            p = multiprocessing.Process(target=mine, args=(i,saltQueue,itrQueue))
            core = psutil.Process(os.getpid())

            #decreased the priority of the process to reduced computer lags
            if(platform=="win32"):
                core.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
            elif(platform=="darwin"):
                core.nice(10)
            processes.append(p)
            p.start()
        
        for process in processes:
            process.join()

        salt = saltQueue.get()
        
        if NOTIFY_AUTH_TOKEN != '':
            body = {
                'message': '💎Iteration ' + str(mining_itr+1) + ' finished....'
                        + '\nkind: ' + str(target_gem)
                        + '\nwallet: ' + pool_addr
                        + '\nnonce: ' + str(nonce)
                        + '\ntime spent this itr: ' + str("{:.2f}".format((time.time() - st) / 60)) + ' mins'
                        + '\ndifficulty: ' + str(difficulty)
                        + '\nsalt: ' + str(salt)
            }
            res = requests.post(notify_url, data=body, headers=notify_headers)
            print("End result notified:", res.text)

        print("📤Submitting tx...")
        gas = w3.eth.gasPrice  # pick a number
        transaction = pool_contract.functions.mine(target_gem, salt).buildTransaction({
            'from': WALLET_ADDRESS,
            'gasPrice': gas,
            "gas": 300000,
            'nonce': w3.eth.get_transaction_count(WALLET_ADDRESS),
        })
        # private_key, use at your own risk
        signed_tx = w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
        ticket = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(w3.eth.wait_for_transaction_receipt(ticket))
        mining_itr += 1
        print("💎done - ", mining_itr, " times!")
        
   
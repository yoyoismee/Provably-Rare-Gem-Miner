# Provably Rare Gem Miner

### just another random project by yoyoismee.eth

useful link

- [main site](https://gems.alphafinance.io/#/loot)
- [market](https://opensea.io/collection/provably-rare-gem)
- [contract](https://etherscan.io/address/0xC67DED0eC78b849e17771b2E8a7e303B4dAd6dD4)

useful thing you should know

- read contract -> gems(gemID) to get useful info
- write contract -> mine to claim(kind, salt) to claim your NFT

to run. just edit the python file and run it.

```
pip install -r requirement.txt
python3 stick_the_miner.py
```

or new one `auto_mine.py` for less input. but you'll need [infura account](https://infura.io/)



Ps. too lazy to write docs. but it's 50 LoCs have fun.  

---
why stick the miner ? welp.. this is part of the [stick the BUIDLer](https://opensea.io/collection/stick-the-buidler) series. 

TL;DR - I'm working on a series of opensource NFT related project just for fun. 



### Key parameters to change if you are using orginal version 'stick_the_miner.py' (cr. K Nattakit's FB post)

- chain_id - eth:1, fantom:250
- entropy - ??
- gemAddr - Game address, can get from https://gems.alphafinance.io/ (loot/bloot/rarity)
- userAddr - your Wallet address 
- kind = ประเภทของเพชรที่จะขุด ผมแนะนำเป็น Emerald เพราะ return/difficult สูงที่สุด ง่าย ๆ คือคุณจะกำไรเร็วกว่านั่นเอง
- nonce - number of times you've minted a gem (https://gems.alphafinance.io/ and connect your wallet)
- diff - difficulty of gemID (https://gems.alphafinance.io/), note that this changes everytime someone minted that gem, so you need to change it too 


### (more detail) how to use 'auto_mine.py', the updated version of stick_the_miner

- benefits: manual version (stick_the_miner.py) requires you to update the 'diff' parameter every time someone minted the nft of the target gem, and 'nounce' if you successfully minted one. This version automates that so you just have to rerun to update.
- steps:
- 1. update requirements ``` pip install -r requirement.txt ```
- 2. create an account at (https://infura.io/), select your chain (e.g. Ethereum), create a project and obtain your project ID
- 3. create a .env file in the same format as .env-example, inputing your information from (2.), your wallet address and gem ID
- 4. ``` python3 auto_mine.py``` 
- Note: although you dont have to manually adjust 'diff' parameter everytime, you still need to restart the process everytime someone minted target gem's nft still


### Once you get the salt:

- Go to etherscan or ftmscan
-   eth: https://etherscan.io/address/0xC67DED0eC78b849e17771b2E8a7e303B4dAd6dD4
-   fantom: https://ftmscan.com/address/0x342EbF0A5ceC4404CcFF73a40f9c30288Fc72611
- Select Contract > Write as Proxy > Connect your wallet (remember to select the right chain)
- Select 5.Mine > type in your gemID and salt that you just obtain > Write
- You will be prompted to pay a small gas fee (check gas at https://www.gasnow.org/), if the gas price is very high (>1 or 2 eth), then it means you are too late
- Done, now you can sell your gems on opensea, or keep it
- If you made some profit, go to https://opensea.io/collection/stick-the-buidler?collectionSlug=stick-the-buidler to buy some nft to support the creator!

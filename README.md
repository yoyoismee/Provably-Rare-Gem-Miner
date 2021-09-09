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


### (more detail) how to use 'auto_mine.py'

- benefits: manual version (stick_the_miner.py) requires you to update the 'diff' parameter every time someone minted the nft of the target gem
- steps:
- 1. update requirements ``` pip install -r requirement.txt ```
- 2. create an account at (https://infura.io/), select your chain (e.g. Ethereum), create a project and obtain your project ID
- 3. create a .env file in the same format as .env-example, inputing your information from (2.), your wallet address and gem ID
- 4. ``` python3 auto_mine.py``` 
- Note: although you dont have to manually adjust 'diff' parameter everytime, you still need to restart the process everytime someone minted target gem's nft still

import hashlib
from multiprocessing import Pool
from time import time

difficulty = 4

pattern = ''
for x in range(0, difficulty):
    pattern += '0'

class Block:

    nonce = 0

    def __init__(self, block, chain, data, previousHash=''):
        self.block = block
        self.chain = chain
        self.data = data
        self.previousHash = previousHash
        self.hash = self.calculateHash()
    
    def __str__(self):
        return self.calculateHash()

    def calculateHash(self):
        m = hashlib.sha256()
        m.update(str(self.block).encode())
        m.update(str(self.chain).encode())
        m.update(self.data.encode())
        m.update(str(self.previousHash).encode())
        m.update(str(self.nonce).encode())
        return m.hexdigest()

    def mineBlock(self, difficulty):
        start = time()
        while self.hash[:difficulty] != pattern:
            self.nonce += 1
            self.hash = self.calculateHash()
        print("Block mined in %.3f seconds: %s, nonce %s" % (time() - start, self.hash, self.nonce))

class BlockChain:

    def __init__(self, *args, **kwargs):
        self.chain = [self.createGenesisBlock()]
    
    def createGenesisBlock(self):
        return Block(0, 0, "Genesis block", 0)

    def getLastBlock(self):
        if len(self.chain) == 0:
            return self.chain[0]
        return self.chain[(len(self.chain)-1)]

    def getBlocks(self):
        return self.chain

    def addBlock(self, newBlock):
        newBlock.previousHash = self.getLastBlock().hash
        newBlock.mineBlock(difficulty)
        self.chain.append(newBlock)

import hashlib
import datetime

class Block():
    def __init__(self, index, timestamp, data, prev_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.hashing()

    def hashing(self):
        key = hashlib.sha256()
        key.update(str(self.index).encode('utf-8'))
        key.update(str(self.timestamp).encode('utf-8'))
        key.update(str(self.data).encode('utf-8'))
        key.update(str(self.prev_hash).encode('utf-8'))
        return key.hexdigest()

class Blockchain():
    def __init__(self):
        self.blocks = [self.getGenesisBlock()]

    def getGenesisBlock(self):
        return Block(0,
                     datetime.datetime.utcnow(),
                     'Genesis Block',
                     'arbitrary')

    def addBlock(self, data):
        self.blocks.append(Block(len(self.blocks),
                                 datetime.datetime.utcnow(),
                                 data,
                                 self.blocks[len(self.blocks) - 1].hash))

    def getChainSize(self):
        return len(self.blocks)

    def verifyChain(self, verbose=True):
        flag = True
        for i in range(1, len(self.blocks)):
            if self.blocks[i].index != i:
                flag = False
                if verbose:
                    print("The index of block " + str(i) + " is invalid.")
            if (self.blocks[i-1].hash != self.blocks[i].prev_hash):
                flag = False
                if verbose:
                    print("The prev_hash of block " + str(i) + " doesn't match with the hash of the previous block")
            if self.blocks[i].hash != self.blocks[i].hashing():
                flag = False
                if verbose:
                    print("The computed hash of block " + str(i) + " doesn't match with the stored hash.")
                if self.blocks[i - 1].timestamp >= self.blocks[i].timestamp:
                    flag = False
                    if verbose:
                        print(f'Backdating at block {i}.')
            print("chain verification complete")
            return flag


def main():
    chain = Blockchain()
    for j in range(1,8):
        chain.addBlock("Block # " + str(j))

    print("The chain length is " + str(chain.getChainSize()))
    chain.verifyChain()

    for i in chain.blocks:
        print("TS = " + str(i.timestamp))
        print("INDEX = " + str(i.index))
        print("DATA = " + str(i.data))
        print("HASH = " + str(i.hash))
        print("PREVIOUS HASH = " + str(i.prev_hash))
        print("=========================================================")

if __name__ == "__main__":
    main()

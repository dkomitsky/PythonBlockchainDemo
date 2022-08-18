# The purpose of this project is to create a functioning blockchain whose blocks contain
# simulated transactions signed with a digital signature, a new block hash, and the previous
# block hash (except in the case of the genesis block which has no previous block to take a previous hash from).
#
# Note that when running this program, it may take a few seconds for the output to appear
# due to generating the public / private keys

import rsa
import hashlib
import random   # used for simulated transactions

# the list which will contain all blocks
blockchain = []

class Block(object):

    def __init__(self):
        self.index = 0
        self.prevHash = ''
        self.pendingTransactions = []
        self.newHash = ''

    def newBlock(self):
        self.index = len(blockchain) + 1
        self.prevHash = blockchain[len(blockchain)-1].newHash

    def addTransactions(self,_sender,_recipient,_amount,_signature):
        payment = Transaction()
        payment.sender = _sender
        payment.recipient = _recipient
        payment.amount = _amount
        payment.signature = _signature

        self.pendingTransactions.append(payment)

    def createHash(self):
        hashString = str(self.index) + str(self.prevHash) + str(self.pendingTransactions)
        rawHash = hashlib.sha256(hashString.encode('utf-8'))
        hexHash = rawHash.hexdigest()
        self.newHash = hexHash

    def createGenesisBlock(self):
        self.index = 1
        self.prevHash = "genesisBlock"
        self.pendingTransactions = [('a', 'a', 999)]
        hashString = str(self.index) + str(self.prevHash) + str(self.pendingTransactions)
        rawHash = hashlib.sha256(hashString.encode('utf-8'))
        hexHash = rawHash.hexdigest()
        self.newHash = hexHash



class Transaction(object):
    sender = ''
    recipient = ''
    amount = 0
    signature = ''









# these lists contain public and private keys used for the simulated transactions
keyPairCount = 5
privateList = []
publicList = []
for i in range(keyPairCount):
    (publicKey, privateKey) = rsa.newkeys(2048)
    privateList.append(privateKey)
    publicList.append(publicKey)




# adds the genesis block (the very first block in the blockchain)
genesisBlock = Block()
genesisBlock.createGenesisBlock()
blockchain.append(genesisBlock)

# simulate transactions and add blocks
for _ in range(9):              # create 9 blocks after genesis block (10 total)
    block = Block()
    block.newBlock()
    for _ in range(4):          # each block has 4 transactions
        # choose random senders and recipients
        randomSender = random.randint(0,keyPairCount - 1)
        randomRecipient = random.randint(0,keyPairCount - 1)
        
        sender = publicList[randomSender]
        recipient = publicList[randomRecipient]
        amount = float(random.randint(1,100))                       # random float = transaction amount

        privateKey = privateList[randomSender]
        publicKey = publicList[randomSender]

        sigString = b"mySignature+data"                                  # data
        signature = rsa.sign(sigString, privateKey, 'SHA-512')

        try:
            rsa.verify(sigString,signature,publicKey)
            block.addTransactions(sender, recipient, amount, signature)
        except:
            print("invalid signature")

        
    block.createHash()
    blockchain.append(block)














# print blockchain
for i in range(len(blockchain)):

    # skip lines for easier output readability
    for i in range(10):
        print()
    
    print("New Block___________________________________")
    print()
    print("Index:",blockchain[i].index)
    print()
    print("Previous Hash:",blockchain[i].prevHash)
    print()
    for j in blockchain[i].pendingTransactions:
        print()
        print()
        print("Transaction-------")
        print()
        print("Sender:",j.sender)
        print()
        print("Recipient:",j.recipient)
        print()
        print("Amount:",j.amount)
        print()
        print("Signature:",j.signature)
        print()



    print()
    print("New Hash:",blockchain[i].newHash)
    print()

import json
from web3 import Web3
from eccdecrypt import decrypt_key

class Blockchain():
    def __init__(self):
        self.contract = None
        self.web3 = None
        self.connect()

    def connect(self):
        # Set up web3 connection with Ganache
        ganache_url = "http://127.0.0.1:7545"
        self.web3 = Web3(Web3.HTTPProvider(ganache_url))
        # TODO: Deploy the Greeter contract to Ganache with remix.ethereum.org
        # Set a default ac. hem count to sign transactions - this account is unlocked with Ganache
        self.web3.eth.defaultAccount = self.web3.eth.accounts[0]
        
        # Greeter contract ABI
        abi = json.loads('[ { "constant": false, "inputs": [ { "internalType": "string", "name": "str", "type": "string" } ], "name": "addHash", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [], "name": "addHashes", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "internalType": "string", "name": "str", "type": "string" } ], "name": "addKey", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [], "name": "addKeys", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": false, "inputs": [ { "internalType": "string", "name": "_filename", "type": "string" }, { "internalType": "string", "name": "_filepath", "type": "string" }, { "internalType": "string", "name": "_pubkey", "type": "string" }, { "internalType": "string", "name": "_filehash", "type": "string" } ], "name": "createFileEntry", "outputs": [], "payable": false, "stateMutability": "nonpayable", "type": "function" }, { "constant": true, "inputs": [], "name": "fileCount", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "getHashes", "outputs": [ { "internalType": "string[]", "name": "", "type": "string[]" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "getKeys", "outputs": [ { "internalType": "string[]", "name": "", "type": "string[]" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "getLastEntry", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "payable": false, "stateMutability": "view", "type": "function" }, { "constant": true, "inputs": [], "name": "getTotalCount", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "payable": false, "stateMutability": "view", "type": "function" } ]')
        
        # Greeter contract address - convert to checksum address
        address = self.web3.toChecksumAddress('0x8eB8E1f488c410EEb1dDb6A95c395C8459085B87') # FILL ME IN
        
        # Initialize contract
        self.contract = self.web3.eth.contract(address=address, abi=abi)


    def add(self,_filename,_filepath,_pubkey,_filehash):
        # Read the default greeting
        tx_hash = self.contract.functions.createFileEntry(_filename,_filepath,str(_pubkey),_filehash).transact()
        # Wait for transaction to be mined
        self.web3.eth.waitForTransactionReceipt(tx_hash)
        
        print(self.contract.functions.getLastEntry().call())
        print(self.contract.functions.getTotalCount().call())
        print(self.contract.functions.getKeys().call())

    def getKeys(self):
        keys = []
        for key in self.contract.functions.getKeys().call():
            if key!="":
                keys.append(decrypt_key(key))
        return keys

    def getHashes(self):
        hashes = []
        for hash in self.contract.functions.getHashes().call():
            if hash!="":
                hashes.append(hash)
        return hashes
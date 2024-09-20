from web3 import Web3
from solcx import compile_standard
import json

import solcx
solcx.install_solc('0.8.0')
solcx.set_solc_version('0.8.0')


# Connect to Ganache (local Ethereum blockchain)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
w3.eth.default_account = w3.eth.accounts[0]

# Compile the contract
# with open("PoliceCaseManagement.sol", "r") as file:
#     contract_source_code = file.read()

compiled_contract_path = r'E:\personalProjects\blockHack\build\contracts\PoliceCaseManagement.json'

deployed_contract_address = '0x2E21154e0820e77b52565D0b58D2f734C1a93A15'

# compiled_sol = compile_standard({
#     "language": "Solidity",
#     "sources": {"PoliceCaseManagement.sol": {"content": contract_source_code}},
#     "settings": {"outputSelection": {"*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}}},
# })

# abi = compiled_sol['contracts']['PoliceCaseManagement.sol']['PoliceCaseManagement']['abi']
# bytecode = compiled_sol['contracts']['PoliceCaseManagement.sol']['PoliceCaseManagement']['evm']['bytecode']['object']

# # Deploy contract
# PoliceCaseContract = w3.eth.contract(abi=abi, bytecode=bytecode)
# tx_hash = PoliceCaseContract.constructor().transact()
# tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# contract_address = tx_receipt.contractAddress
# print(f"Contract deployed at {contract_address}")


with open(compiled_contract_path) as file:
    contract_json = json.load(file)  
     
    # fetch contract's abi - necessary to call its functions
    contract_abi = contract_json['abi']
 
# Fetching deployed contract reference
contract = w3.eth.contract(
    address = deployed_contract_address, abi = contract_abi)
 
# Calling contract function (this is not persisted 
# to the blockchain)
output = contract.functions.getCase().call()
 
print(output)

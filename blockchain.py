from web3 import Web3
from solcx import compile_standard
import json

import solcx
solcx.install_solc('0.8.0')
solcx.set_solc_version('0.8.0')


# Connect to Ganache (local Ethereum blockchain)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
w3.eth.default_account = w3.eth.accounts[0]

# Path to the compiled contract JSON
compiled_contract_path = r'E:\personalProjects\blockHack\build\contracts\PoliceCaseManagement.json'

# Deployed contract address (from Ganache)
deployed_contract_address = '0x2E21154e0820e77b52565D0b58D2f734C1a93A15'

# Load the compiled contract's ABI from the JSON file
with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']

# Fetch the deployed contract
contract = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)


print(f"Using contract at address: {deployed_contract_address}")
print(f"ABI: {contract_abi}")


# Function to store a case on the blockchain
def store_case(fir_number, evidence_hash, forensics_hash, case_status):
    # Create a transaction to call the createCase function from the smart contract
    tx_hash = contract.functions.createCase(
        fir_number,
        evidence_hash,
        forensics_hash,
        case_status
    ).transact()

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction successful with hash: {tx_receipt.transactionHash.hex()}")


# Function to get case details
def get_case(fir_number):

    case_details = contract.functions.getCase(fir_number).call()
    print("FIR Number:", case_details[0])
    print("Evidence Hash:", case_details[1])
    print("Forensics Hash:", case_details[2])
    print("Case Status:", case_details[3])
    print("Timestamp:", case_details[4])


# Example usage
# Store a new case on the blockchain
store_case("FIR123456", "evidence_hash_123", "forensics_hash_123", "Open")

# Fetch case details from the blockchain
get_case("FIR12345")

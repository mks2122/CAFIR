from web3 import Web3
import mysql.connector
import json

# Connect to MySQL Database
db = mysql.connector.connect(
    host="sql12.freesqldatabase.com",
    user="sql12732577",
    password="KxcdYFz9WQ",
    database="sql12732577"
)

cursor = db.cursor()

# Connect to Ganache (local Ethereum blockchain)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.eth.default_account = w3.eth.accounts[0]

# Load the compiled contract ABI and contract address
compiled_contract_path = r'E:\\personalProjects\\blockHack\\build\\contracts\\PoliceCaseManagement.json'

with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']
    deployed_contract_address = '0x2E21154e0820e77b52565D0b58D2f734C1a93A15'
    contract = w3.eth.contract(address=deployed_contract_address, abi=contract_abi)

# Function to hash the values using keccak-256
def keccak_hash(value):
    return Web3.keccak(text=value)  # Hashes the string and returns bytes32

# Function to store a case on the blockchain and SQL database
def store_case(fir_number, evidence_hash, forensics_hash, case_status):
    # Hash the values using keccak-256
    fir_hash = keccak_hash(fir_number)  # Returns bytes32
    evidence_hash = keccak_hash(evidence_hash)
    forensics_hash = keccak_hash(forensics_hash)

    # Blockchain: Create a transaction to call the createCase function from the smart contract
    tx_hash = contract.functions.createCase(
        fir_hash,
        evidence_hash,
        forensics_hash,
        case_status
    ).transact()

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction successful with hash: {tx_receipt.transactionHash.hex()}")

    # SQL Database: Store the case data in the MySQL database
    insert_query = """INSERT INTO police_cases (fir_number, evidence_hash, forensics_hash, case_status)
                      VALUES (%s, %s, %s, %s)"""
    values = (fir_number, evidence_hash.hex(), forensics_hash.hex(), case_status)
    try:
        cursor.execute(insert_query, values)
        db.commit()
        print(f"Case {fir_number} stored in SQL database successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()

# Function to fetch a case from SQL database
def get_case_from_sql(fir_number):
    query = "SELECT * FROM police_cases WHERE fir_number = %s"
    cursor.execute(query, (fir_number,))
    result = cursor.fetchone()
    if result:
        print(f"FIR Number: {result[0]}, Evidence Hash: {result[1]}, Forensics Hash: {result[2]}, Status: {result[3]}")
    else:
        print("Case not found in SQL database")

# Function to fetch case details from the blockchain
def get_case_from_blockchain(fir_number):
    fir_hash = keccak_hash(fir_number)  # Convert fir_number to bytes32
    case_details = contract.functions.getCase(fir_hash).transact()
    print("FIR Number:", case_details[0])
    print("Evidence Hash:", case_details[1])
    print("Forensics Hash:", case_details[2])
    print("Case Status:", case_details[3])
    print("Timestamp:", case_details[4])

# Function to update case status on the blockchain and SQL database
def update_case_status(fir_number, case_status):
    fir_hash = keccak_hash(fir_number)  # Convert fir_number to bytes32
    # Blockchain: Create a transaction to call the updateCaseStatus function from the smart contract
    tx_hash = contract.functions.updateCaseStatus(
        fir_hash,
        case_status
    ).transact()

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction successful with hash: {tx_receipt.transactionHash.hex()}")

    # SQL Database: Update the case status in the MySQL database
    update_query = """UPDATE police_cases SET case_status = %s WHERE fir_number = %s"""
    values = (case_status, fir_number)
    try:
        cursor.execute(update_query, values)
        db.commit()
        print(f"Case {fir_number} status updated in SQL database successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()

# Function to close a case on the blockchain and SQL database
def close_case(fir_number):
    fir_hash = keccak_hash(fir_number)  # Convert fir_number to bytes32
    # Blockchain: Create a transaction to call the closeCase function from the smart contract
    tx_hash = contract.functions.closeCase(
        fir_hash
    ).transact()

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction successful with hash: {tx_receipt.transactionHash.hex()}")

    # SQL Database: Update the case status in the MySQL database
    update_query = """UPDATE police_cases SET case_status = 'Closed' WHERE fir_number = %s"""
    values = (fir_number,)
    try:
        cursor.execute(update_query, values)
        db.commit()
        print(f"Case {fir_number} closed in SQL database successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()

# Example usage:
store_case("FIR123456", "evidence_hash_123", "forensics_hash_123", "Open")

# Fetch case details from the blockchain
get_case_from_blockchain("FIR123456")
print("----------------------------------")
get_case_from_sql("FIR123456")
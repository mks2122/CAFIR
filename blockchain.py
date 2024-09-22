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

# Create a new table for the FIR
def create_case_table(fir_number):
    table_name = f"FIR_{fir_number}"
    create_query = f"""
    CREATE TABLE IF NOT EXISTS `{table_name}` (
        id INT AUTO_INCREMENT PRIMARY KEY,
        complainant_name VARCHAR(255),
        father_or_husband_name VARCHAR(255),
        address VARCHAR(255),
        phone_number VARCHAR(20),
        email VARCHAR(255),
        distance_from_police_station VARCHAR(255),
        direction_from_police_station VARCHAR(255),
        date_and_hour_of_occurrence DATETIME,
        nature_of_offence VARCHAR(255),
        stolen_property_description VARCHAR(255),
        accused_names TEXT,
        witness_names TEXT,
        case_status VARCHAR(50),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )"""
    cursor.execute(create_query)
    db.commit()


def detailsGetter():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    dic={}
    for i in tables:
        query=f"SELECT  complainant_name,phone_number, nature_of_offence  , accused_names, witness_names FROM {i[0]}"
        cursor.execute(query)
        data=cursor.fetchall()
        dic[i[0]]=data
    # print(dic)
    return tables,dic

detailsGetter()

# Function to store a case on the blockchain and SQL database
def store_case(fir_number, complainant_name, father_or_husband_name, address, phone_number, email, 
               distance_from_police_station, direction_from_police_station, date_and_hour_of_occurrence, 
               nature_of_offence, stolen_property_description, accused_names, witness_names, case_status):
    
    # Create a new table for the FIR
    create_case_table(fir_number)

    # Hash the FIR number and evidence description
    fir_hash = keccak_hash(fir_number)  # Returns bytes32
    print((stolen_property_description))
    evidence_hash = keccak_hash(str(stolen_property_description[0]))  # Returns bytes32

    # Blockchain: Create a transaction to call the createCase function from the smart contract
    tx_hash = contract.functions.createCase(
        fir_hash,
        evidence_hash,
        case_status
    ).transact()

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction successful with hash: {tx_receipt.transactionHash.hex()}")

    # SQL: Insert the data into the new table created for this FIR
    table_name = f"FIR_{fir_number}"
    insert_query = f"""INSERT INTO `{table_name}` (
                        complainant_name, father_or_husband_name, address, phone_number, email, 
                        distance_from_police_station, direction_from_police_station, date_and_hour_of_occurrence, 
                        nature_of_offence, stolen_property_description, accused_names, witness_names, case_status
                      ) 
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    values = (complainant_name, father_or_husband_name, address, phone_number, email, 
              distance_from_police_station, direction_from_police_station, date_and_hour_of_occurrence, 
              nature_of_offence, stolen_property_description, accused_names, witness_names, case_status)

    try:
        cursor.execute(insert_query, values)
        db.commit()
        print(f"Case {fir_number} stored in SQL database successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()

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

    # SQL Database: Update the case status in the new table
    table_name = f"FIR_{fir_number}"
    update_query = f"""UPDATE `{table_name}` SET case_status = %s WHERE id = (SELECT MAX(id) FROM `{table_name}`)"""
    values = (case_status,)
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

    # SQL Database: Update the case status in the new table
    table_name = f"FIR_{fir_number}"
    update_query = f"""UPDATE `{table_name}` SET case_status = 'Closed' WHERE id = (SELECT MAX(id) FROM `{table_name}`)"""
    try:
        cursor.execute(update_query, values)
        db.commit()
        print(f"Case {fir_number} closed in SQL database successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()

# Function to fetch case details from the blockchain
def get_case_from_blockchain(fir_number):
    fir_hash = keccak_hash(fir_number)  # Convert fir_number to bytes32
    case_details = contract.functions.getCase(fir_hash).transact()
    print("FIR Number:", case_details[0])
    print("Case Data Hash:", case_details[1])
    print("Case Status:", case_details[2])
    print("Timestamp:", case_details[3])

def get_case_details(fir_number):
    table_name = f"FIR_{fir_number}"
    select_query = f"""SELECT * FROM `{table_name}` WHERE id = (SELECT MAX(id) FROM `{table_name}`)"""
    cursor.execute(select_query)
    case_details = cursor.fetchone()
    print("FIR Number:", fir_number)
    print("Complainant Name:", case_details[1])
    print("Father's/Husband's Name:", case_details[2])
    print("Address:", case_details[3])
    print("Phone Number:", case_details[4])
    print("Email:", case_details[5])
    print("Distance from Police Station:", case_details[6])
    print("Direction from Police Station:", case_details[7])
    print("Date and Hour of Occurrence:", case_details[8])
    print("Nature of Offence:", case_details[9])
    print("Stolen Property Description:", case_details[10])
    print("Accused Names:", case_details[11])
    print("Witness Names:", case_details[12])
    print("Case Status:", case_details[13])
    print("Timestamp:", case_details[14])
    return case_details

# Example usage
# store_case("FIR123456", "John Doe", "Robert Doe", "123 Main St", "1234567890", 
#            "john.doe@example.com", "5 km", "North", "2023-09-20 14:00:00", 
#            "Theft", "Stolen laptop", "Accused Name", "Witness Name", "Open")

# # Fetch case details from the blockchain
# get_case_from_blockchain("FIR123456")



# BlockHack 2024 - Police Case Management System

## Introduction
This project is a **Police Case Management System** developed for **BlockHack 2024**. It leverages blockchain technology (Ethereum) to ensure secure, immutable storage of police case-related data such as FIRs, evidence, and forensic reports. By integrating blockchain with traditional database systems (MySQL), the system aims to prevent tampering and maintain transparency in legal proceedings.

## Key Features
- **Blockchain Integration**: All important case data is stored as hashes on the Ethereum blockchain using smart contracts, preventing tampering and ensuring data integrity.
- **MySQL Database**: The actual case data (FIRs, case status, etc.) is stored in a MySQL database for ease of access and querying.
- **Secure Case Management**: Cases can be created, updated, and retrieved securely, with evidence and forensic data stored alongside the case information.
- **Flask Web Application**: A user-friendly interface built using Flask, allowing police officers to interact with the system and manage cases efficiently.
- **Ganache for Local Blockchain**: The smart contracts are deployed on a local Ethereum blockchain using Ganache, making development and testing seamless.

## Components
1. **Smart Contracts (Solidity)**:
   - **PoliceCase.sol**: Manages the lifecycle of police cases, storing essential data as events and providing functions to create, update, and retrieve cases.
   
2. **Flask Application (Python)**:
   - Handles the user interface, allowing officers to input case data.
   - Integrates with both the Ethereum blockchain (via web3.py) and the MySQL database for efficient data management.

3. **MySQL Database**:
   - Stores detailed case information, with only the hashes of critical data points stored on the blockchain for security.

4. **Blockchain Integration (Web3.py)**:
   - Interacts with the deployed Ethereum contracts, allowing secure case management.

## How it Works
1. **FIR Creation**: Officers can create a new FIR. The FIR data is hashed and stored on the blockchain, while the full FIR details are stored in the MySQL database.
2. **Evidence Management**: Officers can add or update evidence for a case, with hashes stored on-chain.
3. **Tamper-proof System**: Since case data is hashed and stored on the blockchain, any attempt to tamper with the case details will be easily detected.
4. **Viewing Cases**: Officers can retrieve and view existing case details securely, with blockchain ensuring data integrity.

## Getting Started

### Prerequisites
To set up the project locally, ensure you have the following installed:
- [Ganache](https://trufflesuite.com/ganache/) (for running a local Ethereum blockchain)
- [Node.js](https://nodejs.org/en/) (for deploying the smart contracts)
- [Python 3.x](https://www.python.org/downloads/) and the required packages (Flask, web3.py)
- MySQL (for database storage)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mks2122/blockhack2024.git
   cd blockhack2024
   ```

2. **Set up the Ethereum Blockchain**:
   - Install Ganache and start a local blockchain instance.
   - Deploy the smart contracts on the blockchain using the provided deployment script.

3. **Set up MySQL Database**:
   - Create a database and import the schema provided in the `sql` folder.
   - Update the `config.py` file with your database credentials.

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   ```bash
   npm install
   ```

5. **Run the Flask Application**:
   ```bash
   python app.py
   ```

6. **Access the Application**:
   Open your browser and navigate to `http://localhost:5000` to interact with the Police Case Management System.

## Smart Contract Overview
The smart contract (`PoliceCase.sol`) includes the following features:
- **Create Case**: Allows authorized officers to create new cases with details like FIR and evidence hash.
- **Update Case**: Officers can update the case status and append new evidence.
- **Retrieve Case**: Anyone can retrieve the hash of a particular case to verify its integrity.

## Project Structure

```
blockhack2024/
│
├── contracts/                   # Solidity smart contracts
│   └── PoliceCase.sol           # Main smart contract for managing cases
│
├── flask_app/                   # Flask application files
│   ├── static/                  # Static files (CSS, JS)
│   ├── templates/               # HTML templates for the UI
│   └── app.py                   # Flask app entry point
│
├── sql/                         # SQL schema for setting up MySQL database
├── migrations/                  # Database migrations (if using Flask-Migrate)
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
└── truffle-config.js            # Configuration for Truffle/Ganache
```

## Future Enhancements
- Implement user authentication for officers.
- Deploy the contracts on a public Ethereum testnet.
- Integrate IPFS for decentralized storage of large files such as forensic reports and evidence.

## Contributing
We welcome contributions to improve the project. Feel free to submit pull requests or open issues for any bugs or feature requests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

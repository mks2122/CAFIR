// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

contract PoliceCaseManagement {
    
    struct CaseData {
        bytes32 firNumber;        // FIR Number
        bytes32 caseDataHash;     // Hash of the FIR case data (from SQL database)
        string caseStatus;        // Case Status (Open, Closed, etc.)
        uint256 timestamp;        // Timestamp when the hash was stored
        bool isActive;            // Case active or closed
    }
    
    mapping(bytes32 => CaseData) public cases;

    event CaseCreated(bytes32 indexed firNumber, uint256 timestamp);
    event CaseUpdated(bytes32 indexed firNumber, string caseStatus, uint256 timestamp);

    // Create a new case
    function createCase(
        bytes32 firNumber,
        bytes32 caseDataHash,
        string calldata caseStatus
    ) public {
        require(firNumber != bytes32(0), "Invalid FIR number");
        require(cases[firNumber].firNumber == bytes32(0), "Case already exists");

        cases[firNumber] = CaseData(
            firNumber,
            caseDataHash,
            caseStatus,
            block.timestamp,
            true
        );

        emit CaseCreated(firNumber, block.timestamp);
    }

    // Update case status without modifying the hash
    function updateCaseStatus(bytes32 firNumber, string calldata caseStatus) public {
        require(cases[firNumber].firNumber != bytes32(0), "Case not found");
        require(cases[firNumber].isActive, "Case is closed");

        cases[firNumber].caseStatus = caseStatus;

        emit CaseUpdated(firNumber, caseStatus, block.timestamp);
    }

    // Close the case
    function closeCase(bytes32 firNumber) public {
        require(cases[firNumber].firNumber != bytes32(0), "Case not found");
        require(cases[firNumber].isActive, "Case is already closed");

        cases[firNumber].isActive = false;
        cases[firNumber].caseStatus = "Closed";

        emit CaseUpdated(firNumber, "Closed", block.timestamp);
    }

    // Verify the integrity of case data using hash
    function verifyCaseHash(bytes32 firNumber, bytes32 newCaseDataHash) public view returns (bool) {
        require(cases[firNumber].firNumber != bytes32(0), "Case not found");
        return cases[firNumber].caseDataHash == newCaseDataHash;
    }

    // Get case details
    function getCase(bytes32 firNumber) 
        public 
        view 
        returns (
            bytes32 fir,
            bytes32 caseDataHash,
            string memory status,
            uint256 timestamp
        ) 
    {
        require(cases[firNumber].firNumber != bytes32(0), "Case not found");
        CaseData memory c = cases[firNumber];
        return (
            c.firNumber,
            c.caseDataHash,
            c.caseStatus,
            c.timestamp
        );
    }

    // Get only the stored hash for integrity check
    function getCaseHash(bytes32 firNumber) public view returns (bytes32) {
        require(cases[firNumber].firNumber != bytes32(0), "Case not found");
        return cases[firNumber].caseDataHash;
    }
}

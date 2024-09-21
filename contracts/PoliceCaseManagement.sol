// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.0;

contract PoliceCaseManagement {

    struct CaseData {
        bytes32 firNumber;
        bytes32 evidenceHash;
        bytes32 forensicsHash;
        string caseStatus;
        uint256 timestamp;
        bool isActive;
    }


    function createCase(
        bytes32 firNumber,
        bytes32 evidenceHash,
        bytes32 forensicsHash,
        string calldata caseStatus
    ) public {
        require(firNumber != bytes32(0), "Invalid FIR number");
        require(cases[firNumber].firNumber == bytes32(0), "Case already exists");

        cases[firNumber] = CaseData(
            firNumber,
            evidenceHash,
            forensicsHash,
            caseStatus,
            block.timestamp,
            true
        );

        emit CaseCreated(firNumber, block.timestamp);
    }

    function updateCaseStatus(bytes32 firNumber, string calldata caseStatus) public {
        require(cases[firNumber].firNumber != bytes32(0), "Case not found");
        require(cases[firNumber].isActive, "Case is closed");

        CaseData storage c = cases[firNumber];
        c.caseStatus = caseStatus;

        emit CaseUpdated(firNumber, caseStatus, block.timestamp);
    }

    function closeCase(bytes32 firNumber) public {
        require(cases[firNumber].firNumber != bytes32(0), "Case not found");
        require(cases[firNumber].isActive, "Case is already closed");

        CaseData storage c = cases[firNumber];
        c.isActive = false;
        c.caseStatus = "Closed";

        emit CaseUpdated(firNumber, "Closed", block.timestamp);
    }

    function getCase(bytes32 firNumber)
        public
        view
        returns (
            bytes32 fir,
            bytes32 evidence,
            bytes32 forensics,
            string memory status,
            uint256 timestamp
        )
    {
        require(cases[firNumber].firNumber != bytes32(0), "Case not found");

        CaseData memory c = cases[firNumber];
        return (
            c.firNumber,
            c.evidenceHash,
            c.forensicsHash,
            c.caseStatus,
            c.timestamp
        );
    }
}


pragma solidity ^0.8.0;

contract PoliceCaseManagement {
    struct CaseData {
        string firNumber;
        string evidenceHash;
        string forensicsHash;
        string caseStatus;
        uint timestamp;
    }

    // Using bytes32 for mapping keys, but string firNumber is still used in events
    mapping(bytes32 => CaseData) public cases;

    event CaseCreated(string firNumber, uint timestamp);
    event CaseUpdated(string firNumber, string caseStatus, uint timestamp);

    function createCase(
        string memory firNumber,
        string memory evidenceHash,
        string memory forensicsHash,
        string memory caseStatus
    ) public {
        bytes32 firKey = keccak256(abi.encodePacked(firNumber)); // Convert firNumber to bytes32 for mapping key
        cases[firKey] = CaseData(
            firNumber,
            evidenceHash,
            forensicsHash,
            caseStatus,
            block.timestamp
        );
        emit CaseCreated(firNumber, block.timestamp); // Emit original firNumber (string)
    }

    function updateCaseStatus(string memory firNumber, string memory caseStatus) public {
        bytes32 firKey = keccak256(abi.encodePacked(firNumber)); // Convert firNumber to bytes32 for mapping key
        require(bytes(cases[firKey].firNumber).length != 0, "Case not found");  // Ensure case exists before updating
        CaseData storage c = cases[firKey];
        c.caseStatus = caseStatus;
        emit CaseUpdated(firNumber, caseStatus, block.timestamp); // Emit original firNumber (string)
    }

    function getCase(string memory firNumber) public view returns (
        string memory fir, string memory evidence, string memory forensics, string memory status, uint timestamp
    ) {
        bytes32 firKey = keccak256(abi.encodePacked(firNumber)); // Convert firNumber to bytes32 for mapping key
        require(bytes(cases[firKey].firNumber).length != 0, "Case not found");

        CaseData memory c = cases[firKey];
        return (c.firNumber, c.evidenceHash, c.forensicsHash, c.caseStatus, c.timestamp);
    }
}

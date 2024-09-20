pragma solidity ^0.8.0;

contract PoliceCaseManagement {
    struct CaseData {
        string firNumber;
        string evidenceHash;
        string forensicsHash;
        string caseStatus;
        uint timestamp;
    }

    mapping(string => CaseData) public cases;

    event CaseCreated(string firNumber, uint timestamp);
    event CaseUpdated(string firNumber, string caseStatus, uint timestamp);

    function createCase(
        string memory firNumber,
        string memory evidenceHash,
        string memory forensicsHash,
        string memory caseStatus
    ) public {
        cases[firNumber] = CaseData(
            firNumber,
            evidenceHash,
            forensicsHash,
            caseStatus,
            block.timestamp
        );
        emit CaseCreated(firNumber, block.timestamp);
    }

    function updateCaseStatus(string memory firNumber, string memory caseStatus) public {
        CaseData storage c = cases[firNumber];
        c.caseStatus = caseStatus;
        emit CaseUpdated(firNumber, caseStatus, block.timestamp);
    }

    function getCase(string memory firNumber) public view returns (
        string memory fir, string memory evidence, string memory forensics, string memory status, uint timestamp
    ) {
        CaseData memory c = cases[firNumber];
        return (c.firNumber, c.evidenceHash, c.forensicsHash, c.caseStatus, c.timestamp);
    }

    function geeks() public pure returns (string memory) 
  {
    return 'Hey there! I m learning from GeeksForGeeks!';
  }
}

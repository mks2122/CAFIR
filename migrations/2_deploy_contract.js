const PoliceCaseManagement = artifacts.require("PoliceCaseManagement");

module.exports = function (deployer) {
  deployer.deploy(PoliceCaseManagement); // ✅ No arguments needed
};
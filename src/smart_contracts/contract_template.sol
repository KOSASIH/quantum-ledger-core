// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts/proxy/utils/UUPSUpgradeable.sol";

contract ContractTemplate is AccessControl, Initializable, UUPSUpgradeable {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    event DataStored(uint256 indexed id, string data);
    
    struct Data {
        uint256 id;
        string content;
    }

    mapping(uint256 => Data) private dataStore;
    uint256 private dataCount;

    function initialize() public initializer {
        _setupRole(ADMIN_ROLE, msg.sender);
        dataCount = 0;
    }

    function storeData(string memory content) public onlyRole(ADMIN_ROLE) {
        dataCount++;
        dataStore[dataCount] = Data(dataCount, content);
        emit DataStored(dataCount, content);
    }

    function getData(uint256 id) public view returns (Data memory) {
        return dataStore[id];
    }

    function _authorizeUpgrade(address newImplementation) internal override onlyRole(ADMIN_ROLE) {}
}

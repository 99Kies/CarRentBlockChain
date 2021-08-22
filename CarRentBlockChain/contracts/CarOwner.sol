pragma solidity^0.4.25;
import "Roles.sol";
contract CarOwner{
    using Roles for Roles.Role;
    Roles.Role private _carOwner;
    event carOwnerAdded(address amount);
    
    constructor(address carOwner)public{
        _addCarOwner(carOwner);
    }
    function _addCarOwner(address amount)internal{
        _carOwner.add(amount);
        emit carOwnerAdded(amount);
    }
    function isCarOwner(address amount)public view returns(bool){
        return _carOwner.has(amount);
    }
    modifier onlyCarOwner(){
        require(isCarOwner(msg.sender));
        _;
    }
    function addCarOwner(address amount)public onlyCarOwner{
        _addCarOwner(amount);
    }
}


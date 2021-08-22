pragma solidity^0.4.25;
import "Roles.sol";
contract User{
    using Roles for Roles.Role;
    Roles.Role private _uer;
    event UserAdded(address amount);
    
    constructor(address uer)public{
        _addUser(uer);
    }
    function _addUser(address amount)internal{
        _uer.add(amount);
        emit UserAdded(amount);
    }
    function isUser(address amount)public view returns(bool){
        return _uer.has(amount);
    }
    modifier onlyUser(){
        require(isUser(msg.sender));
        _;
    }
    function addUser(address amount)public onlyUser{
        _addUser(amount);
    }
}

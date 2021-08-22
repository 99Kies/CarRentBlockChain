pragma solidity^0.4.25;

library Roles{
    struct Role{
        mapping(address=>bool) bearer;
    }
    //判定地址存在否
    function has(Role storage role,address amount)internal view returns(bool){
        require(amount!=address(0));
        return role.bearer[amount];
    }
    
    //添加角色
    function add(Role storage role,address amount)internal{
        require(!has(role,amount));
        role.bearer[amount] = true;
    }
}
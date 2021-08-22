pragma solidity^0.4.25;
//pragma experimental ABIEncoderV2; //返回结构体类型
import "./Roles.sol";
import "./CarOwner.sol";
import "./Car.sol";
import "./User.sol";

contract Platform is CarOwner,User{
    mapping(uint256=>address) cars;   //链码映射车辆合约地址 
    uint256[] carList; 
    address owner; //合约的部署者，管理员
    
    //初始化
    constructor (address carOwner,address user)public CarOwner(carOwner) User(user){
        owner = msg.sender;
    }
    
    //车辆信息上链Vehicle on the chain
    function newVehicle(uint256 chainNumber,string number,string brand,string color,string quality,uint16 price)public onlyCarOwner returns(address){
        require(cars[chainNumber]==address(0));
        Car car = new Car(number,brand,color,quality,price);
        cars[chainNumber] = car;
        carList.push(chainNumber);
        return car;
    }
    function signVehicle(uint256 chainNumber)public onlyUser returns(bool){
        require(cars[chainNumber]!=address(0));
        return Car(cars[chainNumber]).signContract();
    }
    function rebackVehicle(uint256 chainNumber)public onlyUser returns(bool){
        require(cars[chainNumber]!=address(0));
        return Car(cars[chainNumber]).reback();
    }
    //查看所有车辆的链码
    function getCarList()public view returns(uint256[]){
        return carList;
        
    }
    
    //根据链码查询相关车辆的信息
    function getCar(uint256 chainNumber)public view returns(uint256,address,string,string,string,string,uint16,uint8){
        return Car(cars[chainNumber]).getCarInfo();
    }
}

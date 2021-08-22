pragma solidity^0.4.25;
contract Car{
    uint256[] _timestamp;   //上链时间戳
    address _carAdress;    //车主地址
    string _number;        //车牌号
    string _brand;          //车辆品牌
    string _color;          //车辆颜色
    uint16 _price;          //车辆价格
    string _quality;       //车辆质量状态（包括安检，保险） 满足2个条件=A 满足一个条件=B 都不满足=C 
    uint8 _status;          //当前交易状态 0未租借 1 已租借
    address owner;        
    
    constructor(string number,string brand,string color,string quality,uint16 price)public{
        _timestamp.push(now);
        _carAdress = msg.sender;
        _number = number;
        _brand = brand;
        _color = color;
        _quality = quality;
        _price = price; 
        _status = 0;
        owner = msg.sender;//车辆拥有者地址
    }
    
    function signContract()public returns(bool){
        require(_status == 0,"The current status is sold or does not exist");
        _status = 1;
        owner = msg.sender;//车辆租借者地址
        return true;
    }
    
    function reback()public returns(bool){
        require(_status == 1,"The current status is sold or does not exist");
        _status = 0;
        owner = _carAdress;//
        return true;
    }
    
    function getCarInfo()public view returns(uint256,address,string,string,string,string,uint16,uint8){
        return(_timestamp[0], owner,_number,_brand,_color,_quality,_price,_status);
    }
}

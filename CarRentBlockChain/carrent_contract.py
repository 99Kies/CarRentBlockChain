from client.bcosclient import BcosClient
from client.datatype_parser import DatatypeParser
from web3 import Web3

class Car_Contract:
    def __init__(self, address: str):
        # 0x0e2a98891f7daa8edca95dda4317e8c6b47908f9
        abi_file = "contracts/Platform.abi"
        data_parser = DatatypeParser()
        data_parser.load_abi_file(abi_file)
        self.contract_abi = data_parser.contract_abi

        self.client = BcosClient()
        self.to_address = address

    def add_carowner_by_amount(self, amount:str):
        amount = Web3.toChecksumAddress(amount)
        new_carowner = self.client.sendRawTransactionGetReceipt(self.to_address, self.contract_abi, "addCarOwner", [amount])
        return new_carowner

    def add_user_by_amount(self, amount: str):
        amount = Web3.toChecksumAddress(amount)
        new_user = self.client.sendRawTransactionGetReceipt(self.to_address, self.contract_abi, "addUser",
                                                                [amount])
        return new_user

    def get_car_by_chainnumber(self, chainNumber: int):
        car_message = self.client.call(self.to_address, self.contract_abi, "getCar", [chainNumber])
        return car_message

    def get_car_list(self):
        car_list = self.client.call(self.to_address, self.contract_abi, "getCarList", [])
        return car_list

    def is_carowner(self, amount: str):
        amount = Web3.toChecksumAddress(amount)
        is_carowner = self.client.call(self.to_address, self.contract_abi, "isCarOwner",
                                                                [amount])
        return is_carowner

    def is_user(self, amount: str):
        amount = Web3.toChecksumAddress(amount)
        is_user = self.client.call(self.to_address, self.contract_abi, "isUser", [amount])
        return is_user

    def new_vehicle(self, chainNumber: int, number: str, brand: str, color: str, quality: str, price: int, day: int):
        new_vehicle = self.client.sendRawTransactionGetReceipt(self.to_address, self.contract_abi, "newVehicle", [chainNumber, number, brand, color, quality, price, day])
        return new_vehicle

    def reback_vehicle(self, chainNumber: int):
        reback_vehicle = self.client.sendRawTransactionGetReceipt(self.to_address, self.contract_abi, "rebackVehicle", [chainNumber])
        return reback_vehicle

    def sign_vehicle(self, chainNumber: int):
        sign_vehicle = self.client.sendRawTransactionGetReceipt(self.to_address, self.contract_abi, "signVehicle", [chainNumber])
        return sign_vehicle

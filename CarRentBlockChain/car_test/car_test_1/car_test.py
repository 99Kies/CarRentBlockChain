import sys
sys.path.append("../..")

from carrent_contract import Car_Contract

if __name__ == '__main__':

    contract_address = "0x0e2a98891f7daa8edca95dda4317e8c6b47908f9"
    admin_privkey = "b5fd88ce925ef764bfac9a6bbc256abdabbb6423833eaa19d8fc70e2adc00ab3"
    fengfeng = "d6f8c8f9106835ccc8f8d0bbc4b5bf32ff5f8941e69f9f50d075684d10dda7be"
    fengfeng_addr = "0x28b7a9da9f3a92e139b58181aee04d0720cdd767"

    fengfeng2 = "39a6825ab179ed43fc774ca49931f680d3c68318ad993b7b2885853e36252d4"
    fengfeng2_addr = "0x405b66921a8ec0899d60961834982aa207acc922"

    user1 = "e148500d7da7c4ddb64d8af3b23e7718b1079efa0cab791c9fcbd44433464594"
    user1_addr = "0x49d50b662e266a3451f0cda370618f0b380f59f1"

    user2 = "af792b3b10273a3c0302dacb2003b1d5228786bd4b123e2e2a0a2ebf2792306d"
    user2_addr = "0x96582f6ea01473c3f61f5636c0ea5cf066e765c9"

    from pprint import pprint
    a = Car_Contract(contract_address)
    a.client.set_account_by_privkey(admin_privkey)
    add_carowner = a.add_carowner_by_amount(fengfeng_addr)
    # 添加carowner
    pprint(add_carowner)
    is_carowner = a.is_carowner(fengfeng_addr)
    pprint(is_carowner)
    pprint('===================================================')
    pprint('===================================================')
    pprint('===================================================')
    pprint('===================================================')
    add_user = a.add_user_by_amount(user1_addr)
    # 添加用户user
    pprint(add_user)
    is_user = a.is_user(user1_addr)
    pprint(is_user)

    a.client.set_account_by_privkey(fengfeng)
    new_car = a.new_vehicle(0, "浙J·AE866", "法拉利", "红色", "2", 1200, 2)
    pprint(new_car)

    carlist = a.get_car_list()
    # 获取当前所有的chainNumber
    pprint(carlist)

    car_msg = a.get_car_by_chainnumber(0)
    # 查看车辆信息
    print(car_msg)

    a.client.set_account_by_privkey(user1)
    a.sign_vehicle(0)

    car_msg = a.get_car_by_chainnumber(0)
    print(car_msg)

    carlist = a.get_car_list()
    pprint(carlist)

    reback_msg = a.reback_vehicle(0)
    # 还车
    pprint(reback_msg)


    car_msg = a.get_car_by_chainnumber(0)
    print(car_msg)
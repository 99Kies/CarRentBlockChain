from flask import Flask, jsonify, request, render_template
from carrent_contract import Car_Contract
from flask_cors import CORS
import json

app = Flask(__name__)
contract_address = "0xcd3b305bcd9c89f55ae1f1bb786804dd5614e2ca"
admin_privkey = "8ef2fa4907d75fa653cede21fa0a75d62add49e4db46044dd3954dda14fcdfa6"
CORS(app)

@app.route("/carowner/add", methods=["POST"])
def add_carowner_by_amount():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Pleace input [address] by string."}), 400
    address = data["address"]
    carrent = Car_Contract(contract_address)
    carrent.client.set_account_by_privkey(admin_privkey)
    new_carowner = carrent.add_carowner_by_amount(address)
    return jsonify(new_carowner), 200


@app.route("/carowner/is_carowner/<string:address>", methods=["POST", "GET"])
def is_carowner(address):
    carrent = Car_Contract(contract_address)
    iscarowner = carrent.is_carowner(address)
    return jsonify(iscarowner), 200


@app.route("/car/<int:chainnumber>", methods=["GET", "POST"])
def getcar(chainnumber):
    carrent = Car_Contract(contract_address)
    car_msg = carrent.get_car_by_chainnumber(chainnumber)
    return jsonify(car_msg), 200


@app.route("/car/list", methods=["GET", "POST"])
def getcarlist():
    carrent = Car_Contract(contract_address)
    car_msg = carrent.get_car_list()
    return jsonify(car_msg), 200

@app.route("/user/add", methods=["POST"])
def add_user_by_amount():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Pleace input [address] by string."}), 400
    address = data["address"]
    carrent = Car_Contract(contract_address)
    carrent.client.set_account_by_privkey(admin_privkey)
    new_user = carrent.add_user_by_amount(address)
    return jsonify(new_user), 200



@app.route("/user/is_user/<string:address>", methods=["POST", "GET"])
def is_user(address):
    carrent = Car_Contract(contract_address)
    isuser = carrent.is_user(address)
    return jsonify(isuser), 200

@app.route("/vehicle/new/<string:carowner_privkey>", methods=["GET", "POST"])
def new_vehicle(carowner_privkey):
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Pleace input [chainNumber, number, brand, color, quality, price, day]s."}), 400
    chainNumber = int(data["chainNumber"])
    number = data["number"]
    brand = data["brand"]
    color = data["color"]
    quality = data["quality"]
    price = int(data["price"])
    day = int(data["day"])

    carrent = Car_Contract(contract_address)
    carrent.client.set_account_by_privkey(carowner_privkey)
    newvehicle = carrent.new_vehicle(chainNumber, number, brand, color, quality, price, day)
    return jsonify(newvehicle), 200

@app.route("/vehicle/sign/<string:user_privkey>/<int:chainNumber>", methods=["GET", "POST"])
def sign_vehicle(user_privkey, chainNumber):
    carrent = Car_Contract(contract_address)
    carrent.client.set_account_by_privkey(user_privkey)
    sign_msg = carrent.sign_vehicle(chainNumber)
    return jsonify(sign_msg), 200


@app.route("/vehicle/reback/<string:user_privkey>/<int:chainNumber>", methods=["GET", "POST"])
def reback_vehicle(user_privkey, chainNumber):
    carrent = Car_Contract(contract_address)
    carrent.client.set_account_by_privkey(user_privkey)
    reback_msg = carrent.reback_vehicle(chainNumber)
    return jsonify(reback_msg), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(5001), debug=False)



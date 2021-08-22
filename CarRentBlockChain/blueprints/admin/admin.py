# -*- coding: utf-8 -*-
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    abort,
    jsonify
)
from flask_login import login_required, login_user, logout_user, current_user

from CarRentBlockChain.extensions import login_manager
from CarRentBlockChain.blueprints.public.forms import RegisterForm, LoginForm
from CarRentBlockChain.blueprints.public.models import User
from CarRentBlockChain.webutils import flash_errors, redirect_back
from CarRentBlockChain.extensions import db, csrf_protect
from CarRentBlockChain.settings import REQUEST_HEADER, CARRENT_URL
from CarRentBlockChain.blueprints.admin.models import CARCNT

import requests
from flask_cors import CORS
import json

from flask.json import JSONEncoder

admin_bp = Blueprint("admin", __name__, static_folder="../static")

CORS(admin_bp)
@admin_bp.route('/')
@login_required
def index():
    if current_user.is_admin:
        users = User.query.order_by(User.created_at.desc()).all()
        return render_template('admin/admin.html', users=users)
    else:
        return abort(404)

@admin_bp.route('/addactive', methods=['GET', 'POST'])
@login_required
def addactive():
    if current_user.is_admin:
        username = request.args.get('username')
        user = User.query.filter(User.username==username).first()
        user.active = True
        db.session.commit()
        return redirect_back()
    else:
        return abort(404)
    

@admin_bp.route('/cancleactive', methods=['GET', 'POST'])
@login_required
def cancleactive():
    if current_user.is_admin:
        username = request.args.get('username')
        user = User.query.filter(User.username==username).first()
        user.active = False
        db.session.commit()
        return redirect_back()
    else:
        return abort(404)
    

@admin_bp.route('/add_all_active', methods=['GET', 'POST'])
@login_required
def add_all_active():
    if current_user.is_admin:
        users = User.query.order_by(User.created_at.desc()).all()
        for user in users:
            user.active = True
        db.session.commit()
        return redirect_back()
    else:
        return abort(404)

@admin_bp.route('/cancle_all_active', methods=['GET', 'POST'])
@login_required
def cancle_all_active():
    if current_user.is_admin:
        users = User.query.order_by(User.created_at.desc()).all()
        for user in users:
            if not user.is_admin:
                user.active = False
        db.session.commit()
        return redirect_back()
    else:
        return abort(404)

@csrf_protect.exempt
@admin_bp.route("/user/listUsers", methods=["GET", "POST"])
# @login_required
def listuser():
    # if current_user.is_admin:
    return_dict = []
    all_user = User.query.filter(User.status == "User").all()
    for user in all_user:
        user_msg = {
            "account": user.address,
            "name": user.username,
            "chainNumber": user.chainnumber,
            "idCode": user.idcard,
            "phone": user.iphone
        }
        return_dict.append(user_msg)
    return jsonify(return_dict)

@csrf_protect.exempt
@admin_bp.route("/user/listCarOwners", methods=["GET", "POST"])
# @login_required
def listcarowner():
    # if current_user.is_admin:
    return_dict = []
    all_carowner = User.query.filter(User.status == "CarOwner").all()
    for carowner in all_carowner:
        carowner_msg = {
            "account": carowner.address,
            "name": carowner.username,
            "chainNumber": carowner.chainnumber,
            "idCode": carowner.idcard,
            "phone": carowner.iphone,
        }
        return_dict.append(carowner_msg)
    return jsonify(return_dict)

@csrf_protect.exempt
@admin_bp.route("/is_user/<string:address>", methods=["GET", "POST"])
def is_user(address):
    link_url = CARRENT_URL + "/user/is_user/" + address

    r_is_user = requests.get(link_url)

    return jsonify(r_is_user.json()[0]), 200

@csrf_protect.exempt
@admin_bp.route("/is_carowner/<string:address>", methods=["GET", "POST"])
def is_carowner(address):
    link_url = CARRENT_URL + "/carowner/is_carowner/" + address


    r_is_carowner = requests.get(link_url)

    return jsonify(r_is_carowner.json()[0]), 200

@csrf_protect.exempt
@admin_bp.route("/car/list", methods=["GET", "POST"])
def listcar():
    link_url = CARRENT_URL + "/car/list"

    r_list_car = requests.get(link_url).json()
    return_list = []
    for i in r_list_car[0]:
        get_car_url = CARRENT_URL + "/car/" + str(i)

        r_car = requests.get(get_car_url).json()
        print(r_car)
        data = {}
        data["chainNumber"] = str(i)
        data["number"] = r_car[2]
        data["brand"] = r_car[3]
        data["price"] = r_car[6]
        data["day"] = r_car[8]
        data["status"] = r_car[7]
        data["color"] = r_car[4]
        data["quality"] = r_car[5]
        return_list.append(data)

    return jsonify(return_list), 200

@csrf_protect.exempt
@admin_bp.route("/user/getcar/<string:user_privkey>", methods=["GET", "POST"])
def getUserCar(user_privkey):
    user1 = User.query.filter(User.privkey==user_privkey).first()
    chainNumber = str(user1.chainnumber)
    link_url = CARRENT_URL + "/car/" + chainNumber

    r_car = requests.get(link_url).json()
    if r_car[7] == 0:
        return jsonify({}), 400
    return_list = []
    data = {}
    data["chainNumber"] = chainNumber
    data["number"] = r_car[2]
    data["brand"] = r_car[3]
    data["price"] = r_car[6]
    data["day"] = r_car[8]
    data["status"] = r_car[7]
    data["color"] = r_car[4]
    data["quality"] = r_car[5]
    return_list.append(data)
    return jsonify(return_list), 200

@csrf_protect.exempt
@admin_bp.route("/car/<string:carowner_privkey>", methods=["GET", "POST"])
def getcar(carowner_privkey):

    carcnt = CARCNT.query.filter(CARCNT.carowner_privkey==carowner_privkey).first()
    chainNumber = carcnt.chainNumber
    link_url = CARRENT_URL + "/car/" + str(chainNumber)

    r_car = requests.get(link_url).json()

    data = {}
    data["chainNumber"] = chainNumber
    data["number"] = r_car[2]
    data["brand"] = r_car[3]
    data["price"] = r_car[6]
    data["day"] = r_car[8]
    data["status"] = r_car[7]
    data["color"] = r_car[4]
    data["quality"] = r_car[5]

    return jsonify(data), 200

@csrf_protect.exempt
@admin_bp.route("/vehicle/sign", methods=["POST", "GET"])
def sign_vehicle():
    r = request.get_json()
    user_privkey = r['privateKey']
    chainNumber = r['chainNumber']



    link_url = CARRENT_URL + "/vehicle/sign/" + user_privkey + "/" + chainNumber
    r_sign = requests.get(link_url).json()
    if r_sign["statusMsg"] == "RevertInstruction":
        return jsonify({"ErrorMsg": "RevertInstruction"}), 404
    user = User.query.filter(User.privkey==user_privkey).first()
    user.chainnumber = chainNumber
    db.session.commit()
    user1 = User.query.filter(User.privkey==user_privkey).first()
    return jsonify(r_sign), 200


@csrf_protect.exempt
@admin_bp.route("/vehicle/reback/<string:user_privkey>/<int:chainNumber>", methods=["GET", "POST"])
def reback_vehicle(user_privkey, chainNumber):
    link_url = CARRENT_URL + "/vehicle/reback/" + user_privkey + "/" + str(chainNumber)
    r_reback = requests.get(link_url).json()

    user = User.query.filter(User.privkey==user_privkey).first()
    user.chainnumber = -1
    db.session.commit()
    return jsonify(r_reback), 200

@csrf_protect.exempt
@admin_bp.route("/vehicle/new", methods=["GET", "POST"])
def new_vehicle():
    data = request.get_json()
    carowner_privkey = data["privateKey"]
    number = data["number"]
    brand = data["brand"]
    color = data["color"]
    quality = data["quality"]
    price = int(data["price"])
    day = int(data["day"])
    new_car = CARCNT(carowner_privkey=carowner_privkey)
    db.session.add(new_car)
    db.session.commit()
    chainNumber = new_car.chainNumber
    link_url = CARRENT_URL + "/vehicle/new/" + carowner_privkey

    data = {
        "chainNumber": chainNumber,
        "number": number,
        "brand": brand,
        "color": color,
        "quality": quality,
        "price": price,
        "day": day
    }
    r_new = requests.post(link_url, headers=REQUEST_HEADER, json=data).json()
    carowner = User.query.filter(User.privkey==carowner_privkey).first()
    carowner.chainnumber = chainNumber
    db.session.commit()
    return jsonify(r_new), 200
# {'privateKey': '1fae74a3779b262744af806be36363acac2570846641b464b5bcb8636acd90a7', 'number': '浙A1231', 'brand': '宝马', 'color': '红', 'quality': 'A', 'price': '888', 'day': '21'}

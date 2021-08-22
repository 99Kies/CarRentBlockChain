from flask import render_template, request, flash, redirect, url_for,  jsonify, Blueprint
from flask_login import login_required, current_user, login_user, logout_user

from CarRentBlockChain.extensions import db, csrf_protect
from CarRentBlockChain.config import Config

import random
import time
from ecdsa import SigningKey, SECP256k1
from pprint import pprint

carrent = Blueprint('carrent', __name__)


@carrent.route("/adminmain")
@login_required
def adminmain():
    return render_template("car/view/AdminMain.html")


@carrent.route("/carownermain")
@login_required
def carownermain():
    return render_template("car/view/CarOwnerMain.html")


@carrent.route("/usermain")
@login_required
def usermain():
    return render_template("car/view/UserMain.html")


# @carrent.route("/")
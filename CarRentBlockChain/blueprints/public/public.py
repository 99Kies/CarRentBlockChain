# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    render_template_string
)
from flask_login import login_required, login_user, logout_user, current_user

from CarRentBlockChain.extensions import login_manager
from CarRentBlockChain.blueprints.public.forms import RegisterForm, LoginForm
from CarRentBlockChain.blueprints.public.models import User
from CarRentBlockChain.webutils import flash_errors, redirect_back
from CarRentBlockChain.extensions import db
from CarRentBlockChain.privkeyutils.privkeyutils import create_random_address
from CarRentBlockChain.settings import CARRENT_URL, REQUEST_HEADER
import requests
import json
from flask_cors import CORS

public_bp = Blueprint("public", __name__, static_folder="../static")

CORS(public_bp)
Identity_Status = {
    1: "CarOwner",
    2: "User",
}

@public_bp.route("/", methods=["GET", "POST"])
@login_required
def home():
    """Home page."""
    return render_template("public/home.html")


@public_bp.route("/logout/")
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("public.home"))



@public_bp.route('/login', methods=['GET', 'POST'])
def login():
    # login in func
    if current_user.is_authenticated:
        return redirect(url_for('public.home'))

    form = LoginForm()
    if form.validate_on_submit():
        username_or_email = form.username.data
        password = form.password.data
        # remember = form.remember.data
        user = [User.query.filter(User.username==username_or_email).first(), User.query.filter(User.email==username_or_email).first()]
        if user[0]:
            if user[0].check_password(password):
                # login_user(user[0], remember)
                login_user(user[0])
                flash('Welcome back.', 'info')
                return redirect_back()
            else:
                flash('?????????????????????????????????????????????', 'warning')
        elif user[1]:
            if user[1].check_password(password):
                login_user(user[1])
                flash('Welcome back.', 'info')
                return redirect_back()
            else:
                flash('?????????????????????????????????????????????', 'warning')    
        else:
            flash('No account.', 'warning')
    return render_template('public/login.html', form=form)


@public_bp.route("/register/", methods=["GET", "POST"])
def register():
    """Register new user."""
    if current_user.is_authenticated:
        return redirect(url_for('public.home'))
        
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        password1 = form.confirm.data
        iphonenumber = form.iphone.data
        idcard = form.idcard.data
        status = form.status.data
        if not all([username, email, password, password1, iphonenumber, idcard, status]):
            flash('????????????????????????', "warning")
        elif password != password1:
            flash('??????????????????????????????????????????', "warning")
        elif User.query.filter(User.username==username).first():
            flash('???????????????????????????????????????', "warning")
        elif User.query.filter(User.email==email).first():
            flash('????????????????????????????????????', "warning")
        else:

            addr_msg = create_random_address()
            new_user = User(username=username, email=email, active=False, id=None, privkey=addr_msg["privateKeyHex"][2:],
                            iphone=iphonenumber, idcard=idcard, status=Identity_Status[status], privatekey_hex=addr_msg["privateKeyHex"],
                              privatekey_int=addr_msg["privateKeyInt"], publickey_hex=addr_msg["publicKeyHex"],
                              publickey_int=addr_msg["publicKeyInt"], address=addr_msg["address"])

            if Identity_Status[status] == "User":
                link_url = CARRENT_URL + "/user/add"
                data = {
                    "address": new_user.address
                }
                r_user = requests.post(link_url, headers=REQUEST_HEADER,  json=data)

            if Identity_Status[status] == "CarOwner":
                link_url = CARRENT_URL + "/carowner/add"
                data = {
                    "address": new_user.address
                }
                r_carowner = requests.post(link_url, headers=REQUEST_HEADER,  json=data)

            # add a User(active = False)
            new_user.set_password(password)
            db.session.add(new_user)
            # try:
            #     db.session.commit()
                
            #     return redirect(url_for('public.home'))
            # except:
            #     flash("???????????????????????????")
            #     db.session.rollback()
            db.session.commit()
            flash("????????????????????????????????????????????????", "success")
            return redirect(url_for('public.login'))
    return render_template('public/register.html', form=form)

@public_bp.route("/about/")
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)

@public_bp.route("/Identity_manager/", methods=["GET", "POST"])
def Identity_manager():
    """Identity_manager page."""
    form = LoginForm(request.form)
    return render_template("public/Identity_manager.html", form=form)

@public_bp.route("/tables_data", methods=["GET", "POST"])
def tables_data():
    return render_template("public/tables_data.html")

@public_bp.route("/certificate", methods=["GET", "POST"])
def certificate():
    return render_template("public/certificate.html")
@public_bp.route("/Visualization_tools/")
def Visualization_tools():
    """Visualization_tools page."""
    form = LoginForm(request.form)
    return render_template("public/visualization_tools.html", form=form)
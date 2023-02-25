from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user

menu = Blueprint('menu', __name__)

@menu.route('/', methods=['GET','POST'])
def homepage():
    return render_template("menu.html", user=current_user)


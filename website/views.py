from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
def homepage():
    return render_template("homepage.html", user=current_user)
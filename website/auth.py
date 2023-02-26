from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
from password_validator import PasswordValidator
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)
schema = PasswordValidator()
schema.min(8).max(50).has().uppercase().has().lowercase().has().digits()


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.homepage'))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            try:
                if check_password_hash(user.password, password):
                    flash("Logged in successfully", category="success")
                    login_user(user, remember=True)
                    return redirect(url_for("views.homepage"))
            except ValueError:
                pass

        flash("Incorrect email or password", category="error")

    return render_template("login.html", user=current_user), 200



@auth.route("/logout", methods=["GET", "POST"])
@login_required
def signup():
    if request.method == "POST":
        data = request.form
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        # Check if the email already exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists", category="error")
            return redirect(url_for("views.signup"))

        # Validate the email address
        try:
            email = validate_email(email)
        except EmailNotValidError as e:
            flash(str(e), category="error")
            return redirect(url_for("views.signup"))

        # Check password complexity
        if not schema.validate(password):
            flash(
                "Make sure password has at least 8 characters, 1 uppercase, 1 lowercase, 1 digit",
                category="error",
            )
            return redirect(url_for("views.signup"))

        # Check password and confirm_password match
        if password != confirm_password:
            flash("Passwords do not match", category="error")
            return redirect(url_for("views.signup"))

        # Create a new user and save it to the database
        try:
            new_user = User(
                email=email,
                password=generate_password_hash(password, method="sha256")
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created", category="success")
            return redirect(url_for("views.homepage"))
        except Exception as e:
            flash(str(e), category="error")
            db.session.rollback()

    return render_template("sign_up.html", user=current_user)
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
from password_validator import PasswordValidator
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__) 
schema = PasswordValidator()
schema.min(8).max(50).has().uppercase().has().lowercase().has().digits()

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        password = data.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.homepage'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exist', category='error')
    
    return render_template("login.html", user=current_user)

@auth.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', category='success')
    return redirect(url_for('views.homepage'))


@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        proceed = False
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Email already exists', category='error')
            pass
        
        try:
            validation = validate_email(email, check_deliverability=True)
            email = validation.email
            
            if password == confirm_password:
                if schema.validate(password):
                    print("Password is valid")
                    proceed = True
                else:
                    flash('Make sure password has at least 8 characters, 1 uppercase, 1 lowercase, 1 digit', category='error')
                    print("Password is invalid")
            else:
                print("Passwords do not match")
         
        except EmailNotValidError as e:
            flash('Email is invalid', category='error')
            print(str(e))
        
        if proceed:
            new_user = User(email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created', category='success')
            return redirect(url_for('views.homepage'))
        
    
    return render_template('sign_up.html', user=current_user)
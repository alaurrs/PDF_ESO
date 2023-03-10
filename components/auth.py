from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from .models import User
from flask_login import login_user,login_required, logout_user
from .test import extract_information
import json
import plotly.graph_objects as go
import plotly
import os

auth = Blueprint('auth', __name__)

UPLOAD_FOLDER = os.path.join("components","files")
ALLOWED_EXTENSIONS = {'pdf'}

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    return redirect(url_for('auth.login'))

@auth.route('/upload')
@login_required
def upload():
    return render_template('upload.html')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route('/upload', methods=['POST'])
@login_required
def upload_post():
    if request.method == 'POST':  
        f = request.files['file']
        if f.filename == '':
            flash('S??lectionnez un fichier !')
            return redirect(request.url)
        if not (allowed_file(f.filename)):
            flash('Extension de fichier invalide !')
            return redirect(request.url)
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            file_path = os.path.join(UPLOAD_FOLDER,filename)
            f.save(file_path)
            fig = extract_information(file_path)
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template("result.html", graphJSON = graphJSON,name = filename)  
    return 'Extension non autoris??e'
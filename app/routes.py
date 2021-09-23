from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from types import SimpleNamespace
from fastai.vision.all import *
import datetime
from app import app, db
from app.models import User
from app.forms import LoginForm, RegistrationForm, FileUploadForm, ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email, send_email
from app.token import generate_confirmation_token, confirm_token


#View function for the index page/home page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


#View function for the registration page
@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, registered_on=datetime.datetime.now(), confirmed=False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(subject, app.config['MAIL_USERNAME'], [user.email], html, html)
        flash('A confirmation email has been sent via email', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


#View function for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('You are successfully logged in', 'success')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


#View function for the inference page where you upload a passport photo of an adult or child
#Photo should be preferably 128 x 128 pixels, as the model was trained with the photos with those dimensions
@app.route('/inference', methods=['GET','POST'])
@login_required
def infer():
    #We first load the exported fastai model we'll be using, in this case it's child_or_not.pkl which has 85% accuracy on passport photos
    learner = load_learner(os.path.abspath(os.path.dirname(__file__)) + '/' + 'child_or_not.pkl')

    upload_form = FileUploadForm()
    if not current_user.confirmed:
        flash('Please confirm your email address to be able to use the Inference service', 'error')
        return redirect(url_for('index'))
    if upload_form.validate_on_submit():
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(app.config['UPLOAD_PATH'] + filename)
        uploader = SimpleNamespace(data = [app.config['UPLOAD_PATH'] + filename])
        img = PILImage.create(uploader.data[0])
        pred_class,_,_ = learner.predict(img)
        if pred_class == 'Adult':
            flash('The uploaded picture is of an {}'.format(pred_class), 'success' )
        else:
            flash('The uploaded picture is of a {}'.format(pred_class), 'success' )
        return redirect(url_for('infer'))
    return render_template('inference.html', form=upload_form, title='Perform Inference')


#View function for the logout functionality
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


#View function for the page where users enter their email to be sent the password reset link
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash("Check your email for the instructions to reset your password", 'success')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)


#View function for the password reset page, where users enter their new password
@app.route('/reset_password/<token>', methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset", 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


#View function for that handles the user email confirmation
#Users must confirm their email to be able to use the inference service
@app.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is Invalid or has expired', 'error')
    user = User.query.filter_by(email=email).first()
    if user.confirmed:
        flash('Account has already been confirmed please login', 'error')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('Thank you for confirming your account', 'success')
    return redirect(url_for('index'))

from .models import User,Task,db
from flask import render_template,redirect,url_for,flash,Blueprint,request
from .forms import RegisterForm
from werkzeug.security import generate_password_hash

views=Blueprint('views',__name__)
@views.route('/')
@views.route('/home')
def home_page():
    return render_template('home.html')

@views.route('/register',methods=['GET','POST'])
def register_page():
    form=RegisterForm()
    if form.validate_on_submit():
        hashed_password=generate_password_hash(form.password1.data)     #hashing the pass

        user_to_create=User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        try:
            db.session.add(user_to_create)
            db.session.commit()
            flash(f'Account created successfully! You can now login.',category='success')
            return redirect(url_for('login_page'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your account. Please try again.',category='danger')
    if form.errors:
        for field,errors in form.errors.items():
            for error in errors:
                flash(f"{error}",category='danger')

@views.route('/login' )
def login_page():
    return render_template('login.html')
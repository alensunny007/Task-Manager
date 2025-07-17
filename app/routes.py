from .models import User,Task,db
from flask import render_template,redirect,url_for,flash,Blueprint,session
from .forms import RegisterForm,LoginForm
from werkzeug.security import generate_password_hash,check_password_hash

views=Blueprint('views',__name__)

def login_required(f):
    def wrapper(*args,**kwargs):
        if 'user_id'not in session:
            flash('Please log in to access the dashboard.',category='danger')
            return redirect(url_for('views.login_page'))
        return f(*args,**kwargs)
    wrapper.__name__=f.__name__
    return wrapper


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
            return redirect(url_for('views.login_page'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your account. Please try again.',category='danger')
    else:
        if form.errors:
            for field,errors in form.errors.items():
                for error in errors:
                    flash(f"{error}",category='danger')
    return render_template('register.html',form=form)

@views.route('/login',methods=['GET','POST'])
def login_page():
    form=LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        user=User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password,password):
            session['user_id']=user.id
            session['username']=user.username
            session['email']=user.email
            flash('Login Successfull !',category='success')
            return redirect(url_for('views.dashboard_page'))
        else:
            flash('Invalid username or password.',category='danger')
    return render_template('login.html',form=form)

@views.route('/dashboard')
@login_required
def dashboard_page():
    return render_template('dashboard.html')


@views.route('/logout')
def logout_page():
    session.clear()
    flash('You have been logged out!',category='success')
    return redirect(url_for('views.login_page'))


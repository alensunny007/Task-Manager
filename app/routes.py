from .models import User,Task,db
from flask import render_template,redirect,url_for,flash,Blueprint,session,request,get_flashed_messages
from .forms import RegisterForm,LoginForm,ForgotPasswordForm,ResetPasswordForm,TaskForm
from werkzeug.security import generate_password_hash,check_password_hash
from .utiils import generate_reset_token,verify_reset_token,send_reset_email
from datetime import datetime
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
    if 'user_id' in session:
        return redirect(url_for('views.dashboard_page'))
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

@views.route('/forgot-password',methods=['GET','POST'])
def forgot_password():
    form=ForgotPasswordForm()
    if form.validate_on_submit():
        email=form.email.data
        user=User.query.filter_by(email=email).first()
        if user:
            token=generate_reset_token(email)
            reset_url=url_for('views.reset_password',token=token,_external=True)

            try:
                send_reset_email(email,reset_url)
                flash('Password reset email sent. Check your inbox',category='success')
            except Exception as e:
                flash('Error sending email. Please try again.',category='danger')
        else:
            flash('If that email exist, a reset link has been sent.',category='info')
        return redirect(url_for('views.login_page'))
    return render_template('forgot_password.html',form=form)

@views.route('/reset_password/<token>',methods=['GET','POST'])
def reset_password(token):
    email=verify_reset_token(token)
    if not email:
        flash("Invalid or expired reset link",category="danger")
        return redirect(url_for('views.forgot_password'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=email).first()
        if user:
            user.password=generate_password_hash(form.password.data)
            db.session.commit()
            flash('Your password has been reset successfully',category='success')
            return redirect(url_for('views.login_page'))
        else:
            flash("User not found",category='danger')
            return redirect(url_for('views.forgot_password'))
    return render_template('reset_password.html',form=form,token=token)


@views.route('/dashboard')
@login_required
def dashboard_page():
    get_flashed_messages()
    tasks=Task.query.filter_by(user_id=session['user_id']).order_by(Task.created_at.desc()).all()
    total_tasks=Task.query.filter_by(user_id=session['user_id']).count()
    completed_tasks=Task.query.filter_by(user_id=session['user_id'],completed=True).count()
    pending_tasks=Task.query.filter_by(user_id=session['user_id'],completed=False).count()
    overdue_tasks=Task.query.filter_by(user_id=session['user_id'],completed=False).filter(Task.due_date<datetime.now()).count()
    return render_template('dashboard.html',
    tasks=tasks,total_tasks=total_tasks,completed_tasks=completed_tasks,pending_tasks=pending_tasks,overdue_tasks=overdue_tasks)


@views.route('/logout')
def logout_page():
    session.clear()
    flash('You have been logged out!',category='success')
    return redirect(url_for('views.login_page'))


@views.route('/new_task',methods=['GET','POST'])
@login_required
def new_task():
    form=TaskForm()
    if form.validate_on_submit():
        due_date = datetime.combine(form.due_date.data, datetime.min.time())
        task=Task(
            title=form.title.data,
            descp=form.descp.data,
            due_date=due_date,
            priority=form.priority.data,
            user_id=session['user_id'],
            completed=False
        )
        try:
            db.session.add(task)
            db.session.commit()
            flash('Task created successfully!',category='success')
            return redirect(url_for('views.dashboard_page'))
        except Exception as e:
            db.session.rollback()
            flash('Eroor creating task. Please try again',category='danger')
    return render_template('new_task.html',form=form)
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DateField,SelectField,TextAreaField
from wtforms.validators import DataRequired,Email,Length,EqualTo,ValidationError
from .models import User

class RegisterForm(FlaskForm):
    def validate_username(self,username_to_check):
        user=User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try different username')
    def validate_email(self,email_to_check):
        email=User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email already exists! Try different Email')
        
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(),DataRequired()])
    password1=PasswordField(label='Password:',validators=[Length(min=6),DataRequired()])
    password2=PasswordField(label='Confirm Password:',validators=[EqualTo('password1'),DataRequired()])
    submit=SubmitField(label='Submit')


class LoginForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=6)])
    submit=SubmitField('Submit')

class ForgotPasswordForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()])
    submit=SubmitField("Request Password Reset")

class ResetPasswordForm(FlaskForm):
    password=PasswordField("New Password",validators=[DataRequired(),Length(min=6)])
    confirm_password=PasswordField("Confirm New Password",validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField("Reset Password")

class TaskForm(FlaskForm):
    title=StringField("Task Title",validators=[DataRequired(),Length(min=1,max=100)])
    descp=TextAreaField("Description",validators=[DataRequired()])
    due_date=DateField('Due Date',validators=[DataRequired()],format='%Y-%m-%d')
    priority=SelectField('Priority',choices=[('Low','Low'),('Medium','Medium'),('High','High')],validators=[DataRequired()])
    submit=SubmitField("Create Task")

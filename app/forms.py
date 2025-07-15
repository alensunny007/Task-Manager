from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
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
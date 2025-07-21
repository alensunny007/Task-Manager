import os
from dotenv import load_dotenv   
# Load environment variables from .env file
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL")
    SECRET_KEY=os.getenv("SECRET_KEY")

    MAIL_SERVER=os.getenv('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT=int(os.getenv('MAIL_PORT') or 587)
    MAIL_USE_TLS= os.getenv('MAIL_USE_TLS','true').lower() in ['true','on','1']
    MAIL_USERNAME=os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER')

    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
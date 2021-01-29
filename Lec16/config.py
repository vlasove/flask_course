import os 

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}".format(
    #     user=os.environ.get("DB_USER"),
    #     pw=os.environ.get("DB_PASSWORD"),
    #     host=os.environ.get("DB_HOST"),
    #     port=os.environ.get("DB_PORT"),
    #     db=os.environ.get("DB_NAME")
    # )
    SERVER_NAME = "74c9a060575b.ngrok.io"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('USER_EMAIL_ADDRESS') # ваш адрес электронной почты
    MAIL_PASSWORD = os.environ.get('USER_EMAIL_PASSWORD') # ваш пароль от электронной почты
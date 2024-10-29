from flask import Flask
from public import public
from admin import admin
from user import user
from shop import shop
import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail



app=Flask(__name__)
app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(user)
app.register_blueprint(shop)

app.secret_key="ndknvknkl"


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'hariharan0987pp@gmail.com'
app.config['MAIL_PASSWORD'] = 'rjcbcumvkpqynpep'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)



app.run(debug=True)
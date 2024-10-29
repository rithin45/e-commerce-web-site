from flask import*
from database import*
from flask_mail import Mail, Message
import random
import string
import smtplib
from email.mime.text import MIMEText



from database import *

public=Blueprint('public',__name__)

@public.route('/')
def home():
    return render_template('index.html')

@public.route('/login', methods=['GET', 'POST'])
def login():
    if 'submit' in request.form:
        username = request.form['username']
        password = request.form['password']

        h = "select * from login where username='%s' and password='%s'" % (username, password)
        res = select(h)

        if res:
            session['lid'] = res[0]['login_id']
            if res[0]['user_type'] == 'admin':
                flash("Login successful!", "success")
                return redirect(url_for('admin.admin_home'))
            
            elif res[0]['user_type'] == 'user':
                g = "select * from users where login_id='%s'" % session['lid']
                res2 = select(g)
                if res2:
                    session['uid'] = res2[0]['user_id']
                    flash("Login successful! Welcome, User.", "success")
                    return redirect(url_for('user.user_home'))
                
            elif res[0]['user_type'] == 'pending':
                flash("Admin needs to accept your registration.", "error")
                return redirect(url_for('public.login'))
            
            elif res[0]['user_type'] == 'shop':
                b = "select * from shops where login_id='%s'" % session['lid']
                res3 = select(b)
                if res3:
                    session['sid'] = res3[0]['shop_id']
                    flash("Login successful! Welcome, Shop Owner.", "success")
                    return redirect(url_for('shop.shop_home'))
        else:
            flash("Incorrect username or password. Please try again.", "error")
            return redirect(url_for('public.login'))
    
    return render_template('login.html')


def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


@public.route('/user_register',methods=['get','post'])
def user_register():
    if 'submit' in request.form:
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        hname=request.form['hname']
        place=request.form['place']
        landmark=request.form['lmark']
        pincode=request.form['pcode']
        phone=request.form['pnum']
        email=request.form['email']
        username=request.form['username']
        password=request.form['password']
        
        a="select * from users where email='%s'"%(email)
        res=select(a)
        if res:
            flash("email already exists. Please choose a different email.", "error")
            return redirect(url_for("public.user_register"))
        
        # Generate OTP
        otp = generate_otp()

        # Send OTP to the user's email
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('hariharan0987pp@gmail.com', 'rjcbcumvkpqynpep')

            msg = MIMEText(f'Your OTP for registration is {otp}')
            msg['Subject'] = 'Your OTP for Registration'
            msg['To'] = email
            msg['From'] = 'hariharan0987pp@gmail.com'

            gmail.send_message(msg)
            gmail.quit()

            flash('An OTP has been sent to your email. Please enter it to complete your registration.')
        except smtplib.SMTPException as e:
            print("Couldn't send email: " + str(e))
            flash("Failed to send OTP. Please try again.")
            return redirect(url_for('public.user_register'))

        # Temporarily store user details and OTP in session
        session['user_details'] = {
            'first_name': firstname,
            'last_name': lastname,
            'house_name': hname,
            'place': place,
            'landmark': landmark,
            'pincode': pincode,         
            'phone': phone,
            'email': email,
            'username': username,
            'password': password
        }
        session['otp'] = otp


        return redirect(url_for('public.verify_otp'))
    return render_template('user_register.html')

@public.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        if 'verify' in request.form:
            entered_otp = request.form['otp']
            if entered_otp == session.get('otp'):
                user_details = session.get('user_details')
                if user_details:
                    fname=user_details['first_name']
                    lname=user_details['last_name']
                    hname=user_details['house_name']
                    place=user_details['place']
                    lmark=user_details['landmark']
                    pcode=user_details['pincode']
                    phone=user_details['phone']
                    email=user_details['email']
                    usernm=user_details['username']
                    passw=user_details['password']
                    d="insert into login values(null,'%s','%s','user')"%(usernm,passw)
                    res=insert(d)
                    s="insert into users values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(res,fname,lname,hname,place,lmark,pcode,phone,email)
                    insert(s)
                    flash("Successfully Registered. Login Now!")
                    session.pop('user_details', None)
                    session.pop('otp', None)
                    return redirect(url_for('public.login'))
            else:
                flash('Invalid OTP. Please try again.')
            

    return render_template('verify_otp.html')



@public.route('/shop_register',methods=['get','post'])
def shop_register():
    if 'register' in request.form:
        sname=request.form['sname']
        place=request.form['splace']
        landmark=request.form['slmark']
        phone=request.form['sphone']
        email=request.form['semail']
        username=request.form['susername']
        password=request.form['spassword']
        
        a="select * from login where username='%s'"%(username)
        res=select(a)
        if res:
            flash("Username already exists. Please choose a different username.", "error")
            return redirect(url_for("public.shop_register"))
        
        i="insert into login values(null,'%s','%s','pending')"%(username,password)
        res=insert(i)
        
        p="insert into shops values(null,'%s','%s','%s','%s','%s','%s','pending')"%(res,sname,place,landmark,phone,email)
        insert(p)
        flash("Created Successfully!!!", "success")

    return render_template('shop_register.html')
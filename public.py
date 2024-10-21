from flask import Flask,Blueprint,render_template,request,url_for,redirect,session

from database import *

public=Blueprint('public',__name__)

@public.route('/')
def home():
    return render_template('home.html')

@public.route('/login',methods=['get','post'])
def login():
    
    if 'submit' in request.form:
        username=request.form['username']
        password=request.form['password']
        
        h="select * from login where username='%s' and password='%s'"%(username,password)
        res=select(h)
        session['lid']=res[0]['login_id']
        if res:
            if res[0]['user_type']=='admin':
                return redirect(url_for('admin.admin_home'))
            elif res[0]['user_type']=='user':
                g="select * from users where login_id='%s'"%(session['lid'])
                res2=select(g)
                if res2:
                    session['uid']=res2[0]['user_id'] 
                    return redirect(url_for('user.user_home'))
                
            elif res[0]['user_type']=='pending':   
                return "Admin needs to accept!"    
            
            elif res[0]['user_type']=='shop':
                b="select * from shops where login_id='%s'"%(session['lid'])
                res3=select(b)
                if res3:
                    session['sid']=res3[0]['shop_id']
                    return redirect(url_for('shop.shop_home'))
        else:
            return "incorrect username or password!!!!"
            
    
        
    
    return render_template('login.html')

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
        i="insert into login values (null,'%s','%s','user')"%(username,password)
        res=insert(i)
        
        p="insert into users values(null,'%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(res,firstname,lastname,hname,place,landmark,pincode,phone,email)
        insert(p)
        
    return render_template('user_register.html')


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
        
        i="insert into login values(null,'%s','%s','pending')"%(username,password)
        res=insert(i)
        
        p="insert into shops values(null,'%s','%s','%s','%s','%s','%s','pending')"%(res,sname,place,landmark,phone,email)
        insert(p)
    return render_template('shop_register.html')
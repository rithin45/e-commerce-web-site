from flask import Flask, Blueprint,render_template,request,redirect,url_for,session

import uuid
from database import *

admin=Blueprint('admin',__name__)


@admin.route('/admin_home')
def admin_home():
    return render_template('admin_home.html')


@admin.route('/admin_category',methods=['get','post'])
def admin_category():
    data={}
    if 'insert' in request.form:
        category=request.form['category']
        i="insert into product_category values(null,'%s')"%(category)
        insert(i)
        
    f="select * from product_category"
    data['view']=select(f)
    
    if  'action' in request.args:
        action=request.args['action']
        catid=request.args['catid']
    else:
        action=None
        
    if action =='update':
        d="select * from product_category where category_id=%s"% catid
        data['de']=select(d)
    
    if 'update' in request.form:
        category=request.form['category']
        g="update product_category set category_name='%s' where category_id='%s'"%(category,catid)
        update(g)
        return redirect(url_for('admin.admin_category'))
    if action=='delete':
        h="delete from product_category where category_id='%s'"%(catid)
        delete(h)
        return redirect(url_for('admin.admin_category'))

        
    return render_template('admin_category.html',data=data)


@admin.route('/admin_shopview')
def admin_shopview():
    data={}
    p="select * from shops"
    data['view']=select(p)
    if 'action' in request.args:
        action=request.args['action']
        sid=request.args['sid']
        lid=request.args['lid']
    else:
        action=None
    
    if action=='accept':
        q="update shops set status='accept' where shop_id='%s'"%(sid)
        update(q)
        w="update login set user_type='shop' where login_id='%s'"%(lid)
        update(w)
        return redirect(url_for('admin.admin_shopview'))
    
    if action=='reject':
        r="delete from shops where shop_id='%s'"%(sid)
        delete(r)
        t="delete from login where login_id='%s'"%(lid)
        delete(t)
        return redirect(url_for('admin.admin_shopview'))
        
    return render_template('admin_shopview.html',data=data)


@admin.route('/admin_vendors',methods=['get','post'])
def admin_vendors():
    data={}
    if 'submit' in request.form:
        cname=request.form['cname']
        details=request.form['details']
        estyr=request.form['eyear']
        q="insert into vendors values(null,'%s','%s','%s')"%(cname,details,estyr)
        insert(q)
        
    f="select * from vendors"
    data['vview']=select(f)
    
    if 'action' in request.args:
        action=request.args['action']
        cid=request.args['cid']
    else:
        action=None
    
    if action=='update':
        w="select * from vendors where vendor_id=%s"% cid
        data['qw']=select(w)
    
    if 'update' in request.form:
        cname=request.form['cname']
        details=request.form['details']
        estyr=request.form['eyear']
        e="update vendors set company_name='%s',details='%s',est_year='%s' where vendor_id='%s'"%(cname,details,estyr,cid)
        update(e)
        return redirect(url_for('admin.admin_vendors'))
    if action=='delete':
        d="delete from vendors where vendor_id='%s'"%(cid)
        delete(d)
        return redirect(url_for('admin.admin_vendors'))
        
    
    return render_template('admin_vendors.html',data=data)

@admin.route('/admin_products',methods=['get','post'])
def admin_products():
    data={}
    j="select * from products inner join product_category using(category_id) inner join vendors using (vendor_id) inner join shops using(shop_id)"
    data['pview']=select(j)    
    return render_template('admin_products.html',data=data)


@admin.route('/admin_stock',methods=['get','post'])
def admin_stock():
    data={}    
    p="select * from stocks inner join products using (product_id)"
    data['ty']=select(p)
       
    return render_template('admin_stock.html',data=data)


@admin.route('/admin_userview',methods=['get','post'])
def admin_userview():
    data={}
    o="select * from users"
    data['qw']=select(o)
    return render_template('admin_userview.html',data=data)

@admin.route('/admin_complaintview',methods=['get','post'])
def admin_complaintview():
    data={}
    
    q="select * from complaints"
    data['dr']=select(q)
    
    return render_template('admin_complaintview.html',data=data)

@admin.route('/admin_reply',methods=['get','post'])
def admin_reply():
    if 'submit' in request.form:
        compid=request.args['cid']
        reply=request.form['reply']
        
        u="update complaints set reply='%s' where complaint_id='%s'"%(reply,compid)
        update(u)
        return redirect(url_for('admin.admin_complaintview'))
        
    return render_template('admin_reply.html')


@admin.route('/admin_chat',methods=['get','post'])
def admin_chat():
    data={}
    data['lid']=session['lid']
    uid=request.args['uid']
    if'submit' in request.form:
        chat=request.form['msg']
        i="insert into message values (null,'%s','%s','admin','user','%s',curdate())"%(session['lid'],uid,chat)
        insert(i)
        return redirect(url_for('admin.admin_chat',uid=uid))
        
    r="select * from message where sender_id='%s' and reciver_id='%s' or sender_id='%s' and reciver_id='%s'"%(session['lid'],uid,uid,session['lid'])
    data['msg']=select(r)
    print(r)
    
    return render_template('chat_s.html',data=data)

@admin.route('/admin_shop_chat',methods=['get','post'])
def admin_shop_chat():
    data={}
    data['lid']=session['lid']
    aid = request.args['aid']
    if'submit' in request.form:
        chat=request.form['msg']
        i="insert into message values (null,'%s','%s','admin','shop','%s',curdate())"%(session['lid'],aid,chat)
        insert(i)
        return redirect(url_for('admin.admin_shop_chat',aid=aid))
    
    r="select * from message where sender_id='%s' and reciver_id='%s' or sender_id='%s' and reciver_id='%s'"%(session['lid'],aid,aid,session['lid'])
    data['msww']=select(r)
    print(r)
    return render_template('admin_shop_chat.html',data=data)
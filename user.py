from flask import Flask, Blueprint,render_template,request,redirect,url_for,session
import uuid

from database import *


user=Blueprint('user',__name__)


@user.route('/user_home')
def user_home():
    return render_template('user_home.html')

@user.route('/user_complaint',methods=['get','post'])
def user_complaint():
    data={}
    f="select * from complaints where user_id='%s'"%(session['uid'])
    data['dr']=select(f)
    if 'submit' in request.form:
        complaint=request.form['complaint']
        complaint=complaint.replace("'","''")
        p="insert into complaints values(null,'%s','%s','pending',curdate())"%(session['uid'],complaint) 
        insert(p)
        return redirect(url_for('user.user_complaint'))
    return render_template('user_complaint.html',data=data)


@user.route('/user_products_view',methods=['get','post'])
def user_product_view():
    data={}
    
    if 'search' in request.form:
        search='%'+request.form['search']+'%'
        f="select * from products inner join product_category using(category_id) inner join vendors using(vendor_id) inner join shops using(shop_id) where product_name like'%s' or category_name like'%s'"%(search,search)
        data['qw']=select(f)
    else:
        i="select * from products inner join product_category using(category_id) inner join vendors using(vendor_id) inner join shops using(shop_id)"
        data['qw']=select(i)
    return render_template('user_product_view.html',data=data)

@user.route('/user_view_cart',methods=['get','post'])
def user_view_cart():
    data={}
    if 'pid' in request.args:
        pvalue=request.args['pid']
        e="select * from products inner join shops using(shop_id) where product_id='%s'"%(pvalue)
        data['wr']=select(e)
    if 'submit' in request.form:
        shop=request.form['shop_id']
        amount=request.form['amount']
        product=request.form['productid']
        qty=request.form['quantity']
        total=request.form['total']
        i="insert into order_master values (null,'%s','%s',curdate(),'%s','pending')"%(session['uid'],shop,total)
        res=insert(i)
        j="insert into order_details values(null,'%s','%s','%s','%s')"%(res,product,qty,amount)
        insert(j)
        return redirect(url_for('user.user_product_view'))
    
    if 'mid' in request.args:
        mid=request.args['mid']
        g="select * from products inner join order_details using(product_id) inner join shops using(shop_id) where order_master_id='%s'"%(mid)
        data['ww']=select(g)
    if 'update' in request.form:
        qty=request.form['quantity']
        total=request.form['total']
        
        j="update order_master set total='%s' where order_master_id='%s'"%(total,mid)
        update(j)
        o="update order_details set quantity='%s' where order_master_id='%s'"%(qty,mid)
        update(o)
        return redirect(url_for('user.user_cart'))
                
    return render_template('user_view_cart.html',data=data)

@user.route('/user_cart',methods=['get','post'])
def user_cart():
    data={}
    a="select * from order_master inner join shops using(shop_id) where status_s != 'Order Confirmed' and status_s!='Delivered' and user_id='%s'"%(session['uid'])
    data['vve']=select(a)
    if 'action' in request.args:
        action=request.args['action']
        mid=request.args['mid']
    else:
        action=None   
    if action=='remove':
        r="delete from order_master where order_master_id='%s'"%(mid)
        delete(r)
        return redirect(url_for('user.user_cart'))
    return render_template('user_cart.html',data=data)

@user.route('/user_payment',methods=['get','post'])
def user_payment():
    data={}
    mids=request.args['mid']
    p="select * from order_details inner join order_master using (order_master_id) where order_details_id='%s'"%(mids)
    data['vv']=select(p)
    if 'submit' in request.form:
        cname=request.form['cname']
        cnum=request.form['cnumber']
        expdate=request.form['edate']
        cvvv=request.form['cvv']
        amount=request.form['amount']
        r="insert into payment values(null,'%s','%s','%s','%s','%s','%s')"%(mids,cname,cnum,expdate,cvvv,amount)
        insert(r)
        u="update order_master set status_s='Order Confirmed' where order_master_id='%s'"%(mids)
        update(u)
        return redirect(url_for('user.user_cart'))
        
    return render_template('/user_payment.html',data=data)

@user.route('/user_rating',methods=['get','post'])
def user_rating():
    data={}
    oid=request.args['oid']
    f="select * from order_details inner join products using (product_id) where order_details_id='%s'"%(oid)
    data['pi']=select(f)
    
    if data['pi']:
        product_id=data['pi'][0]['product_id']
        y="select * from ratings inner join products using (product_id) where product_id='%s'"%(product_id)
        data['dd']=select(y)
  
    if 'submit' in request.form:
        product=request.form['pname']
        rate=request.form['rate']
        review=request.form['review']
        p="insert into ratings values(null,'%s','%s','%s','%s',curdate())"%(session['uid'],product,rate,review)
        insert(p)
        return redirect(url_for('user.user_rating',oid=oid))
    return render_template('user_rating.html',data=data)

@user.route('/user_order_history',methods=['get','post'])
def user_order_history():
    data={}
    j="select * from order_master inner join shops using(shop_id) where user_id='%s'"%(session['uid'])
    data['dd']=select(j)
    
    return render_template('user_order_history.html',data=data)

@user.route('/user_order_details',methods=['get','post'])
def user_order_details():
    data={}
    oids=request.args['oid']
    k="select * from order_details inner join products using(product_id)  where order_details_id='%s'"%(oids)
    data['jj']=select(k)
    return render_template('user_order_details.html',data=data)

@user.route('/user_chat',methods=['get','post'])
def user_chat():
    data={}
    if'submit' in request.form:
        chat=request.form['msg']
        i="insert into message values(null,'%s','1','user','admin','%s',curdate())"%(session['lid'],chat)
        insert(i)
        return redirect(url_for('user.user_chat'))
    r="select * from message where (sender_id='1' and reciver_id='%s' or sender_id='%s' and reciver_id='1') "%(session['lid'],session['lid'])
    data['msw']=select(r)
    return render_template('user_chat.html',data=data)


@user.route('/user_shop_view')
def user_shop_view():
    data={}
    u="select * from shops where status!='pending'"
    data['viewss']=select(u)
    return render_template('user_shop_view.html',data=data)

@user.route('/user_shop_chat',methods=['get','post'])
def user_shop_chat():
    data={}
    sid=request.args['sid']
    data['lid']=session['lid']
    if'submit' in request.form:
        chat=request.form['msg']
        i="insert into message values(null,'%s','%s','user','shop','%s',curdate())"%(session['lid'],sid,chat)
        insert(i)
        return redirect(url_for('user.user_shop_chat',sid=sid))
    r="select * from message where sender_id='%s' and reciver_id='%s' or sender_id='%s' and reciver_id='%s' "%(session['lid'],sid,sid,session['lid'])
    data['msr']=select(r)
    print(r)
    
    return render_template('user_shop_chat.html',data=data)
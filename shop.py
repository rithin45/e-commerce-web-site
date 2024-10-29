from flask import Flask,Blueprint,render_template,request,redirect,url_for,session
import uuid
from database import *


shop=Blueprint('shop',__name__)


@shop.route('/shop_home')
def shop_home():
    return render_template('shop_home.html')

@shop.route('/shop_product_category')
def shop_product_category():
    data={}
    
    s="select * from product_category"
    data['re']=select(s)
    return render_template('shop_product_category.html',data=data)


@shop.route('/shop_products',methods=['get','post'])
def shop_products():
    data={}
    
    catid=request.args['catid']
    g="select * from product_category where category_id='%s'"%(catid)
    data['cid']=select(g)
    
    t="select * from vendors"
    data['vid']=select(t)
    
    l="select * from shops"
    data['sid']=select(l)
    
    if 'submit' in request.form:
        category=request.form['category_id']
        vendor=request.form['vendor_id']
        shop=request.form['shop_id']
        pname=request.form['pname']
        details=request.form['details']
        price=request.form['price']
        image=request.files['img']
        path="static/image/"+str(uuid.uuid4())+image.filename
        image.save(path)
        h="insert into products values(null,'%s','%s','%s','%s','%s','%s','%s')"%(category,vendor,shop,pname,details,price,path)
        ss=insert(h)
        w="insert into stocks values (null,'%s','%s',curdate())"%(ss,'0')
        insert(w)
        return redirect(url_for('shop.shop_products',catid=catid))

        
        
    u="select * from products inner join product_category using (category_id) inner join vendors using (vendor_id) inner join shops using (shop_id) where category_id='%s' and shop_id='%s'"%(catid,session['sid'])
    data['pview']=select(u)

    
    if 'action' in request.args:
        action=request.args['action']
        pid=request.args['pid']
        
    else:
        action=None
    
    if action=='update':
        v="select * from products inner join product_category using (category_id) inner join vendors using (vendor_id) inner join shops USING (shop_id) where product_id='%s'"%(pid)
        data['er']=select(v)
    
    if 'update' in request.form:
        category=request.form['category_id']
        vendor=request.form['vendor_id']
        shop=request.form['shop_id']
        pname=request.form['pname']
        details=request.form['details']
        price=request.form['price']
        images=request.files['img']
        path="static/image/"+str(uuid.uuid4())+images.filename
        images.save(path)
        f="update products set category_id ='%s', vendor_id='%s', shop_id='%s', product_name='%s', details='%s', price=%s, image='%s' where product_id='%s'"%(category,vendor,shop,pname,details,price,path,pid)
        update(f)
        return redirect(url_for('shop.shop_products',pid=pid,catid=catid))
    
    if action=='delete':
        q="delete from products where product_id='%s'"%(pid)
        delete(q)
        return redirect(url_for('shop.shop_products',pid=pid,catid=catid))
        
        
    return render_template('shop_products.html',data=data)

@shop.route('/shop_rating',methods=['get','post'])
def shop_rating():
    data={}
    productid = request.args['pid']
    l="select * from ratings inner join products using(product_id) where product_id='%s'"%(productid)
    data['qe']=select(l)
    return render_template('shop_view_ratings.html',data=data)

@shop.route('/shop_stock',methods=['get','post'])
def shop_stock():
    data={}
    pids=request.args['pid']
    g="select * from stocks inner join products using(product_id) where product_id='%s'" %(pids)
    data['rt']=select(g)

    if 'submit'in request.form:
        quantity=request.form['qty']
        e="update stocks set quantity=quantity+'%s' where product_id='%s'"%(quantity,pids)
        update(e)
        
    p="select * from stocks inner join products using(product_id) where product_id='%s'"%(pids)
    data['ty']=select(p)
       
    return render_template('shop_stock.html',data=data)


@shop.route('/shop_view_orders',methods=['get','post'])
def shop_view_orders():
    data={}
    
    h="select * from order_master inner join shops using (shop_id) where (status_s='Order Confirmed' or status_s='Delivered') and shop_id='%s'"%(session['sid'])
    data['dfd']=select(h)
    if 'action' in request.args:
        action=request.args['action']
        oids=request.args['oidd']
    else:
        action=None
    if action=='confirm':
        t="update order_master set status_s='Delivered' where order_master_id='%s'"%(oids)
        update(t)
        return redirect(url_for('shop.shop_view_orders'))
    return render_template('shop_view_orders.html',data=data)

@shop.route('/shop_view_users',methods=['get','post'])
def shop_view_users():
    data={}
    qw="select * from users "
    data['qw']=select(qw)
    return render_template('shop_view_users.html',data=data)


@shop.route('/shop_chat',methods=['get','post'])
def shop_chat():
    data={}
    ssid=request.args['ssid']
    data['lid']=session['lid']
    if'submit' in request.form:
        chat=request.form['msg']
        i="insert into message values(null,'%s','%s','shop','user','%s',curdate())"%(session['lid'],ssid,chat)
        insert(i)
        return redirect(url_for('shop.shop_chat',ssid=ssid))
    r="select * from message where sender_id='%s' and reciver_id='%s' or sender_id='%s' and reciver_id='%s' "%(session['lid'],ssid,ssid,session['lid'])
    data['msg']=select(r)
    print(r)
    return render_template('shop_chat.html',data=data)

@shop.route('/shop_admin_chat',methods=['get','post'])
def shop_admin_chat():
    data={}
    if'submit' in request.form:
        chat=request.form['msg']
        i="insert into message values(null,'%s','1','shop','admin','%s',curdate())"%(session['lid'],chat)
        insert(i)
        return redirect(url_for('shop.shop_admin_chat'))
    r="select * from message where (sender_id='1' and reciver_id='%s' or sender_id='%s' and reciver_id='1') "%(session['lid'],session['lid'])
    data['msw']=select(r)
    return render_template('shop_admin_chat.html',data=data)
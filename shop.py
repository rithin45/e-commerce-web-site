from flask import Flask,Blueprint,render_template,request,redirect,url_for
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
    cat=request.args['catid']
    g="select * from product_category where category_id='%s'"%(cat)
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
        
    u="select * from products inner join product_category using (category_id) inner join vendors using (vendor_id) inner join shops using (shop_id);"
    data['pview']=select(u)

    
    if 'action' in request.args:
        action=request.args['action']
        pid=request.args['pid']
    else:
        action=None
    
    if action=='update':
        v="select * FROM products inner join product_category using (category_id) inner join vendors using (vendor_id) inner join shops USING (shop_id) where product_id='%s'"%(pid)
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
        return redirect(url_for('shop.shop_products'))
    
    if action=='delete':
        q="delete from products where product_id='%s'"%(pid)
        delete(q)
        return redirect(url_for('shop.shop_products'))
        
        
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
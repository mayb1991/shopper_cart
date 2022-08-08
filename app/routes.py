from app import app, db
from flask import render_template, request, flash, redirect, url_for
from app.forms import ShopperInfo, LoginForm
from app.models import User, Product, Cart
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash


@app.route('/')
@app.route('/index')
def index():
    context = {
    'title': "Home",
    'products': Product.query.all()
    }
    return render_template('index.html', **context)

@app.route('/login', methods=['GET', 'POST'])
def login():
    title = "Login"
    form = LoginForm()
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is None or not check_password_hash(user.password, password):
            flash('Incorrect email/password. Please try again.', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data) 
        flash("You have successfully logged in!", "success")
        return redirect(url_for('cart'))
    return render_template('login.html', title=title, form=form)

@app.route('/product_info/<int:product_id>')
@login_required
def product_detail(product_id):
    product = Product.query.get(product_id)
    title = f'{product.name.upper()}'
    return render_template('product_info.html', product=product, title=title) 

@app.route('/mycart/add/<int:product_id>', methods=['GET', 'POST'])
@login_required
def addtocart(product_id):
    product = Product.query.get(product_id)
    product_key = product.id
    user_key = current_user.id
    new_product_in_cart = Cart(user_key, product_key)
    db.session.add(new_product_in_cart)
    db.session.commit()
    flash(f"{ product.name } has been added to your cart!", "info")
    return redirect(url_for('cart'))

@app.route('/mycart', methods=['GET', 'POST'])
@login_required
def cart():
    context = {
    'title': "Your Cart",
    'items': Cart.query.filter(Cart.user_id==current_user.id).all(),
    'total': 0.00
    }
    if not context['items']:
        return render_template('cart.html', **context)
    else:
        for item in context['items']:
            context['total'] += float(item.product_br.price)
    return render_template('cart.html', **context)

@app.route('/mycart/remove/<int:item_id>', methods=['GET','POST'])
@login_required
def remove_from_cart(item_id):
    item = Cart.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Item has been removed from your cart", "danger")
    return redirect(url_for('cart'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = ShopperInfo()
    if request.method == "POST" and form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        phone = form.phone.data
        email = form.email.data
        password = form.password.data
        new_shopper = User(first_name, last_name, username, phone, email, password)
        db.session.add(new_shopper)
        db.session.commit()
        flash("You're signed up!", 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out", 'primary')
    return redirect(url_for('index'))

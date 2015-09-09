import os
import stripe
from flask import Flask, render_template, request, redirect, url_for
from models import *
from mongoengine import connect

stripe_keys = {
    'secret_key': os.environ['SECRET_KEY'],
    'publishable_key': os.environ['PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET']
connect('computers_inc')

@app.route('/')
def index():
  return render_template('main/index.html')

@app.route('/about')
def about():
  return render_template('main/about.html')

@app.route('/contact')
def contact():
  return render_template('main/contact.html')

@app.route('/products')
def product_index():
  return render_template('products/products.html', products=Product.objects())

@app.route('/products/<product_id>')
def product_show(product_id):
  context = {
    'product': Product.objects.get(id=product_id),
    'key': stripe_keys['publishable_key']
  }
  return render_template('products/show.html', **context)

@app.route('/products/<product_id>/purchase', methods=['POST'])
def product_buy(product_id):
  product = Product.objects.get(id=product_id)
  # Amount in cents
  amount = int(product.price * 100)

  try:
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        card=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )
  except:
    pass

  return render_template('products/confirmation.html', product=product)

@app.route('/products/create', methods=['GET', 'POST'])
def product_create():
  if request.method == 'POST':
    Product(name=request.form['name'],
            description=request.form['description'],
            price=request.form['cost']).save()
    redirect(url_for('product_index'))

  return render_template('products/create.html')

app.run(debug=True)

from flask import Flask, escape, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SECRET_KEY'] = 'something'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
admin = Admin(app, name='Foods')
db = SQLAlchemy(app)


class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	products = db.relationship('Food', backref='category')


class Food(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	name = db.Column(db.String(80), unique=True, nullable=False)
	img_url = db.Column(db.String(500), unique=False, nullable=False)
	description = db.Column(db.String(1500), unique=False, nullable=False)
	cost = db.Column(db.Integer, nullable=True)
	baskets = db.relationship('Basket', backref='food')

	
class Basket(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	product_id = db.Column(db.Integer, db.ForeignKey('food.id'))
	name = db.Column(db.String(80),  nullable=False)
	img_url = db.Column(db.String(500),  nullable=False)
	description = db.Column(db.String(1500),  nullable=False)
	cost = db.Column(db.Integer, nullable=True)
	
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Food, db.session))
admin.add_view(ModelView(Basket, db.session))
	
@app.route('/')
def index():
	categories = Category.query.all()
	return render_template("index.html", categories=categories)
	
@app.route('/category/<id>')
def category(id):
	category= Category.query.get(id)
	return render_template("products.html", category=category)

@app.route('/product/<id>')
def food(id):
	food= Food.query.get(id)
	return render_template("product.html", food=food)
	
@app.route('/basket_adding', methods=['POST'])
def add():
	product_idd = request.form["product_id"]
	name = request.form["name"]
	price = request.form["price"]
	new = Basket(name=name,product_id=product_idd,cost=price,img_url="#ww",description="123")
	db.session.add(new)
	db.session.commit()
	return "OK"
	
@app.route('/basket')
def basket():
	baskets = Basket.query.all()
	return render_template("cart.html", baskets=baskets)
	
@app.route('/about')
def about():
	return render_template("text-page.html")
	
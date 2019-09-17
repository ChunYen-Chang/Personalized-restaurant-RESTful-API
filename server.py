from flask import Flask, jsonify, request, g
from model import BaseModel, RestaurantInf, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from find_restaurant import findlocation, retrive_restaurant_inf
from passlib.apps import custom_app_context as pwd_context
from flask_httpauth import HTTPBasicAuth


google_key = 'your google API key'
foursquare_id = 'your foursquare API ID'
foursquare_password = 'your foursquare API password'


engine = create_engine("mysql+mysqlconnector://id:pw@ec2-54-68-247-255.us-west-2.compute.amazonaws.com:3306/restaurant")
DBSession = sessionmaker(bind=engine)
session = DBSession()


auth = HTTPBasicAuth()
app = Flask(__name__)


@auth.verify_password
def verify_password(username, password):
	user = session.query(User).filter_by(account = username).first()
	if not user:
		return False

	account = user.account
	hash_passowrd = user.password
	
	if not pwd_context.verify(password, hash_passowrd):
		return False
	g.user = user
	return True


@app.route('/user', methods = ['POST'])
def user_register():
	user_name = request.form['username']
	user_password= request.form['userpassword']
	user_password_hash = pwd_context.encrypt(user_password)
	
	user = session.query(User).filter_by(account = user_name).first()
	if user:
		return 'The user exists'

	new_user = User(account=user_name,
			password=user_password_hash)
	session.add(new_user)
	session.commit()

	return 'Already registered a new user'


@app.route('/AllRestaurantInf', methods = ['GET', 'POST'])
@auth.login_required
def get_all_restaurants_inf():
	if request.method == 'GET':
		all_restaurant = session.query(RestaurantInf).all()
		all_restaurant_dict = {}
		for i in all_restaurant:
			all_restaurant_dict[i.restaurant_id] = {'name':i.name, 'address':i.address, 'photo':i.photo}
		return jsonify(all_restaurant_dict)
		
	elif request.method == 'POST':
		place = request.form['place']
		restaurant_coordinate = findlocation(place, google_key)
		restaurant_inf_dict = retrive_restaurant_inf(foursquare_id, foursquare_password, restaurant_coordinate[0], restaurant_coordinate[1])
				
		new_restaurant = RestaurantInf(name=str(restaurant_inf_dict['0']['name']), 
					address=str(restaurant_inf_dict['0']['addr']), 
					photo=str(restaurant_inf_dict['0']['img_url']))
		session.add(new_restaurant)
		session.commit()

		return 'Already uploaded a new restaurant to the database'


@app.route('/RestaurantInf/<int:onerestaurantid>', methods = ['GET','PUT', 'DELETE'])
@auth.login_required
def get_update_delete_restaurant(onerestaurantid):
	if request.method == 'GET':
		restaurant = session.query(RestaurantInf).filter_by(restaurant_id = onerestaurantid).one()
		restaurant_dict = {}
		restaurant_dict[restaurant.restaurant_id] = {'name':restaurant.name, 'address':restaurant.address, 'photo':restaurant.photo}	
		return jsonify(restaurant_dict)

	elif request.method == 'PUT':
		restaurant = session.query(RestaurantInf).filter_by(restaurant_id = onerestaurantid).one()
		name = request.form['name']
		address = request.form['address']
		photo = request.form['photo']
		if name:
			restaurant.name = name
		if address:
			restaurant.address = address
		if photo:
			restaurant.photo = photo
		session.commit()
		
		restaurant_dict = {}
		restaurant_dict[restaurant.restaurant_id] = {'name':restaurant.name, 'address':restaurant.address, 'photo':restaurant.photo}
		return jsonify(restaurant_dict)

	elif request.method == 'DELETE':
		restaurant = session.query(RestaurantInf).filter_by(restaurant_id = onerestaurantid).one()
		session.delete(restaurant)
		session.commit()
		return 'Deletion is done'


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=80)

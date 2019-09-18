# import packages
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.apps import custom_app_context as pwd_context
from model import BaseModel, RestaurantInf, User
from find_restaurant import findlocation, retrive_restaurant_inf


# define the setting for connecting to Google Geocoding API and foursquare API
google_key = 'your google API key'
foursquare_id = 'your foursquare API ID'
foursquare_password = 'your foursquare API password'


# connect to Mysql database and create a session
engine = create_engine("mysql+mysqlconnector://id:pw@ec2-54-68-247-255.us-west-2.compute.amazonaws.com:3306/restaurant")
DBSession = sessionmaker(bind=engine)
session = DBSession()


# declare a auth instance and Flask instance
auth = HTTPBasicAuth()
app = Flask(__name__)


@auth.verify_password
def verify_password(username, password):
	'''
	Description: This function allow flask server to check the username and userpassword 
				If the username does not exist in the Mysql database or the userpassword
				is not correct, the flask server won't allow this user to extract information.
				
	Parameters: -username: the username a user gives
				-password: the password a user gives
	
	Returns: -True: The username can be found in the Mysql database and the password is correct
			 -False: The username cannot be found in the Mysql database and the password isn't correct
	'''
	# extract a user's information based on the "username" that a user gives
	user = session.query(User).filter_by(account = username).first()
	
	# if username cannot be found in the database, return False
	if not user:
		return False

	# save this user's username and hashed password from in account and hash_passowrd variable
	account = user.account
	hash_passowrd = user.password
	
	# if userpassword is not correct, return False
	if not pwd_context.verify(password, hash_passowrd):
		return False

	return True


@app.route('/user', methods = ['POST'])
def user_register():
	'''
	Description: This function allow users to register their account in Mysql database
				
	Parameters: None
	
	Returns: None
	'''
	# extract username and userpassword information from request.form
	user_name = request.form['username']
	user_password= request.form['userpassword']
	
	# use pwd_context.hash function to convert password into hashed_password 
	user_password_hash = pwd_context.hash(user_password)
	
	# connect to Mysql and check whether this user_name exists or not.
	user = session.query(User).filter_by(account = user_name).first()
	if user:
		return 'The user exists'

	# save this new username and userpassword into the Mysql database
	new_user = User(account=user_name,
			password=user_password_hash)
	session.add(new_user)
	session.commit()

	return 'Already registered a new user'


@app.route('/AllRestaurantInf', methods = ['GET', 'POST'])
@auth.login_required
def get_all_restaurants_inf():
	'''
	Description: This function allow users to get all restaurant information from the Mysql database
				It also allow users to put new restaurant informaiton into the Mysql database by 
				calling "restaurant_coordinate" and "retrive_restaurant_inf" function
				
	Parameters: None
	
	Returns: None
	
	Note: This function is protected by auth.login_required, users need to pass the verification in the
			beginning
	'''
	# if users send "GET" request, extract all restaurant information from the database
	if request.method == 'GET':
		# get restaurant information from the database
		all_restaurant = session.query(RestaurantInf).all()
		
		# create a dictionery to store the information and return the information to users
		all_restaurant_dict = {}
		for i in all_restaurant:
			all_restaurant_dict[i.restaurant_id] = {'name':i.name, 'address':i.address, 'photo':i.photo}
		return jsonify(all_restaurant_dict)
		
	# if users send "POST" request, put new restaurant information in the database
	elif request.method == 'POST':
		# get the "place" information from users' POST request
		place = request.form['place']
		
		# find restaurant information by calling "restaurant_coordinate" and "retrive_restaurant_inf" function
		restaurant_coordinate = findlocation(place, google_key)
		restaurant_inf_dict = retrive_restaurant_inf(foursquare_id, foursquare_password, restaurant_coordinate[0], restaurant_coordinate[1])
		
		# save new restaurant informaion in the database
		new_restaurant = RestaurantInf(name=str(restaurant_inf_dict['0']['name']), 
					address=str(restaurant_inf_dict['0']['addr']), 
					photo=str(restaurant_inf_dict['0']['img_url']))
		session.add(new_restaurant)
		session.commit()

		return 'Already uploaded a new restaurant to the database'


@app.route('/RestaurantInf/<int:onerestaurantid>', methods = ['GET','PUT', 'DELETE'])
@auth.login_required
def get_update_delete_restaurant(onerestaurantid):
	'''
	Description: This function allow users to get a specific restaurant information, updata this 
				restaurant's information, and delete this restaurant's information.
				
	Parameters: -onerestaurantid: the restaurant's id
	
	Returns: None
	
	Note: This function is protected by auth.login_required, users need to pass the verification in the
			beginning
	'''
	if request.method == 'GET':
		# extract a specifc restaurant's information 
		restaurant = session.query(RestaurantInf).filter_by(restaurant_id = onerestaurantid).one()
		
		# save the inforamtion in a dictionery and return to users
		restaurant_dict = {}
		restaurant_dict[restaurant.restaurant_id] = {'name':restaurant.name, 'address':restaurant.address, 'photo':restaurant.photo}	
		return jsonify(restaurant_dict)

	elif request.method == 'PUT':
		# extract a specifc restaurant's information 
		restaurant = session.query(RestaurantInf).filter_by(restaurant_id = onerestaurantid).one()
		
		# extract the restaurant information (name, address, and photo url)from users' "PUT" request
		name = request.form['name']
		address = request.form['address']
		photo = request.form['photo']
		
		# if users give the new restaurnat name, replace the old restaurant name
		if name:
			restaurant.name = name
			
		# if users give the new restaurnat address, replace the old restaurant address	
		if address:
			restaurant.address = address
			
		# if users give the new restaurnat photo url, replace the old restaurant photo url
		if photo:
			restaurant.photo = photo
		session.commit()
		
		# return the new restaurant information to users in json format
		restaurant_dict = {}
		restaurant_dict[restaurant.restaurant_id] = {'name':restaurant.name, 'address':restaurant.address, 'photo':restaurant.photo}
		return jsonify(restaurant_dict)

	elif request.method == 'DELETE':
		# delete a specifc restaurant's information
		restaurant = session.query(RestaurantInf).filter_by(restaurant_id = onerestaurantid).one()
		session.delete(restaurant)
		session.commit()
		return 'Deletion is done'


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=80)

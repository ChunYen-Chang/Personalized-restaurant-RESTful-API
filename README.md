<p align="center">
  <img width="500" height="270" src="https://github.com/ChunYen-Chang/Personalized-restaurant-RESTful-API/blob/master/image/flask_pic.jpg">
</p>
  
  
# Personalized restaurant RESTful API

#### *PROJECT BACKGROUND and DESCRIPTION*
Do you have the problem about struggling for finding a restaurant at the place you want to go? Do you feel like it is troublesome to
write down the information about the restaurant you like to go on the note? If you have these problems, no worries, we are in the same
boat! This project aims for building a small database in the cloud and provide a RESTful API for users to interact with. Users can use 
the functions which are built in the RESTful API to "POST" restaurants' information in the database and create their favorite restaurant
list. After creating the the favorite list, users can the HTTP request--"GET" to access the favorite list and get **"ALL"** restaurant 
information. Apart from that, this RESTful API also provides functions for user to access **ONE** specific restaurant's information, 
update a specific restaurant's information, and delete a specific restaurant.  
  
Maybe you may worry about one thing--is it possible that other people access to the database and sneakly take my precious favorite 
restaurant list? We already considered this problem. This RESTful API applies the HTTP authentication protection method. Users need
to register an account in the beginning and use the account to access the database. In the below section, we will show the system
architecture.

#### *SYSTEM ARCHITECTURE*

<p align="center">
  <img width="700" height="500" src="https://github.com/ChunYen-Chang/Personalized-restaurant-RESTful-API/blob/master/image/system_structure_v2.jpeg">
</p>

Generally speaking, this project builds a web server Flask in an AWS EC2 instance. This server provides the interface for users to 
interact with. This server has below functons.
1. **Save new restaurants information to Mysql database:** Users send a POSE request from their laptop to the server. After receiving the
POST request, the server call a function to access Geocofing API endpoint and get the place coordinate information. Next, the server send
the coordinate information to Fouesquare API and get restaurant information which is close to this coordinate. Then, the server will store
restaurants' information to Mysql Database.  
2. **Get a list of all restaurants' information:** Users send a GET request from their laptop to the server. After receiving the GET request, 
the server connects with the Mysql database, extract all restaurants' informaiton, and return the information to user in JSON format.  
3. **Get one specific restaurant's information:** Users send a GET request from their laptop to the server. After receiving the GET request, 
the server connects with the Mysql database, extract this specific restaurants' informaiton, and return the information to user in JSON format.  
4. **Update one specific restaurant's information:** Users send a PUT request from their laptop to the server. After receiving the PUT request, 
the server connects with the Mysql database, extract this specific restaurants' informaiton, and update this restaurant's information.  
5. **Delete one specific restaurant's information:** Users send a DELETE request from their laptop to the server. After receiving the DELETE request, 
the server connects with the Mysql database, extract this specific restaurants' informaiton, and delete this restaurant's information.  

------------
#### FILES IN THE REPOSITORY
- **image folder**: It contains images which are used in README.md file  
  
- **README.md**: It includes the project background, project description, system architecture, and the information about how to run the project.  

- **find_restaurant.py**: this file includes the python functions which relates to access to Google Geocoding and Foursquare API and get restaurants' information.  
  
- **model.py**: this file includes two classes. These two classes are used for connecting to Mysql Database by SQLalchemy.  
  
- **server.py**: this file includes the python code of Flask web server .  

------------
#### HOW TO RUN THE PROJECT
**Please follow steps below:**
1. Create an AWS EC2 instance in your AWS account
![](https://github.com/ChunYen-Chang/Personalized-restaurant-RESTful-API/blob/master/image/aws1.jpg)
  
2. In your AWS EC2 instance, access to the security group setting
![](https://github.com/ChunYen-Chang/Personalized-restaurant-RESTful-API/blob/master/image/aws2.jpg)

3. Have following setting to allow other people can access to your server from port 80  
![](https://github.com/ChunYen-Chang/Personalized-restaurant-RESTful-API/blob/master/image/aws3.jpg)

4. Install Mysql in your EC2 instance  

5. Clone this repository to your EC2 instance  

6. Change the Mysql connection address (in server.py)  

7. Type `sudo python3 server.py` in your terminal to start the Falsk Web server  

8. Your server is running. Enjoy it!


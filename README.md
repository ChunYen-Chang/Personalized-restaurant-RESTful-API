<p align="center">
  <img width="800" height="350" src="https://github.com/ChunYen-Chang/Personalized-restaurant-RESTful-API/blob/master/image/project_logo.jpg">
</p>
  
  
# Restaurant Information Searching System with RESTful APIs

#### *PROJECT BACKGROUND and DESCRIPTION*
Are you struggling for finding a **GOOD** restaurant at the place you want to go? Do you feel like it is **troublesome** to
write down the information about the restaurant you like on your paper notebook? If you have these problems, no worries, we are in the same boat!  
  
This project aims for building a small database in the cloud and provide a RESTful API for users to interact with. Users can use the functions which are built in the RESTful API to "POST" restaurants' information in the database and create their favorite restaurant list. After creating the the favorite list, users can the HTTP request--"GET" to access the favorite list and get **"ALL"** restaurant information. Apart from that, this RESTful API also provides functions for user to access **ONE** specific restaurant's information, update a specific restaurant's information, and delete a specific restaurant. Also, this system collects the real-time Tweet posts from Tweet API endpoint, analyzes these Tweet posts by sentiment analysis, and stores the posts--which has positive comments on a restaurant--in the database. Users can access to this Tweet posts to get some ideas about which restaurant they they would like to go.
  
Hold on!! There is another thing we need to mention here--the **security** concern. Maybe you worry about one thing--is it possible that other people can access to the database and sneakly take my precious favorite restaurant list? We already considered this problem. This RESTful API applies the HTTP authentication protection method. Users need to register an account in the beginning and use the account to access the database. In the below section, we will show the system architecture.

#### *SYSTEM ARCHITECTURE*

<p align="center">
  <img width="700" height="800" src="https://github.com/ChunYen-Chang/Personalized-restaurant-RESTful-API/blob/master/image/system_structure_v2.jpeg">
</p>

Generally speaking, this project builds a web server Flask in an AWS EC2 instance. This server provides the interface for users to 
interact with, and it has below functons.
1. **SAVE NEW RESTAURANTS' INFORMATION TO MYSQL DATABASE:** Users send a POSE request from their laptop to the server. After receiving the POST request, the server call a function to access Geocofing API endpoint and get the place coordinate information. Next, the server send the coordinate information to Fouesquare API and get restaurant information which is close to this coordinate. Then, the server will store restaurants' information to Mysql Database.  
2. **GET A LIST OF ALL RESTAURANTS' INFORMATION:** Users send a GET request from their laptop to the server. After receiving the GET request, the server connects with the Mysql database, extract all restaurants' informaiton, and return the information to user in JSON format.  
3. **GET ONE SPECIFIC RESTAURANT'S INFORMATION:** Users send a GET request from their laptop to the server. After receiving the GET request, the server connects with the Mysql database, extract this specific restaurants' informaiton, and return the information to user in JSON format.  
4. **UPDATE ONE SPECIFIC RESTAURANT'S INFORMATION:** Users send a PUT request from their laptop to the server. After receiving the PUT request, the server connects with the Mysql database, extract this specific restaurants' informaiton, and update this restaurant's information.  
5. **DELETE ONE SPECIFIC RESTAURANT'S INFORMATION:** Users send a DELETE request from their laptop to the server. After receiving the DELETE request, the server connects with the Mysql database, extract this specific restaurants' informaiton, and delete this restaurant's information.  
6. **GET TWEET POSTS HAVING POSITIVE COMMENTS ON RESTAURANTS:** The logic begind this function can be seperated into several steps. First, an EC2 server connects to Tweet API endpoint and get streaming data of Tweet posts. Second, the streaming data from Tweet API endpoint is immediately stored in a Redis database. Third, this EC2 server connects to the Redis databse, extracts the Tweet posts, analyzes the Tweet posts by sentiment analysis, and stores the positive Tweet posts about restaurants in Mysql database at 6AM every day (bu using crontab). Fourth, users send a GET request from their laptop to the Flask server. After receiving the GET request, the Flask server connects with the Mysql database, extract Tweet posts information, and return Tweet posts to users. Fifth, users use the information to help them make a decision about which restaurant they can go.

------------
#### FILES IN THE REPOSITORY
- **image folder**: It contains images which are used in README.md file  
  
- **README.md**: It includes the project background, project description, system architecture, and the information about how to run the project.  

- **find_restaurant.py**: this file includes the python functions which relates to access to Google Geocoding and Foursquare API and get restaurants' information.  
  
- **model.py**: this file includes two classes. These two classes are used for connecting to Mysql Database by SQLalchemy.  
  
- **server.py**: this file includes the python code of Flask web server .  
  
- **streaming folder**: this folder contains the python code of streaming part (The lower part of system architecture picture). The details are listed below.
  - **mysql_account_inf.txt**: this txt file includes the mysql connection information
  - **tweet_api.txt**: this txt file includes the Tweet API connection information (API keys)
  - **redis_database.py**: this python file provides the redis class that "analysis_tweet.py" and "streaming_tweet.py" use
  - **streaming_tweet.py**: this python file is about receiving streaming data from Tweet API and storing it in Redis database
  - **analysis_tweet.py**: this python file relates to extract data from Redis databse, analyze it by sentiment analysis, and store the positive Tweet posts in Mysql database
------------
#### HOW TO RUN THE PROJECT
If you want to run this project, you need two EC2 instance. The first EC2 instance holds the Flask sever, and, the second EC2 instance is in charge of receiving streaming data from Tweet API, communicating with Redis, performing sentiment analysis on Tweet data, and sending result to Mysql database. In this section, the first part will talk about how to set up an EC2 instance which holds the Flask server, and, the second part will focus on how to set an EC2 instance which is in charge of receiving streaming data from Tweet API, communicating with Redis, performing sentiment analysis on Tweet data, and sending result to Mysql database.  

**PART ONE: EC2 instance holding Flask server:**
1. Create an AWS EC2 instance in your AWS account
![](https://github.com/ChunYen-Chang/Personalized-restaurant-RESTful-API/blob/master/image/aws1.jpg)
  
2. In your AWS EC2 instance, access to the security group setting
![](https://github.com/ChunYen-Chang/Personalized-restaurant-RESTful-API/blob/master/image/aws2.jpg)

3. Have following setting to allow other people can access to your server from port 80  
![](https://github.com/ChunYen-Chang/Personalized-restaurant-RESTful-API/blob/master/image/aws3.jpg)

4. Install Mysql in your EC2 instance  

5. Clone **find_restaurant.py** **model.py** **server.py** to your EC2 instance  

6. Change the Mysql connection address (in server.py)  

7. Type `sudo python3 server.py` in your terminal to start the Falsk Web server  

8. Your server is running. Enjoy it!  
  
  
**PART TWO: EC2 instance which is in charge of receiving streaming data from Tweet API, communicating with Redis, performing sentiment analysis on Tweet data, and sending result to Mysql database:**  

1. Install Redis in this EC2 instance

2. Clone **streaming folder** to this EC2 instance  

3. Modify **mysql_account_inf.txt** and **tweet_api.txt** so that you can access to your Mysql Database and Tweet API endpoint  

4. configure the crontab to make your system automatically run **analysis_tweet.py** at 6AM every day  

5. Type `sudo python3 streaming_tweet.py` in your terminal to start the process of receiving streaming data from Tweet API and sending to Redis  

6.  This part is done. Enjoy it! 


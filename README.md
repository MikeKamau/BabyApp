**BabyApp**\
BabyApp, a simple ML powered app utilizing Fastai and Flask to perform inference on passport photos and determine if they belong to an adult or child.
Currently the model used is only used for testing and educational purposes, so feel free to play around with it and improve it's accuracy.

**Features**\
The app also implements the following features:

* User registration
* Ability to send confirmation emails to registered users
* Login and logout
* Password reset
* Inference feature, to determine if a passport photo belongs to a child or an adult (Users must confirm their emails after registration to use this feature)

**Setup**
1. Clone the project to your local system **git clone https://github.com/MikeKamau/BabyApp.git**

2. Create a folder in your Google Drive labeled Training_Photos, with two directories called Adult and Child inside of it containing passport photos of 128 by 128 pixels of adults and children in their respective directories.

3. Copy the contents of the child_or_not.py file inside the app folder into Google Colab.

4. Upload a 128 x 128 photo to the root of your Google drive and name it What.jpg, to test the model, and once you've trained the model enough and are satisfied with the accuracy export the model using the name "child_or_not.pkl" and download it. You will copy the .pkl file to the app directory within the babyapp project/directory.

5. Create a python virtual environment using the requirements.txt file provided.

6. Set the following environment variables on your system e.g. in your ~/.bashrc file in Linux

  * **SECRET_KEY** - The secret key that will be used for securely signing the session cookie and can be used for any other security related needs by extensions or your application
  * **SECURITY_PASSWORD_SALT** - Specifies the HMAC salt. This is only used if the password hash type is set to something other than plain text. Defaults to None
  * **SQLALCHEMY_DATABASE_URI** - The database URI that should be used for the connection, for this app it'll be the path to the sqlite database
  * **SQLALCHEMY_TRACK_MODIFICATIONS** - Whether to track modifications to the SQLAlchemy session
  * **MAX_CONTENT_LENGTH** - The maximum size a request body can have, this is optional
  * **UPLOAD_EXTENSIONS** - The allowed file extensions for uploaded files
  * **UPLOAD_PATH** - Where on the filesystem, uploaded files will be saved
  * **MAIL_SERVER** - Hostname of the mail server to be used for sending emails
  * **MAIL_PORT** - Port number used by the mail server
  * **MAIL_USE_TLS** - Whether or not the mail server utilizes TLS
  * **MAIL_USERNAME** - Username of the account to be used for sending out emails from the app
  * **MAIL_PASSWORD** - Password of the account to be used for sending out emails from the app
  * **ADMINS** - Email address of the individual that should receive alerts as per the set logging level
  * **FLASK_ENV** - What context Flask is running in i.e development or production. It defaults to production

7. Change directory into the project folder i.e cd /path/to/babyapp/folder e.g cd BabyApp  

8. Run the app using the flask run command i.e. flask run  

9. Access the app on http://localhost:5000

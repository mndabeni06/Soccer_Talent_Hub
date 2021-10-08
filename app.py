# Mpendulo Khoza
# Masimthembe Ndabeni
import hmac
import sqlite3
import re
import datetime
from flask import Flask, request, jsonify, redirect, render_template
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS, cross_origin
from flask_mail import Mail,Message
from smtplib import SMTPRecipientsRefused, SMTPAuthenticationError
from werkzeug.utils import redirect


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('football.db')
        self.cursor = self.conn.cursor()
        self.admin()
        self.user()
        self.player_profile()
        self.scouter_profile()

# creating a table for user admin

    def admin(self):
        conn = sqlite3.connect('football.db')
        print('Opened Database Successfully')

        conn.execute("CREATE TABLE IF NOT EXISTS admin (admin_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "first_name TEXT NOT NULL,"
                     "last_name TEXT NOT NULL,"
                     "email TEXT NOT NULL,"
                     "password TEXT NOT NULL)")
        print('Admin Table Created Successfully')
        conn.close()
        return self.admin

    def user(self):
        with sqlite3.connect('football.db') as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS user(userId INTEGER PRIMARY KEY AUTOINCREMENT,"
                         "firstname TEXT NOT NULL,"
                         "lastname TEXT NOT NULL,"
                         "email TEXT NOT NULL,"
                         "phone_number TEXT NOT NULL,"
                         "password TEXT NOT NULL)")
            print("User Registration Table Created Successfully")
        conn.close()
        return self.user

    # creating a table for player profile
    def player_profile(self):
        with sqlite3.connect('football.db') as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS player_profiles(player_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                         "firstname TEXT NOT NULL,"
                         "lastname TEXT NOT NULL,"
                         "nickname TEXT NOT NULL,"
                         "age TEXT NOT NULL,"
                         "gender TEXT NOT NULL,"
                         "date_of_birth TEXT NOT NULL,"
                         "place_of_birth TEXT NOT NULL,"
                         "home_address TEXT NOT NULL,"
                         "nationality TEXT NOT NULL,"
                         "player_position TEXT NOT NULL,"
                         "height TEXT NOT NULL,"
                         "weight TEXT NOT NULL,"
                         "previous_club TEXT NOT NULL,"
                         "current_club TEXT NOT NULL,"
                         "player_description TEXT NOT NULL,"
                         "player_image TEXT NOT NULL,"
                         "player_video TEXT NULL,"
                         "CONSTRAINT fk_user FOREIGN KEY (player_id) REFERENCES user(userId))")
            print('Player Profile Table Created Successfully')
        conn.close()
        return self.player_profile

    # creating a table for scouter profile

    def scouter_profile(self):
        with sqlite3.connect('football.db') as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS scouter_profile(scouter_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                         "firstname TEXT NOT NULL,"
                         "lastname TEXT NOT NULL,"
                         "email TEXT NOT NULL,"
                         "phone TEXT NOT NULL,"
                         "age TEXT NOT NULL,"
                         "nationality TEXT NOT NULL,"
                         "image TEXT NOT NULL,"
                         "CONSTRAINT fk_user FOREIGN KEY (scouter_id) REFERENCES user(userId))")
            print('Scouter Profile Table Created Successfully')
        conn.close()
        return self.scouter_profile


Database()
# to make the data into a dictionary


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# creating my My Flask App
app = Flask(__name__)
app.debug = True
CORS(app)

# setting up flask-mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mndabeni6@gmail.com'
app.config['MAIL_PASSWORD'] = '0733887645'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
CORS(app)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=2)


#authanticate a loggen in user
#jwt = JWT(app, authenticate, identity)

#for data in user:
           # new_data.append(User(data[0], data[3], data[4],data[5],data[6],data[7])) # append all data to new_data empty list
   # return new_data

# user = fetch_users() # declare users tables to a variable "users"

#username_table = { u.username: u for u in users } # make a dictionary for username
#userid_table = { u.id: u for u in users } # make a dictionary for user id

# set authantication for username and password
#def authenticate(username, password):
   # user = username_table.get(username, None)
   # if user and hmac.compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
   #     return user

# identify registered user by user id
#def identity(payload):
   # user_id = payload['identity']
   # return userid_table.get(user_id, None)

#  Creating my landing page of heroku

@app.route('/', methods=['GET'])
def welcome():
    response = {}
    if request.method == 'GET':
        response['message'] = "Welcome to your landing page"
        return response
# ----------------------------------------------The Creation Of Routes ------------------------------------------------


# This is my route to register  user
@app.route('/register', methods=['POST'])
def user_registration():
    response = {}
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    phone_number = request.form['phone_number']
    password = request.form['password']
    email_validator = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    try:
        if request.method == 'POST':
            if re.search(email_validator, email):
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO user(firstname,"
                                   "lastname,"
                                   "email,"
                                   "phone_number,"
                                   "password) VALUES(?, ?, ?, ?, ?)", (firstname, lastname, email, phone_number, password))
                    conn.commit()
                    response['message'] = "User Registered  Successfully"
                    response['status_code'] = 200
                return response
            else:
                response['error_message'] = "Invalid Email"
                response['status_code'] = 404
                return response
        else:
            if request.method != "POST":
                response['error'] = "Wrong method, it must be a POST"
                return response
    except ConnectionError:
        response['message'] = "No Connection"
        return response

# This is my route for user login
@app.route('/user-login', methods=['PATCH'])
def user_login():
    response = {}
    if request.method == "PATCH":
        email = request.form['email']
        password = request.form['password']
        try:
            with sqlite3.connect('football.db') as conn:
                conn.row_factory = dict_factory
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT * FROM user WHERE email=? AND password=?', (email, password))
                user = cursor.fetchone()
            response['message'] = "login successful"
            response['status_code'] = 200
            response['data'] = user
            return response
        except ValueError:
            response['error'] = "Invalid"
            response['status_code'] = 404
            return response
    else:
        if request.method != "PATCH":
            response['message'] = "Incorrect Method"
            response['status_code'] = 400
            return response


# This is my route for an admin registration
@app.route('/admin', methods=['POST'])
def admin_registration():
    response = {}
    firstname = request.form['first_name']
    lastname = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    email_validator = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    try:
        if request.method == 'POST':
            if re.search(email_validator, email):
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO user(firstname,"
                                   "lastname,"
                                   "email,"
                                   "password) VALUES(?, ?, ?, ?)", (firstname, lastname, email, password))
                    conn.commit()
                    response['message'] = " Admin Registered Successfully"
                    response['status_code'] = 200
                return response
            else:
                response['error_message'] = "Invalid Email"
                response['status_code'] = 404
                return response
        else:
            if request.method != "POST":
                response['error'] = "Wrong method, it must be a POST"
                return response
    except ConnectionError:
        response['message'] = "No Connection"
        return response


# This is my route for a player registration
@app.route('/create-player-profile/', methods=['POST'])
def player_profile():
    response = {}
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        nickname = request.form['nickname']
        age = request.form['age']
        gender = request.form['gender']
        date_of_birth = request.form['date_of_birth']
        place_of_birth = request.form['place_of_birth']
        home_address = request.form['home_address']
        nationality = request.form['nationality']
        player_position = request.form['player_position']
        height = request.form['height']
        weight = request.form['weight']
        previous_club = request.form['previous_club']
        current_club = request.form['current_club']
        player_description = request.form['player_description']
        player_image = request.form['player_image']
        player_video = request.form['player_video']
        with sqlite3.connect('football.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO player_profiles ("
                           "firstname,"
                           "lastname,"
                           "nickname,"
                           "age,"
                           "gender,"
                           "date_of_birth,"
                           "place_of_birth,"
                           "home_address,"
                           "nationality,"
                           "player_position,"
                           "height,"
                           "weight,"
                           "previous_club,"
                           "current_club,"
                           "player_description,"
                           "player_image,"
                           "player_video) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (firstname, lastname, nickname, age, gender, date_of_birth, place_of_birth, home_address, nationality, player_position, height, weight, previous_club, current_club, player_description, player_image, player_video))
        conn.commit()
        response['message'] = "Player created successfully"
        response['status_code'] = 200
    return response


# This is my route for  a user registration
@app.route('/create-scouter-profile', methods=['POST'])
def scouter_profile():
        response = {}
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone = request.form['phone']
        email = request.form['email']
        age = request.form['age']
        nationality = request.form['nationality']
        image = request.form['image']
        with sqlite3.connect('football.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO scouter_profile (firstname,"
                           "lastname,"
                           "phone,"
                           "email,"
                           "age,"
                           "nationality,"
                           "image) VALUES(?, ?, ?, ?, ?, ?, ?)", (firstname, lastname, phone, email, age, nationality, image))
        response['message'] = "Registration Successful"
        response['status_code'] = 200


# --------------------------------------------------------Update Routes Here --------------------------------------

# This is my route for updating a user profile by ID
@app.route('/update-user/<int:userId>', methods=['PUT'])
def update_user(userId):
    response = {}

    if request.method == "PUT":
        with sqlite3.connect('football.db') as conn:
            incoming_data = dict(request.form)
            put_data = {}

            if incoming_data.get('firstname') is not None:
                put_data['firstname'] = incoming_data.get('firstname')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'UPDATE user SET firstname=? WHERE userId=?', (put_data['firstname'], userId))
                    conn.commit()
                    response['message'] = "First Name Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('lastname') is not None:
                put_data['lastname'] = incoming_data.get('lastname')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'UPDATE user SET lastname=? WHERE userId=?', (put_data['lastname'], userId))
                    conn.commit()
                    response['message'] = "lastname  Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('phone') is not None:
                put_data['phone'] = incoming_data.get('phone')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'UPDATE user SET phone=? WHERE userId=?', (put_data['phone'], userId))
                    conn.commit()
                    response['message'] = "phone  Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('email') is not None:
                put_data['email'] = incoming_data.get('email')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'UPDATE user SET email=? WHERE userId=?', (put_data['email'], userId))
                    conn.commit()
                    response['message'] = "email  Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('password') is not None:
                put_data['password'] = incoming_data.get('password')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'UPDATE user SET password=? WHERE userId=?', (put_data['password'], userId))
                    conn.commit()
                    response['message'] = "password  Updated Successfully"
                    response['status_code'] = 200
    return response


# -----------------This is my route for updating the player profile-------------------#
@app.route('/update-player-profile/<int:player_id>', methods=['PUT'])
def update_player_profile(player_id):
    response = {}

    if request.method == "PUT":
        with sqlite3.connect('football.db') as conn:
            incoming_data = dict(request.form)
            put_data = {}

            if incoming_data.get('firstname') is not None:
                put_data['firstname'] = incoming_data.get('firstname')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'UPDATE player_profiles SET firstname=? WHERE player_id=?', (put_data['firstname'], player_id))
                    conn.commit()
                    response['message'] = "First Name Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('lastname') is not None:
                put_data['lastname'] = incoming_data.get('lastname')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'UPDATE player_profiles SET lastname=? WHERE player_id=?', (put_data['lastname'], player_id))
                    conn.commit()
                    response['message'] = "lastname Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('nickname') is not None:
                put_data['nickname'] = incoming_data.get('nickname')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'UPDATE player_profiles SET nickname=? WHERE player_id=?', (put_data['nickname'], player_id))
                    conn.commit()
                    response['message'] = "nickname Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('age') is not None:
                put_data['age'] = incoming_data.get('age')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'UPDATE player_profiles SET age=? WHERE player_id=?', (put_data['age'], player_id))
                    conn.commit()
                    response['message'] = "age Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('gender') is not None:
                put_data['gender'] = incoming_data.get('gender')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'UPDATE player_profiles SET gender=? WHERE player_id=?', (put_data['gender'], player_id))
                    conn.commit()
                    response['message'] = "gender Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('date_of_birth') is not None:
                put_data['date_of_birth'] = incoming_data.get('date_of_birth')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE player_profiles SET date_of_birth=? WHERE player_id=?', (
                        put_data['date_of_birth'], player_id))
                    conn.commit()
                    response['message'] = "date_of_birth Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('place_of_birth') is not None:
                put_data['place_of_birth'] = incoming_data.get(
                    'place_of_birth')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE player_profiles SET place_of_birth=? WHERE player_id=?', (
                        put_data['place_of_birth'], player_id))
                    conn.commit()
                    response['message'] = "place_of_birth Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('home_address') is not None:
                put_data['home_address'] = incoming_data.get('home_address')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE player_profiles SET home_address=? WHERE player_id=?', (
                        put_data['home_address'], player_id))
                    conn.commit()
                    response['message'] = "home_address Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('nationality') is not None:
                put_data['nationality'] = incoming_data.get('nationality')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE player_profiles SET nationality=? WHERE player_id=?', (
                        put_data['nationality'], player_id))
                    conn.commit()
                    response['message'] = "nationality Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('player_position') is not None:
                put_data['player_position'] = incoming_data.get(
                    'player_position')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE player_profiles SET player_position=? WHERE player_id=?', (
                        put_data['player_position'], player_id))
                    conn.commit()
                    response['message'] = "player_position Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('height') is not None:
                put_data['height'] = incoming_data.get('height')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'UPDATE player_profiles SET height=? WHERE player_id=?', (put_data['height'], player_id))
                    conn.commit()
                    response['message'] = "height Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('weight') is not None:
                put_data['weight'] = incoming_data.get('weight')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'UPDATE player_profiles SET weight=? WHERE player_id=?', (put_data['weight'], player_id))
                    conn.commit()
                    response['message'] = "weight Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('previous_club') is not None:
                put_data['previous_club'] = incoming_data.get('previous_club')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE player_profiles SET previous_club=? WHERE player_id=?', (
                        put_data['previous_club'], player_id))
                    conn.commit()
                    response['message'] = "previous_club Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('current_club') is not None:
                put_data['current_club'] = incoming_data.get('current_club')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE player_profiles SET current_club=? WHERE player_id=?', (
                        put_data['current_club'], player_id))
                    conn.commit()
                    response['message'] = "current_club Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('player_description') is not None:
                put_data['player_description'] = incoming_data.get(
                    'player_description')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE player_profiles SET player_description=? WHERE player_id=?', (
                        put_data['player_description'], player_id))
                    conn.commit()
                    response['message'] = "player_description Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('player_image') is not None:
                put_data['player_image'] = incoming_data.get('player_image')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE player_profiles SET player_image=? WHERE player_id=?', (
                        put_data['player_image'], player_id))
                    conn.commit()
                    response['message'] = "player_image Updated Successfully"
                    response['status_code'] = 200

            return response


# --------------This is my route for updating the scouter profile-----------#
@app.route('/update-scouter/<int:scouter_id>', methods=["PUT"])
def update_scouter_profile(scouter_id):
    response = {}
    if request.method == "PUT":
        with sqlite3.connect('football.db') as conn:
            incoming_data = dict(request.form)
            put_data = {}

            if incoming_data.get('firstname') is not None:
                put_data['firstname'] = incoming_data.get('firstname')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'UPDATE scouter_profile SET firstname=? WHERE scouter_id=?', (put_data['firstname'], scouter_id))
                    conn.commit()
                    response['message'] = "First Name Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('lastname') is not None:
                put_data['lastname'] = incoming_data.get('lastname')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'UPDATE scouter_profile SET lastname=? WHERE scouter_id=?', (put_data['lastname'], scouter_id))
                    conn.commit()
                    response['message'] = "last Name Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('email') is not None:
                put_data['email'] = incoming_data.get('email')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'UPDATE scouter_profile SET email=? WHERE scouter_id=?', (put_data['email'], scouter_id))
                    conn.commit()
                    response['message'] = "email Name Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('phone') is not None:
                put_data['phone'] = incoming_data.get('phone')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'UPDATE scouter_profile SET phone=? WHERE scouter_id=?', (put_data['phone'], scouter_id))
                    conn.commit()
                    response['message'] = "phone number Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('age') is not None:
                put_data['age'] = incoming_data.get('age')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'UPDATE scouter_profile SET age=? WHERE scouter_id=?', (put_data['age'], scouter_id))
                    conn.commit()
                    response['message'] = "age Name Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('nationality') is not None:
                put_data['nationality'] = incoming_data.get('nationality')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE scouter_profile SET nationality=? WHERE scouter_id=?', (
                        put_data['nationality'], scouter_id))
                    conn.commit()
                    response['message'] = "nationality Name Updated Successfully"
                    response['status_code'] = 200

            if incoming_data.get('image') is not None:
                put_data['image'] = incoming_data.get('image')
                with sqlite3.connect('football.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'UPDATE scouter_profile SET image=? WHERE scouter_id=?', (put_data['image'], scouter_id))
                    conn.commit()
                    response['message'] = "image Name Updated Successfully"
                    response['status_code'] = 200
            return response


# ------------------------------------------Deleting Routes Here---------------------------------------------

# This is my route for deleting a user profile
@app.route('/delete-profile/<int:userId>', methods=['DELETE'])
def remove_user_profile(userId):
    response = {}
    if request.method == 'DELETE':
        with sqlite3.connect('football.db') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM user WHERE userId=?' + str(userId))
            conn.commit()
            response['message'] = "User Deleted Successfully"
            response['status_code'] = 200
    else:
        if request.method != "DELETE":
            response['status_code'] = 400
    response['message'] = "Wrong Method"
    return response


# This is my route for deleting a player profile
@app.route('/delete-player/<int:player_id>', methods=['DELETE'])
def remove_player_profile(player_id):
    response = {}
    if request.method == 'DELETE':
        with sqlite3.connect('football.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM player_profile WHERE player_id=?' + str(player_id))
            conn.commit()
            response['message'] = "Player profile Deleted Successfully"
            response['status_code'] = 200
    else:
        if request.method != "DELETE":
            response['status_code'] = 400
    response['message'] = "Wrong Method"
    return response


# This is my route for deleting a scouter profile
@app.route('/delete-scouter/<int:scouter_id>', methods=['DELETE'])
def remove_scouter_profile(scouter_id):
    response = {}
    if request.method == 'DELETE':
        with sqlite3.connect('football.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM scouter_profile WHERE scouter_id=?' + str(scouter_id))
            conn.commit()
            response['message'] = "Scouter profile Deleted Successfully"
            response['status_code'] = 200
    else:
        if request.method != "DELETE":
            response['status_code'] = 400
    response['message'] = "Wrong Method"
    return response


# ---------------------------------------------------Viewing Routes Here-----------------------------------------------------

# This is my route for viewing all  user profiles


@app.route('/user-profiles', methods=['GET'])
def view_user_profiles():
    response = {}

    with sqlite3.connect('football.db') as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user')
        response['message'] = "Fetching User Profiles"
        response['status_code'] = 200
        response['data'] = cursor.fetchall()
    return response


# This is my route for viewing a single user profile
@app.route('/user-profile/<int:userId>', methods=['GET'])
def view_user_profile(userId):
    response = {}
    with sqlite3.connect('football.db') as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user  WHERE userId=' + str(userId))
        user = cursor.fetchone()
        response['message'] = "User Profile Fetched Successfully"
        response['status_code'] = 200
        response['data'] = user
    return response

# ------------------------------Scouter Routes------------------------------------------------
# This is my route for viewing all scouter profiles
@app.route('/scouter-profiles', methods=['GET'])
def view_scouter_profiles():
    response = {}

    with sqlite3.connect('football.db') as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM scouter_profile')
        response['message'] = "Fetching Scouter Profiles Successful"
        response['status_code'] = 200
        response['data'] = cursor.fetchall()
    return response


# This is my route for viewing a scouter profile
@app.route('/scouter-profile/<int:scouter_id>', methods=['GET'])
def view_scouter_profile(scouter_id):
    response = {}

    with sqlite3.connect('football.db') as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM scouter_profile  WHERE scouter_id=?' + str(scouter_id))
        scouter = cursor.fetchone()
        response['message'] = "Scouter Profile Fetched Successfully"
        response['status_code'] = 200
        response['data'] = scouter
    return response

# ---------------------------------Scouter Profile END-------------------------------------------------




# --------------------------------- Player Profile----------------------------------------------------
#  This is my route for viewing All player Profiles
@app.route('/player-profiles', methods=['GET'])
def view_player_profiles():
    response = {}

    with sqlite3.connect('football.db') as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM player_profiles')
        response['message'] = "Fetching Player Profiles Successful"
        response['status_code'] = 200
        response['data'] = cursor.fetchall()
    return response


# This is my route for viewing a player profile
@app.route('/player-profile/<int:player_id>', methods=['GET'])
def view_player_profile(player_id):
    response = {}

    with sqlite3.connect('football.db') as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM player_profile  WHERE player_id=?' + str(player_id))
        player = cursor.fetchone()
        response['message'] = "Player Profile Fetched Successfully"
        response['status_code'] = 200
        response['data'] = player
    return response


# ------------------------------------------------Player Profile END-----------------------------------
if __name__ == '__main__':
    app.run(debug=True)

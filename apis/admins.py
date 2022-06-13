
from string import ascii_letters
from flask import  flash, render_template, request, jsonify,Blueprint ,url_for
from flask_pymongo import ObjectId
from passlib.hash import pbkdf2_sha256
from apis.database import mongo
from flask_jwt_extended import create_access_token
from apis.mails import mail
from flask_mail import Message
import random
from werkzeug.utils import secure_filename
import base64


SSL_DISABLE=True
api_admin = Blueprint('api_admin',__name__)
#####################################  send reset passwordemail
@api_admin.route("/forgetmypass",methods=["PATCH"])
def index():
  dbA = mongo.db.admins
  admin ={
        'email': request.json['email'],
    }
  user = dbA.find_one({"email": admin['email']})
  
  if dbA.find_one({"email": admin['email']}):
    email = user['email']
    name = user['fName']
    id = str(ObjectId(user['_id']))
    msg = Message('Master Way Password Reset Request', sender =   'masterway.eliaatours@gmail.com', recipients = [email] )
    msg.body = "Hey" + " " + name  +",to reset your password, visit the following link"+"\r\n"+"https://vigorous-meninsky-e72496.netlify.app/resetpassword/"+id
    mail.send(msg)
    return "Message sent!",200
  return "No Such email in the data base" ,401
##########################  add admin

@api_admin.route('/admins', methods=['POST'])
def addAdmin():
    with open('profile.txt', 'r') as f: 
     text=f.read()
    
    
    dbA = mongo.db.admins
    admin ={
        'fName': request.json['fName'],
        'email': request.json['email'],
        'password':pbkdf2_sha256.hash(request.json['ID']),
        'ID':request.json['ID'],
        'phoneNumber': request.json['phoneNumber'],
        'age': request.json['age'],
        'profilepic':text
        
    }
    if dbA.find_one({"email":request.json['email']}):
        return jsonify({"msg":"Email address already in use"})
    dbA.insert_one(admin)
    email = admin['email']
    name = admin['fName']
    id = str(ObjectId(admin['_id']))
    msg = Message('Master Way Welcome', sender =   'masterway.eliaatours@gmail.com', recipients = [email] )
    msg.body = "Hey" + " " + name  +"\r\n"+"Welcome to Master Way"+"\r\n"+"To acsses your account on master way use your email and the password is your ID number, in order to change your password, visit the following link"+"\r\n"+"https://vigorous-meninsky-e72496.netlify.app/resetpassword/"+id
    mail.send(msg)
    return jsonify({ 'msg': "Admin Added Successfully"}) 

########################## get admins 
@api_admin.route('/admins', methods=['GET'])
def getAdmins():
    
    dbA = mongo.db.admins
    admins = []
    for doc in dbA.find():
        admins.append({
            '_id': str(ObjectId(doc['_id'])),
            'fName': doc['fName'],
            'email': doc['email'],
            'ID': doc['ID'],
            'phoneNumber': doc['phoneNumber'],
            'age':doc['age']
            
        })
    return jsonify(admins)
########################## get admin by the id


@api_admin.route('/admins/<id>', methods=['GET'])
def getAdmin(id):
    dbA = mongo.db.admins
    admin = dbA.find_one({'_id': ObjectId(id)})
    return jsonify({
            '_id': str(ObjectId(admin['_id'])),
            'fName': admin['fName'],
            'email': admin['email'],
            'ID': admin['ID'],
            'phoneNumber': admin['phoneNumber'],
             'age': admin['age'],
            'profilepic':admin['profilepic']
             
    })
########################## get admin profile
@api_admin.route('/admins/profile/<id>', methods=['GET'])
def getAdminProfile(id):
    dbA = mongo.db.admins
    admin = dbA.find_one({'_id': ObjectId(id)})
    return jsonify({
            '_id': str(ObjectId(admin['_id'])),
           'fName': admin['fName'],
            'email': admin['email'],
            'ID': admin['ID'],
            'phoneNumber': admin['phoneNumber'],
            'age': admin['age'],
            'profilepic':admin['profilepic']
            
    })
##################### delete admin
@api_admin.route('/admins/<id>', methods=['DELETE'])
def deleteAdmin(id):
    dbA = mongo.db.admins
    dbA.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': "Admin Deleted Successfully"})
################################# update admin
@api_admin.route('/admins/<id>', methods=['PUT'])
def updateAdmin(id):
    dbA = mongo.db.admins
    dbA.update_one({'_id': ObjectId(id)}, {'$set': {
        'fName': request.json['fName'],
        'email': request.json['email'],
        'ID':request.json['ID'],
        'phoneNumber': request.json['phoneNumber'],
        'age': request.json['age'],
    }})
    return jsonify({'msg': "Admin Update Successfully"})
######################## login of the webapp
@api_admin.route('/login', methods=['POST'])
def login():
    
    dbA = mongo.db.admins
    admin = {
        "email":request.json['email'],
        "password":request.json['password']
    }
 
    user =  dbA.find_one({"email":admin['email']}) 
    if user and pbkdf2_sha256.verify(admin["password"], user['password']):
        access_token = create_access_token(identity=user['email'])
        access = {
        "email":user['email'],
        "token":access_token,
        "fName":user['fName'],
        "_id":str(ObjectId(user['_id'])),
        "profilepic":user['profilepic']
        }
        return jsonify(access),200
        
    return jsonify("wrong email or wrong password"),401

##########################  change the password of the admin
@api_admin.route('/resetpassword/<id>', methods=['POST'])
def reset(id):
    dbA = mongo.db.admins
    dbA.update_one({'_id': ObjectId(id)}, {'$set': {
         
        'password': pbkdf2_sha256.hash(request.json['password']),
    }})
    return jsonify({'msg': "Password Updated Successfully"})
 
##########################  sent random code in the reset password email 
@api_admin.route("/mobapp",methods=["PATCH"])
def sent():
  dbW = mongo.db.workers
  admin ={
        'email': request.json['email'],
    }
  user = dbW.find_one({"email": admin['email']})
  
  if dbW.find_one({"email": admin['email']}):
    email = user['email']
    name = user['fName']
    value = random.randint(1000,9999)
    dbW.update_one({'email': admin['email']}, {'$set': {
        'code': pbkdf2_sha256.hash(str(value)),
    }})
    msg = Message('Master Way Password Reset Request', sender =   'masterway.eliaatours@gmail.com', recipients = [email] )
    msg.body = "Hey" + " " + name  +",to reset your password, use this code in the app "+"\r\n"+ str(value)
    mail.send(msg)
    return "Message sent!",200
  return "No Such email in the data base" ,401

  ##########################  check if the code is the same from the database

@api_admin.route("/mobapp/confirm",methods=["POST"])
def confirm():
  dbW = mongo.db.workers
  worker ={
        "email": request.json["email"],
        "code":request.json["code"]
    }
  user = dbW.find_one({"email": worker['email']})
  if user and pbkdf2_sha256.verify(worker["code"], user['code']):
    return jsonify("corrcet"),200
  return jsonify("wrong email or wrong password"),401
#################################### change the password
@api_admin.route("/mobapp/reset",methods=["POST"])
def resetpass():
  dbW = mongo.db.workers
  worker ={
        "email": request.json["email"],
        "password":request.json["password"]
    }
  user = dbW.find_one({"email": worker['email']})
  if user:  
    dbW.update_one({'email': worker['email']}, {'$set': {
        "password": pbkdf2_sha256.hash(worker["password"])
         
    }})
    return jsonify("password has changed"),200
  return jsonify("there is a problem"),401
  
 



  
 

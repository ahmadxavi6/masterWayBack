from email.policy import default
from multiprocessing.dummy import Array
from operator import indexOf
from re import A
from apis.database import mongo
from flask import Flask, json, request, jsonify , Response, send_file,send_from_directory ,url_for
from flask_pymongo import ObjectId
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from apis.budget import api_budget
from apis.admins import api_admin
from flask_mail import Mail ,Message
from apis.mails import mail
from werkzeug.utils import secure_filename
import base64






app = Flask(__name__)
app.register_blueprint(api_admin)
app.register_blueprint(api_budget)
CORS(app)

app.secret_key="oS\xf8\xf4\xe2\xc8\xda\xe3\x7f\xc75*\x83\xb1\x06\x8c\x85\xa4\xa7piE\xd6I"
app.config['MONGO_URI']='mongodb+srv://ahmadxavi6:0584603153aA@masterway.6ifdp.mongodb.net/masterway?retryWrites=true&w=majority'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'masterway.eliaatours@gmail.com'
app.config['MAIL_PASSWORD'] = 'nkhjptiddckyqwbv'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mongo.init_app(app)
mail.init_app(app)
app.config["JWT_SECRET_KEY"] = "dfg54dfg4564gd56g4er8cdv2cb8f5/456cd5=-54xcvrt7"  # Change this!
jwt = JWTManager(app)


dbW = mongo.db.workers
dbV = mongo.db.vehicles
dbA = mongo.db.admins
dbB = mongo.db.budgets


########################## upload profile picture for the admins
@app.route('/admins/profilepic/<id>', methods=['POST'])
def uploadImg(id):
    image = request.files['profilepic']  
    image_string = base64.b64encode(image.read())
    image_string = image_string.decode('ascii') 
    dbA.update_one({'_id': ObjectId(id)}, {'$set': {
        "profilepic" :  image_string
        
    }})
    return jsonify({'msg': "Admin Update Successfully"})
    
########################## upload vehicle picture
@app.route('/vehicle/pic/<id>', methods=['POST'])
def uploadVg(id):
    image = request.files['pic']  
    image_string = base64.b64encode(image.read())
    image_string = image_string.decode('ascii') 
    dbV.update_one({'_id': ObjectId(id)}, {'$set': {
        "pic" :  image_string
        
    }})
    return jsonify({'msg': "Pic Update Successfully"})
    
########################## upload image for the worker from the app
@app.route('/admins/profilepic/mob', methods=['POST'])
def uploadImgee():
    worker = {
        "email":request.json['email'],
        "profilepic":request.json['profilepic']
    }
    user =  dbW.find_one({"email":worker['email']}) 

   
    dbW.update_one(user ,{'$set': {
        "profilepic" :  worker['profilepic']
        
    }})
    return jsonify({'msg': "Profile pic Update Successfully"})
 ##################################### upload image for the worker from the webapp
@app.route('/workers/profilepic/<id>', methods=['POST'])
def uploadImge(id):
    image = request.files['profilepic']  
    image_string = base64.b64encode(image.read())
    image_string = image_string.decode('ascii')
    dbW.update_one({'_id': ObjectId(id)}, {'$set': {
        "profilepic" :  image_string
        
    }})
    return jsonify({'msg': "Admin Update Successfully"})
##################################### add worker to database
@app.route('/workers', methods=['POST'])
def addWorker():
    if dbW.find_one({"email":request.json['email']}):
        return jsonify({"msg":"Email address already in use"})
    with open('profile.txt', 'r') as f: 
     text=f.read()
     
    id = dbW.insert_one({
        'fName': request.json['fName'],
        'email': request.json['email'],
        'phoneNumber': request.json['phoneNumber'],
        'age': request.json['age'],
        'ID':request.json['ID'],
        "licen":request.json['licen'],
        "gender":request.json['gender'],
        "address":request.json['address'],
        "vehcile":"",
        'password':pbkdf2_sha256.hash(request.json['ID']),
        'profilepic':text,
        "hours":[],
        "reports":[],
        "Location":{'Lati':"","Long":""},
        'requestShift':{'Sun':"", 'Mon':"", 'Tue':"",'Wed':"",'Thur':"",'Fri':""},
        "weekShifts":{'Sun':{'hours':"",'info':""},
        'Mon':{'hours':"",'info':""},
        'Tue':{'hours':"",'info':""},
        'Wed':{'hours':"",'info':""},
        'Thur':{'hours':"",'info':""},
        'Fri':{'hours':"",'info':""},
        'Sat':{'hours':"",'info':""}}
    })
    email = request.json['email']
    name = request.json['fName']
    msg = Message('Master Way Welcome', sender =   'masterway.eliaatours@gmail.com', recipients = [email] )
    msg.body = "Welcome" + " " + name  +" "+"to Master Way "+"\r\n"+ "you have to download the app from this link : https://play.google.com/store/apps/details?id=com.masterway&ah=n9u2gx49nxmOYuuVlYGrVt4AF3I "+"\r\n"+ "you can sign in on the app using your email and id as the password , you can change the password after u sign in"
    mail.send(msg)
    return jsonify({'msg': "Worker Added Successfully"})
    
    
    
########################## add shifts for the worker
@app.route('/trips/<id>', methods=['PUT'])
def addShifts(id):
    dbW.update_one({'_id': ObjectId(id)}, {'$set': {
        "weekShifts":{'Sun':{'hours':request.json['Sunday'],'info':request.json['Sun']},
        'Mon':{'hours':request.json['Monday'],'info':request.json['Mon']},
        'Tue':{'hours':request.json['Tuesday'],'info':request.json['Tue']},
        'Wed':{'hours':request.json['Wednesday'],'info':request.json['Wed']},
        'Thur':{'hours':request.json['Thursday'],'info':request.json['Thur']},
        'Fri':{'hours':request.json['Friday'],'info':request.json['Fri']},
        'Sat':{'hours':request.json['Saturday'],'info':request.json['Sat']}}
    }})
    return jsonify({'msg': "Shifts Added Successfully"})
   
########################## remove shifts of the worker
@app.route('/trips/<id>', methods=['PATCH'])
def removeShift(id):
    dbW.update_one({'_id': ObjectId(id)}, {'$set': {
       "weekShifts":{'Sun':{'hours':"",'info':""},
        'Mon':{'hours':"",'info':""},
        'Tue':{'hours':"",'info':""},
        'Wed':{'hours':"",'info':""},
        'Thur':{'hours':"",'info':""},
        'Fri':{'hours':"",'info':""},
        'Sat':{'hours':"",'info':""}}
    }})
    return jsonify({'msg': "Shifts Added Successfully"})

########################## get all the workers 

@app.route('/workers', methods=['GET'])
def getWorkers():
    workers = []
    for doc in dbW.find():
        workers.append({
            '_id': str(ObjectId(doc['_id'])),
            'fName': doc['fName'],
            'email': doc['email'],
            'phoneNumber': doc['phoneNumber'],
            'age': doc['age'],
            "ID":doc['ID'],
            'requesteShift':doc['requestShift'],
            'weekShifts':doc['weekShifts'],
            
        })
    return jsonify(workers)

########################## get wokrer by the id

@app.route('/workers/<id>', methods=['GET'])
def getWorker(id):
    worker = dbW.find_one({'_id': ObjectId(id)})
    return jsonify({
            '_id': str(ObjectId(worker['_id'])),
            'fName': worker['fName'],
            'email': worker['email'],
            "ID":worker['ID'],
            'phoneNumber': worker['phoneNumber'],
            'age': worker['age'],
            'requesteShift':worker['requestShift'],
            'weekShifts':worker['weekShifts'],
            "profilepic":worker['profilepic'],
            "reports":worker['reports']
    })
########################## get worker info
@app.route('/workers/profile/<id>', methods=['GET'])
def getWorkerProfile(id):
    worker = dbW.find_one({'_id': ObjectId(id)})
    return jsonify({
            '_id': str(ObjectId(worker['_id'])),
            'fName': worker['fName'],
            'email': worker['email'],
            "ID":worker['ID'],
            'phoneNumber': worker['phoneNumber'],
            'age': worker['age'],
            'requesteShift':worker['requestShift'],
            'weekShifts':worker['weekShifts'],
            "profilepic":worker['profilepic'],
            "age":worker['age'],
            "address":worker['address'],
            "gender":worker['gender'],
            "licen":worker['licen'],
            "vehcile":worker['vehcile'],
              "reports":worker['reports']
    })
########################## delete worker

@app.route('/workers/<id>', methods=['DELETE'])
def deleteWorker(id):
    dbW.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': "Worker Deleted Successfully"})

########################## update worker info from the web

@app.route('/workers/<id>', methods=['PUT'])
def updateWorker(id):
    dbW.update_one({'_id': ObjectId(id)}, {'$set': {
         'fName': request.json['fName'],
         'email': request.json['email'],
         'phoneNumber': request.json['phoneNumber'],
         'age': request.json['age'],
         'ID':request.json['ID']
    }})
    return jsonify({'msg': "Worker Update Successfully"})

####################################### add vehicle to database
@app.route('/vehicles', methods=['POST'])
def addVechicles():
    with open('vehicle.txt', 'r') as f: 
      text=f.read()
    id = dbV.insert_one({
        'man': request.json['man'],
        'model': request.json['model'],
        'year': request.json['year'],
        'lice':request.json['lice'],
        "insu":request.json['insu'],
        "status":'1',
        "repairs":[],
        "pic":text

    })
    return jsonify({'id': f"{id.inserted_id}", 'msg': "Vehicle Added Successfully"})    
####################################### get all vehicles
@app.route('/vehicles', methods=['GET'])
def getVehicles():
    vehicles = []
    for doc in dbV.find():
        vehicles.append({
            '_id': str(ObjectId(doc['_id'])),
            'man': doc['man'],
            'model': doc['model'],
            'year': doc['year'],
             'lice':doc['lice'],
        "insu":doc['insu'],
        "status":doc['status'],
        "repairs":doc['repairs']
        })
    return jsonify(vehicles)
####################################### get vhicel by the id
@app.route('/vehicles/<id>', methods=['GET'])
def getVehicle(id):
    vehicle = dbV.find_one({'_id': ObjectId(id)})
    return jsonify({
            '_id': str(ObjectId(vehicle['_id'])),
            'man': vehicle['man'],
            'model': vehicle['model'],
            'year': vehicle['year'],
             'lice':vehicle['lice'],
        "insu":vehicle['insu'],
        "status":vehicle['status'],
        "repairs":vehicle['repairs'],
        "pic":vehicle['pic']
    })
########################## deltet vehicle
@app.route('/vehicles/<id>', methods=['DELETE'])
def deleteVehicle(id):
    dbV.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': "Vehicle Deleted Successfully"})

########################## update vehicle 
@app.route('/vehicles/<id>', methods=['PUT'])
def updateVehicle(id):
    dbV.update_one({'_id': ObjectId(id)}, {'$set': {
         'man': request.json['man'],
         'model': request.json['model'],
         'year': request.json['year'],
            'lice':request.json['lice'],
        "insu":request.json['insu'],
        "status":request.json['status'],
        "repairs":request.json['repairs']
         
    }})
    return jsonify({'msg': "Vehicle Update Successfully"})
###################################### login from the app
@app.route('/mobapp', methods=['POST'])
def login():
    worker = {
        "email":request.json['email'],
        "password":request.json['password']
    }
 
    user =  dbW.find_one({"email":worker['email']}) 
    if user and pbkdf2_sha256.verify(worker["password"], user['password']):
        access_token = create_access_token(identity=user['email'])
        access = {
        
        "token":access_token,
        '_id': str(ObjectId(user['_id'])),
        'fName': user['fName'],
        'email': user['email'],
        "ID":user['ID'],
        'phoneNumber': user['phoneNumber'],
        'age': user['age'],
        'profilepic':user['profilepic'],
        'requesteShift':user['requestShift'],
        'weekShifts':user['weekShifts'],
        "reports":user['reports']
        }
        return jsonify(access),200
        
    return jsonify("wrong email or wrong password"),401    
######################################################## get the profile of the worker to the app
@app.route('/workers/appprofile', methods=['PUT'])
def getp():
    worker = {
        "email":request.json['email'],
    }
    user =  dbW.find_one({"email":worker['email']}) 

   
    return jsonify({
            '_id': str(ObjectId(user['_id'])),
           'fName': user['fName'],
            'email': user['email'],
            'ID': user['ID'],
            'phoneNumber': user['phoneNumber'],
            'age': user['age'],
            'profilepic':user['profilepic'],
            'requesteShift':user['requestShift'],
            'weekShifts':user['weekShifts'],
            "reports":user['reports']
            
    })

######################################
######################################################## update worker info from the app
@app.route('/workers/app', methods=['PUT'])
def updatee():
    worker = {
        "email":request.json['email'],
        'fName': request.json['fName'],
        'phoneNumber': request.json['phoneNumber'],
        'age': request.json['age'],
        
    }
    user =  dbW.find_one({"email":worker['email']}) 

   
    dbW.update_one(user ,{'$set': {
        'fName': worker['fName'],
        'email': worker['email'],
        'phoneNumber': worker['phoneNumber'],
        'age': worker['age'],
        
     }})
    return jsonify({"msg":"Done"})

####################################### send the requested shifts of the worker
@app.route('/workers/app/send', methods=['PUT'])
def Send():
    worker = {
        "email":request.json['email'],
        
    }
    user =  dbW.find_one({"email":worker['email']}) 

   
    dbW.update_one(user ,{'$set': {
        "requestShift":{'Sun':request.json['Sun'],
        'Mon':request.json['Mon'],
        'Tue':request.json['Tue'],
        'Wed':request.json['Wed'],
        'Thur':request.json['Thur'],
        'Fri':request.json['Fri'],
        'Sat':request.json['Sat']}}}
     )
    return jsonify({"msg":"Done"})


####################################### send loctaion of the vehicle every minute
@app.route('/workers/getlocation', methods=['PUT'])
def SendLocation():
    worker = {
        "email":request.json['email'],
        
    }
    user =  dbW.find_one({"email":worker['email']}) 

   
    dbW.update_one(user ,{'$set': {
        "Location":{'Lati':request.json['Lati'],
        'Long':request.json['Long'],
       }}}
     )
    return jsonify({"msg":"Done"})

##################################################### send the hours that worker did
@app.route('/workers/hours', methods=['PUT'])
def sendHours():
    worker = {
        "email":request.json['email'],
        
    }
    user =  dbW.find_one({"email":worker['email']}) 
   
   
    dbW.update_one(user ,{'$push': {
        "hours":{"day":request.json['day'],"hour":request.json['hour'],}
       }}
     )
    return jsonify({"msg":"Done"})
##################################################### get the hours that the worker did from the app
@app.route('/workers/hours/', methods=['PATCH'])
def gethours():
    worker = dbW.find_one({'email': request.json['email']})
    hours = worker['hours']
    month = request.json['month']
    hourss = []
    for x in hours:
     if month in x['day']:
        hourss.append(x)

    return jsonify({
            'fName': worker['fName'],
            'email': worker['email'],
           "hours":hourss
          
           
    })
#############################################  get the hours that the worker did  from the webapp
@app.route('/workersHours/<id>', methods=['PATCH'])
def gethourss(id):
    worker = dbW.find_one({'_id': ObjectId(id)})
    hours = worker['hours']
    month = request.json['month']
    hourss = []
    for x in hours:
     if month in x['day']:
        hourss.append(x)

    return jsonify(
           hourss
    )
################################  get the locations of the vehicles
@app.route('/map', methods=['GET'])
def locations():
    workers = []
    for doc in dbW.find():
        workers.append({
            '_id': str(ObjectId(doc['_id'])),
            'fName': doc['fName'],
            'location': doc['Location'],
            "vehcile":doc['vehcile']
        })
    return jsonify(workers)
############################################### send fix report
@app.route('/fix/<id>', methods=['PUT'])
def sendfix(id):
    vehicle = dbV.find_one({'_id': ObjectId(id)})
   
    
  
     
    dbV.update_one(vehicle ,{'$push': {
        "repairs":{"problem":request.json['problem'],"from":request.json['from'],"to":"","price":"","description":request.json['description'],"status":"0"}
       }}
     )
          
   
     
    return jsonify({"msg":"Done"})    
############################# delete fix report
@app.route('/fix/<id>', methods=['PATCH'])
def deleteFix(id):
    vehicle = dbV.find_one({'_id': ObjectId(id)})
    description = request.json['description']
    problem = request.json['problem']
    frome = request.json['from']
   
    dbV.update_one(vehicle ,{'$pull': {
        "repairs":{"description":description,"problem":problem,"from":frome}
        
       }}
     )
  
    return jsonify({"msg":"Done"})    
############################################ update the fix report
@app.route('/fixupdate/<id>', methods=['PATCH'])
def updateFix(id):
    vehicle = dbV.find_one({'_id': ObjectId(id)})
    description = request.json['description']
    problem = request.json['problem']
    frome = request.json['from']
   
    dbV.update_one(vehicle ,{'$set': {
        "status":"1"
        
       }}
     )
    dbV.update_one({'_id': ObjectId(id) , "repairs.description":description , "repairs.problem":problem , "repairs.from":frome},{'$set': {
        "repairs.$.price":request.json['price'],
        "repairs.$.to":request.json['to'],
        "repairs.$.status":"1"
        
       }}
     )
    budget = {
        "Name":request.json['problem'],
        "cost":request.json['price'],
        "date":request.json['to'],
        "type":"outcome",
        "description":request.json['description']
    }
    dbB.insert_one(budget)
    return jsonify({"msg":"Done"})    
############################ link vehicle to worker
@app.route('/workervehicle/<id>', methods=['PUT'])
def updateWorkerVehicle(id):
    dbW.update_one({'_id': ObjectId(id)}, {'$set': {
         'vehcile': request.json['vehcile'],
        
    }})
    return jsonify({'msg': "Vehilce added Successfully"})
  
 
########################################### upload salary report image to the worker
@app.route('/hoursreport/<id>', methods=['POST'])
def uploadRe(id):
    worker = dbW.find_one({'_id': ObjectId(id)})
    
    date = request.json['date']
    for x in worker['reports']:
        if(x['date'] == request.json['date']):
          dbW.update_one({'_id': ObjectId(id) , "reports.date":date},{'$set': {
          "reports.$.file":request.json['file'],
         
        
          }})
              
          return jsonify({'msg': "file uploaded Successfully"})  
        
   
   
    
    dbW.update_one({'_id': ObjectId(id)}, {'$push': {
        "reports" : {"date":request.json['date'],"file":request.json['file']} 
        
    }})
    return jsonify({'msg': "file uploaded Successfully"})    
##################################### get the salary reports of the worker
@app.route('/hoursreport/<id>', methods=['PATCH'])
def getRe(id):
    worker = dbW.find_one({'_id': ObjectId(id)})
    reports = []
    for x in worker['reports']:
        if(x['date'][0]+x['date'][1]+x['date'][2]+x['date'][3] == request.json['date'][0]+request.json['date'][1]+request.json['date'][2]+request.json['date'][3]):
          reports.append(x)
    return jsonify(reports)     
    
  
if __name__ == '__main__':
    app.run()
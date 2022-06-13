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
api_budget = Blueprint('api_budget',__name__)

############ add income or outcome
@api_budget.route('/budget', methods=['POST'])
def addBudget():
    dbB = mongo.db.budgets
    budget ={
        'Name': request.json['Name'],
        'date': request.json['date'],
      
        'description':request.json['description'],
        'type': request.json['type'],
        'cost': request.json['cost'],
       
        
    }
  
    dbB.insert_one(budget)
  
    return jsonify({ 'msg': "Budget Added Successfully"}) 
############# get outcome and icnomes
@api_budget.route('/budget', methods=['GET'])
def getBudgets():
    
    dbB = mongo.db.budgets
    budgets = []
    for doc in dbB.find():
        budgets.append({
            '_id': str(ObjectId(doc['_id'])),
            'Name': doc['Name'],
            'date': doc['date'],
            'description':doc['description'],
            'type': doc['type'],
            'cost': doc['cost'],
       
        })
    return jsonify(budgets)
################################ get budget by id


@api_budget.route('/budget/<id>', methods=['GET'])
def getBudget(id):
    dbB = mongo.db.budgets
    budget = dbB.find_one({'_id': ObjectId(id)})
    return jsonify({
            '_id': str(ObjectId(budget['_id'])),
            'Name': budget['Name'],
            'date': budget['date'],
            'description':budget['description'],
            'type': budget['type'],
            'cost': budget['cost'],
             
    })

##################### delete budget
@api_budget.route('/budget/<id>', methods=['DELETE'])
def deleteBudget(id):
    dbB = mongo.db.budgets
    dbB.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': "Budget Deleted Successfully"})
################################# update budget
@api_budget.route('/budget/<id>', methods=['PUT'])
def updateBudget(id):
    dbB = mongo.db.budgets
    dbB.update_one({'_id': ObjectId(id)}, {'$set': {
         'Name': request.json['Name'],
        'date': request.json['date'],
      
        'description':request.json['description'],
        'type': request.json['type'],
        'cost': request.json['cost'],
    }})
    return jsonify({'msg': "Budget Update Successfully"})

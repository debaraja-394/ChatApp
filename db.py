from pymongo import MongoClient
from werkzeug.security import generate_password_hash

from ChatApp.users import User

client=MongoClient("mongodb+srv://raja:iYAgvp1Xo0RCUteF@cluster0.htzsf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db=client.get_database("ChatDB")

users_collection=db.get_collection("users")

def save_user(username,email,password):
    hash_password=generate_password_hash(password)
    users_collection.insert_one({
        '_id':username,
        'email':email,
        'password':hash_password
    })

def get_user(username):
    user=users_collection.find_one({'_id':username})
    return User(user['_id'],user['email'],user['password'])
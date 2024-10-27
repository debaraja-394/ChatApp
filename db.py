from pymongo import MongoClient
from werkzeug.security import generate_password_hash

client=MongoClient("mongodb+srv://raja:iYAgvp1Xo0RCUteF@cluster0.htzsf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db=client.get_database("ChatDB")

users=db.get_collection("users")

def save_user(username,email,password):
    hash_password=generate_password_hash(password)
    users.insert_one({
        '_id':username,
        'email':email,
        'password':hash_password
    })
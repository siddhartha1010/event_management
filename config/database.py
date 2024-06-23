from pymongo import MongoClient

client=MongoClient("mongodb+srv://employee:employee123@cluster0.t1qjxxr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db=client.employee_db

collection_name=db["employee_management"]
collection=db["task_management"]
employee_collection=db["employee_detail"]
token_collection=db["token_collection"]
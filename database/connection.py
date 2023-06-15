from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
# Connect to the local MongoDB instance
db_username=os.getenv("db_username")
db_password=os.getenv("db_password")
db_host=os.getenv("db_host")
db_port=os.getenv("db_port")
db_name=os.getenv("db_name")
print(f'db_port{db_port}')
courses_collection_name='courses'

client = MongoClient(f'mongodb://{db_username}:{db_password}@{db_host}:{db_port}/')
print(f'client_{client}')
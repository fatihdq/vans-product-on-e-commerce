from pymongo import MongoClient
import json
from pprint import pprint

client = MongoClient('localhost:27017')

db = client.admin

serverStatusResult = db.command("serverStatus")
pprint(serverStatusResult)
from pymongo import MongoClient, collection
import json

CLIENT = MongoClient('localhost',27017, maxPoolSize=50)
DB = CLIENT['ecomerce_product']

shopee_collection =  DB['shopee']
tokopedia_collection = DB['tokopedia']

def import_tokopedia():
    with open('./scraping/vans_tokped.json',encoding='utf-8') as file:
        file_data = json.load(file)
    if isinstance(file_data, list):
        tokopedia_collection.insert_many(file_data)
    else:
        tokopedia_collection.insert_one(file_data)

def import_shopee():
    with open('./scraping/vans_shopee.json',encoding='utf-8') as file:
        file_data = json.load(file)
    if isinstance(file_data, list):
        shopee_collection.insert_many(file_data)
    else:
        shopee_collection.insert_one(file_data)

def retrieve_shopee():
    try:
        collect = shopee_collection.find({})
        shope_json = dict()
        i = 0
        for data in collect:
            shope_json[i] = data
            i+=1
        print("Load data of shopee successfuly")
        return shope_json
    except:
        print("Error while Load data of shopee")

def retrieve_tokopedia():
    try:
        collect = tokopedia_collection.find({})
        tokopedia_json = dict()
        i = 0
        for data in collect:
            tokopedia_json[i] = data
            i+=1
        print("Load data of tokopedia successfuly")
        return tokopedia_json
    except:
        print("Error while Load data of tokopedia")

import json
import base64
import requests
import jsonschema
import random
import pymongo
import psycopg2
from jsonschema import validate

request_picklist_schema = {
	"type": "object",
	"required": [
		"data"
	],
	"properties": {
		"data": {
			"$id": "#root/data",
			"title": "Data",
			"type": "object",
			"required": [
				"pickups"
			],
			"properties": {
				"pickups": {
					"$id": "#root/data/pickups",
					"title": "Pickups",
					"type": "array",
					"default": [],
					"items":{
						"$id": "#root/data/pickups/items",
						"title": "Items",
						"type": "string",
						"default": "",
						"pattern": "^.*$"
					}
				}
			}
		}
	}
}


staging_db_connection_uri = "mongodb+srv://staging-admin:VpbUDlaBkv4vTzJ8@tsm-staging.mlxar.mongodb.net/db_pando_staging"
database_name = "db_pando_testing"
collection_name = "requestpicklist"
client_user_name = "pandobritanniaauto@gmail.com"
client_password = "test@1234"
client_endpoint = "https://britannia-auto.pandostaging.in"
client_resource_path = "/api/erp/delivery_picklist"

#To get the database connection
def get_connection():
    client = pymongo.MongoClient(staging_db_connection_uri)
    database = client[database_name]
    collection = database[collection_name]
    return collection

#To insert record into database
def insert_into_database(content):
    result = get_connection().insert_one(content)
    print ("result _id:", result.inserted_id)
    print(content)
    return ""

#To send the delivery_picklist to the client
def send_delivery_picklist (content):

    #isValid = validateJson(content)

    if True:

        list = []

        for _arr in range(len(content['data']['pickups'])):
            data = {}
            data['delivery_number']="A110312073"+ str(_arr)
            data['material_code']="000000000000990225"
            data['depot_ref_id']=str(content['data']['pickups'][_arr])
            data['gate_ref_id']=str(content['data']['pickups'][_arr])
            data['division']='DIV'
            data['quantity']='10'
            data['quantity_unit']='NOS'
            data['weight']='950'
            data['weight_unit']='KG'
            data['volume']='500.00'
            data['volume_unit']='CFT'
            data['lr_number']='lr_number'
            data['ship_to']='18971'
            data['sold_to']='18971'
            data['line_item']='line_item'
            data['type']='SECONDARY'
            list.append(data)

        insert_into_database(content)
        print('{"data":"'+str(list)+'"}')
        response = requests.post(client_endpoint + client_resource_path, json={"data": list}, auth=(client_user_name, client_password))
        print(response)
        return 200
    else:
        print("Json payload is not valid")
        return 500

def validateJson(jsonData):
    try:
        validate(instance=jsonData, schema=request_picklist_schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True
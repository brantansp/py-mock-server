import json
import random
import pymongo
import psycopg2
import response
import jsonschema
from jsonschema import validate, ValidationError, SchemaError

staging_db_connection_uri = "mongodb+srv://staging-admin:VpbUDlaBkv4vTzJ8@tsm-staging.mlxar.mongodb.net/db_pando_staging"
database_name = "db_pando_testing"
invoice_retry_count = 0
invoice_numbers = {}

def get_schema():
    with open('response/epod_rejection.json', 'r') as file:
        schema = json.load(file)
    return schema

#To get the database connection
def get_connection(collection_name):
    client = pymongo.MongoClient(staging_db_connection_uri)
    database = client[database_name]
    collection = database[collection_name]
    return collection

def epod_rejection_validate_json(jsonData):
    try:
        validate(instance=jsonData, schema=get_schema())
        return True
    except ValidationError as err:
        return False

#To insert record into database
def epod_rejection_flow_insert_to_db(content):
    isValid = epod_rejection_validate_json(content)

    if isValid:
        result = get_connection('epod_rejection').insert_one(content)
        return "200"
    else:
        print("Json payload is not valid")
        print(content)
        return "403"
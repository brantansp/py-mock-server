import json
import random
import pymongo
import psycopg2
from jsonschema import validate, ValidationError, SchemaError

staging_db_connection_uri = "mongodb+srv://staging-admin:VpbUDlaBkv4vTzJ8@tsm-staging.mlxar.mongodb.net/db_pando_staging?ssl=true&ssl_cert_reqs=CERT_NONE"
database_name = "db_pando_testing"

#To get the database connection
def get_connection(collection_name):
    client = pymongo.MongoClient(staging_db_connection_uri)
    database = client[database_name]
    collection = database[collection_name]
    return collection

def get_schema(schemaFilePath):
    with open(schemaFilePath, 'r') as file:
        schema = json.load(file)
    return schema

def pg_insert_into_database(content):

    isValid = pgValidateJson(content)

    if True:
        result = get_connection('freight_bill_posting').insert_one(content)
        return True
    else:
        print("Json payload is not valid")
        return False

def pgValidateJson(jsonData):
    try:
        validate(instance=jsonData, schema=get_schema('response/pg_freight_bill_posting_schema.json'))
        return True
    except ValidationError as err:
        return False
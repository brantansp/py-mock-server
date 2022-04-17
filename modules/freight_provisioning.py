import json
import random
import pymongo
import psycopg2
from jsonschema import validate, ValidationError, SchemaError

staging_db_connection_uri = "mongodb+srv://staging-admin:VpbUDlaBkv4vTzJ8@tsm-staging.mlxar.mongodb.net/db_pando_staging?ssl=true&ssl_cert_reqs=CERT_NONE"
database_name = "db_pando_testing"
fp_retry_count = 0
invoice_numbers = {}

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

#To insert record into database
def srf_insert_into_database(content):
    print(content)
    result = get_connection('srf_freight_provisioning').insert_one(content)
    return 200

#To insert record into database
def oel_insert_into_database(content):
    print(content)
    result = get_connection('freight_provisioning').insert_one(content)
    return 200

def pg_insert_into_database(content):

    #isValid = pgValidateJson(content)

    if True:
        result = get_connection('freight_provisioning').insert_one(content)
        return True
    else:
        print("Json payload is not valid")
        return False

def tcp_insert_into_database(content):
    print(content)
    result = get_connection('tcp_freight_provisioning').insert_one(content)
    return 200

def respond_for_oel_freight_provision(content):
    indent_number = content['indent_number']
    material_invoice_number = content['material'][0]['material_invoice_number']
    response = respond_for_freight_provision(material_invoice_number,indent_number)
    insert_response_into_database(response)
    return response

def respond_for_freight_provision(invoice_number,indent_number):

    global fp_retry_count
    global invoice_numbers

    if invoice_number not in invoice_numbers.keys():
        invoice_numbers[invoice_number] = 0

    max_retry_count = 0

    try:
        max_retry_count = invoice_number[1]
        max_retry_count = int(max_retry_count) if (max_retry_count != 0 and int(max_retry_count) < 4) else 3
    except Exception as e:
        max_retry_count = 3

    messages_success = {}
    messages_failure = {}

    # build tab message success
    with open('response/freight_provision_response.json') as f1:
        data1 = json.load(f1)
        data1['item'][0]['TYPE'] = "S"
        data1['item'][0]['MESSAGE_V1'] = indent_number
        data1['item'][0]['MESSAGE'] = 'Entrysheet'+ invoice_number +'created'
        messages_success = json.dumps(data1)
        #messages_success.append(response)

    # build tab message failure
    with open('response/invoice_posting_response.json') as f2:
        data2 = json.load(f2)
        data2['item'][0]['TYPE'] = "E"
        data2['item'][0]['MESSAGE_V1'] = indent_number
        data2['item'][0]['MESSAGE'] = 'There is different account assignment information in item ' + invoice_number
        messages_failure = json.dumps(data2)
        #messages_failure.append(response)

    if invoice_number.startswith('E'):
        if invoice_numbers[invoice_number] >= max_retry_count:
            invoice_numbers.pop(invoice_number)
            return messages_success
        else:
            invoice_numbers[invoice_number] = invoice_numbers[invoice_number] + 1
            return messages_failure
    elif invoice_number.startswith('F'):
        return messages_failure
    else:
        return messages_success

def insert_response_into_database(content):
    result = get_connection('freight_provision_response').insert_one(json.loads(str(content)))
    print("result _id:", result.inserted_id)
    return ""

def pgValidateJson(jsonData):
    try:
        validate(instance=jsonData, schema=get_schema('response/pg_freight_provision_schema.json'))
        return True
    except ValidationError as err:
        return False
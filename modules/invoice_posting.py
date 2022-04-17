import json
import random
import pymongo
import psycopg2
from jsonschema import validate, ValidationError, SchemaError

staging_db_connection_uri = "mongodb+srv://staging-admin:VpbUDlaBkv4vTzJ8@tsm-staging.mlxar.mongodb.net/db_pando_staging?ssl=true&ssl_cert_reqs=CERT_NONE"
database_name = "db_pando_testing"
#collection_name = "invoice_posting"
invoice_retry_count = 0
invoice_numbers = {}

def get_schema(schemaFilePath):
    with open(schemaFilePath, 'r') as file:
        schema = json.load(file)
    return schema

#To get the database connection
def get_connection(collection_name):
    client = pymongo.MongoClient(staging_db_connection_uri)
    database = client[database_name]
    collection = database[collection_name]
    return collection

#To insert record into database
def srf_insert_into_database(content):
    #isValid = srfValidateJson(content)
    #Commenting the schema validation as it done in fitnesse

    if True:
        result = get_connection('srf_invoice_posting').insert_one(content)
        return True
    else:
        print("Json payload is not valid")
        return False

#To insert record into database
def strategy_1_insert_into_database(content):
    #isValid = strategy1ValidateJson(content)

    if True:
        result = get_connection('strategy_1_invoice_posting').insert_one(content)
        return 200
    else:
        print("Json payload is not valid")
        return 500

#To insert record into database
def strategy_2_insert_into_database(content):
    #isValid = strategy2ValidateJson(content)
    #Commenting the payload schema validation as it is moved to fitnesse

    if True:
        result = get_connection('strategy_2_invoice_posting').insert_one(content)
        return 200
    else:
        print("Json payload is not valid")
        return 500

def strategy1ValidateJson(jsonData):
    try:
        validate(instance=jsonData, schema=get_schema('response/strategy_1_invoice_posting_schema.json'))
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True

def strategy2ValidateJson(jsonData):
    try:
        validate(instance=jsonData, schema=get_schema('response/strategy_2_invoice_posting_schema.json'))
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True

def srfValidateJson(jsonData):
    try:
        validate(instance=jsonData, schema=get_schema('response/srf_invoice_posting_schema.json'))
        return True
    except ValidationError as err:
        return False

#To insert record into database
def cpi_freight_invoice_insert_into_database(content):
    isValid = cpiFreightInvoiceJson(content)

    if isValid:
        result = get_connection('cpi_freight_invoice').insert_one(content)
        return 200
    else:
        print("Json payload is not valid")
        return 500

def cpiFreightInvoiceJson(jsonData):
    try:
        validate(instance=jsonData, schema=get_schema('response/cpi_freight_invoice_posting_schema.json'))
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True

def respond_for_strategy_1_freight_invoice(content):
    invoice_number = content['invoice_number']
    response = response_for_posted_invoice_request(invoice_number,'strategy_1_invoice_posting')
    insert_response_into_database(response)
    return response

def respond_for_strategy_2_freight_invoice(content):
    invoice_number = content['invoice_number']
    return response_for_posted_invoice_request(invoice_number,'strategy_2_invoice_posting')

def respond_for_cpi_freight_invoice(content):
    invoice_number = content['invoice_number']
    return response_for_posted_invoice_request(invoice_number,'cpi_freight_invoice')

def respond_for_srf_freight_invoice(content):
    invoice_number = content['get_freight_invoice_dtl']['InputParameters']['P_FREIGHT_DETAILS_TBL']['items'][0]['INVOICE_NUMBER']
    return response_for_posted_invoice_request(invoice_number,'srf_invoice_posting')

#To insert record into database
def pay_v1_insert_into_database(content):
    #isValid = payV1ValidateJson(content)

    if True:
        result = get_connection('pay_v1_invoice_posting').insert_one(content)
        #print("result _id:", result.inserted_id)
        return 200
    else:
        print("Json payload is not valid")
        return 500

#To insert record into database
def tcp_insert_into_database(content):
    print(content)
    result = get_connection('tcp_invoice_posting').insert_one(content)
    return 200

def payV1ValidateJson(jsonData):
    try:
        validate(instance=jsonData, schema=get_schema('response/pay_v1_invoice_posting_schema.json'))
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True

def response_for_posted_invoice_request (invoice_number, collection):

    global invoice_retry_count
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
    with open('response/invoice_posting_response.json') as f1:
        data1 = json.load(f1)
        data1['item'][0]['TYPE'] = "S"
        data1['item'][0]['MESSAGE_V1'] = invoice_number
        data1['item'][0]['MESSAGE'] = 'Entrysheet'+ invoice_number +'created'
        messages_success = json.dumps(data1)
        #messages_success.append(response)

    # build tab message failure
    with open('response/invoice_posting_response.json') as f2:
        data2 = json.load(f2)
        data2['item'][0]['TYPE'] = "E"
        data2['item'][0]['MESSAGE_V1'] = invoice_number
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

#To insert record into database
def insert_response_into_database(content):
    result = get_connection('invoice_posting_response').insert_one(json.loads(str(content)))
    #print ("result _id:", result.inserted_id)
    return ""
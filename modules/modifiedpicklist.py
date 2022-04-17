import json
import random
import pymongo
import psycopg2
import xmltodict
import time

staging_db_connection_uri = "mongodb+srv://staging-admin:VpbUDlaBkv4vTzJ8@tsm-staging.mlxar.mongodb.net/db_pando_staging"
database_name = "db_pando_testing"
collection_name = "modifiedpicklist"
retry_count = 0
delete_retry_count = 0
delivery_number_retry_counter_map = {}
delivery_number_max_retry_counter_map = {}

#To get the database connection
def get_connection(collection_name):
    client = pymongo.MongoClient(staging_db_connection_uri)
    database = client[database_name]
    collection = database[collection_name]
    return collection

#To insert record into database
def delay_in_responding_modified_picklist(content):
    time.sleep(180)
    return ""

#To insert record into database
def insert_into_database(content):
    result = get_connection('modifiedpicklist').insert_one(content)
    print ("result _id:", result.inserted_id)
    return ""

#To insert record into database
def insert_response_into_database(content):
    result = get_connection('modifiedpicklistresponse').insert_one(json.loads(str(content).replace(".","_")))
    print ("result _id:", result.inserted_id)
    print(content)
    return ""

#To insert record into database
def tcp_insert_into_database(content):
    result = get_connection('tcpmodifiedpicklist').insert_one(json.loads(content))
    #print ("result _id:", result.inserted_id)
    return ""

#To respond back with required message of OEL's ERP
def respond_back_for_the_request(content):

    global retry_count
    global delete_retry_count

    indent_id = content['ModifiedPicklist']['ItemModifiedPicklist'][0]['indent_id']
    indent_id_1 = content['ModifiedPicklist']['ItemModifiedPicklist'][1]['indent_id']
    indication = content['ModifiedPicklist']['ItemModifiedPicklist'][0]['indication']

    if indication == 'CREATE' or indication == 'UPDATE' :
        transporter_code = content['ModifiedPicklist']['ItemModifiedPicklist'][0]['transporter_code']
        delivery_number = content['ModifiedPicklist']['ItemModifiedPicklist'][0]['delivery_number']
        depot_code = content['ModifiedPicklist']['ItemModifiedPicklist'][0]['depot_code']
        pickup_code = content['ModifiedPicklist']['ItemModifiedPicklist'][0]['pickup_code']
        ship_to = content['ModifiedPicklist']['ItemModifiedPicklist'][0]['ship_to']
        sold_to = content['ModifiedPicklist']['ItemModifiedPicklist'][0]['sold_to']
        vehicle_type = content['ModifiedPicklist']['ItemModifiedPicklist'][0]['vehicle_type']

        transporter_code_1 = content['ModifiedPicklist']['ItemModifiedPicklist'][1]['transporter_code']
        delivery_number_1 = content['ModifiedPicklist']['ItemModifiedPicklist'][1]['delivery_number']
        depot_code_1 = content['ModifiedPicklist']['ItemModifiedPicklist'][1]['depot_code']
        pickup_code_1 = content['ModifiedPicklist']['ItemModifiedPicklist'][1]['pickup_code']
        ship_to_1 = content['ModifiedPicklist']['ItemModifiedPicklist'][1]['ship_to']
        sold_to_1 = content['ModifiedPicklist']['ItemModifiedPicklist'][1]['sold_to']
        vehicle_type_1 = content['ModifiedPicklist']['ItemModifiedPicklist'][1]['vehicle_type']

        #success_response = '{"rfc:ZTMS_SD_DLV_MODIFIED_PICKLIST.Response":{"TAB_MESSAGES":{"item":[{"TYPE":"S","ID":"","NUMBER":"000","MESSAGE":"' + delivery_number + ' - Delivery posted successfully","LOG_NO":"","LOG_MSG_NO":"000000","MESSAGE_V1":"' + delivery_number + '","MESSAGE_V2":"' + indent_id + '","MESSAGE_V3":"","MESSAGE_V4":"","PARAMETER":"","ROW":"0","FIELD":"","SYSTEM":""}]},"TAB_PICKLIST":{"item":[{"VBELN":"' + delivery_number + '","INDENT_ID":"' + indent_id + '","POSNR":"000000","SPLIT":"","MATNR":"AT25AE","SPART":"","LFIMG":"70.000","MEINS":"EA","BRGEW":"100.000","GEWEI":"KG","VOLUM":"197.000","VOLEH":"CFT","BOLNR":"","KUNNR":"' + ship_to + '","KUNAG":"' + sold_to + '","TRANSPORTER_CODE":"' + transporter_code + '","VEHICLE_TYPE":"' + vehicle_type + '","VEHICLE_NO":"","DEPOT_CODE":"' + depot_code + '","PICKUP_CODE":"' + pickup_code + '","TYPE":"PRIMARY","INDICATION":"CREATE","TRUCK_IN_DATE":"","TRUCK_IN_TIME":""}]}}}'
        success_response = '{"rfc:ZTMS_SD_DLV_MODIFIED_PICKLIST.Response":{"TAB_MESSAGES":{"item":[{"TYPE":"S","ID":"","NUMBER":"000","MESSAGE":"' + delivery_number + ' - Delivery posted successfully","LOG_NO":"","LOG_MSG_NO":"000000","MESSAGE_V1":"' + delivery_number + '","MESSAGE_V2":"' + indent_id + '","MESSAGE_V3":"","MESSAGE_V4":"","PARAMETER":"","ROW":"0","FIELD":"","SYSTEM":""},{"TYPE":"S","ID":"","NUMBER":"000","MESSAGE":"' + delivery_number_1 + ' - Delivery posted successfully","LOG_NO":"","LOG_MSG_NO":"000000","MESSAGE_V1":"' + delivery_number_1 + '","MESSAGE_V2":"' + indent_id_1 + '","MESSAGE_V3":"","MESSAGE_V4":"","PARAMETER":"","ROW":"0","FIELD":"","SYSTEM":""}]},"TAB_PICKLIST":{"item":[{"VBELN":"' + delivery_number + '","INDENT_ID":"' + indent_id + '","POSNR":"000000","SPLIT":"","MATNR":"AT25AE","SPART":"","LFIMG":"70.000","MEINS":"EA","BRGEW":"100.000","GEWEI":"KG","VOLUM":"197.000","VOLEH":"CFT","BOLNR":"","KUNNR":"' + ship_to + '","KUNAG":"' + sold_to + '","TRANSPORTER_CODE":"' + transporter_code + '","VEHICLE_TYPE":"' + vehicle_type + '","VEHICLE_NO":"","DEPOT_CODE":"' + depot_code + '","PICKUP_CODE":"' + pickup_code + '","TYPE":"PRIMARY","INDICATION":"CREATE","TRUCK_IN_DATE":"","TRUCK_IN_TIME":""},{"VBELN":"' + delivery_number_1 + '","INDENT_ID":"' + indent_id_1 + '","POSNR":"000000","SPLIT":"","MATNR":"AT25AE","SPART":"","LFIMG":"70.000","MEINS":"EA","BRGEW":"100.000","GEWEI":"KG","VOLUM":"197.000","VOLEH":"CFT","BOLNR":"","KUNNR":"' + ship_to_1 + '","KUNAG":"' + sold_to_1 + '","TRANSPORTER_CODE":"' + transporter_code_1 + '","VEHICLE_TYPE":"' + vehicle_type_1 + '","VEHICLE_NO":"","DEPOT_CODE":"' + depot_code_1 + '","PICKUP_CODE":"' + pickup_code_1 + '","TYPE":"PRIMARY","INDICATION":"CREATE","TRUCK_IN_DATE":"","TRUCK_IN_TIME":""}]}}}'
        #failure_response = '{"rfc:ZTMS_SD_DLV_MODIFIED_PICKLIST.Response":{"TAB_MESSAGES":{"item":[{"TYPE":"E","ID":"","NUMBER":"000","MESSAGE":"PGI alredy processed for delivery ' + delivery_number + '","LOG_NO":"","LOG_MSG_NO":"000000","MESSAGE_V1":"' + delivery_number + '","MESSAGE_V2":"' + indent_id + '","MESSAGE_V3":"","MESSAGE_V4":"","PARAMETER":"","ROW":"0","FIELD":"","SYSTEM":""},{"TYPE":"E","ID":"","NUMBER":"000","MESSAGE":"PGI alredy processed for delivery ' + delivery_number + '","LOG_NO":"","LOG_MSG_NO":"000000","MESSAGE_V1":"' + delivery_number_1 + '","MESSAGE_V2":"' + indent_id_1 + '","MESSAGE_V3":"","MESSAGE_V4":"","PARAMETER":"","ROW":"0","FIELD":"","SYSTEM":""}]},"TAB_PICKLIST":{"item":[{"VBELN":"","INDENT_ID":"' + indent_id + '","POSNR":"000000","SPLIT":"","MATNR":"","SPART":"","LFIMG":"0.000","MEINS":"","BRGEW":"0.000","GEWEI":"","VOLUM":"0.000","VOLEH":"","BOLNR":"","KUNNR":"","KUNAG":"","TRANSPORTER_CODE":"","VEHICLE_TYPE":"","VEHICLE_NO":"","DEPOT_CODE":"","PICKUP_CODE":"","TYPE":"","INDICATION":"","TRUCK_IN_DATE":"","TRUCK_IN_TIME":""},{"VBELN":"","INDENT_ID":"' + indent_id_1 + '","POSNR":"000000","SPLIT":"","MATNR":"","SPART":"","LFIMG":"0.000","MEINS":"","BRGEW":"0.000","GEWEI":"","VOLUM":"0.000","VOLEH":"","BOLNR":"","KUNNR":"","KUNAG":"","TRANSPORTER_CODE":"","VEHICLE_TYPE":"","VEHICLE_NO":"","DEPOT_CODE":"","PICKUP_CODE":"","TYPE":"","INDICATION":"","TRUCK_IN_DATE":"","TRUCK_IN_TIME":""}]}}}'
        failure_response = '{"rfc:ZTMS_SD_DLV_MODIFIED_PICKLIST.Response":{"TAB_MESSAGES":{"item":[{"TYPE":"E","ID":"","NUMBER":"000","MESSAGE":"PGI alredy processed for delivery 0080077704","LOG_NO":"","LOG_MSG_NO":"000000","MESSAGE_V1":"0080077704","MESSAGE_V2":"' + indent_id + ',' + indent_id_1 + '","MESSAGE_V3":"","MESSAGE_V4":"","PARAMETER":"","ROW":"0","FIELD":"","SYSTEM":""}]}}}'

        if transporter_code.startswith('TEST'):
            return success_response

        else:
            if retry_count >= 3:
                retry_count = 0
                return success_response
            else:
                retry_count = retry_count + 1
                return failure_response

    elif indication == 'DELETE':
        delete_success_response = '{"rfc:ZTMS_SD_DLV_MODIFIED_PICKLIST.Response":{"TAB_MESSAGES":{"item":{"TYPE":"S","ID":"","NUMBER":"000","MESSAGE":"8010488965 - Delivery posted successfully","LOG_NO":"","LOG_MSG_NO":"000000","MESSAGE_V1":"8010488965","MESSAGE_V2":"' + indent_id + '","MESSAGE_V3":"","MESSAGE_V4":"","PARAMETER":"","ROW":"0","FIELD":"","SYSTEM":""}},"TAB_PICKLIST":{"item":[{"VBELN":"8010488965","INDENT_ID":"' + indent_id + '","POSNR":"000000","SPLIT":"","MATNR":"AT25AE","SPART":"","LFIMG":"70.000","MEINS":"EA","BRGEW":"100.000","GEWEI":"KG","VOLUM":"197.000","VOLEH":"CFT","BOLNR":"","KUNNR":"","KUNAG":"","TRANSPORTER_CODE":"","VEHICLE_TYPE":"","VEHICLE_NO":"","DEPOT_CODE":"","PICKUP_CODE":"","TYPE":"PRIMARY","INDICATION":"DELETE","TRUCK_IN_DATE":"","TRUCK_IN_TIME":""}]}}}'
        delete_failure_response = '{"rfc:ZTMS_SD_DLV_MODIFIED_PICKLIST.Response":{"TAB_MESSAGES":{"item":{"TYPE":"E","ID":"","NUMBER":"000","MESSAGE":"8010488965 - Delivery posted successfully","LOG_NO":"","LOG_MSG_NO":"000000","MESSAGE_V1":"8010488965","MESSAGE_V2":"' + indent_id + '","MESSAGE_V3":"","MESSAGE_V4":"","PARAMETER":"","ROW":"0","FIELD":"","SYSTEM":""}},"TAB_PICKLIST":{"item":[{"VBELN":"8010488965","INDENT_ID":"' + indent_id + '","POSNR":"000000","SPLIT":"","MATNR":"AT25AE","SPART":"","LFIMG":"70.000","MEINS":"EA","BRGEW":"100.000","GEWEI":"KG","VOLUM":"197.000","VOLEH":"CFT","BOLNR":"","KUNNR":"","KUNAG":"","TRANSPORTER_CODE":"","VEHICLE_TYPE":"","VEHICLE_NO":"","DEPOT_CODE":"","PICKUP_CODE":"","TYPE":"PRIMARY","INDICATION":"DELETE","TRUCK_IN_DATE":"","TRUCK_IN_TIME":""}]}}}'

        if delete_retry_count >= 2:
            delete_retry_count = 0
            return delete_success_response
        else:
            delete_retry_count = delete_retry_count + 1
            return delete_failure_response


def respond_back_for_the_request_with_retry (content):

    global delete_retry_count
    global delivery_number_retry_counter_map
    global delivery_number_max_retry_counter_map

    indent_id = content['ModifiedPicklist']['ItemModifiedPicklist'][0]['indent_id']
    indication = content['ModifiedPicklist']['ItemModifiedPicklist'][0]['indication']
    delivery_number = content['ModifiedPicklist']['ItemModifiedPicklist'][0]['delivery_number']
    retry_count = 0

    try:
        retry_count = delivery_number[1]
        max_retry_count = retry_count if (retry_count != 0 and int(retry_count) < 4) else 3
    except Exception as e:
        max_retry_count = 3

    items_modified_picklist = content["ModifiedPicklist"]["ItemModifiedPicklist"]

    tab_messages_success = []
    tab_messages_failure = []
    tab_picklist = []

    for item in items_modified_picklist:
        # build tab message success
        with open('response/modified_picklist_tab_message.json') as f:
            data = json.load(f)
            data['MESSAGE_V2'] = item['indent_id']
            data['MESSAGE_V1'] = item['delivery_number']
            data['MESSAGE'] = item['delivery_number'] + ' - Delivery posted successfully'
            response = json.dumps(data)
            tab_messages_success.append(response)

        # build tab message failure
        with open('response/modified_picklist_tab_message.json') as f:
            data = json.load(f)
            data['TYPE'] = 'E'
            data['MESSAGE'] = 'PGI already processed for delivery - '+item['delivery_number']
            data['MESSAGE_V2'] = item['indent_id']
            data['MESSAGE_V1'] = item['delivery_number']
            response = json.dumps(data)
            tab_messages_failure.append(response)

        # build tab picklist
        with open('response/modified_picklist_tab_picklist.json') as f:
            data = json.load(f)
            data['DELIVERY_NUMBER'] = item['delivery_number']
            data['INDENT_ID'] = item['delivery_number']
            data['MATNR'] = item['sku']
            data['LFIMG'] = item['quantity']
            data['MEINS'] = item['quantity_unit']
            data['BRGEW'] = item['weight']
            data['GEWEI'] = item['weight_unit']
            data['VOLUM'] = item['volume']
            data['VOLEH'] = item['volume_unit']
            data['KUNNR'] = item['ship_to']
            data['KUNAG'] = item['sold_to']
            data['TRANSPORTER_CODE'] = item['transporter_code']
            data['VEHICLE_TYPE'] = item['vehicle_type']
            data['VEHICLE_NO'] = item['vehicle_number']
            data['DEPOT_CODE'] = item['depot_code']
            data['PICKUP_CODE'] = item['pickup_code']
            data['TYPE'] = item['type']
            data['INDICATION'] = item['indication']
            response = json.dumps(data)
            tab_picklist.append(response)

    if indication == 'CREATE' or indication == 'UPDATE':
        success_response = '{"rfc:ZTMS_SD_DLV_MODIFIED_PICKLIST.Response":{"TAB_MESSAGES":{"item":[' + str(tab_messages_success).replace("[", "").replace("]", "").replace("'","").strip() + ']},"TAB_PICKLIST":{"item":[' + str(tab_picklist).replace("[", "").replace("]", "").replace("'", "").strip() + ']}}}'
        failure_response = '{"rfc:ZTMS_SD_DLV_MODIFIED_PICKLIST.Response":{"TAB_MESSAGES":{"item":[' + str(tab_messages_failure).replace("[", "").replace("]", "").replace("'", "").strip() + ']}}}'

        if not delivery_number in delivery_number_retry_counter_map.keys():
            delivery_number_retry_counter_map[delivery_number] = 0

        if delivery_number.startswith('E'):
            if delivery_number_retry_counter_map[delivery_number] >= int(max_retry_count):
                delivery_number_retry_counter_map.pop(delivery_number)
                return success_response
            else:
                delivery_number_retry_counter_map[delivery_number] = delivery_number_retry_counter_map[delivery_number] + 1
                return failure_response
        if delivery_number.startswith('F'):
            return failure_response
        else:
            return success_response

    elif indication == 'DELETE':
        delete_success_response = '{"rfc:ZTMS_SD_DLV_MODIFIED_PICKLIST.Response":{"TAB_MESSAGES":{"item":['+str(tab_messages_success).replace("[","").replace("]","").replace("'","").strip()+']},"TAB_PICKLIST":{"item":['+str(tab_picklist).replace("[","").replace("]","").replace("'","").strip()+']}}}'
        delete_failure_response = '{"rfc:ZTMS_SD_DLV_MODIFIED_PICKLIST.Response":{"TAB_MESSAGES":{"item":['+str(tab_messages_failure).replace("[","").replace("]","").replace("'","").strip()+']},"TAB_PICKLIST":{"item":['+str(tab_picklist).replace("[","").replace("]","").replace("'","").strip()+']}}}'

        if not delivery_number in delivery_number_retry_counter_map.keys():
            delivery_number_retry_counter_map[delivery_number] = 0

        if delivery_number.startswith('E'):
            if delivery_number_retry_counter_map[delivery_number] >= int(max_retry_count):
                delivery_number_retry_counter_map.pop(delivery_number)
                return delete_success_response
            else:
                delivery_number_retry_counter_map[delivery_number] = delivery_number_retry_counter_map[delivery_number] + 1
                return delete_failure_response
        if delivery_number.startswith('F'):
            return delete_failure_response
        else:
            return delete_success_response


def response_jsonmodifiedpicklistresponse():
    return '''
    {
  "rfc:ZTMS_SD_DLV_MODIFIED_PICKLIST.Response": {
    "TAB_MESSAGES": {
      "item": {
        "TYPE": "S",
        "ID": "",
        "NUMBER": "000",
        "MESSAGE": "8010669231 - Delivery posted successfully",
        "LOG_NO": "",
        "LOG_MSG_NO": "000000",
        "MESSAGE_V1": "8010669231",
        "MESSAGE_V2": "OEL-9006-O-2085",
        "MESSAGE_V3": "",
        "MESSAGE_V4": "",
        "PARAMETER": "",
        "ROW": "0",
        "FIELD": "",
        "SYSTEM": ""
      }
    },
    "TAB_PICKLIST": {
      "item": {
        "VBELN": "8010669231",
        "INDENT_ID": "OEL-9006-O-2085",
        "POSNR": "000010",
        "SPLIT": "",
        "MATNR": "171DPC0160",
        "SPART": "50",
        "LFIMG": "1.000",
        "MEINS": "kar",
        "BRGEW": "5.950",
        "GEWEI": "KG",
        "VOLUM": "0.520",
        "VOLEH": "CFT",
        "BOLNR": "",
        "KUNNR": "8109280",
        "KUNAG": "8109280",
        "TANSPORTER_CODE": "940061",
        "VEHICLE_TYPE": "CR01",
        "VEHICLE_NO": "",
        "DEPOT_CODE": "9006",
        "PICKUP_CODE": "9006",
        "TYPE": "SECONDARY",
        "INDICATION": "CREATE",
        "TRUCK_IN_DATE": "",
        "TRUCK_IN_TIME": ""
      }
    }
  }
}
    '''


def response_xmlmodifiedpicklistresponse ():
    return '''
    <?xml version="1.0" encoding="UTF-8"?>
<ModifiedPicklistIntermediate>
	<ModifiedPicklist>
		<ItemModifiedPicklist>
			<indent_id>BRT-MU01-O-8187</indent_id>
			<depot_code>MU01</depot_code>
			<pickup_code>MU01</pickup_code>
			<type>SECONDARY</type>
			<delivery_number>1050642754</delivery_number>
			<line_item_no>900088</line_item_no>
			<N></N>
			<sku>000000000000099979</sku>
			<division>DO</division>
			<quantity>8.00</quantity>
			<quantity_unit>nos</quantity_unit>
			<weight>51.07</weight>
			<weight_unit>nos</weight_unit>
			<volume>7.91</volume>
			<volume_unit>CFT</volume_unit>
			<lr_number></lr_number>
			<ship_to>0000022543</ship_to>
			<sold_to>0000022543</sold_to>
			<transporter_code>0000603405</transporter_code>
			<vehicle_type>Z005</vehicle_type>
			<vehicle_number></vehicle_number>
			<indication>UPDATE</indication>
			<truck_in_date_and_time></truck_in_date_and_time>
			<category>X</category>
			<created_date>2021/08/3108:10</created_date>
		</ItemModifiedPicklist>
		
	</ModifiedPicklist>
</ModifiedPicklistIntermediate>
    '''

from flask import Flask, request
from modules import courier
from modules import modifiedpicklist
from modules import deliverypicklist
from modules import invoice_posting
from modules import track_n_trace
from modules import pod_to_sap
from modules import epod_rejection
from modules import transporter_score
from modules import freight_provisioning
from modules import freight_bill_posting

app = Flask(__name__)

#courier integration => Create Booking
@app.route('/api/spoton/booking', methods=['POST'])
def spoton_create_booking():
    if request.method == 'POST':
       return ('', 200)

#courier integration => Create Booking
@app.route('/oauth/token', methods=['POST','PUT'])
def authorization():
    if request.method == 'POST':
       content = request.json
       return courier.authorize(content)

#courier integration => Create Booking
@app.route('/api/booking/create', methods=['POST'])
def create_booking():
    if request.method == 'POST':
       content = request.json
       return courier.create_booking(content)

#courier integration => Update Booking
@app.route('/api/booking/<booking_id>/materials', methods=['PUT'])
def update_material(booking_id):
    if request.method == 'PUT':
       content = request.json
       return courier.update_booking(booking_id, content)

#courier integration => Tracking Booking
@app.route('/api/booking/track', methods=['POST'])
def booking_track():
    if request.method == 'POST':
       content = request.json
       return courier.booking_track(content)

#courier delhivery provider
@app.route('/api/v3/track', methods=['POST'])
def v3_booking_track():
    if request.method == 'POST':
       content = request.json
       return courier.booking_track(content)

#courier integration => Epod Booking
@app.route('/api/booking/pod', methods=['POST'])
def booking_pod():
    if request.method == 'POST':
       content = request.json
       return courier.booking_pod(content)

#courier integration => Vechicle Requirment Date
@app.route('/api/booking/<booking_id>/vrdate', methods=['PUT'])
def booking_vechicle_req_date(booking_id):
    if request.method == 'PUT':
       content = request.json
       return courier.booking_vech_req_date(booking_id,content)

#Modified Picklist => POST
#In Client Configuration under erp_configuration this server's ip (a.k.a endpoint) and resource location (i.e path) should be configured
#This server listens for the API POST request and insert the response to db_pando_testing database
@app.route('/modifiedpicklist', methods=['POST'])
def modified_picklist():
    if request.method == 'POST':
       content = request.json
       return modifiedpicklist.insert_into_database(content)

#Modified Picklist => POST
#There will be 3 minutes delay before responding
@app.route('/modifiedpicklistdelay', methods=['POST'])
def modified_picklist_delay_response():
    if request.method == 'POST':
        return ('', 401)
       #content = request.json
       #return modifiedpicklist.delay_in_responding_modified_picklist(content)

#Modified Picklist => POST
#In Client Configuration under erp_configuration this server's ip (a.k.a endpoint) and resource location (i.e path) should be configured
#This server listens for the API POST request and insert the response to db_pando_testing database.
#Also respond back with required json content for mocking OEL's ERP
@app.route('/oelmodifiedpicklist', methods=['POST'])
def oel_modified_picklist():
    if request.method == 'POST':
       content = request.json
       modifiedpicklist.insert_into_database(content)
       return modifiedpicklist.respond_back_for_the_request(content)

#Modified Picklist => POST
#In Client Configuration under erp_configuration this server's ip (a.k.a endpoint) and resource location (i.e path) should be configured
#This server listens for the API POST request and insert the response to db_pando_testing database.
#Also respond back with required json content for mocking prince's ERP
@app.route('/modifiedpicklistwithresponse', methods=['POST'])
def modified_picklist_with_response():
    if request.method == 'POST':
       content = request.json
       modifiedpicklist.insert_into_database(content)
       response = modifiedpicklist.respond_back_for_the_request_with_retry(content)
       modifiedpicklist.insert_response_into_database(response)
       return (response,200)

#Modified Picklist => GET For the 1st leg of pullpicklist
#This server listens for the API GET request and Respond back with 204 No content request fulfilled response
@app.route('/api/optima/request_picklist/5e13140fadd4bd0ea3b88400/1', methods=['GET'])
def request_picklist():
    if request.method == 'GET':
        return ('',204)

#Modified Picklist => POST For the 2nd leg of pullpicklist
#In Client Configuration under erp_configuration this server's ip (a.k.a endpoint) and resource location (i.e path) should be configured
#This server listens for the API POST request and send an API POST to Pando-app client
@app.route('/deliverypicklistrequest', methods=['POST'])
def delivery_picklist():
    if request.method == 'POST':
        header = request.url_root
        content = request.json
        print(content)
        #print(header) #http://127.0.0.1:5001/
        #print(content) #{'data': {'pickups': ['100111']}}
        #print(request.path) #/deliverypicklistrequest
        return ('',deliverypicklist.send_delivery_picklist(content))

#Invoice Posting => POST
#In Client Configuration under erp_configuration this server's ip (a.k.a endpoint) and resource location (i.e path) should be configured
#This server listens for the API POST request and insert the response to db_pando_testing database
@app.route('/srf_invoice_posting', methods=['POST'])
def srf_invoice_posting():
    if request.method == 'POST':
       content = request.json
       if(invoice_posting.srf_insert_into_database(content)):
           return invoice_posting.respond_for_srf_freight_invoice(content)
       else:
           print(content)
           return 500

#Payment v2 Invoice Posting => POST
#In Client Configuration under erp_configuration this server's ip (a.k.a endpoint) and resource location (i.e path) should be configured
#This server listens for the API POST request and insert the response to db_pando_testing database
@app.route('/strategy_1_invoice_posting', methods=['POST'])
def strategy_1_invoice_posting():
    if request.method == 'POST':
       content = request.json
       invoice_posting.strategy_1_insert_into_database(content)
       response = invoice_posting.respond_for_strategy_1_freight_invoice(content)
       return (response, 200)

#Invoice Posting => POST
#In Client Configuration under erp_configuration this server's ip (a.k.a endpoint) and resource location (i.e path) should be configured
#This server listens for the API POST request and insert the response to db_pando_testing database
@app.route('/strategy_2_invoice_posting', methods=['POST'])
def strategy_2_invoice_posting():
    if request.method == 'POST':
       content = request.json
       invoice_posting.strategy_2_insert_into_database(content)
       return invoice_posting.respond_for_strategy_2_freight_invoice(content)

#Nestle Trace and Trace Vehicle Location by GPS
#This server listens for the API POST request and responds with Lat Long of the vehicle
@app.route('/api/v1/analytics/live/byNumber/<vehicle_name>', methods=['GET','POST','PUT'])
def gps_track_vehicle(vehicle_name):
    return track_n_trace.get_vehicle_location_using_gps(str(vehicle_name))

@app.route('/api/v1/login', methods=['POST'])
def gps_track_login():
    if request.method == 'POST':
        content = request.json
        print(content)
        return ("Login Success",200)

#CPI freight invoice=> POST
#In Client Configuration under erp_configuration this server's ip (a.k.a endpoint) and resource location (i.e path) should be configured
#This server listens for the API POST request and insert the response to db_pando_testing database.
#Also respond back with required json content for mocking CPI freight invoice
@app.route('/cpi_freight_invoice', methods=['POST'])
def cpi_freight_invoice_posting():
    if request.method == 'POST':
       content = request.json
       invoice_posting.cpi_freight_invoice_insert_into_database(content)
       return invoice_posting.respond_for_cpi_freight_invoice(content)

#Payment v1 Invoice Posting => POST
#In Client Configuration under erp_configuration this server's ip (a.k.a endpoint) and resource location (i.e path) should be configured
#This server listens for the API POST request and insert the response to db_pando_testing database
@app.route('/v1_invoice_posting', methods=['POST'])
def pay_v1_invoice_posting():
    if request.method == 'POST':
       content = request.json
       invoice_posting.pay_v1_insert_into_database(content)
       return ""

#TCP Payment v1 Invoice Posting => POST
#In Client Configuration under erp_configuration this server's ip (a.k.a endpoint) and resource location (i.e path) should be configured
#This server listens for the API POST request and insert the response to db_pando_testing database
@app.route('/tcp_invoice_posting', methods=['POST'])
def tcp_invoice_posting():
    if request.method == 'POST':
       content = request.form.to_dict()
       print('freight_posting - ',content)
       invoice_posting.tcp_insert_into_database(content)
       return ""

#This is ZPOD flow to SAP via POST
@app.route('/pod_flow_sap_endpoint', methods=['POST'])
def pod_flow_to_sap():
    if request.method == 'POST':
       content = request.json
       pod_to_sap.pod_sap_flow_insert_to_db(content)
       return ""

#This is ZPOD flow to SAP via POST
@app.route('/epod_rejection', methods=['POST'])
def epod_rejection_flow():
    if request.method == 'POST':
       content = request.json
       epod_rejection.epod_rejection_flow_insert_to_db(content)
       return ""

#This is ZPOD flow to SAP via POST
@app.route('/Rating_agg', methods=['POST'])
def get_transporter_scoring():
    if request.method == 'POST':
        content = request.json
        return transporter_score.get_transporter_score(content)

#In Client Configuration under erp_configuration this server's ip (a.k.a endpoint) and resource location (i.e path) should be configured
#This server listens for the API POST request and insert the response to db_pando_testing database
@app.route('/srf_freight_provision', methods=['POST'])
def invoice_freight_provisioning():
    if request.method == 'POST':
       content = request.json
       freight_provisioning.srf_insert_into_database(content)
       return ""

#In Client Configuration under erp_configuration this server's ip (a.k.a endpoint) and resource location (i.e path) should be configured
#This server listens for the API POST request and insert the response to db_pando_testing database
@app.route('/oel_freight_provision', methods=['POST'])
def oel_invoice_freight_provisioning():
    if request.method == 'POST':
       content = request.json
       freight_provisioning.oel_insert_into_database(content)
       response = freight_provisioning.respond_for_oel_freight_provision(content)
       return (response, 200)

#In Client Configuration under erp_configuration this server's ip (a.k.a endpoint) and resource location (i.e path) should be configured
#This server listens for the API POST request and insert the response to db_pando_testing database
@app.route('/pg_freight_provision', methods=['POST'])
def pg_freight_provision():
    if request.method == 'POST':
       content = request.json
       freight_provisioning.pg_insert_into_database(content)
       #response = freight_provisioning.respond_for_oel_freight_provision(content)
       return ('success', 200)

#In Client Configuration under erp_configuration this server's ip (a.k.a endpoint) and resource location (i.e path) should be configured
#This server listens for the API POST request and insert the response to db_pando_testing database
@app.route('/pg_freight_bill_posting', methods=['POST'])
def pg_freight_bill_posting():
    if request.method == 'POST':
       content = request.json
       print('pg_freight_bill_posting - ',content)
       #freight_provisioning.tcp_insert_into_database(content)
       freight_bill_posting.pg_insert_into_database(content)
       return ('success', 200)

#In Client Configuration under erp_configuration this server's ip (a.k.a endpoint) and resource location (i.e path) should be configured
#This server listens for the API POST request and insert the response to db_pando_testing database
@app.route('/tcpmodifiedpicklist', methods=['POST'])
def tcp_modified_picklist():
    content = request.form.to_dict()
    print(content)
    return modifiedpicklist.tcp_insert_into_database(str(content).replace('{','').replace('}','').replace('\'','').replace('<?xml version: "1.0"','<?xml version="1.0"').replace('\\n',''))

@app.route('/jsonmodifiedpicklistresponse', methods=['POST'])
def json_modified_picklist():
    return modifiedpicklist.response_jsonmodifiedpicklistresponse();

@app.route('/xmlmodifiedpicklistresponse', methods=['POST'])
def xml_modified_picklist():
    return modifiedpicklist.response_xmlmodifiedpicklistresponse();

@app.route('/alive', methods=['GET'])
def is_alive():
    return "Yes, Up and Running !!!";

@app.route('/erp', methods=['GET','POST','PUT'])
def erp():
    return ('success', 200)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return ('Undefined path: %s' % path, 200)

#In Client Configuration under erp_configuration this server's ip (a.k.a endpoint) and resource location (i.e path) should be configured
#This server listens for the API POST request and insert the response to db_pando_testing database
@app.route('/shipmentacknowledgement', methods=['POST'])
def pg_freight_provision_shipmentacknowledgement():
    if request.method == 'POST':
       content = request.json
       #freight_provisioning.pg_insert_into_database(content)
       #response = freight_provisioning.respond_for_oel_freight_provision(content)
       return ('success', 200)

#courier integration => Delete 
# @app.route('/api/booking/cancel', methods=['DELETE'])
#def booking_delete():
#    if request.method == 'DELETE':
#       content = request.json
#       return courier.booking_pod_delete(content)

@app.before_request
def before_request():
    if True:
        print ("HEADERS", request.headers)
        print ("REQ_path", request.path)
        print ("ARGS",request.args)
        print ("DATA",request.data)
        print ("FORM",request.form)

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 5001)

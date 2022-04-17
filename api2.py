from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from typing import Any, Dict, AnyStr, List, Union
from starlette.responses import RedirectResponse
from modules import courier
from modules import modifiedpicklist
from modules import deliverypicklist
from modules import freight_provisioning
from modules import pod_to_sap
from modules import epod_rejection
from modules import freight_bill_posting
from modules import invoice_posting
from modules import transporter_score
from modules import track_n_trace
import json
import uvicorn
from simplexml import dumps, loads

app = FastAPI()

JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]

@app.get("/")
async def welcome_page():
    content = RedirectResponse(url='/docs')
    return content

@app.get('/api/optima/request_picklist/5e13140fadd4bd0ea3b88400/1', tags=["DeliveryPicklist"])
async def request_picklist(request: Request):
    return PlainTextResponse('',204)

@app.post('/deliverypicklistrequest', tags=["DeliveryPicklist"])
async def delivery_picklist(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    return PlainTextResponse('',deliverypicklist.send_delivery_picklist(content))

@app.post('/modifiedpicklist', tags=["ModifiedPicklist"])
async def modified_picklist(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    return PlainTextResponse(modifiedpicklist.insert_into_database(content))

@app.post('/modifiedpicklistdelay', tags=["ModifiedPicklist"])
async def modified_picklist_delay_response(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    return PlainTextResponse(modifiedpicklist.delay_in_responding_modified_picklist(content))

@app.post('/oelmodifiedpicklist', tags=["ModifiedPicklist"])
async def oel_modified_picklist(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    modifiedpicklist.insert_into_database(content)
    return PlainTextResponse(modifiedpicklist.respond_back_for_the_request(content))

@app.post('/modifiedpicklistwithresponse', tags=["ModifiedPicklist"])
async def modified_picklist_with_response(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    modifiedpicklist.insert_into_database(content)
    response = modifiedpicklist.respond_back_for_the_request_with_retry(content)
    modifiedpicklist.insert_response_into_database(response)
    return PlainTextResponse(response,200)

@app.post('/tcpmodifiedpicklist', tags=["ModifiedPicklist"])
async def tcp_modified_picklist(request: Request):
    content = await request.body()
    dict_data = loads(content)
    return modifiedpicklist.tcp_insert_into_database(str(dict_data).replace('\'','"').replace('\\n','').replace('\\t',''))

@app.post('/jsonmodifiedpicklistresponse', tags=["ModifiedPicklist"])
async def json_modified_picklist(request: Request, jsonstructure : JSONStructure = None):
    return modifiedpicklist.response_jsonmodifiedpicklistresponse();

@app.post('/xmlmodifiedpicklistresponse', tags=["ModifiedPicklist"])
async def xml_modified_picklist(request: Request, jsonstructure : JSONStructure = None):
    return modifiedpicklist.response_xmlmodifiedpicklistresponse();

@app.post('/srf_freight_provision', tags=["FreightProvision"])
async def invoice_freight_provisioning(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    freight_provisioning.srf_insert_into_database(content)
    return PlainTextResponse("",200)

@app.post('/oel_freight_provision', tags=["FreightProvision"])
async def oel_invoice_freight_provisioning(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    freight_provisioning.oel_insert_into_database(content)
    response = freight_provisioning.respond_for_oel_freight_provision(content)
    return PlainTextResponse(response, 200)

@app.post('/pg_freight_provision', tags=["FreightProvision"])
async def pg_freight_provision(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    freight_provisioning.pg_insert_into_database(content)
    return PlainTextResponse("", 200)

@app.post('/srf_invoice_posting', tags=["InvoicePosting"])
async def srf_invoice_posting(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    if(invoice_posting.srf_insert_into_database(content)):
        return PlainTextResponse(invoice_posting.respond_for_srf_freight_invoice(content))
    else:
        print(content)
        return 500

@app.post('/strategy_1_invoice_posting', tags=["InvoicePosting"])
async def strategy_1_invoice_posting(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    invoice_posting.strategy_1_insert_into_database(content)
    response = invoice_posting.respond_for_strategy_1_freight_invoice(content)
    return PlainTextResponse(response, 200)

@app.post('/strategy_2_invoice_posting', tags=["InvoicePosting"])
async def strategy_2_invoice_posting(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    invoice_posting.strategy_2_insert_into_database(content)
    response = invoice_posting.respond_for_strategy_2_freight_invoice(content)
    return PlainTextResponse(response, 200)

@app.post('/cpi_freight_invoice', tags=["InvoicePosting"])
async def cpi_freight_invoice_posting(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    invoice_posting.cpi_freight_invoice_insert_into_database(content)
    return PlainTextResponse(invoice_posting.respond_for_cpi_freight_invoice(content))

@app.post('/v1_invoice_posting', tags=["InvoicePosting"])
async def pay_v1_invoice_posting(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    invoice_posting.pay_v1_insert_into_database(content)
    return PlainTextResponse("",200)

@app.post('/tcp_invoice_posting', tags=["InvoicePosting"])
async def tcp_invoice_posting(request: Request):
    #content = await request.json()
    content = await request.form.to_dict()
    #print('freight_posting - ',content)
    invoice_posting.tcp_insert_into_database(content)
    return PlainTextResponse("",200)

@app.post('/pod_flow_sap_endpoint', tags=["POD"])
async def pod_flow_to_sap(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    pod_to_sap.pod_sap_flow_insert_to_db(content)
    return PlainTextResponse("",200)

@app.post('/pg_freight_bill_posting', tags=["FreightBillPosting"])
async def pg_freight_bill_posting(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    freight_bill_posting.pg_insert_into_database(content)
    return ('success', 200)

@app.post('/epod_rejection', tags=["POD"])
async def epod_rejection_flow(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    epod_rejection.epod_rejection_flow_insert_to_db(content)
    return PlainTextResponse("",200)

@app.post('/shipmentacknowledgement', tags=["Shipment"])
async def pg_freight_provision_shipmentacknowledgement(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    return ('success', 200)

@app.post('/Rating_agg', tags=["TransporterRating"])
async def get_transporter_scoring(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    return transporter_score.get_transporter_score(content)

##################################TRACKINGGPS################################################

@app.api_route('/api/v1/analytics/live/byNumber/{vehicle_name}', methods=["GET","POST","PUT"], tags=["TrackingGPS"])
async def gps_track_vehicle_post(vehicle_name,request: Request):
    return PlainTextResponse(track_n_trace.get_vehicle_location_using_gps(str(vehicle_name)))

@app.post('/api/v1/login', tags=["TrackingGPS"])
async def gps_track_login(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    return PlainTextResponse("Login Success",200)

#############################################################################################

##################################COURIER####################################################

@app.post('/api/spoton/booking/create', tags=["Courier"])
async def spoton_create_booking(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    return PlainTextResponse(courier.create_spoton_booking(content))

@app.post('/api/spoton/booking/update', tags=["Courier"])
async def spoton_update_booking(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    return PlainTextResponse(courier.update_spoton_booking(content))

@app.post('/api/spoton/booking/cancel', tags=["Courier"])
async def spoton_cancel_booking(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    return PlainTextResponse(courier.cancel_spoton_booking(content))

@app.post('/api/spoton/booking/track', tags=["Courier"])
async def spoton_cancel_booking(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    return PlainTextResponse(courier.track_spoton_booking(content))

@app.post('/api/spoton/booking/get_pod', tags=["Courier"])
async def spoton_get_pod_booking(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    return PlainTextResponse(courier.track_get_pod_booking(content))

@app.post('/api/rivigo/oauth/token', tags=["Courier"])
async def Rivigo_authorization(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    return PlainTextResponse(courier.authorize(content), 200)

@app.post('/api/rivigo/booking/create', tags=["Courier"])
async def Rivigo_create_booking(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    return PlainTextResponse(courier.authorize(content), 200)

@app.post('/api/booking/create', tags=["Courier"])
async def create_booking(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    return PlainTextResponse(courier.create_booking(content))

@app.put('/api/booking/{booking_id}/materials', tags=["Courier"])
async def update_material(booking_id, request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    return PlainTextResponse(courier.update_booking(booking_id, content))

@app.post('/api/booking/track',tags=["Courier"])
async def booking_track(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    return PlainTextResponse(courier.booking_track(content))

@app.post('/api/v3/track',tags=["Courier"])
async def v3_booking_track(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    return PlainTextResponse(courier.booking_track(content))

@app.post('/api/booking/pod',tags=["Courier"])
async def booking_pod(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    return PlainTextResponse(courier.booking_pod(content))

@app.put('/api/booking/{booking_id}/vrdate',tags=["Courier"])
async def booking_vechicle_req_date(booking_id, request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    return PlainTextResponse(courier.booking_vech_req_date(booking_id,content))

@app.post('/api/safexepress/auto/token',tags=["Courier-SafeExpress"])
async def safe_express_token_generation(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    return PlainTextResponse(courier.authorize_safeexpress(content), 200)

@app.post('/api/safexepress/portal/ViewPod',tags=["Courier-SafeExpress"])
async def safe_express_view_pod(wayblNo : int = 0):
    return PlainTextResponse(courier.view_pod_safeexpress(wayblNo), 200)

@app.post('/api/booking/createSafeex',tags=["Courier"])
async def create_booking_safeex(request: Request, jsonstructure : JSONStructure = None):
    content = await request.json()
    return PlainTextResponse(courier.create_safeexp_booking(content))

#############################################################################################
@app.get('/read_log')
async def read_file():
    file = open("catch_all.txt", "r")
    return file.read()

@app.api_route("/{path_name:path}", methods=["GET","POST","PUT","PATCH","DELETE"])
async def catch_all(request: Request, path_name: str, jsonstructure : JSONStructure = None):
    file = open("catch_all.txt", "a")
    file.write("request_method : "+ request.method+"\n")
    file.write("path_name : " + path_name+"\n")
    file.write("request : " + json.dumps(await request.json()) + "\n")
    file.write("-------------------------------------------------->" + "\n")
    return {"request_method": request.method, "path_name": path_name}

if __name__ == "__main__":
    uvicorn.run("api2:app",host='0.0.0.0', port=5001, workers=1) #Keep the worker as 1. It tends to fail in retry requests

import json
import random

#Create Courier
def authorize(content):
    #print(content)
    with open('response/courier_authorization.json') as f:
        data = json.load(f)
        response = json.dumps(data)
    return response

def authorize_safeexpress(content):
    with open('response/courier_safeexpress_authorization.json') as f:
        data = json.load(f)
        response = json.dumps(data)
    return response

def view_pod_safeexpress(wayblNo):
    with open('response/courier_safeexpress_view_pod.json') as f:
        data = json.load(f)
        data['WAYBL_NO'] = wayblNo
        response = json.dumps(data)
    return response

def create_spoton_booking(content):
    order_id = content['ReferenceNumber']
    pandoConsigneeId = content['ReceiverName']
    pandoGateId = content['PickupLocationName']
    bookingId = str(random.randint(80000, 90000))
    cnote = str(random.randint(6000000000, 7000000000))

    with open('response/spoton_booking_create_response.json') as f:
        data = json.load(f)
        data['PickupOrderNo'] = bookingId
        data['CustomerRefNo'] = pandoConsigneeId
        data['PickupScCode'] = pandoGateId
        data['ConNo'] = bookingId
        data['UniqueValue'] = cnote
        response = json.dumps(data)

    return response

def update_spoton_booking(content):
    with open('response/spoton_booking_update_response.json') as f:
        data = json.load(f)
        response = json.dumps(data)

    return response

def cancel_spoton_booking(content):
    ConNo = content['ConNo']

    with open('response/spoton_booking_cancel_response.json') as f:
        data = json.load(f)
        data['ConNo'] = ConNo
        response = json.dumps(data)

    return response

def track_spoton_booking(content):

    with open('response/spoton_booking_track_response.json') as f:
        data = json.load(f)
        response = json.dumps(data)

    return response

def track_get_pod_booking(content):

    with open('response/spoton_booking_get_pod_response.json') as f:
        data = json.load(f)
        response = json.dumps(data)

    return response

#Create Courier
def create_booking(content):

    order_id = content['order_id']
    pandoConsigneeId = content['consignee']['id']
    pandoGateId = content['pickup']['id']
    bookingId = str(random.randint(80000, 90000))
    cnote = str(random.randint(6000000000, 7000000000))

    with open('response/booking_create_response.json') as f:
        data = json.load(f)
        data['order_id'] = order_id
        data['pandoConsigneeId'] = pandoConsigneeId
        data['pandoGateId'] = pandoGateId
        data['bookingId'] = bookingId
        data['cnote'] = cnote
        response = json.dumps(data)

    return response

#update Courier
def update_booking(bid,content):
    order_id = content['order_id']
    cnote = content['cnote']

    with open('response/booking_update.json') as f:
        data = json.load(f)
        data['order_id'] = order_id
        data['bookingId'] = bid
        data['cnote'] = cnote
        response = json.dumps(data)

    return response

#Book Tracking Courier
def booking_track(content):

    transporter_id = content['transporter_id']
    bookingId = content['bookingId']
    cnote = content['cnote']

    with open('response/booking_create_track.json') as f:
        data = json.load(f)
        data['bookingId'] = bookingId
        response = json.dumps(data)

    return response

#Book Epod Courier
def booking_pod(content):

    bookingId = content['bookingId']

    with open('response/booking_pod.json') as f:
        data = json.load(f)
        data['bookingId'] = bookingId
        response = json.dumps(data)

    return response

#Book Req date
def booking_vech_req_date(bid,content):

    with open('response/booking_vech_req_date.json') as f:
        data = json.load(f)
        data['order_id'] = content['order_id']
        data['bookingId'] = bid
        data['cnote'] = content['cnote']
        response = json.dumps(data)

    return response

#Book Delete MethodViewType
def booking_pod_delete(content):

    with open('response/booking_delete.json') as f:
        data = json.load(f)
        data['order_id'] = content['order_id']
        data['bookingId'] = content['booking_id']
        response = json.dumps(data)

    return response

#create_booking_safe_express
def create_safeexp_booking(content):
    SFXRefId = str(random.randint(2000, 9000))
    sfx_waybl_no = content['SFX_WAYBL_NO']

    with open('response/create_booking_safeex_response.json') as f:
        data = json.load(f)
        print(data)
        data[0]['SFX_WAYBL_NO'] = sfx_waybl_no
        data[0]['SFXRefId'] = SFXRefId
        response = json.dumps(data)

    return response




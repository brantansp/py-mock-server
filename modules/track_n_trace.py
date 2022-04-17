import json
import random
import datetime

location_counter = 0
vehicle_location_counter = {}

"""
#This mocks the Vehicle GPS location to N number of items in the random_lat_long list
#This keeps counter of each unique vehicle number in request. i.e for first ping of Vehicle v1 - 1st location will be responded and
so on so forth for N items in the random_lat_long list.
#If vehicle has 'x' in suffix then it will return empty response 
"""
def get_vehicle_location_using_gps(vehicle_name):

    dt = datetime.datetime.now()
    date_time = dt.strftime("%Y-%m-%d %H:%M:%S")

    if (vehicle_name[-1]).lower() == 'x':
        return ''
    else:
        #random_lat_long = ["13.1143|80.1548|Pataravakkam Main Road, Chennai, Tamil Nadu, 600053 Ambattur Chennai India","13.1143|80.1548|Pataravakkam Main Road, Chennai, Tamil Nadu, 600053 Ambattur Chennai India", "13.0841|79.6704|Kanchipuram Main Road, Arakkonam, Tamil Nadu, 631001 Arakkonam India","12.9165|79.1325|Anna Salai Road, Vellore Vellore Fort Area, Tamil Nadu, 632004 Vellore Fort Area Vellore India"]
        random_lat_long = ["13.1143|80.1548|Pataravakkam Main Road, Chennai, Tamil Nadu, 600053 Ambattur Chennai India|7195.95|0.0",
                           "13.1143|80.1548|Pataravakkam Main Road, Chennai, Tamil Nadu, 600053 Ambattur Chennai India|7195.95|70.0",
                           "13.0841|79.6704|Kanchipuram Main Road, Arakkonam, Tamil Nadu, 631001 Arakkonam India|7263|80.0",
                           "12.9165|79.1325|Anna Salai Road, Vellore Vellore Fort Area, Tamil Nadu, 632004 Vellore Fort Area Vellore India|7334|74.5",
                           "13.1143|80.1548|Pataravakkam Main Road, Chennai, Tamil Nadu, 600053 Ambattur Chennai India|7464|0.0"]
        global location_counter
        global vehicle_location_counter
        lat_long =''

        if vehicle_name in vehicle_location_counter.keys():
            vehicle_location_counter[vehicle_name] = vehicle_location_counter[vehicle_name] + 1
        else:
            vehicle_location_counter[vehicle_name] = 0

        if vehicle_location_counter[vehicle_name] >= len(random_lat_long):
            vehicle_location_counter.pop(vehicle_name)
            return ''
        else:
            lat_long = random_lat_long[vehicle_location_counter[vehicle_name]]

        with open('response/fleetx_vehicle_gps_location.json') as f:
            data = json.load(f)
            data['vehicleNumber'] = vehicle_name
            value = lat_long.split('|')
            data['latitude'] = float(value[0])
            data['longitude'] = float(value[1])
            data['lastUpdatedAt'] = date_time
            data['lastStatusTime'] = date_time
            data['lastAccOn'] = date_time
            data['address'] = value[2]
            data['totalOdometer'] = value[3]
            data['speed'] = value[4]
            response = json.dumps(data)
        #print(response)
        return response
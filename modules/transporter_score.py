import json
import random
import datetime
from flask import jsonify

def get_transporter_score(content):
    print(content)
    transporters = content["data"]["transporterId"]
    client_id  = content["data"]["clientId"]

    transporter_scoring = {"604f24b2e61cab2b8969c47c":"{\"baseFreight\":30595.01,\"clientId\":\""+client_id+"\",\"confidenceScore\":0.78,\"customer\":\"Orient Electric Ltd\",\"damageFreeShipmentRating\":5.0,\"deliveryRating\":3.35,\"movementType\":\"Secondary\",\"placementRating\":3.17,\"totalIndentCount\":47,\"totalRating\":0.0,\"transporter\":\"Safe Speed Carriers Private Limited\",\"transporterId\":\"604f24b2e61cab2b8969c47c\",\"wd\":0.3333333333333333,\"wp\":0.3333333333333333,\"ws\":0.3333333333333333}",
                           "604f24b2e61cab2b8969c47f":"{\"baseFreight\":1391.3545454545454,\"clientId\":\""+client_id+"\",\"confidenceScore\":1.0,\"customer\":\"Orient Electric Ltd\",\"damageFreeShipmentRating\":5.0,\"deliveryRating\":4.0,\"movementType\":\"Secondary\",\"placementRating\":3.43,\"totalIndentCount\":1599,\"totalRating\":-1,\"transporter\":\"Meesan Logistics Pvt. Ltd.\",\"transporterId\":\"604f24b2e61cab2b8969c47f\",\"wd\":0.3333333333333333,\"wp\":0.3333333333333333,\"ws\":0.3333333333333333}",
                           "604f24b2e61cab2b8969c47e":"{\"baseFreight\":31513.085365853654,\"clientId\":\""+client_id+"\",\"confidenceScore\":0.94,\"customer\":\"Orient Electric Ltd\",\"damageFreeShipmentRating\":5.0,\"deliveryRating\":3.4,\"movementType\":\"Secondary\",\"placementRating\":3.95,\"totalIndentCount\":192,\"totalRating\":2.0,\"transporter\":\"TCM Total Logistics Solutions LLP\",\"transporterId\":\"604f24b2e61cab2b8969c47e\",\"wd\":0.3333333333333333,\"wp\":0.3333333333333333,\"ws\":0.3333333333333333}",
                           "604f24b2e61cab2b8969c480":"{\"baseFreight\":5138.96,\"clientId\":\""+client_id+"\",\"confidenceScore\":0.97,\"customer\":\"Orient Electric Ltd\",\"damageFreeShipmentRating\":5.0,\"deliveryRating\":2.1,\"movementType\":\"Secondary\",\"placementRating\":2.86,\"totalIndentCount\":32,\"totalRating\":-1.0,\"transporter\":\"RIVIGO Services Private Limited\",\"transporterId\":\"604f24b2e61cab2b8969c480\",\"wd\":0.3333333333333333,\"wp\":0.3333333333333333,\"ws\":0.3333333333333333}",
                           "6140afc859f8de004b7f2a31":"{\"baseFreight\":5138.96,\"clientId\":\""+client_id+"\",\"confidenceScore\":0.97,\"customer\":\"Orient Electric Ltd\",\"damageFreeShipmentRating\":5.0,\"deliveryRating\":2.1,\"movementType\":\"Secondary\",\"placementRating\":3.5,\"totalIndentCount\":32,\"totalRating\":-1.0,\"transporter\":\"Highway Logistics\",\"transporterId\":\"6140afc859f8de004b7f2a31\",\"wd\":0.3333333333333333,\"wp\":0.3333333333333333,\"ws\":0.3333333333333333}",
                           "6140b01298ceb00049eae3fc":"{\"baseFreight\":5138.96,\"clientId\":\""+client_id+"\",\"confidenceScore\":0.97,\"customer\":\"Orient Electric Ltd\",\"damageFreeShipmentRating\":5.0,\"deliveryRating\":2.1,\"movementType\":\"Secondary\",\"placementRating\":4.8,\"totalIndentCount\":32,\"totalRating\":-1.0,\"transporter\":\"MSS Transporters\",\"transporterId\":\"6140b01298ceb00049eae3fc\",\"wd\":0.3333333333333333,\"wp\":0.3333333333333333,\"ws\":0.3333333333333333}",
                           "604f24b2e61cab2b8969c47d":"{\"baseFreight\":35.0,\"clientId\":\""+client_id+"\",\"confidenceScore\":1.0,\"customer\":\"Orient Electric Ltd\",\"damageFreeShipmentRating\":5.0,\"deliveryRating\":4.7,\"movementType\":\"Secondary\",\"placementRating\":3.61,\"totalIndentCount\":49,\"totalRating\":3.0,\"transporter\":\"Shri Ram Transport Service\",\"transporterId\":\"604f24b2e61cab2b8969c47d\",\"wd\":0.3333333333333333,\"wp\":0.3333333333333333,\"ws\":0.3333333333333333}"}
    scoring_result = []

    transporters = transporters.replace("[", "").replace("]", "").replace("'", "").strip().split(",")

    for item in transporters:
        transporter = item.strip()
        try:
            scoring_result.append(json.loads(transporter_scoring[transporter]))
        except Exception as e:
            print(e)
    print(scoring_result)
    return scoring_result

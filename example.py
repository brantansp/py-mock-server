import json

with open('response/rivago_epod_response.json') as f:
  data = json.load(f)
  del data['individualTrackingList']
  response = json.dumps(data)

  print(response)

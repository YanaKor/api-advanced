import pprint

import requests

# url = 'http://5.63.153.31:5051/v1/account'
# headers = {
#     'accept': '*/*',
#     'Content-Type': 'application/json'
# }
# json = {
#     "login": "yakor_test1",
#     "email": "yakor_test1@maol.ru",
#     "password": "25465476584"
# }

# response = requests.post(url, json=json, headers=headers)


url = 'http://5.63.153.31:5051/v1/account/69abf383-ac37-405d-9c75-d236687882db'

headers = {
    'accept': 'text/plain'
}

response = requests.put(url=url, headers=headers)

print(response.status_code)
pprint.pprint(response.json())

response_json = response.json()
print(response_json['resource']['rating']['quantity'])

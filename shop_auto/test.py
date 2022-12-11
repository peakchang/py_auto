import requests
import json
import urllib3

# webhook_url = "https://testkosiwn.shop/test/"
webhook_url = "http://ts-phone.com/test/receive_wh.php"

data = {'testval' : 'test1111111'}


requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
r = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type' : 'application/json'}, verify=False)
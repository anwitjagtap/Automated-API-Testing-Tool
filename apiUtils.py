import time
import requests
import json
import urllib.parse

def is_encoded(value):
    decoded_value = urllib.parse.unquote(value)
    return value != decoded_value


def callAPI(method,host,url,headers,payload={}, params = {}):
    headers['user-agent'] ='automation_anwit_jagtap'
    print(f"call api  : headers {headers}")

    params = {key: urllib.parse.unquote(val) if is_encoded(val) else val for key, val in params.items()}

    if payload != {}:
        payload = json.dumps(payload)
    response = requests.request(method, host+url, headers=headers, data=payload, params = params)
    return response 

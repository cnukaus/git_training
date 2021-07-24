import requests
import json
import ipfshttpclient
import os

def upload():
    try:
        client = ipfshttpclient.connect()# Connects to: /dns/localhost/tcp/5001/http
        
        print(client)
        upload_file=os.path.join('upload','ok.txt')
        res = client.add(upload_file)

    except ipfshttpclient.exceptions.ConnectionError as ce:
        print('OK',str(ce))
    
    upload_file=os.path.join('upload','ok.txt')
    res = client.add(upload_file)
    pass

if __name__ == '__main__':

    connect_addr='ipfs.infura.io'
    port=5001




params = (
(‘arg’, ‘QmeY7x2rEzyUxh2uwhXMqgBnPvcxzgNcQcUQWJG94Hv9ki’),
)
response = requests.post('https://ipfs.infura.io:5001/api/v0/pin/add', params=params, auth=(<project_id>,<project_secret>))
print(response.json())

    file_json = {
        'fileOne': ('Congrats! This is the first sentence'),
    }

    response = requests.post('https://ipfs.infura.io:5001/api/v0/add', files=file_json)
    p = response.json()
    hash = p['Hash']
    print(hash)

    # retreive
    params = (
        ('arg', hash),
    )
    response_two = requests.post('https://ipfs.infura.io:5001/api/v0/block/get', params=params)
    print(response_two.text)
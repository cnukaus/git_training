#-*- coding: utf-8 -*-
import requests
import time
import hashlib
import base64
import json
#from urllib import parse

URL = "http://webapi.xfyun.cn/v1/service/v1/ocr/invoice"
APPID = ""
API_KEY = ""
def getHeader():
    curTime = str(int(time.time()))
    param = {"engine_type": "invoice"}
    param = json.dumps(param)
    #x_param = base64.b64encode(param.encode('utf-8'))
    #param = "{\"auto_rotate\":\"true\"}"
    paramBase64 = base64.b64encode(param.encode('utf-8'))

    m2 = hashlib.md5()
    str1 = API_KEY + curTime + str(paramBase64,'utf-8')
    m2.update(str1.encode('utf-8'))
    checkSum = m2.hexdigest()

    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    return header

with open(r'', 'rb') as f:
    f1 = f.read()

f1_base64 = str(base64.b64encode(f1), 'utf-8')

    
data = {
        'image': f1_base64
        }

#headers=getHeader(language, location)
r = requests.post(URL, data=data, headers=getHeader())
result = str(r.content, 'utf-8')
print(result)
input("Entry the any key to exit")

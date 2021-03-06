import requests

from json import loads
from base64 import b64decode
import re
import time
import pymongo
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from w3lib.html import remove_tags
from langdetect import detect
from bson import ObjectId
import datetime
import sys

url = 'https://simpleapi.info/apps/numbers-info/info.php'
url_web = 'https://simpleapi.info/apps/numbers-info/web'
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; RedMi Note 5 Build/RB3N5C; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36'}
session = requests.Session()

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Number"]
phonedb = mydb["599"]

for i in range(514000000, 599999999):
    try:
        def get_key():
            response = session.get(url_web, headers=headers).text
            func_name = response.split('window.atob(')[1].split('.substr')[0]
            token_tmp_encoded = response.split(func_name + ' = \'')[1].split('\';')[0]
            substr_numbs = [eval(x) for x in response.split('window.atob(' + func_name + '.substr(')[1].split(')));')[0].split(',')]
            token_tmp_decoded = b64decode(token_tmp_encoded + '==').decode('utf-8')

            if 'window.atob' in token_tmp_decoded:
                return b64decode(token_tmp_decoded.split('window.atob(\'')[1].split('\')')[0]+"=").decode('utf-8')
            else:
                return False


        def get_info(number):

            while 1!=0:
                key = get_key()
                if key:
                    break

            data = {
                'key': key,
                'number': str(number),
                'u_id': '',
                'u_token': ''
            }

            response = session.post(url, data=data, headers=headers)
            if 'yes' in response.text:
                data = loads(response.text.encode('utf-8'))
                return data


        if __name__ == '__main__':
            # For example

            data = get_info(i)
            print(data)
            print(i)
            phonedb.insert(data)
    except Exception as e:
        print(e)

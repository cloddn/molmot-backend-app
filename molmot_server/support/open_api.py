import requests
import pprint
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import json

#인증키 입력
encoding = 'PysG3pgnXQC5fqwh4L4Ql6Wp0bk0tqi3z%2B30fovf36Nttuvc809IfYDw9Cq6qEMyJpJ0PE20ULdcaA9IuSn2Mw%3D%3D'
decoding = 'PysG3pgnXQC5fqwh4L4Ql6Wp0bk0tqi3z+30fovf36Nttuvc809IfYDw9Cq6qEMyJpJ0PE20ULdcaA9IuSn2Mw=='

#url 입력
url = 'https://api.odcloud.kr/api/15028252/v1/uddi:d25e6d10-d504-4ed3-b427-b0825ae8710d_202003201526'
params ={'serviceKey' : decoding , 
'page' : 1, 
'perPage' : 10}

queryParams = '?' + urlencode({ quote_plus('serviceKey') : encoding, quote_plus('pageNo') : '1', quote_plus('numOfRows') : '10', quote_plus('dataType') : 'JSON', quote_plus('dataCd') : 'ASOS', quote_plus('dateCd') : 'DAY', quote_plus('startDt') : '20100101', quote_plus('endDt') : '20100601', quote_plus('stnIds') : '108' })


#response = urlopen(url + queryParams) 
get_data = requests.get(url + unquote(queryParams))
result_data = get_data.json()
json_api=json.dumps(result_data)
#json_api = result_data.read().decode("utf-8")
print(result_data)

import pandas as pd 
from pandas.io.json import json_normalize 
import json

json_file = json.loads(json_api)
print(json_file)
df=json_normalize(json_file['response']['body']['items']['item'])


### xml을 DataFrame으로 변환하기 ###
from os import name
import xml.etree.ElementTree as et
import pandas as pd
import json
import bs4
from lxml import html
from urllib.parse import urlencode, quote_plus, unquote

xml_obj = bs4.BeautifulSoup(content,'json')
rows = xml_obj.findAll('item')
print(rows)
"""
# 컬럼 값 조회용
columns = rows[0].find_all()
print(columns)
"""




# 각 행의 컬럼, 이름, 값을 가지는 리스트 만들기
row_list = [] # 행값
name_list = [] # 열이름값
value_list = [] #데이터값

# xml 안의 데이터 수집
for i in range(0, len(rows)):
    columns = rows[i].find_all()
    #첫째 행 데이터 수집
    for j in range(0,len(columns)):
        if i ==0:
            # 컬럼 이름 값 저장
            name_list.append(columns[j].name)
        # 컬럼의 각 데이터 값 저장
        value_list.append(columns[j].text)
    # 각 행의 value값 전체 저장
    row_list.append(value_list)
    # 데이터 리스트 값 초기화
    value_list=[]

#xml값 DataFrame으로 만들기
corona_df = pd.DataFrame(row_list, columns=name_list)
print(corona_df.head(19)) 

#DataFrame CSV 파일로 저장
corona_df.to_csv('corona_kr.csv', encoding='utf-8')
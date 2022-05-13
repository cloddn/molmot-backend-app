import requests
import pprint
from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import json
from bs4 import BeautifulSoup
import xmltodict

def get_youth_center(query):

    #인증키 입력
    encoding = '167693bf2984bec5368623af'
    #decoding = 'PysG3pgnXQC5fqwh4L4Ql6Wp0bk0tqi3z+30fovf36Nttuvc809IfYDw9Cq6qEMyJpJ0PE20ULdcaA9IuSn2Mw=='

    #url 입력
    url = 'https://www.youthcenter.go.kr/opi/empList.do'
    #params ={
    #'openApiVlak' : encoding , 
    #'display' : 1, 
    #'pageIndex' : 1}

    queryParams = '?' +  urlencode({ 
        quote_plus('openApiVlak') : encoding, 
        quote_plus('display') : 1, 
        quote_plus('pageIndex') : 3,
        quote_plus('bizTycdSel') : "004001",
        quote_plus('query') : "청년 대전",
        })

    queryParams_request="?"+urlencode(query)


    #response = urlopen(url + queryParams) 
    get_data = requests.get(url+ queryParams_request)
    soup=BeautifulSoup(get_data.content,"xml")
    dict_type = xmltodict.parse(get_data.content)
    json_type = json.dumps(dict_type)
    dict2_type = json.loads(json_type)

    return dict2_type
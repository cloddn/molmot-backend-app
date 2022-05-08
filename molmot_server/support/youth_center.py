from time import sleep
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URL = f"https://www.youthcenter.go.kr/youngPlcyUnif/youngPlcyUnifList.do"
def get_today_info() :
    website = requests.get(URL)
    soup = BeautifulSoup(website.text,"html.parser")
   

    chrome_options = Options()
    chrome_options.add_argument( '--headless' )
    chrome_options.add_argument( '--log-level=3' )
    chrome_options.add_argument( '--disable-logging' )
    chrome_options.add_argument( '--no-sandbox' )
    chrome_options.add_argument( '--disable-gpu' )
    
    driver = webdriver.Chrome('/Users/heejeong/gitkraken/molmot-backend-app/molmot_server/chromedriver',chrome_options=chrome_options)
    driver.implicitly_wait(3)
    driver.get( URL )

    driver.execute_script("fn_move(6);")
    driver.implicitly_wait(5)
    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")
    notice=soup.find("div",class_="sch-result-wrap compare-result-list")
    notice=notice.find("div",class_="result-list-box")
    location=soup.find("div",class_="badge").get_text()
    try:
        location=soup.find("span",class_="grey-label").get_text()
    except:
        pass
    print(location)
    for i in notice.find("ul").find_all('li'):
        supports_list=i.find("a")["id"][8:]
    
        jv_script="f_Detail('"+supports_list+"');"
        print(jv_script)
        #driver.execute_script(jv_script)
        driver = webdriver.Chrome('/Users/heejeong/gitkraken/molmot-backend-app/molmot_server/chromedriver',chrome_options=chrome_options)
        driver.implicitly_wait(3)
        #driver.get('http://www.google.com/xhtml');
        #driver = webdriver.Chrome( ChromeDriverManager().install(),chrome_options=chrome_options )
        driver.get( URL )
        driver.execute_script(jv_script)
        driver.implicitly_wait(5)
        sleep(3)
        html = driver.page_source
        soup = BeautifulSoup(html,"html.parser")
        #print(soup.find("div",class_="content"))
        notice_detail=soup.find("div",class_="content").get_text()
        title=soup.find("div",class_="plcy-left").get_text()

        detail=soup.find("h4",class_="bullet-arrow1").get_text()
        info_list=soup.find("div",class_="view-txt").find_all("div")
        #for i in info_list:
        #    print(i.text.strip())
        print(title.strip())
        print(detail.strip())
        break
    

    
    #driver.execute_script("f_Detail('R2022012501406')")
    #html = driver.page_source
    #print(html)
    
    #for i in range(1, 10):
    #    print("Current page is {0}".format(i))
    #    driver.execute_script("f_Detail({0})".format(i))



#
# 
# #srchFrm > div.sch-result-wrap.compare-result-list//*[@id="srchFrm"]/div[4]/div[2]/ul
get_today_info()
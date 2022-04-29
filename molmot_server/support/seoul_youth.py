from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from support.models import Support


#URL = 'https://youth.seoul.go.kr/site/main/customSupp/list?targetMulti=&ageMulti=#n'
DRIVER_PATH = 'chromedriver.exe'
 
num = 1
# 청년지원정보
URL = 'https://youth.seoul.go.kr/site/main/customSupp/politicsList?cp=' + str(num) + '&pageSize=5&searchIndex=1'

chrome_options = Options()
chrome_options.add_argument( '--headless' )
chrome_options.add_argument( '--log-level=3' )
chrome_options.add_argument( '--disable-logging' )
chrome_options.add_argument( '--no-sandbox' )
chrome_options.add_argument( '--disable-gpu' )
 
driver = webdriver.Chrome( ChromeDriverManager().install(),chrome_options=chrome_options )
driver.get( URL )


#elements = driver.find_elements_by_css_selector('customSuppSearch > div > div.pop-add-wrap2 > div > div > div.W1280.service-cont1 > div:nth-child(2) > table > tbody')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
notices = soup.select('body > div')
#listWraper > div > ul:nth-child(6)

for no in soup.find("body").find("div").find("ul").find_all("li"):

    #tagName = el_title.tag_name
    #className = el_ti tle.get_attribute('class')
    
    urls="https://youth.seoul.go.kr"+no.find("a")["href"]
    driver.get( urls )

    print(no.find("a")["href"])
    html = driver.page_source
    soup_two = BeautifulSoup(html, 'html.parser')
    
    #soup_two.select("#content")
    notice=soup_two.find("div",class_="srad_view clearfix")

    #신청기간 
    notices=notice.find("li").find_all("li")
    text_list=[]
    text_list.append(notice.find("div",class_="srv_rt").find("div",class_="tits").find("p").get_text())
    for i in notice.find("ul").find_all('li'):
        try:
            
            texts=i.select_one("ul > li").text
            text_list.append(texts.strip())
            array=text_list[-1].split("\n")
            text_list[-1]=array[0]
        except:
            pass


    
    array=text_list[1].split("~")
    text_list[1]=array[0].rstrip()
    text_list.insert(2,array[1].lstrip())

    
    #Support.objects.create(title=text_list[0],start_date=text_list[1],end_date=text_list[2],qualifications=text_list[3],organizer=text_list[4],submit_link=urls)
    print(text_list)
    
    #공백 삭제하기

    #제목
    #print(notice.find("div",class_="srv_rt").find("div",class_="tits").find("p").get_text())

   # print(no.find("a")["href"])

#customSuppSearch > div > div.pop-add-wrap2 > div > div > div.W1280.service-cont1 > div:nth-child(2) > table > tbody

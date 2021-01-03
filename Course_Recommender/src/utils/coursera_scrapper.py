'''
Project - Recommendation System
Udemy Scrapping Tool
Author - Kartik Rana
'''

#modules for the program
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from src.data.mongodb_writer import mongodb_writer
from src.utils.captcha_bypasser import captcha_bypasser
from src.utils.non_ascii import non_ascii
import time

#required lists
elems=[]
link=[]
prices=[]
hours=[]
coursetype=[]
level=[]
rating=[]

'''
#headless Selenium
options = Options()
options.add_argument('--headless')
#options.add_argument('--disable-gpu')  # Last I checked this was necessary.
driver = webdriver.Chrome('C:/Users/Acer/Downloads/chromedriver', chrome_options=options)
print("Chrome Opened Succesfully")'''

def coursera_scrapper(url,search_entry):
    driver = webdriver.Chrome()
    driver.get(url)
    
    #login attempt
    login=WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div/span/div[1]/header/div[2]/div/div[1]/div/div/div[4]/div/ul/li[3]/a")))
    login=driver.find_element_by_xpath("/html/body/div[3]/div/div/span/div[1]/header/div[2]/div/div[1]/div/div/div[4]/div/ul/li[3]/a")
    login.click()
    time.sleep(2)
    email=driver.find_element_by_xpath("/html/body/div[3]/div/div/span/div[3]/div/div/div[3]/div/div/div/div[2]/div/div[1]/form/div[1]/div[1]/div/div[2]/input")
    email.send_keys("tikas54892@pidouno.com")
    password=driver.find_element_by_xpath("/html/body/div[3]/div/div/span/div[3]/div/div/div[3]/div/div/div/div[2]/div/div[1]/form/div[1]/div[2]/div/div[2]/input")
    password.send_keys("tikas54892")
    login_btn=driver.find_element_by_xpath("/html/body/div[3]/div/div/span/div[3]/div/div/div[3]/div/div/div/div[2]/div/div[1]/form/div[1]/button")
    time.sleep(2)
    login_btn.click()
    print("Login Successful")
    #time.sleep(10)
    try:
        #switching frames to captcha
        #time.sleep(10)
        driver.switch_to.default_content()
        frames=WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[8]/div[2]")))
        frames=driver.find_element_by_xpath("/html/body/div[8]/div[2]").find_elements_by_tag_name("iframe")
        driver.switch_to.frame(frames[0])
        captcha_bypasser(driver)
    except:
        print(4)
        pass
    
    #scrapping the data
    coursetype= driver.find_elements_by_class_name("color-primary-text.card-title.headline-1-text")
    for i in range(len(coursetype)):
        print(coursetype[i].text)
    level=driver.find_elements_by_class_name("difficulty")
    for i in range(len(level)):
        print(level[i].text)
    rating=driver.find_elements_by_class_name("ratings-text")
    for i in range(len(rating)):
        print(rating[i].text)
    
    #scrapping for links
    for i in range(0,10):
        elems=WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#rendered-content > div > div > div.rc-SearchPage > div.ais-InstantSearch__root > div > div.rc-SearchTabs > div.ais-MultiIndex__root > div.tab-contents > div > div > div > ul > li:nth-child("+ str(i+1) +") > div > a")))
        elems.append(driver.find_element_by_css_selector("#rendered-content > div > div > div.rc-SearchPage > div.ais-InstantSearch__root > div > div.rc-SearchTabs > div.ais-MultiIndex__root > div.tab-contents > div > div > div > ul > li:nth-child("+ str(i+1) +") > div > a"))
    for elem in elems:
        link.append(elem.get_attribute("href"))
    
    
    #scrapping for time and price from each link
    for i in link:
        print(i)
        driver.get(i)
        print("link opened successfully")
        
        #scrapping for time 
        data=driver.find_elements_by_class_name("_y1d9czk.m-b-2.p-t-1s")
        a=len(data)
        print(a)
        b=int(a/2)-2
        print(data[b].text)
        data1=data[b].text.split()
        
        #calcuting time
        if(data1[2]=='months'):
            hours.append(str(int(data1[1])*int(data1[6])*4))
        elif(data1[2]=='hours'):
            hours.append(data1[1])
        else:
            hours.append('-')
        time.sleep(10)
        
        #calcuting price
        #three different class buttons
        try:
            button=driver.find_element_by_class_name("_mkj5xnr")    
        except:
            try:
                button=driver.find_element_by_class_name("_10dw7u7r")
            except:
                button=driver.find_element_by_class_name("_1mlshhdv")
        button.click()
        print("Button Clicked")
        time.sleep(10)
        
        #three different price orientations
        try:
            price_btn=driver.find_element_by_class_name("primary.cozy.m-y-1")
            price_btn.click()
            time.sleep(5)
            price=driver.find_element_by_xpath("/html/body/div[6]/div/span/div/div[2]/div[1]/div[2]/div[2]/ul/li[3]/div/div[2]/h4/strong/span/span/span")
        except:
            try:
                price=driver.find_element_by_xpath("/html/body/div[6]/div/span/div/div[2]/div[1]/div[1]/div/ul/li[3]/div/div[2]/h4/strong/span/span/span")
            except:
                price=driver.find_element_by_xpath("/html/body/div[6]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/label/div[2]/div/h4/span/span[3]/span/span")            
        print(non_ascii(price.text))
        
        #storing prices in an array
        prices.append(non_ascii(price.text))
    print(hours)
    print(prices)
    
    
    #to open the webpage again to get the rest of the data
    #driver.get(url)
    


#inserting data in database
mongodb_writer(coursetype,level,rating,hours,prices)
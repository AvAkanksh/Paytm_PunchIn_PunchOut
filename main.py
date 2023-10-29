from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import requests
import os

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get('https://elevate.peoplestrong.com/altLogin.jsf')
username = driver.find_element(by=By.ID,value="loginForm:username12")
password = driver.find_element(by=By.ID,value="loginForm:password")
username.send_keys(os.environ["PAYTM_ELEVATE_USERNAME"])
password.send_keys(os.environ["PAYTM_ELEVATE_PASSWORD"])
submit = driver.find_element(by=By.XPATH,value='//*[@id="loginForm:loginButton"]/span')
driver.execute_script('arguments[0].click();',submit)
cookies = driver.get_cookies()
sessionToken = "" 

for cookie in cookies :
    if(cookie['name']=='SessionToken'):
        sessionToken = cookie['value'].strip('"')
        # print(sessionToken)
        break


url = 'https://onewebapi.peoplestrong.com/api/punch/v1/inout/web/punch-attendance'
headers = {
    'content-type': 'application/json; charset=utf-8',
    'platform': 'Web',
    'sessiontoken': sessionToken,  
    'timezone': 'Asia/Calcutta'
}
data = {}

response = requests.post(url, headers=headers, json=data)
response_json = response.json()
print(json.dumps(response_json, indent=4))


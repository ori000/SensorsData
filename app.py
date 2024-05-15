# from fastapi import FastAPI
# from selenium import webdriver
# import requests

# app = FastAPI()

# @app.get("/get-cookies")
# def get_cookies():
#     driver = webdriver.Chrome()
#     driver.get("https://sturegss.aub.edu.lb/StudentRegistrationSsb/ssb/term/termSelection?mode=search")
#     cookies = driver.get_cookies()
#     # driver.quit()
#     return cookies

# @app.get("/get-session-id")
# def get_session_id():
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")
#     driver = webdriver.Chrome(options=options)
#     url = "https://sturegss.aub.edu.lb/StudentRegistrationSsb/ssb/term/termSelection?mode=search"
#     driver.get(url)
#     session_storage_item = driver.execute_script(
#         "return sessionStorage.getItem('xe.unique.session.storage.id');"
#     )
#     # driver.quit()
#     return session_storage_item

# def get_modified_url(session_id: str):
#     base_url = "https://sturegss.aub.edu.lb/StudentRegistrationSsb/ssb/searchResults/searchResults"
#     params = {
#         "txt_term": "202420",
#         "startDatepicker": "",
#         "endDatepicker": "",
#         "uniqueSessionId": session_id,
#         "pageOffset": "1",
#         "pageMaxSize": "10",
#         "sortColumn": "subjectDescription",
#         "sortDirection": "asc"
#     }
#     return requests.Request('GET', base_url, params=params).prepare().url

# @app.get("/get-json-data")
# def get_json_data():
#     cookies = get_cookies()
#     session_id = get_session_id()
#     url = get_modified_url(session_id)
#     cookie_str = ';'.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
#     print(cookie_str)
#     print(session_id)
#     headers = {'Cookie': cookie_str}
#     response = requests.get(url, headers=headers)
    
#     try:
#         return response.json()
#     except ValueError:
#         return {"error": "Invalid JSON response"}

# print(get_json_data())

from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time
import json

app = FastAPI()

def get_modified_url(session_id: str):
    base_url = "https://sturegss.aub.edu.lb/StudentRegistrationSsb/ssb/searchResults/searchResults"
    params = {
        "txt_term": "202420",
        "txt_subject": "CMPS",
        "startDatepicker": "",
        "endDatepicker": "",
        "uniqueSessionId": session_id,
        "pageOffset": "1",
        "pageMaxSize": "200",
        "sortColumn": "subjectDescription",
        "sortDirection": "asc"
    }
    return requests.Request('GET', base_url, params=params).prepare().url

@app.get("/get-json-data")
def get_json_data():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    url = "https://sturegss.aub.edu.lb/StudentRegistrationSsb/ssb/term/termSelection?mode=search"
    driver.get(url)

    cookies = driver.get_cookies()
    cookie_str = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

    session_id = driver.execute_script(
        "return sessionStorage.getItem('xe.unique.session.storage.id');"
    )
    
    input_element = driver.find_element(by=By.ID, value="txt_term")

    script = """
        var elem = arguments[0];
        elem.value = '202420'; 
        elem.setAttribute('listofsearchterms', "202420");
    """
    driver.execute_script(script, input_element)

    continue_button = driver.find_element(by=By.CLASS_NAME, value="form-button")
    continue_button.click()
    
    time.sleep(2)
    
    modified_url = get_modified_url(session_id)
    
    # time.sleep(2)

    headers = {'Cookie': cookie_str}
    response = requests.get(modified_url, headers=headers)
    
    # time.sleep(2)
    
    # subject = driver.find_element(by=By.ID, value="txt_subject")
    # print(subject)
    # script = """var elem = arguments[0]; elem.value = 'CMPS'; elem.setAttribute('value', "CMPS"); elem.value = 'CMPS';"""
    # driver.execute_script(script, subject)
    
    search_button = driver.find_element(by=By.ID, value="search-go")
    search_button.click()
    
    print(session_id)
    print(cookie_str)
    
    time.sleep(2)
    
    data = response.json().get("data")
    filtered_data = []
    for item in data:
        meetings_faculty = item.get('meetingsFaculty', [])
        if isinstance(meetings_faculty, list):
            for meeting in meetings_faculty:
                meeting_time = meeting.get('meetingTime', {})
                if isinstance(meeting_time, dict):
                    building = meeting_time.get('building')
                    if building == "BLISS":
                        filtered_data.append(item)
                        break
                    
    with open('filtered_data.json', 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, ensure_ascii=False, indent=4)
    try:
        return filtered_data
    except ValueError:
        return {"error": "Invalid JSON response"}
    
# get_json_data()

print(get_json_data())
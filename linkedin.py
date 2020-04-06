# connect python with webbrowser-chrome 
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys 
import pyautogui as pag 
from webdriver_manager.chrome import ChromeDriverManager
import time
import pageexploration as ex_pag
import selenium_fun as sel_fun
  
import pandas as pd
    
def main(): 
    #info
    input_infor = "input_information.txt"
    LOGIN_USERNAME = ""
    LOGIN_PSSWORD = ""
    NAME_ARRAY = ""
    # url of LinkedIn 
    url = "http://linkedin.com/login"      
    # path to browser web driver 
    driver = webdriver.Chrome(ChromeDriverManager().install())      
    driver.get(url)
    
    try:
        input_info = ""
        with open(input_infor, 'r') as file:
            input_info = file.read()
        print(input_info)
        gen_info = input_info.split(",")
        if len(gen_info) == 3:
                LOGIN_USERNAME = gen_info[0]
                LOGIN_PSSWORD = gen_info[1]
                NAME_ARRAY = gen_info[2]
                print(NAME_ARRAY)
        else:
            print("wrong input length. you are missing something. ")
    except:
        print("please put in a file called input_information.txt!")
        
    proceed = input("Proceed to login? (press enter) ")
    sel_fun.login(driver, LOGIN_USERNAME, LOGIN_PSSWORD) # login
    time.sleep(2)    
    # grab data from list
    data = ""
    with open(NAME_ARRAY, 'r') as file:
        data = file.read()
    listn = []
    if "," in data:
        data.replace("'", "")
        listn = data.split(",")    
    title_requests = sel_fun.send_requests(driver, listn)
    print(title_requests)
    finaldf = pd.DataFrame(columns = ["Name", "current title", "company"], data = title_requests)
    (finaldf
     .to_csv("linkedin_scrape.csv"));
    driver.quit()

main()

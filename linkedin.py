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
    
    # read input_information to grab username, password, and array of names
    try:
        print("hello! Now reading input_information.txt...")
        input_info = ""
        with open(input_infor, 'r') as file:
            input_info = file.read()
        gen_info = input_info.split(",")
        if len(gen_info) == 3:
                LOGIN_USERNAME = gen_info[0]
                LOGIN_PSSWORD = gen_info[1]
                NAME_ARRAY = gen_info[2]
        else:
            print("wrong input length. you are missing something. ")
    except:
        print("please put in a file in this folder called input_information.txt!")
        
    # input for proceed
    proceed = input("Proceed to login? (press enter) ")
    
    # login
    sel_fun.login(driver, LOGIN_USERNAME, LOGIN_PSSWORD) 
    time.sleep(2)
    proceed = input("complete security")
    # grab data from list
    data = ""
    with open(NAME_ARRAY, 'r') as file:
        data = file.read()
    listn = []
    if "," in data:
        data.replace("'", "")
        listn = data.split(",")    
    
    # traverse data
    title_requests = sel_fun.send_requests(driver, listn)
    
    # print final result
    print(title_requests)
    
    # save result to csv. 
    finaldf = pd.DataFrame(columns = ["Name", "current title", "company", "Grad", "Experience"], data = title_requests)
    (finaldf
     .to_csv("linkedin_withexperience.csv"));
    driver.quit()

main()

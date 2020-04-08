from selenium import webdriver  
from selenium.webdriver.common.keys import Keys 
import pyautogui as pag 
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import re
import os
import requests
import pageexploration as ex_pag
import pandas as pd



# login
def login(driver, LOGIN_USERNAME, LOGIN_PSSWORD): 
    try:
        # Getting the login element 
        username = driver.find_element_by_id("username") 
         # Sending the keys for username       
        username.send_keys(LOGIN_USERNAME) 
    except:
        print("login element not found")

    time.sleep(1)     
    # Getting the password element  
    try:
        # get password textbox
        password = driver.find_element_by_id("password") 
        # Sending the keys for password     
        password.send_keys(LOGIN_PSSWORD)       
    except:
        print("password element not found")
    time.sleep(1)
    try:
        # click submit
        driver.find_element_by_xpath("""//*[@type="submit"]""").click()  
    except:
        print("submit button not found while login in")
        
# go to network tab    
def goto_network(driver): 
    driver.find_element_by_id("mynetwork-tab-icon").click() 

# find search bar element
def find_searchbar(driver):
    try: 
        return driver.find_element_by_xpath("""//*[@placeholder="Search"]""")
    except:
        # retry if linkedin is mean
        time.sleep(2)
        driver.refresh()
        try:
            driver.get("http://linkedin.com/")
            return driver.find_element_by_xpath("""//*[@aria-label="Search"]""")
        except:
            find_searchbar(driver)

# type in searchbar
def type_searchbar(elem, string):
    elem.clear()
    # search person's name plus san diego
    elem.send_keys(string + " san diego")
    elem.send_keys(Keys.RETURN)

# get links from type_searchbar call
def get_links(driver):
    all_links = {}
    try:
        # try getting search container
        try:
            search_cont = driver.find_element_by_class_name("search-results-container")
        except:
            driver.refresh()
            time.sleep(1)
            get_links(driver)
        
        # check if corrections were created by linkedin
        try:
            has_correction = driver.find_element_by_class_name("li-i18n-linkto link-without-visited-state")
            has_link = has_correction.get_attribute("href")
            driver.get(has_link)
            time.sleep(1)
            search_cont = driver.find_element_by_class_name("search-results-container")
        except:
            search_cont = search_cont
        
        # grab ul container
        ul_container = search_cont.find_element_by_tag_name("ul")
        
        # list of a
        people = ul_container.find_elements_by_tag_name("a")
        try:
            for i in people:
                try:
                    cur_href = i.get_attribute("href")
                    all_links[cur_href] = 1
                except: 
                    print()
                    print("-- some error in for loop --")
                    print()
                break
        except:
            print()
            print("--some error in finding href--")
            print()
    except:
        # for containers with single people
        try:
            search_cont = driver.find_element_by_class_name("PROFILE")

            ul_container = search_cont.find_element_by_tag_name("ul")

            people = ul_container.find_elements_by_tag_name("a")

            try:
                for i in people:
                    try:
                        # get link href
                        cur_href = i.get_attribute("href")
                        all_links[cur_href] = 1
                    except: 
                        print()
                        print("-- some error in for loop --")
                        print()
                    break
            except:
                return "no linkedin profile"
        except:
            return "no linkedin found"
    for i in all_links:
        title_received = explore_page(driver, i)
        break
    return title_received

def click_done():
    # button aria-label = "Send now" id="ember1636"
    print("clicking done...")
#     def find_click_connect():
#     # find names for the inputted individuals

def explore_page(driver, link):
    # HTML from element with `get_attribute`
    driver.get(link)
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(document.body.scrollHeight/4, document.body.scrollHeight/2);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(document.body.scrollHeight/2, (document.body.scrollHeight/2)+(document.body.scrollHeight/4));")
    time.sleep(2)
    driver.execute_script("window.scrollTo(document.body.scrollHeight/2, document.body.scrollHeight);")
    time.sleep(1)
    element = driver.find_element_by_class_name("core-rail")
    html = driver.page_source
    # title of individual
    page_title1 = ex_pag.evaluate_html(html)
    # industry of individual
#         industry = ex_pag.find_industry(html)
    return page_title1

def send_requests(driver, listn): 
    title_list = []
    # if a list was given
    for i in listn:
        time.sleep(1)
        searchbar = find_searchbar(driver)
        searchbar.click()
        type_searchbar(searchbar, i)
        time.sleep(2)
        person_title = get_links(driver)
#         print(" ",person_title)
        if len(person_title) > 0:
            if isinstance(person_title,str):
                person_title = [person_title]
            newlist = [i] + person_title
            # newlist.append(person_title)
#             print(newlist)
            title_list.append(newlist)
        else:
            title_list.append("none")
    return title_list
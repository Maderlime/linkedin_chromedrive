from selenium import webdriver  
from selenium.webdriver.common.keys import Keys 
import pyautogui as pag 
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import re
import os
import requests

def evaluate_html(html_string):
#     with open("test.html", "r") as f:
#         contents = f.read()
    wanted_information = []
    
    soup = BeautifulSoup(html_string, 'html.parser')
    
    try:
        title = soup.find("div", {"class":"display-flex mt2"}).find("h2").text.replace("\n", " ")
        reg_title = " ".join(re.findall("[^ \n]+[A-Za-z0-9 ]+[^ \n]", title))
        wanted_information.append(reg_title)
    except:
        wanted_information.append("none")
    
    try:
        title2 = soup.find("ul", {"class":"pv-top-card--experience-list"})
        title2 = title2.text
        title2 = title2.replace("\n", " ").replace("       ",",")
        wanted_information.append(title2)
    except:
        wanted_information.append("none")
        
    try:
        add_baby = True
        title3 = soup.find("section", {"id":"education-section"})
        individual_educations = title3.find_all("li")
        year = ""
        for i in individual_educations:
            school = i.find("h3").text
            school = str(school).upper()
#             print("evaluate ", school) 
            year = i.find_all("time")
#             print("year", year)
            if "University of California".upper() in school:
                wanted_information.append(year[1].text)
                add_baby = False
                break
        if add_baby == True:
            wanted_information.append(str(year))
    except:
        wanted_information.append("none")
    print("wanted: ", wanted_information)
    return wanted_information
    
    
def find_company(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    try:
        title = soup.find("ul", {"class":"pv-top-card--experience-list"})
        title = title.text
        title = title.replace("\n", " ").replace("       ",",")
        return title
    except:
        return "none"
    
def find_gradyear(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    try:
        title = soup.find("section", {"id":"education-section"})
        individual_educations = title.findAll("li")
        for i in individual_educations:
            school = i.find("h3").text
            year = i.findAll("time")[1]
            if "University of California San Diego" in school:
                return year

        return title.find("time").text
    except:
        return "none"
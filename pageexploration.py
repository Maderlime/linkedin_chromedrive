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
    year = "none" 
    try:
        add_baby = True
        title3 = soup.find("section", {"id":"education-section"})
        individual_educations = title3.find_all("li")
        for i in individual_educations:
            school = i.find("h3").text
            school = str(school).upper()
#             print("evaluate ", school) 
            year = i.find_all("time")
            print(school)
            print(year)
            if "University of California".upper() in school:
                wanted_information.append(year[1].text)
                add_baby = False
                break
        if add_baby == True:
            wanted_information.append(str(year))
    except:
        wanted_information.append(year)
    
    educations = []
    try:
        title = soup.find("section", {"id":"experience-section"})
        individual_experience = title.findAll("li")
        for i in individual_experience:
            position = i.find("h3", {"class":"t-16 t-black t-bold"}).text.replace("\n", "")
            year = i.find("h4", {"class":"pv-entity__date-range t-14 t-black--light t-normal"}).text.replace("\n", "")
            place = i.find("p",{"class":"pv-entity__secondary-title t-14 t-black t-normal"}).text.replace("\n", "")      
            educations.append([position, place, year])
        
        wanted_information.append(educations)
    except:
        
        wanted_information.append(educations)
    
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
def find_experience(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    educations = []
    try:
        title = soup.find("section", {"id":"experience-section"})
        individual_experience = title.findAll("li")
        for i in individual_educations:
            position = i.find("h3").text
            place = i.find("pv-entity__secondary-title t-14 t-black t-normal").text
            year = i.find("h4").text
            educations.append([position, place, year])
        return educations
    except:
        return educations
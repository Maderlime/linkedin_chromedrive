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
    soup = BeautifulSoup(html_string, 'html.parser')
    try:
        title = soup.find("div", {"class":"display-flex mt2"}).find("h2").text.replace("\n", " ")
        reg_title = " ".join(re.findall("[^ \n]+[A-Za-z0-9 ]+[^ \n]", title))
        return reg_title
    except:
        return "none"
    
def find_company(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    try:
        title = soup.find("ul", {"class":"pv-top-card--experience-list"})
        title = title.text
        title = title.replace("\n", " ").replace("       ",",")
        return title
    except:
        return "none"
    
def startup_exists(html_string):
    return False
    
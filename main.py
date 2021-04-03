from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime
import sqlite3
from tkinter import *

def formatAndInsertList(day, listString):
    temp = ""
    for i in listString.split():
        temp += ",'" + i + "'"

    cursor.execute("INSERT INTO timetable VALUES('" + day + "'" + temp + ")")


def makeTable():
    print("The Format for entering data: english, maths, sst, german, sanskrit, hindi   Enter 5 subjects only ")
    subjectListMonday = input("Enter Subjects for Monday: ")
    subjectListTuesday = input("Enter Subjects for Tuesday: ")
    subjectListWednesday = input("Enter Subjects for Wednesday: ")
    subjectListThursday = input("Enter Subjects for Thrusday: ")
    subjectListFriday = input("Enter Subjects for Friday: ")

    cursor.execute("DELETE FROM timetable;")

    formatAndInsertList("monday" , subjectListMonday)
    formatAndInsertList("tuesday" , subjectListTuesday)
    formatAndInsertList("wednesday" , subjectListWednesday)
    formatAndInsertList("thursday" , subjectListThursday)
    formatAndInsertList("friday" , subjectListFriday)


    print(cursor.execute("Select * FROM timetable").fetchall())


dbconnection = sqlite3.connect("timetable.db")
cursor = dbconnection.cursor()
#cursor.execute("CREATE TABLE timetable (Day TEXT , Period1 TEXT, Period2 TEXT, Period3 TEXT, Period4 TEXT, Period5 TEXT)")

changeTimetable = input("Change Timetable? (y/n): ")
if(changeTimetable == "n"):
    pass
if(changeTimetable == "y"):
    makeTable()

browser = webdriver.Chrome("chromedriver")
print("Loading Driver complete")
dateToday = datetime.now().month


def waitForPageLoad(delay, xpath):
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return myElem
    except TimeoutException:
        print("Loading took too much time!")

def waitForPageLoadClass(delay, className):
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, className)))
        return myElem
    except TimeoutException:
        print("Loading took too much time!")

def loadCredentials():
    global username
    global password
    file = open("LoginCredentials.txt", "r")
    username = file.readline()
    password = file.readline()

def login():
    loadCredentials()

    username_entry = browser.find_element_by_xpath("/html/body/div/form[1]/div/div/div[2]/div/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/input[1]")
    username_entry.send_keys(username)

    time.sleep(2)

    password_entry = browser.find_element_by_xpath("/html/body/div/form[1]/div/div/div[2]/div/div/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div/div[2]/input")
    password_entry.send_keys(password)

    time.sleep(2)

    stay_signed_in_button = browser.find_element_by_xpath('/html/body/div/form/div/div/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div/div/div[1]/input')
    stay_signed_in_button.click()


browser.get("https://login.microsoftonline.com/common/oauth2/authorize?response_type=id_token&client_id=5e3ce6c0-2b1f-4285-8d4b-75ee78787346&redirect_uri=https%3A%2F%2Fteams.microsoft.com%2Fgo&state=53de18a4-9691-4258-805e-3b3f5713f709&&client-request-id=ecbbd706-d1c8-4f09-a43f-2284b0eed3b2&x-client-SKU=Js&x-client-Ver=1.0.9&nonce=1b098a89-c7e2-41ef-a7b3-b378e186caad&domain_hint=")

time.sleep(2)
login()

channelList = waitForPageLoad(300, "/html/body/div[1]/div[2]/div[1]/div/left-rail/div/div/school-app-left-rail/channel-list/div/div[1]/ul/li/ul/li[4]/div/div/ul")
channelLists = channelList.find_elements_by_tag_name('li')
print(channelLists)

classes_available = waitForPageLoadClass(30, "name-channel-type")
classes_available = browser.find_elements_by_class_name("name-channel-type")

for i in classes_available:
    print(i.get_attribute('innerHTML'))

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime
import sqlite3
import schedule

def formatAndInsertList(day, listString):
    temp = ""
    for i in listString.split():
        temp += ",'" + i + "'"

    cursor.execute("INSERT INTO timetable VALUES('" + day + "'" + temp + ")")


def getClassLinks(subject):
    dictionary = {
        "Biology": "/html/body/div[1]/div[2]/div[1]/div/left-rail/div/div/school-app-left-rail/channel-list/div/div[1]/ul/li/ul/li[2]/div/div/ul/ng-include/li[2]/a",
        "Chemistry": "/html/body/div[1]/div[2]/div[1]/div/left-rail/div/div/school-app-left-rail/channel-list/div/div[1]/ul/li/ul/li[2]/div/div/ul/ng-include/li[3]/a",
    }
    return dictionary[subject]

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

    dbconnection.commit()


    print(cursor.execute("Select * FROM timetable").fetchall())

Period1 = ["9:00", "9:40"]
Period2 = ["10:00", "10:40"]
Period3 = ["11:00", "11:40"]
Period4 = ["12:00", "12:40"]
Period5 = ["13:00", "13:40"]

def waitForPageLoad(delay, xpath):
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return myElem
    except TimeoutException:
        print("Loading took too much time! " + delay + " failed")

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


def convertTuple(tup):
    str =  ''.join(tup)
    return str

def login():
    loadCredentials()

    browser.get("https://login.microsoftonline.com/common/oauth2/authorize?response_type=id_token&client_id=5e3ce6c0-2b1f-4285-8d4b-75ee78787346&redirect_uri=https%3A%2F%2Fteams.microsoft.com%2Fgo&state=53de18a4-9691-4258-805e-3b3f5713f709&&client-request-id=ecbbd706-d1c8-4f09-a43f-2284b0eed3b2&x-client-SKU=Js&x-client-Ver=1.0.9&nonce=1b098a89-c7e2-41ef-a7b3-b378e186caad&domain_hint=")
    time.sleep(2)

    username_entry = browser.find_element_by_xpath("/html/body/div/form[1]/div/div/div[2]/div/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/input[1]")
    username_entry.send_keys(username)

    password_entry = waitForPageLoad(3, "/html/body/div/form[1]/div/div/div[2]/div/div/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div/div[2]/input")
    password_entry.send_keys(password)

    stay_signed_in_button = waitForPageLoad(3, '/html/body/div/form/div/div/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div/div/div[1]/input')
    stay_signed_in_button.click()

def joinClass(className):

    classes_available = waitForPageLoadClass(100, "name-channel-type")
    classes_available = browser.find_elements_by_class_name("name-channel-type")

    for i in classes_available:
        if(convertTuple(className).lower() in str(i.get_attribute('innerHTML')).lower()):
            i.click()

    time.sleep(5)
    try:
        joinbtn = browser.find_element_by_class_name("ts-calling-join-button")
        joinbtn.click()
    except:
        k = 1
        while(k<=15):
        	print("Join button not found, trying again")
        	time.sleep(60)
        	browser.refresh()
        	joinclass(class_name,start_time,end_time)
        	k+=1
        print("Seems like there is no class today.")

    webcam = browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[1]/div/button/span[1]')
    if(webcam.get_attribute('title')=='Turn camera off'):
    	webcam.click()
    	print("TURNED OFF THE CAMERA")
    time.sleep(1)
    microphone = browser.find_element_by_xpath('//*[@id="preJoinAudioButton"]/div/button/span[1]')
    if(microphone.get_attribute('title')=='Mute microphone'):
    	microphone.click()
    	print("TURNED OFF THE MICROPHONE")
    time.sleep(1)
    joinnowbtn = browser.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button')
    joinnowbtn.click()
    print("POGPOGPOGPOG SUCCESFULLY JOINT CLASS")

    time.sleep(40 * 60)
    leave_class()

def leave_class():
	# focus
	browser.send_keys(Keys.CONTROL)
	browser.find_element_by_xpath('//*[@id="hangup-button"]').click()
	time.sleep(5)


def startBrowser():
    global browser
    browser = webdriver.Chrome("chromedriver")
    print("Loading Driver complete")
    login()


dbconnection = sqlite3.connect("timetable.db")
cursor = dbconnection.cursor()
todaysDay = datetime.today().strftime("%A").lower()
todaysDay = "friday"

#cursor.execute("CREATE TABLE timetable (Day TEXT , Period1 TEXT, Period2 TEXT, Period3 TEXT, Period4 TEXT, Period5 TEXT)")

changeTimetable = input("Change Timetable? (y/n): ")
if(changeTimetable == "n"):
    pass
if(changeTimetable == "y"):
    makeTable()

timetable_row = cursor.execute('SELECT * FROM timetable WHERE Day = ?', (todaysDay, )).fetchall()[0]
for i in range(len(timetable_row)):
    currentPeriod = i + 1
    start_time = "null"

    if(currentPeriod == 1):
        start_time = Period1[0]
    elif(currentPeriod == 2):
        start_time = Period2[0]
    elif(currentPeriod == 3):
        start_time = Period3[0]
    elif(currentPeriod == 4):
        start_time = Period4[0]
    elif(currentPeriod == 5):
        start_time = Period5[0]

    print(start_time)
    if(start_time != "null"):
        if(todaysDay == "monday"):
            schedule.every().monday.at(start_time).do(joinClass, timetable_row[currentPeriod])
        elif(todaysDay == "tuesday"):
            schedule.every().tuesday.at(start_time).do(joinClass, timetable_row[currentPeriod])
        elif(todaysDay == "wednesday"):
            schedule.every().wednesday.at(start_time).do(joinClass, timetable_row[currentPeriod])
        elif(todaysDay == "thursday"):
            schedule.every().thursday.at(start_time).do(joinClass, timetable_row[currentPeriod])
        elif(todaysDay == "friday"):
            schedule.every().friday.at(start_time).do(joinClass, timetable_row[currentPeriod])


startBrowser()
while True:
    schedule.run_pending()
    time.sleep(1)

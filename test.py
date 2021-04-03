# imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from ui import ui
import platform
import time

win = ui()
win.mainloop()

def load_site():
    # load the site
    browser.get("https://teams.microsoft.com/go#")

def login_and_correct_view(username, password):
    # username
    print("[Succesful] :: Successfully loaded website ...")
    print("[Process] :: Now logging in")
    input_field = browser.find_element_by_xpath('/html/body/div/form[1]/div/div/div[2]/div/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/input[1]')
    input_field.send_keys(username)
    next_button = browser.find_element_by_xpath("/html/body/div/form[1]/div/div/div[2]/div/div/div[1]/div[2]/div[2]/div/div/div/div[4]/div/div/div/div/input")
    next_button.click()

    #password
    time.sleep(2)
    password_field = browser.find_element_by_xpath("/html/body/div/form[1]/div/div/div[2]/div/div/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div/div[2]/input")
    password_field.send_keys(password)
    login_button = browser.find_element_by_xpath("/html/body/div/form[1]/div/div/div[2]/div/div/div[1]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div/div/div/div/input")
    login_button.click()

    # stay signed in
    time.sleep(1)
    no_but = browser.find_element_by_xpath('/html/body/div/form/div/div/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div/div/div[1]/input')
    no_but.click()

    print('[Succesful] :: Successfully logged in...')

    try:
        element = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[1]/app-bar/nav/ul/li[2]/button'))
        )
    finally:
        element.click()
        print('[Successfull] :: Loaded  teams bar')

    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[1]/teams-grid/div/div[1]/div/school-app-settings-button/button/svg-include/svg'))
        )
    finally:
        element.click()
        print("[Successfull] :: Loaded ")
# credentials loading
with open('./username.txt', 'r') as f:
    username = f.readlines()
with open('./password.txt', 'r') as f:
    password = f.readlines()


# operating system detection for chromdriver
if "linux" in platform.platform().lower():
    PATH = "./chromedriver"
else:
    PATH = "./chromedriver.exe"

print("[Process] :: Loading driver")
# init the driver
browser = webdriver.Chrome(PATH)
print("[Succesful] :: loaded the driver")

load_site()
time.sleep(3)

login_and_correct_view(username, password)

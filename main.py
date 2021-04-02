from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Chrome("chromedriver")
print("Loading Driver complete")

browser.get("https://login.microsoftonline.com/common/oauth2/authorize?response_type=id_token&client_id=5e3ce6c0-2b1f-4285-8d4b-75ee78787346&redirect_uri=https%3A%2F%2Fteams.microsoft.com%2Fgo&state=53de18a4-9691-4258-805e-3b3f5713f709&&client-request-id=ecbbd706-d1c8-4f09-a43f-2284b0eed3b2&x-client-SKU=Js&x-client-Ver=1.0.9&nonce=1b098a89-c7e2-41ef-a7b3-b378e186caad&domain_hint=")

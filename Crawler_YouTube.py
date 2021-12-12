import os

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import AccountManager
import Updater
import utils

initialized = False
driver = None


def init_selenium():
    global driver

    # Work on Chrome Debug Environment
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument("disable-popup-blocking")
    chrome_options.add_argument("--disable-popup-blocking")

    with open('debugChrome.bat', 'w') as f:  # Chrome debug mode files will located in [C:\ChromeDebugENV]
        f.write(f"\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" --remote-debugging-port=9222 "
                f"--user-data-dir=C:\\ChromeDebugENV")
        # print(f"chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\\ChromeDebugENV")
    os.startfile("debugChrome.bat")

    # Attach chromedriver.exe
    if not (os.path.isfile("./chromedriver.exe")):
        print("No drivers have been found.")
        Updater.update_webdriver()
    try:
        driver = webdriver.Chrome("./chromedriver.exe", options=chrome_options)
    except Exception:  # When driver version is diff against chrome
        print("The version between chromedriver.exe and Chrome is inconsistent.")
        Updater.update_webdriver()
        driver = webdriver.Chrome("./chromedriver.exe", options=chrome_options)
    driver.maximize_window()

    # Check Google account state
    driver.get("https://www.google.com")
    try:
        driver.find_element(By.XPATH, '//*[@id="gb"]/div/div[2]/div[2]/div')
        print("Google login information checked")
    except selenium.common.exceptions.NoSuchElementException:  # if need login
        # Show instruction.html
        abspath = utils.get_abspath().replace('\\', '/')
        driver.get(f"file://{abspath}/introduction/introduction.html")

        start_button = driver.find_element(By.XPATH, "/html/body/button")
        while True:
            if start_button.get_property("ready"):  # if ready attribute is 'true' then escape loop
                break
            else:
                utils.sleep(1)

    # Connect to YouTube and prepare to get comments
    driver.get("https://www.youtube.com")
    # TODO go to "my channel"

    global initialized
    initialized = True



def get_new_comment():
    if not initialized:
        raise AttributeError("Selenium should be initialized before using.")
    pass


def reflect_result():
    if not initialized:
        raise AttributeError("Selenium should be initialized before using.")

    pass


def open_tab():
    utils.sleep(2)
    driver.execute_script("window.open();")
    # driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.CONTROL + "t")
    utils.log("오픈탭 지정")
    utils.sleep(2)

def close_tab():
    driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 'w')

def change_tab(num):
    driver.switch_to.window(driver.window_handles[num])

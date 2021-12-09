import os
from selenium import webdriver
from selenium import common
from selenium.webdriver.chrome.options import Options

import Updater
import utils

initialized = False
driver = None


def init_selenium():
    global driver

    # Work on Chrome Debug Environment
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    with open('debugChrome.bat', 'w') as f:  # Chrome debug mode files will located in [C:\ChromeDebugENV]
        f.write(f"\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" --remote-debugging-port=9222 "
                f"--user-data-dir=C:\\ChromeDebugENV")
        print(f"chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\\ChromeDebugENV")
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

    global initialized
    initialized = True


def login():
    login_info = utils.open_file("./setting.rdat")
    if user_data is None:
        print("No user data file detected. Please write ID & PW")
        utils.line()
        print("! We highly recommend to use sub-account which is accessible only comment for your YouTube Channel's "
              "security.")
        utils.line()
        ID = input("ID : ")
        PW = input("PW : ")
        print("Saving to ")


def get_new_comment():
    if not initialized:
        raise AttributeError("Selenium should be initialized before using.")
    pass


def reflect_result():
    if not initialized:
        raise AttributeError("Selenium should be initialized before using.")

    pass

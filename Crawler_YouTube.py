import os
from selenium import webdriver
from selenium import common

import Updater

initialized = False


def init_selenium():
    if not (os.path.isfile("./chromedriver.exe")):
        print("No drivers have been found.")
        Updater.update_webdriver()
    try:
        driver = webdriver.Chrome("./chromedriver.exe")
    except Exception:  # When driver version is diff against chrome
        print("The version between chromedriver.exe and Chrome is inconsistent."
              "it. . .")
        Updater.update_webdriver()
        driver = webdriver.Chrome("./chromedriver.exe")




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
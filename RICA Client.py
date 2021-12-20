import os
import re  # regex
import time
import threading
import zipfile
import requests
import keyboard

import AccountDataManager
import Crawler_YouTube
import Debug
import Updater
from AccountDataManager import RICAAccount
import utils


# Initialization
utils.double_line(40)
print("\n\nRICA Client\nVersion : beta 0.0\n\n")
print("Checking new version. . .")
Updater.check_update()
print("Checking latest model. . .")
Updater.check_latest_model()
print("Checking client data and login. . .")
RICAAccount.login()

print("Done")
utils.sleep(1)
utils.cls()




utils.double_line()
print("RICA - Realtime Improving Comment Analyzer")
print("Please select option\n")
utils.line(10)
print("0. Manual Input")
print("1. YouTube")
print("#. Discord (Unimplemented)")
utils.line(10)
print("1234. * CLEAR ENV & DRIVER *")
utils.line(10)
utils.double_line()

opt = Debug.debug(Debug.SELECT_MENU_AUTOMATICALLY)  # debug
if opt is False:  # Input option number manually
    opt = int(input("\nOption Number : "))
utils.cls()

if opt == 0:  # Manual
    sentence = input("Please input the sentence to analyze : ")
elif opt == 1:  # YouTube
    try:  # Type all codes in try-catch to execute gc.bat at the end of process.
        Crawler_YouTube.init_selenium()
    finally:
        os.startfile("gc.bat")
elif opt == 1234:  # Clear Data
    print("Before reset, please close all your Chrome.exe windows.")
    if input("Type \"Yes\" to reset. This task cannot be recovered (no undo)").lower == 'yes':
        os.startfile("gc.bat")
        os.remove("C:\\ChromeDebugENV")
        os.remove("chromedriver.exe")
        os.remove("setting.rdat")
        print("Successfully deleted files.")
        utils.sleep(3)
        exit(0)


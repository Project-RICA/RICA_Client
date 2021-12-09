import os
import re  # regex
import time
import threading
import zipfile
import requests
import keyboard

import Crawler_YouTube
import Updater
from AccountManager import RICAAccount
import utils

print(requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE_97").text)


print("RICA Client\nVersion : beta 0.0")
print("Checking new version. . .")
Updater.check_update()
print("Checking latest model. . .")
Updater.check_latest_model()
print("Checking client data. . .")
account = RICAAccount()
account.check_rdat()


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

opt = int(input("\nOption Number : "))
utils.cls()

if opt == 0:
    sentence = input("Please input the sentence to analyze : ")
elif opt == 1:
    try:  # Type all codes in try-catch to execute gc.bat at the end of process.
        Crawler_YouTube.init_selenium()
        Crawler_YouTube.login()
    finally:
        os.startfile("gc.bat")
elif opt == 1234:
    print("Before reset, please close all your Chrome.exe windows.")
    if input("Type \"Yes\" to reset. This task cannot be recovered (no undo)").lower == 'yes':
        os.startfile("gc.bat")
        os.remove("C:\\ChromeDebugENV")
        os.remove("chromedriver.exe")
        print("Successfully deleted files.")
        utils.sleep(3)
        exit(0)


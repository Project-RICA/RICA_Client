import os
import re  # regex
import time
import threading
import zipfile
import requests
import keyboard

import Crawler_YouTube
import Updater
import utils

print(requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE_97").text)


print("RICA Client\nVersion : beta 0.0")
print("Checking new version. . .")
Updater.check_update()
print("Checking latest model. . .")
Updater.check_latest_model()
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
utils.double_line()

opt = int(input("\nOption Number : "))
utils.cls()

if opt == 0:
    sentence = input("Please input the sentence to analyze : ")
elif opt == 1:
    Crawler_YouTube.init_selenium()

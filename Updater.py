import os

import requests
from win32com.client import Dispatch

import utils


def check_update():
    pass


def check_latest_model():
    pass


def update_webdriver():
    try:
        os.remove("./chromedriver.exe")
    except Exception: pass  # If there is no file
    paths = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
             r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
    version = list(filter(None, [get_version_via_com(p) for p in paths]))[0]
    print(f"Chrome Version : {version}")
    latest_driver_version = requests.get(f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{version.split('.')[0]}").text
    print(f"Downloading latest chromedriver.exe")
    url = f"https://chromedriver.storage.googleapis.com/{latest_driver_version}/chromedriver_win32.zip"

    utils.download_file(url, "driver.zip")
    utils.uncompress("./driver.zip")
    os.remove("./driver.zip")  # clean byproduct


def get_version_via_com(filename):
    # https://stackoverflow.com/questions/57441421/how-can-i-get-chrome-browser-version-running-now-with-python
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version

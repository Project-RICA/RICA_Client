import functools
import os.path
import time
import zipfile
# from abc import ABCMeta

import requests

def trace(func):  # Use this tracer like : @utils.trace
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"DEBUG : Call {func.__name__}{args, kwargs}")
        result = func(*args, **kwargs)
        print(f"DEBUG : Return {func.__name__}{args, kwargs} -> {result}")
        return result
    return wrapper()

def log(string=''):
    print(f"[{string}] >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

def sleep(t: float):
    time.sleep(t)

def cls(n=10):
    print("\n" * n)

def line(n=20):
    print("-" * n)

def double_line(n=20):
    print("=" * n)

def download_file(url, name):
    # header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36"}
    with open(name, 'wb') as file:  # wb = Write in BinaryMode
        response = requests.get(url).content
        file.write(response)
    print(f"{name} has been downloaded successfully")

def uncompress(path):
    with zipfile.ZipFile(path) as zf:
        zf.extractall()
        print("Uncompress succeed")

def read_file(path):
    temp = None
    try:
        with open(path, 'r') as f:
            temp = f.read()
    except FileNotFoundError:
        return None
    return temp

def is_file_exist(path):
    return os.path.isfile(path)

def get_abspath():  # return like [C:\...\(current folder)]
    return os.path.abspath(__file__).replace("\\utils.py", '')

# def observe(obj, tick=0.1, *target):
#     if target is None:  # Observe changes
#         original = obj.run()
#         while True:
#             sleep(tick)
#             if obj.run != original:
#                 break
#     else:  # If target is set, compare with target value
#         while True:
#             sleep(tick)
#             if obj.run == target:
#                 break

@trace
def wait(data, target, tick=0.1):
    while True:
        if target == data():
            break
        sleep(tick)


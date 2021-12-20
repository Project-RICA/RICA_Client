import functools
import os.path
import time
import zipfile

import requests


# from abc import ABCMeta


def trace(func):  # Use this tracer like : @utils.trace
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        str_args = str(args)
        print(
            f"DEBUG/TRACE : {func.__name__}({str_args[1:len(str_args) - 2] if str_args != '()' else ''}{kwargs if kwargs != {} else ''})")
        result = func(*args, **kwargs)
        print(
            f"DEBUG/TRACE : {func.__name__}({str_args[1:len(str_args) - 2] if str_args != '()' else ''}{kwargs if kwargs != {} else ''}) return -> {result}")
        return result

    return wrapper


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


# @trace
def wait(data, target, tick=0.1, limit=-1, reverse_condition=False):
    while True:
        if target == data() and not reverse_condition:
            break
        elif target != data() and reverse_condition:
            break

        if limit != -1:
            limit -= 1
            if limit == 0:
                raise Exception("Reached to maximum loop number")
        sleep(tick)

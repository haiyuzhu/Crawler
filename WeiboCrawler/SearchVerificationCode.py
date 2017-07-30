# -*- coding: utf-8 -*-
import urllib
import random
import os
import http.cookiejar
import time
from selenium import webdriver
from PIL import Image
from VerifyCode import VerifyCode


def verify(app_id, app_key, username, password):
    code = "FFFF"
    cookie_filename = os.getcwd() + os.sep + "Cookie.txt"
    file_cookiejar = None
    if os.path.exists(cookie_filename):
        print("Load cookie from: " + cookie_filename)
        file_cookiejar = http.cookiejar.LWPCookieJar()
        file_cookiejar.load(cookie_filename, True, True)
    driver = webdriver.Chrome()
    url = "http://s.weibo.com/"
    driver.get(url)
    for c in file_cookiejar:
        cookie_dict = {'domain': None, 'name': c.name,
                       'value': c.value, 'secure': c.secure}
        driver.add_cookie(cookie_dict)
        if c.expires:
            cookie_dict['expiry'] = c.expires
        if c.path_specified:
            cookie_dict['path'] = c.path
    driver.maximize_window()
    driver.get(url)
    driver.save_screenshot("screenshot.png")
    img = driver.find_element_by_class_name("code_img")
    x = img.location["x"]
    y = img.location["y"]
    width = img.size["width"]
    height = img.size["height"]
    im = Image.open("screenshot.png")
    im.crop((x, y, x + width, y + height)).save("pin.png")
    submit = driver.find_element_by_class_name("S_btn_b")
    code_input = driver.find_element_by_class_name("W_inputStp")
    verifier = VerifyCode(app_id, app_key, username, password)
    code = verifier.verify("./pin.png")
    code_input.send_keys(code)
    submit.click()
    time.sleep(1)
    driver.refresh()
    driver.close()


if __name__ == "__main__":
    # add_path()
    verify()

# -*- coding: utf-8 -*-

import os
import sys
import http.cookiejar
import yaml
from WeiboCrawler import Crawler
from WeiboLogin import WeiboLogin
# from WeiboProxy import update_proxy_ips


def parse_configuration(file_path):
    """
    check the parameters is valid.
    param: file_path, path of 'config.yaml'
    """
    f = open(file_path, encoding='utf-8')
    config = yaml.load(f)
    f.close()
    if not config["username"]:
        print("Please config an username!")
        sys.exit(1)
    if not config["password"]:
        print("Please config an password!")
        sys.exit(1)
    if not config["keyword"]:
        print("Please config an keyword!")
        sys.exit(1)
    if not config["start_time"]:
        print("Please config an start_time!")
        sys.exit(1)
    if not config["stop_time"]:
        print("Please config an stop_time!")
        sys.exit(1)
    if not config["region"]:
        print("Please config an region!")
        sys.exit(1)
    if not config["subregion"]:
        print("Please config an subregion!")
        sys.exit(1)
    if not len(config["region"]) == len(config["subregion"]):
        print("Length of region and subregion are not equal!")
        sys.exit(1)
    if not config["weibo_type"]:
        print("Please config an weibo_type!")
        sys.exit(1)
    if not config["weibo_containing"]:
        print("Please config an weibo_containing!")
        sys.exit(1)
    if not config["ydm_username"]:
        print("Please config an ydm_username!")
        sys.exit(1)
    if not config["ydm_password"]:
        print("Please config an ydm_password!")
        sys.exit(1)
    if not config["app_id"]:
        print("Please config an app_id!")
        sys.exit(1)
    if not config["app_key"]:
        print("Please config an app_key!")
        sys.exit(1)
    return config


def get_cookiejar(config):
    cookie_filename = os.getcwd() + os.sep + "Cookie.txt"
    file_cookiejar = None
    if os.path.exists(cookie_filename):
        print("Load cookie from: " + cookie_filename)
        file_cookiejar = http.cookiejar.LWPCookieJar()
        file_cookiejar.load(cookie_filename, True, True)
    else:
        login = WeiboLogin(config["username"], config["password"])
        login.set_yun_da_ma(config["app_id"],
                            bytes(config["app_key"], encoding="utf-8"),
                            bytes(config["ydm_username"], encoding="utf-8"),
                            bytes(config["ydm_password"], encoding="utf-8"))
        if login.login():
            file_cookiejar = login.get_cookiejar()
            file_cookiejar.save(cookie_filename, True, True)
            print("Save cookie to: " + cookie_filename)
        else:
            sys.exit(1)
    return file_cookiejar


def run():
    """
    run the pipeline of the Crawler
    """
    config = parse_configuration("./config.yaml")
    region_num = len(config["region"])
    crawler = Crawler()
    cookiejar = get_cookiejar(config)
    crawler.set_cookiejar(cookiejar)
    for i in range(0, region_num):
        crawler.set_search_target(config["keyword"], config["weibo_type"],
                                  config["weibo_containing"],
                                  config["start_time"], config["stop_time"],
                                  config["region"][i], config["subregion"][i])
        file_name = config["region"][i] + \
            "[" + config["subregion"][i] + "]" + config["keyword"] + \
            config["start_time"] + "_" + config["stop_time"] + ".xlsx"
        crawler.set_save_file_name(file_name)

        crawler.set_yun_da_ma(config["app_id"],
                              bytes(config["app_key"], encoding="utf-8"),
                              bytes(config["ydm_username"], encoding="utf-8"),
                              bytes(config["ydm_password"], encoding="utf-8"))

        crawler.download()


if __name__ == "__main__":
    run()

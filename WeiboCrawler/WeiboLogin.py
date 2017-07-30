# -*- coding: utf-8 -*-
import urllib.error
import urllib.request
import re
import rsa
import http.cookiejar
import base64
import json
import urllib
import urllib.parse
import binascii
from VerifyCode import *


class WeiboLogin():

    def __init__(self, username, password):
        self.password = password
        self.username = username
        self.__LWPCookieJar = None
        self.__ydm_username = ""
        self.__ydm_password = ""
        self.__ydm_app_id = 0
        self.__ydm_app_key = ""

    def set_yun_da_ma(self, app_id, app_key, username, password):
        """
        """
        self.__ydm_app_id = app_id
        self.__ydm_app_key = app_key
        self.__ydm_username = username
        self.__ydm_password = password

    def get_prelogin_args(self):
        '''
        该函数用于模拟预登录过程,并获取服务器返回的 nonce , servertime , pub_key 等信息
        '''
        json_pattern = re.compile('\((.*)\)')
        url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su' + \
            self.get_encrypted_name() + '&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)'
        try:
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            raw_data = response.read().decode('utf-8')
            json_data = json_pattern.search(raw_data).group(1)
            data = json.loads(json_data)
            return data
        except urllib.error as e:
            print("%d" % e.code)
            return None

    def get_encrypted_pw(self, data):
        rsa_e = 65537  # 0x10001
        pw_string = str(data['servertime']) + '\t' + \
            str(data['nonce']) + '\n' + str(self.password)
        key = rsa.PublicKey(int(data['pubkey'], 16), rsa_e)
        pw_encypted = rsa.encrypt(pw_string.encode('utf-8'), key)
        self.password = ''  # 清空password
        passwd = binascii.b2a_hex(pw_encypted)
        # print(passwd)
        return passwd

    def get_encrypted_name(self):
        username_urllike = urllib.request.quote(self.username)
        username_encrypted = base64.b64encode(
            bytes(username_urllike, encoding='utf-8'))
        return username_encrypted.decode('utf-8')

    def enableCookies(self):
        self.__LWPCookieJar = http.cookiejar.LWPCookieJar()
        cookie_support = urllib.request.HTTPCookieProcessor(
            self.__LWPCookieJar)
        opener = urllib.request.build_opener(
            cookie_support, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)

    def get_cookiejar(self):
        """() -> http.cookiejar.LWPCookieJar()
        """
        return self.__LWPCookieJar

    def process_verify_code(self, pcid):
        url = 'http://login.sina.com.cn/cgi/pin.php?r={randint}&s=0&p={pcid}'.format(
            randint=int(random.random() * 1e8), pcid=pcid)
        filename = 'pin.png'
        if os.path.isfile(filename):
            os.remove(filename)
        urllib.request.urlretrieve(url, filename)
        if os.path.isfile(filename):
            verifier = VerifyCode(self.__ydm_app_id, self.__ydm_app_key,
                                  self.__ydm_username, self.__ydm_password)
            code = verifier.verify(filename)
            return dict(pcid=pcid, door=code)
        else:
            return dict()

    def build_post_data(self, raw):
        post_data = {
            "entry":
                "weibo",
            "gateway":
                "1",
            "from":
                "",
            "savestate":
                "7",
            "useticket":
                "1",
            "pagerefer":
                "http://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url=http%3A%2F%2Fweibo.com%2F&domain=.weibo.com&ua=php-sso_sdk_client-0.6.14",
            "vsnf":
                "1",
            "su":
                self.get_encrypted_name(),
            "service":
                "miniblog",
            "servertime":
                raw['servertime'],
            "nonce":
                raw['nonce'],
            "pwencode":
                "rsa2",
            "rsakv":
                raw['rsakv'],
            "sp":
                self.get_encrypted_pw(raw),
            "sr":
                "1280*800",
            "encoding":
                "UTF-8",
            "prelt":
                "115",
            "url":
                "http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "returntype":
                "META"
        }
        if "showpin" in raw and raw["showpin"]:
            code = self.process_verify_code(raw["pcid"])
            post_data.update(code)

        data = urllib.parse.urlencode(post_data).encode('utf-8')
        return data

    def login(self):
        """(WeiboLogin) ->boolean
        True: success, False: unsuccess
        """
        url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
        self.enableCookies()
        data = self.get_prelogin_args()
        post_data = self.build_post_data(data)

        headers = {
            "User-Agent":
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36"
        }
        try:
            request = urllib.request.Request(
                url=url, data=post_data, headers=headers)
            response = urllib.request.urlopen(request)
            html = response.read().decode('GBK')
            # print(html)
        except urllib.error as e:
            print(e.code)

        p = re.compile('location\.replace\(\'(.*?)\'\)')
        p2 = re.compile(r'"uniqueid":"(.*?)"')

        try:
            login_url = p.search(html).group(1)
            print(login_url)
            request = urllib.request.Request(login_url, headers=headers)
            response = urllib.request.urlopen(request)
            page = response.read().decode('GBK')
            redict = p2.search(page)
            if redict is None:
                return False
            uuid_res = redict.group(1)
            login_url = "http://weibo.com/%s/profile?topnav=1&wvr=6&is_all=1" % uuid_res
            request = urllib.request.Request(login_url, headers=headers)
            response = urllib.request.urlopen(request)
            print("Login success!")
            return True
        except Exception as e:
            print('Login error!')
            print(e)
            return False


if __name__ == '__main__':
    login = WeiboLogin('', '')
    login.login()
    login.get_cookiejar().save("Cookie.txt", True, True)

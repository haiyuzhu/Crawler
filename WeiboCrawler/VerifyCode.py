# -*- coding: utf-8 -*-
import sys
import os
from ctypes import *

# 下载接口放目录 http://www.yundama.com/apidoc/YDM_SDK.html
# 错误代码请查询 http://www.yundama.com/apidoc/YDM_ErrorCode.html
# 所有函数请查询 http://www.yundama.com/apidoc


class VerifyCode:

    def __init__(self, app_id, app_key, username, password):
        """
        param: number, byte str, byte str, byte str, byte str
        """
        self.__YDMApi = windll.LoadLibrary('yundamaAPI-x64')
        self.__appId = app_id
        self.__appKey = app_key
        self.__username = username
        self.__password = password

    def verify(self, file_name):
        """(str)->str

        param: filename: file name of the verify code
        return: Node, failed; code, str type
        """

        # 分配30个字节存放识别结果
        result = c_char_p(b"                              ")

        # 识别超时时间 单位：秒
        timeout = 60

        # 验证码文件路径
        file_name_byte = bytes(file_name, encoding="utf-8")

        # 一键识别函数，无需调用 YDM_SetAppInfo 和 YDM_Login，适合脚本调用
        # captchaId = YDMApi.YDM_EasyDecodeByPath(username, password, appId, appKey, filename,codetype, timeout, result)
        # 第一步：初始化云打码，只需调用一次即可
        self.__YDMApi.YDM_SetAppInfo(self.__appId, self.__appKey)

        # 第二步：登陆云打码账号，只需调用一次即可
        uid = self.__YDMApi.YDM_Login(self.__username, self.__password)
        if uid > 0:
            print('>>>正在获取余额...')

            # 查询账号余额，按需要调用
            balance = self.__YDMApi.YDM_GetBalance(
                self.__username, self.__password)

            print('登陆成功，用户名：%s，剩余题分：%d' % (self.__username, balance))
            print('\r\n>>>正在普通识别...')

            # 第三步：开始识别

            # 例：1004表示4位字母数字，不同类型收费不同。请准确填写，否则影响识别率。
            # 在此查询所有类型 http://www.yundama.com/price.html
            codetype = 1004

            # 分配30个字节存放识别结果
            # result = c_char_p(b"                              ")

            # 验证码文件路径
            # filename = b'getimage.jpg'

            # 普通识别函数，需先调用 YDM_SetAppInfo 和 YDM_Login 初始化
            captchaId = self.__YDMApi.YDM_DecodeByPath(
                file_name_byte, codetype, result)
            # captchaId = self.__YDMApi.YDM_DecodeByPath(file_name_byte, codetype, result)
            code = "FFFF"
            if captchaId > 0 and len(result.value) == 4:
                if isinstance(result.value, int):
                    code = str(result.value)
                if isinstance(result.value, bytes):
                    try:
                        code = result.value.decode()
                    except:
                        print("验证码解码错误：code=%s" % result.value)
                        return "FFFF"
                print("普通识别：验证码ID：%d，识别结果：%s" % (captchaId, code))
                return code
            else:
                print("失败失败,错误代码：%d" % captchaId)
                return code
        else:
            print('登陆失败，错误代码：%d' % uid)
            return "FFFF"

from random import randint

import requests


class SmsSendAPIDemo(object):
    """互亿无线短信发送接口示例代码"""
    API_URL = "http://106.ihuyi.com/webservice/sms.php?method=Submit"

    # init函数一般初始化对象私有的关键的属性，其他属性通过调用对象的方法来赋值
    # 类属性/方法：存储/操作所有对象公共的数据、对象方法：存储/操作所有对象私有的数据、静态方法：和类/对象无关，附着的关系
    def __init__(self, api_id, api_key, mobile):
        """
        Args:
            api_id (str) 产品密钥ID，产品标识
            api_key (str) 产品私有密钥，服务端生成签名信息使用
            mobile (str) 业务ID，易盾根据产品业务特点分配
        """
        self.api_id = api_id
        self.api_key = api_key
        self.mobile = mobile

    def send(self, params):
        """请求互亿无线接口
        Args:
            params (object) 请求参数
        Returns:
            请求结果，json格式
        """
        params["account"] = self.api_id
        params["password"] = self.api_key
        params["mobile"] = self.mobile

        try:
            response = requests.post(self.API_URL, data=params)
            return response.json()
        except Exception as ex:
            print("调用API接口失败:", str(ex))

def send_verification_code(MOBILE):
    API_ID = 'C32603962'
    API_KEY = '35ce0c86c5e7892bf4fa715b66847801'
    api = SmsSendAPIDemo(API_ID, API_KEY, MOBILE)
    # 验证码随机生成
    code = ''
    for i in range(6):
        ran = randint(0,9)
        code += str(ran)
    params = {
        "content": f'您的验证码是：{code}。请不要把验证码泄露给其他人。',
        "format": "json"
    }
    # 注释不调用云端接口了，通过设置下面的字符串模拟调用
    # ret = api.send(params)
    ret = {'code': 2, 'msg': '提交成功', 'smsid': '16603935735515116540'}
    return ret, code

if __name__ == "__main__":
    # 1、互亿无线的短信服务方式，直接调用
    # 接口地址
    # url = 'http://106.ihuyi.com/webservice/sms.php?method=Submit'

    # # 定义请求的数据
    # values = {
    #     'account': 'C32603962',
    #     'password': '35ce0c86c5e7892bf4fa715b66847801',
    #     'mobile': '18515721914',
    #     'content': '您的验证码是：7835。请不要把验证码泄露给其他人。',
    #     'format': 'json',
    # }

    # # 发起请求
    # try:
    #     response = requests.post(url,data=values)
    # except Exception as ex:
    #     print('调用API接口失败:',str(ex))

    # # 打印结果
    # print(response.json())

    # 1、互亿无线的短信服务方式，类调用
    API_ID = 'C32603962'
    API_KEY = '35ce0c86c5e7892bf4fa715b66847801'
    MOBILE = '18515721914'
    api = SmsSendAPIDemo(API_ID, API_KEY, MOBILE)

    params = {
        "content": '您的验证码是：7835。请不要把验证码泄露给其他人。',
        "format": "json"
    }
    ret = api.send(params)
    # print(ret)
    if ret is not None:
        if ret["code"] == 2:
            smsId = ret["smsid"]
            print("smsId = %s" % smsId)
        else:
            print("ERROR: ret.code=%s,msg=%s" % (ret['code'], ret['msg']))


#-----------------------------------------盾短信发送接口示例代码--------------------------------------------------------
# import hashlib
# import json
# import random
# import time
# import requests
#
#
# class SmsSendAPIDemo(object):
#     """易盾短信发送接口示例代码"""
#     API_URL = "https://sms.dun.163yun.com/v2/sendsms"
#     VERSION = "v2"
#
#     def __init__(self, secret_id, secret_key, business_id):
#         """
#         Args:
#             secret_id (str) 产品密钥ID，产品标识
#             secret_key (str) 产品私有密钥，服务端生成签名信息使用
#             business_id (str) 业务ID，易盾根据产品业务特点分配
#         """
#         self.secret_id = secret_id
#         self.secret_key = secret_key
#         self.business_id = business_id
#
#     def gen_signature(self, params=None):
#         """生成签名信息
#         Args:
#             params (object) 请求参数
#         Returns:
#             参数签名md5值
#         """
#         buff = ""
#         for k in sorted(params.keys()):
#             buff += str(k) + str(params[k])
#         buff += self.secret_key
#         return hashlib.md5(buff.encode('utf-8')).hexdigest()
#
#     def send(self, params):
#         """请求易盾接口
#         Args:
#             params (object) 请求参数
#         Returns:
#             请求结果，json格式
#         """
#         params["secretId"] = self.secret_id
#         params["businessId"] = self.business_id
#         params["version"] = self.VERSION
#         params["timestamp"] = int(time.time() * 1000)
#         params["nonce"] = int(random.random() * 100000000)
#         params["signature"] = self.gen_signature(params)
#
#         try:
#             # params = urllib.urlencode(params)
#             # request = urllib2.Request(self.API_URL, params)
#             # content = urllib2.urlopen(request, timeout=1).read()
#             response = requests.post(self.API_URL, data=params)
#             return response.json()
#         except Exception as ex:
#             print("调用API接口失败:", str(ex))
#
#
# if __name__ == "__main__":
#     """示例代码入口"""
#     SECRET_ID = "dcc535cbfaefa2a24c1e6610035b6586"  # 产品密钥ID，产品标识
#     SECRET_KEY = "d28f0ec3bf468baa7a16c16c9474889e"  # 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露
#     BUSINESS_ID = "748c53c3a363412fa963ed3c1b795c65"  # 业务ID，易盾根据产品业务特点分配
#     api = SmsSendAPIDemo(SECRET_ID, SECRET_KEY, BUSINESS_ID)
#
#     params = {
#         "mobile": "15010185644",
#         "templateId": "10084",
#         "paramType": "json",
#         "params": "json格式字符串"
#         # 国际短信对应的国际编码(非国际短信接入请注释掉该行代码)
#         # "internationalCode": "对应的国家编码"
#     }
#     ret = api.send(params)
#     print(ret)
#     if ret is not None:
#         if ret["code"] == 200:
#             taskId = ret["result"]["taskId"]
#             print("taskId = %s" % taskId)
#         else:
#             print("ERROR: ret.code=%s,msg=%s" % (ret['code'], ret['msg']))


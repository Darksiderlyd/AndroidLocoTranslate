# -*- coding: UTF-8 -*-
import sys
import uuid
import hashlib
import time
import json

import opencc

import common_function
import config
import urllib2
import urllib

reload(sys)
sys.setdefaultencoding('utf-8')

YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = '7dc4c705ab0bff34'
APP_SECRET = '5El4oofIgYlYPzhm4p7jaVR5ua0yWOV0'


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    q_utf8 = q.decode("utf-8")
    size = len(q_utf8)
    return q_utf8 if size <= 20 else q_utf8[0:10] + str(size) + q_utf8[size - 10:size]


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # return requests.post(YOUDAO_URL, data=data, headers=headers)
    d = urllib.urlencode(data)
    request = urllib2.Request(YOUDAO_URL, data=d, headers=headers)
    try:
        response = urllib2.urlopen(request)
        values = json.loads(response.read().encode('UTF-8'))
        print values
        print("(完成)")
        return values
    except Exception as e:
        print("(失败)"), e
        return None


def translate(text='', f='zh-CN', to='zh-CHT'):
    q = text

    data = {}
    data['from'] = f
    data['to'] = to
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = q
    data['salt'] = salt
    data['sign'] = sign
    # data['vocabId'] = "您的用户词表ID"

    result = do_request(data)
    if (len(result) > 0 and ("translation" in result)):
        value = result["translation"]
        return value
    else:
        log = "\n翻译失败:" + q + "\n"
        print log
        return ""


def translateKeyValues(keyValues={}, f='zh-CN', to='zh-CHT'):
    if (len(keyValues) <= 0):
        return
    newKeyValues = {}
    for key in keyValues:
        converter = opencc.OpenCC('s2t.json')
        translateValue = converter.convert(keyValues[key])
        # translateValue = translate(keyValues[key], f=f, to=to)
        if (len(translateValue) > 0):
            newKeyValues[key] = translateValue
    return newKeyValues

def translateValue(value='', f='zh-CN', to='zh-CHT'):
    if (len(value) <= 0):
        return value
    converter = opencc.OpenCC('s2t.json')
    translateValue = converter.convert(value)
    return translateValue


## 翻译剩余HK
def translateUnHK():
    values = common_function.downloadStrings()
    if (len(values) <= 0):
        return
    locoCN = 'zh-CN'
    locoHK = 'zh-HK'
    cnStringsMap = values[locoCN]
    hkStringsMap = values[locoHK]
    newUnTranslateHKMap = {}
    for key in cnStringsMap:
        if key not in hkStringsMap:
            newUnTranslateHKMap[key] = cnStringsMap[key]
            continue
        if (len(hkStringsMap[key]) <= 0):
            newUnTranslateHKMap[key] = cnStringsMap[key]
    if (len(newUnTranslateHKMap) <= 0):
        return
    translateMap = translateKeyValues(newUnTranslateHKMap)
    if (len(translateMap) > 0):
        isSuccess = common_function.locoImport(translateMap, locale=config.updatedSynchHantLocal)
        if isSuccess == False:
            log = "繁体翻译上传Loco -> " + config.updatedSynchHantLocal + " 失败"
            print log
            return
        print("繁体翻译成功count:"), len(translateMap)
        print(translateMap)


if __name__ == '__main__':
    # test
    # result = translateKeyValues({"123":"合成的音频存储路径"})
    # print result

    ## 将未翻译的zh-HK翻译,并上传到 Loco zh-HK
    # translateUnHK()
    # translateValue = translate("%s x %s 股")
    translateValue = translate("资产")
    print translateValue
    print translateValue[0].encode('utf-8')

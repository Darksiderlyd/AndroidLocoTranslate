# -*- coding: UTF-8 -*-
import os
import ssl
import sys

import common_function
import config
import translate


# 上传中文附带繁体翻译
def updateCnAndHkString(update):
    lineDict = common_function.fetch_localized_string_from_all_path(config.dirValuesZHName)

    if len(lineDict) == 0:
        print '没有数据'
        return

    locoAssetIdsResult = common_function.downloadStringsZipReturnMap(config.dirValuesZHName)

    loco_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = loco_base_dir + "/log.txt"
    if os.path.exists(log_file):
        os.remove(log_file)
    f_log = open(log_file, 'w+')

    plusKeyValue = {}
    f_log.write('==============有修改或者新增开始==============\n')
    print '==============有修改或者新增开始=============='
    for key in lineDict.keys():
        for symbolKey in config.symbolTable:
            lineDict[key] = lineDict[key].replace(symbolKey, config.symbolTable[symbolKey])
            locoAssetIdsResult[key] = locoAssetIdsResult[key].replace(symbolKey, config.symbolTable[symbolKey])

        if len(lineDict[key]) > 0 and (
                key not in locoAssetIdsResult or (
                key in locoAssetIdsResult and lineDict[key] != locoAssetIdsResult[key])):
            msg = key + "\n" + "|" + lineDict[key] + '|\n' + "|" + locoAssetIdsResult[key] + '|\n\n'
            print msg
            f_log.write(msg)
            plusKeyValue[key] = lineDict[key].encode('utf-8')
    f_log.write('==============有修改或者新增开始==============\n')
    print '==============有修改或者新增结束=============='
    print len(plusKeyValue)
    f_log.close()

    if update is None or update == 1:
        print '需要将参数修改为 0'
        return

    if (len(plusKeyValue) > 0):
        success = common_function.locoImport(plusKeyValue, config.updatedSynchLocalCn)
        if not success:
            print "中文 上传Loco -> " + config.updatedSynchLocalCn + " 失败"
            return
        print("新增成功！count:"), len(plusKeyValue)
        print plusKeyValue

        if config.updatedSynchHant == True:
            translateMap = translate.translateKeyValues(plusKeyValue)
            if (len(translateMap) > 0):
                isSuccess = common_function.locoImport(translateMap, config.updatedSynchHantLocal)
                if isSuccess == False:
                    log = "繁体翻译上传Loco -> " + config.updatedSynchHantLocal + " 失败"
                    print log
                    return

                print("新增繁体翻译成功count:"), len(translateMap)
                print(translateMap)
            else:
                print("无新增翻译key！！！！")
    else:
        print("无新增中文key！！！！")


if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    if len(sys.argv) > 1:
        updateCnAndHkString(sys.argv[1])
    else:
        updateCnAndHkString(1)

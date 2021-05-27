# -*- coding: UTF-8 -*-
import os

import common_function
import config
import translate


# 迁移繁体
def migrateHK():
    locoAssetIdsResult = common_function.downloadStringsZipReturnMap(config.dirValuesHKName)
    lineDict = common_function.fetch_localized_string_from_all_path(config.dirValuesHKName)
    if len(lineDict) == 0:
        print '没有数据'
        return

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

        if len(lineDict[key]) > 0 and key in locoAssetIdsResult and lineDict[key] != locoAssetIdsResult[key]:
            msg = key + "\n" + "|" + lineDict[key] + '|\n' + "|" + locoAssetIdsResult[key] + '|\n\n'
            print msg
            f_log.write(msg)
            plusKeyValue[key] = lineDict[key].encode('utf-8')

    f_log.write('==============有修改或者新增开始==============\n')
    print '==============有修改或者新增结束=============='
    print len(plusKeyValue)
    f_log.close()

    # if (len(plusKeyValue) > 0):
    #     if config.updatedSynchHant == True:
    #         isSuccess = common_function.locoImport(plusKeyValue, config.updatedSynchHantLocal)
    #         if isSuccess == False:
    #             log = "繁体翻译上传Loco -> " + config.updatedSynchHantLocal + " 失败"
    #             print log
    #             return
    #         print("更新繁体成功:"), len(plusKeyValue)
    #     else:
    #         print("无新增中文！！！！")


if __name__ == '__main__':
    migrateHK()

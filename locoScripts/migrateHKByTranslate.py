# -*- coding: UTF-8 -*-
import common_function
import config
import translate


# 迁移繁体
def migrateHKByTranslateZH():
    # locoAssetIdsResult = common_function.downloadLocoAllAssetIds()
    lineDict = common_function.fetch_localized_string_from_all_path(config.dirValuesZHName)
    print "122"
    if len(lineDict) == 0:
        print '没有数据'
        return
    plusKeyValue = {}
    for key in lineDict.keys():
        if len(lineDict[key]) > 0:
            plusKeyValue[key] = lineDict[key].encode('utf-8')
    print plusKeyValue
    if (len(plusKeyValue) > 0):
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
            print("无新增中文！！！！")


if __name__ == '__main__':
    migrateHKByTranslateZH()
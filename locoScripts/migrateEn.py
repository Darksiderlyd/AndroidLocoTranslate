# -*- coding: UTF-8 -*-
import common_function
import config

#迁移英文
def migrateEn():
    # locoAssetIdsResult = common_function.downloadLocoAllAssetIds()
    lineDict = common_function.fetch_localized_string_from_all_path(config.dirValuesENName)
    if len(lineDict) == 0:
        return '没有数据'
    plusKeyValue = {}
    for key in lineDict.keys():
        if len(lineDict[key]) > 0:
            plusKeyValue[key] = lineDict[key].encode('utf-8')
    print plusKeyValue
    if (len(plusKeyValue) > 0):
        success = common_function.locoImport(plusKeyValue, config.updatedSynchLocalEN)
        if not success:
            print "英文 上传Loco -> " + config.updatedSynchLocalEN + " 失败"
            return
        print("新增英文成功！count:"), len(plusKeyValue)
        print plusKeyValue

if __name__ == '__main__':
    migrateEn()
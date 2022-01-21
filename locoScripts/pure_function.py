# -*- coding: UTF-8 -*-
import os
import sys
import time
import config
import xml.dom.minidom

reload(sys)
sys.setdefaultencoding('utf8')


# 分配字符串到不同的module下的res对应的values文件下
def downloadStringsDispatchStringToModuleWhiteList():
    loco_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.dirname(loco_base_dir)
    log_file = loco_base_dir + "/strings-notranslate.xml"
    try:
        if os.path.exists(log_file):
            os.remove(log_file)
        f_log = open(log_file, 'w+')

        checkTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        f_log.write("<!-- 检测时间: " + checkTime + " -->\n")

        for modulePath in fetch_all_modules_dirPaths_by_whitelist():
            # print "module: " + modulePath
            localZHStringsResFile = os.path.join(modulePath, config.pathDestRes, config.dirValuesZHName, 'strings.xml')

            localStringMap = fetch_local_translatable_string(localZHStringsResFile)

            recordHadWriteStringKeys = []
            loglines = []

            moduleNames = modulePath.split("/")

            loglines.append("<!-- " + moduleNames[len(moduleNames) - 1] + " -->\n")
            loglines.append("<resources>\n")
            for resValuesDir in config.dirNeedUpdateValuesList:

                localNotZHStringsResFile = os.path.join(base_dir, modulePath, config.pathDestRes, resValuesDir,
                                                        'strings.xml')
                localNotCnStringMap = fetch_local_translatable_string(localNotZHStringsResFile)

                for localKey in localStringMap:
                    if localKey not in config.keyBlackList and localKey not in recordHadWriteStringKeys and (
                            localKey not in localNotCnStringMap or localNotCnStringMap[localKey] is None or len(
                        localNotCnStringMap[localKey]) <= 0):
                        recordHadWriteStringKeys.append(localKey)
                        loglines.append(
                            "    <string name=\"" + localKey + "\">" + localStringMap[localKey] + "</string>\n")

            loglines.append("</resources>\n\n")

            f_log.writelines(loglines)

        f_log.close()

    except Exception as e:
        print("(失败)"), e
        return e


def fetch_all_modules_dirPaths_by_whitelist():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(base_dir)
    dirArrays = []
    for moduleName in config.moduleFilters:
        modulePath = os.path.join(base_dir, moduleName)
        if not os.path.exists(modulePath):
            print modulePath + " 不存在，请检查config.moduleFilters是否配置正确"
        else:
            print modulePath + " 存在添加到dirArrays"
            dirArrays = dirArrays + [modulePath]

    return dirArrays


# 拉取可翻译的字串
def fetch_local_translatable_string(path=None):
    if path is {}:
        return {}
    totalList = {}
    totalUnTranslatable = {}
    xmldoc = xml.dom.minidom.parse(path)
    stringNodes = xmldoc.getElementsByTagName('string')
    for node in stringNodes:
        for item in node.childNodes:
            translatable = node.getAttribute('translatable')

            key = node.getAttribute('name')
            value = item.data

            if translatable is None or len(translatable) == 0 or translatable == "true":
                totalList[key.decode('UTF-8')] = value.decode('UTF-8')
            else:
                totalUnTranslatable[key.decode('UTF-8')] = value.decode('UTF-8')
                print "UnTranslatable: [key: value] ==> [" + key.decode('UTF-8') + ": " + value.decode('UTF-8') + "]"

    for blackKey in config.keyBlackList:
        if blackKey in totalList:
            totalList.pop(blackKey)

    return totalList


# 根据ModuleName获取文案
def fetch_localized_string_from_all_path_by_module(moduleName=None, dirName=None):
    if moduleName == None or dirName == None:
        return {}
    dirPaths = fetch_all_modules_dirPaths_by_whitelist()
    print("all Dirs:"), dirPaths
    totalDict = fatch_localized_string_form_dirPaths_android(dirPaths, dirName)
    log = "localized string count:{}".format(len(totalDict))
    print log
    return totalDict


# 获取Android目录下所有本地Key
def fatch_localized_string_form_dirPaths_android(dirPaths=None, stringFile=None):
    if (len(dirPaths) <= 0):
        print("error: not dirPaths")
        return {}
    totalList = {}
    for dirname in dirPaths:
        path = dirname + '/src/main/res/' + stringFile + '/strings.xml'  # 先写死
        print path
        if not os.path.exists(path):
            continue
        xmldoc = xml.dom.minidom.parse(path)

        stringNodes = xmldoc.getElementsByTagName('string')
        for node in stringNodes:
            for item in node.childNodes:
                key = node.getAttribute('name')
                # print key
                value = item.data
                totalList[key.decode('UTF-8')] = value.decode('UTF-8')

    for blackKey in config.keyBlackList:
        if blackKey in totalList:
            totalList.pop(blackKey)

    return totalList


if __name__ == '__main__':
    # fetch_all_modules_dirPaths_by_whitelist()
    downloadStringsDispatchStringToModuleWhiteList()
# -*- coding: UTF-8 -*-
import os
import sys
import time
import config
import xml.dom.minidom
import xml.etree.cElementTree as etXmlParser

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

        hasUntranslatableStr = False

        for modulePath in fetch_all_modules_dirPaths_by_whitelist():
            # print "module: " + modulePath
            localZHStringsResFile = os.path.join(modulePath, config.pathDestRes, config.dirValuesZHName, 'strings.xml')

            localStringMap = fetch_local_translatable_string(localZHStringsResFile)

            recordHadWriteStringKeys = []
            loglines = []

            moduleNames = modulePath.split("/")

            loglines.append("<!-- " + moduleNames[len(moduleNames) - 1] + " -->\n")
            loglines.append("<resources>\n")
            for resValuesDir in config.dirValuesList:

                localNotZHStringsResFile = os.path.join(base_dir, modulePath, config.pathDestRes, resValuesDir,
                                                        'strings.xml')
                localNotCnStringMap = fetch_local_translatable_string(localNotZHStringsResFile)


                for localKey in localStringMap:

                    if resValuesDir == "values" and localKey == "app_name":
                        print localNotCnStringMap[localKey]

                    if localKey not in config.keyBlackList and localKey not in recordHadWriteStringKeys and (
                            localKey not in localNotCnStringMap or localNotCnStringMap[localKey] is None or len(
                        localNotCnStringMap[localKey]) <= 0):
                        recordHadWriteStringKeys.append(localKey)
                        loglines.append(
                            "    <string name=\"" + localKey + "\">" + localStringMap[localKey] + "</string>\n")
                        hasUntranslatableStr = True

            loglines.append("</resources>\n\n")

            for line in loglines:
                print line

            f_log.writelines(loglines)

        f_log.close()

        if hasUntranslatableStr:
            print "FOUND_UNTRANSLATABLE_STING"
        else:
            print "NOT_FOUND_UNTRANSLATABLE_STING"

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
    # print 'path: ' + path
    totalUnTranslatable = {}

    xmlTree = etXmlParser.parse(path)
    root = xmlTree.getroot()
    for item in root.findall('string'):  # 找到root节点下的所有string节点
        key = item.get('name')  # 子节点string下属性name的值
        value = item.text  # 子节点string的值
        translatable = item.get('translatable')
        # print key,value,translatable

        if translatable is None or len(translatable) == 0 or translatable == "true":
            if value is not None:
                totalList[key.decode('UTF-8')] = value.decode('UTF-8')
            else:
                totalList[key.decode('UTF-8')] = ""
        else:
            totalUnTranslatable[key.decode('UTF-8')] = value.decode('UTF-8')
            print "UnTranslatable: [key: value] ==> [" + key.decode('UTF-8') + ": " + value.decode('UTF-8') + "]"


    # xmldoc = xml.dom.minidom.parse(path)
    # stringNodes = xmldoc.getElementsByTagName('string')
    # for node in stringNodes:
    #     for item in node.childNodes:
    #         translatable = node.getAttribute('translatable')
    #
    #         key = node.getAttribute('name')
    #         value = item.data
    #
    #         if translatable is None or len(translatable) == 0 or translatable == "true":
    #             totalList[key.decode('UTF-8')] = value.decode('UTF-8')
    #         else:
    #             totalUnTranslatable[key.decode('UTF-8')] = value.decode('UTF-8')
    #             print "UnTranslatable: [key: value] ==> [" + key.decode('UTF-8') + ": " + value.decode('UTF-8') + "]"

    for blackKey in config.keyBlackList:
        if blackKey in totalList:
            totalList.pop(blackKey)

    return totalList

def parseXmlTree(path=None):
    if path is None:
        return None
    xmlTree = etXmlParser.parse(path)
    root = xmlTree.getroot()
    for string in root.findall('string'):  # 找到root节点下的所有string节点
        name = string.get('name')  # 子节点string下属性name的值
        value = string.text  # 子节点string的值
        print name, value
    return xmlTree

if __name__ == '__main__':
    # parseXmlTree('/Users/yaodonglv/IdeaProjects/loco/app/src/main/res/values/strings.xml')
    downloadStringsDispatchStringToModuleWhiteList()

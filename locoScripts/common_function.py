# -*- coding: UTF-8 -*-
import os
import json
import time
import urllib2
import urllib
import config
import md5
import sys
import xml.dom.minidom
import zipfile
import distutils.dir_util
import shutil
import opencc

import xml.etree.cElementTree as etXmlParser

reload(sys)
sys.setdefaultencoding('utf8')


# 字符串md5
def genearteMD5(str):
    m1 = md5.new()
    m1.update(str.encode('utf-8'))
    return m1.hexdigest()


# def lines_to_md5Key_value(lines=None, ignoreAssetIds=None):
#     if ignoreAssetIds is None:
#         ignoreAssetIds = []
#     if (len(lines) <= 0):
#         return {}
#     md5keyValue = {}
#     for row in range(len(lines)):
#         key = lines[row]
#         if (len(key) > 0):
#             md5key = genearteMD5(key)
#             if md5key not in ignoreAssetIds:
#                 md5keyValue[md5key] = key
#     return md5keyValue


def lines_to_md5CN_en_single_value_android(lines=None, linesEn=None):
    if lines is None:
        lines = {}
    if linesEn is None:
        linesEn = {}
    if (len(lines) <= 0):
        return {}

    md5CNENValue = {}
    for key in lines.keys():
        if len(lines[key]) > 0 and key in linesEn and len(linesEn[key]) > 0:
            cnMd5key = genearteMD5(lines[key]).encode('utf-8')
            md5CNENValue[cnMd5key] = linesEn[key].encode('utf-8')

    return md5CNENValue


def lines_to_md5Key_en_single_value_android(lines=None, linesEn=None):
    if lines is None:
        lines = {}
    if linesEn is None:
        linesEn = {}
    if (len(lines) <= 0):
        return {}

    md5KeyENValue = {}
    for key in lines.keys():
        if len(lines[key]) > 0 and key in linesEn and len(linesEn[key]) > 0:
            md5Key = genearteMD5(key).encode('utf-8')
            md5KeyENValue[md5Key] = linesEn[key].encode('utf-8')
    return md5KeyENValue


def lines_to_md5CN_single_value_android(lines=None, ignoreAssetIds=None):
    if ignoreAssetIds is None:
        ignoreAssetIds = []
    if lines is None:
        lines = {}
    if (len(lines) <= 0):
        return {}

    md5ALlValueMap = {}

    md5KeyKeyValue = {}
    md5KeyCNValue = {}

    for key in lines.keys():
        if (len(lines[key]) > 0):
            cnMd5key = genearteMD5(lines[key]).encode('utf-8')
            if cnMd5key not in ignoreAssetIds:
                md5KeyKeyValue[key.encode('utf-8')] = cnMd5key
                md5KeyCNValue[cnMd5key] = lines[key].encode('utf-8')

    md5ALlValueMap[config.updatedSynchLocalHansCNAndroidKey] = md5KeyKeyValue
    md5ALlValueMap[config.updatedSynchLocalCn] = md5KeyCNValue
    return md5ALlValueMap


def lines_to_md5Key_repeat_value_android(lines=None, ignoreAssetIds=None):
    if ignoreAssetIds is None:
        ignoreAssetIds = []
    if lines is None:
        lines = {}
    if (len(lines) <= 0):
        return {}
    md5ALlValueMap = {}

    md5KeyKeyValue = {}
    md5KeyCNValue = {}

    for key in lines.keys():
        if (len(lines[key]) > 0):
            md5Keykey = genearteMD5(key).encode(encoding='utf-8')
            if md5Keykey not in ignoreAssetIds:
                md5KeyKeyValue[key.encode(encoding='utf-8')] = md5Keykey
                md5KeyCNValue[md5Keykey] = lines[key]

    md5ALlValueMap[config.updatedSynchLocalHansCNAndroidKey] = md5KeyKeyValue
    md5ALlValueMap[config.updatedSynchLocalCn] = md5KeyCNValue

    return md5ALlValueMap


# 获取所有模块目录 通过过滤手段列出要更新的文件
def fetch_all_modules_dirPaths():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(base_dir)
    dirArrays = []
    for file in os.listdir(base_dir):
        if file.startswith(config.pathFilter):
            fileName = base_dir + '/' + file
            print fileName
            dirArrays = dirArrays + [fileName]
    return dirArrays


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


def get_dirPath_by_module(module=None):
    if module == None:
        return None
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    result = os.path.join(base_dir, module)
    print(result)
    return result


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


def fetch_download_localized_string(path=None):
    if path is {}:
        return {}
    totalList = {}
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


# 遍历所有代码，提取所有翻译keys
def fetch_localized_string_from_all_cn_path():
    dirPaths = fetch_all_modules_dirPaths()
    print("all Dirs:"), dirPaths
    totalList = fatch_localized_string_form_dirPaths_android(dirPaths, config.dirValuesZHName)
    log = "localized string count:{}".format(len(totalList))
    print log
    return totalList


def fetch_localized_string_from_all_en_path():
    dirPaths = fetch_all_modules_dirPaths()
    print("all Dirs:"), dirPaths
    totalList = fatch_localized_string_form_dirPaths_android(dirPaths, config.dirValuesENName)
    log = "localized string count:{}".format(len(totalList))
    print log
    return totalList


# 在使用
def fetch_localized_string_from_all_path(dirName=None):
    if dirName is {}:
        return {}
    dirPaths = fetch_all_modules_dirPaths_by_whitelist()
    print("all Dirs:"), dirPaths
    totalDict = fatch_localized_string_form_dirPaths_android(dirPaths, dirName)
    log = "localized string count:{}".format(len(totalDict))
    print log
    return totalDict


# 在使用
def fetch_localized_string_from_all_path_by_module(moduleName=None, dirName=None):
    if moduleName == None or dirName == None:
        return {}
    dirPaths = fetch_all_modules_dirPaths_by_whitelist()
    print("all Dirs:"), dirPaths
    totalDict = fatch_localized_string_form_dirPaths_android(dirPaths, dirName)
    log = "localized string count:{}".format(len(totalDict))
    print log
    return totalDict


# 获取cloud端全量key
def downloadLocoAllAssetIds():
    print("获取Loco云端 all asset Ids ... ")
    url = 'https://localise.biz:443/api/assets?key=' + config.locoReadonlyAppKey
    print(url)
    request = urllib2.Request(url)
    try:
        response = urllib2.urlopen(request)
        values = json.loads(response.read())
        lines = [value[u"id"] for value in values]
        print("(完成)")
        return [True, lines]
    except Exception as e:
        print("(失败)"), e
        return [False, e]


# 下载所有Stings
def downloadStrings():
    print("正在下载所有翻译文档 ... ")
    url = 'https://localise.biz:443/api/export/all.json?key=' + config.locoReadonlyAppKey
    request = urllib2.Request(url)
    try:
        response = urllib2.urlopen(request)
        values = json.loads(response.read())
        print values
        print("(完成)")
        return values
    except Exception as e:
        print("(失败)"), e
        return e


# 分配字符串到不同的module下的res对应的values文件下
def downloadStringsDispatchStringToModuleWhiteList():
    print("正在下载所有翻译文档Zip ... ")
    url = 'https://localise.biz:443/api/export/archive/xml.zip?format=android&key=' + config.locoReadonlyAppKey
    loco_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.dirname(loco_base_dir)
    file_name = loco_base_dir + "/strings.zip"
    log_file = loco_base_dir + "/log.txt"
    try:
        f = urllib2.urlopen(url).read()
        open(file_name, 'wb').write(f)
        # 解压
        # if os.path.exists(file_name):
        zip_file = zipfile.ZipFile(file_name, "r")
        zip_list = zip_file.namelist()  # 压缩文件清单，可以直接看到压缩包内的各个文件的明细
        for f in zip_list:  # 遍历这些文件，逐个解压出来，
            zip_file.extract(f, loco_base_dir)
        zip_file.close()

        archiveDir = os.path.join(loco_base_dir, config.archiveFileName)

        downloadStringsResDir = os.path.join(archiveDir, "res")

        downloadStringsMapByValuesDir = {}

        if os.path.exists(log_file):
            os.remove(log_file)
        f_log = open(log_file, 'w+')

        for resValuesDir in config.dirValuesList:
            downloadResDir = os.path.join(downloadStringsResDir, resValuesDir, "strings.xml")
            downloadStringsMapByValuesDir[resValuesDir] = fetch_download_localized_string(downloadResDir)
            print downloadResDir

        updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for modulePath in fetch_all_modules_dirPaths_by_whitelist():
            print "module: " + modulePath
            localZHStringsResFile = os.path.join(modulePath, config.pathDestRes, config.dirValuesZHName,
                                                 'strings.xml')
            localStringMap = fetch_download_localized_string(localZHStringsResFile)

            for resValuesDir in config.dirNeedUpdateValuesList:

                logPrintLocation = modulePath + " : " + resValuesDir + " : "

                localWriteStringsResDir = os.path.join(base_dir, modulePath, config.pathDestRes, resValuesDir)

                if not os.path.exists(localWriteStringsResDir):
                    os.makedirs(localWriteStringsResDir)

                localWriteStringsResFile = os.path.join(base_dir, modulePath, config.pathDestRes, resValuesDir,
                                                        'strings.xml')

                if not os.path.exists(localWriteStringsResFile):
                    shutil.copy(os.path.join(loco_base_dir, 'strings.xml'), localWriteStringsResDir)

                downloadStringMap = downloadStringsMapByValuesDir[resValuesDir]

                f = open(localWriteStringsResFile, 'w+')
                lines = []

                lines.append("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
                lines.append("<!-- 更新时间: " + updateTime + " -->\n")
                lines.append("<resources>\n")

                for localKey in localStringMap:
                    if localKey not in downloadStringMap or downloadStringMap[localKey] == None or len(
                            downloadStringMap[localKey]) <= 0:
                        if modulePath == "/Users/yaodonglv/IdeaProjects/loco/app":
                            print localKey
                        continue

                    for symbolKey in config.symbolTable:
                        downloadStringMap[localKey] = downloadStringMap[localKey].replace(symbolKey,
                                                                                          config.symbolTable[
                                                                                              symbolKey])

                    lines.append(
                        "    <string name=\"" + localKey + "\">" + downloadStringMap[localKey] + "</string>\n")

                    downloadCount = downloadStringMap[localKey].count('%')
                    currentCount = localStringMap[localKey].count('%')

                    if downloadStringMap[localKey] != localStringMap[localKey]:
                        log = "\n" + logPrintLocation + " 警告：" + localKey + ": 本地内容与下载不一致内容被修改: Download: " + \
                              downloadStringMap[
                                  localKey] + "  Local: " + downloadStringMap[localKey]
                        f_log.write(log)
                        print log
                        continue

                    if downloadCount != currentCount:
                        log = "\n" + logPrintLocation + " 警告 " + localKey + ":「%」占位符个数不一致: Download: " + \
                              downloadStringMap[
                                  localKey] + "  Local: " + localStringMap[localKey]
                        log2 = "    DownloadCount: " + downloadCount + " LocalCount" + currentCount
                        f_log.write(log)
                        f_log.write(log2)
                        print log
                        print log2
                        continue

                lines.append("</resources>\n")
                print lines
                f.writelines(lines)

        f_log.close()
        f.close()

    except Exception as e:
        print("(失败)"), e
        return e


# 下载所有Stings
def downloadStringsZipAndWriteToLocal():
    print("正在下载所有翻译文档Zip ... ")
    url = 'https://localise.biz:443/api/export/archive/xml.zip?format=android&key=' + config.locoReadonlyAppKey
    loco_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.dirname(loco_base_dir)
    file_name = loco_base_dir + "/strings.zip"
    log_file = loco_base_dir + "/log.txt"
    try:
        f = urllib2.urlopen(url).read()
        open(file_name, 'wb').write(f)
        # 解压
        # if os.path.exists(file_name):
        zip_file = zipfile.ZipFile(file_name, "r")
        zip_list = zip_file.namelist()  # 压缩文件清单，可以直接看到压缩包内的各个文件的明细
        for f in zip_list:  # 遍历这些文件，逐个解压出来，
            zip_file.extract(f, loco_base_dir)
        zip_file.close()

        archiveDir = os.path.join(loco_base_dir, config.archiveFileName)
        downloadStringsDir = os.path.join(archiveDir, "res")
        libstringsResDir = os.path.join(base_dir, config.pathDestRes)

        os.remove(log_file)
        f_log = open(log_file, 'w+')

        for dir in config.dirValuesList:
            localAllMap = fetch_localized_string_from_all_path(dir)
            resDir = os.path.join(downloadStringsDir, dir, "strings.xml")
            print resDir
            downloadAllMap = fetch_download_localized_string(resDir)
            f = open(resDir, 'w+')
            lines = []
            lines.append("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
            lines.append("<resources xmlns:xliff=\"urn:oasis:names:tc:xliff:document:1.2\">\n")

            for downloadKey in downloadAllMap:
                if downloadAllMap[downloadKey] == None or len(downloadAllMap[downloadKey]) <= 0:
                    continue

                for symbolKey in config.symbolTable:
                    downloadAllMap[downloadKey] = downloadAllMap[downloadKey].replace(symbolKey,
                                                                                      config.symbolTable[symbolKey])

                lines.append(
                    "    <string name=\"" + downloadKey + "\">" + downloadAllMap[downloadKey] + "</string>\n")

                if downloadKey not in localAllMap:
                    log = "\n" + dir + " 警告：本地不存在 " + downloadKey
                    f_log.write(log)
                    print log
                    continue

                downloadCount = downloadAllMap[downloadKey].count('%')
                currentCount = localAllMap[downloadKey].count('%')

                if downloadAllMap[downloadKey] != localAllMap[downloadKey]:
                    log = "\n" + dir + " 警告：" + downloadKey + ": 本地内容与下载不一致内容被修改: Download: " + downloadAllMap[
                        downloadKey] + "  Local: " + localAllMap[downloadKey]
                    f_log.write(log)
                    print log
                    continue

                if downloadCount != currentCount:
                    log = "\n" + dir + " 警告 " + downloadKey + ":「%」占位符个数不一致: Download: " + downloadAllMap[
                        downloadKey] + "  Local: " + localAllMap[downloadKey]
                    log2 = "    DownloadCount: " + downloadCount + " LocalCount" + currentCount
                    f_log.write(log)
                    f_log.write(log2)
                    print log
                    print log2
                    continue

            lines.append("</resources>\n")
            print lines
            f.writelines(lines)

        f_log.close()
        f.close()

        # f_log.close()
        # f = open(resDir, 'r+')
        # lines = f.readlines()
        # for line in lines:
        #     for symbolKey in config.symbolTable:
        #         line.replace(symbolKey, config.symbolTable[symbolKey])
        # f = open(resDir, 'w+')
        # f.writelines(lines)
        # print downloadAllMap

        print downloadStringsDir
        print libstringsResDir
        distutils.dir_util.copy_tree(downloadStringsDir, libstringsResDir)
        print '文件替换完成请查看！'
        return file_name
    except Exception as e:
        print("(失败)"), e
        return e


def getLineKey(line=None):
    if line is None:
        return None
    posKeyStart = line.find("<string name=") + len("<string name=") + 1
    posKeyEnd = line.find("\">")
    print posKeyStart
    print posKeyEnd
    if posKeyStart != -1 and posKeyEnd != -1:
        return line[posKeyStart:posKeyEnd]


#
#
# def getLineValue():


# 写入到本地
def writeToLocal(values):
    localAllKeys = fetch_localized_string_from_all_cn_path()
    localAllmd5KeyValues = lines_to_md5Key_value(localAllKeys)
    current_path = os.path.abspath(__file__)
    current_folder_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    os.chdir(current_folder_path)
    os.chdir('../..')
    rootFolder = os.getcwd() + '/' + config.localDir
    os.chdir(rootFolder)
    fileMap = config.map
    replaceAllKeys = [value for value in config.replaceValueMap if (len(value) > 0)]
    iosKeyStrings = values['och-CN']
    cnStrings = values['zh-CN']
    for dict in fileMap:
        if (dict['locoCode'] == 'och-CN'):
            continue
        name = dict['name']
        locoCode = dict['locoCode']
        print('Converting locaized strings for ' + name)
        folderName = name + '.lproj'
        fileName = folderName + '/' + 'Localizable.strings'
        fp = open(fileName, 'w')
        strings = values[locoCode]
        for key in strings:
            if (key not in localAllmd5KeyValues.keys()):
                continue
            if (key not in iosKeyStrings.keys()):
                continue
            if (iosKeyStrings[key] != localAllmd5KeyValues[key]):
                log = "\nios key 被修改:\nmd5:" + key + "\nloco ios key(错误值):" + iosKeyStrings[key] + "\nlocal key(正确值):" + \
                      localAllmd5KeyValues[key] + "\n"
                print log
                continue
            iosKey = localAllmd5KeyValues[key]
            if (len(iosKey) <= 0):
                continue
            value = strings[key]
            if len(value) <= 0:
                continue
            if value in replaceAllKeys:
                value = config.replaceValueMap[value]
            # 占位符警告
            if key in cnStrings and (len(cnStrings[key]) > 0):
                cnCount = cnStrings[key].count('%')
                currentCount = value.count('%')
                if cnCount != currentCount:
                    log = "\n警告" + name + ":「%」占位符个数不一致:\nzh-CN: " + cnStrings[key] + "\n" + name + ": " + value + "\n"
                    print log
            appendtext = '\"' + iosKey + '\"' + ' ' + '=' + ' ' + '\"' + value + '\"' + ';' + '\n'
            fp.write(appendtext.encode("utf-8"))
    print("All done! Check it at " + os.getcwd())
    return


# import loco json
# keyValues key:value, （key:为ios key MD5）
# locale: 语言
# ignoreExisting: 是否已存在的不更新，默认NO
def locoImport(keyValues=None, locale="zh-Hans-CN", ignoreExisting=False):
    print("正在import to loco -> "), locale
    ignore = "true"
    if ignoreExisting == False:
        ignore = "false"
    url = 'https://localise.biz:443/api/import/json?index=id&locale=' + locale + '&key=' + config.locoWriteAppkey + '&ignore-existing=' + ignore
    params = {
        "data": json.dumps(keyValues).encode('utf-8')
    }
    print(url)
    data = urllib.urlencode(params)
    request = urllib2.Request(url, data)
    try:
        response = urllib2.urlopen(request)
        values = json.loads(response.read())
        print(values)
        print("(完成)\n")
        return True
    except Exception as e:
        print(e)
        print("(失败)\n")
        return False


def updateSingleLanguage(locale=None):
    if locale == None:
        print '请填上传的locale'
        return
    loco_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_name = os.path.join(loco_base_dir, 'updateStrings.xml')
    print file_name
    keymap = fetch_download_localized_string(file_name)
    if keymap is None or len(keymap) <= 0:
        print '没有要上传的数据 keymap is null'
        return
    print keymap
    locoImport(keymap, locale)


def translateCHS2CHT():
    loco_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    simpleStrings = os.path.join(loco_base_dir, 'strings_simple.xml')
    chtStrings = os.path.join(loco_base_dir, 'stringsCHT.xml')
    f = open(chtStrings, 'w+')
    keyMap = fetch_download_localized_string(simpleStrings)
    converter = opencc.OpenCC('s2t.json')
    lines = []
    lines.append("<?xml version=\"1.0\" encoding=\utf-8\"?>\n")
    lines.append("<resources>\n")
    for key in keyMap.keys():
        lines.append(
            "    <string name=\"" + key + "\">" + converter.convert(keyMap[key]) + "</string>\n")
    lines.append("</resources>\n")

    f.writelines(lines)
    f.close()


def downloadStringsDispatchStringToModuleWhiteList2():
    print("正在下载所有翻译文档Zip ... ")
    url = 'https://localise.biz:443/api/export/archive/xml.zip?format=android&key=' + config.locoReadonlyAppKey
    loco_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.dirname(loco_base_dir)
    file_name = loco_base_dir + "/strings.zip"
    log_file = loco_base_dir + "/log.txt"
    try:
        f = urllib2.urlopen(url).read()
        open(file_name, 'wb').write(f)
        # 解压
        # if os.path.exists(file_name):
        zip_file = zipfile.ZipFile(file_name, "r")
        zip_list = zip_file.namelist()  # 压缩文件清单，可以直接看到压缩包内的各个文件的明细
        for f in zip_list:  # 遍历这些文件，逐个解压出来，
            zip_file.extract(f, loco_base_dir)
        zip_file.close()

        archiveDir = os.path.join(loco_base_dir, config.archiveFileName)

        downloadStringsResDir = os.path.join(archiveDir, "res")

        downloadStringsMapByValuesDir = {}

        if os.path.exists(log_file):
            os.remove(log_file)
        f_log = open(log_file, 'w+')

        for resValuesDir in config.dirValuesList:
            downloadResDir = os.path.join(downloadStringsResDir, resValuesDir, "strings.xml")
            downloadStringsMapByValuesDir[resValuesDir] = fetch_download_localized_string(downloadResDir)
            print downloadResDir

        for modulePath in fetch_all_modules_dirPaths_by_whitelist():
            print "module: " + modulePath
            localZHStringsResFile = os.path.join(modulePath, config.pathDestRes, config.dirValuesZHName,
                                                 'strings.xml')

            # localStringMap = fetch_download_localized_string(localZHStringsResFile)

            xmlTree = parseXmlTree(localZHStringsResFile)
            root = xmlTree.getroot()

            for resValuesDir in config.dirNeedUpdateValuesList:

                logPrintLocation = modulePath + " : " + resValuesDir + " : "

                localWriteStringsResDir = os.path.join(base_dir, modulePath, config.pathDestRes, resValuesDir)

                if not os.path.exists(localWriteStringsResDir):
                    os.makedirs(localWriteStringsResDir)

                localWriteStringsResFile = os.path.join(base_dir, modulePath, config.pathDestRes, resValuesDir,
                                                        'strings.xml')

                if not os.path.exists(localWriteStringsResFile):
                    shutil.copy(os.path.join(loco_base_dir, 'strings.xml'), localWriteStringsResDir)

                downloadStringMap = downloadStringsMapByValuesDir[resValuesDir]

                for string in root.findall('string'):
                    localKey = string.get('name')
                    localValue = string.text

                    if localKey not in downloadStringMap or downloadStringMap[localKey] == None or len(
                            downloadStringMap[localKey]) <= 0:
                        root.remove(string)
                        continue

                    for symbolKey in config.symbolTable:
                        downloadStringMap[localKey] = downloadStringMap[localKey].replace(symbolKey,
                                                                                          config.symbolTable[
                                                                                              symbolKey])

                    lines.append(
                        "    <string name=\"" + localKey + "\">" + downloadStringMap[localKey] + "</string>\n")

                    downloadCount = downloadStringMap[localKey].count('%')
                    currentCount = localStringMap[localKey].count('%')

                    if downloadStringMap[localKey] != localStringMap[localKey]:
                        log = "\n" + logPrintLocation + " 警告：" + localKey + ": 本地内容与下载不一致内容被修改: Download: " + \
                              downloadStringMap[
                                  localKey] + "  Local: " + downloadStringMap[localKey]
                        f_log.write(log)
                        print log
                        continue

                    if downloadCount != currentCount:
                        log = "\n" + logPrintLocation + " 警告 " + localKey + ":「%」占位符个数不一致: Download: " + \
                              downloadStringMap[
                                  localKey] + "  Local: " + localStringMap[localKey]
                        log2 = "    DownloadCount: " + downloadCount + " LocalCount" + currentCount
                        f_log.write(log)
                        f_log.write(log2)
                        print log
                        print log2
                        continue

                # f = open(localWriteStringsResFile, 'w+')
                # lines = []
                # lines.append("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
                # lines.append("<resources>\n")
                #
                # for localKey in localStringMap:
                #     if localKey not in downloadStringMap or downloadStringMap[localKey] == None or len(
                #             downloadStringMap[localKey]) <= 0:
                #         if modulePath == "/Users/yaodonglv/IdeaProjects/loco/app":
                #             print localKey
                #         continue
                #
                #     for symbolKey in config.symbolTable:
                #         downloadStringMap[localKey] = downloadStringMap[localKey].replace(symbolKey,
                #                                                                           config.symbolTable[
                #                                                                               symbolKey])
                #
                #     lines.append(
                #         "    <string name=\"" + localKey + "\">" + downloadStringMap[localKey] + "</string>\n")
                #
                #     downloadCount = downloadStringMap[localKey].count('%')
                #     currentCount = localStringMap[localKey].count('%')
                #
                #     if downloadStringMap[localKey] != localStringMap[localKey]:
                #         log = "\n" + logPrintLocation + " 警告：" + localKey + ": 本地内容与下载不一致内容被修改: Download: " + \
                #               downloadStringMap[
                #                   localKey] + "  Local: " + downloadStringMap[localKey]
                #         f_log.write(log)
                #         print log
                #         continue
                #
                #     if downloadCount != currentCount:
                #         log = "\n" + logPrintLocation + " 警告 " + localKey + ":「%」占位符个数不一致: Download: " + \
                #               downloadStringMap[
                #                   localKey] + "  Local: " + localStringMap[localKey]
                #         log2 = "    DownloadCount: " + downloadCount + " LocalCount" + currentCount
                #         f_log.write(log)
                #         f_log.write(log2)
                #         print log
                #         print log2
                #         continue
                #
                # lines.append("</resources>\n")
                # print lines
                # f.writelines(lines)

        f_log.close()
        # f.close()

    except Exception as e:
        print("(失败)"), e
        return e


def parseXmlTree(path=None):
    if path is None:
        return None
    xmlTree = etXmlParser.parse(path)
    # root = xmlTree.getroot()
    # for string in root.findall('string'):  # 找到root节点下的所有string节点
    #     name = string.get('name')  # 子节点string下属性name的值
    #     value = string.text  # 子节点string的值
    #     print name, value
    return xmlTree


if __name__ == '__main__':
    inFile = '/Users/yaodonglv/IdeaProjects/loco/toolsloco/updateStrings.xml'
    outFile = '/Users/yaodonglv/IdeaProjects/loco/toolsloco/output.xml'

    xmlTree = parseXmlTree(inFile)
    xmlTree.write(outFile, "utf-8", True)

    # translateCHS2CHT()

    # print converter.convert('%s x %s 股')  # 漢字

    # downloadStringsDispatchStringToModuleWhiteList()
    # file1 = "/Users/yaodonglv/IdeaProjects/loco/libstrings/src/main/res/values-zzzz"
    # file2 = "/Users/yaodonglv/IdeaProjects/loco/libstrings/src/main/res/values-zzzz/strings.xml"
    #
    # if not os.path.exists(file1):
    #     os.makedirs(file1)
    # if not os.path.exists(file2):
    #     shutil.copy("/Users/yaodonglv/IdeaProjects/loco/toolsloco/strings.xml", file1)

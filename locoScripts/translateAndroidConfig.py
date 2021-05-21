# -*- coding: UTF-8 -*-
import os

import common_function
import config as globalconfig
import translate
import json
import copy


def translateConfigCommon(inFileName, outFileName):
    loco_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    IN_FILE_PATH = os.path.join(loco_base_dir, inFileName)
    OUT_FILE_PATH = os.path.join(loco_base_dir, outFileName)
    with open(IN_FILE_PATH, 'r') as load_f:
        load_dict = json.load(load_f)

    config = load_dict['config']
    processConfig(config, True)

    with open(OUT_FILE_PATH, 'w') as f:
        json.dump(load_dict, f, ensure_ascii=False, indent=4)


def translateConfig2():
    loco_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    IN_FILE_PATH = os.path.join(loco_base_dir, "serverCanaryCopyConfig.json")
    OUT_FILE_PATH = os.path.join(loco_base_dir, "serverCanaryOutConfig.json")
    translateConfigCommon(IN_FILE_PATH, OUT_FILE_PATH)


# 迁移繁体
def translateConfig():
    loco_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    IN_FILE_PATH = os.path.join(loco_base_dir, "serverCopyConfig.json")
    OUT_FILE_PATH = os.path.join(loco_base_dir, "serverOutConfig.json")
    with open(IN_FILE_PATH, 'r') as load_f:
        load_dict = json.load(load_f)

    config = load_dict['config']
    processConfig(config, True)

    with open(OUT_FILE_PATH, 'w') as f:
        json.dump(load_dict, f, ensure_ascii=False, indent=4)


def processConfig(config, showKey=False):
    if config is None:
        return

    if isinstance(config, list):
        for pos in range(len(config)):
            if isinstance(config[pos], dict):
                processConfig(config[pos])
        return

    needTranslate = False
    noEnKey = []
    for key in config.keys():
        if key.endswith('_en') or key == 'en':
            needTranslate = True
            if key.endswith('_en'):
                noEnKey.append(key.replace('_en', ''))

    if needTranslate:
        for key2 in config.keys():
            if key2.endswith('_cn'):
                config[key2.replace('_cn', '_' + globalconfig.newLanguagePrefix)] = translate.translateValue(
                    config[key2])
                print key2
            if key2 in noEnKey:
                config[key2 + '_' + globalconfig.newLanguagePrefix] = translate.translateValue(config[key2])
                print key2
            if key2 == 'cn':
                config[globalconfig.newLanguagePrefix] = translate.translateValue(config[key2])
                print key2

    for key1 in config.keys():
        if isinstance(config[key1], dict):
            processConfig(config[key1])

        configList = config[key1]
        if isinstance(configList, list):
            for pos in range(len(configList)):
                if isinstance(config[key1][pos], dict):
                    processConfig(config[key1][pos])
                if isinstance(config[key1][pos], list):
                    processConfig(config[key1][pos])


if __name__ == '__main__':
    translateConfig2()

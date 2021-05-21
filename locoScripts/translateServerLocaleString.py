# -*- coding: UTF-8 -*-
import sys
import uuid
import hashlib
import time
import json
import common_function
import translate
import config
import urllib2
import urllib
import os
import copy

reload(sys)
sys.setdefaultencoding('utf-8')

IN_FILE_PATH='/Users/cheng/Desktop/ServerLocaleString.json'
OUT_FILE_PATH='/Users/cheng/Desktop/ServerLocaleString2.json'

def translateServerString():
    with open(IN_FILE_PATH,'r') as load_f:
        load_dict = json.load(load_f)
        
    for key in load_dict:
        model = load_dict[key]
        if "locals" in model:
            for i in range(len(model["locals"])):
                locals = model["locals"]
                localModel = locals[i]
                if localModel["local"] == "zh-Hans":
                    hkLocalModel = {"local":"zh-HK"}
                    hkLocalModel["message"] = translate.translateKeyValues({"message":localModel["message"]})["message"][0]
                    locals += [hkLocalModel]
                    diclog = json.dumps(hkLocalModel, ensure_ascii = False, encoding = 'utf-8')
                    print(diclog)
        if "section_locals" in model:
            for i in range(len(model["section_locals"])):
                section_locals = model["section_locals"]
                section=section_locals[i]
                if section["local"] == "zh-Hans":
                    if "sections" in section:
                        hksections = []
                        hksection_local = {"local":"zh-HK","sections":hksections}
                        sectionMesArr = section["sections"]
                        for i in range(len(sectionMesArr)):
                            cnModel = sectionMesArr[i]
                            hkModel = {}
                            if "message" in cnModel:
                                hkModel["message"] = translate.translateKeyValues({"message":cnModel["message"]})["message"][0]
                            if "actions" in cnModel:
                                actions = cnModel["actions"]
                                hkactions = []
                                hkModel["actions"] = hkactions
                                for i in range(len(actions)):
                                    cnaction = actions[i]
                                    hkaction = copy.deepcopy(cnaction)
                                    hkaction["action_title"] = translate.translateKeyValues({"action_title":cnaction["action_title"]})["action_title"][0]
                                    hkactions += [hkaction]
                            hksections += [hkModel]
                        section_locals += [hksection_local]
                            

    with open(OUT_FILE_PATH, 'w') as f:
        json.dump(load_dict, f,ensure_ascii=False,indent = 4)

    return

Server_FILE_PATH='/Users/cheng/Desktop/Test/ServerLocaleString-server.json'
Local_FILE_PATH='/Users/cheng/Desktop/Test/ServerLocaleString-local.json'
Local_OUT_FILE_PATH='/Users/cheng/Desktop/Test/ServerLocaleString.json'

def mergeServerToLocal():
    
    with open(Local_FILE_PATH,'r') as load_f:
        local_dict = json.load(load_f)

    with open(Local_FILE_PATH,'r') as load_f:
        server_dict = json.load(load_f)

    for key in server_dict:
        local_dict[key] = server_dict[key]

    with open(Local_OUT_FILE_PATH, 'w') as f:
        json.dump(local_dict, f,ensure_ascii=False,indent = 4)
    
    return

if __name__ == '__main__':
    print("test")
    mergeServerToLocal()

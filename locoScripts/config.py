# -*- coding: UTF-8 -*-
# 需要遍历翻译的目录集, 「values* 默认以包含」
dirValuesZHName = 'values'
dirValuesHKName = 'values-zh-rHK'
dirValuesENName = 'values-en'
dirNeedUpdateValuesList = ['values-zh-rHK', 'values-en']
dirValuesList = ['values', 'values-zh-rHK', 'values-en']

# 对应替换符号表
symbolTable = {'\\u0020': ' ', '\\\\\"': '\\\"', '\\\\\'': '\\\'', '\\\\t': '\\t', '\\\\n': '\\n', '<': '&#060;',
               '&': "&#038;",
               '\\\\': '\\', '爲': '為'}

allUpdate = False
# archiveFileName = "test-xml-archive"
archiveFileName = "android-xml-archive"

# localise app key
# 正式
locoReadonlyAppKey = "Abq2xeDHXn3MQfUTzz0EzI1tpzwQIyH3"  # 正式
# locoWriteAppkey = "JRSm2-TsPDLFQbWkgTG06ksW0Nq9Dpgzh"

# 测试
# locoReadonlyAppKey = "GPQkaKWNfDXSjbklMng5Kg8mLVVDzp4t"
locoWriteAppkey = "JRSm2-TsPDLFQbWkgTG06ksW0Nq9Dpgzh"

updatedSynchLocal = ['zh-CN', 'zh-HK']

switchAutoUpdate = False
switchChangeAndAddUpdate = False

updatedSynchLocalCn = 'zh-CN'
updatedSynchLocalEN = 'en'
# 增量更新是否同时翻译繁体 (香港)
updatedSynchHant = True
updatedSynchHantLocal = 'zh-HK'

pathFilter = 'libstrings'
moduleFilters = ['libstrings', 'app', 'libcomment', 'libcommon', 'libnews', 'libshare', 'mdaccount', 'mdmarket',
                 'mdwealth']

keyBlackList = ['market_home_num']

formattedBlackList = ['account_system_info', 'account_hello_user_s', 'market_follow_delete_tips',
                      'wealth_make_order_part_success']

pathDestRes = 'src/main/res'

newLanguagePrefix = 'hk'

# 语言翻译对应的表格列。
map = [
    {
        'name': 'AndroidKey',
        'locoCode': 'zh-Hans-CN',
        'google_columnIndex': 0
    },
    {
        'name': 'en',
        'locoCode': 'en-US',
        'google_columnIndex': 1
    },
    {
        'name': 'zh-HK',
        'locoCode': 'zh-HK',
        'google_columnIndex': 2
    },
    {
        'name': 'zh-CN',
        'locoCode': 'zh-CN',
        'google_columnIndex': 3
    }
]

# 匹配全量value字符串替换, value完全相等时才替换
replaceValueMap = {
    '{{$NULL$}}': "",  # 空字符串
}

# 增量更新同时同步到local
updatedSynchLocalHansCNAndroidKey = 'zh-Hans-CN'

################### 迁移已完成 ###################
# #GoogleDocs 用于迁移翻译
# token =  'ya29.a0AfH6SMDLTVCL2wxXUyyWdaaGXtTSJfJsmZzWCGHUF2uygwMZu4eMJqz3oC-JoiFJ5WQnef_K8Siwcu65FjYZj2EwEmuSeZwDvnZen7Wf23QcrVMigupcyTuRGfkzkeVyJlT_fHO7z_F0aWPJdGEhaqaVZWM94w'
# #google表格ID
# sheetid = '1vsMVwVzn4I6K-BipbBfmLW4jgBPjR9_jjy4PZ8E0Xdg'
# #google表
# sheetTable = 'translate-ios'
# #key对应的列
# keyColumn = 'B'
# #翻译语言对应的列，B列:key,C列:en,D列:zh-Hans
# range = 'B:E'

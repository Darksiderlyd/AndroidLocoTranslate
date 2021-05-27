# -*- coding: UTF-8 -*-
import ssl
import sys
import common_function
import config
import translate


# 迁移繁体
def migrateSomeLanguage(locale):
    if not config.switchAutoUpdate or locale is None or len(locale) == 0:
        print "config.switchAutoUpdate is false"
        return

    if locale == config.updatedSynchLocalCn or locale == config.updatedSynchLocalEN or locale == config.updatedSynchHantLocal:
        common_function.updateSingleLanguage(locale)
    else:
        print "locale not in zh-CN  or zh-HK or en"

if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    # for i in range(1, len(sys.argv)):
    #     print(sys.argv[i])
    if len(sys.argv) > 1:
        migrateSomeLanguage(sys.argv[1])

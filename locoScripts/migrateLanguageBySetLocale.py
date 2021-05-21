# -*- coding: UTF-8 -*-
import common_function
import config
import translate


# 迁移繁体
def migrateSomeLanguage():
    if not config.switchAutoUpdate:
        return
    common_function.updateSingleLanguage(config.updatedSynchLocalEN)


if __name__ == '__main__':
    migrateSomeLanguage()

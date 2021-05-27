# -*- coding: UTF-8 -*-
import os
import ssl

import common_function
import distutils.dir_util


def downloadWriteToLocal():
    common_function.downloadStringsDispatchStringToModuleWhiteList()


if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    downloadWriteToLocal()

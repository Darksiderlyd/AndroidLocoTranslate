# -*- coding: UTF-8 -*-
import json
import os
import shutil
import ssl
import time
import zipfile
from string import Template

ICONFONT_JSON = 'iconfont.json'
ICONFONT_TTF = 'iconfont.ttf'
ICONFONT_DIR_PREFIX = 'font_'
DOWNLOADD_FILE_NAME = 'download.zip'
CLASS_FILE_PATH = 'libpierui/src/main/java/global/longbridge/libpierui/iconfont/'
PIERUI_ASSETS = 'libpierui/src/main/assets/fonts'
PIERUI_ICONFONT_CLASS_NAME = 'IconFont.java'
ICONFONT_ITEM = 'glyphs'

ICONFONT_VERSION = '1.0.0'
PRE_LB = 'lb_'


def downloadAndCreateIconFont():
    # url = 'https://www.iconfont.cn/api/project/download.zip?spm=a313x.7781069.1998910419.d7543c303&pid=1509243&ctoken=NQxh6Ywh9HGhHr7Q_hBmjRNK'
    base_icon_font_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.dirname(base_icon_font_dir)
    print base_icon_font_dir

    iconfont_class_path = os.path.join(base_dir, CLASS_FILE_PATH)
    iconfont_assets_path = os.path.join(base_dir, PIERUI_ASSETS)
    print iconfont_class_path
    iconfont_zip_path = os.path.join(base_icon_font_dir, DOWNLOADD_FILE_NAME)
    print iconfont_zip_path

    try:
        zip_file = zipfile.ZipFile(iconfont_zip_path, "r")
        zip_list = zip_file.namelist()  # 压缩文件清单，可以直接看到压缩包内的各个文件的明细
        for f in zip_list:  # 遍历这些文件，逐个解压出来，
            zip_file.extract(f, base_icon_font_dir)
        zip_file.close()

        fontFile = ''
        listFile = os.listdir(base_icon_font_dir)
        for file in listFile:
            if os.path.isdir(os.path.join(base_icon_font_dir, file)) and file.startswith(ICONFONT_DIR_PREFIX):
                fontFile = file

        print fontFile

        iconfontTTFFile = os.path.join(base_icon_font_dir, fontFile, ICONFONT_TTF)

        if not os.path.exists(iconfont_assets_path):
            print "不存在创建"
            os.makedirs(iconfont_assets_path)

        shutil.copy(iconfontTTFFile, iconfont_assets_path)

        if not os.path.exists(iconfont_class_path):
            os.makedirs(iconfont_class_path)

        iconfontJavaFile = os.path.join(iconfont_class_path, PIERUI_ICONFONT_CLASS_NAME)
        print iconfontJavaFile
        open(iconfontJavaFile, "w")

        iconfontJsonFile = os.path.join(base_icon_font_dir, fontFile, ICONFONT_JSON)
        with open(iconfontJsonFile, 'r') as load_f:
            iconFontJson = json.load(load_f)

        # print iconFontJson[ICONFONT_ITEM]

        createIconFontJavaFile(iconfontJavaFile, iconFontJson[ICONFONT_ITEM])

    except Exception as e:
        print("(失败)"), e
        return e


def createIconFontJavaFile(javafile, iconFontJson=[]):
    templ = Template('''package global.longbridge.libpierui.iconfont;

import com.mikepenz.iconics.Iconics;
import com.mikepenz.iconics.typeface.GenericFont;

/**
* author : yaodonglv
* date : ${iconFontCreateTime}
* desc : IconFont初始化
*/
public class IconFont {

    public static String version = "${iconFontVersion}";

    public static void initIconFont() {
        GenericFont gf = new GenericFont("IconFont", "LongBridge", "${prefix_lb}", "fonts/iconfont.ttf");
        addIcon(gf);
        Iconics.registerFont(gf);
    }

   private static void addIcon(GenericFont gf) {
${iconFontList}
   }
}''')

    iconFontList = ''

    for model in iconFontJson:
        name = model['font_class'].encode('utf-8')
        code = model['unicode'].encode('utf-8')
        name = name.lower()
        name = name.replace(' ', "_")
        name = name.replace('-', "_")
        code = '\u' + code
        # print name
        # print code
        item = "         gf.registerIcon(\"%s\", '%s');\n" % (PRE_LB + name, code)
        iconFontList += item.encode('utf-8')

    # print iconFontList.encode('utf-8')
    updateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    finalJavaFile = templ.substitute(iconFontCreateTime=updateTime, iconFontVersion=ICONFONT_VERSION,
                                     iconFontList=iconFontList,prefix_lb=PRE_LB)

    fo = open(javafile, "w")
    fo.write(finalJavaFile)
    # 关闭打开的文件
    fo.close()


if __name__ == '__main__':
    downloadAndCreateIconFont()

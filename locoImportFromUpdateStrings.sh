#!/bin/bash
# 参数 $1
# 中文: zh-CN
# 英文: en
# 繁体: zh-HK
echo $1

read -n1 -p "请先执行locoUploadCnAndTranslateHKToLoco.sh完成上传，此方法不可以随便使用，只有在迫不得已的时候才能用，将需要更新的strings放到updateStrings.xml中去,需要去config中将switchAutoUpdate=True [Y/N]?" answer
case $answer in
Y | y)
      echo "上传部分文案"
      python -B locoScripts/migrateLanguageBySetLocale.py $1;;
N | n)
     echo "请先执行locoUploadCnAndTranslateHKToLoco.sh完成上传";;
*)
     echo "取消";;
esac


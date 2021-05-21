#!/bin/bash

read -n1 -p "请先执行locoUploadCnAndTranslateHKToLoco.sh完成上传，此方法不可以随便使用，只有在迫不得已的时候才能用，需要去config中将switchAutoUpdate=True [Y/N]?" answer
case $answer in
Y | y)
      echo "上传部分文案"
      python -B migrateLanguageBySetLocale.py;;
N | n)
     echo "请先执行locoUploadCnAndTranslateHKToLoco.sh完成上传";;
*)
     echo "取消";;
esac


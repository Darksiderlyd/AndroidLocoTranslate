#!/bin/bash

read -n1 -p "请先执行locoUploadCnAndTranslateHKToLoco.sh完成上传，你是否已经将最新的添加中文上传到Loco [Y/N]?" answer
case $answer in
Y | y)
      echo "迁移英文"
      python -B locoScripts/migrateEn.py;;
N | n)
     echo "请先执行locoUploadCnAndTranslateHKToLoco.sh完成上传";;
*)
     echo "取消";;
esac


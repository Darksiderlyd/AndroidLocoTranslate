#!/bin/bash

read -n1 -p "你是否已经将最新的添加中文翻译为繁体上传到Loco，会覆盖之前的翻译！！！ [Y/N]?" answer
case $answer in
Y | y)
      echo "迁移英文"
      python -B locoScripts/migrateHKByTranslate.py;;
N | n)
     echo "请先执行locoUploadCnAndTranslateHKToLoco.sh完成上传";;
*)
     echo "取消";;
esac


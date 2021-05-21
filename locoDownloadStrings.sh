#!/bin/bash
cd ..
cp -r libstrings/src/main/res toolsloco/res
cd toolsloco
read -n1 -p "你是否已经将最新添加的中文上传到Loco [Y/N]?" answer
case $answer in
Y | y)
      echo "接下来将继续下载Strings"
      python -B locoScripts/downloadStrings.py;;
N | n)
     echo "请先执行locoUploadCnAndTranslateHKToLoco.sh完成上传";;
*)
     echo "取消";;
esac
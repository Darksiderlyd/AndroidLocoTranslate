#!/bin/bash

# 参数 $1
# 开启上传: 0
# 关闭上传只分析增加修改: 1 或者 不传参数
# 分析结果在log.txt中
echo $1

read -n1 -p "分析新增和修改的string,参数传0开启上传，参数传1或者不传关闭上传，建议第一次不传参或者传1先进行分析，分析结果在log.txt中获取！！！ [Y/N]?" answer
case $answer in
Y | y)
      echo "分析新增和修改"
      python -B locoScripts/updateAndroidStringsChangeAndAdd.py $1;;
N | n)
     echo "请先执行locoUploadCnAndTranslateHKToLoco.sh完成上传";;
*)
     echo "取消";;
esac


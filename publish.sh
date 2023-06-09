#!/usr/bin/env sh

if [ "$1" != "" ]; then
    echo "正在发布分支: " $1
else
    echo "需要指定发布分支"
    exit
fi

echo '开始执行 publish 命令'
# 生成静态文件
echo '执行命令: gitbook build .'
gitbook install
gitbook build

# 进入生成的文件夹
echo "执行命令: cd ./_book\n"
cd ./_book

echo "发布开始: start\n"
git init
git add -A
git commit -m 'release:    publish last version!'
git push -f git@github.com:Windsander/Project_M.git $1:publish
echo "发布完成: https://arikanli.github.io/<REPO>"

# 返回到上一次的工作目录
echo '完成执行 publish 命令'
echo "回到刚才工作目录"
cd -
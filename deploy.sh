#!/usr/bin/env sh

echo '开始执行 deploy 命令'
gitbook install
gitbook build
gitbook server
echo '完成部署.'

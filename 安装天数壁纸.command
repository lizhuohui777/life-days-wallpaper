#!/bin/zsh
set -euo pipefail
cd "$(dirname "$0")"
print '请先使用图形应用选择日期、玩家名字及背景。'
print '本脚本只构建并打开应用，不直接修改登录任务。'
zsh 构建安装包.command --app-only
open "$PWD/dist/人生天数壁纸.app"

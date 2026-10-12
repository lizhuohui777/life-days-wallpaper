# 停用、卸载与设置恢复

1. 退出图形应用，运行 `launchctl bootout "gui/$(id -u)/local.daywallpaper"`；未注册时出现找不到服务提示可忽略。
2. 在系统设置选择其他墙纸，避免删除仍被系统引用的图片。
3. 手动移除 `~/Library/LaunchAgents/local.daywallpaper.plist` 和应用。
4. 根据需要备份后，手动移除 `~/Library/Application Support/DayWallpaper/`。该目录含名字、日期、背景副本、日志及可选配置备份。

兼容清理前的备份为 `wallpaper-store-before-cleanup.plist`。如需回退，先停用任务并保存当前系统墙纸设置。优先在系统设置中重新选择图片。不要把旧备份直接覆盖到不同 macOS 版本或已有新设置的电脑；备份包含当时全部墙纸配置，整体还原可能撤销其他改动。必要时由熟悉 plist 的维护者核对差异后恢复，只操作与本程序相关的条目。

# 开发与源码构建

环境：macOS 13+、Xcode Command Line Tools；测试和源码导出另需 Python 3。以下命令在仓库根目录执行。

```sh
zsh scripts/test.sh
zsh scripts/build.sh --app-only
open dist/人生天数壁纸.app
```

生成 DMG：

```sh
zsh scripts/build.sh
```

输出位于 `dist/`；脚本构建 arm64 / x86_64 通用二进制并进行临时签名，不依赖已安装应用。正式分发需要 Developer ID 签名和 Apple 公证，见[发布说明](RELEASING.md)。

## 文件结构

- `Sources/`：`WallpaperApp.swift` 为设置界面，`DayWallpaper.swift` 为渲染与每日更新，`Shared.swift` 为日期、图片导入及兼容迁移。
- `Resources/`：版本信息 `Info.plist` 和安装包使用说明。
- `Tests/` 与 `.github/`：合成数据测试、CI、问题和 PR 模板。
- `scripts/`：构建、测试、图标和默认背景生成、元数据清理及公开源码导出。
- `docs/` 与 `bonus/`：文档、预览，以及单独授权的附赠照片。

若本机存在 `Resources/background.jpg`，构建时会将其作为默认背景；该文件默认不提交。不存在时自动生成山丘背景。`bonus/` 不被构建脚本读取，用户须自行导入附赠照片。发布构建应从干净源码导出目录执行，避免误打包本机私有图片。

## 安全预览

预览不设置实际桌面，不注册登录任务，不触发兼容清理：

```sh
DAYWALLPAPER_PREVIEW_ROOT="/private/tmp/life-days-preview" \
DAYWALLPAPER_PREVIEW_DATE="2024-01-02" \
"dist/人生天数壁纸.app/Contents/Resources/day-wallpaper" --preview
```

测试脚本使用独立临时目录及合成图片。修改导入、日期或系统迁移行为时，应增加对应行为验证。

## 导出可公开源码

```sh
python3 scripts/export_public_source.py /private/tmp/life-days-public
```

目标目录必须不存在，且位于仓库外。导出只复制白名单中的源码、文档和已授权附赠图，排除 `.git`、应用、DMG、个人设置、原始照片和日志。不要上传上一级私人工作区。

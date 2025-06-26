# IPTV 自动更新

## 功能
- 🌐 从 `sources.txt` 中配置的多个网址抓取 M3U 或 TXT 格式直播源
- 🗂 去重、分类（如 CCTV、体育、电影等）
- 📁 保存为 `result/iptv.m3u`
- ⏱ 每天 UTC 00:00 和 12:00 自动运行并推送至 GitHub 仓库

## 使用方式
1. 将直播源地址添加至 `sources.txt`
2. Commit 并 Push 到仓库
3. GitHub Actions 定时执行，会生成并更新 `result/iptv.m3u`
4. 可手动触发 workflow（Actions -> Run workflow）

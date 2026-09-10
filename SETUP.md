# 主页维护说明

主页展示密态数据库研究、RMDB、信息安全和南开大学课程课件与学习资料。私有研究不公开仓库名称或链接。

## 图片

主视觉、RMDB 模块图、工作台贴纸、Snake 和页脚位于 `assets/`。英文打字动画和技术图标继续使用原来的外部服务。

活动展示仅保留 Snake，不生成贡献热力图。另有独立的公开仓库统计卡，展示 Star 总数、公开仓库数和 Fork 总数。

## 自动更新

将修改提交并推送到 `main`。工作流 **Update profile visuals**：

- 工作流或统计脚本变更推送至 main 后运行。
- 每天 UTC 00:17（北京时间 08:17）运行，可在 Actions 手动启动。
- 使用自动提供的 `GITHUB_TOKEN`，无需额外 Secret。
- 生成桌面/手机统计卡与深色/浅色 Snake，检查 SVG 后一起提交到 main。
- 生成失败时保留上一版图片；图片更新不会递归触发工作流。

分支保护若限制机器人写入，需要让更新方式符合仓库规则。GitHub 可能在公开仓库长期无活动后停用定时任务，可在 Actions 重新启用。

## 原 Snake 问题

旧工作流给 `crazy-max/ghaction-github-pages@v4` 传入了 `branch`，插件要求的参数是 `target_branch`。图片实际生成在默认的 gh-pages 分支，README 却访问 output，因而返回 404。现在直接将 Snake 保存到 main 的 assets 中。

[Snake 配置参考](https://github.com/Platane/snk)

## 统计与徽章

`python scripts/generate_stats.py` 读取账号名下的公开仓库，分页汇总 `stargazers_count` 和 `forks_count`。Star 与 Fork 指这些仓库收到的数量，不是账号收藏或 Fork 别人的数量；包含名下的公开 Fork 仓库，不包含私有仓库。统计卡标有 UTC 更新时间。请求失败会报错并保留旧图，不将错误显示为零。

`python scripts/build_badges.py` 生成 `assets/badges/` 下的标准矩形徽章。README 按单个徽章引用，窄屏可换行。徽章不依赖外部图片接口。

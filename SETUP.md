# 主页维护说明

README 保留密态数据库研究、RMDB 工程实践、南开信息安全课件与学习资料三条主线。私有研究只描述方向，不公开仓库名称或链接；未验证的性能结果不写入主页。

## 图片修复原因

- 原 Snake 发布步骤给 `crazy-max/ghaction-github-pages@v4` 传入了 `branch`，正确参数应为 `target_branch`。因此 2026-09-09 的运行虽然成功，产物实际位于默认的 `gh-pages` 分支，而 README 访问 `output`，返回 404。
- 同次检查中，公共 Stats 服务返回 503，Activity Graph 服务返回 402。
- 新版第 6、7 部分和页脚均引用 `assets/` 中的 SVG，不依赖公共 Vercel 图片接口，也不再依赖产物分支。

## 更新与启用

将 README、assets、scripts 和 `.github/workflows/snake.yml` 一起提交并推送至 `main`。仓库内已包含真实公开数据生成的统计图及本账号成功运行的 Snake 快照，因此无需等首次 Actions 完成即可显示。

工作流名称：**Update profile visuals**。

- 推送工作流或生成脚本变更时自动运行。
- 每天 UTC 00:17（北京时间 08:17）运行，GitHub 排队可能延迟。
- 可在 Actions 中选择该工作流，点击 Run workflow 手动刷新。
- 使用自动提供的 `GITHUB_TOKEN`，不需要新增 PAT 或其他 Secret。
- 四张动态 SVG 全部成功生成并通过 XML 检查后才提交到 `main`；生成失败时线上保留上次快照，失败记录可在 Actions 查看。
- 仅图片更新不会递归触发该工作流。

如果分支保护规则禁止机器人直接写入 main，需要让工作流提交符合仓库规则；请勿为了更新图片关闭保护。公共仓库长期无活动时 GitHub 可能停用定时运行，可在 Actions 重新启用。图片已经入库，停更不会造成破图。

## 数据口径

`python scripts/generate_telemetry.py` 使用 Python 3.13 标准库，读取 GitHub 公开 REST API 与公开贡献日历。

- 仓库数和 Star 数：公开仓库；关注者：公开用户资料。
- 语言：公开非 Fork 仓库的 GitHub 语言字节数，显示前六项，百分比分母为全部语言。没有数据时明确显示空状态，不虚构 C++ 等比例。
- 贡献格子：公开主页日历的强度等级，不等于 commit 数。用户选择公开的匿名私有贡献可能包含在日历里，但不会公开私有仓库名称或内容。
- Active days：日历中强度大于零的日期数。
- 日历 HTML 若变化导致解析异常，脚本报错并保留原图。
- 初始 Snake 快照来自本账号 2026-09-09 成功运行的 gh-pages 产物；后续使用 Platane/snk 自动重新生成。

主页沿用原版赛博主视觉、打字效果与技术徽章。第 6、7 部分及页脚使用仓库内图片。统计口径和维护说明只保留在本文件，不在主页正文展示。

## 上游参考

- [Snake 配置](https://github.com/Platane/snk)
- [原发布 Action 的参数定义](https://github.com/crazy-max/ghaction-github-pages/blob/v4/action.yml)
- [GitHub Actions 定时触发](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)

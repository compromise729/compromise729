# compromise729 GitHub Profile README · v3

## 本次修正

### 1. `.github` 已确认包含在压缩包中

压缩包内部结构为：

```text
README.md
SETUP.md
assets/
└── cyber-db-core.svg
.github/
└── workflows/
    └── snake.yml
```

`snake.yml` 用于自动生成 GitHub Contribution Snake。

### 2. 南开大学信息安全资料区已精简

不再列出任何具体课程名称，只概括为：

- 课程课件
- 学习资料
- 个人笔记
- 复习材料
- 实验与工程记录

公开仓库：

https://github.com/compromise729/NKU-InformationSecurity

## 部署

创建公开仓库：

```text
compromise729/compromise729
```

将压缩包中的所有文件和目录完整上传。

随后进入：

```text
Actions
→ Generate contribution snake
→ Run workflow
```

首次运行完成后会生成 `output` 分支，README 底部的 Snake 动画即可显示。

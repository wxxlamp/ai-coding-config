# AI Coding Config

Claude Code 配置、技能与 Codex Plugin 源码集合，用于提升 AI 辅助编程效率。

## 目录结构

```
.claude/
├── settings.json          # 全局配置与 hooks
├── settings.local.json    # 本地个人配置（未纳入版本控制）
├── hooks/                 # Claude Code 钩子脚本
│   └── session-end/
│       └── regeneration-readme.sh  # 提交后自动更新 README
└── skills/                # 技能集合
    ├── skill-creator/     # 官方技能创建与评估工具
    ├── img-uploader/      # 图片上传工具
    └── skill-create/      # 技能创建模板（基础版）
plugins/
└── yuque-multichannel-publisher/  # 语雀多平台发布 Codex Plugin
```

## 技能说明

| 技能 | 用途 |
|------|------|
| `skill-creator` | 创建、优化、评估技能性能的完整工具链 |
| `img-uploader` | 上传图片到图床（支持 Imgur、sm.ms、GitHub + jsDelivr） |
| `skill-create` | 快速创建新技能的基础模板 |

## Codex Plugin

| 插件 | 用途 |
|------|------|
| `yuque-multichannel-publisher` | 将语雀文章加工为博客、微信公众号和小红书发布包，支持断点恢复、质量检查、公众号官方草稿投递和小红书安全预览填充 |

插件源码位于 `plugins/yuque-multichannel-publisher/`。其中不包含账号凭据、Cookie、文章项目状态或用户语气档案；外部 `md2wechat` 与 `XiaohongshuSkills` 适配器也不随仓库分发。

## 使用方法

### 1. 克隆配置

```bash
git clone git@github.com:wxxlamp/ai-coding-config.git
cd ai-coding-config
```

### 2. 应用到项目

将 `.claude/` 目录复制到目标项目：

```bash
cp -r .claude /path/to/your/project/
```

### 3. 添加本地配置

创建 `.claude/settings.local.json` 存放个人敏感信息：

```json
{
  "project": {
    "name": "your-project-name"
  }
}
```

> `settings.local.json` 已加入 `.gitignore`，不会提交到仓库。

## Hooks 说明

- **PreToolUse:Bash** - 执行 Bash 命令前触发，用于自动化任务
- **Notification** - Claude Code 需要用户注意时触发系统通知
- **PostCommit** - Git 提交后自动执行（通过 `session-end` 模拟）

## License

MIT License - 详见 [LICENSE](LICENSE) 文件

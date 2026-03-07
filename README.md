# AI Coding Config

个人 AI 编程工具的配置文件集合，主要用于 [Claude Code](https://claude.ai/code) 等 AI 辅助编程工具。

## 包含内容

### 1. Claude Code 配置 (`.claude/`)

- **`settings.local.json`** - Claude Code 本地配置文件（包含个人设置，已排除在版本控制外）
- **`skills/`** - 自定义技能集合
  - `skill-create` - 创建新技能的工具和模板
  - `yuque-doc-downloader` - 语雀文档下载工具

## 使用方法

### 克隆到本地

```bash
git clone git@github.com:wxxlamp/ai-coding-config.git
```

### 配合 Claude Code 使用

将 `.claude/` 目录复制到你的项目根目录，Claude Code 会自动加载其中的配置和技能。

```bash
cp -r .claude /path/to/your/project/
```

### 添加个人配置

在项目目录下创建 `.claude/settings.local.json` 来覆盖默认设置：

```json
{
  "project": {
    "name": "你的项目名称"
  }
}
```

## 注意事项

- `settings.local.json` 包含个人敏感信息，已添加到 `.gitignore`，不会提交到仓库
- 每个项目的具体配置请在本地单独维护

## License

MIT License - 详见 [LICENSE](LICENSE) 文件

# Obsidian 双 Agent 协作 Vault

> 两个 AI agent，一个 Obsidian vault，git 同步，冲突走一手 docs 仲裁。

[English](./README.md) · [架构](./docs/01-architecture.zh-CN.md) · [部署](./docs/02-setup.zh-CN.md) · [协作规范](./docs/03-collaboration.zh-CN.md) · [故障排查](./docs/04-troubleshooting.zh-CN.md)

---

## 这是什么

一套让 **两个独立 AI agent 在同一个 Obsidian vault 里协作** 的蓝图——双方读、写、互审，git 留全审计轨迹。

只要 agent 能：
- 跑 shell 命令读写文件
- 提交 git
- 读 markdown

就可以接入。已在 **Hermes Agent**（`default` + `second` 双 profile）上跑通，pattern 与 agent 无关，Claude Code / Cursor / OpenCode / 自研 agent 都能照搬。

## 为什么需要

单 agent 研究的死穴：编造听起来对但其实错的细节，没人 catch。加第二个 agent，**独立提示词、共享可写知识库**，幻觉就会变成可见的分歧——你拿一手 docs 仲裁就行。

驱动这个 repo 的真实案例：两个 agent 调研永续 DEX 费率，A 写报告，B 审计，**B 找到 4 处费率错误**（Lighter rebate 符号反了、HL VIP0 maker rebate 错、trade.xyz Standard 档错、Aster USD1 行错）。没有 B，这 4 个错就 ship 出去了。

## 架构（90 秒看完）

```
┌─────────────────┐         ┌─────────────────┐
│   Agent A       │         │   Agent B       │
│  （比如 VPS-1）  │         │  （比如 VPS-2）  │
└────────┬────────┘         └────────┬────────┘
         │                           │
         │  git push / pull          │  git push / pull
         ▼                           ▼
        ┌──────────────────────────────┐
        │   GitHub（私有 repo）        │
        │   = 唯一真相源                │
        └──────────────────────────────┘
                      ▲
                      │  Obsidian Git 插件
                      │  （5 分钟自动 pull，10 分钟自动 push）
                      │
        ┌──────────────────────────────┐
        │   你的笔记本                  │
        │   Obsidian app 读 vault       │
        └──────────────────────────────┘
```

每个 agent 用 **自己的 author 身份** commit。每段文字标 `[AGENT-A]` / `[AGENT-B]` / `[BOTH]`。冲突走一手 docs（官方 API、RFC、源码）裁决，不靠嘴硬。

## 5 分钟速通

```bash
# 1. GitHub 建一个私有 repo（名字随意，agent-vault / ops-notes 都行）

# 2. 在 Agent A 的机器上
git clone git@github.com:you/your-vault.git
cd your-vault
cp /path/to/this-repo/templates/AGENTS.md ./AGENTS.md
cp /path/to/this-repo/templates/.gitignore ./.gitignore
git add . && git commit -m "init: dual-agent rules" && git push

# 3. 在 Agent B 的机器上
git clone git@github.com:you/your-vault.git
# （用刚 push 的同一份 AGENTS.md）

# 4. 在你笔记本上
git clone git@github.com:you/your-vault.git "$HOME/Documents/Obsidian Vault"
# Obsidian 打开这个文件夹 → 装 Obsidian Git 社区插件
# 设置：自动 pull 5 分钟，自动 push 10 分钟
```

两个 agent + 你的笔记本同时落到同一份 vault。详细步骤见 [docs/02-setup.zh-CN.md](./docs/02-setup.zh-CN.md)。

## 协作规范（最关键的部分）

三条规则，背下来：

1. **每段都要标作者**：`[AGENT-A]` / `[AGENT-B]` / `[BOTH]`，不能有裸文。
2. **不动对方的标签块**。要补充就在下面新起一段，或用 `[AGENT-B audit]:` 行内备注。
3. **冲突走一手 docs**。A 说费率 4.5bps，B 说 9.0bps——谁声音大都没用，打开官方 docs URL，贴原文，引来源。

完整冲突协议 + 写区规则见 [docs/03-collaboration.zh-CN.md](./docs/03-collaboration.zh-CN.md)。

## 仓库结构

```
.
├── README.md                    英文版
├── README.zh-CN.md              （你在这里）
├── docs/
│   ├── 01-architecture.md       架构与原理
│   ├── 02-setup.md              VPS + 本地全流程
│   ├── 03-collaboration.md      标签 + 冲突仲裁
│   └── 04-troubleshooting.md    git 冲突 / 插件问题
├── templates/
│   ├── AGENTS.md                丢进 vault 根目录
│   ├── .gitignore               Obsidian 推荐忽略项
│   └── obsidian-git-settings.md 插件配置片段
└── LICENSE                       MIT
```

## 真实案例

这套 workflow 在大约 6 小时内产出了一份 **12 家永续 DEX 费率 + 空投横向报告**，由两个独立 Hermes agent 共写：A 起稿、B 审计、冲突走官方 docs。最终报告有 80+ 引用 URL，每段都有作者标注。

两个 agent 在 4 个费率档上分歧——一手 docs 全部仲裁完，4 处都不是 A 原本的数字。

## License

MIT 协议——随便 fork、随便 ship、欢迎写文章传播。

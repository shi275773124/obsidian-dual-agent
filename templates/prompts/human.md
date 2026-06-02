# Human Operator Prompt

你是 Human Operator，负责最终仲裁。

你的职责：
1. 查看 `research/04-conflicts.md` 里的 `[CONFLICT]` 区
2. 要求 A / B 回到一手资料提供证据
3. 判断最终采用哪个结论
4. 把已仲裁内容标为 `[BOTH]`，写入 `research/05-resolutions.md`
5. 在 `logs/decisions.md` 中保留关键决策记录

不要逐字重写报告。  
重点处理分歧、证据和发布决策。

---

## 仲裁流程

1. 打开 `research/04-conflicts.md`，找所有 `[CONFLICT]` 条目
2. 对每个 conflict：
   - 要求 A / B 给出一手资料链接（官方 docs、API、源码）
   - 自己验证或要求 Agent 验证
   - 写下仲裁结论到 `research/05-resolutions.md`
3. 仲裁完成后，更新原始内容为 `[BOTH]`
4. 在 `logs/decisions.md` 记录关键决策（为什么选 A / 为什么选 B）
5. 提交 commit，格式：`resolve(human): <描述>`

## 发布标准

- 最终报告里所有段落必须是 `[BOTH]` 或 `[RESOLUTION]`
- 没有未解决的 `[CONFLICT]`
- 没有 `[NEEDS-AUDIT]` 或 `[NEEDS-SOURCE]` 的内容进入报告
- Git history 完整，可以追溯每个结论从哪里来

## 一手资料定义

可以作为仲裁依据：
- 官方文档 URL（对方平台的官方网站）
- 官方 API 响应（直接调用返回的数据）
- 源代码（合约代码、开源代码库）
- RFC / 白皮书 / 官方公告
- 原始数据（自己获取的 raw data）

不能作为仲裁依据：
- 博客文章（包括官方博客的总结性内容）
- 推文 / 社交媒体
- 二手分析报告
- 其他 AI 的输出

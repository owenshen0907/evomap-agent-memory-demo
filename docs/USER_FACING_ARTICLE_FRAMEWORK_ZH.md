# 面向普通用户的 EvoMap 文章框架

图文版飞书文档：<https://ccnjn62goe9e.feishu.cn/docx/So4SdLJOFoz1dvxMP49c6x1gnlh>

## 标题

**一次真实经验复现：EvoMap 如何让 Agent 在新线程里少绕弯**

## 核心定位

这篇文章不是协议说明，也不是演示真实上传、改库或发布任务。它面向普通 coding-agent 用户，讲一个更容易感知的问题：

> Skill 在具体场景里很好用，但类似任务稍微变化后，旧 Skill 里的约束可能变成摩擦。EvoMap / Evolver 的价值，是让 Agent 从真实使用、纠正和验证里沉淀经验，在新线程里先 recall 再回答。

## 读者

- 正在使用 Codex、Cursor、Claude Code 的独立开发者。
- 已经在写 Skill / Rules / CLAUDE.md，但发现规则越补越厚的人。
- 经常在新线程里反复解释项目背景、服务器、文件服务、数据库和历史约定的人。
- 想知道 EvoMap 怎么接入、怎么生效、怎么验证的人。

## 推荐目录

1. **Skill 很好用，但不应该越写越厚**
2. **普通用户怎么接入 EvoMap**
3. **它为什么会对 Agent 起作用**
4. **一个轻量真实场景：日语工作坊和跟读视频互相反哺**
5. **同一句需求，两种起手式**
6. **开源 demo：把它当成接入后的验证信号**
7. **怎么判断 EvoMap 真的起作用**
8. **结论**

## 各节作用

### 1. Skill 很好用，但不应该越写越厚

先从用户熟悉的 Skill 讲起。承认 Skill 在稳定流程里很有用，但指出它的边界：类似任务变化后，旧 Skill 的约束可能会影响新任务。不要一上来讲 Gene / Capsule。

### 2. 普通用户怎么接入 EvoMap

提前说明接入方式：

- Codex：安装 / 使用 `evomap-agent-economy` skill。
- Cursor：把规则放入 `.cursor/rules`。
- Claude Code：写入 `CLAUDE.md` 或使用对应 skill。
- Evolver hooks：`evolver setup-hooks --platform=codex|cursor|claude-code`。

同时强调首次试用应关闭自动购买、自动发布和验证者自动能力，先走本地、可审查、零自动消费。

### 3. 它为什么会对 Agent 起作用

解释机制，但保持普通用户语言：

- hooks 捕获会话开始、工具调用、错误、用户纠正、会话结束等信号；
- Evolver 从信号里提炼 Gene；
- 通过测试、执行记录或人工确认形成证据；
- 把正向经验或错误示例包装成 Capsule；
- 新线程里 Agent 先 recall，再回答。

### 4. 一个轻量真实场景

保留真实经验，但压缩成一个例子：

> 日语工作坊网站已经有 17000 多个日语单词和 17000 多张照片。跟读视频要从网站词库按场景筛词，生成视频合集、例句图片和音频；这些视频产物又要反哺回网站展示。

不要展开所有服务器、数据库和项目细节。场景只服务于“两个具体工作面互相借用经验”这条主线。

### 5. 同一句需求，两种起手式

展示用户最容易感知的差异：

- 普通 Agent：先反问网站表结构、照片/音频位置、场景分类、视频脚本入口、回写方式。
- EvoMap Agent：先 recall 日语工作坊 ↔ 跟读视频反馈循环 Gene / Capsule，再给 `scene_word_set + video_collection_manifest + word_learning_assets` 的最小复现方案。

### 6. 开源 demo：接入后的验证信号

强调 demo 是纯文字验证，不执行生产任务。

验证命令：

```bash
python3 demo.py
python3 scripts/validate_recall.py
python3 -m unittest discover
```

重点解释 `scripts/validate_recall.py`：

- 模拟历史线程；
- 模拟 UI / 视频音乐等干扰线程；
- 在新线程里提出相似需求；
- 命中正确 Gene / Capsule 后输出 `PASS`。

### 7. 怎么判断 EvoMap 真的起作用

判断标准：

- 是否减少基础背景反问；
- 是否能避开干扰信息；
- 是否能复用已验证策略；
- 是否能保持必要安全确认；
- 是否让 Agent 更快进入最小实现方案。

## 图片规划

建议使用 6 张图：

| 位置 | 图片 | 作用 |
| --- | --- | --- |
| Skill 边界之后 | `11-cross-thread-experience-reuse-zh.png` | 说明经验从多线程进入新线程 |
| 接入方式 | `09-install-architecture-zh.png` | 说明 EvoMap / hooks / Hub 的关系 |
| 工作原理 | `04-evolver-signal-gene-capsule-zh-v2.png` | 说明 Signal / Gene / Evidence / Capsule |
| 普通 Agent | `05-normal-agent-question-path-zh.png` | 展示没有 recall 时的反问 |
| EvoMap Agent | `06-evolved-direct-path-zh.png` | 展示 recall 后直达方案 |
| Demo 验证 | `07-test-evidence-zh-v2.png` | 展示自动化验证证据 |

## 篇幅建议

- 总字数：2200 到 3200 字。
- Skill 边界与用户痛点：20%。
- 接入方式和工作原理：25%。
- 轻量场景：15% 以内。
- 前后效果对比：20%。
- demo 证据：15%。
- 结论：5%。

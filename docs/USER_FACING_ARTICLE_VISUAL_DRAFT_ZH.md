# 一次真实经验复现：EvoMap 如何让 Agent 在新线程里少绕弯

飞书版本：<https://ccnjn62goe9e.feishu.cn/docx/So4SdLJOFoz1dvxMP49c6x1gnlh>

开源 demo：<https://github.com/owenshen0907/evomap-agent-memory-demo>

> 这篇文章想讲一个很具体的问题：Skill 很适合解决明确、稳定的任务，但当类似任务稍微变化，旧 Skill 里的假设和约束就可能变成新的摩擦。EvoMap / Evolver 要解决的，不是把所有规则塞进更长的 Skill，而是让 Agent 从多次真实使用里识别信号、提炼经验，并在新线程里先 recall 再回答。

## Skill 很好用，但不应该越写越厚

我现在会给 Codex、Cursor、Claude Code 配一些 Skill。它们在具体场景里非常好用：比如固定的视频生成流程、某个项目的发布检查、某类文档整理、某个素材上传步骤。

问题出现在“类似但不完全相同”的任务里。

一个 Skill 往往会写清楚触发条件、操作步骤、目录约定、安全边界和输出格式。对原场景来说，这些约束很有价值；但当任务只变化一点，例如从“给网站上传素材”变成“让网站、App、视频流水线共用素材”，原来的约束就可能开始影响判断。

这时常见做法是继续补 Skill：加一个例外、加一段说明、加一个新分支。短期有效，但长期会让 Skill 变厚，也会让 Agent 更难判断“这次到底该套哪一段规则”。

我想要的不是每次都手动维护一份越来越复杂的 Skill，而是让 Agent 在使用 Skill、被用户纠正、通过验证之后，能把其中真正稳定的经验沉淀下来。

![多线程经验如何被 EvoMap 复用](images/mainline-gpt-image-2/zh/11-cross-thread-experience-reuse-zh.png)

这就是我看 EvoMap 的入口：它不是替代 Skill，而是让 Skill 背后的经验可以继续进化。

## 普通用户怎么接入 EvoMap

EvoMap 的接入可以先理解成两层。

第一层是让 Agent 知道“什么时候该使用 EvoMap / Evolver”。在 Codex 里可以安装 `evomap-agent-economy` 这类 Skill；在 Cursor 里可以放到 `.cursor/rules`；在 Claude Code 里可以写进 `CLAUDE.md` 或使用对应 Skill。它的作用是告诉 Agent：遇到 EvoMap、Evolver、Skill 优化、经验沉淀、Gene / Capsule、发布或信用消耗相关任务时，先读取这套规则，并遵守安全默认值。

第二层是 Evolver 的运行时接入。当前 CLI 可以用 hooks 接入常见 coding agent：

```bash
evolver setup-hooks --platform=codex
evolver setup-hooks --platform=cursor
evolver setup-hooks --platform=claude-code
```

首次试用时，我建议先保持本地、可审查、零自动消费：

```bash
export EVOLVER_ATP_AUTOBUY=off
export ATP_AUTOBUY_DAILY_CAP_CREDITS=0
export ATP_AUTOBUY_PER_ORDER_CAP_CREDITS=0
export EVOLVER_AUTO_PUBLISH=false
export EVOLVER_VALIDATOR_ENABLED=false
```

![EvoMap 接入 Agent 的方式](images/mainline-gpt-image-2/zh/09-install-architecture-zh.png)

这样接入后，Evolver 不是在替你偷偷改规则，也不是自动花费 credits。更合理的第一步是：让它从本地任务里识别信号，生成可审查的经验资产，等你确认后再固化或发布。

## 它为什么会对 Agent 起作用

普通 Skill 更像一份“操作说明”。Agent 读到它，就按里面的流程做事。

Evolver 处理的是另一层：任务过程中不断出现的信号。

这些信号可能来自几类地方：

- 用户反复纠正同一个问题。
- Agent 在相似任务里反复卡住。
- 某个方案通过了测试或人工确认。
- 某个 Skill 的限制在新任务里暴露出不适用。
- 某个错误做法被证明以后应该避免。

Evolver 会把这些信号提炼成 Gene，也就是可复用的策略；再用验证结果、执行记录或人工确认形成证据；最后把某个 Gene 的正向经验或错误示例包装成 Capsule。

![Evolver 如何把信号变成胶囊](images/mainline-gpt-image-2/zh/04-evolver-signal-gene-capsule-zh-v2.png)

所以它对 Agent 的影响不只是“多记住一点聊天记录”。更关键的是，新线程开始时，Agent 可以先拿到相关 Gene / Capsule，再决定怎么回答。

这会改变起手式：

- 以前：先问一堆基础背景。
- 现在：先说明命中的经验，再基于经验给方案，只在真实高风险动作前确认。

## 一个轻量真实场景：素材发布 Skill 遇到变化

我的真实场景可以压缩成一句话：

我有日语学习网站、两个 App 和一条短视频流水线，它们都要复用同一批单词、语法、音频、插图素材。

一开始，某个素材发布 Skill 可能只服务于一个网站流程。它知道素材放哪里、URL 怎么写、生成后怎么更新页面。只看这个场景，Skill 很好用。

后来任务变了：同一批 N5 单词卡的音频和插图，不只是给网站用，还要给 App 和视频流水线复用；国内用户和海外用户的访问路径也可能不同。

这时旧 Skill 里如果隐含了“把完整 URL 写进数据库”或“只面向网站路径组织素材”的假设，就会影响新任务。正确经验应该被抽出来：

> 数据库保存稳定的 `object_key` 和校验信息；素材访问 URL 由 `AssetUrlResolver(region, object_key)` 动态生成；网站、App、视频流水线共用 `asset_manifest`，不要各自维护一套路径规则。

这个场景本身不需要占据文章太多篇幅。它只是用来说明：很多长期项目里的问题，不是 Agent 不会写代码，而是它不知道哪些经验已经被验证过，哪些 Skill 假设已经不适合新变化。

## 同一句需求，两种起手式

我用一个最小需求来复现这个差异：

```text
我要给 N5 单词卡生成一批音频和插图，上传到 OSS，并让网站、两个 app、视频剪辑流水线都能复用。国内用户走国内 OSS/CDN，海外用户走海外加速。你帮我设计并落地最小实现。
```

没有 EvoMap 的 Agent 很可能先问：

- 国内和海外服务器分别是什么角色？
- OSS 桶、CDN 域名、签名规则是什么？
- 网站、App、视频流水线分别读哪里？
- 素材 URL 是直接存数据库，还是运行时生成？
- 视频流水线是读数据库、CSV、JSON manifest，还是直接扫 OSS？

这些问题不是错。一个没有历史经验的 Agent 确实应该问清楚。

![普通 Agent 会先反问基础上下文](images/mainline-gpt-image-2/zh/05-normal-agent-question-path-zh.png)

但如果 Evolver 已经从过去线程里沉淀了 Gene / Capsule，Agent 应该先这样起手：

> 我先复用之前沉淀的共享素材经验：用 `asset_manifest` 作为共同事实源，数据库只保存 `object_key` 和校验信息，不保存固定完整 URL，再用 `AssetUrlResolver` 按国内 / 海外区域生成访问地址。

然后它可以直接给最小实现路径：选少量 N5 单词做垂直切片，生成音频和插图，上传并校验 hash，写入 manifest，API 返回国内和海外两套访问地址，视频流水线消费 manifest snapshot。

![接入 EvoMap 后，Agent 先复用经验再给方案](images/mainline-gpt-image-2/zh/06-evolved-direct-path-zh.png)

它仍然应该确认两类真实风险：是否允许写数据库 migration，是否允许使用当前环境里的 OSS 凭证执行真实上传。减少绕弯不等于取消安全确认。

## 开源 demo：把它当成接入后的验证信号

我为这次经验做了一个开源 demo。它不是为了真的上传素材、改数据库或跑视频任务，而是作为接入 EvoMap 后的一个验证信号：

> 在多个模拟线程里输入相对复杂的信息，再混入一些干扰线程，最后在新线程里提出相关需求，看 Agent 是否能 recall 正确的 Gene / Capsule，并给出正确方向。

你可以这样运行：

```bash
git clone https://github.com/owenshen0907/evomap-agent-memory-demo.git
cd evomap-agent-memory-demo
python3 demo.py
python3 scripts/validate_recall.py
python3 -m unittest discover
```

`demo.py` 会展示三类内容：

- `SIMULATED_SOURCE_THREADS`：历史线程里的 Skill 适配、用户纠正和验证信号。
- `DISTRACTOR_THREADS`：UI 配色、视频片头音乐这类相近但不该影响本任务的干扰信息。
- `NEW_THREAD_WITH_EVOMAP_RECALL`：新线程里先 recall，再给方案。

`scripts/validate_recall.py` 是更明确的自动化验证。它会构造一个带干扰信息的新线程 query，并在命中共享素材 Gene 和正向 Capsule 后输出 `PASS`。

![开源 demo 用来复现经验沉淀与新线程复用](images/mainline-gpt-image-2/zh/07-test-evidence-zh-v2.png)

这个 demo 的意义不是证明生产任务已经成功，而是证明一个更前置的能力：Agent 能否从历史线程和干扰信息中，取回这次真正需要的经验。

## 怎么判断 EvoMap 真的起作用

我会用几个很普通的指标判断它是否有效。

| 判断点 | 没有 EvoMap 时 | 接入 EvoMap 后 |
| --- | --- | --- |
| Skill 遇到变化 | 继续补规则，或让 Agent 套错旧约束 | 从历史使用中提炼更稳定的 Gene |
| 新线程起手式 | 先反问基础背景 | 先说明命中的经验 |
| 干扰信息 | 可能被 UI、视频等相近上下文带偏 | 能召回与当前需求真正相关的 Capsule |
| 方案输出 | 容易泛泛而谈 | 直接进入最小实现路径 |
| 安全边界 | 可能乱问或漏问 | 只确认写库、上传、发布等高风险动作 |

对普通用户来说，这些指标比“协议有没有完整跑通”更直观。因为我们最先需要看到的是 Agent 行为变化：少反问、少纠结、少重复踩同一个坑。

## 结论

Skill 仍然重要。它适合把明确、稳定的操作流程交给 Agent。

但长期使用 coding agent 后，真正消耗人的往往不是写第一个 Skill，而是不断处理“类似但有变化”的任务。每次都补 Skill，会让规则越来越重；完全不补，又会让 Agent 继续从零开始。

EvoMap / Evolver 的价值在这里变得清楚：它让 Agent 从使用过程里识别信号，把稳定经验提炼成 Gene，把被验证过的正向经验或错误示例包装成 Capsule。这样下一个新线程里，Agent 不只是读一份固定说明，而是可以先 recall 已经验证过的经验，再进入方案。

对我来说，这就是“少绕弯”的含义：不是让 Agent 擅自做更多事，而是让它更快站到正确经验上。

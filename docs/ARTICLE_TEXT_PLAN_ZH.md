# 文章文字版规划：一次真实经验复现：EvoMap 如何让 Agent 在新线程里少绕弯

> 状态：规划稿。目标是先把文章节奏、场景、验收方式和图片位置定下来，后续再重画图片。

## 这版要解决的问题

上一版太短，读者能看到“EvoMap 可以减少绕弯”，但看不到三件事：

1. **怎么接入**：安装方式应该更像 `evomap-agent-skill` 仓库的 README，而不是手写复杂安装教程。
2. **真实场景**：日语工作坊和跟读视频之间的互相反哺要讲清楚。
3. **验收效果**：读者要看到 demo 到底验证了什么，不只是看到一条 `PASS`。

这一版的定位：

> 普通用户先知道怎么让 Agent 帮自己接入 EvoMap，再通过一个真实但很小的场景，看见“历史线程经验如何在新线程里被 recall 并产生效果”。

## 推荐文章结构

### 1. 开头：Skill 好用，但新线程仍然会绕弯

重点不要讲协议，先讲用户感受：

- 我会给 Codex / Cursor / Claude Code 配 Skill。
- Skill 对稳定流程很好用。
- 但任务稍微变化后，Skill 里的旧约束可能影响新任务。
- 长期项目里，真正累的是每个新线程都要重新解释背景。

建议正文：

> Skill 能把“固定怎么做”交给 Agent，但它不能天然知道哪些经验在别的线程里已经被验证过。EvoMap / Evolver 要解决的是后一件事：让 Agent 把任务里的有效经验沉淀下来，在新线程里先 recall，再回答。

配图建议：

- **图 1：Skill 和 Evolver 的边界**
- 内容：左边是 Skill 固定流程，右边是 Evolver 从多个线程提炼经验，中间标出“类似任务发生变化”。

### 2. 接入方式：直接让 Agent 按仓库说明安装

参考 `evomap-agent-skill` 仓库，写得更简单：

第一步，安装 Evolver：

```bash
npm install -g @evomap/evolver
evolver --help
```

第二步，在项目里启用 hooks：

```bash
evolver setup-hooks --platform=cursor
evolver setup-hooks --platform=claude-code
evolver setup-hooks --platform=codex
```

第三步，可选安装 agent guide skill：

```bash
npx skills add owenshen0907/evomap-agent-skill -g -y
```

更面向普通用户的写法：

```text
请参考 https://github.com/owenshen0907/evomap-agent-skill，
帮我在当前机器安装 @evomap/evolver，
在当前项目里配置对应平台的 hooks，
并保持自动购买、自动发布和 credits 消耗关闭。
```

这里不要展开 A2A、GEP、Hub、credits 市场。只保留一句：

> 第一次使用先保持本地、可审查、零自动消费。真正发布、购买或接 bounty 之前，都需要用户确认。

配图建议：

- **图 2：三步接入**
- 内容：安装 Evolver → setup hooks → 可选安装 skill。
- 图中标出 Cursor / Claude Code / Codex 三个入口。

### 3. 场景：日语工作坊和跟读视频互相反哺

这一节要比上一版更具体，但不要铺开服务器和 App。

建议正文：

> 我的日语工作坊网站最初有 17000 多个日语单词。为了让单词更好理解，我给这些词生成了 17000 多张照片。后来我想继续做跟读视频合集：按场景筛选单词，生成适合用户跟读的视频。
>
> 这个过程不是单向的。网站给视频提供词库、照片和音频；视频生成过程中产生的场景标签、例句图片和旁白音频，又应该反哺回网站展示。

用一个小表讲清楚：

| 工作面 | 已有内容 | 产生的新价值 |
| --- | --- | --- |
| 日语工作坊网站 | 17000+ 单词、照片、读音、解释 | 给视频提供稳定 `word_id` 和素材 |
| 跟读视频 | 按场景筛词，生成合集 | 产出场景、例句图片、旁白音频 |
| 反哺网站 | 接收视频产物 | 单词页展示更丰富 |

核心经验一句话：

> 网站的 `word_id` 是事实源；视频读取 `scene_word_set`；视频生成的场景、例句图片和音频写入 `word_learning_assets`，再回到网站展示。

配图建议：

- **图 3：日语工作坊 ↔ 跟读视频反馈循环**
- 内容：网站词库 → 场景筛词 → 跟读视频 → 例句图片/音频/场景标签 → 网站单词页。

### 4. 没有 EvoMap：Agent 会合理地反问

这一节要让读者看到“普通 Agent 不是笨，而是没有继承历史经验”。

固定 prompt：

```text
日语工作坊网站已经有 17000 多个日语单词和对应照片。
我想按场景筛选一批词，生成跟读视频合集；
视频生成过程中会产生单词场景、例句图片和音频，
这些又要反哺回网站展示。你帮我设计一个最小复现流程。
```

普通 Agent 可能会问：

- 日语工作坊的单词表结构是什么？
- 17000 张照片和已有音频在哪里？
- 场景分类是已有字段，还是需要重新生成？
- 跟读视频脚本从数据库、CSV、JSON，还是网站接口读取？
- 视频生成的例句图片和音频要回写到网站哪里？

这一节的结论：

> 这些问题合理，但如果网站线程、视频线程和反馈规则线程里已经反复解释过，Agent 每次都重新问，就说明经验没有跨线程留下来。

配图建议：

- **图 4：普通 Agent 的新线程起手式**
- 内容：新线程 prompt → 五个反问 → 用户重复解释。

### 5. 接入 EvoMap 后：先 recall，再给最小方案

这里展示理想回答，不要只写抽象结论。

建议正文：

> 接入 EvoMap 后，Agent 不应该先问完整背景，而应该先 recall 到两个资产：
>
> - `Gene workshop-shadowing-feedback-loop`
> - `Capsule workshop-shadowing-positive-feedback-case`

然后给出最小方案：

1. 以日语工作坊 `word_id` 为主键，不复制一套视频专用单词表。
2. 从 17000 多个单词里筛一个最小场景，例如餐厅。
3. 生成 `scene_word_set_restaurant.json`。
4. 为 3 个词生成例句、例句图片和跟读音频。
5. 生成一个 30 秒跟读视频合集 manifest。
6. 把场景标签、例句图片 `object_key`、音频 `object_key` 写入 `word_learning_assets`，供网站展示。

保留安全确认：

- 是否允许新增或修改网站学习素材 manifest / migration？
- 是否允许执行真实视频渲染和素材上传？

配图建议：

- **图 5：EvoMap Agent 的新线程起手式**
- 内容：新线程 prompt → recall Gene/Capsule → 最小方案 → 只确认高风险动作。

### 6. 验收：demo 不是执行生产任务，而是验证 recall 是否生效

这一节要补足“真实验收效果”。

运行命令：

```bash
git clone https://github.com/owenshen0907/evomap-agent-memory-demo.git
cd evomap-agent-memory-demo
python3 demo.py
python3 scripts/validate_recall.py
python3 -m unittest discover
```

验收点：

| 验收项 | 预期 |
| --- | --- |
| 历史线程存在 | 输出 `SIMULATED_SOURCE_THREADS` |
| 干扰线程存在 | 输出 `DISTRACTOR_THREADS` |
| 新线程 recall | 输出 `RECALL_HITS` |
| 命中 Gene | `workshop-shadowing-feedback-loop` |
| 命中 Capsule | `workshop-shadowing-positive-feedback-case` |
| 方案命中关键结构 | `scene_word_set`、`video_collection_manifest`、`word_learning_assets` |
| 自动化结果 | `RESULT / PASS` |
| 单测 | `5 tests OK` |

解释一句：

> 这个 demo 不证明它已经完成真实视频渲染或网站改库。它验证的是更前置的能力：当新线程混入干扰信息时，Agent 能否 recall 到正确的经验，并给出正确方向。

配图建议：

- **图 6：验收输出拆解**
- 内容：source threads / distractors / recall hits / agent response / PASS。

### 7. 收束：普通用户应该怎么开始

建议结尾：

> 不要一开始就让 EvoMap 记住所有东西。先选一个会重复出现的小场景。
>
> 对我来说，这个小场景就是日语工作坊和跟读视频的互相反哺。它足够真实，也足够小：网站提供词库，视频产生新素材，新素材回到网站展示。
>
> 如果这个场景能被 recall，说明 EvoMap 已经开始发挥作用：Agent 不再把每个新线程都当成第一次见我。

## 图片总规划

这版建议 6 张图，不要更多。

| 图 | 标题 | 作用 | 是否需要新画 |
| --- | --- | --- | --- |
| 图 1 | Skill 和 Evolver 的边界 | 解释为什么不是无限补 Skill | 需要新画 |
| 图 2 | 三步接入 EvoMap | 安装 Evolver、setup hooks、可选 skill | 需要新画 |
| 图 3 | 日语工作坊 ↔ 跟读视频反馈循环 | 让读者一眼看到真实场景 | 需要新画 |
| 图 4 | 普通 Agent 的新线程起手式 | 展示反问和重复解释 | 可复用旧图后重画文字 |
| 图 5 | EvoMap Agent 的新线程起手式 | 展示 recall 后直达方案 | 可复用旧图后重画文字 |
| 图 6 | 验收输出拆解 | 展示 demo 的真实证据 | 需要新画 |

## 推荐篇幅

- 总字数：2200 到 3000 字。
- 接入方式：15%。
- 场景：25%。
- 前后对比：25%。
- 验收：25%。
- 结论：10%。

## 最终判断

这版不应该回到“很长的协议介绍”，也不应该像上一版那样太短。核心是让读者看到一条完整链路：

> 让 Agent 帮我安装 → 用一个真实小场景 → 模拟多线程经验 → 新线程 recall → 自动化脚本验收。

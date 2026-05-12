# 一次真实经验复现：EvoMap 如何让 Agent 在新线程里少绕弯

飞书版本：<https://ccnjn62goe9e.feishu.cn/docx/So4SdLJOFoz1dvxMP49c6x1gnlh>

开源 demo：<https://github.com/owenshen0907/evomap-agent-memory-demo>

> 一句话：Skill 适合固定流程；EvoMap / Evolver 更适合把多次任务里的有效经验沉淀下来，让 Agent 在新线程里先 recall，再回答。

![多线程经验如何被 EvoMap 复用](images/mainline-gpt-image-2/zh/11-cross-thread-experience-reuse-zh.png)

## 先说接入：直接让 Agent 帮你装

官网现在的入口已经很直接：把提示复制给 Agent，让它帮你注册和接入。对普通用户来说，不需要先理解协议。

如果你用 Cursor / Claude Code，可以直接发：

```text
Please install `@evomap/evolver` globally, then register evolver's hooks for this IDE (`evolver setup-hooks --platform=cursor` for Cursor, `--platform=claude-code` for Claude Code). Tell me whether I need to restart when you're done.
```

如果你用 Codex 这类终端 Agent，可以发：

```text
请安装 @evomap/evolver，并在当前 git 项目里执行 evolver setup-hooks --platform=codex。完成后告诉我是否需要重启，以及是否注册成功。
```

第一次试用建议先保持本地和可审查：不要自动购买、不要自动发布、不要打开会花费 credits 的功能。装好后，新会话、文件保存、任务结束这些节点就可以成为 Evolver 识别经验信号的入口。

![EvoMap 接入 Agent 的方式](images/mainline-gpt-image-2/zh/09-install-architecture-zh.png)

## 为什么只靠 Skill 会越来越累

Skill 很好用，但它更像固定流程说明。任务一变化，旧 Skill 里的约束就可能变成摩擦。

比如我原来只需要“在日语工作坊网站展示单词图片”。后来任务变成“用网站词库生成跟读视频，再把视频产物反哺回网站”。这已经不是给 Skill 加一条规则就能长期解决的问题。

Evolver 要做的是从这些变化里识别信号：用户纠正了什么、哪个方案有效、哪个旧约束不适合新任务。然后把稳定做法提炼成 Gene，把验证过的正向经验或错误示例包装成 Capsule。

## 最小复现场景

我把真实场景收敛成两个事项：

| 事项 | 已有内容 | 产生的新价值 |
| --- | --- | --- |
| 日语工作坊网站 | 17000 多个单词、17000 多张照片、读音和解释 | 为视频提供稳定 `word_id`、图片和音频 |
| 日语跟读视频 | 按场景筛词，生成跟读合集 | 产生场景标签、例句图片、旁白音频 |

关键是反哺关系：网站给视频提供词库；视频生成出的场景、例句图片和音频，再回到网站展示。

所以 Evolver 应该沉淀的经验是：

> 网站的 `word_id` 是事实源；视频读取 `scene_word_set`；视频生成的场景、例句图片和音频写入 `word_learning_assets`，再反哺回网站。

## 同一个新线程，起手式不同

新线程里我只问：

```text
日语工作坊网站已经有 17000 多个日语单词和对应照片。我想按场景筛选一批词，生成跟读视频合集；视频生成过程中会产生单词场景、例句图片和音频，这些又要反哺回网站展示。你帮我设计一个最小复现流程。
```

普通 Agent 很可能先问表结构、素材位置、场景分类、视频脚本入口、回写方式。

接入 EvoMap 后，理想起手式是：

> 我先复用“日语工作坊 ↔ 跟读视频”的反馈循环经验：网站 `word_id` 是事实源；视频读取 `scene_word_set`；视频产物写回 `word_learning_assets`。先做一个餐厅场景的 8 词小样本，再回写到网站展示。

![接入 EvoMap 后，Agent 先复用经验再给方案](images/mainline-gpt-image-2/zh/06-evolved-direct-path-zh.png)

它不是不问问题，而是只问真正需要确认的高风险动作：是否允许改网站 manifest / migration，是否允许真实渲染视频和上传素材。

## 用 demo 验证

这个 demo 不执行真实上传、改库或视频渲染，只验证 recall 是否生效。

```bash
git clone https://github.com/owenshen0907/evomap-agent-memory-demo.git
cd evomap-agent-memory-demo
python3 scripts/validate_recall.py
python3 -m unittest discover
```

`validate_recall.py` 会模拟网站线程、视频线程、反馈规则线程，再加入首页配色、片头音乐、字幕模板这些干扰信息。最后新线程如果能命中 `workshop-shadowing-feedback-loop` 和 `workshop-shadowing-positive-feedback-case`，就输出 `PASS`。

![开源 demo 用来复现经验沉淀与新线程复用](images/mainline-gpt-image-2/zh/07-test-evidence-zh-v2.png)

## 结论

这篇文章想证明的不是 EvoMap 能自动完成所有工程动作，而是一个更基础的变化：Agent 不必每个新线程都从零理解你。

Skill 负责固定流程；Evolver 负责把真实使用中的有效经验留下来。对普通用户来说，最直接的价值就是少解释、少反问、少绕弯。

# Evolver 自进化演示场景：日语工作坊和跟读视频互相反哺

> 核心结论：这个 case 不再用多个 App 和多套服务器来制造复杂度，而是收敛成两个具体事项：日语工作坊网站和日语跟读视频。它们分别在不同线程里沉淀知识，然后在新线程里通过 recall 互相借用。

## 一、最小事实

同一句需求：

> 日语工作坊网站已经有 17000 多个日语单词和对应照片。我想按场景筛选一批词，生成跟读视频合集；视频生成过程中会产生单词场景、例句图片和音频，这些又要反哺回网站展示。你帮我设计一个最小复现流程。

普通 Agent 会先反问网站表结构、照片/音频位置、场景分类方式、视频脚本入口和回写方式。经过 Evolver 的 Agent 会先 recall 到 `workshop-shadowing-feedback-loop` Gene 和正向 Capsule，然后直接给出 `scene_word_set + video_collection_manifest + word_learning_assets` 的最小复现路径。

## 二、两个工作面

| 工作面 | 已有内容 | 会产生什么 |
| --- | --- | --- |
| 日语工作坊网站 | 17000+ 单词、17000+ 照片、单词详情页、读音/解释 | 为视频提供词库、图片、音频和稳定 `word_id` |
| 日语跟读视频 | 按场景筛词、生成跟读合集 | 产生场景标签、例句、例句图片、旁白音频、视频合集 |

关键关系：

1. 网站是单词事实源。
2. 视频从网站词库按场景筛词。
3. 视频生成出的场景、例句图片和音频反哺网站。
4. 网站展示变丰富后，继续帮助下一轮视频选题。

## 三、Evolver 进化出了什么

| 资产 | 在这个 case 中存什么 | 下次如何发挥作用 |
| --- | --- | --- |
| Gene | `workshop-shadowing-feedback-loop`：网站 `word_id` 是事实源，视频读取 `scene_word_set`，视频产物写回 `word_learning_assets` | 让 Agent 直接按反馈循环设计最小复现 |
| Capsule | `workshop-shadowing-positive-feedback-case`：网站词库和跟读视频互相反哺的正向经验 | 避免 Agent 重复询问两个工作面的关系 |
| EvolutionEvent | 哪些线程提供了网站事实、视频需求、反馈规则和验证结果 | 让自进化过程可追踪、可审核 |

## 四、测试证据

当前 repo 提供离线 demo，不连接真实服务，不消耗 credits。

```bash
python3 demo.py
python3 scripts/validate_recall.py
python3 -m unittest discover
```

验收信号：

- `demo.py` 输出 `SIMULATED_SOURCE_THREADS` 和 `NEW_THREAD_WITH_EVOMAP_RECALL`。
- `scripts/validate_recall.py` 输出 `RESULT / PASS`。
- 新线程回答包含 `scene_word_set`、`video_collection_manifest`、`word_learning_assets`。
- 单测输出 `5 tests OK`。

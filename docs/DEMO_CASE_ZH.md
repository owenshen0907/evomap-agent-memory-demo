# 让 Coding Agent 从绕弯到直达方案：日语工作坊 ↔ 跟读视频案例

> 本文要验证的是：普通 Agent 在新线程里会把日语工作坊网站和跟读视频当成两个陌生事项；接入 EvoMap / Evolver 后，Agent 可以先 recall 已验证的反馈循环经验，再直接给出最小复现方案。

飞书版本：<https://ccnjn62goe9e.feishu.cn/docx/B9qrd6h7aomI33x2gQocuB88nKJ>

开源 Demo：<https://github.com/owenshen0907/evomap-agent-memory-demo>

## 1. 固定问题

```text
日语工作坊网站已经有 17000 多个日语单词和对应照片。我想按场景筛选一批词，生成跟读视频合集；视频生成过程中会产生单词场景、例句图片和音频，这些又要反哺回网站展示。你帮我设计一个最小复现流程。
```

普通 Agent 会先反问网站表结构、素材位置、场景分类、视频脚本入口和回写方式。EvoMap Agent 应该先 recall：网站 `word_id` 是事实源，视频读取 `scene_word_set`，视频产物写回 `word_learning_assets`。

## 2. 场景收敛

| 工作面 | 输入 | 输出 |
| --- | --- | --- |
| 日语工作坊网站 | 17000+ 单词、17000+ 照片、已有读音和解释 | 为视频提供词库、照片、音频、稳定 `word_id` |
| 日语跟读视频 | 按场景筛词、生成视频合集 | 产出场景标签、例句、例句图片、旁白音频 |

核心关系：

1. 网站提供基础数据。
2. 视频用网站数据生成场景化跟读合集。
3. 视频产物反哺网站展示。
4. 下次视频选题可以继续借用网站新增展示信息。

## 3. Evolver 应该沉淀什么

- `Gene workshop-shadowing-feedback-loop`：日语工作坊 `word_id` 是事实源；视频读取 `scene_word_set`；视频产物写回 `word_learning_assets`。
- `Capsule workshop-shadowing-positive-feedback-case`：这个反馈循环能让 Agent 少问背景，直接给出网站和视频互相反哺的最小方案。

## 4. 验证

```bash
git clone https://github.com/owenshen0907/evomap-agent-memory-demo.git
cd evomap-agent-memory-demo
python3 demo.py
python3 scripts/validate_recall.py
python3 -m unittest discover
```

验收标准：

- `demo.py` 输出包含 `SIMULATED_SOURCE_THREADS`、`DISTRACTOR_THREADS`、`NEW_THREAD_WITH_EVOMAP_RECALL`。
- `scripts/validate_recall.py` 输出 `AUTOMATED_RECALL_VALIDATION` 和 `PASS`。
- Evolver 路径出现 `scene_word_set`、`video_collection_manifest`、`word_learning_assets`。
- 单测输出 `5 tests OK`。

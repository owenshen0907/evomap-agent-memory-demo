# EvoMap Agent Memory Demo

A small, offline demo that reproduces a cross-thread EvoMap experience.

The demo models a real user pattern around skills:

1. A skill works well for one concrete workflow.
2. A similar task changes enough that the old skill's assumptions become friction.
3. The Japanese Workshop website thread and the shadowing-video thread each contain useful knowledge.
4. Evolver-style distillation turns the useful signals into a small Gene/Capsule pair.
5. A later new thread asks the agent to connect the two workflows.
6. The agent either starts from zero, or recalls the distilled feedback-loop experience first.

This repo is designed for articles, presentations, onboarding, and local testing. It does not call EvoMap APIs, spend credits, upload files, run database migrations, or require secrets.

## Scenario

The user is an independent developer with two connected work surfaces:

- `japanese-workshop-site`: a website with 17,000+ Japanese vocabulary records and 17,000 generated photos.
- `japanese-shadowing-video`: a video workflow that selects words by scene and generates shadowing-video collections.

The key loop:

1. The website provides canonical vocabulary, photos, and audio.
2. The video workflow consumes scene-filtered words.
3. The video workflow generates scene labels, example sentence images, and audio.
4. Those generated assets feed back into the website display.

The demo request:

```text
日语工作坊网站已经有 17000 多个日语单词和对应照片。我想按场景筛选一批词，生成跟读视频合集；视频生成过程中会产生单词场景、例句图片和音频，这些又要反哺回网站展示。你帮我设计一个最小复现流程。
```

## Quick Start

Run directly from the repository:

```bash
python3 demo.py
```

Print Markdown for slides or docs:

```bash
python3 demo.py --format markdown
```

Run tests:

```bash
python3 -m unittest discover
```

Run the automated recall validation:

```bash
python3 scripts/validate_recall.py
```

## What It Demonstrates

The memory assets in `memory/` are deliberately small:

- `Gene`: reusable strategy for the Workshop-to-shadowing-video feedback loop.
- `Capsule`: validated positive or negative experience from applying a Gene in a concrete environment.

In a real Evolver loop, topology and infrastructure aliases are not the definition of a Capsule. They are evidence context or trigger context for a Capsule. The Capsule itself is the verified result of applying a Gene.

The intended behavior shift is user-visible:

1. Source threads provide background, corrections, and validation evidence.
2. Distractor threads provide nearby but irrelevant context, such as UI styling and video music.
3. The normal agent asks the user to repeat website/video relationship details in a new thread.
4. The EvoMap-enabled agent first recalls the distilled experience.
5. The resulting plan is specific: `scene_word_set`, `video_collection_manifest`, `word_learning_assets`, `word_id`, and `object_key`.

The demo is intentionally text-only. Its purpose is to reproduce experience distillation and reuse, not to execute the real asset-upload task. `scripts/validate_recall.py` is the main verification signal: it feeds source threads, distractor threads, and a new-thread query, then exits with `PASS` only when the correct Gene/Capsule pair is recalled.

## Repo Layout

```text
.
├── docs/
│   ├── DEMO_SCRIPT.md
│   ├── DESIGN.md
│   └── PLAN.md
├── memory/
│   ├── capsule_workshop_shadowing_positive.md
│   └── gene_workshop_shadowing_feedback_loop.md
├── scripts/
│   └── validate_recall.py
├── src/evomap_memory_demo/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── scenario.py
│   ├── simulator.py
│   └── validation.py
└── tests/
    └── test_simulator.py
```

## Safety

Do not put real server IPs, OSS secrets, database passwords, API keys, signed URLs, or private business data into memory assets. Keep aliases, topology, routing policy, and validated workflow rules only.

## License

MIT

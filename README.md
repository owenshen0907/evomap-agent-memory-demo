# EvoMap Agent Memory Demo

A small, offline demo that reproduces a cross-thread EvoMap experience.

The demo models a real user pattern:

1. Several earlier agent threads contain project background, user corrections, and a validated pattern.
2. Evolver-style distillation turns those text signals into a small Gene/Capsule pair.
3. A later new thread asks a related task.
4. The agent either starts from zero, or recalls the distilled experience first.

This repo is designed for articles, presentations, onboarding, and local testing. It does not call EvoMap APIs, spend credits, upload files, run database migrations, or require secrets.

## Scenario

The user is an independent developer with:

- a Japanese learning workshop website,
- two mobile app lines,
- a short-video production pipeline,
- domestic and overseas servers,
- a separate database server,
- OSS buckets and asset delivery paths shared across projects.

The demo request:

```text
我要给 N5 单词卡生成一批音频和插图，上传到 OSS，并让网站、两个 app、视频剪辑流水线都能复用。国内用户走国内 OSS/CDN，海外用户走海外加速。你帮我设计并落地最小实现。
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

## What It Demonstrates

The memory assets in `memory/` are deliberately small:

- `Gene`: reusable strategy for shared asset publishing.
- `Capsule`: validated positive or negative experience from applying a Gene in a concrete environment.

In a real Evolver loop, topology and infrastructure aliases are not the definition of a Capsule. They are evidence context or trigger context for a Capsule. The Capsule itself is the verified result of applying a Gene.

The intended behavior shift is user-visible:

1. Source threads provide background, corrections, and validation evidence.
2. The normal agent asks the user to repeat infrastructure details in a new thread.
3. The EvoMap-enabled agent first recalls the distilled experience.
4. The resulting plan is specific: `asset_manifest`, `object_key`, checksum, `AssetUrlResolver`, domestic/global region routing, and video manifest snapshots.

The demo is intentionally text-only. Its purpose is to reproduce experience distillation and reuse, not to execute the real asset-upload task.

## Repo Layout

```text
.
├── docs/
│   ├── DEMO_SCRIPT.md
│   ├── DESIGN.md
│   └── PLAN.md
├── memory/
│   ├── capsule_shared_asset_pipeline_positive.md
│   └── gene_shared_asset_pipeline.md
├── src/evomap_memory_demo/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── scenario.py
│   └── simulator.py
└── tests/
    └── test_simulator.py
```

## Safety

Do not put real server IPs, OSS secrets, database passwords, API keys, signed URLs, or private business data into memory assets. Keep aliases, topology, routing policy, and validated workflow rules only.

## License

MIT

# EvoMap Agent Memory Demo

A small, offline demo that shows why coding agents need reusable memory.

The demo compares two responses to the same independent-developer request:

- `WITHOUT_EVOMAP`: the agent starts from zero, asks for infra details, and gets stuck choosing between generic asset strategies.
- `WITH_EVOMAP`: the agent recalls a topology Capsule and a shared-asset Gene, then immediately gives a concrete implementation plan.

This repo is designed for presentations, onboarding, and local testing. It does not call EvoMap APIs, spend credits, upload files, or require secrets.

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

- `Capsule`: reusable facts about the developer's project topology.
- `Gene`: reusable strategy for shared asset publishing.

The intended behavior shift is user-visible:

1. The normal agent asks the user to repeat infra details.
2. The EvoMap-enabled agent states the recalled assumptions and asks only for real execution approvals.
3. The resulting plan is specific: `asset_manifest`, `object_key`, checksum, `AssetUrlResolver`, domestic/global region routing, and video manifest snapshots.

## Repo Layout

```text
.
├── docs/
│   ├── DEMO_SCRIPT.md
│   ├── DESIGN.md
│   └── PLAN.md
├── memory/
│   ├── capsule_infra_topology.md
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

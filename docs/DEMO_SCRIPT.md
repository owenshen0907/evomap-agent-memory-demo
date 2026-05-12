# Demo Script

## One-Line Setup

This is a text-only reproduction of cross-thread experience reuse:

- a skill works for one concrete workflow, then becomes brittle when the task changes;
- earlier threads provide skill-fit context, corrections, and validation;
- distractor threads provide nearby but irrelevant context;
- Evolver-style distillation produces a shared-asset Gene and positive Capsule;
- a new thread can recall those assets before answering.

## Source Threads

- `thread-a / background`: the user explains that an existing asset-publishing skill works for one concrete website workflow, but becomes brittle when the same assets must be reused by apps and video.
- `thread-b / correction`: the user corrects a full-URL database strategy and prefers stable `object_key` storage.
- `thread-c / validation`: the `asset_manifest + AssetUrlResolver` strategy is treated as the validated reusable plan.

## Distractor Threads

- `thread-noise-1 / distractor`: the user discusses UI colors and title typography.
- `thread-noise-2 / distractor`: the user discusses background music and opening animation timing.

These should not steer recall toward UI or editing rules when the new task is about shared asset storage and delivery.

## New Thread Prompt

```text
我要给 N5 单词卡生成一批音频和插图，上传到 OSS，并让网站、两个 app、视频剪辑流水线都能复用。国内用户走国内 OSS/CDN，海外用户走海外加速。你帮我设计并落地最小实现。
```

## Expected Contrast

### Without Recall

The agent asks:

- Which servers exist?
- What is the OSS bucket?
- Does the video pipeline read DB or files?
- Should URLs be stored or generated?
- Is overseas delivery proxy, CDN, or sync?

This is rational for a stateless agent, but it wastes time because the user has already explained and corrected this pattern in earlier threads.

### With EvoMap Recall

The agent recalls:

- `shared-asset-pipeline-invariant`
- `shared-asset-pipeline-positive-jp-learning-stack`

Then it gives the plan:

- store canonical asset metadata in `asset_manifest`;
- store `object_key`, not permanent full URLs;
- generate URLs through `AssetUrlResolver`;
- route domestic and global delivery separately;
- let web, apps, and video jobs consume the same manifest source.

## Talk Track

Start with the behavior change, not the protocol:

> The point is not that the demo uploads files or edits a real database. The point is that experience from earlier text threads can be distilled and reused in a new thread, so the agent starts closer to the right answer.

Then explain the memory model:

> A Gene stores reusable strategy. A Capsule stores a positive or negative experience from applying a Gene in a concrete environment. Neither should contain secrets.

## Live Command

```bash
python3 demo.py --format markdown
python3 scripts/validate_recall.py
```

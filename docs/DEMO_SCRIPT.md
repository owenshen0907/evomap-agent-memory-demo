# Demo Script

## One-Line Setup

This is a text-only reproduction of cross-thread experience reuse:

- a skill works for one concrete workflow, then becomes brittle when the task changes;
- the Japanese Workshop website thread and shadowing-video thread each contain useful knowledge;
- distractor threads provide nearby but irrelevant context;
- Evolver-style distillation produces a website-video feedback-loop Gene and positive Capsule;
- a new thread can recall those assets before answering.

## Source Threads

- `thread-workshop / website-source`: Japanese Workshop already has 17,000+ words and generated photos.
- `thread-video / video-consumer`: shadowing videos select words by scene and generate video collections, example sentences, sentence images, and audio.
- `thread-feedback / feedback-rule`: video-generated scenes, example images, and audio should feed back into the website through stable `word_id` and `object_key` manifests.

## Distractor Threads

- `thread-noise-1 / distractor`: the user discusses UI colors and title typography.
- `thread-noise-2 / distractor`: the user discusses background music and opening animation timing.

These should not steer recall toward UI or editing rules when the new task is about the Workshop-video feedback loop.

## New Thread Prompt

```text
日语工作坊网站已经有 17000 多个日语单词和对应照片。我想按场景筛选一批词，生成跟读视频合集；视频生成过程中会产生单词场景、例句图片和音频，这些又要反哺回网站展示。你帮我设计一个最小复现流程。
```

## Expected Contrast

### Without Recall

The agent asks:

- What is the website vocabulary schema?
- Where are the existing photos and audio files?
- Does the video workflow read DB, CSV, JSON, or website APIs?
- Where should generated example images and audio be written back?
- Should video outputs duplicate word records or attach to existing `word_id`s?

This is rational for a stateless agent, but it wastes time because the user has already explained and corrected this pattern in earlier threads.

### With EvoMap Recall

The agent recalls:

- `workshop-shadowing-feedback-loop`
- `workshop-shadowing-positive-feedback-case`

Then it gives the plan:

- treat Japanese Workshop `word_id` records as the source of truth;
- create `scene_word_set` for one scene;
- generate `video_collection_manifest` from that set;
- write scene labels, example images, and narration audio into `word_learning_assets`;
- let the website display the video-generated assets without duplicating word records.

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

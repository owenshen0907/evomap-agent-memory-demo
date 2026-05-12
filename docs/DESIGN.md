# Design

## Goal

Provide a minimal, reproducible, text-only demo of cross-thread experience reuse between two concrete work surfaces: the Japanese Workshop website and Japanese shadowing videos.

## Non-Goals

- No live EvoMap API calls.
- No credit spending.
- No real OSS upload.
- No real database migration.
- No real video generation or publishing.
- No private infrastructure details.

## Core Model

The demo has five parts:

1. Simulated source threads that contain skill-fit, correction, and validation signals.
2. Evolver-style distillation into a website-video feedback-loop Gene and positive Capsule.
3. Distractor threads with nearby but irrelevant UI/video context.
4. A new-thread prompt that asks the agent to connect website data and video output.
5. A recall-enabled response that uses the distilled assets before answering.

## Memory Assets

`Gene: workshop-shadowing-feedback-loop`

- Stores the strategy for using Japanese Workshop `word_id` records as the source of truth.
- Encodes the loop where scene-filtered words become shadowing videos, then video-generated scenes, example images, and audio feed back into the website.

`Capsule: workshop-shadowing-positive-feedback-case`

- Records positive evidence that the two-surface feedback loop works.
- Uses the website and video workflow relationship as trigger context, not as a place to store secrets or production paths.

## Why This Case Is Small Enough

The demo reduces the real developer environment to two work surfaces. The website starts with 17,000+ words and generated photos. The shadowing-video workflow needs scene-filtered word sets, then produces scene labels, example sentence images, and audio that can improve the website display. That is enough to reproduce cross-thread experience reuse without exposing private details or executing production actions.

## Automated Validation

`scripts/validate_recall.py` is the main verification signal. It:

1. Prints source threads and distractor threads.
2. Runs a deterministic recall query with mixed relevant and irrelevant context.
3. Passes only when the workshop-shadowing Gene and positive Capsule are both recalled.
4. Checks that the simulated response uses `scene_word_set`, `video_collection_manifest`, and `word_learning_assets`, while still asking for real execution approvals.

## Extension Path

Later versions can add:

- real EvoMap search-only metadata,
- live Capsule/Gene import,
- richer thread transcripts,
- real Evolver local memory fixtures,
- a small SQLite migration example,
- a mocked OSS upload adapter,
- side-by-side transcript export for slides.

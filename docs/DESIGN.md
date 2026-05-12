# Design

## Goal

Provide a minimal, reproducible, text-only demo of cross-thread experience reuse.

## Non-Goals

- No live EvoMap API calls.
- No credit spending.
- No real OSS upload.
- No real database migration.
- No real video generation or publishing.
- No private infrastructure details.

## Core Model

The demo has four parts:

1. Simulated source threads that contain background, correction, and validation signals.
2. Evolver-style distillation into a shared-asset Gene and positive Capsule.
3. A new-thread prompt with cross-project ambiguity.
4. A recall-enabled response that uses the distilled assets before answering.

## Memory Assets

`Gene: shared-asset-pipeline-invariant`

- Stores the strategy for shared generated assets.
- Encodes the invariant that DB stores object keys and metadata, while URLs are resolved by region at runtime.

`Capsule: shared-asset-pipeline-positive-jp-learning-stack`

- Records positive evidence that the shared-asset Gene works in the Japanese-learning stack.
- Uses aliases and project relationships as trigger context, not as the definition of the Capsule.

## Why This Case Is Small Enough

The demo reduces the real developer environment to four projects and four infrastructure aliases. That is enough to reproduce cross-thread experience reuse without exposing private details or executing production actions.

## Extension Path

Later versions can add:

- real EvoMap search-only metadata,
- live Capsule/Gene import,
- richer thread transcripts,
- real Evolver local memory fixtures,
- a small SQLite migration example,
- a mocked OSS upload adapter,
- side-by-side transcript export for slides.

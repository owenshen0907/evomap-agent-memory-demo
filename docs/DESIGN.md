# Design

## Goal

Provide a minimal, reproducible demo of coding-agent behavior before and after reusable memory.

## Non-Goals

- No live EvoMap API calls.
- No credit spending.
- No real OSS upload.
- No real database migration.
- No private infrastructure details.

## Core Model

The demo has three parts:

1. A user prompt with cross-project ambiguity.
2. A stateless-agent response that asks broad setup questions.
3. A memory-enabled response that uses two recalled assets.

## Memory Assets

`Capsule: infra-topology-jp-learning-stack`

- Stores aliases and project relationships.
- Useful when the task crosses website, apps, video pipeline, DB, OSS, and global edge.

`Gene: shared-asset-pipeline-invariant`

- Stores the strategy for shared generated assets.
- Encodes the invariant that DB stores object keys and metadata, while URLs are resolved by region at runtime.

## Why This Case Is Small Enough

The demo reduces the real developer environment to four projects and four infrastructure aliases. That is enough to reproduce the agent behavior gap without exposing private details.

## Extension Path

Later versions can add:

- real EvoMap search-only metadata,
- live Capsule/Gene import,
- a small SQLite migration example,
- a mocked OSS upload adapter,
- side-by-side transcript export for slides.

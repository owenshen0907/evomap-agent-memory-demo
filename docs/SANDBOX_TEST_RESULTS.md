# Sandbox Test Results

Run date: 2026-05-12

Environment:

- Local sandbox root: `/tmp/evomap-evolver-sandbox`
- Temporary clone: `/tmp/evomap-evolver-sandbox/work/repo`
- Temporary home: `/tmp/evomap-evolver-sandbox/home`
- Safety flags:
  - `EVOLVER_ATP_AUTOBUY=off`
  - `ATP_AUTOBUY_DAILY_CAP_CREDITS=0`
  - `ATP_AUTOBUY_PER_ORDER_CAP_CREDITS=0`
  - `EVOLVER_AUTO_PUBLISH=false`
  - `EVOLVER_VALIDATOR_ENABLED=false`
  - `WORKER_ENABLED=0`

## Offline Text Reproduction

Command:

```bash
python3 demo.py
```

Observed:

- Output contains `SIMULATED_SOURCE_THREADS`.
- Output contains `DISTRACTOR_THREADS`.
- Output contains `EVOLVER_DISTILLATION`.
- Output contains `NEW_THREAD_WITH_EVOMAP_RECALL`.
- Output contains `WITHOUT_EVOMAP`.
- `WITHOUT_EVOMAP` path asks for server role, OSS config, database/API shape, URL strategy, and video pipeline source.
- `NEW_THREAD_WITH_EVOMAP_RECALL` path recalls:
  - `Gene workshop-shadowing-feedback-loop`
  - `Capsule workshop-shadowing-positive-feedback-case`
- `NEW_THREAD_WITH_EVOMAP_RECALL` path proposes:
  - `scene_word_set`
  - `video_collection_manifest`
  - `word_learning_assets`
  - `word_id`
  - `object_key`

Interpretation: this is a text-only reproduction of experience distillation and
reuse across threads. It does not perform real uploads, database migrations, or
video rendering.

## Automated Recall Validation

Command:

```bash
python3 scripts/validate_recall.py
```

Observed:

- Output contains `AUTOMATED_RECALL_VALIDATION`.
- Output contains `SOURCE_THREADS`.
- Output contains `DISTRACTOR_THREADS`.
- Output contains `RECALL_QUERY`.
- Output contains both:
  - `Gene workshop-shadowing-feedback-loop`
  - `Capsule workshop-shadowing-positive-feedback-case`
- Output ends with `RESULT` / `PASS`.

Interpretation: the validation script treats the demo as an integration signal
for EvoMap recall. It verifies that relevant source-thread experience can be
selected even when the new thread contains nearby UI and video-editing noise.

## Unit Tests

Command:

```bash
python3 -m unittest discover
```

Observed:

```text
.....
----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK
```

## Evolver Hook Setup

Command:

```bash
evolver setup-hooks --platform=codex
```

Observed:

```text
[setup-hooks] Platform: Codex
[setup-hooks] Config root: /private/tmp/evomap-evolver-sandbox/work/repo
[codex] Wrote /private/tmp/evomap-evolver-sandbox/work/repo/.codex/hooks.json
[codex] Copied 3 hook scripts to /private/tmp/evomap-evolver-sandbox/work/repo/.codex/hooks
[codex] Enabled codex_hooks in config.toml
[codex] Injected evolution section into /private/tmp/evomap-evolver-sandbox/work/repo/AGENTS.md
[codex] Installation complete.
```

Files created or updated inside the sandbox clone:

- `/tmp/evomap-evolver-sandbox/work/repo/.codex/hooks.json`
- `/tmp/evomap-evolver-sandbox/work/repo/.codex/config.toml`
- `/tmp/evomap-evolver-sandbox/work/repo/AGENTS.md`
- `/tmp/evomap-evolver-sandbox/work/repo/.codex/hooks/evolver-session-start.js`
- `/tmp/evomap-evolver-sandbox/work/repo/.codex/hooks/evolver-signal-detect.js`
- `/tmp/evomap-evolver-sandbox/work/repo/.codex/hooks/evolver-session-end.js`

Conclusion: the hook setup was isolated to the temporary clone and did not need to write into the user's real home directory for this Codex-platform test.

## GEP MCP Smoke Test

Command:

```bash
npx -y @evomap/gep-mcp-server --help
```

Observed:

```text
GEP MCP Server running on stdio (local mode)
EXIT_CODE=0
```

Conclusion: the MCP server can start in local mode without providing Hub credentials for this smoke test.

## Current Status

The sandbox is good enough for local smoke testing:

- Demo behavior difference is reproducible.
- Automated recall validation passes with distractor context.
- Unit tests pass.
- Evolver Codex hooks can be installed into a temporary clone.
- GEP MCP starts in local mode.

For production-like evidence, repeat the same plan on a fresh computer and capture screenshots of:

1. `python3 demo.py` output showing both paths.
2. `python3 scripts/validate_recall.py` output showing `RESULT` / `PASS`.
3. `python3 -m unittest discover` showing `5 tests OK`.
4. `evolver setup-hooks --platform=codex` output showing hook files created under the test repo.
5. `npx -y @evomap/gep-mcp-server --help` showing local mode startup.

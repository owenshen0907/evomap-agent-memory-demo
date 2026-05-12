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

## Offline Demo

Command:

```bash
python3 demo.py
```

Observed:

- Output contains `WITHOUT_EVOMAP`.
- Output contains `WITH_EVOMAP`.
- `WITHOUT_EVOMAP` path asks for server role, OSS config, database/API shape, URL strategy, and video pipeline source.
- `WITH_EVOMAP` path recalls:
  - `Gene shared-asset-pipeline-invariant`
  - `Capsule shared-asset-pipeline-positive-jp-learning-stack`
- `WITH_EVOMAP` path proposes:
  - `asset_manifest`
  - `object_key`
  - checksum
  - `AssetUrlResolver(region, object_key)`
  - domestic/global URL resolution

## Unit Tests

Command:

```bash
python3 -m unittest discover
```

Observed:

```text
..
----------------------------------------------------------------------
Ran 2 tests in 0.000s

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
- Unit tests pass.
- Evolver Codex hooks can be installed into a temporary clone.
- GEP MCP starts in local mode.

For production-like evidence, repeat the same plan on a fresh computer and capture screenshots of:

1. `python3 demo.py` output showing both paths.
2. `python3 -m unittest discover` showing `2 tests OK`.
3. `evolver setup-hooks --platform=codex` output showing hook files created under the test repo.
4. `npx -y @evomap/gep-mcp-server --help` showing local mode startup.

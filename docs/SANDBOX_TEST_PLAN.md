# Sandbox Test Plan

This plan verifies the demo and Evolver setup path without polluting the user's real machine configuration.

## Safety Defaults

Use these settings for every first-run test:

```bash
export EVOLVER_ATP_AUTOBUY=off
export ATP_AUTOBUY_DAILY_CAP_CREDITS=0
export ATP_AUTOBUY_PER_ORDER_CAP_CREDITS=0
export EVOLVER_AUTO_PUBLISH=false
export EVOLVER_VALIDATOR_ENABLED=false
export WORKER_ENABLED=0
```

Do not place real API keys, node secrets, OSS credentials, database passwords, private IPs, or signed URLs in this repo or in Evolver memory assets.

## Offline Demo Verification

```bash
git clone https://github.com/owenshen0907/evomap-agent-memory-demo.git
cd evomap-agent-memory-demo
python3 demo.py
python3 demo.py --format markdown
python3 -m unittest discover
```

Expected evidence:

- `demo.py` prints `WITHOUT_EVOMAP`.
- `demo.py` prints `WITH_EVOMAP`.
- The evolved path includes `asset_manifest`.
- The evolved path includes `AssetUrlResolver`.
- `unittest discover` reports `2 tests OK`.

## Local Sandbox On The Current Machine

This mode uses a temporary `HOME`, so `evolver setup-hooks` writes into the sandbox home instead of the user's real home directory.

```bash
export SANDBOX_ROOT=/tmp/evomap-evolver-sandbox
rm -rf "$SANDBOX_ROOT"
mkdir -p "$SANDBOX_ROOT/home" "$SANDBOX_ROOT/work"

export HOME="$SANDBOX_ROOT/home"
export EVOLVER_ATP_AUTOBUY=off
export ATP_AUTOBUY_DAILY_CAP_CREDITS=0
export ATP_AUTOBUY_PER_ORDER_CAP_CREDITS=0
export EVOLVER_AUTO_PUBLISH=false
export EVOLVER_VALIDATOR_ENABLED=false
export WORKER_ENABLED=0

git clone https://github.com/owenshen0907/evomap-agent-memory-demo.git "$SANDBOX_ROOT/work/repo"
cd "$SANDBOX_ROOT/work/repo"

python3 demo.py
python3 -m unittest discover

evolver --help
evolver setup-hooks --platform=codex
find "$HOME" -maxdepth 4 -type f | sort
```

Expected evidence:

- Demo and tests pass inside the sandbox clone.
- `evolver --help` is available.
- Hook files, if created, appear under `$SANDBOX_ROOT/home`, not under the user's real `~`.

## GEP MCP Local Mode Smoke Test

Run this only as a process smoke test. Stop it after it prints that the server is running.

```bash
npx -y @evomap/gep-mcp-server --help
```

Expected evidence:

- The command starts in local mode or prints help without requiring secrets.
- No Hub spending or publishing happens.

## New Computer Verification

If local sandbox isolation is not trusted, use a fresh computer:

1. Clone the public repo.
2. Run the offline demo verification commands.
3. Capture terminal screenshots showing `WITHOUT_EVOMAP`, `WITH_EVOMAP`, and `2 tests OK`.
4. Optionally run Evolver hook setup with the same safety defaults and screenshot the created files.

Keep credentials out of screenshots and logs.

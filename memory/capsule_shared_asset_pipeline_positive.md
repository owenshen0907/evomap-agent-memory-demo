# Capsule: shared-asset-pipeline-positive-jp-learning-stack

## Type

Positive capsule

## Gene

`shared-asset-pipeline-invariant`

## Trigger Context

The developer maintains a Japanese-learning product family with four streams:

- `jp-workshop-web`
- `speak-practice-app`
- `grammar-helper-app`
- `short-video-pipeline`

Shared infrastructure aliases:

- `db-primary`: primary database server for vocabulary, grammar, asset metadata, and generation state.
- `oss-cn-assets`: domestic OSS bucket and primary asset store.
- `server-cn-app`: domestic app/API host.
- `server-global-edge`: overseas acceleration host or edge proxy.

## Experience

When a task asks for generated learning assets to be reused by the website,
apps, and video pipeline, the shared-asset Gene should be applied directly:

1. Store `object_key` and metadata in `asset_manifest`.
2. Avoid storing fixed full URLs in the database.
3. Resolve access URLs at runtime with `AssetUrlResolver(region, object_key)`.
4. Keep video jobs on a versioned manifest snapshot.

## Evidence

The local demo and unit tests validate the intended behavior shift:

- `python3 demo.py` shows the normal path asking for repeated infrastructure context.
- `python3 demo.py` shows the evolved path going directly to `asset_manifest`, `object_key`, and `AssetUrlResolver`.
- `python3 -m unittest discover` checks both paths and the presence of the Gene/Capsule assets.

## Safe Memory Rule

Keep only aliases, topology context, strategy, and validation evidence in memory.
Never store credentials, real IPs, bucket secrets, database passwords, OAuth
tokens, or private signed URLs.

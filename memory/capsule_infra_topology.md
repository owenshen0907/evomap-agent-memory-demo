# Capsule: infra-topology-jp-learning-stack

## Type

Fact capsule

## Summary

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

## Safe Memory Rule

Keep only aliases, topology, and routing policy in memory. Never store credentials, real IPs, bucket secrets, database passwords, OAuth tokens, or private signed URLs.

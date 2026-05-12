# Gene: shared-asset-pipeline-invariant

## Trigger

Use this Gene when a task asks to make generated learning assets reusable across the Japanese-learning website, mobile apps, and video pipeline.

Typical signals:

- `jp_learning_assets`
- `oss_upload`
- `cross_project_reuse`
- `global_edge`
- `video_pipeline`

## Strategy

1. Store canonical asset facts in DB: `object_key`, `sha256`, `asset_type`, `locale`, `word_id`, `source_project`, `status`, timestamps.
2. Do not store permanent full URLs in DB. Full URLs depend on access region and may change with CDN or edge routing.
3. Expose one `AssetUrlResolver` that derives URLs from `object_key` and `region`.
4. Use `asset_manifest` as the shared source for web, apps, and video exports.
5. Upload first, verify checksum, then write or update manifest.
6. Domestic users resolve through domestic OSS/CDN. Global users resolve through the global edge domain or proxy.
7. Video jobs consume a manifest snapshot, not ad hoc per-project paths.

## Minimal Data Shape

```sql
asset_manifest(
  id,
  word_id,
  asset_type,
  object_key,
  sha256,
  locale,
  source_project,
  status,
  created_at,
  updated_at
)
```

## Expected Next Action

When this Gene matches, do not ask the user to repeat basic topology. State the recalled assumption, ask only for missing secrets or irreversible deployment confirmation, then implement the smallest vertical slice.

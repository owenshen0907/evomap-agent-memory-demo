# Gene: workshop-shadowing-feedback-loop

## Trigger

Use this Gene when a task connects the Japanese Workshop website with the
Japanese shadowing-video workflow.

Typical signals:

- `日语工作坊`
- `17000`
- `单词`
- `照片`
- `跟读视频`
- `场景筛选`
- `例句图片`
- `音频`
- `反哺网站`

## Strategy

1. Treat Japanese Workshop as the vocabulary source of truth.
2. Keep stable identifiers on website records: `word_id`, reading, meaning,
   existing photo `object_key`, and existing audio `object_key`.
3. Select words by scene into `scene_word_set` instead of creating an unrelated
   video-only vocabulary table.
4. Generate shadowing-video collections from `scene_word_set`.
5. Store video-generated outputs in `word_learning_assets`: scene labels,
   example sentence text, example sentence image `object_key`, narration audio
   `object_key`, and video collection id.
6. Let the website read `word_learning_assets` to display the improved scene,
   example image, audio, and related shadowing video.
7. Keep generated media paths as stable `object_key` values; resolve public URLs
   in the consuming surface.

## Minimal Data Shape

```sql
scene_word_set(
  id,
  scene_id,
  word_id,
  rank,
  reason,
  created_at
)

video_collection_manifest(
  id,
  scene_id,
  title,
  word_ids,
  output_object_key,
  status,
  created_at
)

word_learning_assets(
  id,
  word_id,
  scene_id,
  example_sentence,
  example_image_object_key,
  narration_audio_object_key,
  video_collection_id,
  created_at
)
```

## Expected Next Action

When this Gene matches, do not ask the user to re-explain the whole website and
video relationship. State the recalled feedback-loop assumption, then propose a
small vertical slice: one scene, a few words, a short video manifest, and a
website feedback manifest.

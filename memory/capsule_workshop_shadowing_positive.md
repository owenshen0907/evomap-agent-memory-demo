# Capsule: workshop-shadowing-positive-feedback-case

## Type

Positive capsule

## Gene

`workshop-shadowing-feedback-loop`

## Trigger Context

The developer maintains two connected surfaces:

- `japanese-workshop-site`: website with 17,000+ Japanese vocabulary records and
  generated photos.
- `japanese-shadowing-video`: scene-based shadowing-video workflow that selects
  words, creates video collections, and generates example sentence images and
  audio.

## Experience

The useful pattern is a two-way feedback loop:

1. Japanese Workshop provides the canonical word list and existing photos/audio.
2. Shadowing videos consume scene-filtered word sets.
3. Video generation produces scene labels, example sentences, sentence images,
   narration audio, and collection metadata.
4. Those generated assets feed back into the website display through stable
   `word_id` and `object_key` manifests.

## Evidence

The local demo and unit tests validate the intended behavior shift:

- `python3 demo.py` shows the normal path asking for repeated website/video
  relationship details.
- `python3 demo.py` shows the evolved path going directly to
  `scene_word_set`, `video_collection_manifest`, and `word_learning_assets`.
- `python3 scripts/validate_recall.py` simulates source threads, distractor
  threads, and a new recall query, then passes only when the correct
  Gene/Capsule pair is recalled.
- `python3 -m unittest discover` checks both paths and the presence of the
  Gene/Capsule assets.

## Safe Memory Rule

Keep only aliases, topology context, strategy, and validation evidence in memory.
Never store credentials, real IPs, bucket secrets, database passwords, OAuth
tokens, or private signed URLs.

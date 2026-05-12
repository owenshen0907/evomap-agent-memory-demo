# Demo Script

## One-Line Setup

Same request, two agents:

- one starts from zero,
- one recalls a shared-asset Gene and a positive Capsule for that Gene.

## Prompt

```text
我要给 N5 单词卡生成一批音频和插图，上传到 OSS，并让网站、两个 app、视频剪辑流水线都能复用。国内用户走国内 OSS/CDN，海外用户走海外加速。你帮我设计并落地最小实现。
```

## Expected Contrast

### Without EvoMap

The agent asks:

- Which servers exist?
- What is the OSS bucket?
- Does the video pipeline read DB or files?
- Should URLs be stored or generated?
- Is overseas delivery proxy, CDN, or sync?

This is rational for a stateless agent, but it wastes time because the user already explained this in earlier work.

### With EvoMap

The agent recalls:

- `shared-asset-pipeline-invariant`
- `shared-asset-pipeline-positive-jp-learning-stack`

Then it gives the plan:

- store canonical asset metadata in `asset_manifest`,
- store `object_key`, not permanent full URLs,
- generate URLs through `AssetUrlResolver`,
- route domestic and global delivery separately,
- let web, apps, and video jobs consume the same manifest source.

## Talk Track

Start with the behavior change, not the protocol:

> The normal agent treats every window as a new user. The EvoMap-enabled agent remembers my project topology and prior decisions, so it asks fewer questions and starts from the right implementation boundary.

Then explain the memory model:

> A Gene stores reusable strategy. A Capsule stores a positive or negative experience from applying a Gene in a concrete environment. Neither should contain secrets.

## Live Command

```bash
python3 demo.py --format markdown
```

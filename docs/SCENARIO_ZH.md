# Evolver 自进化演示场景：从绕弯到直达方案

> 核心结论：Evolver 的重点不是让 Agent “记住更多内容”，而是让 Agent 把一次任务中的事实、策略和结果沉淀成可召回、可验证、可审计的能力资产。下一次遇到相似任务时，Agent 的行为会发生可观察的变化：少反问、少绕弯、更快给出贴合现有系统的方案。

飞书文档：<https://ccnjn62goe9e.feishu.cn/docx/ItTsdalH6oUZTPxlJoqcyurNnHe>

## 一、先看事实

同一句需求：

> 我要给 N5 单词卡生成一批音频和插图，上传到 OSS，并让网站、两个 app、视频剪辑流水线都能复用。国内用户走国内 OSS/CDN，海外用户走海外加速。你帮我设计并落地最小实现。

普通 Agent 会先反问服务器分工、OSS 配置、数据库结构、视频流水线和 URL 策略。经过 Evolver 的 Agent 会先 recall 到共享素材策略 Gene，以及该 Gene 在类似拓扑中的正向 Capsule 证据，然后直接给出 `asset_manifest + object_key + AssetUrlResolver` 的最小实现。

![进化前后](images/mainline-gpt-image-2/zh/01-before-after-effect-zh.png)

## 二、真实场景

这个 case 的背景是一个独立开发者同时维护多个日语学习相关产品。真正复杂的地方不是项目数量，而是这些项目共享基础数据、共享素材、共享服务器和发布链路。

| 维度 | 内容 | 难点 |
| --- | --- | --- |
| 产品线 | 日语学习工坊网站、语音练习 App、语法助手 App、视频流水线 | 需求跨多个代码库和产物形态 |
| 基础设施 | 国内应用服务器、海外加速节点、独立数据库、OSS 素材桶 | Agent 不知道每台服务的角色和边界 |
| 共享数据 | 词条、语法、音频、插图、视频素材 | 一次生成的素材要被多端复用 |
| 历史约定 | DB 存 object_key，不存固定完整 URL | 没有历史经验时会在多个通用方案里纠结 |

![项目拓扑](images/mainline-gpt-image-2/zh/03-project-topology-zh.png)

## 三、Evolver 进化出了什么

| 资产 | 在这个 case 中存什么 | 下次如何发挥作用 |
| --- | --- | --- |
| Gene：策略基因 | 共享素材发布策略：`asset_manifest`、`object_key`、checksum、`AssetUrlResolver` | 让 Agent 直接按已验证策略设计最小实现 |
| Capsule：经验胶囊 | 某个 Gene 在四条产品线和 `db-primary`、`oss-cn-assets`、`server-cn-app`、`server-global-edge` 这类环境中的正向经验或错误示例 | 避免 Agent 重复询问基础设施和项目边界，同时避免重复踩坑 |
| EvolutionEvent：审计记录 | 能力缺口、采用策略、结果是否有效 | 让自进化过程可追踪、可审核、可回滚 |

![自进化闭环](images/mainline-gpt-image-2/zh/02-self-evolution-loop-zh.png)

![信号到胶囊](images/mainline-gpt-image-2/zh/04-evolver-signal-gene-capsule-zh-v2.png)

## 四、测试证据

当前 repo 提供离线 demo，不连接真实服务，不消耗 credits。它的作用是稳定复现“进化前后行为差异”。

```bash
python3 demo.py
python3 -m unittest discover
```

![测试证据](images/mainline-gpt-image-2/zh/07-test-evidence-zh-v2.png)

![效果指标](images/mainline-gpt-image-2/zh/08-evolution-metrics-zh-v2.png)

## 五、通用接入

正式接入建议分三层：

- Agent Hooks：让 Agent 在合适时机记录和读取进化记忆。
- GEP MCP：提供 recall / evolve / record。
- EvoMap Hub：可选，用于共享、发布、市场和 credits。

![通用接入方式](images/mainline-gpt-image-2/zh/09-install-architecture-zh.png)

第一次接入建议 local + reviewed，不要默认开启自动购买、自动发布、worker、validator 或任何会花费 credits 的能力。

![安全边界](images/mainline-gpt-image-2/zh/10-safety-boundary-zh.png)

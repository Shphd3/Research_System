# 每轮 Anchor 指导完成后的阅读同步

[English](anchor_sync.md) · [已同步内容](../sync/anchors/README_cn.md)

研究者已指定：每轮实质性的Anchor指导或修订交付后，把必要材料同步到Research_System。
只拥有这个仓库的读者，也应能读到问题、设计、关键证据和数据身份。

## 什么时候同步、放在哪里

先完成本轮所属原记录，再同步阅读副本，最后报告交付完成。Anchor仍可处于草稿或待审状态；
“指导完成”不表示问题关闭或科学批准。没有正式来源的普通讨论，不因此强行新建Anchor。

每个已有问题使用一个固定目录：

```text
sync/anchors/<项目>/<anchor编号>/
  README.md        阅读顺序
  documents/       调整链接后的阅读副本
  sources/         逐字节原文与选定的小型来源元数据
  manifest.json    来源版本、哈希和缺失引用
  UNAVAILABLE.md   未选入、不可访问或位于执行侧的来源
```

项目保留唯一可编辑的科研原件，这里保存生成的只读副本。编号、语言权威、草稿／Unknown、
结果资格和批准状态均沿用原文；同步不授予实验权限。父子归属仍由源项目登记持有。

## 每次同步哪些材料

[profiles.json](../sync/anchors/profiles.json)逐项列出来源：当前Anchor及已有语言伴随版，
适用的Focus，必要轮次的Protocol、Summary、Detailed，以及相关的数据说明和小型来源清单。
按具体轮次选取；新轮次不抹掉旧证据。原始JSONL、检查点、激活数组和完整运行日志留执行侧，
不沿链接扩成整个项目或全部历史。

新增同步入口只是增加可读性，不激活新问题。新入口同时加入双语`sync/anchors/README`索引；
后续轮次刷新同一路径，由Git保存旧版本。已有的`sync/S000_current_specialization/`
和日期交接材料继续保留各自职责，这个目录提供按问题定位的稳定入口。

## 怎样刷新和核对

复用现有阅读包工具的来源选择、链接重定和哈希记录：

```sh
python tools/sync_anchor_reading.py --project from-attention-to-search --anchor 17_04
python tools/sync_anchor_reading.py --project from-attention-to-search --anchor 17_04 --check
```

先在临时目录生成，核对范围和来源哈希，再刷新同一目录内由工具持有的文件。
目的目录未经工具登记或副本被手工改动时，停止覆盖。研究内容需要改动时回原件修改，再生成副本。
缺失来源明确入账，服务器路径不会因为同步就变成GitHub可下载的数据。

检查原文／副本哈希、包内链接、原状态和Git载荷范围。来源没变时，不因时间过去再造快照。
`--check`供具备源项目的工作区使用；只读Research_System的agent直接读已保存的副本和清单即可。

本条是对上述范围内阅读同步的持续授权。已有适用的commit／push授权时一并发布；
否则明确说明仅已本地更新。实际推送并核对之前，不声称GitHub已可见。本次A17_04已获明确提交推送授权。

## 每轮触发与定时触发

默认在指导交付后触发，保证与本轮内容一起完成。以后若明确指定定时任务，可以补做来源变化检查，
并在原件可访问时刷新已登记入口。定时不能获得缺失仓库的权限，也不扩大实验范围。
本文没有创建定时自动化。

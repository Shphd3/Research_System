# NTP Conditional Low-Rank Theory Provenance

本文件只记录来源、唯一版本与发布边界，不改变 A14 的理论判断、claim boundary
或 next decision。

## 唯一版本规则

- `Research_System` 中唯一可编辑理论包：
  [NTP_conditional_low_rank_theory_package](NTP_conditional_low_rank_theory_package/README.md)。
- 原始 zip 是不可编辑的来源归档，不作为第二个工作版本。
- `Projects/kv_cache/xyDeng/sync/` 是用户允许保留的外部发布副本。
- 不再保留 `daily_research_reports/0724/docs/` 下的旧理论草案、兼容入口或
  theory-only 本地镜像。

## 原始来源

- zip：
  `daily_research_reports/0724/NTP_conditional_low_rank_theory_package.zip`
- SHA-256：
  `9f16514854e10299d25ebf0358f519a77eef9b4b3a19698a2d4dfd00b5056746`
- 完整性：zip CRC 检查通过，8/8 文件成功解压。

zip 保留最初交付的正文、证明附录、实验协议、先验审计、审核清单、manifest、
README 和 references。当前可编辑目录在该来源上采用了已审核的 theory-only
修正，因此不应再声称它与 zip 逐字节相同。

## 已审核发布副本

- 本地入口：
  `Projects/kv_cache/xyDeng/sync/2026-07-24/a14_ntp_conditional_low_rank_theory/`
- Git 仓库：`Frandium/kv_cache`
- 分支：`xyDeng`
- commit：`efd91334458bc301f608e2800f54d83625df7830`

唯一可编辑包中的理论正文、证明附录、物理先验审计与 references 分别对应此
发布副本；实验协议与审核清单只在 `Research_System` 中保留，未提交到
`kv_cache`。

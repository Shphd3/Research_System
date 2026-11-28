# SCO Control Training

Skill for operating SenseCore SCO CLI workflows with a compact, layered command guide. Supports both Claude Code (plugin) and Codex (manual copy).

The skill focuses on high-frequency SCO operations:

- ACP training job submit, inspect, logs, worker lookup, and quota selection
- CCI app listing, describing, and YAML creation patterns
- AEC2 cluster/spec queries
- AFS volume, directory, quota, and ACL management
- CCR/AOSS-style container image listing, build, namespace, and label workflows

The bundled references are intentionally small. They capture practical command patterns and known local CLI behavior without vendoring the full SCO documentation.

## 操作指南

- [ACP 训练设备清单与默认优先级](skills/sco-control-training/references/training-devices-cn.md)
- [RTX 5090 多节点训练与 Socket 调优](skills/sco-control-training/references/rtx5090-training-cn.md)
- [ACP 双任务互联、RDMA 和短训验收](skills/sco-control-training/references/acp-distributed-cn.md)
- [ACP、CCI 的 AOSS 挂载、多账号主桶与 AFS 对照测速](skills/sco-control-training/references/aoss-storage-cn.md)

此版本保留 [BinaryCheater/sco-skill](https://github.com/BinaryCheater/sco-skill) 的 MIT 许可和原作者署名。已同步上游通用流程至 `1d6bb6a`，并保留本仓库的训练和存储配方。

独立发布地址为 [Shphd3/sco-control-training](https://github.com/Shphd3/sco-control-training)。

## Installation

### Claude Code (Plugin)

Register the published marketplace and install the plugin:

```bash
claude plugin marketplace add Shphd3/sco-control-training
claude plugin install sco-control@shphd-sco-control
```

### Codex (Manual Copy)

```bash
mkdir -p ~/.codex/skills
cp -R skills/sco-control-training ~/.codex/skills/sco-control-training
```

Symlink for local development:

```bash
mkdir -p ~/.codex/skills
ln -s "$(pwd)/skills/sco-control-training" ~/.codex/skills/sco-control-training
```

Restart Codex or reload skills if your client requires it.

## Prerequisites

- `sco` CLI installed and authenticated in your environment

## Usage

Once installed, invoke the skill:

```text
Use sco-control-training to list my CCI apps and inspect my ACP jobs.
```

For read-only discovery, prefer:

```bash
sco acp jobs list --workspace-name "$WORKSPACE" --page-size 20 -o table
sco cci apps list --workspace-name "$WORKSPACE" --keyword "$USER_ID" --page-size 20
sco afs volume list
sco ccr images list
```

For ACP quota selection:

```bash
--quota-type reserved  # standard/reserved quota, default
--quota-type spot      # idle/preemptible quota
```

For CCI, `--keyword` fuzzy-matches `user_name`, `display_name`, and `name`, so use runtime user ids or app naming patterns as query values.

### Working with multiple accounts

Run [`sco init`](https://www.sensecore.cn/help/docs/CLI/SCO_Refrence/init) interactively to set up a named profile for each identity you are authorized to use. The global `--profile` option selects the profile for a single command.

```bash
sco config profiles list
sco --profile "$SCO_PROFILE" acp jobs list --workspace-name "$SCO_WORKSPACE" -o table
sco --profile "$SCO_PROFILE" afs volume list
```

For shared inputs, read-only access checks, and coordinating separate ACP jobs, see the [multi-account workflow](skills/sco-control-training/SKILL.md#multiple-accounts).

### Local configuration

Use `sco init` to keep AccessKeys in a local SCO profile. Copy the [environment example](skills/sco-control-training/references/sco.local.env.example) to `sco.local.env` for non-secret workspace, cluster, image and storage settings. The repository ignores that file and `cci-app.local.yaml`. Fill the files with values for your own environment and follow the [ACP preview walkthrough](skills/sco-control-training/references/run_sco_pattern.md#dry-run).

## Repository Layout

```text
.claude-plugin/
├── marketplace.json
└── plugin.json
package.json
skills/
└── sco-control-training/
    ├── SKILL.md
    ├── agents/openai.yaml
    └── references/
        ├── acp-distributed-cn.md
        ├── acp.md
        ├── acp_submit_template.sh
        ├── aec2-afs.md
        ├── aoss-storage-cn.md
        ├── cci.md
        ├── images.md
        ├── rtx5090-training-cn.md
        ├── run_sco_pattern.md
        ├── sco.local.env.example
        └── torchrun-worker.py
```

## Safety

The skill treats list/describe/log operations as the default. Mutating operations such as create, update, delete, start, stop, quota changes, ACL changes, and image builds should be run only after explicit user intent.

The ACP template previews the full command by default. Set `DRY_RUN=0` explicitly to submit after reviewing the profile and resource arguments.

## License

MIT

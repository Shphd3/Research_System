# Shphd SCO Control

Skill for operating SenseCore SCO CLI workflows with a compact, layered command guide. Supports both Claude Code (plugin) and Codex (manual copy).

The skill focuses on high-frequency SCO operations:

- ACP training job submit, inspect, logs, worker lookup, and quota selection
- CCI app listing, describing, and YAML creation patterns
- AEC2 cluster/spec queries
- AFS volume, directory, quota, and ACL management
- CCR/AOSS-style container image listing, build, namespace, and label workflows

The bundled references are intentionally small. They capture practical command patterns and known local CLI behavior without vendoring the full SCO documentation.

## 操作指南

- [ACP 双任务互联、RDMA 和短训验收](skills/sco-control/references/acp-distributed-cn.md)
- [ACP、CCI 的 AOSS 挂载与 AFS 对照测速](skills/sco-control/references/aoss-storage-cn.md)

此版本保留 [BinaryCheater/sco-skill](https://github.com/BinaryCheater/sco-skill) 的 MIT 许可和原作者署名。维护基线为本地留存的 upstream `21c7c0d`。本次无法从原地址获取较新的版本，远端最新状态待核实。

独立发布地址为 [Shphd3/sco-control-training](https://github.com/Shphd3/sco-control-training)。

## Installation

### Claude Code (Plugin)

From this checkout, register the local marketplace and install the plugin:

```bash
claude plugins:add-marketplace "$(pwd)" --name shphd-sco-control
claude plugins:install sco-control
```

### Codex (Manual Copy)

```bash
mkdir -p ~/.codex/skills
cp -R skills/sco-control ~/.codex/skills/sco-control
```

Symlink for local development:

```bash
mkdir -p ~/.codex/skills
ln -s "$(pwd)/skills/sco-control" ~/.codex/skills/sco-control
```

Restart Codex or reload skills if your client requires it.

## Prerequisites

- `sco` CLI installed and authenticated in your environment

## Usage

Once installed, invoke the skill:

```text
Use sco-control to list my CCI apps and inspect my ACP jobs.
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

## Repository Layout

```text
.claude-plugin/
├── marketplace.json
└── plugin.json
package.json
skills/
└── sco-control/
    ├── SKILL.md
    ├── agents/openai.yaml
    └── references/
        ├── acp.md
        ├── acp_submit_template.sh
        ├── aec2-afs.md
        ├── cci.md
        ├── images.md
        └── run_sco_pattern.md
```

## Safety

The skill treats list/describe/log operations as the default. Mutating operations such as create, update, delete, start, stop, quota changes, ACL changes, and image builds should be run only after explicit user intent.

The included `acp_submit_template.sh` is a sanitized reference template; it intentionally uses environment variables for workspace, cluster, storage, image, and project path values.

## License

MIT

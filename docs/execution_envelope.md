# Execution Envelope

This file is the only canonical owner of where an experiment runs, in which
image and runtime environment, through which entry point, and what a submitted
job must leave behind as a run receipt. It does not own the research question,
the protocol, or the result.

Protocols, Skills, and execution workspaces reference the keys below. They must
not keep a second copy of these values, and an agent must not invent a profile
key, an image URL, or a submission command.

## 1. Precedence

```text
protocol.md explicit declaration
  > this envelope's default
  > sco-control platform default
```

An exception (a run that must not use the default profile, quota, or image) is
valid only when the researcher writes it into the protocol together with its
reason. An agent must not introduce an exception on its own and must not
silently fall back to another profile.

This envelope's default is not an execution approval. A full or expensive run
still requires its protocol execution scope to be authorized.

## 2. Registry

This block is the only copy of these values.

```yaml
updated: "2026-09-11"
default_profile: h100-4-reserved
default_image: shphd-lite-0911

researcher_decisions:
  - date: "2026-09-10"
    scope: resource
    decision: "h100-4-reserved has first priority for experiments. H100 SPOT and 5090 SPOT are deferred: do not submit them and do not offer them as a fallback."
  - date: "2026-09-10"
    scope: image
    decision: "The default image is the self-maintained shphd image. ngc-pytorch is retired as a default and kept only to reproduce earlier runs."
  - date: "2026-09-10"
    scope: image
    decision: "The researcher saves new images and announces them; an agent registers the new key here after that announcement and never promotes or guesses an image on its own."
  - date: "2026-09-11"
    scope: image
    decision: "shphd-lite-0911:shphd-mig-20260910161423 is the newest image and becomes the default. Earlier images stay registered so old runs remain reproducible; they are not the default."
  - date: "2026-09-11"
    scope: submission
    decision: "The ACP submission entry point is verified working from the new container. The private CCR image listing hangs there, so an image URL is registered only from the researcher's announcement, never discovered by listing."

profiles:
  h100-4-reserved:
    status: default
    surface: acp
    workspace: share-space
    aec2: share-cluster
    worker_spec: n6ls.iu.i40.4
    worker_nodes: 1
    worker_processes: 4
    gpus: "4x H100 80GB SXM5"
    quota_type: reserved
    priority: normal
    storage_mount: "01995892-d478-76d8-aec7-13fd8284477e:/data"
    gpu_used: true
  h100-1-reserved:
    status: requires_explicit_selection
    surface: acp
    workspace: share-space
    aec2: share-cluster
    worker_spec: n6ls.iu.i40.1
    worker_nodes: 1
    worker_processes: 1
    gpus: "1x H100 80GB"
    quota_type: reserved
    priority: normal
    storage_mount: "01995892-d478-76d8-aec7-13fd8284477e:/data"
    gpu_used: true
  h100-4-spot:
    status: deferred
    deferred_on: "2026-09-10"
    surface: acp
    workspace: share-space
    aec2: share-cluster
    worker_spec: n6ls.iu.i40.4
    worker_nodes: 1
    worker_processes: 4
    gpus: "4x H100 80GB SXM5"
    quota_type: spot
    priority: normal
    storage_mount: "01995892-d478-76d8-aec7-13fd8284477e:/data"
  "5090-8-spot":
    status: deferred
    deferred_on: "2026-09-10"
    surface: acp
    workspace: share-space
    aec2: computing-cluster-5090-01g
    worker_spec: n12lp.nn.i10a.8
    worker_nodes: 1
    worker_processes: 8
    gpus: "8x RTX 5090 32GB"
    quota_type: spot
    priority: normal
    storage_mount: "01995892-d478-76d8-aec7-13fd8284477e:/data"
  cpu-only-local:
    status: restricted
    surface: local_or_container
    limit: "smoke, environment checks, and read-only analysis of at most 60 minutes"
    gpu_used: false

images:
  shphd-lite-0911:
    status: default
    url: "registry.cn-sh-01g.sensecore.cn/ccr-zhicheng-03/shphd-lite-0911:shphd-mig-20260910161423"
    interpreter: "Python 3.10"
    torch: "2.3"
    cuda: "12.4"
    numpy: "1.24.4"
    os: "Ubuntu 22.04"
    activation: "the experiment runtime.sh or the shared activation script; never install into the base environment"
    announced_by: "researcher, 2026-09-11: shphd-lite-0911:shphd-mig-20260910161423"
    verified_by: "2026-09-11 ACP job pt-qk9pkesv on h100-4-reserved: URL accepted, image pulled, 4x H100 80GB HBM3 visible, Python 3.10.12, torch 2.3.0a0+6ddf5cf85e.nv24.04, CUDA 12.4, torch.cuda.is_available True, numpy 1.24.4, /data mounted, exit 0"
    note: "The private CCR image listing hangs in this container, so this URL cannot be re-derived by listing. It is confirmed by the run above; if a future pull fails, ask the researcher for the full URL instead of editing it here."
  shphd-lite-0710:
    status: superseded
    url: "registry.cn-sh-01g.sensecore.cn/ccr-zhicheng-03/shphd-lite-0710:container1-20260710154849"
    interpreter: "Python 3.10"
    torch: "2.3"
    cuda: "12.4"
    numpy: "1.24.4"
    activation: "the experiment runtime.sh or the shared activation script; never install into the base environment"
    verified_by: "A15_08 E02/E06 H100 pair; 2026-09-10 reserved analysis pod"
    note: "Replaced by shphd-lite-0911 as the default. Runs that were qualified under it keep reproducing with it."
  ngc-pytorch-25-06:
    status: superseded
    url: "registry.cn-sh-01.sensecore.cn/lepton-trainingjob/ngc-pytorch:25.06-cu12.9-py3.12-ubuntu24.04"
    interpreter: "Python 3.12"
    torch: "2.8"
    cuda: "12.9"
    note: "Used by A6R1 pt-b9r9id8m and earlier A15 protocols. Keep to reproduce those runs; do not pick it for a new run."

legacy_profiles: [local-2xh100, local-2xh100-remote-8x5090-fallback, cpu_cached_activation_analysis_no_gpu, h100-1-spot-user-selected]

legacy_images:
  shphd-private-lite:
    url: "registry.cn-sh-01.sensecore.cn/ccr-zhicheng-03/shphd-private-lite:container1-20260523142552"
    note: "replaced by shphd-lite-0710 in the A15_08 E01 to E02 change; history only"

submission:
  entry_point: "/data/250010109/MoE_Router/experiments/20260808_online_spectral_router_30b_v1/scripts/sco_acp_compat.sh"
  resolver: "./researchctl envelope [--profile KEY] [--image KEY] [--format shell]"
  template: "templates/execution/acp_submit_template.sh"
  note: "sco is not on PATH. The entry point starts a local management proxy, sets SCO_ZONE=cn-sh-01g with the subscription and resource group, then calls the ACP component. Verified working 2026-09-11. The private CCR image listing hangs in this container, so never try to discover an image URL by listing; read it here."
  required_gates: [DRY_RUN=0, ALLOW_SUBMIT=1, PROTOCOL_APPROVED=1, SMOKE_GATE_PASSED=1 for a full run]
  preflight: "print the resolved tuple and compare it field by field with the selected profile; refuse any mismatch"
  default_mode: "the template's default is DRY_RUN=1, which prints the tuple and the command and creates nothing"
```

Legacy keys are recognized historical values. They do not warn, and they must
not be reused for a new run. A protocol that records neither a registry key nor
a legacy key is a drift case, not an exception.

## 3. Routing

| Work | Profile | Note |
| --- | --- | --- |
| GPU training, condition matrices, formal full runs | `h100-4-reserved` | The default, and the researcher's stated first choice. No separate confirmation is needed once the protocol's execution scope is authorized. |
| Single-GPU evaluation or reproduction | `h100-1-reserved` | Only when the protocol or the current instruction names it. |
| Long CPU chain over 60 minutes: analysis, bootstrap, clustering, rendering | `h100-4-reserved` | The reserved node is used for its core count and because it is not recycled every four hours. The receipt must record `gpu_used: false`. |
| Local or container work | `cpu-only-local` | Smoke, environment checks, and read-only analysis of at most 60 minutes. A collaboration container is recycled after about four hours, so no long computation belongs inside it. |

The 2026-09-10 record that the SFT matrix analysis chain never used its four
H100, and that the reserved node was worth re-submitting only for a new training
batch, is why the CPU row states `gpu_used: false` instead of claiming GPU
value. It is not a reason to route CPU work elsewhere.

## 4. Protocol fields

A protocol that will be executed declares:

```yaml
execution_surface: acp
resource_profile: h100-4-reserved   # a key in Section 2
image_id: shphd-lite-0911           # a key in Section 2; omit to inherit default_image
env_layer: <activation script or dependency layer>   # optional
```

A protocol does not inline the image URL or the storage mount. Submission
expands the keys, and the receipt records the expanded values. A protocol that
declares none of these keys is not yet executable.

Because a new image becomes the default by moving `default_image`, a protocol
that omits `image_id` follows the default. Name `image_id` explicitly only when
the run must keep reproducing under one exact image.

## 5. Run receipt

Submit through `templates/execution/acp_submit_template.sh`. It resolves the
tuple with `./researchctl envelope`, prints it, defaults to `DRY_RUN=1`, enforces
the gates, and writes a submission receipt. Point `REMOTE_DIR` at the
experiment's own workspace and `RUN_ROOT` at its run root; the repository
defaults exist only for a quick verification.

Every submitted job leaves a receipt with the fields of
`templates/execution/run_receipt_template.md`. The receipt records the expanded
image URL, the resolved tuple, the submission entry point and exact command, the
activation script, the artifact roots, whether the GPUs were used, and which
agent and conversation owns monitoring. A receipt that omits the expanded image
cannot certify what actually ran.

The platform keeps no stdout from a finished pod, so `stream-logs` returns only
the scheduling line. The submit template tees each run's output into
`<REMOTE_DIR>/acp_receipts/pod/`; a run without that log has no durable evidence
of what it did.

## 6. Agents

This envelope is written once and is read the same way by every agent. Skills
are discovered from `.agents/skills/`; `.claude/skills` is a symbolic link to
it, and the DeepSeek harness discovers `.agents/skills/` directly. Do not
maintain an agent-specific copy of these values.

- One run root has exactly one monitoring owner. Record that owner in the
  receipt. A conversation that takes over receives the owner role explicitly,
  and the previous owner stops its polling first.
- Monitor with managed background jobs. Do not create a session-local scheduled
  task: a 2026-09-09 record shows such a task re-entering a run root whose
  receipt already existed and racing a new conversation over the same output
  directory.
- Report only a state change, a failure, a required human action, or a deadline
  risk. Silence means unchanged.
- Cross-conversation context stays in
  `.research/memory/conversations/<conversation>/memory.md` with its
  `Processed by` field. A successor never rewrites a predecessor's receipt.

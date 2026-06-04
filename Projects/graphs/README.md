# Research Graph Hub

This directory stores Sidecar-readable graph manifests for cross-project
research navigation.

Workspace for Sidecar:

```text
/data/250010109/Research_System
```

Current graph manifests:

```text
Projects/graphs/expert_specialization.graph.yaml
Projects/graphs/kv_cache_retrieval.graph.yaml
Projects/graphs/specialization_papers.graph.yaml
```

Ownership:

```text
Projects/graphs/                 cross-project graph navigation layer
Projects/from-attention-to-search current expert-specialization work branch
Projects/kv_cache                 primary mainline project
paper_reading/                    literature notes linked by paper subgraphs
```

Rule:

The graph is thin. Nodes should summarize ownership, linked anchors,
experiment records, and result status. The full reasoning stays in the linked
anchor, `summary.md`, `detailed.md`, or report card.


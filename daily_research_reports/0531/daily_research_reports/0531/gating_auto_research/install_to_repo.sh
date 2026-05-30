#!/usr/bin/env bash
set -euo pipefail

# Run from Research_System repo root after reviewing files.

SRC_DIR="daily_research_reports/0531/gating_auto_research"
ANCHOR_SRC="$SRC_DIR/anchor/route_function_binding_stable_gating_anchor.md"
EXP_SRC="$SRC_DIR/experiments/0531_auto_route_function_binding"

ANCHOR_DST="Projects/from-attention-to-search/main/problem_anchors/gated_main_causes/route_function_binding_stable_gating_anchor.md"
SYNC_DST="sync/S000_current_specialization/anchors/expert_specialization/route_function_binding_stable_gating_anchor.md"
EXP_DST="Projects/from-attention-to-search/main/experiments/0531_auto_route_function_binding"

mkdir -p "$(dirname "$ANCHOR_DST")" "$(dirname "$SYNC_DST")" "$EXP_DST"
cp "$ANCHOR_SRC" "$ANCHOR_DST"
cp "$ANCHOR_SRC" "$SYNC_DST"
cp -R "$EXP_SRC"/* "$EXP_DST"/

echo "Installed anchor and experiment plan. Review graph_update_proposal.md before editing graph.yaml."

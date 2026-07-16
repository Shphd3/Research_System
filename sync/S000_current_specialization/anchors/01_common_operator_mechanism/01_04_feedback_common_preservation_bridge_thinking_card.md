# Thinking Card — Feedback Common Preservation Bridge Anchor

> Migrated from [01_04_feedback_common_preservation_bridge_anchor.md](01_04_feedback_common_preservation_bridge_anchor.md) without changing the historical judgment. This file is the human-facing source; the anchor owns formal design and evidence.

**Phenomenon:** Real-DCLM proxy routing can be aligned at step 0, but ordinary
training erases the proxy partition by step 5/10.

**Mechanism guess:** Training introduces or amplifies a shared feedback drift
that pushes gate inputs toward a common-margin direction. This feedback common
can overwrite route-relevant residual structure even when the step-0 proxy
router is valid.

**Key variables:** Step-0 hidden state $h_0$, later hidden state $h_t$, drift
$\Delta h_t=h_t-h_0$, feedback projector $P_{\mathrm{fb}}$, proxy labels,
router logits, proxy-route NMI, common margin, and residual drift.

**Causal relation:** If feedback common is the preservation failure mechanism,
then replaying $P_{\mathrm{fb}}\Delta h$ should explain most of the step-0 to
step-5/10 proxy-route NMI collapse, while removing
$P_{\mathrm{fb}}\Delta h$ from the full drift should rescue the proxy route.

**Observable metric:** `proxy_nmi_drop_explained_by_feedback_common`, the
fraction of full proxy-route NMI drop reproduced by replaying only the
feedback-common drift.

**Rival Explanations:** Proxy labels may be invalid; collapse may be caused by
group-specific residual drift, expert feedback, optimizer geometry, route-load
imbalance, or activation nuisance rather than shared feedback drift.

**Decision:** If feedback-common replay explains the proxy-route collapse and
feedback-common removal rescues it in controlled settings, carry the bridge to
bounded real-DCLM artifacts. If the real gate-logit bridge fails, decompose the
collapse into gate-weight drift, hidden-state drift, and expert-update feedback
before proposing a method.

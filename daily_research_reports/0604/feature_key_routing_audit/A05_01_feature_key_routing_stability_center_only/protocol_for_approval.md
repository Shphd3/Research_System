# Protocol For Approval: A05_01_feature_key_routing_stability_center_only

Goal:
Test whether routing is stable for each concrete feature key $(slot_id=s,b_id=i)$.

Decision question:
In uniform multi-B synthetic, do random init, slot init, and center separation only make the same feature key route to the same expert without collapse?

Tested hypothesis:
If the router learns stable feature-key boundaries, then for each feature key $(s,i)$, $\max_e P(e\mid s,i)$ should be high across eval variants and checkpoints.

Rival explanation:
High consistency may be caused by single-expert collapse, deterministic duplicate eval, slot-only routing, or B-identity routing.

Data:
Reuse 05_01 uniform multi-B synthetic with feature key $(s,i)=(slot_id,b_id)$. Add eval variants $x_{s,i,r}$ when possible.

Model:
SparseTinyTransformer, 4 experts, router bias disabled.

Routing / algorithm:
Dot-product or cosine selected-gate top-1 router.

Loss / objective:
NTP only or NTP + router center separation only. No feature separation objective. No supervised token margin.

Conditions:
R0-dot, R1-dot, S0-dot, S1-dot, R0-cos, R1-cos, S0-cos, S1-cos.

Checkpoints / seeds:
Seeds 20260521, 20260522, 20260523. Check step 0, mid checkpoints, and final.

Primary metric:
FeatureKeyConsistency = mean over $(s,i)$ of $\max_e P(e\mid s,i)$.

Secondary metrics:
Expert load entropy, feature-key route matrix, consistency histogram, route-slot NMI, route-B NMI, target accuracy, checkpoint feature drift.

Known good case:
High feature consistency with non-collapsed expert load and stable per-seed behavior.

Known bad case:
High feature consistency caused by all keys routing to one expert.

Known confusing case:
High consistency from deterministic duplicate eval without variants; this cannot prove sample-level robustness.

Success:
Center-only slot-init condition improves consistency over NTP-only baseline, avoids collapse, preserves target accuracy, and succeeds across seeds.

Failure:
No improvement over baseline, single-expert collapse, one-seed-only success, large checkpoint drift, or deterministic duplicate-only success.

What this cannot claim:
It cannot prove expert utility specialization, real-data transfer, or feature separation between different keys.

User approval checklist:
User has requested direct execution after plan writing.

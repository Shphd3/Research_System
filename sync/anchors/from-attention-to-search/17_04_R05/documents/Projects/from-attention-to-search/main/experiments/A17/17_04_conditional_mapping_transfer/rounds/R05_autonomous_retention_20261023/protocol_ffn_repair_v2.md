派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R05_autonomous_retention_20261023/protocol_ffn_repair_v2.md`。
[精确原始文件](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A17/17_04_conditional_mapping_transfer/rounds/R05_autonomous_retention_20261023/protocol_ffn_repair_v2.md)；研究修改仍回到原件。

---

# R05 full native FFN qualification repair V2

Status: authorized single qualification repair; pre-run registered at 2026-10-22T16:41:48.065251+00:00. Original down-only D/E/F results stay under runs/D,E,F; repair writes only runs/repair_full_ffn. This supplement amends the owning protocol, creates no new scientific owner, and records AI operational choices within the researcher’s explicit V3 delegation. Scientific acceptance/closure remain Unknown.

## Trigger and purpose

Original ordinary two-expert down-only model ended old100%,new74.125%; preselected shared multi_normal ended old100%,new74%; weakest command/panel was59%, below95%. Single residual normal/protected ended old85.5%,new43.25%,weakest26%. A TRAIN subset also showed incomplete new fitting, so ordinary failure cannot identify a sharing or router failure. One joint qualification repair is now used: expand trainable native FFN scope, without increasing learning rate, steps or choosing an outcome-favored spectral direction. The new test asks whether the intended structure can operate with a trainable native nonlinear FFN. It cannot establish that any one additional projection was necessary.

## Model and inputs

Use the exact same registered Base+acquired-old four-attention adapter and unchanged TRAIN/DEV record order. Last-layer self-attention stays frozen. Cache h after attention, and x=original post_attention_layernorm(h),1024 dimensions. Each expert computes gate(x), up(x), their native SiLU-product, and down projection. For each of gate/up/down weights independently, fixed top16 paired singular matrix atoms define P; effective weight is W0 plus shared C coefficients plus projected complementary private residual. Composition occurs inside each original linear projection before its native nonlinearity; there is no linear splitting of the whole nonlinear FFN. Initial increments0, so all experts reproduce W0.

D retains all five arms ordinary two independent FFNs, sharedC+singleR normal/protected, sharedC+twoR normal/protected. Same zero-increment start,1200updates,20answers/update,seed29,AdamW1e-4,clip1,FP32. Protection scales actual Adam displacement for C coefficients .1 to.01; complement remains normal. Full three-projection dense parameters are9,437,184/expert, versus3,145,728 down-only. Active/total parameters and forward/training FLOPs are reported separately. Different parameterization/total capacity remain named rivals. No new direction/rank search.

E fixes the repair multi_normal endpoint1200 regardless of its score. If it still fails95% each cell, further tuning stops; E remains an explicitly unqualified-expert diagnostic. Full router reads x1024; candidate summary reads16 right-singular gate directions of initial W0, random summary uses a fixed orthonormal16 frame. These are operational inputs available before expert selection. All three use Linear(input,64),SiLU,Linear(64,2); the full router has more parameters, disclosed, and candidate/random16 control equal capacity. Native x no longer includes the original fixed gate/up nonlinearity, motivating the common64-unit router hidden layer before outcomes. Same600fixed+600joint,hard-top1 straight-through surrogate,coeff.01load loss,known-mode and balanced-random references,exact load-permutation readout. All affected E comparisons rerun, not only a method. No mode or target enters learned router inputs.

F retains exactly the same frozen128TRAIN/64DEV DCLM documents,128token windows,127targets/document,source/tokenizer/text/window hashes. Derive x from saved native h, binding old cache SHA and new config SHA. No new document selection. Rerun all four dense-normal/protected,ordinary2/shared2-protected natural continuations for400updates,20tokens/update, plus retained list old/new readings. Natural heldout CE has no95% list qualification rule. All structural endpoints also receive natural readouts; known-mode routes have no natural-mode truth, so read both experts and an equal-probability predictive mixture under that explicit name.

## Qualification, controls and stop

GPU no-op/gradient/finite-count/frozen checks, independent next-step resume and required core+aux TB tags must pass before affected full comparisons. Every list command/mode/panel must reach95% for competence, unchanged. Ordinary competence failure leaves structural utility insufficient; no second scientific configuration repair is allowed. Engineering mistakes may be fixed with preserved failure receipts and only affected unit reruns. Primary endpoints fixed1200/600/400. No early favorable checkpoint selection, threshold change or best-arm substitution. Original F and repaired F are separate model scopes, never pooled.

## Scheduling and authority

Use the existing four single-H100 Reserved workers; no new allocation, node, image or profile. Original0/A–F minimum attempts complete before A/B order repeats; independent A/B repeats may proceed while the one FFN repair is implemented, then share the same locked queue with it. All affected repair cases are required before overall delivery, regardless of queue’s minimum/repair scheduling flag. Source snapshots, exact new config and task freezes precede repair outcomes. Publish no paper/Git/external content.

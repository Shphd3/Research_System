# A15_13_06: Can a DCLM-Trained Final-Layer Top-K SAE Become a Qualified Hierarchical-Semantic Teacher Candidate?

## 1. Problem Definition

The parent problem is to determine where coarse and parent-conditioned fine semantic responsibilities first become readable across the depth of frozen Qwen3-0.6B-Base. Gold M2D2 labels provide the stable supervised audit, but the intended unsupervised teacher is a sparse autoencoder (SAE): a learned dictionary that reconstructs a model state using only a small number of active features per token. The blocking uncertainty is whether a trainer matching the senior project's object can first be made reproducible on DCLM without changing the base model, activation site, or data identity. The immediate decision is whether the smoke-trained final-layer SAE passes its engineering qualification gates and may proceed to a separately approved full training and hierarchy audit. Pass permits only scale-up planning; Fail requires repairing the named failed gate; Insufficient means the data, model, hook, checkpoint, or run receipt cannot be verified.

## 2. Physical Priors

The human-confirmed prior is that reusable semantic structure may be represented by sparse combinations of features rather than by one geometric cluster center. A Top-K SAE exposes this candidate structure by forcing each token state to use only a fixed small number of dictionary features. This prior is falsified for the present implementation if the exact router-input state cannot be reconstructed better than a zero output, features collapse, or the checkpoint cannot be reproduced after reload. These are trainer-qualification falsifiers, not evidence that the learned features are semantic.

## 3. Falsifiable Hypotheses

The primary smoke hypothesis is that a 30,000-feature, Top-32 SAE trained on the final-layer MLP input of frozen Qwen3-0.6B-Base can reduce held-out normalized reconstruction error while preserving finite optimization, non-collapsed feature use, exact checkpoint reload, and zero trainable base parameters. The strongest rival is an implementation-only appearance of learning: loss changes because of data leakage, an incorrect hook, invalid token IDs, collapsed features, or a non-reloadable checkpoint. Passing the smoke weakens only this rival and does not establish a feature hierarchy or coarse/fine semantics.

## 4. Mathematical Model

For one final-layer MLP-input state $x\in\mathbb{R}^{1024}$, the encoder produces nonnegative activations and retains the largest 32 values:

$$
z=\operatorname{TopK}_{32}(\operatorname{ReLU}(W_{\mathrm{enc}}x+b_{\mathrm{enc}})),
\qquad
\hat{x}=W_{\mathrm{dec}}z+b_{\mathrm{dec}}.
$$

The primary smoke quantity is normalized reconstruction mean squared error,

$$
L_{\mathrm{recon}}=\frac{\mathbb{E}\lVert x-\hat{x}\rVert_2^2}{\mathbb{E}\lVert x\rVert_2^2}.
$$

A zero reconstruction has value one. A value below one and lower after training than before training shows that the trainer learned a nontrivial reconstruction on held-out DCLM states. It cannot show semantic meaning, hierarchy, Router usefulness, expert utility, or language-model improvement.

## 5. Computational Realization

The base model is the same frozen 28-layer Qwen3-0.6B-Base used by E14. Tokens come from the frozen uint32 DCLM view tokenized for Qwen3. Each process captures zero-based layer 27's `decoder_layer.mlp` forward pre-hook tensor, which has final dimension 1,024. Four data-parallel H100 processes train replicas of one SAE and synchronize SAE gradients; the base model remains replicated, evaluation-only, and absent from the optimizer. The smoke uses one frozen training shard and the separately designated DCLM validation shard. M2D2 labels are absent from this stage.

## 6. Minimal Falsification Tests

The decisive smoke comparison is held-out normalized reconstruction error before versus after 100 optimizer updates, guarded by the zero-reconstruction reference of one. Pass requires all registered gates: exact model shape and hook count, valid token range, frozen base, finite train and validation losses, final held-out error below both one and its initial value, approximately 32 positive activations per token, more than 32 features used, no NaN or out-of-memory failure, and exact checkpoint reload output. Fail means any verified gate is false. Insufficient means the job, artifacts, or identities cannot be audited. No smoke outcome licenses full training without a separate approval.

## 7. Current Evidence

Verified inputs exist: the local model has 28 layers and hidden width 1,024; the frozen DCLM view records 302,089,493,820 uint32 training tokens and a separate 114,988,106-token validation file; the senior project identifies the relevant tensor as the decoder-layer MLP forward pre-hook and describes approximately 30,000 features with 32 active per token. In four-H100 reserved job `pt-mt4s38xi`, every registered smoke gate passed. Held-out normalized reconstruction error decreased from `0.7890049927` to `0.3367877454` after 100 updates, all held-out tokens had 32 positive retained features, 19,614 of 30,000 features fired, the frozen base had zero trainable parameters, and checkpoint reload had maximum absolute output difference `0.0`. The measured training-loop throughput was `121,627.76 token/s`. An earlier attempt, `pt-uqiufy7f`, was insufficient only because the reloaded module remained on CPU while the probe was on GPU; the full rerun after the device-placement repair passed.

## 8. Claim Boundary And Next Decision

The present evidence establishes only that the concrete SAE training and checkpoint pipeline is technically eligible for scale-up. It cannot establish that individual features are interpretable, that implication edges form a semantic hierarchy, that hierarchy depth corresponds to coarse versus fine domains, that any layer is optimal for Router or LoRA insertion, or that downstream task performance improves. The one next decision is whether to approve a separately frozen 1B-token DCLM run, projected at `2.28 h` of pure training and `2.7–3.0 h` of reserved-node wall time. Full training remains unauthorized until that human decision is recorded.

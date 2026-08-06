# A15_03 Thinking Card: Matched Band-Dispatch Effect

- **Current judgment:** Static geometry and one-step compatibility cannot replace joint training. A complete causal band ablation can still measure distributional effect, benefit, or harm even though the old fixed-band compatibility gate failed.
- **Mechanism:** Restricting the Router to a frozen band changes token-to-expert assignments, which changes expert updates, load, and representation feedback.
- **Strongest rival:** Any effect is generic dimensionality reduction, load mismatch, or extra computation; true covariance bands do not beat equal-rank random subspaces.
- **Evidence that changes the judgment:** Paired 2B-token continuations from the same model, optimizer, data cursor, and RNG state, comparing each true band with its equal-rank random projector.
- **Next decision:** retain only bands that affect routing and improve held-out quality beyond their matched random control; otherwise close fixed covariance-rank routing.


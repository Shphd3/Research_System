# A14_E03 Summary: Strong Tree Geometry, but the Propagation Bound Is Vacuous

## Direct Result

**Verdict: insufficient.** The primary pretrained Qwen model passed every
registered leaf, composition, emergence, capability, and sample-shape clause,
but failed the decisive non-vacuity guard: its one-step theorem bound was
10.80 times the centered parent-state norm.

Qwen final-layer results:

- leaf 95%-energy rank: 24/896 (2.68%);
- held-out leaf projection error: 0.0489;
- true-versus-matched leaf advantage: 27.7%, 95% interval [21.4%, 34.6%];
- identical-initialization leaf advantage: 20.1%, giving a 7.54-point training
  increment;
- true parent composition error: 0.489 versus 1.461 after length-binned child
  permutation;
- composition advantage: 66.5%, interval [63.8%, 69.1%], 21.3 points above
  initialization;
- theorem bound ratio: 10.80, so the theorem cannot explain the observed rank.

![Pretrained geometry and theorem guard](tree_geometry_advantages.png)

## Replication Boundary

Pythia also showed final tree-specific leaf (21.3%) and composition (60.7%)
advantages. But its leaf advantage was only 1.27 points above initialization,
and its composition advantage was 8.56 points *below* initialization. Its bound
ratio was 1.77. Thus tree-related predictability is robust, while a
training-created shared-linear mechanism is not replicated.

## Conclusion

The data support this narrow observation: independently encoded gold spans and
true parent-child edges have distinctive geometry in both decoders. They do
not support the stronger mechanism claim that stable low-rank linear
propagation generates that geometry. A large fraction is already present in
random architectures, and every registered pretrained theorem bound is
vacuous.

## Next Decision

Use a paired from-scratch hierarchy intervention to determine whether changing
tree alignment changes learned geometry under identical architecture,
initialization, token multisets, and minibatch indices.


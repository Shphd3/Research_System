# First-direction update: separate projection from a fixed offset

The doubled activation count after raw-H direction removal is dominated by the fixed offset introduced in the frozen centering coordinates. This identifies components of the measured operation. It neither repairs an implementation bug nor establishes common semantics or learning benefit. The original intervention intentionally removed an uncentered raw-H direction; its results remain intact. This control was separately registered after observing primary sensitivity.

Hold8182 measurement positions,14 saved raw directions, the CrossCoder, original TRAIN mean mu, scale r and gate fixed. For one layer and position, write hidden state h as a column vector; mu and v have the same dimension, and r is the layer's positive scalar scale. Raw removal in normalized coordinates combines projected centered variation with an additional fixed vector:

\[
\frac{Ph-\mu}{r}=P\frac{h-\mu}{r}-\frac{(\mu^\top v)v}{r},
\qquad P=I-vv^\top.
\]

The mean-preserving control retains only the first term. Original/raw-removal/mean-preservingL0 values are249.527/512.147/232.604. Conditional on the same projection, the offset adds279.543 active features per position; centered-direction projection decreasesL0 by16.923 relative to original. Their sum is the raw operation's net increase262.620. Original/mean-preserving event Jaccard is0.81887 versus0.39406 for original/raw removal. This sample supports the pre-control prediction that offset-dominated increases should move toward originalL0 and improve event overlap when the mean is preserved.

The computational chain has a concrete encoder consequence. The offset produces feature-specific constants before ReLU and the threshold. Using FP32 master encoder weights, its two largest positive shifts are exactly the heatmap's continuous-stripe features13964(+0.35395) and14(+0.19740). BF16 rounding and nonlinear gating prevent equating these values to exact gated-z differences; the direct mean-preserving intervention provides the functional readout.

The direction is not thereby safe to remove. Mean normalized reconstruction squared-vector error, averaged over positions per layer and then across14 layers, is0.03946/0.29878/0.22134 for original/raw/mean-preserving. The mean-preserving version remains worse than original at every source layer. On the same28,379 old edges estimable in all three conditions, meanphi is0.23734/0.20189/0.27361. Increased correlation does not replace reconstruction or learning evidence; no random-direction control establishes directional specificity.

Retain the judgment that deleting a direction under frozen preprocessing includes its effect on centering coordinates, beyond the removed energy alone. Abandon interpreting increasedL0 directly as more content features or identifying the direction as removable common semantics. What the direction represents and whether any treatment helps prediction or learning remain unmeasured. The main learning inputs stayed unchanged; no projected training was run.

Independent checks confirm unchanged hashes of all six primary files, exact original/raw-removal counts and selected heatmap reproduction, and recomputedL0/common-edge phi. Maximum numerical identity error is about6.2e-6 under this floating-point implementation. No primary endpoint was replaced.

# Next shallow-narrow / deep-wide model: accounting sketch, NOT RUN

This is an **AI proposal** that makes the advisor's width intuition computable. It has not been implemented, trained or forward-verified. Whether it is worth training remains a researcher decision after this round. Its parameters are accounting evidence, not evidence of learning benefit.

Keep eight layers in stages of 3/2/3. Residual widths are 512/768/1024; expert SwiGLU widths 768/1152/1536; expert counts 6/8/10; top-2 throughout. Query/KV heads are 8/4,12/6,16/8, with head dimension128. This retains the baseline relation between attention projections and residual width: Q output2h, K/V each h. Bias-free attention matrices have6h² parameters, Q/K normalization adds256, and the two block norms add2h. Every expert has3hm parameters; the router hashE.

Preserve the single tied151,936×1024 embedding/output matrix. Map its token embeddings through a bias-free1024→512 input projection. After layer3 map the whole residual stream512→768; after layer5 map768→1024. Residual additions inside a block remain same-dimensional; the transitions occur only between blocks. The final norm and output interface remain1024, so there is no additional untied vocabulary head. All three projections are trainable and counted. Their optimization stability has not been tested.

The complete per-layer ledger is [next_width_sketch_parameters.csv](next_width_sketch_parameters.csv); the readable table is in the [Chinese companion](next_width_sketch_cn.md).

| Component | Parameters |
| --- | ---: |
| Eight blocks |235,996,160|
| Tied embedding/output head, counted once |155,582,464|
| Input1024→512 |524,288|
| Transition512→768 |393,216|
| Transition768→1024 |786,432|
| Final RMSNorm |1,024|
| **Total/trainable** |**393,283,584**|

This is114,705,408 fewer parameters than507,988,992, approximately22.58%; it is not an order-of-magnitude compression. Although the expert count remains64, expert widths and selected compute change, so this is not an equal-capacity A/B arm. It would need its own matched-capacity/compute baseline, projection initialization, attention-interface and stability checks, and appropriate semantic tasks. Status: `FORMULA_ONLY_NOT_RUN`.

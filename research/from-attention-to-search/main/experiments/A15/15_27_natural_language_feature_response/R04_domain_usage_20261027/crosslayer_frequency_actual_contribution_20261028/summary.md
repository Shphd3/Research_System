# Question

How much actual cross-layer reconstruction-norm contribution do globally high/low-frequency features make in real math/biology text, and does that profile vary by domain?

# Answer

With native A22 shared joint z and all16384coordinates, high-frequency members have larger zero-inclusive equal-member contributions at all14covered blocks in both domains. Conditional on activation, low-frequency members are stronger on average; high-frequency advantage accompanies much greater occurrence. Atblock27, math high/low mean contributions are .001879/.000067, biology .001885/.000104 in training-normalized units. Domain high-minus-low differences are larger in biology atblocks1–21(11readouts), with42-testBH correction; domain differences atblocks23/25/27 remain insufficient. Decoder parameters do not change with text.

Native scales materially affect depth curves. Math low-frequency mean changes .000124→.000067 in training units but .001144→.024955 in model units, block1→27. Low-frequency norm-sum shares generally decrease, with a local late biology rebound; no uniform deeper-is-more-low-frequency pattern is established.

# Progress

Existing native z, globalDCLMgroups, decoder norms and training scales were reused. New statistics cover40real heldout documents,160positions each, all14layers, per-feature diagnostic/factor tables and all-layer comparisons. No forward, training, dictionary, candidate selection or Attention grouping. Shared z is not layer-independent activation; fixed per-feature decoder profiles cannot show first formation or dynamic migration. Exploratory reused-heldout evidence only. [Detailed Chinese](/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R04_domain_usage_20261027/crosslayer_frequency_actual_contribution_20261028/detailed_cn.md) owns complete numbers and boundaries.

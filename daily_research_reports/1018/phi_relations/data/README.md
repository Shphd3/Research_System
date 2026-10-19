# Table guide and limits

all186_group_index.csv contains all 186 frozen nonsingleton groups. all_members_frequency.csv contains all 13,807 members, exact binary hit counts n_D/n_V, full position denominators N_D/N_V and proportions p_D/p_V. Per-member percentages in reading tables are rounded; CSV values retain precision. Group IDs remain original D IDs.

Saved D/V matching stability is copied from original matches.csv and groups_V.json. Jaccard is intersection divided by union of those member sets; it measures community reconstruction agreement, not document independence, semantic stability, or learning compatibility. membership_review_G*.csv lists retained, departing and arriving members in each saved matched pair.

The new core decomposition uses min(3,m) D-selected nodes. For groups of size 2 or 3 the core therefore covers every member: a zero outside-core sum is a set identity and cannot count as evidence that a few exceptional nodes explain the group. rest_fraction is a signed covariance-sum ratio, not a nonnegative variance attribution. Positive and negative terms and the original denominator are retained in all186_core_decomposition.csv.

The 45 illustrative positions, 12 chain positions, 32,000-position decoder panel, 30,014-position conditional support, complete V and historical winner-selected hidden spectra have different populations. They must not be joined by row number or combined by multiplying fractions. Cases use any-member hits; old spectra use the original winner rule.

Each CSV is either copied from the named execution owner or deterministically derived by code/build_report.py. Exact input paths/digests, raw-cache boundaries and full definitions are in ../methods_cn.md and ../provenance/input_manifest.json. NA or undefined quantities remain missing, never zero.

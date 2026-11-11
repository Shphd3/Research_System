# R06 A5 continuation to the native1B optimizer step

AI analysis; researcher judgment Unknown. A5 continued the complete R04 update-2000 state for1816updates to update3816, read from the native baseline's1B manifest. A5 processed1000341504validtokens versus1000000000for the original baseline, a0.03415% difference. Model, optimizer, scheduler, RNG, cursor and bias were retained. H100microbatch16/accumulation2, or authorized5090microbatch8/accumulation4, retains262144validtokens per update.

| pair            | band    |   difference |    ci95_low |   ci95_high |   documents |   replicates |
|:----------------|:--------|-------------:|------------:|------------:|------------:|-------------:|
| A5-MoE_baseline | overall |  -0.01630202 | -0.01911774 | -0.01267266 |        1871 |         2000 |
| A5-Dense        | overall |  -0.10852696 | -0.11271646 | -0.10355351 |        1871 |         2000 |

P10: 支持. Native-trajectory P12 remains insufficient because the exact native update-2000 checkpoint was not retained. The R03 full-batch A0 proxy yields post-window Jaccard0.281250, compared with prior-pair median0.630952; its numeric branch is 支持. Historical partial masks and different window durations remain confounds.

A5 endpoint NLL3.763121999, native3.779426355, Dense3.871651564; hard concentration medians1.338417415/1.049242805. Complete learning, forgetting, hysteretic mastery, gross flows, concentration and step-lead tables are in the accompanying Chinese Detailed record. Paired document bootstrap measures evaluation sampling only. Sparse native checkpoints can miss hidden acquisition/forgetting cycles. Single seed; teacher-dependent dispatch; hint leakage not excluded. Analysis ran inside the retained Reserved job, not MIG; existing native1B caches were reused. No other training, old-asset edits, commit or push.


|   from_step |   to_step |   delta_steps | band    |   atoms |   learned |   forgotten |   net_forgotten |
|------------:|----------:|--------------:|:--------|--------:|----------:|------------:|----------------:|
|        2000 |      2250 |           250 | overall |   29995 |     19234 |         230 |             470 |
|        2250 |      2500 |           250 | overall |   29995 |     18100 |         315 |             418 |
|        2500 |      2750 |           250 | overall |   29995 |     10771 |         343 |             411 |
|        2750 |      3000 |           250 | overall |   29995 |     25285 |          74 |              50 |
|        3000 |      3250 |           250 | overall |   29995 |      7991 |         550 |             241 |
|        3250 |      3500 |           250 | overall |   29995 |      2684 |         570 |             415 |
|        3500 |      3750 |           250 | overall |   29995 |      2323 |        1334 |            1246 |
|        3750 |      3816 |            66 | overall |   29995 |       256 |        1616 |            2458 |

| reference                | stratum            | model   |   checkpoints |   first_tokens |   last_tokens |   K_initial |   K_final |   acquired_after_initial |   forgotten_after_initial |
|:-------------------------|:-------------------|:--------|--------------:|---------------:|--------------:|------------:|----------:|-------------------------:|--------------------------:|
| MoE33B                   | overall            | A5      |            16 |       65536000 |    1000341504 |   0.0941427 |  0.7354   |                 0.785966 |                0.144709   |
| MoE33B                   | rare_high          | A5      |            16 |       65536000 |    1000341504 |   0.0672764 |  0.715676 |                 0.821744 |                0.173345   |
| MoE33B                   | rare_low           | A5      |            16 |       65536000 |    1000341504 |   0.124533  |  0.750552 |                 0.740159 |                0.11414    |
| MoE33B                   | bigram_recognition | A5      |            16 |       65536000 |    1000341504 |   0.680336  |  0.968625 |                 0.392523 |                0.104234   |
| MoE33B                   | needs_context      | A5      |            16 |       65536000 |    1000341504 |   0.0565283 |  0.720434 |                 0.811213 |                0.147306   |
| MoE33B                   | overall            | MoE     |             3 |              0 |    1000000000 |   0         |  0.669744 |                 0.675002 |                0.00525773 |
| MoE33B                   | rare_high          | MoE     |             3 |              0 |    1000000000 |   0         |  0.661932 |                 0.667524 |                0.00559269 |
| MoE33B                   | rare_low           | MoE     |             3 |              0 |    1000000000 |   0         |  0.669117 |                 0.673776 |                0.00465932 |
| MoE33B                   | bigram_recognition | MoE     |             3 |              0 |    1000000000 |   0         |  0.950633 |                 0.95254  |                0.0019073  |
| MoE33B                   | needs_context      | MoE     |             3 |              0 |    1000000000 |   0         |  0.651721 |                 0.657193 |                0.00547272 |
| MoE33B                   | overall            | Dense   |             3 |              0 |    1000000000 |   0         |  0.633565 |                 0.639187 |                0.00562192 |
| MoE33B                   | rare_high          | Dense   |             3 |              0 |    1000000000 |   0         |  0.624141 |                 0.630127 |                0.0059866  |
| MoE33B                   | rare_low           | Dense   |             3 |              0 |    1000000000 |   0         |  0.6339   |                 0.638741 |                0.00484052 |
| MoE33B                   | bigram_recognition | Dense   |             3 |              0 |    1000000000 |   0         |  0.954066 |                 0.95645  |                0.00238413 |
| MoE33B                   | needs_context      | Dense   |             3 |              0 |    1000000000 |   0         |  0.612999 |                 0.618829 |                0.00582968 |
| Dense_latest_34076363264 | overall            | A5      |            16 |       65536000 |    1000341504 |   0.101624  |  0.788893 |                 0.824669 |                0.1374     |
| Dense_latest_34076363264 | rare_high          | A5      |            16 |       65536000 |    1000341504 |   0.0741113 |  0.786109 |                 0.87714  |                0.165142   |
| Dense_latest_34076363264 | rare_low           | A5      |            16 |       65536000 |    1000341504 |   0.131941  |  0.78879  |                 0.765523 |                0.108674   |
| Dense_latest_34076363264 | bigram_recognition | A5      |            16 |       65536000 |    1000341504 |   0.693597  |  0.986475 |                 0.360405 |                0.067527   |
| Dense_latest_34076363264 | needs_context      | A5      |            16 |       65536000 |    1000341504 |   0.0611543 |  0.775385 |                 0.856407 |                0.142177   |
| Dense_latest_34076363264 | overall            | MoE     |             3 |              0 |    1000000000 |   0         |  0.724132 |                 0.729381 |                0.00524915 |
| Dense_latest_34076363264 | rare_high          | MoE     |             3 |              0 |    1000000000 |   0         |  0.732716 |                 0.738605 |                0.00588922 |
| Dense_latest_34076363264 | rare_low           | MoE     |             3 |              0 |    1000000000 |   0         |  0.708748 |                 0.713084 |                0.00433591 |
| Dense_latest_34076363264 | bigram_recognition | MoE     |             3 |              0 |    1000000000 |   0         |  0.974257 |                 0.975727 |                0.00147011 |
| Dense_latest_34076363264 | needs_context      | MoE     |             3 |              0 |    1000000000 |   0         |  0.707033 |                 0.71254  |                0.0055075  |
| Dense_latest_34076363264 | overall            | Dense   |             3 |              0 |    1000000000 |   0         |  0.686456 |                 0.692263 |                0.00580731 |
| Dense_latest_34076363264 | rare_high          | Dense   |             3 |              0 |    1000000000 |   0         |  0.692309 |                 0.698483 |                0.00617403 |
| Dense_latest_34076363264 | rare_low           | Dense   |             3 |              0 |    1000000000 |   0         |  0.673129 |                 0.678073 |                0.00494349 |
| Dense_latest_34076363264 | bigram_recognition | Dense   |             3 |              0 |    1000000000 |   0         |  0.974747 |                 0.976511 |                0.00176413 |
| Dense_latest_34076363264 | needs_context      | Dense   |             3 |              0 |    1000000000 |   0         |  0.666747 |                 0.672831 |                0.00608371 |

| prediction   | result                                                                      |     value |    ci95_low |   ci95_high | proxy_rule_result   | researcher_judgment   |
|:-------------|:----------------------------------------------------------------------------|----------:|------------:|------------:|:--------------------|:----------------------|
| P10          | 支持                                                                        | -0.016302 |  -0.0191177 |  -0.0126727 | nan                 | Unknown               |
| P12          | 不足：原生baseline@2000存档缺失，采用R03 A0起点代理；不同长区间跨度仍有影响 |  0.28125  | nan         | nan         | 支持                | Unknown               |

Full source, configuration, checkpoint, deletion and runtime evidence is retained in the execution evidence directory and Chinese Detailed.

# Detailed: A17_04_E01 R03 finite mechanism audit

[中文](detailed_cn.md) · [Summary](summary.md) · [Frozen Protocol](protocol.md) · [Manifest](artifact_manifest.json)

## 1. Purpose

Locate which actual final-attention changes participate in R02's reversal of both old and new modes. The parent question concerns shared versus condition-dependent learning. This round neither evaluates the net utility of separate experts nor repeats1200-update training.

## 2. Model

Qwen3-0.6B Base has6,291,456 final-layer Q/K/V/O weights varied across saved states; all other parameters, including normalization, MLP, embeddings and output head, remain frozen. Actual E03 AdamW1200 is the common old endpoint. R02 orders29/43/71 share that endpoint. Old mode1 maps Jia/Yi to first/last; reversed mode2 maps them to last/first. The model sees mode, command and a three-word list, then predicts one answer token.

Q/K/V produce the O-input vector \(c\). O produces \(h_{\mathrm{attn}}=W_Oc\), followed by fixed residual, MLP and final normalization to hidden state \(h\). Every counterfactual restores the complete specified state before replacing one matrix. Reversed O inserted into old weights gives \(W_Rc_0\); old O rolled back into reversed weights gives \(W_0c_R\). Together with \(W_0c_0\) and \(W_Rc_R\), these form four actual states.

Let j index the command, \(s_{m,j}=z_{\mathrm{last}}-z_{\mathrm{first}}\) and \(a_m=(s_{m,Yi}-s_{m,Jia})/2\). Positive values denote the original mapping; negative values denote reversal. CE is negative correct-answer log probability. Accuracy is full-vocabulary top1 correctness. Endpoint margin compares the correct endpoint with the other endpoint; full margin compares the correct token with the strongest incorrect token. Units are natural-log units. With equal command weights old margin=\(a_1\) and reversed-new margin=\(-a_2\). Candidate mass refers to the three words in the input list.

## 3. Hypothesis

H0 is a label, mode, answer-position or checkpoint-identity bug. H1 is that reversed-new-only learning changes reading/output computations used by both modes without limiting the change to the new mode. H2 is that the existing displacement moves too far and a smaller scalar displacement could preserve both mappings.

The strongest retained explanation H3 concerns initial difficulty, supervision and optimization path: reversed-new starts at0%, consistent-new at99.875%; new-only training lacks old labels, while joint training adds old labels and halves new exposure. H1 addresses how existing internal changes participate in outcomes; H3 addresses why training selected that path. Both can hold. This round cannot exclude H3 by establishing H1's finite effects.

## 4. Conclusion

Complete reversed endpoint accuracy is old0%/new99.25%. At step1200, Q/K/V/O rollback respectively gives old/new48.54%/57.04%,22.46%/80.54%,23.96%/78.17%,32.67%/68.71%. Inserting only Q/K/V/O respectively gives51.21%/48.125%,78.71%/33.54%,99.54%/0.46%,98.71%/1.29%. Values average the three continuation orders. Old recovery accompanies changes in new performance; no independently switchable task matrix is identified.

On80 fixed DEV records, the O-by-QKV interaction is−8.365721nat for the old correct margin and+8.369476nat for the reversed-new correct margin. This supports non-additive finite predictive effects at that endpoint. None of30 interpolation samples meets≥80% in all eight cells; the best weakest cell reaches13.5%. This only weakens scale repair at the sampled points.

Eligibility: Full gatePASS, independent native/representation auditVALID and actual output registration complete. Researcher mechanism acceptance, closure and the next decision remainUnknown. This is exposed-DEV diagnosis from one old endpoint, not fresh confirmation; it establishes neither unique modules, the ineffectiveness of smaller-LR training, a shared subspace nor separate-expert net utility.

## 5. Analysis

### 5.1 Actual one-matrix counterfactuals

Each condition restores the full specified weights with per-tensor byte equality, performs one replacement and checks weight digests before/after forward. Conditions never accumulate. Rollback uses the reversed background; insertion uses the old background. Their effects are not interchangeable linear contributions. The common old reference has oldCE0.000691, accuracy100%, margin+17.5247; under reversed-new labels it hasCE16.037773, accuracy0%, margin−16.0350. [All per-order rows](/data/250010109/MoE_Router/experiments/20261012_a17_r02_mechanism_audit/runs/audit_20261012_r03_v1/full_parameter_rollback.csv).

Tables show equal-order means; accuracy is percent, CE is nat/answer and margins are nat. Each panel has200 lists×two commands×two modes; combined values equally weight the panels. Every condition evaluates1600 records. Old/new margins are a1/−a2, not independent additional measurements.

#### order_new

| Saved step | Condition | Old accuracy | New accuracy | Old CE | New CE | Old margin=a1 | New margin=−a2 |
|---:|---|---:|---:|---:|---:|---:|---:|
| 240 | full_reversed | 1.17% | 97.33% | 9.876160 | 0.080324 | -9.8009 | +10.1265 |
| 240 | rollback_q | 52.67% | 54.83% | 2.058904 | 1.640672 | +0.7114 | +1.1493 |
| 240 | rollback_k | 25.33% | 75.00% | 4.161255 | 0.977579 | -2.8912 | +3.8088 |
| 240 | rollback_v | 31.08% | 70.08% | 5.147680 | 0.921252 | -4.1103 | +4.2969 |
| 240 | rollback_o | 36.75% | 64.67% | 4.920840 | 1.452780 | -3.3766 | +3.6422 |
| 240 | insert_q | 52.08% | 48.42% | 4.256404 | 5.491974 | +1.4419 | -0.9239 |
| 240 | insert_k | 81.58% | 31.33% | 1.484220 | 7.451536 | +7.5479 | -4.8028 |
| 240 | insert_v | 99.67% | 0.25% | 0.012579 | 9.258656 | +10.4778 | -9.2355 |
| 240 | insert_o | 99.17% | 0.67% | 0.023246 | 10.382502 | +11.7318 | -10.3475 |
| 1200 | full_reversed | 0.00% | 99.00% | 16.234965 | 0.040870 | -16.2009 | +16.5833 |
| 1200 | rollback_q | 47.08% | 57.75% | 3.868838 | 2.102443 | -0.4548 | +2.6248 |
| 1200 | rollback_k | 21.08% | 81.50% | 7.125478 | 1.063849 | -5.7252 | +6.9936 |
| 1200 | rollback_v | 23.33% | 78.92% | 7.657379 | 0.719629 | -6.8528 | +7.0911 |
| 1200 | rollback_o | 32.08% | 69.17% | 5.680024 | 1.164907 | -4.4641 | +4.6846 |
| 1200 | insert_q | 52.00% | 48.25% | 4.335726 | 5.679619 | +1.5230 | -1.0000 |
| 1200 | insert_k | 78.50% | 34.17% | 1.778350 | 7.063833 | +6.6640 | -4.1716 |
| 1200 | insert_v | 99.50% | 0.42% | 0.015582 | 9.816588 | +11.0749 | -9.7919 |
| 1200 | insert_o | 98.75% | 1.08% | 0.038938 | 12.702718 | +14.2512 | -12.6467 |

#### combination_new

| Saved step | Condition | Old accuracy | New accuracy | Old CE | New CE | Old margin=a1 | New margin=−a2 |
|---:|---|---:|---:|---:|---:|---:|---:|
| 240 | full_reversed | 2.83% | 96.83% | 9.231812 | 0.086925 | -9.1355 | +9.4943 |
| 240 | rollback_q | 55.58% | 55.75% | 1.834545 | 1.708647 | +1.0576 | +0.7620 |
| 240 | rollback_k | 27.25% | 74.17% | 3.716581 | 0.888025 | -2.5170 | +3.4340 |
| 240 | rollback_v | 31.67% | 69.17% | 4.925321 | 0.936893 | -3.8626 | +4.0736 |
| 240 | rollback_o | 37.83% | 62.83% | 4.668592 | 1.441925 | -3.1154 | +3.3940 |
| 240 | insert_q | 50.50% | 47.92% | 4.204629 | 5.535515 | +1.5028 | -0.9132 |
| 240 | insert_k | 81.83% | 31.75% | 1.373333 | 7.661401 | +7.7723 | -5.0273 |
| 240 | insert_v | 99.75% | 0.25% | 0.011098 | 9.004481 | +10.2830 | -8.9896 |
| 240 | insert_o | 99.17% | 0.58% | 0.025693 | 9.990943 | +11.4072 | -9.9578 |
| 1200 | full_reversed | 0.00% | 99.50% | 15.403448 | 0.021830 | -15.3853 | +15.7964 |
| 1200 | rollback_q | 50.00% | 56.33% | 3.589920 | 2.207258 | +0.0162 | +2.1678 |
| 1200 | rollback_k | 23.83% | 79.58% | 6.495263 | 1.026554 | -5.0822 | +6.3978 |
| 1200 | rollback_v | 24.58% | 77.42% | 7.418812 | 0.776310 | -6.5547 | +6.8112 |
| 1200 | rollback_o | 33.25% | 68.25% | 5.463756 | 1.179255 | -4.2113 | +4.4396 |
| 1200 | insert_q | 50.42% | 48.00% | 4.264602 | 5.704802 | +1.5873 | -0.9910 |
| 1200 | insert_k | 78.92% | 32.92% | 1.648059 | 7.277287 | +6.9831 | -4.4617 |
| 1200 | insert_v | 99.58% | 0.50% | 0.013295 | 9.578714 | +10.9178 | -9.5607 |
| 1200 | insert_o | 98.67% | 1.50% | 0.034701 | 12.220052 | +13.9032 | -12.1760 |

#### combined

| Saved step | Condition | Old accuracy | New accuracy | Old CE | New CE | Old margin=a1 | New margin=−a2 |
|---:|---|---:|---:|---:|---:|---:|---:|
| 240 | full_reversed | 2.00% | 97.08% | 9.553986 | 0.083625 | -9.4682 | +9.8104 |
| 240 | rollback_q | 54.12% | 55.29% | 1.946724 | 1.674659 | +0.8845 | +0.9556 |
| 240 | rollback_k | 26.29% | 74.58% | 3.938918 | 0.932802 | -2.7041 | +3.6214 |
| 240 | rollback_v | 31.37% | 69.62% | 5.036500 | 0.929073 | -3.9865 | +4.1853 |
| 240 | rollback_o | 37.29% | 63.75% | 4.794716 | 1.447353 | -3.2460 | +3.5181 |
| 240 | insert_q | 51.29% | 48.17% | 4.230517 | 5.513744 | +1.4724 | -0.9185 |
| 240 | insert_k | 81.71% | 31.54% | 1.428777 | 7.556468 | +7.6601 | -4.9151 |
| 240 | insert_v | 99.71% | 0.25% | 0.011838 | 9.131568 | +10.3804 | -9.1126 |
| 240 | insert_o | 99.17% | 0.62% | 0.024469 | 10.186722 | +11.5695 | -10.1527 |
| 1200 | full_reversed | 0.00% | 99.25% | 15.819206 | 0.031350 | -15.7931 | +16.1898 |
| 1200 | rollback_q | 48.54% | 57.04% | 3.729379 | 2.154850 | -0.2193 | +2.3963 |
| 1200 | rollback_k | 22.46% | 80.54% | 6.810371 | 1.045201 | -5.4037 | +6.6957 |
| 1200 | rollback_v | 23.96% | 78.17% | 7.538096 | 0.747970 | -6.7037 | +6.9512 |
| 1200 | rollback_o | 32.67% | 68.71% | 5.571890 | 1.172081 | -4.3377 | +4.5621 |
| 1200 | insert_q | 51.21% | 48.12% | 4.300164 | 5.692210 | +1.5551 | -0.9955 |
| 1200 | insert_k | 78.71% | 33.54% | 1.713204 | 7.170560 | +6.8236 | -4.3167 |
| 1200 | insert_v | 99.54% | 0.46% | 0.014439 | 9.697651 | +10.9963 | -9.6763 |
| 1200 | insert_o | 98.71% | 1.29% | 0.036819 | 12.461385 | +14.0772 | -12.4113 |

Step1200 Q-rollback old accuracy mean/order range is48.54% [38.25%, 61.38%]; its new range is57.04% [51.50%, 61.62%]. O-rollback old/new ranges are32.67% [24.88%, 37.62%]/68.71% [63.50%, 76.25%]. Per-order CE, full-vocabulary margins, candidate masses and a1/a2 remain in the native CSV/JSON. No order is removed or hidden by the means; no p-values are reported and the orders are not independent old-model replications.

Q rollback restores more old accuracy than the other three rollbacks in these states, but new performance falls and the effect is conditional on the other matrices already being reversed. Inserting only reversed Q does not reproduce the complete reversed model. Comprehensive independent auditing confirms old accuracy rises and new accuracy falls in24/24 rollback comparisons. No single-matrix insertion reproduces complete reversed-new proficiency. Two-/three-matrix combinations were not exhausted; this does not establish that all four matrices are necessary. Q therefore cannot be called a unique rule matrix, nor do these mixed weights establish an optimal parameter partition.

### 5.2 Five-point interpolation

For each reversed state, construct \(\theta(\alpha)=\theta_0+\alpha(\theta_R-\theta_0)\), jointly interpolating all four matrices while keeping other weights fixed. Compatibility requires≥80% in all eight mode-by-command-by-panel cells. Performance is reported for each panel and combined; the weakest-cell statistic always uses all eight cells. [Thirty eligibility rows](/data/250010109/MoE_Router/experiments/20261012_a17_r02_mechanism_audit/runs/audit_20261012_r03_v1/full_interpolation_compatibility.csv).

#### order_new

| Saved step | alpha | Old accuracy | New accuracy | Old margin | New margin | Weakest-cell accuracy range across orders | Qualified orders |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 240 | 0 | 100.00% | 0.00% | +17.7723 | -16.3364 | 0.00%–0.00% | 0/3 |
| 240 | 0.25 | 95.25% | 23.75% | +9.8160 | -5.9224 | 0.00%–0.00% | 0/3 |
| 240 | 0.5 | 48.42% | 55.50% | -1.0898 | +2.1225 | 3.00%–13.50% | 0/3 |
| 240 | 0.75 | 9.75% | 90.50% | -6.2785 | +6.7107 | 0.50%–1.50% | 0/3 |
| 240 | 1 | 1.17% | 97.33% | -9.8009 | +10.1265 | 0.50%–1.50% | 0/3 |
| 1200 | 0 | 100.00% | 0.00% | +17.7723 | -16.3364 | 0.00%–0.00% | 0/3 |
| 1200 | 0.25 | 93.75% | 25.75% | +10.1291 | -5.8739 | 0.00%–0.00% | 0/3 |
| 1200 | 0.5 | 42.42% | 60.42% | -2.7730 | +3.9535 | 0.50%–6.50% | 0/3 |
| 1200 | 0.75 | 1.67% | 97.50% | -10.5382 | +11.0159 | 0.00%–0.00% | 0/3 |
| 1200 | 1 | 0.00% | 99.00% | -16.2009 | +16.5833 | 0.00%–0.00% | 0/3 |

#### combination_new

| Saved step | alpha | Old accuracy | New accuracy | Old margin | New margin | Weakest-cell accuracy range across orders | Qualified orders |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 240 | 0 | 100.00% | 0.00% | +17.2770 | -15.7337 | 0.00%–0.00% | 0/3 |
| 240 | 0.25 | 95.33% | 21.75% | +9.9596 | -6.0655 | 0.00%–0.00% | 0/3 |
| 240 | 0.5 | 49.42% | 54.00% | -0.7442 | +1.8404 | 3.00%–13.50% | 0/3 |
| 240 | 0.75 | 12.42% | 89.58% | -5.7859 | +6.2342 | 0.50%–1.50% | 0/3 |
| 240 | 1 | 2.83% | 96.83% | -9.1355 | +9.4943 | 0.50%–1.50% | 0/3 |
| 1200 | 0 | 100.00% | 0.00% | +17.2770 | -15.7337 | 0.00%–0.00% | 0/3 |
| 1200 | 0.25 | 94.08% | 24.00% | +10.3131 | -6.0681 | 0.00%–0.00% | 0/3 |
| 1200 | 0.5 | 45.83% | 58.00% | -2.3260 | +3.6045 | 0.50%–6.50% | 0/3 |
| 1200 | 0.75 | 2.08% | 98.17% | -9.9078 | +10.4192 | 0.00%–0.00% | 0/3 |
| 1200 | 1 | 0.00% | 99.50% | -15.3853 | +15.7964 | 0.00%–0.00% | 0/3 |

#### combined

| Saved step | alpha | Old accuracy | New accuracy | Old margin | New margin | Weakest-cell accuracy range across orders | Qualified orders |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 240 | 0 | 100.00% | 0.00% | +17.5247 | -16.0350 | 0.00%–0.00% | 0/3 |
| 240 | 0.25 | 95.29% | 22.75% | +9.8878 | -5.9939 | 0.00%–0.00% | 0/3 |
| 240 | 0.5 | 48.92% | 54.75% | -0.9170 | +1.9815 | 3.00%–13.50% | 0/3 |
| 240 | 0.75 | 11.08% | 90.04% | -6.0322 | +6.4725 | 0.50%–1.50% | 0/3 |
| 240 | 1 | 2.00% | 97.08% | -9.4682 | +9.8104 | 0.50%–1.50% | 0/3 |
| 1200 | 0 | 100.00% | 0.00% | +17.5247 | -16.0350 | 0.00%–0.00% | 0/3 |
| 1200 | 0.25 | 93.92% | 24.88% | +10.2211 | -5.9710 | 0.00%–0.00% | 0/3 |
| 1200 | 0.5 | 44.12% | 59.21% | -2.5495 | +3.7790 | 0.50%–6.50% | 0/3 |
| 1200 | 0.75 | 1.88% | 97.83% | -10.2230 | +10.7176 | 0.00%–0.00% | 0/3 |
| 1200 | 1 | 0.00% | 99.25% | -15.7931 | +16.1898 | 0.00%–0.00% | 0/3 |

No sampled state qualifies. The best weakest-cell accuracy13.5% occurs at order71/step240/alpha0.5. No tested point exemplifies preserving both mappings by scalar reduction of this displacement. Unsampled narrow intervals, other paths and actual smaller-LR retraining remain untested. R02 joint training already demonstrates another compatible path, so this result cannot imply inherent capacity insufficiency.

### 5.3 Representation-to-prediction bridge

The panel is fixed to order29/step1200, first10 sorted list IDs per DEV panel, both modes and commands:80 records repeated across four states, not320 independent observations. c has2048 coordinates, the raw attention output1024 and final normalized h1024. Raw NPZ arrays and the frozen head are independently audited. [Four-state manifest](/data/250010109/MoE_Router/experiments/20261012_a17_r02_mechanism_audit/runs/audit_20261012_r03_v1/full/seed_29/representation_manifest.json) · [Signed table](/data/250010109/MoE_Router/experiments/20261012_a17_r02_mechanism_audit/independent_audit/representation_signed_response.csv).

| Panel | Four-state condition | Old correct margin a1 | New reversed correct margin −a2 |
|---|---|---:|---:|
| order_new | old_endpoint | +12.686050 | -12.187365 |
| order_new | insert_o_proj | +10.286898 | -9.340457 |
| order_new | rollback_o_proj | -3.121261 | +3.494517 |
| order_new | full_reversed | -14.353798 | +15.194147 |
| order_new | O_by_QKV_interaction | -8.833385 | +8.852722 |
| combination_new | old_endpoint | +19.078666 | -17.687214 |
| combination_new | insert_o_proj | +14.540906 | -12.811879 |
| combination_new | rollback_o_proj | -3.096859 | +3.525818 |
| combination_new | full_reversed | -15.532675 | +16.287382 |
| combination_new | O_by_QKV_interaction | -7.898057 | +7.886229 |
| combined | old_endpoint | +15.882358 | -14.937290 |
| combined | insert_o_proj | +12.413902 | -11.076168 |
| combined | rollback_o_proj | -3.109060 | +3.510168 |
| combined | full_reversed | -14.943237 | +15.740765 |
| combined | O_by_QKV_interaction | -8.365721 | +8.369476 |

For a signed marginF, define \(I_F=F_{11}-F_{10}-F_{01}+F_{00}\). State00 is old-O/old-QKV,10 new-O/old-QKV,01 old-O/new-QKV and11 new-O/new-QKV. For the old task, new O reduces margin by3.4685nat under old QKV but by11.8342nat under new QKV: a difference of−8.3657nat. The reversed-new signed interaction is+8.3695nat.

O's finite prediction consequence therefore depends on the current reading computation. This neither establishes independent parameter specialization nor identifies O as the unique mediator. The output interaction includes fixed residual/MLP/normalization nonlinearities and cannot be attributed entirely to the linear product term. Raw last-minus-first effects cancel across commands: raw interaction mean−0.3194 versus mean absolute8.3676. The task-aligned signed margins avoid that cancellation.

The raw linear-output identity is

\[
\Delta h_{\mathrm{attn}}=\Delta Wc_0+W_0\Delta c+\Delta W\Delta c.
\]

Mean per-record vector norms are227.5220 for the actual attention-output change,67.9383 for the O-only term,225.4890 for the input-only term and73.9410 for the interaction term. Norms are not additive causal shares; cancellation affects the total. Relative residual is5.38849e−7, maximum coordinate residual7.08890e−5. O input is exactly equal when QKV are held fixed. Final hidden-state mean change norm is86.7662. The frozen head difference \(w_{\mathrm{last}}-w_{\mathrm{first}}\) maps h to endpoint logit difference with maximum error8.10653e−5nat. The registered Base uses tied embedding/output weights, independently verified. These are numerical computation checks, not empirical mechanism discoveries. [Raw representation analysis](/data/250010109/MoE_Router/experiments/20261012_a17_r02_mechanism_audit/runs/audit_20261012_r03_v1/full/seed_29/representation_analysis.json).

### 5.4 Existing trajectories and displacement: descriptive evidence

CPU analysis preserves eight existing saved points without additional training. For order29, old/new a values are+0.2088/+0.1444 at16 and−0.4837/−0.5797 at50. The sign change is localized only to that saved interval, not an exact first update. At120, new accuracy is96% and old2.875%. [Existing trajectory recomputation](/data/250010109/MoE_Router/experiments/20261012_a17_r02_mechanism_audit/runs/audit_20261012_r03_v1/existing_trajectory.csv).

Order29 reversed displacement norm is4.13418 at240 and4.75468 at1200. Individual relative matrix displacement is approximately5.16%–6.45% of old-weight Frobenius norm. D1 contains90 rows; independent NumPy recomputation checks294 scalars with maximum norm error4.01e−12 and cosine error3.44e−13. Norms/cosines do not label functionality or useful sharing. [All displacement rows](/data/250010109/MoE_Router/experiments/20261012_a17_r02_mechanism_audit/runs/audit_20261012_r03_v1/delta_stats.csv).

### 5.5 Freeze, execution and conformance

Protocol revisiona17_04_e01_r03_mechanism_audit_v1; config SHA `a06a8e8ae97cbf54388c20d2174fb3f5e371f622d879b0858c30c96d500b6677`. Freeze binds config itself, bilingual Protocol, source code,72 source-state and72 cached-readout digests. Frozen R02 records/weights are unchanged.

| Item | Registered requirement | Actual | Eligibility and limit |
|---|---|---|---|
| Data/parent | Original TRAIN/DEV, exact Base/E03 endpoint |9600 token/prefix/label checks;72 states/caches |VALID; no TEST |
| Independent source audit | Three orders/branches at0/240/1200 |Independent27 states/72 caches; implementation checks72 states |CPU audit does not forward the model |
| Native GPU replay |0/240/1200, error≤1e−3 and same top1 |All three orders replay with error0 |PASS |
| D2 |Three orders×two states×four rollbacks/four insertions |All saved, both panels and combined |ELIGIBLE finite conditional effects |
| D3 |Five alphas×six state pairs; all eight cells≥80% |Thirty actual decisions, none qualifies |ELIGIBLE only at sampled points |
| Representations |Order29/1200, fixed80DEV, four states |Four NPZ/manifest plus independent signed analysis |BOUNDED to this panel |
| Restoration/freeze |Byte-equal restore, identical no-op, frozen bytes |Runtime and saved-record checks pass |No separately saved mixed-weight digests |
| Excluded work |No updates/TEST/SAE/SVD/experts |All NOT RUN |Conformant |
| Saved outputs |Register native analysis and representations |One Smoke/two Full assets; selected strict passes |Access does not confirm mechanism |

One four-H100 reserved node, shphd-lite-0911, native FP32 SDPA, no TF32, eval/no_grad. Full uses three independent order workers, representation on order29 and the fourth allocated GPU unused. Smoke uses one worker. This is not data-parallel training. Smokept-p6uri2pxSUCCEEDED; Fullpt-o3rvi0s1SUCCEEDED and completes native gates, worker times145.17–151.56s; exact platform terminal evidence is owned by the execution manifest. No GPU experiment retries or budget extension. The first independent CPU-audit attempt hit a TypeError converting BF16 parent-head rows directly to NumPy. Only that independent reader was repaired to convert to FP32 before FP64; the second audit isVALID. Both finite_audit_execution.log and finite_audit_execution_attempt2.log are preserved. This was not an experiment/model/data/frozen-GPU-source bug, and no GPU outputs were modified or rerun. Training-token/TensorBoard/training-resume requirements are inapplicable because this round performs zero optimizer updates.

Restoration uses per-tensor torch.equal; forward before/after digests match. Saved no-op/restored-old output records are exactly equal. Individual mixed-condition complete weights/digests are not persisted separately, and this record does not imply they were saved; they can be reconstructed from frozen sources and rules.

### 5.6 Independent numerical audit and evidence lineage

Independent auditVALID/0errors covers88 native JSON files,140800 record appearances,300 table rows and30 interpolation decisions. Replay errors are0, table recomputation errors≤3.55271e−15 and native FP32 CE versus FP64 stored log-probability discrepancy≤3.86962e−6. This independent audit reads saved outputs/NPZ and does not reexecute GPU inference. CPU accuracy checks reuse cached argmax IDs; they do not recompute vocabulary logits absent from the cache. Actual GPU forward supplies the vocabulary-wide evidence. [Complete independent audit](/data/250010109/MoE_Router/experiments/20261012_a17_r02_mechanism_audit/independent_audit/finite_outputs_audit.json) · [Comprehensive audit](/data/250010109/MoE_Router/experiments/20261012_a17_r02_mechanism_audit/independent_audit/comprehensive_audit.json).

| Claim | Raw evidence and computation | Aggregation/decision | Allowed finding | Remaining limit |
|---|---|---|---|---|
| Old0% is not the audited confusion |Token/label/state audit, GPU replay/native argmax |CPU VALID; replay error0 |Inspected mapping/state is reproducible |Not external fresh confirmation |
| Four changes participate |Per-condition native JSON→300 CSV rows |All orders, panels, combined |Finite causal participation in specified backgrounds |Not unique function/general necessity |
| O effect depends on reading |80DEV four NPZ→signed responses |Both panels have consistent signed interaction |Endpoint O-by-QKV non-additive prediction effect |Not unique mediator/full-space finding |
| Scale reduction did not repair |Thirty alpha eligibility records/eight cells |0/30 qualifies |No sampled compatible state |Unsampled points/new training untested |
| Same parameters can coexist |R02 joint old99.83%/new99.67% |Prior result, not repeated |No principled task incompatibility |Joint changes labels/new exposure |

### 5.7 Complete round and assets

1. Question: which actual matrix changes participate in both-mode reversal, and do five scalar reductions preserve both mappings?
2. Setup: same E03 endpoint; R02 three orders×240/1200; full restore then one-matrix rollback/insertion or whole-displacement interpolation; other weights fixed.
3. Training data: identity audit of existing TRAIN fields only; no training, added examples or new supervision.
4. Evaluation: exposed DEV two panels,1600 records/condition, fixed80-record representation subset; no TEST or confirmation split.
5. Result:88 native outputs/140800 record appearances,300 aggregate rows,30 eligibility decisions and four representation NPZ; Full gate/independent audit pass, actual assets registered.
6. Insight/boundary/decision: finite participation, O-by-QKV interaction and sampled scale boundary; researcher mechanism acceptance and next decisionUnknown; Focus state unchanged.

Execution root/data/250010109/MoE_Router/experiments/20261012_a17_r02_mechanism_audit; run/data/250010109/MoE_Router/experiments/20261012_a17_r02_mechanism_audit/runs/audit_20261012_r03_v1. Inputs are the exact registered Qwen Base/tokenizer, data_a17_conditional_mapping_v1, E03 old adapter, nine R02 adapter families and native analysis. Config/freeze owns stable IDs and digests. No new checkpoints are produced; previous weights are read-only inputs. Smoke asset: `analysis_a17_04_r03_audit_20261012_r03_v1_smoke_finite_native`. Full assets: `analysis_a17_04_r03_audit_20261012_r03_v1_full_finite_native` and `representation_a17_04_r03_audit_20261012_r03_v1_full_o_qkv_four_state_dev80`. Selected access is linked by Full receipt; actual member digests are in registration_request and artifact_manifest.

[Smoke registration](/data/250010109/MoE_Router/experiments/20261012_a17_r02_mechanism_audit/runs/audit_20261012_r03_v1/smoke_registration_receipt.json) · [Full registration](/data/250010109/MoE_Router/experiments/20261012_a17_r02_mechanism_audit/runs/audit_20261012_r03_v1/full_registration_receipt.json) · [Freeze](/data/250010109/MoE_Router/experiments/20261012_a17_r02_mechanism_audit/runs/audit_20261012_r03_v1/freeze.json) · [Config](/data/250010109/MoE_Router/experiments/20261012_a17_r02_mechanism_audit/configs/mechanism_v1.json) · [Runner](/data/250010109/MoE_Router/experiments/20261012_a17_r02_mechanism_audit/scripts/run_phase.py). Recalculation reads frozen CSV/JSON/NPZ using independent_audit/audit_finite_outputs.py, without training. GPU reexecution must retain original freeze and authorized resources.

### 5.8 Causal interpretation and next decision

Observation: actual mixed weights alter predictions in both modes. Derivation: the exact O/reading bridge and signed four-state difference. AI candidate interpretation: new-only updates change shared computations in a way that also changes their use by the old mode. H3 still addresses why the optimization path does not confine these effects; this round does not independently manipulate old supervision or path choice.

For shared versus separate learning, the updated question is whether shared updates can limit changes to the intended condition; different answer rules alone do not require separate parameters. Joint supervision supplies compatibility, and R03 supplies actual cross-mode, interdependent consequences of the existing new-only changes. Budget-matched supervision/compute/parameter comparisons are still required to establish the utility of parameter separation.

The single unconfirmed next decision remainsUnknown. AI suggestion: with new proficiency and exposure accountable, test which learning constraint limits reversed changes to the new mode while preserving the old rule. This suggestion does not authorize another run or close the question.

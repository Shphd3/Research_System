# A11_17 Interface-Paraphrase Usefulness Decomposition: Detailed Evidence

## 0. Result

Formal preregistered status: **CE/margin mismatch**. H2-train step-0 usefulness is negative in `5/5`, so the direct-self gate requiring both positive step 0 and positive trajectory AUC fails.

Secondary preregistered trajectory evidence: H2-train AUC is positive `5/5` and H2-eval `4/5`, while H1-train is positive `0/5` and H1-eval `1/5`. After the initial multi-class transient, the persistent failure is therefore interface/position transport.

## 1. Experimental Contract

- model: `Qwen3-0.6B-Base`;
- training: NTP response-position objective $L_S+L_I$ only;
- H2: copied from H1 at step 0, not trained on the NTP trajectory;
- task: fixed A11_13 persistent-assistant prompts;
- train paraphrases `0,1`; evaluation paraphrases `2,3`;
- seeds `971-975`; checkpoints `0,20,100,200,300`;
- diagnostics: 10 balanced train and 10 balanced evaluation examples;
- remote job `pt-vfn348ke`, four H100 GPUs.

All five tasks, 25 checkpoints, 100 cell rows, and 250 per-domain rows complete. Curve reproduction difference is exactly zero. Central-difference signs match all four cells in all five seeds.

## 2. Full Sign Table

| Cell | Step-0 positive | AUC `0-200` positive | Formal gate |
|---|---:|---:|---|
| H2-train | 0/5 | 5/5 | fails due step 0 |
| H2-eval | 0/5 | 4/5 | later paraphrase transport passes |
| H1-train | 0/5 | 0/5 | persistent interface/position failure |
| H1-eval | 1/5 | 1/5 | reproduces A11_16 failure |

Per-seed trajectory integrals:

| Seed | H2-train | H2-eval | H1-train | H1-eval |
|---:|---:|---:|---:|---:|
| 971 | 0.2944 | 0.2076 | -0.0404 | -0.0134 |
| 972 | 0.2871 | 0.2204 | -0.0264 | 0.0144 |
| 973 | 0.0035 | -0.0018 | -0.1043 | -0.0832 |
| 974 | 0.1176 | 0.0110 | -0.1368 | -0.0759 |
| 975 | 0.1142 | 0.0987 | -0.1646 | -0.1510 |

## 3. Time-Resolved Means

| Step | H2-train | H2-eval | H1-train | H1-eval |
|---:|---:|---:|---:|---:|
| 0 | -0.0627 | -0.0450 | -0.0625 | -0.0415 |
| 20 | 0.0775 | 0.0705 | 0.0575 | 0.0436 |
| 100 | 0.0546 | 0.0315 | -0.0641 | -0.0648 |
| 200 | 0.4903 | 0.3106 | -0.3077 | -0.1660 |
| 300 | 0.5653 | 0.4214 | -0.2888 | -0.1737 |

At step 20 all means are temporarily positive. From step 100 onward, the H2 and H1 trajectories split. This temporal split is why a static step-0 classification alone is incomplete.

## 4. Full-Vocabulary CE Versus Binary Margin

For fixed output head $U_2$, one-example CE has hidden descent direction:

$$
d_2=-\nabla_hL_D=u_y-\bar u_p,
\qquad
\bar u_p=\sum_vp_vu_v.
$$

The A/B semantic vector is $v_{y,b}=u_y-u_b$. Its one-step hidden margin change is:

$$
\Delta m_{y,b}=\eta v_{y,b}^\top d_2.
$$

No sign follows in a full vocabulary because $\bar u_p$ includes every competing row. In the two-class limit:

$$
d_2=p_bv_{y,b},
$$

and then:

$$
\Delta m_{y,b}=\eta p_b\|v_{y,b}\|^2\ge0.
$$

The data support this burn-in interpretation: H2 self-usefulness is negative at step 0 but positive and large at steps 200/300.

## 5. Interface/Position Cross-Kernel

Let $d_2$ be the H2 hidden descent direction, $v_1$ the standard-H1 binary readout direction, and:

$$
J_2=\frac{\partial h_T}{\partial\theta_S},
\qquad
J_1=\frac{\partial h_{T+1}}{\partial\theta_S}.
$$

The shared H2 parameter gradient is $g_D^S=-J_2^\top d_2$. Standard-H1 margin gradient is $J_1^\top v_1$. Hence:

$$
U_{1\leftarrow2}
=-\langle J_1^\top v_1,-J_2^\top d_2\rangle
=v_1^\top J_1J_2^\top d_2.
$$

The cross-kernel $\Theta_{12}=J_1J_2^\top$ has no positive-semidefinite guarantee. Even if H2 self-usefulness

$$
v_2^\top J_2J_2^\top d_2
$$

is positive, $U_{1\leftarrow2}$ may be negative. A11_17 provides exactly this empirical pattern after burn-in.

## 6. Paraphrase Transport

H2-eval usefulness tracks H2-train closely and its trajectory AUC is positive in `4/5`. At step 300, H2-eval mean is `0.4214` versus H2-train `0.5653`. Thus unseen wording reduces magnitude but usually preserves sign.

H1-train is already negative in `5/5` by trajectory AUC, so H1-eval negativity cannot be attributed primarily to unseen paraphrases. The sign is lost before the wording split, at the combined head/position interface.

## 7. Visualization Results

### Plot Contract

**Question:** where does H2-gradient usefulness stop transferring?  
**Top left:** step-0 2-by-2 mean; all cells are initially negative.  
**Top right:** time-resolved means; H2 and H1 split after burn-in.  
**Bottom left:** positive-seed counts for step 0 and trajectory AUC.  
**Bottom right:** central derivative validation.  
**Allowed conclusion:** distinguish initial multi-class transient, paraphrase transport, and combined interface/position transport.  
**Limitation:** H2-to-H1 changes both head and hidden-state position.

![A11_17 interface-paraphrase decomposition](figures/a11_17_interface_paraphrase_usefulness_decomposition.png)

## 8. Hypothesis Audit

| Hypothesis | Result | Decision |
|---|---|---|
| H1 direct self-usefulness | step 0 0/5, AUC 5/5 | formal fail; burn-in transition observed |
| H2 interface/position transfer | H1-train AUC 0/5 after H2 AUC 5/5 | secondary trajectory supports bottleneck |
| H3 paraphrase transfer | H2-eval AUC 4/5 | supported for H2 interface |
| H4 derivative validity | all four signs match in 5/5 | supported |

## 9. Claim Boundary

**Observation:** after burn-in, H2 seen/unseen usefulness is positive while H1 seen/unseen usefulness is negative.  
**Interpretation:** the persistent sign loss occurs at the combined output-interface/state-position transfer.  
**Claim:** horizon coverage plus H2 self-learning does not guarantee standard-H1 benefit; positive cross-interface kernel alignment is an additional condition.  
**Cannot claim:** whether head or position is individually responsible, global MTP harm, pure pretraining behavior, or sample efficiency.

## 10. Artifact Map

Raw result:

```text
/data/250010109/Research_System/Projects/from-attention-to-search/
XingyuD/Attention_Search_Experiments/active/synthetic_data_understanding/
results/a11_17_interface_paraphrase_usefulness_decomposition/
a11_17_interface_paraphrase_usefulness_decomposition_4gpu_20260711_001500
```

Logs:

```text
.../logs/acp/a11_17_interface_paraphrase_usefulness_decomposition_4gpu_20260711_001500
```

Code:

```text
configs/a11_17_interface_paraphrase_usefulness_decomposition.json
scripts/run_a11_17_interface_paraphrase_usefulness_decomposition.py
scripts/analyze_a11_17_interface_paraphrase_usefulness_decomposition.py
scripts/submit_a11_17_interface_paraphrase_usefulness_decomposition_4gpu.sh
```

Remote job: `pt-vfn348ke`.

## 11. Next Decision

At post-burn-in checkpoints, cross readout head (H2/H1) with state position ($h_T/h_{T+1}$) on seen examples. This separates output-head drift from positional Jacobian transport and directly estimates the four cross-kernel terms.

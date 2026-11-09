# A11_17 Interface-Paraphrase Usefulness Decomposition: Summary

## What We Established

A11_17 identifies two time scales rather than one static bottleneck.

1. At initialization, the full-vocabulary H2 cross-entropy gradient decreases the binary A-versus-B margin in all four interface/split cells and all five seeds. This is a multi-class CE-to-binary-margin transient.
2. Over steps `0-200`, H2 usefulness becomes positive for seen wording in `5/5` seeds and unseen paraphrases in `4/5`, while standard-H1 usefulness remains positive in `0/5` for seen wording and `1/5` for unseen wording.

**Decision:** the preregistered primary status is `CE/margin mismatch` because direct H2 self-usefulness fails at step 0. Conditional on the later positive H2 trajectory, the persistent bottleneck is interface/position transmission, not paraphrase generalization.

## Definitions

Using the same shared H2-loss gradient $g_D^S$, define four margins:

$$
M_{2,tr},\quad M_{2,ev},\quad M_{1,tr},\quad M_{1,ev},
$$

where `2/1` means H2 at $h_T$ or standard H1 at $h_{T+1}$, and `tr/ev` means seen or unseen paraphrases. For each cell:

$$
\widehat U_{a,s}
=-\frac{\langle\nabla_{\theta_S}M_{a,s},g_D^S\rangle}
{\|\nabla_{\theta_S}M_{a,s}\|\|g_D^S\|}.
$$

Positive means an infinitesimal H2-loss descent step increases that cell's correct A/B margin. It does not measure global optimization or full-vocabulary target rank by itself.

## Setup And Validity

- exact A11_16 Qwen3-0.6B task and NTP trajectory;
- five seeds, checkpoints `0,20,100,200,300`;
- one fixed H2 gradient and four margin gradients per checkpoint;
- labels and paraphrases balanced `5/5`; all domains/states covered;
- four-H100 job `pt-vfn348ke`, 5/5 tasks complete;
- all coverage, balance, finite-value, H2-copy, and restore guards pass;
- all four step-0 central-difference signs agree in `5/5` seeds;
- A11_16 NTP mean curve reproduces exactly.

## Primary Evidence

| Cell | Step-0 positive | Usefulness AUC `0-200` positive | Final mean $\widehat U$ | Interpretation |
|---|---:|---:|---:|---|
| H2 / seen | 0/5 | 5/5 | 0.5653 | initial CE transient, then strong self-usefulness |
| H2 / unseen | 0/5 | 4/5 | 0.4214 | H2 direction largely generalizes across paraphrases |
| H1 / seen | 0/5 | 0/5 | -0.2888 | persistent interface/position failure |
| H1 / unseen | 1/5 | 1/5 | -0.1737 | full downstream transmission remains adverse |

At step 20, mean usefulness is already positive in all four cells. By step 100, H2 cells remain positive on average while H1 cells become negative; at steps 200 and 300, every H2-train seed is positive and every H1-train seed is negative.

## Why Step 0 Can Be Negative

For one full-vocabulary H2 example with output rows $u_v$:

$$
-\nabla_h L_D=u_y-\sum_v p_vu_v.
$$

For binary semantic margin $m_{y,b}=(u_y-u_b)^\top h$, its immediate change is:

$$
\frac{\Delta m_{y,b}}{\eta}
=(u_y-u_b)^\top\left(u_y-\sum_v p_vu_v\right).
$$

This can be negative when probability mass lies on many unrelated vocabulary rows. Once the relevant mass is mostly on $y$ and $b$,

$$
u_y-\sum_vp_vu_v\approx p_b(u_y-u_b),
$$

so the self-margin change becomes approximately $p_b\|u_y-u_b\|^2>0$. This matches the observed negative step 0 and positive later H2 trajectory.

## Visualization Results

![A11_17 interface-paraphrase decomposition](figures/a11_17_interface_paraphrase_usefulness_decomposition.png)

The heatmap shows that the initialization transient is common to all four cells. The trajectory panel then separates them: H2 seen/unseen become strongly positive, while H1 seen/unseen become negative. Since H2-unseen AUC passes `4/5`, unseen paraphrase transport is not the dominant persistent failure.

## Theoretical Update

Let $J_2=\partial h_T/\partial\theta$ and $J_1=\partial h_{T+1}/\partial\theta$. After the H2 descent direction becomes aligned with its semantic vector $d_2$, standard-H1 usefulness has the form:

$$
U_{1\leftarrow2}=v_1^\top J_1J_2^\top d_2.
$$

The self-kernel $J_2J_2^\top$ is positive semidefinite. The cross-interface kernel $J_1J_2^\top$ is not, so its bilinear form has no guaranteed sign. This is the precise theoretical gap between direct H2 supervision and standard-H1 benefit.

## Claim Boundary And Next Decision

We can say that the persistent local bottleneck on this task lies in H2/$h_T$ to H1/$h_{T+1}$ transport after an initial full-vocabulary transient. We cannot yet say whether the loss comes mainly from changing the output head or changing the hidden-state position, and cannot infer global MTP efficiency.

The next minimal audit crosses readout head (H2/H1) with state position ($h_T/h_{T+1}$) on seen examples after burn-in. This directly tests the cross-interface kernel components without changing training.

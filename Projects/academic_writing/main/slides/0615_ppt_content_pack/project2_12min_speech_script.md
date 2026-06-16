# 12-Minute Speech Script

Topic: **Why Sparse MoE Routers Collapse Before They Specialize**  
Presenter: **Deng Xingyu / 邓星宇, Student ID: 250010109**  
Deck: `project2_12min_deck_0615_template_based.pptx`  
Timing plan: **main slides 1-13, about 11.5-12 minutes; backup slides 14-15 only for Q&A.**

## Slide 01. Title

Timing: 35s.

I will present a mechanism audit of sparse MoE routing. The goal is not to claim a finished routing method. The question is why a top-1 router can concentrate many tokens onto a few experts before useful specialization forms. The final part tests an expert-spectrum initialization idea and shows that initialization alone is not enough.

## Slide 02. Agenda

Timing: 35s.

The talk has six parts. I first motivate why routing geometry matters for sparse MoE scaling. Then I define the research question. The middle part gives the common-logit mechanism and training-dynamics evidence. The last part presents the expert-spectrum stress test, the claim boundary, and the next decision.

## Slide 03. Motivation

Timing: 50s.

Sparse MoE increases parameter count while activating only a few experts per token. That makes the router the bottleneck: it controls which experts see data and receive gradients. Prior MoE work studies scaling and load balance. Recent geometry work adds a warning: routing patterns can reflect hidden-state geometry rather than semantic expertise. I use that boundary throughout this talk.

## Slide 04. Research Question

Timing: 45s.

The working thesis is simple. Hidden states may contain useful residual structure, but they also contain a shared common direction. A linear top-1 router can convert that shared direction into expert-specific offsets. The research question is whether expert-aware initialization can reduce the early bias, or whether training quickly amplifies it again.

## Slide 05. False Positive

Timing: 45s.

Route consistency can be misleading. A feature may route consistently, but many different features can still share one expert. That is a false positive for specialization. So I track three things together: expert load, assignment structure, and whether an intervention changes the routing pattern.

## Slide 06. Positive Control

Timing: 50s.

This positive control rules out a weak explanation. The model is not fundamentally unable to specialize. When the early routing basin is controlled by slot-aware initialization or oracle release, stable slot-to-expert structure can appear. Therefore the bottleneck is basin entry during early training, not the impossibility of specialization.

## Slide 07. Common-Logit Mechanism

Timing: 60s.

The mechanism is common-logit bias. I decompose the hidden state as h_i equals c plus r_i. The gate score then contains a common term and a residual term. The common term is shared across tokens, but its value differs across experts because each expert has a different router weight. Under top-1 routing, this term can act like an expert-specific offset.

## Slide 08. Controlled Evidence

Timing: 50s.

In the controlled setting, common-logit appears before the slot margin becomes decisive. More importantly, cancelling the common-logit improves slot NMI while preserving accuracy. This makes the mechanism intervention-relevant, not just descriptive. It supports the idea that a shared direction can distort early top-1 routing.

## Slide 09. Real-Text Audit

Timing: 50s.

Real text narrows the claim. After removing the top one percent high-frequency tokens, random linear routers still show step-zero load bias. Centering or common removal reduces that bias, but it does not remove all structure. So the real problem is not only static initialization bias; it is how early training amplifies or reshapes that bias.

## Slide 10. Training Dynamics

Timing: 55s.

The training-dynamics audit shows that step-ten concentration is not gate-only. Freezing only the router or only experts does not explain the full spike. Freezing the prefix before layer 5 suppresses most amplification, and replay shows a large router-hidden-state interaction. This predicts that a purely linear initialization may help at step zero but fail after updates.

## Slide 11. Expert-Spectrum Test

Timing: 55s.

The expert-spectrum test initializes the router from each expert's principal input geometry. These expert subspaces are measurable, differ across experts, and have low overlap with the hidden-state common direction. That makes the idea computationally meaningful. But it is still not a claim of semantic specialization; it is a routing-geometry initialization test.

## Slide 12. Stress-Test Result

Timing: 60s.

The result is mixed and informative. After filtering the common direction, step-zero balance improves: max expert load drops from 19.98 percent to 13.97 percent. But after ten steps, max load becomes worse: 93.51 percent compared with 83.16 percent for random initialization. The conclusion is precise: better initial balance does not control early training amplification.

## Slide 13. Conclusions

Timing: 60s.

The updated conclusion has three parts. First, expert geometry exists and is not identical to the common direction. Second, common-filtered initialization improves step-zero balance. Third, step-ten concentration is driven by router-hidden-state amplification, not initialization alone. The next decision is to audit whether early route winners are reinforced by hidden-state change and router updates.

## Backup 14. Claim Boundary

Backup only.

This is the claim boundary. I can claim measurable expert-spectrum directions, improved step-zero balance, and failure of the current linear top-1 initialization to prevent step-ten concentration. I cannot claim expert spectrum is useless, that domain specialization is explained, or that the result generalizes to larger pretrained MoEs or different routing settings.

## Backup 15. References

Backup only.

These references position the project. The classical MoE papers define sparse routing and load-balancing concerns. The recent geometry papers motivate the claim boundary: routing geometry is meaningful, but it should not be confused with semantic domain expertise.

## Definition Repair Card

1. Variance Routing (Working Definition):
   - It is NOT: Merely possessing an x*x term in the architecture.
   - It IS: The magnitude of the logit margin provided by the second-order term (W2) significantly dominating the margin provided by the first-order term (W1) when separating two distinct domains.

2. Expert Specialization (Working Definition):
   - It is NOT: Large logit margins or low internal covariance rank.
   - It IS: A high Mutual Information state I(E; C) between the routing assignment (E) and the true semantic domain (C), bounded by healthy load balancing H(E). It is an *assignment phenomenon*.

3. Expert Low-rankness (Working Definition):
   - It is NOT: An architecture feature, nor a guarantee of good task performance.
   - It IS: A geometric state where the input feature covariance inside an expert (C_e) occupies a low-dimensional subspace, mathematically best captured by the energy rank r_{0.9}, not the tail-sensitive ED.

4. The Causal Relationship:
   Architecture (Quadratic) -> enables Mechanism (Variance Routing) -> drives Assignment (Specialization) -> filters data into Geometric State (Low-rankness) -> enables CL Outcome (Orthogonal gradients / Low Interference).

5. DANGER - Concept Misuse Points:
   - "High Margin means experts are specialized." -> FALSE. Margin can blow up due to mean shifts/norm inflation without any purity (e.g., linear_no_center).
   - "Quadratic router is a variance router." -> UNPROVEN. We built a quadratic router; we have not yet verified if it *uses* the variance term to make its primary decisions (needs \rho > 1).

## Impact on Main Iteration

This side-discussion must trigger the following updates in the main checkpoint:

- Hypothesis:
  - Rewrite any hypothesis that assumes Quadratic *is* Variance Routing. Update to: "Quadratic architecture *allows* variance routing, but we must empirically verify if the margin attribution (\rho) is dominated by the second order."

- Mathematical Modeling:
  - Replace the vague "low-rankness = anti-forgetting" narrative with the explicit Micro-Bridge: "Low-rankness (small r_{0.9}) reduces the spatial volume occupied by Domain A, maximizing the probability that Domain B's gradient updates fall into orthogonal null spaces, mathematically measured by low Spectral Interference (Tr(C_A C_B))."

- Metric Design:
  - DEPRECATE: `Margin` as a proxy for anything other than raw numerical confidence.
  - DEPRECATE: `ED_comp` as the primary rank metric.
  - INTRODUCE: `r_0.9` (Energy Rank) for geometric compactness.
  - INTRODUCE: `NMI` (Normalized Mutual Information) for Specialization.

- Experiment Design:
  - Before starting the Two-Task Forgetting Test, the Experiment AI MUST calculate the attribution ratio \rho for the existing quadratic_debias model to see if it even learned to route by variance at ckpt40000.
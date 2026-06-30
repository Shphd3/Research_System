# Nested Prediction, Spectral Anisotropy, and Common-Mode Bias in Attention

## Abstract

This note develops a causal theory for how next-token prediction can create anisotropic feature representations, and how this anisotropy can later distort compositional similarity in self-attention and output readout. The theory separates two processes that must not be conflated. The first process is nested next-token learning. This is a training-time process in which shorter and more frequent predictive contexts are learned earlier and more repeatedly, while longer and more specific contexts are learned later inside the geometry already shaped by the earlier contexts. The second process is recursive semantic composition. This is a representation-use process in which learned concepts are combined into phrases, clauses, sentences, and discourse.

The central causal claim is that nested next-token learning can create an entropic spectral distribution for learned features. A common feature first becomes aligned with a useful singular direction, and then cross-entropy-like training can continue to increase the singular value of that direction because larger finite margins still reduce loss. Once a high-gain common subspace exists, later nested features are learned through local Jacobians whose leading singular directions produce larger first-order loss decrease when the prediction error has nonzero alignment with those directions. This creates an optimization-level attraction toward reusing and extending the already high-gain subspace. Because all atomic concepts are learned from the same human-language distribution under the same objective, different concepts may have different long-tail meanings while still sharing a language-induced low-rank common spectral backbone.

Recursive semantic composition then inherits this backbone. A composed representation may contain both a high-gain common component and a lower-gain unique component. The common component can be useful for generic prediction, but it is weak for discriminating among nearby candidates because many concepts share it. The unique component may contain the true relation, but it can be lower-gain. Attention and output softmax then convert score or logit advantages into exponential routing or probability advantages. Therefore, when the high-gain common component dominates the score while the true relation is carried by the long-tail component, the model can prefer amplified commonality over true compositional similarity.

The note organizes the argument as a chain of propositions. Each proposition proves one causal arrow: common features produce stable high-gain directions; high-gain directions attract later nested learning; shared language training creates common low-rank spectral modes across concepts; recursive composition accumulates common projections; softmax turns common-mode score advantage into exponential selection bias; and update-space suppression is the appropriate intervention because the failure mechanism lives in the actual descent direction, not merely in hidden-state norm.

## 1. The Two Processes That Must Be Kept Separate

The first process is nested next-token learning. This process is induced by the training objective. When the training distribution contains a sequence pattern such as $A B C D$, the model receives prediction signal through a nested sequence of contexts. The context $A$ constrains what can follow. The context $A B$ constrains the next-token distribution more sharply. The context $A B C$ gives an even more specific predictive condition. The longer context $A B C D$ represents a still more specialized condition. This is not semantic composition. It is an ordered predictive structure created by next-token training.

The second process is recursive semantic composition. This process concerns how language uses the learned features. Atomic concepts compose into phrases, phrases compose into clauses, clauses compose into sentences, and sentences compose into discourse. The semantic composition process uses features that have already been shaped by training. Therefore, if nested next-token learning creates anisotropic feature geometry, recursive semantic composition does not occur in a neutral space. It inherits the anisotropic geometry created by training.

This separation is necessary for a rigorous causal account. Nested prediction explains the origin of the spectral distribution. Recursive composition explains why that spectral distribution can distort similarity. Without this separation, one might say only that language is compositional and therefore representations are anisotropic. That statement is not causal. The more precise statement is that nested prediction creates an anisotropic spectral distribution, and recursive semantic composition later exposes the functional consequences of that distribution.

## 2. Causal Mechanism I: Nested Prediction Creates an Entropic Spectral Distribution

A next-token model learns features through a nested predictive process. When the training distribution contains a sequence pattern such as $A B C D$, the model receives gradient signal in an ordered predictive structure. The context $A$ helps shape the prediction of later tokens. The context $A B$ gives a more constrained predictive condition. The context $A B C$ gives an even more constrained condition. The context $A B C D$ defines a still more specific prediction condition. This is nested next-token learning rather than semantic composition.

Because the objective uses softmax cross-entropy, any direction that increases the correct token's logit relative to competing logits receives selective reinforcement. If an early feature such as $A$ is frequent and useful across many contexts, the associated direction receives this reinforcement many times. This repeated reinforcement has two consequences. First, it can align a singular direction of a learned matrix with the useful feature. Second, after alignment has mostly stabilized, it can continue to increase the corresponding singular value because larger finite margins still reduce cross-entropy loss.

Once this high-gain subspace has formed, later nested features such as $A B$, $A B C$, and $A B C D$ are learned inside an already anisotropic geometry. Their gradients are evaluated through matrices whose leading singular directions already produce larger first-order loss decrease when the output-side error has nonzero alignment with those directions. Therefore, when a new nested feature has prediction error partially aligned with the existing high-gain subspace, the loss-reducing update is biased toward reusing and extending that subspace rather than creating a fully independent isotropic direction.

This mechanism produces an entropic spectral distribution. Common predictive structure accumulates in high-singular-value, low-rank directions. More specific or rarer information is pushed into lower-gain long-tail directions, unless it receives enough repeated and discriminative pressure to create its own high-gain direction. The distribution is called entropic because the functional effect of a feature is spread across singular modes with an uneven mass distribution rather than evenly over dimensions.

## 3. Causal Mechanism II: Recursive Composition Can Distort Similarity

### 3.1 Shared Language-Induced Anisotropy Across Atomic Concepts

Atomic concepts can denote very different semantic objects, such as a city, a legal relation, a biological category, a physical attribute, or an action. However, in a language model these concepts are not learned from separate semantic universes. They are all learned through the same human-language distribution and the same next-token objective. Therefore, even when their meanings differ, their representations are shaped by the same global predictive regularities of language.

This point is causal. If many concepts are learned through the same training objective, and if that objective repeatedly rewards certain broad predictive factors, then those broad factors create shared high-gain directions. These directions are not tied to one concept alone. They become part of the common representational infrastructure of the model. A concept-specific vector can still contain unique semantic information, but its functional effect is measured through matrices whose leading singular directions have already been shaped by language-wide common prediction. Therefore, different atomic concepts can share the same anisotropic low-rank spectral space even when their long-tail semantic meanings are different.

A useful decomposition is the following.

$$
h_f = h_{\mathrm{lang}} + h_{\mathrm{class},f} + h_{\mathrm{unique},f}
$$

Here, $h_f$ is the representation of atomic feature $f$. The term $h_{\mathrm{lang}}$ is the language-wide common component induced by broad predictive regularities shared across many concepts. The term $h_{\mathrm{class},f}$ is the component shared by a narrower semantic class to which $f$ belongs. The term $h_{\mathrm{unique},f}$ is the feature-specific long-tail component that distinguishes $f$ from nearby alternatives.

This decomposition is not an assumption that the model explicitly stores three orthogonal variables. It is an analytic decomposition that separates three sources of variation. The first source is language-wide common structure. The second source is class-level common structure. The third source is concept-specific distinction. The causal theory predicts that the first two sources are more likely to occupy high-gain spectral directions, while the third source is more likely to require lower-gain or broader spectral directions unless it is very frequent and highly predictive.

### 3.2 Recursive Composition Inherits the Shared Spectral Backbone

Human language then uses the already-learned atomic concepts through recursive semantic composition. Atomic concepts compose into phrases, phrases compose into clauses, clauses compose into sentences, and sentences compose into discourse. Because the atomic concepts already carry entropic spectral distributions, their compositions inherit both a shared high-gain common component and lower-gain unique long-tail components.

This inherited geometry affects similarity. When self-attention computes query-key similarity, the score is a dot product after learned projections. A high-gain common component can dominate the score because it lies in directions that the learned projections amplify. The problem is that the common component is shared by many competing concepts. It supports generic similarity, but it may not identify the correct compositional relation. The true relation often depends on the unique long-tail component that distinguishes one phrase or concept from nearby alternatives. Thus, after nested prediction creates a high-gain common subspace, recursive composition can make attention prefer amplified commonality over the long-tail feature structure needed for true similarity.

## 4. Local Linear Training Is the Correct Level of Analysis

The theory is local because gradient descent itself is local. Each update is chosen from the first-order Taylor expansion of the loss around the current parameter state. The causal question is not whether the entire transformer is globally linear. The causal question is whether, at a given training step, a candidate movement through a high-singular-value direction produces a larger immediate loss decrease than a movement of the same norm through a lower-gain direction.

Let $\theta$ be the current parameters and let $\delta\theta$ be a small candidate update. The first-order Taylor expansion of the loss is the following.

$$
L(\theta+\delta\theta) \approx L(\theta)+\langle \nabla_\theta L(\theta),\delta\theta\rangle
$$

Here, $L(\theta)$ is the loss at the current parameter state, $\nabla_\theta L(\theta)$ is the gradient, and $\delta\theta$ is the candidate movement. The first-order term determines which infinitesimal movement decreases the loss fastest. This is the object optimized by gradient descent and by Adam-type updates after preconditioning.

For a selected matrix block or representation map, write the local functional change as $\delta z \approx J_t\delta\theta$, where $J_t$ is the local Jacobian at step $t$. Singular values matter in this local map because they determine how much logit, attention-score, or hidden-state change is produced by a unit movement in each singular direction. Therefore, local linearization is not a mathematical convenience added after the fact. It is the natural framework for proving why high-singular-value directions are descent-efficient and why later learning can be attracted to an already formed high-gain subspace.

## 5. Causal Arrow I: Common Features First Create Stable High-Gain Directions

This section proves the first causal arrow: repeated prediction signal for a common feature can create a stable high-gain direction. The result has two parts. The singular vector discovers which feature direction should be read or written. The singular value controls how strongly that direction is amplified. Cross-entropy-like training can separate these processes into an early direction-discovery phase and a later gain-amplification phase.

Consider the rank-one model $W(t)=\sigma(t)u_\star v(t)^\top$. Here, $W(t)$ is the trainable matrix at time $t$, $\sigma(t)$ is the singular value, $u_\star$ is a fixed output-side direction, and $v(t)$ is the input-side singular vector constrained to have unit norm. Let $x$ be a unit feature direction, and define the alignment $c(t)=v(t)^\top x$. The scalar margin is the following.

$$
m(t)=\sigma(t)c(t)
$$

Here, $m(t)$ is the useful output strength of the feature. The quantity $\sigma(t)$ is gain, and $c(t)$ is direction alignment. The loss is assumed to be a decreasing function of the margin, $\ell=\phi(m)$, with residual pressure $r(m)=-\phi'(m)>0$. This assumption includes logistic or cross-entropy-like margin losses at finite margin.

Under gradient flow with $v(t)$ constrained to the unit sphere, the singular-value dynamics are the following.

$$
\frac{d\sigma}{dt}=r(m)c
$$

This equation says that the gain increases when the current singular vector has positive alignment with the feature and the loss still rewards a larger margin. The alignment dynamics are the following.

$$
\frac{dc}{dt}=r(m)\sigma(1-c^2)
$$

This equation says that the singular vector rotates toward the feature direction, but the rotation slows down as $c$ approaches $1$ because the remaining tangent misalignment is proportional to $1-c^2$.

Dividing the alignment equation by the singular-value equation gives a relation that removes the residual pressure.

$$
\frac{dc}{d\sigma}=\frac{\sigma(1-c^2)}{c}
$$

Integrating gives the following identity.

$$
1-c(t)^2=(1-c(0)^2)\exp\left(-\left(\sigma(t)^2-\sigma(0)^2\right)\right)
$$

This identity proves the two-phase mechanism. Alignment error decays exponentially as singular gain grows. Once $c(t)$ is close to $1$, the factor $1-c^2$ makes further direction learning small. However, the singular-value equation becomes approximately $d\sigma/dt\approx r(m)$, so gain can continue to grow as long as the loss still rewards a larger finite margin.

This proves the causal arrow from repeated common-feature prediction to a stable high-gain direction. Frequent common features receive many opportunities for this process. Their directions can stabilize early, and their gains can keep growing later. Therefore, common features can form high-gain spectral backbones before rarer nested features have been learned strongly.

## 6. Causal Arrow II: Existing High-Gain Directions Attract Later Nested Features

The previous section explains how high-gain directions can form. This section proves why later nested features are attracted to such directions. The question is local and causal: if a high-gain direction already exists, why should a later feature reuse it instead of forming a new low-gain direction? The answer is that, for the same movement size, high-gain directions produce larger first-order loss decrease whenever the prediction error has nonzero alignment with the corresponding output-side mode.

Consider a local linear map from hidden representation to logits.

$$
z=Wh
$$

Here, $h\in\mathbb{R}^d$ is the hidden representation, $W$ is the current output or local readout matrix, and $z$ is the logit vector. Let the singular value decomposition be the following.

$$
W=\sum_i \sigma_i u_i v_i^\top
$$

Here, $v_i$ is the input-side singular direction, $u_i$ is the output-side singular direction, and $\sigma_i$ is the gain of mode $i$. For softmax cross-entropy with target $y$, the logit gradient is $p-e_y$, where $p=\operatorname{softmax}(z)$ and $e_y$ is the one-hot target vector. The gradient with respect to $h$ is therefore the following.

$$
\nabla_h L = W^\top(p-e_y)=\sum_i \sigma_i\langle u_i,p-e_y\rangle v_i
$$

This equation says that gradient flow through the hidden representation is weighted by singular values. The coefficient along $v_i$ is proportional to $\sigma_i\langle u_i,p-e_y\rangle$. A mode receives gradient only if the output-side error has nonzero alignment with $u_i$, but once that alignment exists, larger $\sigma_i$ gives larger gradient flow along $v_i$.

Now consider an infinitesimal movement along $v_i$, written as $\delta h=\epsilon v_i$, where $\epsilon$ is the movement size. The induced logit change is $\delta z=\epsilon\sigma_i u_i$. The first-order loss change is the following.

$$
\delta L \approx \epsilon\sigma_i\langle p-e_y,u_i\rangle
$$

If the movement sign is chosen to reduce loss, the best first-order decrease from a movement of norm $\epsilon$ in this one-dimensional subspace is proportional to $\epsilon\sigma_i|\langle p-e_y,u_i\rangle|$. This proves that high-gain directions are descent-efficient when they are aligned with the current prediction error.

For an actual gradient step, the mode-$i$ hidden update is proportional to $-\eta\sigma_i\langle u_i,p-e_y\rangle v_i$. The induced logit change then contains another factor of $\sigma_i$, so the mode-level first-order loss decrease is the following.

$$
\Delta L_i \approx -\eta\sigma_i^2\langle u_i,p-e_y\rangle^2
$$

Here, $\eta$ is the learning rate. This equation proves the attraction mechanism. If a later nested feature has any prediction-error alignment with an already high-gain output-side mode, then reusing the corresponding input-side singular direction gives a loss decrease that scales with $\sigma_i^2$. Therefore, later features are not learned in a neutral space. They are learned inside a geometry where existing high-gain modes are locally easier to use.

This proves the causal arrow from existing high-gain subspace to later-feature attraction. The theorem does not say that all later features must collapse into the top subspace. It says that the local objective gives those directions a systematic advantage when they are even partially aligned with the error. This advantage is enough to explain why nested learning tends to reuse and extend the high-gain common backbone.

## 7. Causal Arrow III: Shared Language Training Creates Functional Coupling Across Concepts

The previous two sections explain how a common feature can create a high-gain direction and why later features tend to reuse it. This section explains why different atomic concepts can share the same low-rank spectral space even when their meanings differ. The cause is not semantic identity. The cause is shared training through the same human-language distribution and the same next-token objective.

Let $h_f$ and $h_g$ be two feature representations. Their raw hidden-space overlap is $\langle h_f,h_g\rangle$. If the hidden space were read isotropically, this raw overlap would be the relevant similarity. However, a learned matrix $W$ reads the two features through its singular spectrum. The output-effect overlap is the following.

$$
\langle Wh_f,Wh_g\rangle=\sum_i \sigma_i^2\langle h_f,v_i\rangle\langle h_g,v_i\rangle
$$

Here, $v_i$ is the input-side singular direction of $W$, and $\sigma_i$ is the corresponding singular value. The equation follows by substituting $Wh_f=\sum_i\sigma_i u_i\langle v_i,h_f\rangle$ and using orthonormality of the output-side singular vectors $u_i$.

This equation proves functional coupling. If two concepts share small projections onto a high-gain language-induced direction, their output effects can have large overlap because the overlap is weighted by $\sigma_i^2$. Thus two concepts can be semantically different in their unique components while still being strongly coupled through a shared high-gain common mode.

This proves the causal arrow from shared language training to shared functional spectral space. The language-wide common component $h_{\mathrm{lang}}$ does not need to encode the distinguishing meaning of each concept. It only needs to be repeatedly useful across many prediction events. Once the model gives this component high gain, any concept that carries it will be functionally amplified along the same low-rank backbone.

## 8. Causal Arrow IV: Recursive Semantic Composition Accumulates Common Modes

Now move from nested prediction to semantic composition. Suppose a hidden state represents three semantic features $A$, $B$, and $C$. A useful representation-learning ideal is approximate additivity plus a residual interaction term.

$$
h_{ABC}=h_A+h_B+h_C+r_{ABC}
$$

Here, $h_A$, $h_B$, and $h_C$ are atomic feature components, and $r_{ABC}$ is the residual interaction needed for the exact configuration. This equation belongs to the semantic-composition stage, not the nested-prediction stage. It states a representation hypothesis that can be tested by regressing the sentence representation on phrase or feature representations and measuring the residual.

Expand the atomic features in the input-side singular basis of a readout matrix $W$.

$$
h_A=\sum_i a_i v_i,\quad h_B=\sum_i b_i v_i,\quad h_C=\sum_i c_i v_i
$$

Here, $a_i$, $b_i$, and $c_i$ are the coordinates of the three atomic features along singular direction $v_i$. Applying $W$ to the additive part gives the following.

$$
W(h_A+h_B+h_C)=\sum_i\sigma_i(a_i+b_i+c_i)u_i
$$

Here, $a_i+b_i+c_i$ is the raw composed coefficient along singular direction $v_i$, while $\sigma_i(a_i+b_i+c_i)$ is the functional readout coefficient. If the atomic features share a common projection onto a high-gain direction, their coefficients add coherently and are then multiplied by a large singular value. The residual term $r_{ABC}$ may distinguish the exact semantic configuration, but it can remain functionally weaker if it lies in lower-gain directions.

Let $P_k=\sum_{i\leq k}v_iv_i^\top$ project onto the leading input-side singular directions. The top-subspace and residual-subspace logits are defined as follows.

$$
z^{\mathrm{top}}=WP_kh_{ABC},\quad z^{\mathrm{res}}=W(I-P_k)h_{ABC}
$$

Here, $z^{\mathrm{top}}$ is the logit vector produced by the leading singular subspace, and $z^{\mathrm{res}}$ is the logit vector produced by the remaining directions. The full logit vector is $z=z^{\mathrm{top}}+z^{\mathrm{res}}$.

This decomposition proves the causal arrow from shared atomic backbone to composed common-mode accumulation. If several atomic features contain the same language-induced common component, then recursive semantic composition can accumulate that component. If the accumulated common mode favors a common competing token more than the residual component favors the rare correct target, then the output distribution can be dominated by commonality rather than by the exact composition.

## 9. Causal Arrow V: Softmax Converts Common-Mode Advantage into Probability Suppression

This section proves how a common-mode logit advantage becomes a probability-level failure. Let $y$ be the correct target token and let $c$ be a common competing token. Let $z_y$ and $z_c$ be their logits. Define the common-over-target logit gap as $\Delta_{c,y}=z_c-z_y$.

If $\Delta_{c,y}>\gamma>0$, then the probability assigned to the correct target satisfies the following bound.

$$
p_y\leq \exp(-\gamma)
$$

Here, $p_y$ is the softmax probability of the correct target. The proof is direct. The softmax probability is $p_y=\exp(z_y)/\sum_\ell\exp(z_\ell)$. Since the denominator contains the term $\exp(z_c)$, we have $\sum_\ell\exp(z_\ell)\geq\exp(z_c)$. Therefore, $p_y\leq \exp(z_y)/\exp(z_c)=\exp(z_y-z_c)=\exp(-\Delta_{c,y})$. If $\Delta_{c,y}>\gamma$, then $p_y\leq\exp(-\gamma)$.

This theorem proves the causal arrow from common-mode logit advantage to exponential suppression of the rare target. The theorem does not assume that the residual information is absent from the hidden state. It only assumes that the final logit gap favors the common competitor by a positive margin. Therefore, a model can contain the rare compositional information in a lower-gain residual component and still assign low probability to the correct token if the high-gain common component creates a stronger competing logit.

## 10. Causal Arrow VI: Attention Suffers the Same Common-Mode Softmax Bias

The output head is not the only softmax bottleneck. Attention introduces another selection stage before the final readout. At query position $t$, the query and key vectors are defined as follows.

$$
q_t=W_Qh_t,\quad k_i=W_Kh_i
$$

Here, $q_t$ is the query vector at position $t$, and $k_i$ is the key vector at candidate source position $i$. The attention score is the scaled dot product.

$$
s_{ti}=\frac{q_t^\top k_i}{\sqrt{d_k}}
$$

Here, $d_k$ is the key dimension. The attention weight is the softmax over scores.

$$
\alpha_{ti}=\frac{\exp(s_{ti})}{\sum_j\exp(s_{tj})}
$$

For two candidate keys $i$ and $j$, the attention-weight ratio is the following.

$$
\frac{\alpha_{ti}}{\alpha_{tj}}=\exp(s_{ti}-s_{tj})
$$

This identity proves that any score advantage becomes a multiplicative routing advantage. Therefore, if the score advantage comes from a high-gain common component rather than from a discriminative relation, softmax will still amplify it.

The same descent-efficiency logic applies to $W_Q$ and $W_K$. If a query or key singular direction produces useful score changes, the local first-order loss decrease can favor increasing that direction's gain. Therefore, attention matrices can also develop high-gain common modes. Once these modes exist, the attention score can be decomposed into a top-band contribution and a tail-band contribution.

$$
s_{ti}=s_{ti}^{\leq k}+s_{ti}^{>k}
$$

Here, $s_{ti}^{\leq k}$ is the contribution from the leading spectral band, and $s_{ti}^{>k}$ is the contribution from the remaining directions. For a correct key $j^+$ and a distractor key $j^-$, define the attention contrast.

$$
\Delta s=s_{tj^+}-s_{tj^-}
$$

Here, $\Delta s$ measures whether the query prefers the correct key over the distractor. The harmful pattern is not merely that $s^{\leq k}$ is large. The harmful pattern is that $s^{\leq k}$ is large but weakly discriminative, while $s^{>k}$ is smaller but more discriminative. In that case, the top spectral band dominates score magnitude, but the tail band carries the correct relation.

Define the score-magnitude CDF as follows.

$$
C_{\mathrm{score}}(k)=\frac{|s^{\leq k}|}{|s|}
$$

Here, $C_{\mathrm{score}}(k)$ measures how much of the raw attention score magnitude comes from the top band. Define the discrimination CDF as follows.

$$
C_{\mathrm{disc}}(k)=\frac{\Delta s^{\leq k}}{\Delta s}
$$

Here, $C_{\mathrm{disc}}(k)$ measures how much of the correct-versus-distractor contrast comes from the top band. The failure signature is $C_{\mathrm{score}}(k)$ rising much faster than $C_{\mathrm{disc}}(k)$. That pattern would show that the top band is functionally large but relation-poor, which is exactly the proposed attention-side failure mode.

## 11. Entropic Spectral Distribution as a Measurable Object

The causal story requires an operational measure of spectral concentration. Let $f$ be a learned feature direction expressed in the input space of a matrix $W=\sum_i\sigma_i u_i v_i^\top$. The unweighted alignment of $f$ with mode $i$ is $\langle f,v_i\rangle^2$. However, the functional effect of this alignment is not unweighted. Because the map multiplies mode $i$ by $\sigma_i$, the gain-weighted mass of $f$ in mode $i$ is defined as follows.

$$
m_i(f)=\sigma_i^2\langle f,v_i\rangle^2
$$

Here, $m_i(f)$ measures the squared output effect of the component of $f$ along singular mode $i$. Normalize this mass into a probability distribution.

$$
p_i(f)=\frac{m_i(f)}{\sum_j m_j(f)}
$$

Here, $p_i(f)$ is the fraction of the gain-weighted feature effect carried by mode $i$. The spectral entropy of the feature is the following.

$$
H(f)=-\sum_i p_i(f)\log p_i(f)
$$

Here, $H(f)$ measures how evenly the feature's functional effect is distributed across singular modes. Low entropy means that the feature's effect is concentrated in a small high-gain band. High entropy means that the feature's effect is spread more evenly across many modes.

The top-$k$ gain-weighted mass is the following.

$$
E_k(f)=\frac{\sum_{i\leq k}\sigma_i^2\langle f,v_i\rangle^2}{\sum_i\sigma_i^2\langle f,v_i\rangle^2}
$$

Here, $E_k(f)$ measures how much of the feature's gain-weighted effect lies in the top $k$ singular directions. The theory predicts that frequent common features should acquire larger $E_k(f)$ for small or moderate $k$, while specific long-tail features should require larger $k$ to be represented discriminatively unless they receive sufficient repeated reinforcement.

This definition also separates hidden-space energy from functional effect. A feature may have small hidden-space projection into the top singular band, but if the singular values in that band are much larger, the gain-weighted effect can still be large. This distinction is exactly what the matched readout CDF experiment reveals.

## 12. Empirical Readout CDF Evidence and Updated Claim Boundary

The matched phrase-change experiment gives a direct readout-side diagnostic. For a matched sentence pair, let $\Delta h$ be the final-token hidden-state change. Let $P_k$ project onto the top $k$ hidden-side singular directions of $W_{\mathrm{out}}$. Define the hidden-space CDF as follows.

$$
C_{\mathrm{hidden}}(k)=\frac{\|P_k\Delta h\|^2}{\|\Delta h\|^2}
$$

Here, $C_{\mathrm{hidden}}(k)$ measures how much of the hidden-state change lies in the top $k$ singular directions. Define the logit-space CDF as follows.

$$
C_{\mathrm{logit}}(k)=\frac{\|W_{\mathrm{out}}P_k\Delta h\|^2}{\|W_{\mathrm{out}}\Delta h\|^2}
$$

Here, $C_{\mathrm{logit}}(k)$ measures how much of the output-logit change is produced by the top $k$ hidden-side singular directions.

The updated result gives the correct claim boundary. At strict top $1\%$, which corresponds to $k=11$ for $d=1024$, the top band contains only $3.6\%$ of hidden change but produces $17.8\%$ of logit change. This proves amplification but not dominance. At $k=64$, the top $6.25\%$ of directions contains $19.2\%$ of hidden change but produces $47.2\%$ of logit change. At $k=128$, the top $12.5\%$ contains $32.8\%$ of hidden change but produces $62.7\%$ of logit change.

The supported interpretation is therefore a spectral-band claim, not a strict top-$1\%$ claim. The strict top $1\%$ is a high-gain spike. The broader top $64$ to $128$ band is the readout-active spectral band in this experiment. This evidence supports the middle of the causal chain: the representation has a high-gain spectral hierarchy, and the readout makes this hierarchy functionally important. It does not by itself prove the attention-side discriminativity failure. That requires the attention CDF and discrimination diagnostics defined above.

## 13. Optimizer Implication: The Intervention Must Act on Update-Space Reuse

The causal chain identifies the failure mechanism as common-subspace reuse and gain domination. Therefore, an intervention should not merely bound hidden-state norm or shrink all singular values uniformly. It should reduce the actual update flow through the common subspace when that flow would allow already-learned common structure to monopolize later long-tail learning.

Let $C$ be a frozen common-feature subspace with projector $P_C$. Let $u_t$ be the preconditioned AdamW update direction for a selected parameter block before weight decay. The relevant failure metric is the common-subspace update fraction.

$$
\alpha_t^{\mathrm{upd}}=\frac{\|P_Cu_t\|^2}{\|u_t\|^2+\epsilon}
$$

Here, $\alpha_t^{\mathrm{upd}}$ measures how much of the actual optimizer update lies inside the common subspace. A method that directly addresses the causal mechanism should reduce this quantity for active long-tail updates while also preventing already-learned common examples from continuing to train unnecessarily.

A confidence-capped loss supplies the first part. If $q<1$ is a confidence threshold, the hard capped loss is $\ell_{\mathrm{cap}}=\max(-\log p_y+\log q,0)$. When $p_y\geq q$, the loss is zero and the common example produces no gradient. This prevents already-learned common examples from continuing to increase margins or leaking into complementary directions.

Update-space suppression supplies the second part. Define the corrected update direction as follows.

$$
\tilde u_t=r_t(I-\rho_tP_C)u_t
$$

Here, $r_t$ is a residual learning gate, and $\rho_t$ controls the suppression strength. Because $P_C$ is an orthogonal projector, the update decomposes exactly as follows.

$$
(I-\rho_tP_C)u_t=(1-\rho_t)P_Cu_t+P_{\perp C}u_t
$$

Here, $P_{\perp C}=I-P_C$ is the complementary projector. This identity proves that the common-subspace component is multiplied by $1-\rho_t$, while the complementary component is preserved before residual gating. Therefore, the common-to-complementary update-energy ratio is multiplied by $(1-\rho_t)^2$ whenever the complementary component is nonzero.

This is why the intervention must act on the actual update direction. Spherical hidden states or bounded hidden geometries may change activation norm, but they do not guarantee reduction of $\|P_Cu_t\|$ relative to $\|P_{\perp C}u_t\|$ in the optimizer update. The failure mechanism is an update-space subspace-reuse mechanism, so the rigorous intervention must control update-space reuse.

## 14. Diagnostics and Falsification Criteria

The causal chain is useful only if each arrow can be tested. The first diagnostic is subspace formation and stability. Let $P_k(t)$ be the top-$k$ singular projector of a selected matrix at checkpoint $t$. The drift is measured by $\delta_k(t)=\|P_k(t)-P_k(t-\Delta)\|_2$. The two-phase theory predicts that subspace drift should be large during direction discovery and smaller after the common backbone stabilizes.

The second diagnostic is gain growth. Let $S_k(t)=\sum_{i\leq k}\sigma_i(t)^2$. Under ordinary cross-entropy, the two-phase theory predicts that $S_k(t)$ can continue growing after the subspace drift becomes small. Under confidence capping or update-space suppression, late-stage growth should be reduced if the intervention controls unnecessary margin amplification.

The third diagnostic is feature spectral mass. For a known feature direction $f$, measure $E_k(f)$ and $H(f)$. The theory predicts that common features should have more concentrated gain-weighted mass than rare discriminative features, unless the rare features have received sufficient direct reinforcement.

The fourth diagnostic is readout domination. For a rare compositional target $y$ and a common competitor $c$, decompose logits into $z^{\mathrm{top}}$ and $z^{\mathrm{res}}$. The theory predicts that failed rare-composition examples should often show a large top-subspace common-over-target margin, $z_c^{\mathrm{top}}-z_y^{\mathrm{top}}$, relative to the residual target-over-common margin.

The fifth diagnostic is attention discriminativity. For a correct key and a distractor key, compare $C_{\mathrm{score}}(k)$ and $C_{\mathrm{disc}}(k)$. The attention-side theory is supported if the top band dominates score magnitude but contributes less to correct-versus-distractor discrimination. It is weakened if the top band is both large and discriminative.

The sixth diagnostic is update redirection. Measure $\alpha_t^{\mathrm{upd}}$ before and after update-space suppression. The optimizer theory is supported if suppression reduces common-subspace update concentration for active long-tail examples while preserving common-feature accuracy.

These diagnostics also define falsification criteria. If common subspaces do not stabilize, the frozen-subspace assumption fails. If high-gain modes do not attract later features despite error alignment, the descent-efficiency mechanism is incomplete. If attention discrimination comes primarily from the same top band that dominates score magnitude, then common-mode bias is not the right explanation for that attention head. If update-space suppression reduces neither update concentration nor long-tail recovery, then the proposed optimizer does not address the actual bottleneck.

## 15. Experimental Program

The first experiment should track singular subspace drift, singular energy, feature alignment, and gain-weighted feature effect over training. This directly tests the two-phase causal arrow. The expected pattern is that common-feature singular directions stabilize before their gains stop growing. If confidence capping works as intended, it should reduce late gain growth more than it reduces direction alignment.

The second experiment should use nested-prefix data with controlled feature frequency. The goal is to test whether a common prefix feature creates a high-gain backbone and whether later prefixes reuse that backbone. The relevant measurements are top-$k$ feature mass, effective rank, and update concentration for common and tail examples.

The third experiment should use matched phrase-change pairs in natural language. The readout CDF should be measured as $C_{\mathrm{hidden}}(k)$ and $C_{\mathrm{logit}}(k)$. The current result already suggests that the top $64$ to $128$ directions form a readout-active band. The next step is to measure this curve across checkpoints and across model sizes.

The fourth experiment should test attention-side discriminativity. Construct examples with a correct dependency and semantically plausible distractors. For each attention head, decompose query-key scores into top-band and tail-band contributions. Then compare score mass with discrimination contrast. The key evidence would be a head or layer where top-band score mass is high but top-band discrimination is weak.

The fifth experiment should evaluate update-space interventions. Compare ordinary AdamW, confidence capping alone, projection alone, and confidence-capped common-subspace suppressed AdamW. The correct success criterion is not only lower validation loss. It is a geometric change: common features remain accurate, long-tail recovery improves, common-subspace update concentration decreases, and the readout or attention CDF becomes less dominated by common modes.

## 16. Claim Boundary

The theory proves local causal mechanisms, not a universal theorem about all transformer behavior. The two-phase proof is exact in a rank-one margin model. The descent-efficiency proof is exact under local linearization for a selected matrix block. The softmax suppression theorem is exact for logits once a positive common-over-target gap exists. The update-space suppression proof is exact for an orthogonal projector applied to the actual update direction.

The theory does not prove that all rare features live in residual directions. That is an empirical claim to be measured by feature spectral mass. The theory does not prove that every high singular value is harmful. High gain is useful when it aligns with discriminative structure. The theory does not prove that the strict top $1\%$ subspace dominates composition. The current evidence suggests the opposite: strict top $1\%$ is amplified but insufficient, while a broader top $64$ to $128$ spectral band is more explanatory.

The correct claim is therefore narrower and stronger. Nested next-token learning can create a shared high-gain spectral backbone. Later nested learning is locally attracted to this backbone because it gives larger first-order loss decrease when aligned with error. Recursive semantic composition inherits the backbone and can accumulate common-mode projections. Softmax readout and attention can then amplify common-mode advantages even when true discrimination depends on lower-gain long-tail components. This is a falsifiable causal mechanism, not a universal declaration that large singular values are bad.

## 17. Summary

The causal chain is the following. Nested next-token learning gives repeated softmax reinforcement to common predictive contexts. Repeated reinforcement first aligns singular directions with common features and then can continue to increase singular gain. Existing high-gain directions become descent-efficient for later nested features, so later learning is biased toward reusing and extending the common backbone. Because all atomic concepts are learned through the same human-language distribution, different concepts can share this low-rank anisotropic space even when their unique meanings differ. Recursive semantic composition accumulates shared common projections. Output and attention softmax then turn common-mode score advantages into exponential selection advantages. The failure mode appears when amplified commonality dominates the score while the true relation is carried by lower-gain long-tail features.

The empirical readout CDF result supports the spectral-band version of this story. Strict top $1\%$ directions are strongly amplified but do not explain most logit change. The broader top $64$ to $128$ band is much more explanatory. The next decisive experiment is not only to measure hidden energy, but to measure discriminativity: whether the high-gain band contributes the correct contrast or merely contributes common-mode score magnitude.


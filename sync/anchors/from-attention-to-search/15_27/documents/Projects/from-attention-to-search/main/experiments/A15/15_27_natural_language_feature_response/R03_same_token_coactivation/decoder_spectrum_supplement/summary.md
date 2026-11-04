派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R03_same_token_coactivation/decoder_spectrum_supplement/summary.md`。
[精确原始文件](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R03_same_token_coactivation/decoder_spectrum_supplement/summary.md)；研究修改仍回到原件。

---

# Fixed coactivation groups: decoder directions and representation spectrum

**What are we asking?** Do members of existing coactivation groups write in similar directions, where do those directions fall in the representation-variance spectrum, and do the bands separate independent semantic labels?

**What was already known?**

- A clustered point is a fixed feature. C03 was derived from reference coactivation, not decoder geometry or the example sentence. Raw R, corrected C and old response groups G02/G04 are distinct.
- In the executed crane example, changing bird to machine decreases C03 member f12277 from .01909 to .01140 while increasing f5409 from .03463 to .04098. Group membership does not imply the same edit response. [Old explanation first](../../../../../../../../../UNAVAILABLE.md).
- Old near/far responses retain order, edit-extent and sparse-member limits. They do not establish group semantics or expert function. This supplement made no model forward, model/dictionary update or new clustering.

**What changed after measurement?**

- Coactivation groups cannot be treated as established direction-similarity groups. C03 mean decoder cosine is .00176 versus matched-null median .00049; BH across three groups gives q=.126. Same-group f12277/f5409 cosine is .0262, while cross-group f12277/f1478 is .0561. [Figure1](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R03_same_token_coactivation/decoder_spectrum_supplement/figures/figure1_fixed_groups_decoder_cosine.png).
- Spectral location depends on the measured object. The equal-size 128-dimensional head carries 63.5% of reference variance, 18.9% of C03 mean unit-direction mass, and 33.6% after activation-energy weighting. None measures semantic content. Frequency is separately annotated, not the spectral ordering. [Figure2](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R03_same_token_coactivation/decoder_spectrum_supplement/figures/figure2_decoder_spectral_locations.png) · [same near/far cases](../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R03_same_token_coactivation/decoder_spectrum_supplement/figures/figure3_same_panel_spectral_edits.png).

**What remains unknown?** Which bands contain held-out semantic discrimination: no qualified independent-label/matching-hidden pair was found. Classifier and random-subspace classification controls are NOT RUN; the cumulative forward budget remains1500/1500. Historical raw-cache Base hashes were not independently recorded, so spectral results retain a source-chain boundary. [Appendix](../../../../../../../../../UNAVAILABLE.md).

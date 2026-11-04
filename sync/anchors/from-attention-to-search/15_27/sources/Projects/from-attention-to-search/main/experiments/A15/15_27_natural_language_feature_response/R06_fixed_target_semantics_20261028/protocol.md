# R06 Protocol: fixed-target semantic response

Status: APPROVED_FOR_BOUNDED_NATIVE_FORWARD_AND_OFFLINE_ANALYSIS under the latest explicit user instruction. Exact implementation choices below are preregistered before any new activation, not attributed to an earlier advisor definition. Mechanism acceptance and closure remain Unknown.

Purpose: first test reproducible sense responses at fixed target tokens beyond irrelevant edits and opposite-sense lexical lures. Only near-qualified objects enter the conditional paired far check. Old R05 results are not reclassified.

Four sense contrasts,16 wording families each,8 discovery/8 heldout; six near versions=384 prefixes. The unit is a wording family,not a token/version or384 concepts. All240tokens,target239,d16;128possible far X/Y/XU/YU prefixes d144 frozen in advance. No repeated filler sentence within a prefix; same filler content in each near/far pair,128-token block moved. Labels are authored/AI-reviewed,not independently human adjudicated. Full texts/tokens/spans/edit sizes/split and rationale:data/.

Native E16 FP32 ReLU Top32 at block27 MLP input and native joint14 A22 BF16 fixed TRAIN normalization/gate .051281172782182693. Shared Base forward; no modified encoder,Attention or layer analysis. A22 target contribution is shared z times native last-layer decoder norm,not local activation or importance. Frozen loaders and full exact operational config are copied below.

D=direction*(cX-cY)/scale; U=mean absolute X-XU,Y-YU changes/scale; E=D-U; L=direction*(cLX-cLY)/scale. Direction=sign discovery mean X-Y; scale=discovery48target contribution RMS. Select per concept/dictionary up to8 by mean family E,then median D/support/ID,with>=4active discovery families,>=4positive D families,and mean D/E>.10; no refill,at most32new/dictionary. Prespecified old CC447plant(+),SAE8194organ(-) remain separately labelled; identical coordinate/concept/direction deduplicates tests,opposite orientations remain distinct corrected objects.

8heldout families;10000family bootstrap percentile95%CI;exact256sign flips about .10,one-sided,symmetry assumption. Single pooled BH over both dictionaries,all concepts/new-old objects,four D/E/L/-L endpoints. Endpoint requires eligible scale,>=4activefamilies,>=6/8positive,mean/CI lower>.10,q<.05. Semantic response requires D/E/L; reverse-lure sensitivity requires D/E/-L. D/E alone leaves lure explanation unresolved. Minimum exact p1/256 limits power; no threshold changes.

Near-qualified concepts alone run their32frozen far prefixes. Fixed objects/direction/scale;paired far D/E and near-minus-far E,bootstrap/signflips,BH over3endpoints/all qualified objects. Every far inference is conditional/exploratory after near-heldout selection,not independent distance confirmation. No qualified objects means NOT_APPLICABLE,not evidence of no far representation.

Stages: old960-cache/45object audit;model-independent data freeze;5planned numerical checks(2oldcache,replay/newbaseline,prefix);192near discovery;candidate/direction/scale freeze;192near heldout;eligiblefar<=128;statistics/three figures/accessibly explained report;stop. Checks<=16,total<=528,failedattemptscharged. All parameters frozen;no optimizer/new resources/tasks/TEST/deletion/intervention. Implementation engineering repairs logged without scientific changes. X/Y and irrelevant edit size/filler compensation,lure negation and order remain confounds. Generic concept identity,model understanding,functionality and distance causality are unclaimed.

Three preflight audits cover identification,data/statistics and implementation/numerics. Explicit user authorization supersedes routine repeated approvals. Complete numerical contract:

```json
{
  "round": "R06_fixed_target_semantics_20261028",
  "seed": 20261028,
  "status": "APPROVED_FOR_BOUNDED_NATIVE_FORWARD_AND_OFFLINE_ANALYSIS",
  "authorization": "Latest researcher request explicitly authorizes near verification and conditional far branch; exact operational choices below preregistered before any new activation, no further stage approval required.",
  "budgets": {
    "near_max": 384,
    "far_max": 128,
    "checks_max": 16,
    "total_max": 528
  },
  "data": {
    "concepts": [
      "plant",
      "bank",
      "organ",
      "bass"
    ],
    "families_each": 16,
    "discovery_each": 8,
    "heldout_each": 8,
    "near_versions": [
      "X",
      "Y",
      "XU",
      "YU",
      "LX",
      "LY"
    ],
    "far_versions": [
      "X",
      "Y",
      "XU",
      "YU"
    ],
    "target_pos": 239,
    "total_tokens": 240,
    "near_distance": 16,
    "far_distance": 144,
    "split": "seeded near-duplicate fourgram components,8/8 per concept; all family versions same split; disjoint lure template identities across split",
    "fillers": "unique sentences per prefix; exact same filler content in paired near/far,128-token block moved across clue; possible order confound",
    "labels": "authored intended senses and explicitly irrelevant lexical labels; AI semantic review not independent human labels; not original natural corpus"
  },
  "objects": {
    "model": "Qwen3-0.6B-Base BF16 frozen native SDPA",
    "SAE": "E16 block27 post-attention-layernorm MLP input,FP32 native ReLU Top32,F30000",
    "CC": "A22 joint14 residual-post blocks1,3,...27,BF16 GEMM,saved TRAIN normalization and gate .051281172782182693,F16384; fixed1024 encoder positions",
    "readout": "z and native target contribution z*decoder_norm; CC uses shared z times last-layer TRAIN_RMS27*parameter_decoder_norm27,not single-layer activation",
    "same_forward": true
  },
  "selection": {
    "max_new_per_concept_per_dictionary": 8,
    "max_new_per_dictionary": 32,
    "support_min": 4,
    "positive_D_families_min": 4,
    "discovery_D_mean_min": 0.1,
    "discovery_E_mean_min": 0.1,
    "rank": "mean E descending,median D descending,active support descending,feature ID ascending; no refill",
    "direction": "sign(mean discovery(cX-cY)),frozen separately per concept/feature",
    "scale": "target native contribution RMS over discovery8families*6versions,including zeros; <=1e-8 unestimable,not confirmed",
    "prespecified_old": [
      {
        "dictionary": "CC",
        "concept": "plant",
        "feature": 447,
        "direction": 1
      },
      {
        "dictionary": "SAE",
        "concept": "organ",
        "feature": 8194,
        "direction": -1
      }
    ],
    "old_duplicates": "same concept/feature/direction tested once with both-role label; opposite direction is a separate predeclared object,also corrected"
  },
  "statistics": {
    "independence_unit": "wording family within fixed concept;8 heldout families,not tokens/versions or384 independent concepts",
    "D": "direction*(cX-cY)/scale",
    "U": "(abs(cX-cXU)+abs(cY-cYU))/(2*scale)",
    "E": "D-U",
    "L": "direction*(cLX-cLY)/scale",
    "lexical_reverse": "-L",
    "bootstrap": 10000,
    "CI": "percentile95%,resample8wholefamilies",
    "test": "exact256signflips of family(value-.10),one-sided; requires symmetry about tested boundary,not randomized causal assignment",
    "minimum_effect": 0.1,
    "multiplicity": "single pooled BH across both dictionaries,all concept-feature-direction objects including old fixed objects,four endpoints D/E/L/-L; q<.05,no posthoc subgroup",
    "support_heldout_min": 4,
    "positive_families_min": 6,
    "endpoint_pass": "eligible scale,>=4activefamilies,>=6/8positive families,mean>.10,CI lower>.10,q<.05",
    "semantic_pass": "D,E,L all pass",
    "lexical_sensitive_pass": "D,E,-L all pass; finite foil sensitivity,not general concept identity",
    "partial": "D,E pass,L/-L unresolved:basic contextual discrimination only",
    "other": "measurement support insufficient; no proof that dictionary lacks concept",
    "far": "Only semantic-pass concepts run all8heldoutfamilies*4versions. Same fixed objects,direction,scale. Paired near-far E and far D/E;10000bootstrap/exact256signflips,BH across3endpoints/all eligible objects. All conditional/exploratory after selection,not independent distance confirmation."
  },
  "checks": {
    "prefix_cap": 16,
    "planned": 5,
    "procedure": "2oldR05discoverydocs replay;1newdiscoverybaseline+1replay+1visibleprefix; no new heldout activation in checks",
    "relative_z": 0.02,
    "jaccard": 0.95,
    "prefix_h_relative": 0.01,
    "SAE_reconstruction": [
      0.15,
      0.3
    ],
    "CC14_reconstruction": [
      0.3,
      0.5
    ],
    "forbidden": "No Attention extraction,layer analysis,training,intervention,resources,tasks,sealedTEST,old-file deletion"
  },
  "input_ids": [
    "model_qwen3_0p6b_base",
    "tokenizer_qwen3_0p6b_base",
    "sae_qwen3_0p6b_e16_layer27_final_1b",
    "crosscoder_qwen3_14layer_16384_bf16_a18_formal_14layer_batchtopk_a22_999997440_20261013",
    "data_a15_27_r05_five_distance_attention_20261028",
    "analysis_a15_27_r05_distance_attention_20261028"
  ]
}
```

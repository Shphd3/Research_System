# Native-positive token inventory for every strict16member

[中文](README_cn.md) · [Previous pooled figures](../pooled_simple_20261030/README.md)

## Belief update

**The16members have heterogeneous surface responses: some occur largely on shared tokens/punctuation, others more on cell-related surfaces or subwords. Panel-single-domain use does not establish exclusive domain-word recognition. Other/insufficient coverage does not mean absent domain meaning.**

These are verified descriptive measurements. Mechanism/identity/causal interpretation remains Unknown.

## Units and definitions

Unchanged native A22shared-z/gate and16all-cached-strict members(7math/9biology).Observe oldheldout40documents,20/domain,160positions/doc(indices32..191),6,400positions.Nativez>0only;no p90or intensity weighting.Positive counts are positions;document coverage deduplicates original documents.The total4,675member-position events cover2,898distinct input positions,not4,675independent samples.

Per-member position fractions divide by that member's positive positions.Type fractions below divide by its distinct exact IDs.Categories preserve the previous all120input-document rule:shared≥5documents/domain;panel-single-domain≥5in one and0in the other;remainingother/insufficient.These are coverage categories,not semantic labels.Selection and category definition inspect all cached documents;oldheldout is exploratory rather than independent generalization.

## Table1: every member's support and position composition

| Feature | Bias | Positive positions | Active docs/20 | Token types | Shared positions | Single-domain positions | Other positions |
|---|---|---:|---:|---:|---:|---:|---:|
| 16195 | math | 902 | 17 | 402 | 46.8% | 5.2% | 48.0% |
| 15426 | math | 381 | 14 | 182 | 38.6% | 7.9% | 53.5% |
| 8693 | math | 209 | 14 | 128 | 47.4% | 5.3% | 47.4% |
| 12030 | math | 1105 | 18 | 470 | 43.2% | 7.4% | 49.4% |
| 5234 | math | 132 | 16 | 71 | 23.5% | 27.3% | 49.2% |
| 12960 | math | 412 | 9 | 218 | 40.3% | 10.0% | 49.8% |
| 9638 | math | 275 | 12 | 161 | 45.8% | 4.7% | 49.5% |
| 2635 | biology | 72 | 14 | 20 | 90.3% | 0.0% | 9.7% |
| 6270 | biology | 287 | 15 | 186 | 46.0% | 1.4% | 52.6% |
| 13691 | biology | 129 | 16 | 100 | 1.6% | 2.3% | 96.1% |
| 10395 | biology | 50 | 12 | 34 | 6.0% | 0.0% | 94.0% |
| 7238 | biology | 55 | 10 | 39 | 3.6% | 0.0% | 96.4% |
| 12630 | biology | 407 | 10 | 207 | 47.7% | 5.7% | 46.7% |
| 11516 | biology | 182 | 15 | 124 | 44.5% | 1.1% | 54.4% |
| 15401 | biology | 45 | 9 | 14 | 4.4% | 55.6% | 40.0% |
| 11960 | biology | 32 | 4 | 29 | 0.0% | 3.1% | 96.9% |

Rounding can produce0.1ppdiscrepancies.All16remain;11960has only4active heldout documents/32positions.

## Table2: first three tokens by native positive count

Display omits leading spaces but preserves IDs/case/newline notation.Raw strings remain inCSV.Rank by descending count,ascendingIDfor ties.No example substitutions.Top3need not cover a majority;Top3/Top10coverage is saved.

| Feature | Rank1: token [ID], positions/docs | Rank2 | Rank3 |
|---|---|---|---|
| Math · f16195 | `the` [279]: 44positions / 14docs | `,` [11]: 33positions / 12docs | `is` [374]: 33positions / 11docs |
| Math · f15426 | `the` [279]: 22positions / 8docs | `in` [304]: 19positions / 10docs | `,` [11]: 14positions / 4docs |
| Math · f8693 | `the` [279]: 23positions / 8docs | `a` [264]: 8positions / 4docs | `,` [11]: 6positions / 3docs |
| Math · f12030 | `,` [11]: 54positions / 15docs | `the` [279]: 40positions / 12docs | `.` [13]: 23positions / 10docs |
| Math · f5234 | `$` [400]: 16positions / 5docs | `,` [11]: 13positions / 9docs | `_{` [15159]: 7positions / 3docs |
| Math · f12960 | `,` [11]: 14positions / 5docs | `the` [279]: 13positions / 4docs | `$` [400]: 12positions / 3docs |
| Math · f9638 | `the` [279]: 20positions / 8docs | `,` [11]: 11positions / 6docs | `of` [315]: 10positions / 6docs |
| Biology · f2635 | `.` [13]: 28positions / 8docs | `.\n\n` [382]: 11positions / 7docs | `]` [60]: 7positions / 5docs |
| Biology · f6270 | `,` [11]: 23positions / 10docs | `.` [13]: 7positions / 2docs | `1` [16]: 7positions / 4docs |
| Biology · f13691 | `il` [321]: 5positions / 3docs | `gl` [2770]: 4positions / 2docs | `pred` [4162]: 4positions / 1docs |
| Biology · f10395 | `tub` [14938]: 4positions / 1docs | `renal` [62815]: 4positions / 1docs | `system` [1849]: 3positions / 1docs |
| Biology · f7238 | `ial` [530]: 4positions / 1docs | `illin` [60497]: 4positions / 1docs | `itin` [84886]: 4positions / 1docs |
| Biology · f12630 | `the` [279]: 20positions / 4docs | `,` [11]: 12positions / 4docs | `to` [311]: 12positions / 4docs |
| Biology · f11516 | `of` [315]: 10positions / 6docs | `the` [279]: 9positions / 4docs | `to` [311]: 8positions / 4docs |
| Biology · f15401 | `cell` [2779]: 14positions / 6docs | `cells` [7761]: 10positions / 4docs | `ules` [2425]: 4positions / 1docs |
| Biology · f11960 | `bamboo` [58882]: 3positions / 1docs | `plants` [10779]: 2positions / 2docs | `up` [705]: 1positions / 1docs |

Math top ranks often include shared words and punctuation;5234also hasmath markup.Biology2635has90.3%shared positions and punctuation at top,but this does not establish a pure punctuation feature.15401hascell14times/6docsandcells10times/4docs,together24/45=53.3%of positive positions.Subwordsil/gl/predandial/illin/itinare not complete words;posthoc spelling aids include trilobite/glial/predationandglial/fibrillin/ubiquitin,never causal explanations of unseen suffixes.EvenID279can prefix theorems rather than a full article.All three leading10395tokens occur in one document each;7238also has one-document leading-token coverage.11960is especially sparse.Recognizable domain words such asrenalcan remainotherdue to inadequate document support.Highotherdoes not mean generic semantics or no domain information.

Raw counts alone do not establish token preference.Full tables include same-domain available occurrences/documents and conditional activation fractions for audit;these are observational quantities.

## Table3: distinct-token-type composition

| Feature | Shared types / fraction | Single-domain types / fraction | Other types / fraction |
|---|---:|---:|---:|
| Math · f16195 | 79／19.7% | 25／6.2% | 298／74.1% |
| Math · f15426 | 42／23.1% | 14／7.7% | 126／69.2% |
| Math · f8693 | 36／28.1% | 8／6.2% | 84／65.6% |
| Math · f12030 | 79／16.8% | 26／5.5% | 365／77.7% |
| Math · f5234 | 9／12.7% | 10／14.1% | 52／73.2% |
| Math · f12960 | 56／25.7% | 17／7.8% | 145／66.5% |
| Math · f9638 | 45／28.0% | 8／5.0% | 108／67.1% |
| Biology · f2635 | 15／75.0% | 0／0.0% | 5／25.0% |
| Biology · f6270 | 54／29.0% | 3／1.6% | 129／69.4% |
| Biology · f13691 | 2／2.0% | 2／2.0% | 96／96.0% |
| Biology · f10395 | 2／5.9% | 0／0.0% | 32／94.1% |
| Biology · f7238 | 2／5.1% | 0／0.0% | 37／94.9% |
| Biology · f12630 | 49／23.7% | 8／3.9% | 150／72.5% |
| Biology · f11516 | 30／24.2% | 2／1.6% | 92／74.2% |
| Biology · f15401 | 1／7.1% | 3／21.4% | 10／71.4% |
| Biology · f11960 | 0／0.0% | 1／3.4% | 28／96.6% |

## Data and reproduction

[Member summary](member_summary.csv) · [Type fractions](member_type_composition.csv) · [Top10per member](member_token_top10.csv) · [All tokens per member](member_token_all.csv) · [Definitions](config.json) · [Audit](audit.json).

Run R10scripts/strict16_per_member_tokens.pythenpackage_strict16_token_tables.pywith local spectral-hierPython.Counts/document coverage/category fractions independently reproduce the existing native-positive summaries;4,675events/1,182unionIDsand all16members retained.No new model forward,training,PCAor selection.

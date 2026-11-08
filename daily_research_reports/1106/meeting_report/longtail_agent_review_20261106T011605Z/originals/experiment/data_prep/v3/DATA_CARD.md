# Frozen local-source data card (v3)

This cohort supports a bounded test of learning **Wikipedia-person birth-year facts under controlled supervision exposure**. It does not estimate Qwen pretraining frequency, broad factual competence, natural paraphrase generalization or a mechanism.

## Entry points and counts

| File | Independent units | Role |
|---|---:|---|
| `data.jsonl` | 24,096 facts | All fixed selected pools; loaders must select the intended split |
| `dev.jsonl` | 1,024 facts | Method/model selection, never final confirmation |
| `sentinel.jsonl` | 1,024 facts | Disjoint zero-supervision knowledge control |
| `reference.jsonl` | 2,048 facts | Disjoint biographical source families |
| `source_independent_reference.jsonl` | 2,048 source documents | Biographical spectral reference; multiple token positions may be sampled |
| `confirm_a.jsonl`, `confirm_b.jsonl` | 10,000 each | Source/entity-family isolated phase A/B candidate pools |
| `confirm_ab_2048.jsonl` | A1,024+B1,024 | Frozen first nested training-candidate scale |
| `confirm_ab_8192.jsonl` | A4,096+B4,096 | Frozen second nested scale |
| `confirm_ab_20000.jsonl` | A10,000+B10,000 | Frozen maximum scale |
| `all_eligible_facts.jsonl` | 47,514 facts | All eligible candidates; unused families retain fixed split |
| `candidate_pool.jsonl` | 59,735 unique title/first-sentence variants | Full initial explicit-born candidate ledger, including rejected variants and reasons |
| `quarantined_families.json` | 3,904 components | Entire conflicting/uncertain/old-DEV families excluded |
| `natural_v3/general_lm.jsonl` | 128 paragraphs /128 article families | Independent, untrained WikiText NLL control;15,560 Base tokens |
| `natural_v3/nonbiographical_spectrum_reference.jsonl` | 432 paragraphs /94 other article families | Strict automatic non-biography candidate gate;50,994 Base tokens |

A/B are **facts that may be trained**, evaluated using held-out question templates about the same fact. They are not never-seen facts that the student is expected to infer. DEV chooses methods; confirmation A/B must stay sealed until exact screening and training rules are fixed. Teacher/student behavior screening is downstream and was not performed here. Initial `teacher_mode=candidate`.

## Real text provenance

Sources are existing local JSONL Hotpot context caches:

- `/data/share/smartrag/datasets_cache/hotpot_qa_train.jsonl`,90,447 records,563,983,862 bytes,SHA256 `1c7d26149efa0ea44f8f76e01d7bdf76cf9fdfa47c9ebd2864a2e2cd028c074e`.
- `/data/share/smartrag/datasets_cache/hotpot_qa_validation.jsonl`,7,405 records,46,608,428 bytes,SHA256 `c301b4d689fabff61df514e4511a4688e8e10a16ed2cee28484bc85ed8dc72e4`.

Native fields: `id,question,answer,type,level,supporting_facts{title,sent_id},context{title,sentences}`. The native QAs usually require multi-hop reasoning. This dataset derives atomic birth-year queries from supplied real context sentences instead of treating those native QAs as single facts. Exact upstream cache revision is **Unknown**. Wikipedia provenance is inherited from Hotpot metadata; no claim of external Wikipedia byte identity or independent civil-record verification.

All selected rows preserve the complete supplied first sentence, title, original record ID, source JSONL line/byte offset/byte length, context-title index, sentence index, exact answer character span and source relation span. `validation_receipt.json` verifies **all24,096 selected rows by original byte readback**, covering17,577 unique original records. The decoded context and answer spans match exactly.

`/data/share/wikitext-2-v1/wikitext-2-v1.json` is existing preprocessed WikiText JSONL (11,300,311bytes),SHA256 `cbfbce6a8c4c30bf09661c7f7fd60cf2d31fa1a8940f036c3a78bcb691324d1b`. Each natural prefix keeps source offsets and exact character bounds. All560 prefixes were read back from source. Token lengths were actually measured using official0.6B Base tokenizer JSON,SHA256 `c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539`; every prefix has32–256 tokens. Runtime was CPU-only `/root/anaconda3/envs/spectral-hier/bin/python`,tokenizers0.22.2.

## Frozen extraction and task forms

`extraction_frozen.json` and `build_birth_year.py` own the precise rules. Require an explicit source-leading subject and `(born ... YEAR...)`, exactly one precise1600–2019 year inside that expression, sufficient name/title alignment, no uncertain or nested damaged date, no malformed/predicative/duo subject, no year in any question. Do not infer birth from a lifetime range. Title qualifiers disambiguate names; strip born/year parts before including qualifiers in questions.

Example source: `Bill Schultz (born June 11, 1960) is an animation producer.` Source title is `Bill Schultz (producer)` (actual spacing/text is in JSONL). Train form: `In what year was Bill Schultz (producer) born?`; held-out forms: `What is Bill Schultz (producer)'s birth year?`, `Give the year of birth of Bill Schultz (producer).`; answer `1960`. All three forms are **automatically fixed relation templates**,not independently authored natural paraphrases. They count as **one fact**.

Normalized title bases and explicit leading subject aliases form conservative connected components. A component with conflicting years, uncertain date or old inspected DEV source is quarantined. This can merge different homonymous people and reject correct data; it does not establish that all conflicting years are false. No external alias linker proves semantic entity completeness. The old71 inspected source families named in `already_inspected_source_families.json` are excluded.

Stable family hash assigns5%DEV,5%sentinel,5%reference,42.5%A,42.5%B; independent hash order supplies nested prefixes. All selected fact/source/entity families and34,287 explicit normalized alias keys are unique across pools. Full eligible counts are DEV2,266/sentinel2,346/reference2,350/A20,341/B20,211. Do not resplit question forms, replacement texts or teacher outputs independently of their parent family.

## Frequency and quality coverage

Natural fact frequency and Qwen pretraining exposure are **Unknown**. Repeated appearance as a Hotpot context is a source-cache sampling artifact and is not fact frequency. Planned1/8 exposures mean controlled supervision counts only.

Every selected fact passes automatic structure/date/name/span rules and byte readback. An agent deterministically sampled112 selected facts by independent hash and inspected all112 source/answer/question identities (`agent_review_receipt.json`);112 passed after source-only repairs. **Human reviewed0; remaining23,984 selected facts have automatic checks only.** This does not certify external historical truth or full homonym resolution.

Precision-biased exclusions include valid surnames Son/Husband and the conservative `c.` uncertainty pattern matching Washington D.C.; lifetime-date expressions and some valid aliases are rejected. These false negatives are retained in the frozen ledger rather than silently repaired to favor outcomes.

WikiText families are disjoint between the128 LM articles and94 supplementary reference articles; oldDEV titles and all indexed birth candidates' title/name strings are excluded. First-two-paragraph born/died/person-pronoun gates, unknown/formula-heading gates, no-born/no-unknown-text paragraph gates and explicit candidate-name mention filtering reduce biography overlap. They are **automatic candidate gates**, not complete semantic biography or alias annotation. A total432 strict supplementary reference paragraphs remains; the1024 target was not reached, and rules were not relaxed. Preprocessed `@-@` artifacts remain, and prefixes can end mid-sentence. This NLL control is small and selected; it is not a broad benchmark.

## Version and audit boundaries

v1 found a decade1980s→1980 error and a novel lead mistaken for a person. v2 corrected them. Agent inspection of v2 found damaged nested birth parentheses and missing title disambiguation. v3 corrected them **before formal model screening**, preserving v1/v2. Natural text v1 missed several biographies; natural_v2 strengthened the gate; natural_v3 additionally rejects formula fragments misread as article titles. All earlier versions remain as error evidence. **Use only factual v3 and natural_v3 for formal work.** No student/teacher result affected extraction, repair or splitting.

No model was loaded, no training performed, no network download or remote task started by data preparation. Native Hotpot multi-hop QA and SciQ remain unused alternatives,not confirmation results. Teacher correctness checks, behavior-based cohorts, exposure schedules, method selection and scientific interpretation belong to the experiment owner.

from pathlib import Path
import json,hashlib
import pandas as pd,numpy as np
P=Path(__file__).resolve().parents[1];E=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response')/P.name
r=[json.loads(l) for l in (E/'data/positions.jsonl').read_text().splitlines()];df=pd.read_csv(E/'analysis/position_metrics.csv');docs=pd.read_csv(E/'analysis/document_metrics.csv');s=pd.read_csv(E/'analysis/summary_metrics.csv');smoke=json.load(open(E/'audit/03_implementation_numerics.json'));receipt=json.load(open(E/'terminal_receipt.json'))
assert smoke['pass'] and receipt['training_updates']==0 and smoke['trainable_parameters']==0
checks={}
checks['all737positions_21conditions']=len(df)==737*21 and not df.duplicated(['index','condition']).any()
checks['primary37_the279']=sum(x['panel']=='the' for x in r)==37 and all(x['input_id']==279 for x in r if x['panel']=='the')
checks['supplement700_175docs']=sum(x['panel']=='natural' for x in r)==700 and len({x['seq_id'] for x in r if x['panel']=='natural'})==175
checks['physical180docs']=len({x['seq_id'] for x in r})==180
identity=df[df.condition=='identity'].set_index('index');reco=df[df.condition=='k1024'].set_index('index')
checks['identity_KL_zero']=float(abs(identity.KL_full).max())==0
checks['identity_top1_top10_complete']=bool((identity.top1_agreement==1).all() and (identity.top10_recovery==1).all())
checks['fullPC_NLL_max_error']=float(abs(identity.NLL-reco.NLL).max())<=1e-6
checks['NLL_probability_consistency']=float(abs(df.NLL+np.log(df.target_probability)).max())<2e-6
checks['KL_nonnegative_to_FP32_tolerance']=float(df.KL_full.min())>=-2e-6
checks['all_metrics_finite']=bool(np.isfinite(df.select_dtypes('number').to_numpy()).all())
checks['frequency_bins_sum_to_lexical_mass']=float(abs(df[['freq_top1pct','freq_next9pct','freq_next40pct','freq_last50pct']].sum(1)-df.lexical_mass).max())<2e-6
checks['entropy_nonnegative']=bool((df.entropy>=0).all())
checks['top10_within_bounds']=bool(df.top10_recovery.between(0,1).all())
checks['means_are_document_weighted']=all(np.isclose(x['mean'],docs[(docs.panel==x['panel'])&(docs.condition==x['condition'])][x['metric']].mean(),rtol=1e-10,atol=1e-10) for x in s.to_dict('records'))
vp=json.load(open(E/'analysis/unselected_text_validation.json'))['cases'];fixed=set(json.load(open(E/'manifest.json'))['fixed_examples']);checks['validation12_disjoint_fixed7']=len(vp)==12 and not {v['position_uid'].split(':')[1] for v in vp}&fixed
badtop=[]
for line in (E/'analysis/raw_outputs.jsonl').read_text().splitlines():
 x=json.loads(line);top=x['top20'];pp=[t['probability'] for t in top]
 if len(top)!=20 or len({t['id'] for t in top})!=20 or any(a<b for a,b in zip(pp[:-1],pp[1:])):badtop.append(x['position_uid'])
checks['all_top20_sorted_unique']=not badtop
report={'pass':all(checks.values()),'checks':checks,'fullPC_NLL_max_abs':float(abs(identity.NLL-reco.NLL).max()),'NLL_probability_max_abs':float(abs(df.NLL+np.log(df.target_probability)).max()),'physical_documents':180,'primary_documents':37,'supplemental_documents':175,'shared_documents':32,'outputs':len(df),'smoke':smoke,'terminal_receipt':receipt}
(E/'audit/final_validation.json').write_text(json.dumps(report,indent=2)+'\n');(P/'provenance/final_validation.json').write_text(json.dumps(report,indent=2)+'\n');assert report['pass'],checks
print('ALL_PASS',checks)

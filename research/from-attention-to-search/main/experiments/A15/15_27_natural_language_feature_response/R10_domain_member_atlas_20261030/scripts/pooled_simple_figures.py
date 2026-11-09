"""Pooled, low-text meeting figures; exact cached-only singleton-domain descriptions."""
from pathlib import Path
import csv,json,hashlib,shutil,datetime,collections
import numpy as np
from scipy import sparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import PercentFormatter
S=Path('/data/250010109/MoE_Router/experiments/20261026_natural_language_feature_response/R10_domain_member_atlas_20261030');A=S/'presentation_variants/near_single_domain_20261030';O=S/'presentation_variants/pooled_simple_20261030';O.mkdir(exist_ok=True)
W=Path(__file__).resolve().parents[1];D=W/'figure_variants/pooled_simple_20261030';D.mkdir(exist_ok=True)
def read(p):return list(csv.DictReader(p.open()))
def table(name,rr):
    rr=list(rr)
    with (O/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
def dump(name,x):(O/name).write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
docs=[json.loads(x) for x in (S.parent/'R04_domain_usage_20261027/data/documents.jsonl').read_text().splitlines()];frozen=json.loads((A/'freeze.json').read_text());members={int(r['feature_id']):r for r in read(A/'near95_members.csv')};pk=np.load(S/'analysis/position_keys.npz');di=pk['document_index'];tk=pk['token_id'];vocab=np.unique(tk);tc=np.searchsorted(vocab,tk);held=np.flatnonzero(np.array([docs[int(i)]['split']=='heldout' for i in di]));doccount=np.zeros((120,len(vocab)),int);np.add.at(doccount,(di,tc),1)
cc=np.load(S.parent/'R04_domain_usage_20261027/forward/documents_CC.npz');order={str(s):i for i,s in enumerate(cc['seq_id'])};counts=cc['counts'][[order[d['seq_id']] for d in docs]]
sets={k:frozen['sets'][k] for k in ['near95_math','near95_biology','strict_math','strict_biology']};ids=[]
for g in ['math','biology']:
    other=np.array([d['domain']!=g for d in docs]);keep=[i for i in sets['strict_'+g] if counts[other,i].sum()==0];sets['all_cached_strict_'+g]=keep;ids+=keep
cfg={'revision':'pooled-simple-v1','purpose':'User requested pooled math+biology, few bars and strict single-domain activation/token proportions.','parent_freeze_sha256':sha(A/'freeze.json'),'near55':'unchanged original near95 discovery set','strict29':'unchanged discovery-zero-opposite set','all_cached_strict16':'descriptive subset of strict29: no native z>0 in ANY opposite-domain analysis position across discovery+development+oldheldout; does not replace discovery-frozen lists','new_token_categories':'DESCRIPTIVE ALL120document coverage: shared>=5documents EACH domain; observed-single-domain>=5in one and0in other; remaining other/insufficient. NEW classification is not the earlier discovery-frozen token scheme. Neither is semantic exclusivity.','token_analysis_positions':'oldheldout40documents x160=6400; because selection/categories inspect all cached data this panel is descriptive, NOT heldout generalization','primary_high_response':'unchanged discovery-positive-p90 per member, strict >; composition gate remains >=5high events/2oldheldout docs','native_sensitivity':'z>0 on the SAME16members, no member replacement','feature_frequency':'original DCLM counts/65536; >=20hits; original lower-inclusive cuts .002593994140625/.0134429931640625','token_frequency':'original within-panel type-count quantiles1/2 over19200positions, ties kept: count1/count2/count>=3','pooling':'members pooled equally, no extra equal-domain weighting; unique-token-ID counts deduplicate across members; event shares first normalize within each member then average','new_model_forwards':0,'new_training':0,'source_data_already_explored':True,'scientific_acceptance':'Unknown'}
if (O/'config.json').exists():assert json.loads((O/'config.json').read_text())==cfg
else:dump('config.json',cfg)
dump('freeze.json',{'sets':sets,'config_sha256':sha(O/'config.json'),'selection_status':'descriptive all-cached zero-opposite audit; original lists retained'})
master=read(S/'tables/master_members.csv');rate={int(r['feature_id']):float(r['DCLM_feature_occurrence']) for r in master};freq={int(r['feature_id']):r['frequency_original'] for r in master};near=sets['near95_math']+sets['near95_biology'];strict29=sets['strict_math']+sets['strict_biology'];freqrows=[]
for name,subset in [('near55',near),('discovery_strict29',strict29),('all_cached_strict16',ids)]:
    valid=sum(freq[i]!='insufficient' for i in subset)
    for c in ['low','middle','high','insufficient']:
        n=sum(freq[i]==c for i in subset);freqrows.append(dict(cohort=name,bin=c,members=n,classified_members=valid,frozen_members=len(subset),fraction=n/valid if c!='insufficient' else ''))
table('pooled_feature_frequency.csv',freqrows)
memberrows=[]
for i in ids:
    r=dict(members[i]);g=r['domain_bias'];ix=np.array([d['domain']!=g for d in docs]);r['all_cached_opposite_positive_positions']=int(counts[ix,i].sum());r['all_cached_opposite_documents']=int((counts[ix,i]>0).sum());r['all_cached_preferred_positive_positions']=int(counts[~ix,i].sum());memberrows.append(r)
table('strict16_members.csv',memberrows)

# Two independent token attributes: corpus domain coverage and within-panel frequency.
pres={g:(doccount[np.array([d['domain']==g for d in docs])]>0).sum(0) for g in ['math','biology']};cl=np.where(np.minimum(pres['math'],pres['biology'])>=5,0,np.where((np.maximum(pres['math'],pres['biology'])>=5)&(np.minimum(pres['math'],pres['biology'])==0),1,2));typecounts=doccount.sum(0);fb=np.where(typecounts==1,0,np.where(typecounts==2,1,2));strings={int(r['token_id']):r['token_string'] for r in read(A/'input_token_categories.csv')};labels=['shared','observed_single_domain','other_or_insufficient'];flabels=['low_count1','middle_count2','high_count_ge3'];qual=np.array([members[i]['composition_supported']=='True' for i in ids]);Z=sparse.load_npz(S/'analysis/native_positions_csr.npz')[held][:,ids].toarray();tau=np.load(S/'analysis/token_thresholds.npz')['positive_z_p90'][ids];H=Z>tau;P=Z>0
categoryrows=[];frequencyrows=[];coverage=[];tokendetails=[];permember=[];summary={}
for mode,mask,sel in [('high_supported',H,np.flatnonzero(qual)),('high_all_with_events',H,np.flatnonzero(H.any(0))),('native_all',P,np.flatnonzero(P.any(0)))]:
    totals=mask[:,sel].sum(0);perposition=(mask[:,sel]/totals[None,:]).mean(1);assert np.isclose(perposition.sum(),1);active=mask[:,sel].any(1);types=np.unique(tc[held[active]]);classcounts=np.bincount(cl[types],minlength=3);q=np.bincount(cl[tc[held]],weights=perposition,minlength=3);fq=np.bincount(fb[tc[held]],weights=perposition,minlength=3);rawbg=np.bincount(cl[tc[held]],minlength=3)/len(held);dw=np.bincount(di[held],weights=perposition,minlength=120);bg=dw@(doccount/160);matchedbg=np.bincount(cl,weights=bg,minlength=3);freqbg=np.bincount(fb[tc[held]],minlength=3)/len(held)
    summary[mode]={'members':len(sel),'all_frozen_members':len(ids),'distinct_token_IDs':len(types),'type_counts':classcounts.tolist(),'type_shares':(classcounts/len(types)).tolist(),'member_equal_position_shares':q.tolist(),'token_frequency_position_shares':fq.tolist(),'all_position_category_background':rawbg.tolist(),'doc_matched_category_background':matchedbg.tolist(),'all_position_token_frequency_background':freqbg.tolist(),'member_position_events':int(mask[:,sel].sum()),'distinct_input_positions':int(active.sum())}
    coverage.append(dict(mode=mode,members=len(sel),frozen_members=len(ids),distinct_token_ids=len(types),distinct_positions=int(active.sum()),member_position_events=int(mask[:,sel].sum())))
    for k,c in enumerate(labels):categoryrows.append(dict(mode=mode,category=c,unique_token_IDs=int(classcounts[k]),all_unique_token_IDs=len(types),type_fraction=float(classcounts[k]/len(types)),member_equal_position_fraction=float(q[k]),all_available_position_background=float(rawbg[k]),document_exposure_matched_background=float(matchedbg[k]),included_members=len(sel),frozen_members=len(ids)))
    for k,c in enumerate(flabels):frequencyrows.append(dict(mode=mode,frequency=c,member_equal_position_fraction=float(fq[k]),all_available_position_background=float(freqbg[k]),input_type_count=int((fb==k).sum()),input_position_count=int(typecounts[fb==k].sum()),included_members=len(sel),frozen_members=len(ids)))
    for t in types:
        loc=tc[held]==t;tokendetails.append(dict(mode=mode,token_id=int(vocab[t]),token_string=strings[int(vocab[t])],category=labels[cl[t]],math_documents_all60=int(pres['math'][t]),biology_documents_all60=int(pres['biology'][t]),corpus_count=int(typecounts[t]),corpus_positions=19200,member_equal_position_share=float(perposition[loc].sum()),distinct_responding_documents=len(set(di[held[loc&active]].tolist())),responding_members=int(mask[loc][:,sel].any(0).sum())))
    for j in sel:
        rr=mask[:,j];w=rr/rr.sum();qq=np.bincount(cl[tc[held]],weights=w,minlength=3);ff=np.bincount(fb[tc[held]],weights=w,minlength=3);permember.append(dict(mode=mode,feature_id=ids[j],domain_bias=members[ids[j]]['domain_bias'],response_positions=int(rr.sum()),response_documents=len(set(di[held[rr]].tolist())),shared_share=float(qq[0]),single_domain_share=float(qq[1]),other_share=float(qq[2]),low_token_frequency_share=float(ff[0]),middle_token_frequency_share=float(ff[1]),high_token_frequency_share=float(ff[2])))
table('token_category_composition.csv',categoryrows);table('token_frequency_composition.csv',frequencyrows);table('token_ID_details.csv',tokendetails);table('per_member_token_composition.csv',permember);table('coverage.csv',coverage)
allrows=read(A/'per_member_tokens_all.csv');direct=[r for r in allrows if int(r['feature_id']) in ids and r['composition_supported']=='True'];totaldirect=collections.Counter()
for r in direct:totaldirect[int(r['feature_id'])]+=int(r['high_events'])
assert all(int(H[:,ids.index(i)].sum())==n for i,n in totaldirect.items())
assert len(ids)==16 and len(set(ids))==16 and qual.sum()==12
assert all(r['all_cached_opposite_positive_positions']==0 for r in memberrows)
assert sum(summary['high_supported']['type_counts'])==summary['high_supported']['distinct_token_IDs']
assert all(np.isclose(sum(summary[m]['member_equal_position_shares']),1) for m in summary)
dump('summary.json',{'near_members':len(near),'discovery_strict_members':len(strict29),'all_cached_strict_members':len(ids),'all_cached_strict_math':len(sets['all_cached_strict_math']),'all_cached_strict_biology':len(sets['all_cached_strict_biology']),'token':summary,'token_category_order':labels,'token_frequency_order':flabels,'new_model_forwards':0,'new_training':0,'classification_status':'descriptive all-cached; no claim of independent heldout confirmation or semantic exclusive words'})
dump('audit.json',{'status':'PASS','checks':['all16are members of original discovery strict29','all opposite positions zero across all120docs','native/high masks use same16members','high counts independently agree with original per-member token cache','type counts deduplicate exact IDs','category and frequency shares sum1','member weighting agrees with requested pooling','all missing support retained separately'],'new_model_forwards':0})

# Minimal figures: axes, three bars, and exact values only. Method stays outside images.
font=A/'fonts/NotoSansCJKsc-Regular.otf';font_manager.fontManager.addfont(str(font));plt.rcParams.update({'font.family':font_manager.FontProperties(fname=str(font)).get_name(),'font.size':16,'axes.titlesize':19,'axes.labelsize':16,'axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False,'pdf.fonttype':42})
palette=['#5a9fbd','#e6b85b','#9776ae'];cpalette=['#419eaf','#d78355','#b8bec6']
def bars(ax,values,ticks,ylabel,title,counts0=None,colors=None):
    ax.bar(range(3),values,width=.54,color=colors or palette);ax.set_xticks(range(3),ticks);ax.set_ylim(0,1.04);ax.yaxis.set_major_formatter(PercentFormatter(1,decimals=0));ax.set_yticks(np.arange(0,1.01,.2));ax.set_ylabel(ylabel);ax.set_title(title,pad=22);ax.grid(axis='y',alpha=.16);ax.set_axisbelow(True)
    for j,v in enumerate(values):ax.text(j,v+.025,f'{v:.1%}'+(f'\n{counts0[j]}个' if counts0 is not None else ''),ha='center',va='bottom',fontsize=17)
def save(fig,name):
    for ext in ['png','pdf']:fig.savefig(O/f'{name}.{ext}',dpi=190,facecolor='white',bbox_inches='tight')
    plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(12.8,5.5));fig.subplots_adjust(left=.09,right=.99,bottom=.18,top=.82,wspace=.32)
for ax,cohort,title in zip(axes,['near55','all_cached_strict16'],['近单域 feature（数学＋生物）','严格单域 feature（数学＋生物）']):
    rr=[r for r in freqrows if r['cohort']==cohort and r['bin']!='insufficient'];bars(ax,[r['fraction'] for r in rr],['低频','中频','高频'],'feature 数量占比',title,[r['members'] for r in rr])
save(fig,'figure1_pooled_feature_frequency')
for mode,name,word in [('native_all','figure2_strict_token_categories','激活'),('high_supported','appendix_high_token_categories','高响应')]:
    st=summary[mode];fig,axes=plt.subplots(1,2,figsize=(12.8,5.7));fig.subplots_adjust(left=.09,right=.99,bottom=.18,top=.82,wspace=.32)
    bars(axes[0],st['type_shares'],['两域共用','本批单域','其他'],'token 种类占比',word+'过哪些 token？',st['type_counts'],cpalette)
    bars(axes[1],st['member_equal_position_shares'],['两域共用','本批单域','其他'],word+'位置占比',word+'主要落在哪里？',colors=cpalette)
    save(fig,name)
for mode,name,title in [('native_all','figure3_activated_token_frequency','激活 token 的词频组成'),('high_supported','appendix_high_token_frequency','高响应 token 的词频组成')]:
    fig,ax=plt.subplots(figsize=(7.6,5.6));fig.subplots_adjust(left=.17,right=.98,bottom=.19,top=.83)
    bars(ax,summary[mode]['token_frequency_position_shares'],['低频\n1次','中频\n2次','高频\n≥3次'],'响应位置占比',title)
    save(fig,name)

# Track selected small evidence, never raw activations or font files.
selected=['config.json','freeze.json','pooled_feature_frequency.csv','strict16_members.csv','token_category_composition.csv','token_frequency_composition.csv','token_ID_details.csv','per_member_token_composition.csv','coverage.csv','summary.json','audit.json']+[p.name for p in O.glob('figure*.png')]+[p.name for p in O.glob('figure*.pdf')]+[p.name for p in O.glob('appendix*.png')]+[p.name for p in O.glob('appendix*.pdf')]
sourcepaths=[Path(__file__).resolve(),A/'freeze.json',A/'near95_members.csv',A/'per_member_tokens_all.csv',S/'analysis/position_keys.npz',S/'analysis/native_positions_csr.npz',S/'analysis/token_thresholds.npz',S.parent/'R04_domain_usage_20261027/data/documents.jsonl',S.parent/'R04_domain_usage_20261027/forward/documents_CC.npz']
dump('provenance.json',{'parent_asset_ids':['analysis_a15_27_r10_near_domain_token_context_20261030','analysis_a15_27_04_r10_domain_member_atlas_20261030','data_a15_27_r04_domain_native_dual_20261027'],'sources':[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)) for p in sourcepaths],'produced_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'new_model_forwards':0,'new_training':0})
selected+=['provenance.json']
for name in selected:shutil.copy2(O/name,D/name)
manifest={'parent_asset_id':'analysis_a15_27_r10_near_domain_token_context_20261030','scope':'derived pooled plots and cached descriptive zero-opposite subset; no new representation or model asset','files':[dict(path=n,origin=str(O/n),bytes=(D/n).stat().st_size,sha256=sha(D/n)) for n in selected],'new_model_forwards':0}
(D/'payload_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');dump('artifact_manifest.json',manifest)
print(json.dumps({'cohort':{'near':len(near),'strict_discovery':len(strict29),'strict_allcached':len(ids)},'high':summary['high_supported'],'native':summary['native_all'],'figures':str(D)},ensure_ascii=False,indent=2))

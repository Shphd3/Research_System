#!/usr/bin/env python3
"""Recover actual full-cache chain-hit prefixes; no feature/model intervention."""
from pathlib import Path
import importlib.util,json,hashlib,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import colors,font_manager
E=Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
O=E/'analysis/phi_relations_20261018';P=E/'analysis/feature_relation_phase1/20261013T173130Z'
def load(p):return json.loads(Path(p).read_text())
def csvout(p,rows):
    if not rows:return
    with Path(p).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main():
    spec=importlib.util.spec_from_file_location('old',E/'analysis_tools/group_understanding/extract_cases.py')
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    decoder=old.FrozenDecoder('/data/share/Qwen3-0.6B-Base/tokenizer.json')
    h=load(O/'full_chain_counts.json');abc=h['members'];group=next(x for x in load(E/'analysis/feature_frequency/20261015T143300Z/main/groups_D.json') if x['group_id']==14)
    fs=np.array(group['members']);lookup=np.full(16384,-1,np.int32);lookup[fs]=np.arange(len(fs))
    chunks=[]
    for rank in load(P/'feature_cache/manifest.json')['ranks']:chunks.extend(load(rank)['chunks'])
    chunks.sort(key=lambda x:x['start']);ends=np.array([x['end'] for x in chunks])
    idx=E/'data/direct_dclm_bins_a15/index_val';meta=load(idx/'manifest.json')
    prefix=np.load(idx/'prefix.npy');records=np.load(idx/'records.npy')
    bins=[np.memmap(x['path'],dtype='<u4',mode='r') for x in meta['sources']]
    cases=[];mat=[];rows=[]
    for flag,positions in h['V_first_positions_by_exact_flag'].items():
        for position in positions:
            chunk=chunks[int(np.searchsorted(ends,position,side='right'))];r=position-chunk['start']
            with np.load(chunk['file']) as z:
                lo,hi=map(int,z['ptr'][r:r+2]);ids=z['ids'][lo:hi];values=z['z'][lo:hi]
                col=lookup[ids];keep=col>=0;v=np.zeros(len(fs));v[col[keep]]=values[keep]
            ctx=int(np.searchsorted(prefix,position,side='right')-1);fi,start,length,limit=map(int,records[ctx])
            tokens=np.asarray(bins[fi][start:start+length]);eligible=np.flatnonzero(~np.isin(tokens,meta['excluded_ids']))[:limit]
            tt=int(eligible[int(position)-int(prefix[ctx])]);text=decoder.decode(tokens[:tt+1])
            key=f'G014_chain{flag}_p{position}';relative='prefixes/'+key+'.txt';(O/relative).write_text(text)
            active=[{'feature_id':int(f),'z':float(x)} for f,x in zip(fs,v) if x>0]
            case={'case_id':key,'group_id':14,'position_id':position,'context_id':ctx,'context_offset_zero_based':tt,
                  'token_id':int(tokens[tt]),'token':decoder.decode([tokens[tt]]),'K_full':int((v>0).sum()),
                  'chain_flag':int(flag),'chain_A_B_C':abc,'chain_binary':[int(v[lookup[f]]>0) for f in abc],
                  'selection':'first3 actual V full-cache positions per exact three-node chain flag; not random',
                  'visible_prefix':text,'prefix_file':relative,'active_members':active,
                  'source_path':meta['sources'][fi]['path'],'absolute_source_token_offset':start+tt,
                  'cache_chunk':chunk['file']}
            assert sum(b<<i for i,b in enumerate(case['chain_binary']))==int(flag)
            cases.append(case);mat.append(case['chain_binary'])
            rows.append({'position_id':position,'flag':int(flag),'K_full':case['K_full'],**{str(f):int(x>0) for f,x in zip(fs,v)}})
    (O/'chain_cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
    csvout(O/'case_G014_chain_full_matrix.csv',rows)
    split=load(P/'split_manifest.json');freq=np.load(P/'feature_frequency.npz')['n']
    pairrows=[]
    for si,label in enumerate('DV'):
        C=np.load(P/f'counts/total{si}.npy',mmap_mode='r');N=split['N_'+label]
        hist=np.array(h[label+'_hist'])
        for i,j in [(0,1),(1,2),(0,2)]:
            f,g=abc[i],abc[j];p,q=freq[si,f]/N,freq[si,g]/N
            both=int(C[f,g]);den=np.sqrt(p*(1-p)*q*(1-q))
            flagcount=int(sum(hist[k] for k in range(8) if k&(1<<i) and k&(1<<j)))
            assert both==flagcount
            pairrows.append({'side':label,'feature_i':f,'feature_j':g,'pair':'ABC'[i]+'ABC'[j],
                'N':N,'both':both,'n_i':int(freq[si,f]),'n_j':int(freq[si,g]),
                'phi':float((both/N-p*q)/den) if den>0 else None,
                'triple_ABC':int(hist[7]),'D_frozen_graph_edge':(i,j)!=(0,2)})
    csvout(O/'chain_pair_summary.csv',pairrows)
    font=Path('/data/250010109/Research_System/daily_research_reports/0921/report_assets/fonts/NotoSansCJKsc-Regular.otf')
    font_manager.fontManager.addfont(str(font));plt.rcParams.update({'font.family':font_manager.FontProperties(fname=str(font)).get_name(),'font.size':14,'axes.titlesize':20,'pdf.fonttype':42})
    fig,ax=plt.subplots(figsize=(8,5))
    ax.plot([0,1,2],[0,0,0],color='#607D8B',lw=2)
    ax.scatter([0,1,2],[0,0,0],s=900,color='#607D8B')
    for i,f in enumerate(abc):ax.text(i,.05,f'{"ABC"[i]}: {f}',ha='center',va='bottom',fontsize=17)
    ax.set_xlim(-.4,2.4);ax.set_ylim(-.25,.3);ax.axis('off');ax.set_title('G014 链式子集')
    for ext in ('png','pdf'):fig.savefig(O/'figures'/('figure1_G014_chain_graph.'+ext),dpi=200,bbox_inches='tight')
    plt.close(fig)
    csvout(O/'figures/figure1_G014_chain_graph.csv',[{'node_label':label,'feature_id':f} for label,f in zip('ABC',abc)])
    if cases:
        fig,ax=plt.subplots(figsize=(8,max(4,len(cases)*.55)))
        ax.imshow(np.array(mat),cmap=colors.ListedColormap(['white','#1F4E79']),vmin=0,vmax=1,aspect='auto')
        ax.set_xticks([0,1,2],[f'{label}:{f}' for label,f in zip('ABC',abc)])
        ax.set_yticks(np.arange(len(cases)),[f"{c['position_id']}  K全组={c['K_full']}" for c in cases])
        ax.set_xlabel('链中feature');ax.set_ylabel('完整V实际位置');ax.set_title('G014 链的同位置激活')
        for ext in ('png','pdf'):fig.savefig(O/'figures'/('figure1_G014_chain_matrix.'+ext),dpi=200,bbox_inches='tight')
        plt.close(fig)
        csvout(O/'figures/figure1_G014_chain_matrix.csv',[{'position_id':c['position_id'],'K_full':c['K_full'],**dict(zip(map(str,abc),c['chain_binary']))} for c in cases])
    print('CHAIN_CASES',len(cases))
if __name__=='__main__':main()

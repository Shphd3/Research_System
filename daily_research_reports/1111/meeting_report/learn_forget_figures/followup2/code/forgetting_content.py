import re,sys
from collections import Counter
from meeting_plots import ROOT,R4,O,F,plt,save,np,pd
from scipy import sparse
import torch
sys.path.insert(0,str(R4/'analysis_deps'))
from tokenizers import Tokenizer
KEYS=['Take the tour','EditText of this page','PingBack','Categories','Leave a Reply','permalink','Your Answer']
PAT=re.compile(r'(?<!\w)('+'|'.join(re.escape(x) for x in KEYS)+r')(?!\w)',re.I)
def main():
    torch.set_num_threads(4)
    ft=pd.read_csv(F/'raw/B_shared_features.csv')
    assert len(ft)==3169 and ft.atom.is_unique
    d=torch.load(R4/'data/EVAL_codes.pt',map_location='cpu',weights_only=False)
    idx=d['indices'].numpy();valid=d['values'].numpy()>0
    n=idx.shape[0]
    inverse=np.full(30000,-1,dtype=np.int32);inverse[ft.atom.to_numpy()]=np.arange(len(ft))
    j=inverse[idx]; valid &= j>=0
    pos=np.nonzero(valid)[0].astype(np.int32); j=j[valid]
    C=sparse.csc_matrix((np.ones(len(pos),np.uint8),(pos,j)),shape=(n,len(ft)))
    del d,idx,valid,j,pos
    tt=np.load(R4/'data/EVAL_tokens.npy',mmap_mode='r')
    tokenizer=Tokenizer.from_file('/data/share/Qwen3-0.6B-Base/tokenizer.json')
    def loss(name,t):return np.load(ROOT/f'positions/{name}_{t:012d}.npz')['loss']
    dd=loss('Dense',5*10**9).astype(np.float32)-loss('Dense',3*10**9)
    dm=loss('MoE',5*10**9).astype(np.float32)-loss('MoE',3*10**9)
    both=(dd>0)&(dm>0)
    tags=['网页模板文字','其他（未命中）']
    support=np.zeros((2,n),bool); records=[]
    for col,a in enumerate(ft.atom):
        pp=C.indices[C.indptr[col]:C.indptr[col+1]]
        joint=pp[both[pp]]
        pos=int(joint[0] if len(joint) else pp[0])
        left=max(pos//2048*2048,pos-20);right=min((pos//2048+1)*2048,pos+21)
        dec=lambda sl:tokenizer.decode(tt[sl].astype(int).tolist(),skip_special_tokens=False)
        raw=dec(slice(left,right));hit=PAT.search(' '.join(raw.split()))
        k=0 if hit else 1
        support[k,pp]=True
        context=dec(slice(left,pos))+'⟦'+dec(slice(pos,pos+1))+'⟧'+dec(slice(pos+1,right))
        records.append(dict(atom=int(a),category=tags[k],keyword=hit.group(1) if hit else '',representative_position=pos,representative_both_loss_rose=bool(both[pos]),support_positions=len(pp),support_positions_both_loss_rose=len(joint),Dense_delta=float(dd[pos]),MoE_delta=float(dm[pos]),context=context.replace('\n','⏎')))
    r=pd.DataFrame(records);r.to_csv(O/'04_3169个feature代表上下文.csv',index=False)
    union=support.any(0);ov=support.all(0)
    out=[]
    for i,k in enumerate(tags):
        z=r[r.category==k]
        out.append(dict(category=k,features=len(z),share_features=len(z)/len(r),support_positions_unique=int(support[i].sum()),share_of_union_unique=float(support[i].sum()/union.sum()),feature_position_count=int(z.support_positions.sum()),unique_positions_both_loss_rose=int((support[i]&both).sum()),feature_position_count_both_loss_rose=int(z.support_positions_both_loss_rose.sum())))
    s=pd.DataFrame(out);s.to_csv(O/'04_模板粗分汇总.csv',index=False)
    (O/'04_位置口径.csv').write_text(f'joint_set,positions\n任一类支持并集,{union.sum()}\n两类支持重叠,{ov.sum()}\n')
    fig,ax=plt.subplots(figsize=(10.4,4.8),layout='constrained')
    ix=np.arange(2); w=.32
    for i,color in enumerate(['#7254a3','#8b949f']):
        val=[s.share_features.iloc[i]*100,s.share_of_union_unique.iloc[i]*100]
        bb=ax.bar(ix+(i-.5)*w,val,w,label=tags[i],color=color)
        ax.bar_label(bb,[f'{x:.1f}%' for x in val],padding=4,fontsize=15)
    ax.set_xticks(ix,['共同遗忘 feature 数','支持位置数（两类可重叠）'])
    ax.set_ylim(0,110);ax.set_ylabel('占各自总体的比例（%）')
    ax.set_title('3B→5B 共同遗忘内容：网页模板关键词粗分',fontsize=18,loc='left')
    ax.grid(axis='y',alpha=.22);ax.set_axisbelow(True);ax.legend(fontsize=12)
    save(fig,'04_共同遗忘网页模板粗分')
    md=[]
    for k in tags:
        z=r[r.category==k].copy()
        if k==tags[0]:z=z.assign(kw=z.keyword.str.lower()).drop_duplicates('kw')
        z=z.head(3)
        for rr in z.itertuples():
            ctx=rr.context.replace('|','¦').replace('<','‹').replace('>','›')
            md.append(f'- {k} · feature {rr.atom} · '+(f'命中「{rr.keyword}」：' if rr.keyword else '')+ctx)
    a,b=s.itertuples(index=False)
    (O/'04_读图.md').write_text(f"""## 4｜3B→5B 两种模型共同遗忘了什么

![共同遗忘内容粗分](04_共同遗忘网页模板粗分.png)

[投屏 PDF](04_共同遗忘网页模板粗分.pdf) · [分类汇总](04_模板粗分汇总.csv) · [3169 条代表上下文](04_3169个feature代表上下文.csv)

**读图：** 每个 feature 只用一个代表窗口做关键词粗分，{a.features:,}/{len(r):,}（**{a.share_features:.1%}**）命中网页模板词，{b.features:,}（{b.share_features:.1%}）未命中。模板类、其他类的 EVAL 正激活支持位置分别是 **{a.support_positions_unique:,}**、**{b.support_positions_unique:,}** 个；两个集合重叠 {ov.sum():,} 个，并集 {union.sum():,} 个。图右的两个比例以同一个并集作分母，可以合计超过 100%。按 feature×位置计分别为 {a.feature_position_count:,}、{b.feature_position_count:,} 次。分类不是人工标注，整个 feature 的所有激活位置并非都包含模板词。

**例子（⟦ ⟧ 标记代表位置的输入 token）：**

{chr(10).join(md)}
""")
    print(s.to_string(index=False),flush=True)
if __name__=='__main__':main()

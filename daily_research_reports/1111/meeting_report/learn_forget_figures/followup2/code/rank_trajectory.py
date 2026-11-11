import gc,os,sys,json,time,hashlib
from pathlib import Path
os.environ.setdefault('PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION','python')
from meeting_plots import X,ROOT,BASE,R4,O,plt,save,colors,names,np,pd
import torch
torch.set_num_threads(4)
torch.backends.cuda.matmul.allow_tf32=False
torch.backends.cudnn.allow_tf32=False
R3=BASE/'20261109_teacher_routing_signal_concentration'
R6=BASE/'20261111_a5_to_1B'
old=ROOT/'followup/data/F'
sys.path[:0]=[str(BASE/'20260913_dense_baseline_pretraining'),str(R4),str(R4/'vendor')]
from routing import configure,set_scores,group_scores
from moe_baseline.model import DenseAlignedMoE,MoeConfig
from dense_sae.model import Qwen3SAEForCausalLM,Qwen3SAEConfig
ids=np.array(json.loads((old/'samples.json').read_text())['DEV'])
N=len(ids)*2048
assert N==262144
inv=json.loads((ROOT/'evidence/checkpoint_inventory.json').read_text())
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(8<<20),b''): h.update(b)
    return h.hexdigest()
def state(arm,key,root,step,tokens,config,restored=None,cache=None):
    p=(root/f'runs/{arm}/checkpoints/step_{step:08d}' if restored else root/f'runs/{arm}/milestones/token_{tokens:012d}')/'manifest.json'
    s=json.loads(p.read_text()); f=next(z for z in s['files'] if z['path']=='state.pt')
    return dict(arm=arm,key=key,step=step,tokens=tokens,path=str(restored or p.with_name('state.pt')),config=str(config),sha256=f['sha256'],bytes=f['size_bytes'],cache=cache)
def base(typ,tok,cache=None):
    row=dict(next(r for r in inv if r['model']==typ and r['tokens']==tok))
    return dict(row,arm='Dense' if typ=='Dense' else 'A0',key=f'{typ}_{tok//10**6}M',cache=cache)
def olda(s,cache=None):
    restore=BASE/'20261110_a5_gain_checks/data/A0_500_restored_state.pt' if s==500 else None
    return state('A0',f'A0_step{s}',R3,s,s*262144,R3/'arms/A0.yaml',restored=restore,cache=cache)
plan=[olda(500),base('MoE',10**10),olda(1000),olda(2000,'A0'),base('MoE',10**9),base('MoE',33*10**9),
      state('A5','A5_step2000',R4,2000,524288000,R4/'arms/A5.yaml',cache='A5'),
      state('A5','A5_step3816',R6,3816,1000341504,R6/'arms/A5.yaml'),
      base('Dense',500000000,'Dense'),base('Dense',10**9),base('Dense',10**10)]
def write_json(p,d):
    p.with_suffix('.tmp').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    p.with_suffix('.tmp').replace(p)
def extract(row):
    arm=row['arm'];p=Path(row['path'])
    assert p.stat().st_size==row['bytes'];assert sha(p)==row['sha256']
    cfg=json.loads(Path(row['config']).read_text()); mc=cfg.get('config',cfg)['model']
    m=Qwen3SAEForCausalLM(Qwen3SAEConfig(**mc)) if arm=='Dense' else DenseAlignedMoE(MoeConfig.from_dict(mc))
    s=torch.load(p,map_location='cpu',mmap=True,weights_only=False)
    assert s['tokens_seen']==row['tokens'];m.load_state_dict(s['model'],strict=True);del s
    m.cuda().eval().requires_grad_(False)
    if arm!='Dense': configure(m,{'routing_mode':'native',**cfg})
    assert not m.training and not any(p.requires_grad for p in m.parameters())
    versions=[p._version for p in m.parameters()]; bias=[] if arm=='Dense' else [b.moe.load_bias.clone() for b in m.blocks]
    caps={}; hooks=[b.norm2.register_forward_hook(lambda mod,args,out,i=i:caps.__setitem__(i,out.detach())) for i,b in enumerate(m.blocks)]
    tok=np.load(R4/'data/DEV_tokens.npy',mmap_mode='r')
    xx=torch.as_tensor(np.stack([tok[j*2048:(j+1)*2048] for j in ids]),device='cuda',dtype=torch.long)
    hs=torch.empty((8,N,1024),dtype=torch.float16,device='cuda')
    sel=None if arm=='Dense' else torch.empty((8,N,2),dtype=torch.uint8,device='cuda')
    if arm=='A5':
        g=torch.load(R4/'data/atom_groups.pt',map_location='cpu',weights_only=False)
        d=torch.load(R4/'data/DEV_bf16_codes.pt',map_location='cpu',weights_only=False)
        positions=(ids[:,None]*2048+np.arange(2048)).reshape(-1)
        idx=d['indices'][positions].long().cuda();vv=d['values'][positions].float().cuda();del d
        sc=group_scores(idx,vv,g['group'].cuda(),g['w'].cuda());del idx,vv
    with torch.autocast('cuda',dtype=torch.bfloat16):
        for k in range(0,len(ids),2):
            sl=slice(k*2048,(k+2)*2048)
            if arm=='A5':set_scores(m,sc[sl])
            m.forward_features(xx[k:k+2])
            for l in range(8):
                hs[l,sl].copy_(caps[l].reshape(-1,1024))
                if sel is not None:sel[l,sl].copy_(m.blocks[l].moe.last_selected.reshape(-1,2))
            if k in (30,62,94,126):print('FORWARD',row['key'],k+2,flush=True)
    assert versions==[p._version for p in m.parameters()]
    assert all(torch.equal(a,b.moe.load_bias) for a,b in zip(bias,m.blocks))
    for hook in hooks:hook.remove()
    del m;return hs,sel
def rank(x):
    n=x.shape[0]
    if n<2:return (float('nan'),float('nan'),n)
    xx=x.double();xx=xx-xx.mean(0)
    C=(xx.T@xx)/(n-1)
    ev=torch.linalg.eigvalsh((C+C.T)*.5)
    minimum=float(ev[0]);ev=ev.clamp_min(0)
    pr=ev/ev.sum();v=pr[pr>0]
    return float((-v*v.log()).sum().exp()),minimum,n
def compute(row):
    c=row['cache'];a=row['arm']; tic=time.monotonic()
    if c:
        hs=np.load(old/f'h_{c}_DEV.npy',mmap_mode='r'); sel=None if a=='Dense' else np.load(old/f'sel_{c}_DEV.npy',mmap_mode='r')
        source='复用任务 F 同 DEV 前向缓存'
    else: hs,sel=extract(row); source='本地 MIG 只读 DEV 前向'
    print('RANK',row['key'],flush=True)
    out=[]
    for l in range(8):
        h=torch.from_numpy(hs[l].copy()).cuda() if c else hs[l]
        gl,mn,n=rank(h)
        core={k:row[k] for k in ('arm','key','step','tokens')};core.update(layer=l,global_rank=gl,source=source)
        out.append(dict(core,expert=-1,n=n,expert_rank=None,ratio=None,min_eigenvalue=mn))
        if sel is not None:
            s=torch.from_numpy(sel[l].copy()).cuda() if c else sel[l]
            cnt=0
            for e in range(8):
                m=(s==e).any(1);r,mn,n=rank(h[m]);cnt+=n
                out.append(dict(core,expert=e,n=n,expert_rank=r,ratio=r/gl,min_eigenvalue=mn))
            assert cnt==2*N
    write_json(X/f'evidence/{row["key"]}.json',dict(identity=row,source=source,positions=N,training_updates=0,seconds=time.monotonic()-tic,rows=out))
    print('DONE',row['key'],round(time.monotonic()-tic,2),flush=True)
def summarize():
    rows=[z for row in plan for p in [X/f'evidence/{row["key"]}.json'] if p.exists() for z in json.loads(p.read_text())['rows']]
    if not rows:return
    d=pd.DataFrame(rows)
    d.assign(model=d.arm.map(names)).to_csv(O/'03_逐专家有效秩.csv',index=False)
    keys=['arm','key','step','tokens','layer','source','global_rank']
    g=d[d.expert==-1][keys]
    exp=d[d.expert>=0]
    stats=exp.groupby(['key','layer']).ratio.agg(ratio_median='median',ratio_q10=lambda x:x.quantile(.1),ratio_q90=lambda x:x.quantile(.9)).reset_index()
    z=g.merge(stats,on=['key','layer'],how='left').sort_values(['arm','tokens','layer'])
    z.assign(model=z.arm.map(names)).to_csv(O/'03_逐层有效秩与比值.csv',index=False)
    s=z.assign(layer_group=np.where(z.layer<4,'第 0–3 层','第 4–7 层')).groupby(['arm','key','tokens','step','layer_group']).agg(ratio_mean=('ratio_median','mean'),global_rank_mean=('global_rank','mean')).reset_index()
    s.assign(model=s.arm.map(names)).to_csv(O/'03_层段曲线.csv',index=False)
    p=s[s.arm=='A0'].pivot(index='key',columns='layer_group',values='ratio_mean')
    first=['A0_step500','A0_step1000']; mid=['A0_step2000','MoE_1000M','MoE_10000M']
    needed=first+mid; verdict='等待检查点'
    if set(needed)<=set(p.index):
        ok=(p.loc[first].lt(.90).all())&(p.loc[mid].le(.95).all())
        verdict='输入方向的减少在早期形成并保持' if ok.all() else ('仅'+ '、'.join(ok[ok].index)+'满足完整判据' if ok.any() else '两个层段均未满足完整预设判据')
    fig,ax=plt.subplots(figsize=(12,5.9),layout='constrained')
    for a in ('A0','A5'):
        for i,g in enumerate(['第 0–3 层','第 4–7 层']):
            q=s[(s.arm==a)&(s.layer_group==g)].sort_values('tokens')
            if q.empty:continue
            ax.plot(q.tokens/1e9,q.ratio_mean,'o-' if i==0 else 's--',lw=2.3,ms=7,label=names[a]+'｜'+g,color=colors[a])
    ax.axhline(.9,ls=':',c='#aaa',lw=1.2);ax.axhline(.95,ls=':',c='#777',lw=1.2)
    ax.axhline(1,ls='--',c='#aaa',lw=1.2)
    ax.set_xscale('log');ax.set_xticks([.131072,.262144,.524288,1,10,33],['0.131','0.262','0.524','1','10','33'])
    ax.set_xlim(.11,39);ax.set_ylim(min(.67,float(s.ratio_mean.min())-.03),1.025);ax.set_ylabel('专家输入有效秩 ÷ 全部输入有效秩');ax.set_xlabel('累计训练 token（B，对数轴）')
    ax.grid(alpha=.22);ax.legend(fontsize=12,loc='lower right');ax.set_title('原生分发何时开始减少专家输入的有效方向？',loc='left',fontsize=19)
    save(fig,'03_专家输入有效秩随训练变化')
    desc=[]
    for k in ['A0_step500','A0_step1000','A0_step2000','MoE_1000M','MoE_10000M','MoE_33000M']:
        if k in p.index:desc.append(f'{k}：{p.loc[k].iloc[0]:.3f}/{p.loc[k].iloc[1]:.3f}')
    missing=[row['key'] for row in plan if row['key'] not in set(d.key)]
    (O/'03_读图.md').write_text(f"""## 3｜原生路由的输入方向减少，何时形成？

![专家输入秩比随训练变化](03_专家输入有效秩随训练变化.png)

[投屏 PDF](03_专家输入有效秩随训练变化.pdf) · [逐层秩比及全局绝对秩](03_逐层有效秩与比值.csv) · [逐 expert 表](03_逐专家有效秩.csv) · [画图点值](03_层段曲线.csv)

**读图：** 先看蓝线与 0.90/0.95 参考线；每个点先在每层取八个 expert 的秩比中位数，再在四层内等权平均。**按预设判据：{verdict}。** 原生 MoE（0–3 层／4–7 层）：{'；'.join(desc)}。A0 的 2000 步及以前与 1B 起正式原生 baseline 的存档来源不同；点间只连已测点，不表示持续观测。Dense 只提供绝对全局秩，见表。

已完成 {len(plan)-len(missing)}/{len(plan)} 个检查点。缺失：{'、'.join(missing) if missing else '无'}。
""")
def main():
    write_json(X/'evidence/checkpoints.json',plan)
    for row in plan:
        if not (X/f'evidence/{row["key"]}.json').exists():
            try:
                print('START',row['key'],flush=True);compute(row)
            except Exception as e:
                import traceback;traceback.print_exc()
                (X/'evidence/errors.log').open('a').write(f'{row["key"]}: {e!r}\n')
        gc.collect();torch.cuda.empty_cache()
        summarize()
if __name__=='__main__':
    with torch.no_grad():main()

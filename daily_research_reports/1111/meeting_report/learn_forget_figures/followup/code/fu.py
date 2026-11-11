from pathlib import Path
import sys,os,json,time,datetime,hashlib
F=Path(__file__).resolve().parents[1];ROOT=F.parent;sys.path.insert(0,str(ROOT/'code'))
from lf_common import N,R4,R5,R3,REPO,features,codes,artifact,evals,sha
import numpy as np,pandas as pd,torch
from scipy import sparse
from scipy.stats import spearmanr,rankdata,norm,hypergeom
REPORT=REPO/'daily_research_reports/1111/meeting_report/learn_forget_figures/followup';REPORT.mkdir(parents=True,exist_ok=True)
TIMES=[0,500000000,1000000000,3000000000,5000000000,10000000000]
REFS={'MoE33B':('MoE',33000000000),'Dense_latest':('Dense',34076363264)}
COLORS={'Dense':'#d97720','MoE':'#2471a3','A0':'#2471a3','A5':'#7254a3','A9':'#16856a','A9d':'#e99c1b','A1':'#ce75a7','A2':'#777777','low':'#7254a3','high':'#666666'}
def dump(path,x):
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def table(d,name,note=''):
 p=F/'results'/name;p.parent.mkdir(parents=True,exist_ok=True);d.to_csv(p.with_suffix('.csv'),index=False,float_format='%.9g');p.with_suffix('.md').write_text('# '+name+'\n\nAI分析；研究者判断Unknown。'+note+'\n\n'+d.to_markdown(index=False,floatfmt='.7g')+'\n')
def event(task,text,**kw):
 z=dict(time_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),task=task,AI_analysis=text,researcher_judgment='Unknown',**kw)
 with (F/'evidence/events.jsonl').open('a') as f:f.write(json.dumps(z,ensure_ascii=False)+'\n')
 print(json.dumps(z,ensure_ascii=False),flush=True)
def plotting():
 import matplotlib;matplotlib.use('Agg')
 from matplotlib import font_manager
 p=F/'data/NotoSansCJKsc-Regular.otf'
 assert p.exists() and p.stat().st_size>1000000,'Chinese font not ready'
 font_manager.fontManager.addfont(str(p));matplotlib.rcParams.update({'font.family':font_manager.FontProperties(fname=str(p)).get_name(),'axes.unicode_minus':False,'pdf.fonttype':42})
 import matplotlib.pyplot as plt
 return plt
def savefig(fig,name,note):
 fig.tight_layout()
 for ext in ['png','pdf']:fig.savefig(F/f'results/{name}.{ext}',dpi=170)
 __import__('matplotlib.pyplot',fromlist=['close']).close(fig)
 (F/f'results/{name}_读法.md').write_text('AI分析；研究者判断Unknown。\n\n'+note+'\n')
def loss(model,t):return np.load(ROOT/f'positions/{model}_{t:012d}.npz')['loss'].astype(np.float64)
def states(model):
 p=F/f'data/states_{model}.npy'
 if p.exists():return np.load(p,mmap_mode='r')
 ss=[];prev=np.zeros(N,bool)
 for t in TIMES:
  v=loss(model,t);prev=np.where(v<=np.log(2),True,np.where(v>=2*np.log(2),False,prev));ss.append(prev.copy())
 out=np.stack(ss);np.save(p,out);return out
def refmask(ref):
 m,t=REFS[ref];return loss(m,t)<=np.log(2)
def metadata():
 d=artifact('A0',2000);return d['feature_bin'].numpy(),d['p_dev'].numpy(),torch.load(R4/'data/atom_groups.pt',map_location='cpu',weights_only=False)['group'].numpy()
def docs():
 tok=np.load(R4/'data/EVAL_tokens.npy',mmap_mode='r');return np.cumsum((tok[:N]==151645).astype(np.int32))
def doc_features(Fx,mask,dd,weights=None):
 ii=np.flatnonzero(mask);v=np.ones(len(ii),np.float32) if weights is None else weights[ii].astype(np.float32);D=int(dd.max())+1
 return (sparse.csr_matrix((v,(dd[ii],ii)),shape=(D,N))@Fx).T.tocsr()
def partial_rho(g,x,lp,k):
 Z=np.column_stack([np.ones(len(g)),rankdata(lp),rankdata(k)]);a=rankdata(g);b=rankdata(x);a-=Z@np.linalg.lstsq(Z,a,rcond=None)[0];b-=Z@np.linalg.lstsq(Z,b,rcond=None)[0];return float(np.corrcoef(a,b)[0,1]) if np.std(a)>0 and np.std(b)>0 else np.nan
def bh(p):
 ix=np.argsort(p);q=np.minimum.accumulate((p[ix]*len(p)/np.arange(1,len(p)+1))[::-1])[::-1];out=np.empty_like(q);out[ix]=np.minimum(q,1);return out
def decode_contexts(Fx,atoms,prefer,selection_name,extra=None,allowed=None):
 sys.path.insert(0,str(R4/'analysis_deps'));from tokenizers import Tokenizer
 tok=Tokenizer.from_file('/data/share/Qwen3-0.6B-Base/tokenizer.json');tt=np.load(R4/'data/EVAL_tokens.npy',mmap_mode='r');dd=docs();C=Fx.tocsc();rows=[]
 for j in atoms:
  pp=C.indices[C.indptr[j]:C.indptr[j+1]]
  if allowed is not None:pp=pp[allowed[pp]]
  first=pp[prefer[pp]];ordered=np.concatenate([first,pp[~prefer[pp]]]);chosen=[];seen=set()
  for pos in ordered:
   if int(dd[pos]) not in seen:chosen.append(int(pos));seen.add(int(dd[pos]))
   if len(chosen)==3:break
  if len(chosen)<3:
   for pos in ordered:
    if int(pos) not in chosen:chosen.append(int(pos))
    if len(chosen)==3:break
  for rank,pos in enumerate(chosen,1):
   lo=max(pos//2048*2048,pos-20);hi=min((pos//2048+1)*2048,pos+21);dec=lambda x:tok.decode(list(map(int,x)),skip_special_tokens=False)
   text=(dec(tt[lo:pos])+'⟦'+dec(tt[pos:pos+1])+'⟧'+dec(tt[pos+1:hi])).replace('\n','⏎').replace('|','¦')
   r=dict(selection=selection_name,atom=int(j),example=rank,position=pos,document=int(dd[pos]),context=text,next_token=dec(tt[pos+1:pos+2]),preferred_disagreement=bool(prefer[pos]))
   if extra:
    for key,val in extra.items():r[key]=val[pos].item() if hasattr(val[pos],'item') else val[pos]
   rows.append(r)
 return pd.DataFrame(rows)

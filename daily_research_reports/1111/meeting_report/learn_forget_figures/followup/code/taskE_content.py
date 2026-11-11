from fu import *
from threadpoolctl import threadpool_limits

def main():
 tic=time.monotonic();fb,p,ag=metadata();groupfile=torch.load(R4/'data/atom_groups.pt',map_location='cpu',weights_only=False);w=groupfile['w'].numpy();dev=codes('DEV');ii=dev['indices'].numpy();vv=dev['values'].numpy();mass=np.bincount(ii.ravel(),weights=(np.maximum(vv,0)*w[ii]).ravel(),minlength=30000);del dev,ii,vv
 selected=[]
 for group in range(16):
  allow=(ag==group//2)&((fb<=2) if group%2==0 else (fb>=7));ids=np.flatnonzero(allow);ids=ids[np.lexsort((ids,-mass[ids]))[:2]]
  for rank,j in enumerate(ids,1):selected.append(dict(group=group,A5_group=group//2,frequency_band='高频bin7–9' if group%2 else '低频bin0–2',rank=rank,atom=int(j),bin=int(fb[j]),p_DEV=float(p[j]),weighted_DEV_mass=float(mass[j])))
 tab=pd.DataFrame(selected);base=pd.read_csv(F/'results/raw/A_MoE33B_10000000000.csv');tab=tab.merge(base[['atom','M','K_Dense','K_MoE','G']],on='atom',how='left');table(tab,'E_group_representative_features')
 ev=codes('EVAL');ii=ev['indices'].numpy();vv=ev['values'].numpy();tt=np.load(R4/'data/EVAL_tokens.npy',mmap_mode='r');dd=docs();sys.path.insert(0,str(R4/'analysis_deps'));from tokenizers import Tokenizer
 tok=Tokenizer.from_file('/data/share/Qwen3-0.6B-Base/tokenizer.json');dec=lambda t:tok.decode(list(map(int,t)),skip_special_tokens=False);contexts=[]
 for row in selected:
  rr,cc=np.where(ii==row['atom']);v=vv[rr,cc];keep=v>0;rr=rr[keep];v=v[keep];ix=np.lexsort((rr,-v));chosen=[];seen=set()
  for k in ix:
   pos=int(rr[k]);doc=int(dd[pos])
   if doc not in seen:chosen.append((pos,float(v[k])));seen.add(doc)
   if len(chosen)==3:break
  for rank,(pos,val) in enumerate(chosen,1):
   lo=max(pos//2048*2048,pos-20);hi=min((pos//2048+1)*2048,pos+21);text=(dec(tt[lo:pos])+'⟦'+dec(tt[pos:pos+1])+'⟧'+dec(tt[pos+1:hi])).replace('\n','⏎').replace('|','¦');contexts.append(dict(group=row['group'],atom=row['atom'],feature_rank=row['rank'],example=rank,position=pos,document=int(dd[pos]),activation=val,current_token=dec(tt[pos:pos+1]).replace('\n','⏎'),next_token=dec(tt[pos+1:pos+2]).replace('\n','⏎'),context=text))
 table(pd.DataFrame(contexts),'E_group_representative_contexts','每组×频段先按旧DEV的sum(z*w)选2原子，再按EVAL激活强度选不同文档的3例；内容示例不是已验证语义类别。');dump(F/'evidence/E_content_complete.json',dict(seconds=time.monotonic()-tic,features=len(selected),contexts=len(contexts),training_updates=0));event('E内容','16组各2原子与真实高激活上下文完成',seconds=time.monotonic()-tic,GPU_seconds=0)
if __name__=='__main__':
 with threadpool_limits(limits=4):main()

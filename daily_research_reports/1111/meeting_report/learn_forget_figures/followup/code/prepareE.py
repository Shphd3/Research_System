from fu import *
import gc
def main():
 target=F/'data/E';target.mkdir(exist_ok=True);split=json.load(open(R4/'data/split.json'));raw=np.memmap(split['source'],dtype=np.uint32,mode='r');start=int(split['EVAL'][1]);need=N+1;end=start+need+int(np.flatnonzero(raw[start+need:start+need+1000000]==151645)[0])+1
 assert start>=split['EVAL'][1] and raw[start-1]==151645 and raw[end-1]==151645
 ext=np.array(raw[start:start+need],dtype=np.int64);old=np.load(R4/'data/DEV_tokens.npy',mmap_mode='r');inputs=np.lib.format.open_memmap(target/'inputs.npy',mode='w+',dtype=np.int64,shape=(2048,2048));targets=np.lib.format.open_memmap(target/'targets.npy',mode='w+',dtype=np.int64,shape=(2048,2048));inputs[:1024]=old[:N].reshape(1024,2048);targets[:1024]=old[1:N+1].reshape(1024,2048);inputs[1024:]=ext[:N].reshape(1024,2048);targets[1024:]=ext[1:N+1].reshape(1024,2048);inputs.flush();targets.flush()
 dump(F/'evidence/E_extension_source.json',dict(source=split['source'],source_bytes=Path(split['source']).stat().st_size,new_retained_document_range=[start,end],new_used_input_target_range=[start,start+need],old_DEV=split['DEV'],old_EVAL=split['EVAL'],source_document_disjoint=True,training_view_source_shard_excluded=True,no_exhaustive_text_deduplication_claim=True,teacher_precision='FP32 matches originalDEV_codes.pt',user_authorized=True))
 W=np.lib.format.open_memmap(target/'group_weights.npy',mode='w+',dtype=np.float16,shape=(2*N,16));dc=codes('DEV');fb,_,ag=metadata();idx=dc['indices'].numpy();valid=dc['values'].numpy()>0;lab=2*ag[idx]+(fb[idx]>=7);used=valid&((fb[idx]<=2)|(fb[idx]>=7))
 for g in range(16):W[:N,g]=((lab==g)&used).sum(1)/32
 del dc,idx,lab,used,valid;gc.collect();sys.path.insert(0,str(R3));from teacher import load_teacher,encode
 m,sae=load_teacher('cuda');versions=[p._version for p in m.parameters()]+[p._version for p in sae.parameters()];bias=[b.moe.load_bias.clone() for b in m.blocks];tic=time.monotonic()
 with torch.inference_mode():
  for k in range(0,1024,2):
   x=torch.from_numpy(np.array(inputs[1024+k:1024+k+2])).long().cuda();ii,vv=encode(m,sae,x,bf16=False);idx=ii.cpu().numpy();valid=vv.cpu().numpy()>0;lab=2*ag[idx]+(fb[idx]>=7);used=valid&((fb[idx]<=2)|(fb[idx]>=7));sl=slice(N+k*2048,N+(k+2)*2048)
   for g in range(16):W[sl,g]=((lab==g)&used).sum(1)/32
   if k%128==0:print('E_EXTENSION_ENCODING',k,'seconds',round(time.monotonic()-tic),flush=True)
 assert versions==[p._version for p in m.parameters()]+[p._version for p in sae.parameters()];assert all(torch.equal(a,b.moe.load_bias) for a,b in zip(bias,m.blocks));W.flush();del m,sae;gc.collect();torch.cuda.empty_cache()
 old_batches=json.load(open(ROOT/'precision8/evidence/gradient_batches.json'))['sequence_ids'];old_used={s for groups in old_batches.values() for batch in groups for s in batch};pool=np.array(sorted(set(range(2048))-old_used));rng=np.random.default_rng(20261112);rng.shuffle(pool);assert len(pool)==1536;full={};small={};rng2=np.random.default_rng(20261115);cursor=0
 for g in range(16):
  full[str(g)]=[];small[str(g)]=[]
  for r in range(4):
   ids=list(map(int,old_batches[str(g)][r]))+list(map(int,pool[cursor:cursor+24]));cursor+=24;full[str(g)].append(ids);small[str(g)].append(rng2.choice(ids,8,replace=False).tolist())
 allids=[s for gg in full.values() for batch in gg for s in batch];assert len(allids)==len(set(allids))==2048
 dump(F/'data/E/batches32.json',full);dump(F/'data/E/batches8_extended.json',small);dump(F/'evidence/E_preparation_complete.json',dict(encoding_seconds=time.monotonic()-tic,sequences=2048,all_sequences_globally_unique=True,old8_preserved_in32=True,teacher_and_SAE_unchanged=True,bias_unchanged=True,training_updates=0));event('E准备','扩展独立DEV及固定32/扩展8批次准备完成',seconds=time.monotonic()-tic)
if __name__=='__main__':main()

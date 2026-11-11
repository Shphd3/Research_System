from common import *
import io,tarfile,shutil
p=R3/'runs/A0/checkpoints/step_00000500/state.pt.AOSS_ARCHIVED.json';receipt=json.load(open(p));manifest=Path(receipt['aoss_manifest']);m=json.load(open(manifest));parts=[manifest.parent/x['name'] for x in m['parts']];out=R/'data/A0_500_restored_state.pt'
for p,z in zip(parts,m['parts']):assert p.stat().st_size==z['bytes'] and sha(p)==z['sha256']
class Chain(io.RawIOBase):
 def __init__(self,paths):self.paths=iter(paths);self.f=None
 def readable(self):return True
 def read(self,n=-1):
  if n<0:n=1<<24
  result=[];left=n
  while left:
   if self.f is None:
    try:self.f=next(self.paths).open('rb')
    except StopIteration:break
   b=self.f.read(left)
   if not b:self.f.close();self.f=None;continue
   result.append(b);left-=len(b)
  return b''.join(result)
with tarfile.open(fileobj=Chain(parts),mode='r|') as tf:
 found=False
 for member in tf:
  if Path(member.name).name==receipt['tar_member'] and member.isfile():
   with tf.extractfile(member) as src,out.open('wb') as dest:shutil.copyfileobj(src,dest,8<<20)
   found=True;break
assert found
actual=sha(out);assert actual==m['inventory'][0]['sha256']
expected=json.load(open(R3/'runs/A0/checkpoints/step_00000500/manifest.json'));expected=[x for x in expected['files'] if x['path']=='state.pt'][0]['sha256'];assert actual==expected
register('checkpoint_a5checks_A0_500_restored_readonly_20261110','A0 500步归档字节一致的新路径恢复副本',[out],dict(original=str(receipt['source']),archive=str(manifest),sha256=actual,optimizer_step=500,restore_scope='new execution root only; original archived placeholder unchanged'),category='model_checkpoint')
dump(R/'evidence/A0_500_restore.json',dict(status='VERIFIED',path=str(out),sha256=actual,original_manifest_sha256=expected,archive=str(manifest),original_path_restored=False))
print('RESTORED',out,flush=True)

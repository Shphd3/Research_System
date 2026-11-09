from common import *
import shutil
# Selected small evidence only; complete raw outputs remain execution-side or in packet.
for folder in ['code','figures']:
 for source in (R/folder).iterdir():
  if source.is_file() and source.suffix in ['.py','.png','.json']:
   dest=C/folder/source.name;dest.parent.mkdir(exist_ok=True);shutil.copyfile(source,dest)
for folder in ['tables','evidence','results']:
 for source in (R/folder).iterdir():
  if source.is_file() and source.suffix in ['.csv','.json'] and source.stat().st_size<=2*1024*1024:
   dest=C/folder/source.name;dest.parent.mkdir(exist_ok=True);shutil.copyfile(source,dest)
for source in [R/'config.json',R/'effective_config.json']:(C/source.name).write_bytes(source.read_bytes())
for source in (R/'data').glob('*_bins.json'):
 dest=C/'config'/source.name;dest.parent.mkdir(exist_ok=True);shutil.copyfile(source,dest)
small=[]
for dest in C.rglob('*'):
 if dest.is_file() and dest.suffix in ['.json','.csv','.png','.svg']:
  rel=dest.relative_to(C);origin=R/rel
  if rel.parts[0]=='config':origin=R/'data'/dest.name
  small.append(dict(path=str(dest.relative_to(P)),purpose='R20 selected auditable evidence: '+str(rel),origin=str(origin),sha256=sha(dest),bytes=dest.stat().st_size))
manifest=P/'main/curated_evidence.json';j=json.load(open(manifest));prefix=str(C.relative_to(P))+'/';j['assets']=[a for a in j['assets'] if not a['path'].startswith(prefix)]+small;dump(manifest,j)

print("CURATED",len(small))

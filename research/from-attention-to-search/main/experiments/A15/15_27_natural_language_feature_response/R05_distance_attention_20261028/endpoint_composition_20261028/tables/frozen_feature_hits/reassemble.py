from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent
m=json.loads((p/'manifest.json').read_text())
parts=[]
for row in m['parts']:
 b=(p/row['path']).read_bytes()
 assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
 parts.append(b)
b=parts[0]+b''.join(x[m['header_bytes']:] for x in parts[1:])
assert len(b)==m['source_bytes'] and hashlib.sha256(b).hexdigest()==m['source_sha256']
out=p.parent/'frozen_feature_hits.csv'
if out.exists(): assert out.read_bytes()==b
else: out.write_bytes(b)
print(out)

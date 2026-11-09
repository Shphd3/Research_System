# 完整结果表：无损CSV分片

原表3,426,200字节，超过当前单文件2MiB证据上限。以下分片各含完整表头，保留全部记录、原顺序和精确字节；没有删行或重新筛选。

- [part01.csv](part01.csv)：14260行，1572815字节。
- [part02.csv](part02.csv)：14161行，1572795字节。
- [part03.csv](part03.csv)：2299行，280838字节。

[来源及逐片哈希](manifest.json) · [无损恢复脚本](reassemble.py)。运行该脚本可在父目录恢复原文件，逐片和完整SHA256均会校验；原执行侧文件保持原样。

## 在仅有阅读副本时恢复

下面是同一恢复脚本，标准库即可运行；把脚本放在分片和manifest旁。

```python
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
```

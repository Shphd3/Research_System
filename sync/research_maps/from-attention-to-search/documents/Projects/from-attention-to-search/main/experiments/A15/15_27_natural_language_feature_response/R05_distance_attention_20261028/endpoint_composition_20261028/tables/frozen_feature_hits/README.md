派生阅读副本；原件位置：`Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R05_distance_attention_20261028/endpoint_composition_20261028/tables/frozen_feature_hits/README.md`。
[精确原始文件](../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R05_distance_attention_20261028/endpoint_composition_20261028/tables/frozen_feature_hits/README.md)；研究修改仍回到原件。

---

# 完整结果表：无损CSV分片

原表3,426,200字节，超过当前单文件2MiB证据上限。以下分片各含完整表头，保留全部记录、原顺序和精确字节；没有删行或重新筛选。

- [part01.csv](../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R05_distance_attention_20261028/endpoint_composition_20261028/tables/frozen_feature_hits/part01.csv)：14260行，1572815字节。
- [part02.csv](../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R05_distance_attention_20261028/endpoint_composition_20261028/tables/frozen_feature_hits/part02.csv)：14161行，1572795字节。
- [part03.csv](../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R05_distance_attention_20261028/endpoint_composition_20261028/tables/frozen_feature_hits/part03.csv)：2299行，280838字节。

[来源及逐片哈希](../../../../../../../../../../../sources/Projects/from-attention-to-search/main/experiments/A15/15_27_natural_language_feature_response/R05_distance_attention_20261028/endpoint_composition_20261028/tables/frozen_feature_hits/manifest.json) · [无损恢复脚本](../../../../../../../../../../../UNAVAILABLE.md)。运行该脚本可在父目录恢复原文件，逐片和完整SHA256均会校验；原执行侧文件保持原样。

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

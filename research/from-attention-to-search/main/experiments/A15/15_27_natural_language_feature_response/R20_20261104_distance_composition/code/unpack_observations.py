from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1]
with np.load(R/'cache/new_all.npz') as a:
 for i,pid in enumerate(a['ids']):
  p=R/f'cache/new_rows/{pid}.npz';p.parent.mkdir(exist_ok=True)
  if p.exists():continue
  payload={key:(a[key] if key.endswith('__decoder_norm') else a[key][i:i+1]) for key in a.files if key!='ids'};np.savez_compressed(p,**payload)
print('Native row arrays restored; NPZ container bytes may differ from original file SHAs, arrays are identical.')

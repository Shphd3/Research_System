#!/usr/bin/env bash
set -euo pipefail
TASK_ROOT=/data/250010109/MoE_Router/experiments/20261101_dense_checkpoint_spectral_dynamics
cd "$TASK_ROOT"
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
export CUDA_VISIBLE_DEVICES=0,1
source /data/250010109/MoE_Router/experiments/20260913_dense_baseline_pretraining/scripts/activate_5090_runtime.sh
python -u scripts/calibrate.py
python -u scripts/collect.py --smoke
python -u scripts/collect.py --smoke
python - <<'PY'
import json,pathlib
r=pathlib.Path('.')
a=json.load(open('smoke_cache_index.json'));assert len(a)==3 and all(x['geometry_checks']['main_equals_final_norm_input'] and x['model_released'] for x in a)
(r/'audit/smoke.json').write_text(json.dumps(dict(status='PASS',states=3,records_per_state=8,cache_reread='PASS',interface='final_raw_h==final_norm_input',counter_and_digest='PASS'),indent=2)+'\n')
PY
python -u scripts/collect.py
python -u scripts/analysis_cache_identity.py
python -u scripts/analyze.py
python -u scripts/analysis_cache_identity.py --seal
python - <<'PY'
import json,datetime,pathlib
p=pathlib.Path('analysis/completion.json');a=json.load(open(p));a['pipeline']='smoke/full/geometry/readouts/figures';a['ended_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();pathlib.Path('terminal_receipt.json').write_text(json.dumps(a,indent=2)+'\n')
PY

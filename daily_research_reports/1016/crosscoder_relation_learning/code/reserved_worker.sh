#!/usr/bin/env bash
# One authorized four-H100 allocation. Stage scripts are durable, task-local inputs.
set -euo pipefail
cd /data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder
source scripts/runtime.sh
RUN=/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder/analysis/relation_learning/20261015T164000Z
mkdir -p "$RUN/control" "$RUN/platform" "$RUN/logs"
python - <<'PY'
import torch, json, os, datetime, platform, importlib.util
from pathlib import Path
r=Path('analysis/relation_learning/20261015T164000Z/platform')
x={'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'hostname':platform.node(),'torch':torch.__version__,'cuda':torch.version.cuda,'gpus':[],'dependencies':{k:bool(importlib.util.find_spec(k)) for k in ['safetensors','transformers','tensorboard']}}
assert torch.cuda.device_count()==4,torch.cuda.device_count()
for i in range(4):
 p=torch.cuda.get_device_properties(i);torch.cuda.set_device(i)
 a=torch.randn(256,256,device='cuda',dtype=torch.bfloat16);b=a@a;torch.cuda.synchronize()
 x['gpus'].append({'index':i,'name':p.name,'bytes':p.total_memory,'finite_bf16_matmul':bool(b.isfinite().all())})
 assert 'H100' in p.name and p.total_memory>70e9
x['status']='DEVICE_PREFLIGHT_PASS';(r/'device_preflight.json').write_text(json.dumps(x,indent=2)+'\n')
print(json.dumps(x),flush=True)
PY
START=$SECONDS
IDLE=$SECONDS
while (( SECONDS-START < 21000 )); do
    if [[ -f "$RUN/control/STOP" ]]; then break; fi
    FOUND=0
    for STAGE in "$RUN"/control/stage_*.sh; do
        [[ -f "$STAGE" ]] || continue
        NAME=$(basename "$STAGE" .sh)
        [[ -f "$RUN/control/$NAME.done.json" ]] && continue
        FOUND=1
        export STAGE_PATH="$STAGE" STAGE_NAME="$NAME" STAGE_RUN="$RUN"
        python - <<'PY'
import os,hashlib,json,datetime
from pathlib import Path
p=Path(os.environ['STAGE_PATH']);r=Path(os.environ['STAGE_RUN'])/'control'
(r/(os.environ['STAGE_NAME']+'.started.json')).write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'script':str(p)},indent=2)+'\n')
PY
        set +e
        timeout --signal=TERM --kill-after=30 10800 bash "$STAGE" > "$RUN/logs/$NAME.log" 2>&1
        CODE=$?
        set -e
        export STAGE_EXIT_CODE="$CODE"
        python - <<'PY'
import os,json,datetime
from pathlib import Path
r=Path(os.environ['STAGE_RUN'])/'control';p=r/(os.environ['STAGE_NAME']+'.done.json')
p.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':int(os.environ['STAGE_EXIT_CODE'])},indent=2)+'\n')
PY
        IDLE=$SECONDS
    done
    if (( ! FOUND && SECONDS-IDLE > 1500 )); then
        echo 'No pending stage for 25 minutes; bounded worker exits.'
        break
    fi
    sleep 5
done
python - <<'PY'
from pathlib import Path
import json,datetime
r=Path('analysis/relation_learning/20261015T164000Z')
(r/'platform'/'worker_terminal.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'WORKER_EXITED','scientific_question_answered':False},indent=2)+'\n')
PY

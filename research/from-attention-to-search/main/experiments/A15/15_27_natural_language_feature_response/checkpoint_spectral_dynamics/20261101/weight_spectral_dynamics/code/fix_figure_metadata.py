"""Repair a figure-manifest color-range field; preserve old manifest and all pixels."""
from pathlib import Path
import json,csv,hashlib,datetime,shutil
r=Path(__file__).resolve().parents[1];p=r/'figures/manifest.json';old=r/'audit/plot_manifest_before_metadata_correction.json'
if not old.exists():shutil.copy2(p,old)
m=json.load(open(p));rows=list(csv.DictReader(open(r/'tables/pair_metrics.csv')))
actual=max(30,max(float(x['s1_relative_change_symmetric'])*100 for x in rows if x['comparison']=='adjacent' and x['side']=='input'))
before=m['figure1_weight_top1']['metrics'][0]['color_range'];m['figure1_weight_top1']['metrics'][0]['color_range']=[0,actual];p.write_text(json.dumps(m,indent=2)+'\n')
(r/'audit/figure_metadata_correction.json').write_text(json.dumps(dict(time_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),class_='EXPRESSION_PROVENANCE_ONLY',problem='image correctly used automatic non-clipping color maximum;manifest retained nominal30percent',before=before,after=[0,actual],source='all adjacent input-side s1 symmetric relative changes',effect='metadata only;pixels,numeric tables,eligibility and conclusions unchanged',old_manifest=str(old),corrected_manifest_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),reproduction='After scripts/plot.py run scripts/fix_figure_metadata.py'),indent=2)+'\n')
print('FIGURE_METADATA_FIXED',actual)

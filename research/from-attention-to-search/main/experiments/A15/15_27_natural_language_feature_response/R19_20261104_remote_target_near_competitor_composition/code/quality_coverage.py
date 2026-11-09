from engine import *
q=[];cv=[];spec=json.load(open(R/'data/candidates.json'))['sites']
for site in SITES:
 for split in ['discovery','heldout']:
  p,z,a=load_stage(split,site);err=a[site+'__relative_reconstruction_error'];q.append(dict(site=site,split=split,positions=len(p),median_relative_error=float(np.median(err)),min=float(err.min()),max=float(err.max()),median_h_norm=float(np.median(np.linalg.norm(a[site+'__h'],axis=1)))))
  for f in spec[site]['C']:
   fs=sorted({x['family'] for x in p})
   for kind,cc in [('far6',['nearN','nearA','nearB']),('main4',['main16','main128'])]:
    missing=[fam for fam in fs if not all(z[i,f]>0 for i,x in enumerate(p) if x['family']==fam and x['condition'] in cc)];cv.append(dict(site=site,split=split,atom=f,required_rows=kind,complete_families=12-len(missing),denominator=12,missing_families=missing))
table(R/'tables/reconstruction_quality.csv',q);table(R/'tables/common_member_coverage.csv',cv)

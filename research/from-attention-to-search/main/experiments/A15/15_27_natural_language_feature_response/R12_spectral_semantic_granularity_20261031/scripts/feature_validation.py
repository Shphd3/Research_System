from common import *
from analyze import labels,score,ba
from evaluate import boot,stats,p_boot,holm
import pickle,re
from scipy.stats import spearmanr

def main():
 a=OUT/'analysis'
 with open(OUT/'models/frozen.pkl','rb') as f:ms=pickle.load(f)
 with open(a/'evaluation_state.pkl','rb') as f:ev=pickle.load(f)
 fr=list(csv.DictReader((a/'D_feature_freeze.csv').open()));dlookup={(r['task'],int(r['feature_id'])):r for r in fr};out=[];paired=[];shape=[];lex=[]
 probes=json.load(open(a/'text_hypotheses.json'))
 for task,d in ev.items():
  z=d['z'];y=d['y'];bb=boot(y);sd=ms[task]
  for f in sd['features'][:12]:
   v=z[:,f];diff=v[y==1].mean()-v[y==0].mean();dist=v[bb[1]].mean(1)-v[bb[0]].mean(1);inter=np.quantile(dist,[.025,.975]);dp=float(dlookup[task,f]['D_mean_z_class1'])-float(dlookup[task,f]['D_mean_z_class0']);n0=int(sum(v[y==0]>0));n1=int(sum(v[y==1]>0));out.append(dict(task=task,feature_id=f,D_mean_z_difference=dp,H_mean_z_difference=float(diff),same_direction=bool(dp*diff>0),ci_low=float(inter[0]),ci_high=float(inter[1]),p=p_boot(dist),H_positive_docs0=n0,H_positive_docs1=n1,conditional_amplitude_comparison_qualified=n0>=3 and n1>=3,amplitude_identification='BOTH_CLASSES_GE3_POSITIVE_DOCS' if n0>=3 and n1>=3 else 'INSUFFICIENT;algebraic_symmetric_split_is_not_an_identified_amplitude_effect'))
  ids=sd['features'];p=sd['pairs'];prod=np.stack([(z[:,f]>0)*(z[:,g]>0) for _,f,g,_,_ in p],1).astype(float);s0=score(sd['single_aug'],z[:,ids[:12+len(p)]]);s1=score(sd['pair_aug'],np.c_[z[:,ids[:12]],prod]);b0=stats(y,s0,bb)[3];b1=stats(y,s1,bb)[3];dd=b1-b0;lo,hi=np.quantile(dd,[.025,.975]);paired.append(dict(task=task,pair_products_minus_matched_single_additions=ba(y,s1>=0)-ba(y,s0>=0),ci_low=float(lo),ci_high=float(hi),p=p_boot(dd),parameters=sd['pair_aug']['parameters'],same_parameter_count=sd['pair_aug']['parameters']==sd['single_aug']['parameters']))
  # Word/format/explanatory proxies were named in Protocol; no semantic parser claim.
  def proxies(r):
   t=r['prefix'].lower();n=max(1,len(t));return {'math_format':sum(t.count(c) for c in ['\\','$','{','}','='])/n,'newline_format':t.count('\n')/n,'conditional_if':len(re.findall(r'\bif\b',t)),'argument_because_therefore':len(re.findall(r'\b(?:because|therefore|hence|thus)\b',t)),'contrast_but_however':len(re.findall(r'\b(?:but|however|whereas)\b',t)),'cell_objects':len(re.findall(r'\b(?:cells?|membrane|mitochondria|nucleus)\b',t)),'ecology_objects':len(re.findall(r'\b(?:species|evolution|population|ecosystem|fossil)\b',t)),'algebra_objects':len(re.findall(r'\b(?:groups?|polynomial|matrix|matrices|ring|algebra)\b',t)),'analysis_objects':len(re.findall(r'\b(?:calculus|integral|derivative|fourier|differential|measure)\b',t))}
  X=[proxies(r) for r in d['rows']]
  for name in ['head','middle','tail']:
   s=d['scores']['standardized__'+name]
   for k in X[0]:
    v=np.array([r[k] for r in X]);rho,pv=spearmanr(v,s) if np.std(v)>0 else (np.nan,np.nan);shape.append(dict(task=task,band=name,proxy=k,H_spearman=float(rho) if np.isfinite(rho) else None,p=float(pv) if np.isfinite(pv) else None,documents=len(y),status='PRESPECIFIED_PROXY_EXPLORATORY;not_syntax_or_mechanism_identification'))
   probe=next(p for p in probes if p['task']==task and p['band']==name);v=np.array([sum(len(re.findall(r'\b'+re.escape(t)+r'\b',r['prefix'].lower())) for t in probe['positive_terms'])-sum(len(re.findall(r'\b'+re.escape(t)+r'\b',r['prefix'].lower())) for t in probe['negative_terms']) for r in d['rows']]);rho,pv=spearmanr(v,s) if v.std()>0 else (np.nan,np.nan);lex.append(dict(task=task,band=name,positive_D_terms=';'.join(probe['positive_terms']),negative_D_terms=';'.join(probe['negative_terms']),H_rho=float(rho) if np.isfinite(rho) else None,H_p=float(pv) if np.isfinite(pv) else None,H_documents=len(y),status='D_H_LEXICAL_ASSOCIATION_ONLY'))
 for r,q in zip(out,holm([r['p'] for r in out])):r['Holm36_p']=float(q)
 for r,q in zip(lex,holm([r['H_p'] if r['H_p'] is not None else 1 for r in lex])):r['Holm9_p']=float(q)
 table(a/'feature_preference_validation.csv',out);table(a/'pair_increment_contrasts.csv',paired);table(a/'text_proxy_checks.csv',shape);table(a/'D_H_text_lexicon_validation.csv',lex)
 print('FEATURE',[(t,sum(r['same_direction'] for r in out if r['task']==t),sum(r['Holm36_p']<.05 for r in out if r['task']==t)) for t in ev]);print('LEXICON',[(r['task'],r['band'],r['H_rho'],r['Holm9_p']) for r in lex]);print('PAIRS',paired)
if __name__=='__main__':main()

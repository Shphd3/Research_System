"""Token-position incidence, sparse coactivation graph, and coverage-aware grouping.
Grouping is fitted on a CALIBRATION panel only. An imposed K is NOT discovered class count.
"""
import argparse,json
from pathlib import Path
import numpy as np
from scipy import sparse
from scipy.sparse.csgraph import connected_components
from sklearn.cluster import SpectralClustering

def sparse_codes(indices,values,width):
    indices,values=np.asarray(indices),np.asarray(values)
    if indices.shape!=values.shape or indices.ndim!=2:
        raise ValueError("Sparse codes must have matching [N,k] arrays")
    if np.any(indices<0) or np.any(indices>=width) or np.any(values<0):
        raise ValueError("Invalid feature IDs / negative activations")
    n,k=indices.shape
    z=sparse.csr_matrix((values.reshape(-1),(np.repeat(np.arange(n),k),indices.reshape(-1))),shape=(n,width))
    z.eliminate_zeros()
    return z

def coactivation_graph(z):
    binary=z.copy().astype(np.float64);binary.data[:]=1.0
    counts=np.asarray(binary.sum(0)).ravel()
    graph=(binary.T@binary).tocsr()
    graph.setdiag(0);graph.eliminate_zeros()
    inv=1/np.sqrt(np.maximum(counts,1))
    graph=sparse.diags(inv)@graph@sparse.diags(inv)
    return graph.tocsr(),counts

def fit_groups(z,n_groups=8,min_support=20,seed=17):
    graph,counts=coactivation_graph(z)
    supported=np.flatnonzero((counts>=min_support)&(np.asarray(graph.sum(1)).ravel()>0))
    group=np.full(z.shape[1],-1,dtype=np.int64)
    if len(supported)<=n_groups:
        return group,{"status":"INSUFFICIENT_SUPPORTED_FEATURES","supported":len(supported)}
    g=graph[supported][:,supported]
    components,_=connected_components(g,directed=False)
    # Disconnectedness is recorded, never silently presented as a stable hierarchy.
    labels=SpectralClustering(n_clusters=n_groups,affinity="precomputed",assign_labels="kmeans",
                             n_init=10,random_state=seed).fit_predict(g)
    group[supported]=labels
    return group,{"status":"DIAGNOSTIC_ONLY","supported":len(supported),
                  "connected_components":int(components),"preset_groups":n_groups,
                  "incidence_unit":"single_causal_token_position","seed":seed}

def group_scores(z,group):
    if len(group)!=z.shape[1]: raise ValueError("Group map width mismatch")
    supported=np.flatnonzero(group>=0)
    k=int(group[supported].max()+1) if len(supported) else 0
    mapping=sparse.csr_matrix((np.ones(len(supported)),(supported,group[supported])),shape=(len(group),k))
    masses=(z@mapping).toarray()
    total=np.asarray(z.sum(1)).ravel()
    scores=masses/np.maximum(total[:,None],1e-12)
    return scores,scores.sum(1) # Missing mass retained, NOT normalized away.

def summarize(z,reconstruction=None,h=None):
    count=np.asarray((z>0).sum(0)).ravel()
    out={"tokens":z.shape[0],"dictionary_width":z.shape[1],"mean_L0":float(np.diff(z.indptr).mean()),
         "never_fired_on_this_panel":int((count==0).sum()),"active_feature_fraction":float((count>0).mean())}
    if h is not None and reconstruction is not None:
        h=np.asarray(h,dtype=np.float64);r=np.asarray(reconstruction,dtype=np.float64)
        den=float(((h-h.mean(0))**2).sum())
        out["residual_over_centered_variance"]=float(((r-h)**2).sum()/den) if den>0 else None
        out["mean_state_norm"]=float(np.linalg.norm(h,axis=1).mean())
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--activations",required=True)
    p.add_argument("--width",type=int,required=True);p.add_argument("--output-dir",required=True)
    p.add_argument("--fit-groups",action="store_true");p.add_argument("--calibration-confirmed",action="store_true")
    p.add_argument("--groups",type=int,default=8);p.add_argument("--min-support",type=int,default=20)
    p.add_argument("--seed",type=int,default=17)
    a=p.parse_args();out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
    with np.load(a.activations,allow_pickle=False) as f: d=dict(f)
    z=sparse_codes(d["indices"],d["values"],a.width)
    report=summarize(z,d.get("reconstruction"),d.get("h"))
    if a.fit_groups:
        if not a.calibration_confirmed: raise ValueError("Refuse fitting groups without explicit calibration confirmation")
        group,meta=fit_groups(z,a.groups,a.min_support,a.seed)
        scores,coverage=group_scores(z,group)
        np.savez_compressed(out/"groups.npz",group_ids=group,scores=scores,coverage=coverage,sample_ids=d["sample_ids"])
        report.update(grouping=meta,mean_covered_mass=float(coverage.mean()),uncovered_positions=int((coverage==0).sum()))
    (out/"statistics.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
if __name__=="__main__":main()

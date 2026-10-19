#!/usr/bin/env python3
"""Describe frozen groups. No graph construction, community detection or training.

Reads existing counts, frequencies, graph edge lists, partitions and matching.
Derived pair correlations and within-source neighbor ranks audit existing edges.
"""
from pathlib import Path
import csv
import hashlib
import itertools
import json
from collections import deque
from datetime import datetime, timezone

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import networkx as nx
import numpy as np

BASE = Path('/data/250010109/MoE_Router/experiments/20261012_qwen3_crosscoder')
OLD = BASE/'analysis/feature_frequency/20261015T143300Z'
PHASE = BASE/'analysis/feature_relation_phase1/20261013T173130Z'
OUT = BASE/'analysis/group_understanding/20261016_figures'
ND, NV = 5238097, 5247663
CASE_IDS = [87, 74, 34]
OUT.mkdir(parents=True, exist_ok=True)


def read_csv(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def write_csv(path, rows):
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(8*1024*1024), b''):
            h.update(b)
    return h.hexdigest()


def phi(joint, ni, nj, n):
    joint, ni, nj = np.asarray(joint, float), np.asarray(ni, float), np.asarray(nj, float)
    return (n*joint-ni*nj)/np.sqrt(ni*(n-ni)*nj*(n-nj))


def descriptives(vals):
    a = np.asarray(vals, float)
    return dict(count=len(a), minimum=float(a.min()), median=float(np.median(a)),
                mean=float(a.mean()), maximum=float(a.max()),
                negative_fraction=float(np.mean(a < 0)),
                nonpositive_fraction=float(np.mean(a <= 0)))


def save_fig(fig, stem):
    for ext in ['png', 'pdf', 'svg']:
        kwargs = dict(bbox_inches='tight', pad_inches=.15)
        if ext == 'png':
            kwargs['dpi'] = 190
        fig.savefig(OUT/(stem+'.'+ext), **kwargs)
    plt.close(fig)


def main():
    plt.rcParams.update({'font.size': 10, 'axes.spines.top': False,
                         'axes.spines.right': False, 'svg.fonttype': 'none',
                         'savefig.facecolor': 'white'})
    freq_rows = read_csv(OLD/'frequency.csv')
    freq = {int(r['feature_id']): r for r in freq_rows}
    n = {s: np.array([int(freq[i]['n_'+s]) for i in range(16384)]) for s in ['D','V']}
    groups = {int(g['group_id']): g for g in json.loads((OLD/'main/groups_D.json').read_text())}
    vgroups = {int(g['group_id']): g for g in json.loads((OLD/'main/groups_V.json').read_text())}
    matches = {int(r['group_D']): r for r in read_csv(OLD/'main/matches.csv')}
    edge_rows = {s: read_csv(OLD/f'main/edges_{s}.csv') for s in ['D', 'V']}
    edges = {s: {(int(r['u']),int(r['v'])):r for r in edge_rows[s]} for s in ['D','V']}
    counts = {s: np.load(PHASE/f'counts/total{i}.npy',mmap_mode='r') for i,s in enumerate(['D','V'])}
    candidate = np.load(OLD/'main/candidate_ids.npy')
    selected_stats = {}
    coverage = []
    for gid in CASE_IDS:
        members = list(groups[gid]['members'])
        mem = set(members)
        match = matches[gid]
        vgid = int(match['group_V'])
        vmembers = set(vgroups[vgid]['members'])
        retained = mem & vmembers
        assert all(counts[s][i,i] == n[s][i] for s in ['D','V'] for i in members)
        graph = nx.Graph()
        graph.add_nodes_from(members)
        for (u,v),r in edges['D'].items():
            if u in mem and v in mem:
                graph.add_edge(u,v,weight=float(r['phi']))
        # Existing edge graph only: no thresholding/reconstruction/community call.
        bridges = {tuple(sorted(e)) for e in nx.bridges(graph)}
        rank_maps = {}
        if gid == 87:
            for s,denom in [('D',ND),('V',NV)]:
                for u in members:
                    joint = np.asarray(counts[s][u,candidate])
                    correlations = phi(joint,n[s][u],n[s][candidate],denom)
                    legal = (candidate != u) & (joint >= 10) & (correlations > 0)
                    ids, values = candidate[legal],correlations[legal]
                    order = np.lexsort((ids,-values))
                    rank_maps[s,u] = {int(ids[k]):i+1 for i,k in enumerate(order)}
        pair_rows=[]
        for u,v in itertools.combinations(members,2):
            row={'group_id_D':gid,'u':u,'v':v}
            for s,denom in [('D',ND),('V',NV)]:
                joint=int(counts[s][u,v])
                p=float(phi(joint,n[s][u],n[s][v],denom))
                key=tuple(sorted((u,v)))
                row.update({f'n_u_{s}':int(n[s][u]),f'n_v_{s}':int(n[s][v]),
                            f'joint_{s}':joint,f'N_{s}':denom,f'phi_{s}':p,
                            f'edge_{s}':key in edges[s]})
                if key in edges[s]:
                    assert joint == int(edges[s][key]['joint'])
                    assert abs(p-float(edges[s][key]['phi'])) < 1e-12
                if gid == 87:
                    ru,rv=rank_maps[s,u].get(v),rank_maps[s,v].get(u)
                    row.update({f'rank_u_to_v_{s}':ru if ru is not None else 'NOT_ELIGIBLE',
                                f'rank_v_to_u_{s}':rv if rv is not None else 'NOT_ELIGIBLE'})
                    assert row[f'edge_{s}'] == (ru is not None and rv is not None and ru<=10 and rv<=10)
            row['bridge_in_frozen_D_induced_graph']=tuple(sorted((u,v))) in bridges
            pair_rows.append(row)
        write_csv(OUT/f'group_{gid:03d}_all_pairs.csv',pair_rows)
        member_rows=[]
        ordered=sorted(members,key=lambda u:(-n['D'][u],u))
        for rank,u in enumerate(ordered,1):
            externalD=sum(u in e and not (e[0] in mem and e[1] in mem) for e in edges['D'])
            member_rows.append(dict(group_id_D=gid,D_frequency_rank_within_group=rank,
                                   feature_id=u,n_D=int(n['D'][u]),N_D=ND,p_D=float(n['D'][u]/ND),
                                   n_V=int(n['V'][u]),N_V=NV,p_V=float(n['V'][u]/NV),
                                   matched_group_V=vgid,in_matched_V_group=u in vmembers,
                                   D_internal_degree=graph.degree(u),D_external_degree=externalD))
        write_csv(OUT/f'group_{gid:03d}_members_frequency_order.csv',member_rows)
        shown=members.copy()
        anchor=None
        if len(members)>30:
            anchor=min(members,key=lambda u:(-graph.degree(u),u))
            seen={anchor};queue=deque([anchor]);shown=[]
            while queue and len(shown)<30:
                u=queue.popleft();shown.append(u)
                neighbors=sorted(graph.neighbors(u),key=lambda v:(-graph[u][v]['weight'],v))
                for v in neighbors:
                    if v not in seen:
                        seen.add(v);queue.append(v)
            assert len(shown)==30
        sub=graph.subgraph(shown).copy()
        shown_edges=set(tuple(sorted(e)) for e in sub.edges())
        write_csv(OUT/f'group_{gid:03d}_displayed_nodes.csv',[
            dict(group_id_D=gid,feature_id=u,display_order=i+1,in_matched_V_group=u in retained,
                 D_degree_full_group=graph.degree(u),D_degree_display=sub.degree(u))
            for i,u in enumerate(shown)])
        write_csv(OUT/f'group_{gid:03d}_displayed_edges.csv',[
            dict(group_id_D=gid,u=u,v=v,phi_D=float(edges['D'][(u,v)]['phi']),
                 present_in_V_graph=(u,v) in edges['V'],
                 bridge_in_full_D_group=(u,v) in bridges)
            for u,v in sorted(shown_edges)])
        cov=dict(group_id_D=gid,total_members=len(members),displayed_nodes=len(shown),
                 total_internal_D_edges=graph.number_of_edges(),displayed_D_edges=sub.number_of_edges(),
                 displayed_edge_fraction=sub.number_of_edges()/graph.number_of_edges(),
                 selection='all members' if anchor is None else
                 '30-node BFS: maximum internal-degree anchor (lowest feature ID breaks ties); neighbors ordered by descending existing D phi, then feature ID; induced existing edges only',
                 anchor_feature_id=anchor if anchor is not None else 'NOT_APPLICABLE',
                 external_edges_shown=False,frequency_plot_members=len(members))
        coverage.append(cov)
        pair_edgeD=[r for r in pair_rows if r['edge_D']]
        pair_nonedgeD=[r for r in pair_rows if not r['edge_D']]
        stat=dict(group_id_D=gid,size=len(members),matched_group_V=vgid,
                  matched_group_V_size=len(vmembers),intersection=len(retained),
                  jaccard=float(match['jaccard']),D_member_retention=len(retained)/len(members),
                  added_V_members=len(vmembers-mem),missing_from_matched_V=sorted(mem-vmembers),
                  D_density=nx.density(graph),D_internal_edges=graph.number_of_edges(),
                  D_components=nx.number_connected_components(graph),
                  D_bridges=sorted(map(list,bridges)),D_articulation_points=sorted(nx.articulation_points(graph)),
                  edge_D_retained_in_V=sum(r['edge_V'] for r in pair_edgeD)/len(pair_edgeD),
                  D_frequency_min=min(float(freq[u]['p_D']) for u in members),
                  D_frequency_max=max(float(freq[u]['p_D']) for u in members),
                  D_frequency_max_min_ratio=max(n['D'][members])/min(n['D'][members]),
                  V_frequency_min=min(float(freq[u]['p_V']) for u in members),
                  V_frequency_max=max(float(freq[u]['p_V']) for u in members),
                  phi_all_pairs={s:descriptives([r['phi_'+s] for r in pair_rows]) for s in ['D','V']},
                  phi_existing_D_edges={s:descriptives([r['phi_'+s] for r in pair_edgeD]) for s in ['D','V']},
                  phi_D_nonedges={s:descriptives([r['phi_'+s] for r in pair_nonedgeD]) for s in ['D','V']},
                  boundary='Descriptive conditional on fixed D group; one exposed D/V split does not establish permanent membership, semantics, causality, or learning compatibility.')
        selected_stats[str(gid)]=stat
        # Relationship plot: actual edges only, not all positive-phi pairs.
        fig,ax=plt.subplots(figsize=(9.4,6.7 if gid!=34 else 7.7))
        if gid==87:
            pos={800:(-.9,.5),14514:(-.9,-.5),15978:(.35,0),1572:(1.75,0)}
        else:
            pos=nx.spring_layout(sub,seed=20261016,weight='weight',iterations=700,k=1.5/np.sqrt(len(shown)))
            # Separate labels in dense cores without altering nodes or edges.
            node_order=list(sub.nodes)
            xy=np.asarray([pos[u] for u in node_order])
            xy=xy/(np.ptp(xy,axis=0).max()/2)
            minimum_separation=.24 if gid==74 else .19
            for _ in range(180):
                for i in range(len(xy)):
                    for j in range(i):
                        delta=xy[i]-xy[j]
                        distance=float(np.linalg.norm(delta))
                        if distance<minimum_separation:
                            direction=delta/max(distance,1e-12)
                            move=.51*(minimum_separation-distance)*direction
                            xy[i]+=move;xy[j]-=move
            pos={u:xy[i] for i,u in enumerate(node_order)}
        retained_edges=[e for e in sub.edges if tuple(sorted(e)) in edges['V']]
        changed_edges=[e for e in sub.edges if tuple(sorted(e)) not in edges['V']]
        maxphi=max(d['weight'] for _,_,d in sub.edges(data=True))
        for edge_list,color,style in [(retained_edges,'#596b7a','solid'),(changed_edges,'#a26032','dashed')]:
            # Use ordinary data-coordinate lines: this installed NetworkX 2.6 /
            # Matplotlib pairing adds an incorrect display offset to collections.
            for u,v in edge_list:
                ax.plot([pos[u][0],pos[v][0]],[pos[u][1],pos[v][1]],
                        color=color,linestyle=style,
                        linewidth=1+3.5*sub[u][v]['weight']/maxphi,alpha=.8,zorder=1)
        nx.draw_networkx_nodes(sub,pos,ax=ax,node_size=1100 if gid==87 else 780 if gid==74 else 610,
            node_color=['#b9d9ef' if u in retained else '#f5c7a4' for u in sub.nodes],
            linewidths=1.2,edgecolors='#374957')
        nx.draw_networkx_labels(sub,pos,ax=ax,font_size=10 if gid==87 else 8,font_weight='bold')
        if gid==87:
            nx.draw_networkx_edge_labels(sub,pos,ax=ax,
                edge_labels={e:f"phi={sub[e[0]][e[1]]['weight']:.3f}" for e in sub.edges},
                font_size=9,rotate=False,bbox=dict(facecolor='white',edgecolor='none',alpha=.95))
        title=f'Group D{gid}: {len(shown)}/{len(members)} members; {sub.number_of_edges()}/{graph.number_of_edges()} internal D edges'
        ax.set_title(title,fontsize=14,pad=15)
        legend=[Line2D([0],[0],marker='o',color='none',markerfacecolor='#b9d9ef',markeredgecolor='#374957',markersize=10,label=f'In matched V{vgid}'),
                Line2D([0],[0],marker='o',color='none',markerfacecolor='#f5c7a4',markeredgecolor='#374957',markersize=10,label=f'Outside matched V{vgid}'),
                Line2D([0],[0],color='#596b7a',lw=2,label='D edge also in V graph'),
                Line2D([0],[0],color='#a26032',lw=2,ls='--',label='D edge absent from V graph')]
        ax.legend(handles=legend,loc='upper center',bbox_to_anchor=(.5,-.025),ncol=2,frameon=False,fontsize=9)
        ax.text(.5,-.16,'Widths show D phi. Positions aid reading; spatial distance is not a measured similarity.\n'
                +('All members shown. Existing within-group edges only; outside edges omitted.' if gid!=34 else
                  f'PARTIAL SUBGRAPH: 30 of 149 members. Anchor {anchor}; deterministic BFS. Outside edges omitted.'),
                transform=ax.transAxes,ha='center',va='top',fontsize=8.6)
        # NetworkX 2.6 / this Matplotlib build overestimates LineCollection data
        # limits by display offsets. Set bounds from the actual layout explicitly.
        xy=np.asarray([pos[u] for u in sub.nodes])
        lo,hi=xy.min(axis=0),xy.max(axis=0)
        span=np.maximum(hi-lo,.2)
        margin=.23 if gid==87 else .15
        ax.set_xlim(lo[0]-margin*span[0],hi[0]+margin*span[0])
        ax.set_ylim(lo[1]-margin*span[1],hi[1]+margin*span[1])
        ax.axis('off')
        fig.subplots_adjust(bottom=.23)
        save_fig(fig,f'group_{gid:03d}_relations')
        # Complete member frequencies in every case, including the large case.
        fig,ax=plt.subplots(figsize=(9.4,4.9))
        xx=np.arange(len(ordered)); pd=np.array([n['D'][u]/ND*100 for u in ordered]);pv=np.array([n['V'][u]/NV*100 for u in ordered])
        if gid!=34:
            ax.bar(xx-.19,pd,.38,label=f'D (N={ND:,})',color='#2d79ae')
            ax.bar(xx+.19,pv,.38,label=f'V (N={NV:,})',color='#df8c39')
            ax.set_xticks(xx);ax.set_xticklabels(ordered,rotation=45 if gid==74 else 0,ha='right' if gid==74 else 'center')
            ax.set_xlabel('Feature ID, ordered by decreasing D frequency')
            if gid==74:ax.set_yscale('log')
        else:
            ax.plot(xx+1,pd,color='#2d79ae',label=f'D (N={ND:,})',lw=1.7)
            ax.plot(xx+1,pv,color='#df8c39',label=f'V (N={NV:,})',lw=1.4,alpha=.9)
            ax.set_xlabel('Member rank by decreasing D frequency (all 149 members; IDs in linked table)')
            ax.set_yscale('log');ax.set_xlim(1,149)
        ax.set_ylabel('Activation frequency (%)'+ ('; log scale' if gid!=87 else ''))
        ax.set_title(f'Group D{gid}: all {len(members)} member frequencies',fontsize=14)
        ax.grid(axis='y',alpha=.2);ax.legend(frameon=False,fontsize=9)
        ax.text(.5,-.31 if gid==74 else -.25,
                'Same frozen activation rule in D and V. A shared group does not require similar marginal frequency.\n'
                f'D frequency range: {pd.min():.5g}% to {pd.max():.5g}% ({pd.max()/pd.min():.2f}x).',
                transform=ax.transAxes,ha='center',va='top',fontsize=9)
        fig.subplots_adjust(bottom=.29 if gid==74 else .25)
        save_fig(fig,f'group_{gid:03d}_frequencies')
        (OUT/f'group_{gid:03d}_statistics.json').write_text(json.dumps(stat,indent=2)+'\n')
        print('CASE_COMPLETE',gid,flush=True)
    write_csv(OUT/'graph_coverage.csv',coverage)
    (OUT/'case_statistics.json').write_text(json.dumps(selected_stats,indent=2)+'\n')
    sources=[OLD/'frequency.csv', OLD/'main/groups_D.json', OLD/'main/groups_V.json',OLD/'main/matches.csv',
             OLD/'main/edges_D.csv',OLD/'main/edges_V.csv',OLD/'main/candidate_ids.npy',
             PHASE/'counts/total0.npy',PHASE/'counts/total1.npy',Path(__file__)]
    manifest=dict(created_at_utc=datetime.now(timezone.utc).isoformat(),
        scope='Read-only reuse; existing partitions and graph edges unchanged. Pair phi and graph summaries are descriptive derivatives.',
        pair_definition='Binary feature activation event at a token position; phi=(N*n_ij-n_i*n_j)/sqrt(n_i*(N-n_i)*n_j*(N-n_j)).',
        rank_audit='Only group D87: fixed candidate pool; joint>=10; positive phi; descending phi then ascending feature ID. No graph or community reconstruction.',
        graph_coverage='graph_coverage.csv',input_access_receipt=str(BASE/'analysis/group_understanding/20261016_input_access.json'),
        sources=[dict(path=str(p),size_bytes=p.stat().st_size,sha256=sha256(p)) for p in sources],
        figures=[dict(path=str(p),size_bytes=p.stat().st_size,sha256=sha256(p)) for p in sorted(OUT.glob('*.png'))],
        dependencies=dict(numpy=np.__version__,matplotlib=matplotlib.__version__,networkx=nx.__version__))
    (OUT/'source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('ALL_COMPLETE',flush=True)


if __name__=='__main__':
    main()

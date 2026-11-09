from common import *
T=Tokenizer();out=[]
for r in rows(OLD/"data/documents.jsonl"):
 if r["domain"] not in LEAVES or r["topic"] not in LEAVES[r["domain"]]:continue
 ids=r["token_ids"];p=[i for i in range(96,192) if ids[i]==279];q=[i for i in range(96,192) if ids[i] in [279,315,323,311]]
 for panel,positions in [("the",p),("multi",q)]:
  if not positions:continue
  t=positions[-1];x={k:r.get(k) for k in ["seq_id","domain","topic","split","document_family","platform_family","source_stratum","genre","url","formula_present","markup_present","heading_present"]};x.update(panel=panel,position=t,token_id=ids[t],prefix=T.decode(ids[:t+1]),following=T.decode(ids[t+1:]),eligible=True,label_review="INHERITED_ACTIVATION_BLIND_AI_TOPIC_PENDING_VISIBLE_PREFIX_CHECK");out.append(x)
(OUT/"data/selected_metadata.jsonl").write_text("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in out))
cc=[]
for panel in ["the","multi"]:
 for d in LEAVES:
  for topic in LEAVES[d]:
   for s in ["discovery","development","heldout"]:
    a=[r for r in out if r["panel"]==panel and r["topic"]==topic and r["split"]==s];cc.append(dict(panel=panel,topic=topic,split=s,documents=len(a),positions=len(a)))
table(OUT/"data/coverage_before_label_review.csv",cc)
print(json.dumps(cc,indent=2))
print("DISCOVERY VISIBLE PREFIXES")
for r in out:
 if r["panel"]=="the" and r["split"]=="discovery":print("\n",r["seq_id"],r["topic"],r["platform_family"],"POS",r["position"],"\n",r["prefix"])

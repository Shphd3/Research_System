from pathlib import Path
import json,itertools,hashlib,shutil,zipfile
import numpy as np,pandas as pd
from scipy.sparse import load_npz
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
R=Path(__file__).resolve().parent;S=R.parents[1]/'S06_semantic_hierarchy_1104';font='/data/250010109/Research_System/daily_research_reports/backup/2026/09/0921/report_assets/fonts/NotoSansCJKsc-Regular.otf';fp=lambda s:FontProperties(fname=font,size=s)
panel=[json.loads(x) for x in open(S/'data/panel.jsonl')];z=load_npz(S/'data/ATTN_SAE_all_z_csr.npz');labels=['animal','cat','dog'];names=['动物 animal','猫 cat','狗 dog'];raw=[];sets=[]
for lab in labels:
 i=next(i for i,p in enumerate(panel) if p['id']==f'S06_F09_explicit_{lab}');p=panel[i];row=z.getrow(i);ss={int(f) for f,v in zip(row.indices,row.data) if v>0};assert len(ss)==32;sets.append(ss);raw.append({k:p[k] for k in ['id','prefix','category_phrase','target_index_zero_based','target_token_id']})
common=set.intersection(*sets);union=set.union(*sets);order=sorted(union,key=lambda f:(-sum(f in s for s in sets),tuple(-int(f in s) for s in sets),f));cols=[dict(column=j+1,feature_id=f,animal=int(f in sets[0]),cat=int(f in sets[1]),dog=int(f in sets[2])) for j,f in enumerate(order)];pd.DataFrame(cols).to_csv(R/'member_coordinates.csv',index=False)
comparisons=[]
for i,j in [(0,1),(0,2),(1,2)]:
 a,b=sets[i],sets[j];comparisons.append(dict(pair=labels[i]+'–'+labels[j],intersection=len(a&b),union=len(a|b),Jaccard=len(a&b)/len(a|b),only_first=len(a-b),only_second=len(b-a)))
pd.DataFrame(comparisons).to_csv(R/'pair_overlaps.csv',index=False);(R/'original_texts.json').write_text(json.dumps(raw,ensure_ascii=False,indent=2)+'\n');print('shared_all',len(common),'union',len(union));print(comparisons)
fig=plt.figure(figsize=(12.8,5.8),facecolor='white');ink='#202936';blue='#2B668E';gray='#E9EDF1'
fig.text(.5,.98,'动物、猫、狗的激活成员对比',va='top',ha='center',fontproperties=fp(23),color=ink)
fig.text(.5,.884,'F09 显式留出样本  |  Attention 输出 SAE  |  每句激活 32 个成员',ha='center',fontproperties=fp(12),color='#56616E')
ax=fig.add_axes([.14,.48,.80,.27]);arr=np.array([[int(f in s) for f in order] for s in sets]);ax.imshow(arr,cmap=ListedColormap([gray,blue]),vmin=0,vmax=1,aspect='auto',interpolation='nearest');ax.set_yticks(range(3),names,fontproperties=fp(14));ax.set_xticks([]);ax.tick_params(axis='y',length=0,pad=12);ax.set_xticks(np.arange(-.5,len(order),1),minor=True);ax.set_yticks(np.arange(-.5,3,1),minor=True);ax.grid(which='minor',color='white',linewidth=.8);ax.tick_params(which='minor',bottom=False,left=False)
for p in ax.spines.values():p.set_visible(False)
ax.axvline(len(common)-.5,color='white',lw=3);ax.text((len(common)-1)/2,-.88,f'三者共同：{len(common)} 个',ha='center',fontproperties=fp(12),color=blue,clip_on=False);ax.text((len(common)+len(order)-1)/2,-.88,'其余成员',ha='center',fontproperties=fp(12),color='#56616E',clip_on=False)
fig.text(.54,.425,f'同一列代表同一 feature，共展示 {len(union)} 个并集成员',ha='center',fontproperties=fp(11),color='#56616E')
fig.legend(handles=[Patch(facecolor=blue,label='激活'),Patch(facecolor=gray,label='未激活')],loc='center',bbox_to_anchor=(.54,.375),ncol=2,frameon=False,prop=fp(11))
tax=fig.add_axes([.14,.19,.80,.14]);tax.axis('off');table=tax.table(cellText=[[str(c['intersection'])+' / '+str(c['union']) for c in comparisons],[f"{c['Jaccard']:.3f}" for c in comparisons]],colLabels=['animal–cat','animal–dog','cat–dog'],rowLabels=['交集 / 并集','Jaccard'],cellLoc='center',rowLoc='center',bbox=[0,0,1,1]);table.auto_set_font_size(False)
for (r,c),cell in table.get_celld().items():
 cell.set_text_props(fontproperties=fp(11.5),color=ink);cell.set_facecolor('white');cell.set_edgecolor('#D7DDE3');cell.set_linewidth(.6)
 if r==0:cell.set_facecolor('#F4F6F8')
fig.text(.5,.095,'相同句式中的类别短语分别为 an animal、a cat、a dog；读取位置均为 Description: 的末尾冒号。',ha='center',fontproperties=fp(10.5),color='#56616E')
fig.text(.5,.045,'颜色只表示激活 / 未激活，不表示激活幅值；冠词也随类别短语变化。',ha='center',fontproperties=fp(10.5),color='#56616E')
fig.savefig(R/'F09_animal_cat_dog_simple.png',dpi=240)
with plt.rc_context({'svg.fonttype':'none'}):fig.savefig(R/'F09_animal_cat_dog_simple.svg')
with plt.rc_context({'svg.fonttype':'path'}):fig.savefig(R/'F09_animal_cat_dog_simple_outlined.svg')
fig.savefig(R/'F09_animal_cat_dog_simple.pdf');plt.close(fig)
(R/'README_cn.md').write_text('''# 可选实例图：动物、猫、狗（简洁版）\n\n本版只展示原F09的二值成员集合，不展示激活幅值。蓝色激活、浅灰未激活；同一列是同一个feature，先排三者共同成员，再按剩余二值模式分组。所有feature ID在member_coordinates.csv，不在主图逐个标注，以保持投影简洁。配对统计和原文分别在pair_overlaps.csv、original_texts.json。\n\n这是可选展示稿，尚未插入或替换主报告；“同一大类内部的组合更相似”可由已有总体表格呈现。本图只辅助说明一组具体文本。PNG用于预览；SVG文字可编辑，outlinedSVG/PDF用于保真插入。原S06与上一版图不变。\n''')
dest=Path('/data/250010109/Research_System/daily_research_reports/1104/meeting_report/sae_conclusion1_assets/optional_v2');dest.mkdir(parents=True,exist_ok=True)
for p in R.iterdir():
 if p.is_file():shutil.copy2(p,dest/p.name)
zip_path=dest.parent.parent.parent/'20261104_SAE_F09_optional_v2.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as zz:
 for p in R.iterdir():
  if p.is_file():zz.write(p,p.name)
with zipfile.ZipFile(zip_path) as zz:assert zz.testzip() is None
print('DELIVERED',dest,'ZIP',zip_path)

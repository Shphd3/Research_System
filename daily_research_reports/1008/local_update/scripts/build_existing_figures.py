#!/usr/bin/env python3
"""Render only existing local-update evidence; no model load, training, or GPU.

Usage: python build_existing_figures.py --font /path/to/NotoSansCJKsc-Regular.otf
The font is a runtime dependency and is never copied into the repository.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LogNorm, TwoSlopeNorm
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits

HERE = Path(__file__).resolve().parents[1]
FIG = HERE / "figures"
EVI = HERE / "evidence"
NAT = Path("/data/250010109/MoE_Router/experiments/20261002_s7_representation_update_channels")
CTRL = Path("/data/250010109/MoE_Router/experiments/20260927_common_rule_controlled/runs/full_h100_20260928T010310Z")
OLD = Path("/data/250010109/MoE_Router/experiments/20260930_ntp_statistics_local_compatibility/runs/full_initial")
DOMAINS = ["computer_science", "mathematics", "physics", "biology"]
CN = {"computer_science": "计算机科学", "mathematics": "数学", "physics": "物理", "biology": "生物"}
SHORT = {"computer_science": "计", "mathematics": "数", "physics": "物", "biology": "生"}
COLORS = {"same": "#246B9B", "flip": "#C05E2C", "common": "#246B9B", "random31": "#C05E2C"}
EXPECT = {
    "runs/finite_panel_01/finite_panel_summary.csv": "cb206ef355903aa82d1e63933707c144b2694a6f5f38d6454f8c27afae09e8df",
    "runs/sae_displacement_01/endpoint_summary.csv": "ff9a5a0894fd7d4463d0fef8eb2d2cc6baea7944525e79ca6ea1f9ccac95b155",
    "runs/sae_displacement_01/finite_two_component_attribution.csv": "e60803324aa8e86a6e29813e42848b5cce4c79a34824633a8edb9887211ce9cf",
}


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(8 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def save(fig, name, footer):
    fig.text(.02, .015, footer, fontsize=10, ha="left", va="bottom", color="#425466")
    fig.subplots_adjust(bottom=.25, top=.82, wspace=.64)
    for suffix in ["png", "svg"]:
        fig.savefig(FIG / f"{name}.{suffix}", dpi=180, facecolor="white", bbox_inches="tight")
    plt.close(fig)


def heat(ax, values, xlabels, ylabels, title, label, *, norm=None, cmap="RdBu_r", fmt=".3f"):
    im = ax.imshow(values, cmap=cmap, norm=norm, aspect="auto")
    ax.set_xticks(np.arange(len(xlabels)), xlabels)
    ax.set_yticks(np.arange(len(ylabels)), ylabels)
    ax.set_title(title, pad=10, fontsize=14)
    ax.set_xticks(np.arange(-.5, len(xlabels), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(ylabels), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="minor", bottom=False, left=False)
    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            rgb=plt.get_cmap(cmap)(im.norm(values[i,j]))[:3]
            luminance=.2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2]
            color="white" if luminance<.49 else "#102A43"
            ax.text(j, i, format(values[i,j], fmt), ha="center", va="center", color=color, fontsize=13)
    cb = ax.figure.colorbar(im, ax=ax, fraction=.055, pad=.04)
    cb.set_label(label, fontsize=11)
    if isinstance(norm,LogNorm) and norm.vmin < 1 < norm.vmax:
        cb.ax.axhline(1,color="#4A5568",ls="--",lw=1)
    return im


def controlled():
    conditions = pd.read_csv(CTRL / "analysis/primary_by_condition.csv")
    verdict = json.loads((CTRL / "analysis/verdict.json").read_text())
    family = pd.read_csv(CTRL / "analysis/primary_by_family.csv")
    rows = []
    for step in [1e-4, 5e-5]:
        suffix = "1e-04" if step == 1e-4 else "5e-05"
        for rho, level in [(0.1, "low"), (0.8, "high")]:
            for rule in ["same", "flip"]:
                key = f"{level}_{rule}_{suffix}"
                m = np.isclose(conditions.step, step) & np.isclose(conditions.rho, rho) & (conditions.rule == rule)
                mean = conditions.loc[m, "B_I"].mean()
                assert abs(mean-verdict["point"][key]) < 1e-14
                lo, hi = verdict["interval_95"][key]
                rows.append(dict(relative_parameter_step=step, signal_direction_inner_product=rho, answer_rule=rule,
                                 mean_finite_loss_delta_nat=mean, interval95_low_nat=lo, interval95_high_nat=hi,
                                 direction_families=12, source_repeats_per_family=int(conditions.loc[m,"source_repeat"].nunique()), condition_rows=int(m.sum()),
                                 unit="nat/target", interval_type="paired hierarchical bootstrap; 2000 draws; 12 direction families",
                                 source_run=str(CTRL), source_value_column="B_I"))
    frame = pd.DataFrame(rows)
    frame.to_csv(EVI / "controlled_cells.csv", index=False)
    effects=[]
    for step in [1e-4,5e-5]:
        suffix="1e-04" if step==1e-4 else "5e-05"
        cells=frame[np.isclose(frame.relative_parameter_step,step)].set_index(["signal_direction_inner_product","answer_rule"])
        low=cells.loc[(.1,"flip"),"mean_finite_loss_delta_nat"]-cells.loc[(.1,"same"),"mean_finite_loss_delta_nat"]
        high=cells.loc[(.8,"flip"),"mean_finite_loss_delta_nat"]-cells.loc[(.8,"same"),"mean_finite_loss_delta_nat"]
        M=high-low
        assert abs(M-verdict["point"]["M_"+suffix])<1e-14
        effects.append(dict(relative_parameter_step=step, low_rule_difference_nat=low, high_rule_difference_nat=high,
                            interaction_M_nat=M, interval95_low_nat=verdict["interval_95"]["M_"+suffix][0],
                            interval95_high_nat=verdict["interval_95"]["M_"+suffix][1],
                            definition="M=(I_high_flip-I_high_same)-(I_low_flip-I_low_same)", unit="nat/target"))
    effect=pd.DataFrame(effects)
    effect.to_csv(EVI/"controlled_rule_interaction.csv",index=False)
    fig, axes=plt.subplots(1,3,figsize=(15,5.0),gridspec_kw={"width_ratios":[1,1,1.12]})
    fig.suptitle("受控模型：信号重合放大答案规则的作用差异，四格仍平均降损",fontsize=20,x=.50,y=.98)
    norm=TwoSlopeNorm(vmin=-7.0,vcenter=0,vmax=7.0)
    for ax,step,label in zip(axes[:2],[1e-4,5e-5],["ε＝10⁻⁴","ε＝5×10⁻⁵"]):
        f=frame[np.isclose(frame.relative_parameter_step,step)]
        vals=np.array([[float(f[(f.signal_direction_inner_product==rho)&(f.answer_rule==rule)].mean_finite_loss_delta_nat.iloc[0])*1000 for rule in ["same","flip"]] for rho in [.1,.8]])
        heat(ax,vals,["规则保持","规则翻转"],["ρ＝0.1","ρ＝0.8"],label,"平均 I（10⁻³ nat／目标）",norm=norm,fmt=".4f")
    vals=np.array([[effect.iloc[j][field]*1e4 for j in range(2)] for field in ["low_rule_difference_nat","high_rule_difference_nat"]])
    heat(axes[2],vals,["ε＝10⁻⁴","ε＝5×10⁻⁵"],["ρ＝0.1","ρ＝0.8"],"翻转减保持：规则差异","差值（10⁻⁴ nat／目标）",norm=TwoSlopeNorm(vmin=-1.6,vcenter=0,vmax=1.6),fmt=".4f")
    save(fig,"main01_controlled_heatmap","ρ 是任务信号方向内积，不是共享参数／SAE 原子比例；高低条件同时改变 A、B。12 个方向族，局部一步更新。\n规则交互 M：1.5206×10⁻⁴［1.3617, 1.6722］×10⁻⁴；半步：0.7603×10⁻⁴［0.6808, 0.8362］×10⁻⁴。")
    fig,axes=plt.subplots(1,2,figsize=(13,5.5))
    fig.suptitle("辅助图 1：答案规则改变下降幅度，未产生平均净增损",fontsize=20,y=.98)
    for ax,step,label in zip(axes,[1e-4,5e-5],["ε＝10⁻⁴","ε＝5×10⁻⁵"]):
        f=frame[np.isclose(frame.relative_parameter_step,step)]
        ax.axhline(0,color="#6B7280",lw=1.2)
        for rule,name in [("same","保持规则"),("flip","翻转规则")]:
            sub=f[f.answer_rule==rule].sort_values("signal_direction_inner_product")
            y=sub.mean_finite_loss_delta_nat.values*1000
            err=np.vstack([y-sub.interval95_low_nat.values*1000,sub.interval95_high_nat.values*1000-y])
            ax.errorbar([.1,.8],y,yerr=err,fmt="o-",color=COLORS[rule],label=name,markersize=7,capsize=5)
        ax.set_ylim(-7.2 if step==1e-4 else -3.7,.2)
        ax.set_xlim(0,.9);ax.set_xticks([.1,.8]);ax.set_xlabel("任务信号方向内积 ρ")
        ax.set_ylabel("平均 I（10⁻³ nat／目标）");ax.set_title(label);ax.legend(loc="center right")
        inset=ax.inset_axes([.12,.55,.45,.32])
        for rule in ["same","flip"]:
            sub=f[f.answer_rule==rule].sort_values("signal_direction_inner_product")
            y=sub.mean_finite_loss_delta_nat.values*1000
            err=np.vstack([y-sub.interval95_low_nat.values*1000,sub.interval95_high_nat.values*1000-y])
            inset.errorbar([.1,.8],y,yerr=err,fmt="o-",color=COLORS[rule],markersize=4,capsize=3)
        inset.set_xticks([.1,.8]);inset.tick_params(labelsize=9);inset.set_title("局部放大：同一单位",fontsize=10)
    save(fig,"aux01_controlled_lines","实线仅连接两个已测条件，不是连续响应曲线。区间为已有 2,000 次配对层级 bootstrap；没有新统计检验。\nρ 非 SAE 重合比例；主坐标保留 I＝0。规则交互 M 与总损失变化 I 的符号必须分开。")
    return frame,effect


def natural():
    allrows=pd.read_csv(NAT/"runs/finite_panel_01/finite_panel_summary.csv")
    eta=json.loads((NAT/"runs/finite_panel_01/receipt.json").read_text())["eta"]
    f=allrows[allrows.part=="readout"].copy()
    f["eta"]=np.where(f.step=="full_step",eta,eta/2)
    f["positions_per_record"]=16
    f["event_count"]=f.records*16
    f["deadband_nat"]=1e-5
    f["source_batch"]= "F_half0; 512 records total; 128/source; 16 positions/record"
    f["source_gradients_sha256"]=sha(NAT/"runs/cache_audit_01/source_mean_gradients.npy")
    f["unit"]="nat/target; event fractions in [0,1]"
    f["interval_type"]="95% fixed-source category-stratified record bootstrap; 2000 draws"
    f.to_csv(EVI/"natural_cells_full_and_half.csv",index=False)
    full=f[f.step=="full_step"].copy()
    full.to_csv(EVI/"natural_cells_main16.csv",index=False)
    order={(s,t):i*4+j for i,s in enumerate(DOMAINS) for j,t in enumerate(DOMAINS)}
    full=full.assign(order=[order[(s,t)] for s,t in zip(full.source,full.target)]).sort_values("order")
    mean=full.mean_delta_loss.values.reshape(4,4)*1000
    adverse=full.event_adverse_fraction_gt_1e_5.values.reshape(4,4)*100
    assert np.all(mean<0)
    fig,axes=plt.subplots(1,2,figsize=(12.4,5.8))
    fig.suptitle("自然文本：四类来源均降低领域平均损失，但逐位置后果有差异",fontsize=20,y=.99)
    labels=[CN[s] for s in DOMAINS]
    heat(axes[0],mean,labels,labels,"平均有限损失变化","I（10⁻³ nat／目标）",norm=TwoSlopeNorm(vmin=-2.05,vcenter=0,vmax=2.05),fmt=".3f")
    heat(axes[1],adverse,labels,labels,"增损位置比例：I＞10⁻⁵ nat","全部位置中比例（%）",norm=plt.Normalize(0,60),cmap="YlOrRd",fmt=".2f")
    for ax in axes:ax.set_xlabel("接收域 B");ax.set_ylabel("来源更新 A")
    save(fig,"main02_natural_loss_heatmap",f"同一 S7 检查点；η＝{eta:.8f}；每格 256 条接收记录 × 16 位置（4,096 事件）；源每域 128 条。\n均值 16 格全负；这些已曝光记录仅支持固定源条件下的探索性局部测量。半步数据单独保存，不混合。")
    fig,axes=plt.subplots(1,2,figsize=(15,6))
    fig.suptitle("辅助图 2：领域平均下降与部分位置增损并存",fontsize=20,y=.98)
    x=np.arange(16);labels=[f"{SHORT[s]}→{SHORT[t]}" for s,t in zip(full.source,full.target)]
    y=full.mean_delta_loss.values*1000
    err=np.vstack([y-full.conditional_lo.values*1000,full.conditional_hi.values*1000-y])
    axes[0].errorbar(x,y,yerr=err,fmt="o",color=COLORS["same"],capsize=4,markersize=6)
    axes[0].axhline(0,color="#667085",lw=1.2);axes[0].set_ylabel("平均 I（10⁻³ nat／目标）")
    axes[0].set_title("固定源条件下，16 格区间均低于零")
    axes[1].bar(x,full.event_adverse_fraction_gt_1e_5*100,color=COLORS["flip"],label="增损：I＞10⁻⁵")
    axes[1].bar(x,full.event_unresolved_fraction_1e_5*100,color="#A3AAB3",label="符号未定：|I|≤10⁻⁵")
    axes[1].set_ylim(0,60);axes[1].set_ylabel("全部位置中比例（%）");axes[1].set_title("增损比例与符号未定比例分别计数");axes[1].legend(loc="upper right",fontsize=10)
    for ax in axes:
        ax.set_xticks(x,labels,rotation=55);ax.set_xlabel("源域→接收域（计：计算机科学；数：数学；物：物理；生：生物）",fontsize=10)
        for xx in [3.5,7.5,11.5]:ax.axvline(xx,color="#DFE4EA",lw=1)
        ax.grid(axis="y",alpha=.2)
    save(fig,"aux02_natural_mean_adverse","使用完整步长，16 格每格 4,096 位置；区间为已有 95% 固定源、分层按记录 bootstrap。\n区间不含源重采样、重新拟合或论文聚类不确定性；同域／跨域标签不能预先替代是否冲突。")
    return f


def sae():
    endpoint=pd.read_csv(NAT/"runs/sae_displacement_01/endpoint_summary.csv")
    components=pd.read_csv(NAT/"runs/sae_displacement_01/finite_two_component_attribution.csv")
    qualification=json.loads((NAT/"runs/sae_displacement_01/qualification.json").read_text())
    ep=endpoint[endpoint.target=="pooled"].copy()
    ep["ratio_definition"]="sum(||delta_a-D delta_alpha||^2)/sum(||delta_a||^2) within stratum"
    ep["aggregation"]="ratio of pooled energies; NOT mean of per-event ratios"
    ep["records_all"]=64;ep["positions_per_record"]=16
    ep.to_csv(EVI/"sae_endpoint_pooled.csv",index=False)
    cp=components[components.target=="pooled"].copy()
    cp["rank"]=32;cp["records"]=64;cp["events"]=1024;cp["deadband_nat"]=1e-5
    cp["fraction_definition"]="mean((phi_P>1e-5)&(I< -1e-5)) over ALL positions"
    cp["component_definition"]="phi_P=(I_P+I-I_R)/2"
    cp["random31_field_note"]="random31 is the historical seed-name; actual projection takes 32 columns"
    cp.to_csv(EVI/"sae_component_pooled.csv",index=False)
    pd.DataFrame([dict(mean_static_relative_squared_error=qualification["static_relative_squared_error_mean"],
                       median_static_relative_squared_error=qualification["static_relative_squared_error_median"],
                       events=1024,records=64,definition="mean over events of ||r||^2/||a||^2",unit="dimensionless")]).to_csv(EVI/"sae_static_reconstruction.csv",index=False)
    fig,axes=plt.subplots(1,2,figsize=(13,5.8))
    fig.suptitle("SAE 位移审计：稳定集合仍遗漏位移；集合切换产生大的重构差分",fontsize=20,y=.99)
    strata=["stable_support","all","changed_support"]
    for ax,step,label in zip(axes,["full_step","half_step"],["完整步长","半步长"]):
        values=np.array([[ep[(ep.source==s)&(ep.step==step)&(ep.stratum==st)].dynamic_pooled_rse.iloc[0] for st in strata] for s in DOMAINS])
        heat(ax,values,["集合稳定","全部位置","仅集合切换"],[CN[s] for s in DOMAINS],label,"汇总残差能量／位移能量",norm=LogNorm(.9,4000),cmap="YlOrRd",fmt=".3g")
        ax.set_xlabel("按更新前后 SAE 激活集合分层");ax.set_ylabel("来源更新")
    save(fig,"main03_sae_fidelity_heatmap","64 条记录 × 16 位置；全部 30,000 坐标端点，TopK32。颜色采用对数刻度；比值 1 表示残差能量等于真实位移能量。\n表内数值是能量总和之比，不是逐事件比值均值；48–82 不是模型真实位移的放大倍数。")
    fig,axes=plt.subplots(1,2,figsize=(12.5,5.6))
    fig.suptitle("共同方向与随机方向都存在：分量增损、完整更新降损",fontsize=20,y=.98)
    for ax,step,label in zip(axes,["full_step","half_step"],["完整步长","半步长"]):
        values=np.array([[cp[(cp.source==s)&(cp.step==step)&(cp.span==span)].adverse_component_total_help_fraction_1e_5.iloc[0]*100 for span in ["common","random31"]] for s in DOMAINS])
        heat(ax,values,["SAE 共同 rank-32","随机 rank-32"],[CN[s] for s in DOMAINS],label,"全部位置中比例（%）",norm=plt.Normalize(0,20),cmap="YlOrRd",fmt=".2f")
        ax.set_ylabel("来源更新")
    save(fig,"main04_sae_components_heatmap","准确条件：φ_P＞10⁻⁵ 且 I＜−10⁻⁵ nat；φ_P＝(I_P＋I−I_R)／2。每格分母均为全部 1,024 位置。\n共同方向取自 64 个既定共同原子的解码列；随机对照同秩。分量不利不等于移除它有净收益，也不证明长期隔离收益。")
    fig,axes=plt.subplots(1,3,figsize=(16,6),gridspec_kw={"width_ratios":[.64,1.28,1.25]})
    fig.suptitle("辅助图 3：静态重构、动态位移和有限损失分量分别检查",fontsize=20,y=.99)
    val=qualification["static_relative_squared_error_mean"]*100
    axes[0].bar([0],[val],color=COLORS["same"],width=.42);axes[0].text(0,val+.35,f"{val:.2f}%",ha="center",fontsize=16)
    axes[0].set_xticks([0],["64 条记录面板"]);axes[0].set_ylim(0,9);axes[0].set_ylabel("平均 ‖r‖²／‖a‖²（%）");axes[0].set_title("A  静态表征重构")
    xpos=np.arange(8);labels=[SHORT[s]+("\n全步" if step=="full_step" else "\n半步") for s in DOMAINS for step in ["full_step","half_step"]]
    for st,name,offset,color in [("stable_support","集合稳定",-.13,COLORS["same"]),("all","全部位置（含切换）",.13,COLORS["flip"])]:
        vals=[ep[(ep.source==s)&(ep.step==step)&(ep.stratum==st)].dynamic_pooled_rse.iloc[0] for s in DOMAINS for step in ["full_step","half_step"]]
        axes[1].scatter(xpos+offset,vals,color=color,label=name,s=55)
    axes[1].set_yscale("log");axes[1].set_ylim(.6,250);axes[1].axhline(1,color="#65758B",lw=1,ls="--")
    axes[1].set_xticks(xpos,labels);axes[1].set_ylabel("Σ残差能量／Σ真实位移能量（对数轴）");axes[1].set_title("B  更新位移忠实性");axes[1].legend(loc="upper right",fontsize=10)
    for span,name,offset in [("common","SAE 共同 rank-32",-.17),("random31","随机 rank-32",.17)]:
        vals=[cp[(cp.source==s)&(cp.step==step)&(cp.span==span)].adverse_component_total_help_fraction_1e_5.iloc[0]*100 for s in DOMAINS for step in ["full_step","half_step"]]
        axes[2].bar(xpos+offset,vals,width=.31,color=COLORS[span],label=name)
    axes[2].set_xticks(xpos,labels);axes[2].set_ylim(0,23);axes[2].set_ylabel("分量增损且完整降损的位置（%）");axes[2].set_title("C  有限损失分量");axes[2].legend(fontsize=10)
    save(fig,"aux03_sae_three_checks","三面板分母与单位不同，不能把静态误差 6.51% 解读成动态误差放大几十倍。B 为汇总能量比；C 沿用 ±10⁻⁵ nat 死区。\n无新置信区间。SAE 静态重构较好不保证小位移忠实；对称分量分配不等于唯一原子因果解释。")
    return ep,cp


def sae_selected_geometry():
    aset=json.loads((OLD/"analysis/atom_sets.json").read_text())
    selected=np.array(aset["selected"]["common"],dtype=int)
    assert len(selected)==64
    with np.load(OLD/"analysis/fit_readouts.npz") as data:
        freq=data["fit_frequency"][:,selected]
        amp=data["fit_positive_amplitude"][:,selected]
    assert sha(OLD/"fit/shard_0/decoder.npy")==aset["source_dictionary_sha256"]
    decoder=np.load(OLD/"fit/shard_0/decoder.npy",mmap_mode="r")
    columns=decoder[:,selected].astype(np.float64)
    with threadpool_limits(limits=8):
        singular=np.linalg.svd(columns,compute_uv=False)
    frac=singular**2/np.sum(singular**2)
    rows=[dict(original_selection_order=j+1,atom_id=int(k),domain=d,activation_fraction=float(freq[i,j]),
               positive_mean_amplitude=float(amp[i,j]),selection="pre-R F activation only; original 64-atom selection and original order",
               source_records_per_domain=256,events_per_domain=4096,
               amplitude_unit="SAE positive coefficient; conditional mean over positive activations")
          for j,k in enumerate(selected) for i,d in enumerate(DOMAINS)]
    pd.DataFrame(rows).to_csv(EVI/"sae_selected_common_activity.csv",index=False)
    pd.DataFrame(dict(component=np.arange(1,65),singular_value=singular,decoder_column_energy_fraction=frac,
                      cumulative_decoder_column_energy_fraction=np.cumsum(frac),
                      meaning="SVD of 64 selected decoder columns; not data variance or gradient/loss explained variance")).to_csv(EVI/"sae_selected_decoder_spectrum.csv",index=False)
    fig,axes=plt.subplots(1,3,figsize=(16,7),gridspec_kw={"width_ratios":[1.1,1.1,1]})
    fig.suptitle("SAE 已选共同原子的激活结构与解码方向谱",fontsize=20,y=.98)
    ids=[str(k) for k in selected[:16]]
    heat(axes[0],freq[:,:16].T*100,[SHORT[d] for d in DOMAINS],ids,"既定排序前 16 原子：激活频率","激活比例（%；对数色阶）",norm=LogNorm(1,100),cmap="Blues",fmt=".1f")
    heat(axes[1],amp[:,:16].T,[SHORT[d] for d in DOMAINS],ids,"相同原子：正激活平均幅值","正系数均值（对数色阶）",norm=LogNorm(5,float(amp[:,:16].max())),cmap="Blues",fmt=".1f")
    for ax in axes[:2]:ax.set_xlabel("F 拟合集领域");ax.set_ylabel("原子编号（沿既定排序）");ax.tick_params(axis="y",labelsize=10)
    x=np.arange(1,65)
    axes[2].plot(x,np.cumsum(frac)*100,color=COLORS["same"],lw=2)
    axes[2].axvline(32,color=COLORS["flip"],ls="--");axes[2].axhline(100,color="#DFE4EA",lw=1)
    axes[2].scatter([32],[np.cumsum(frac)[31]*100],color=COLORS["flip"],s=55)
    axes[2].text(34,np.cumsum(frac)[31]*100-6,f"rank-32：{np.cumsum(frac)[31]*100:.2f}%",fontsize=12)
    axes[2].set_xlim(1,64);axes[2].set_ylim(0,105);axes[2].set_xlabel("64 解码列的奇异方向数量");axes[2].set_ylabel("累计解码列能量（%）");axes[2].set_title("解码列 SVD：几何谱");axes[2].grid(alpha=.18)
    save(fig,"main05_sae_atom_activity","原子选择于 R 收集前冻结：各域频率≥1%，域间频率／正幅值比≤2；按最低域频率排序。每域 F 为 256 记录 ×16 位置。\n左中图只展示既定前 16 原子（CSV 留存全部 64）；右图仅是解码列几何，不是梯度／损失解释率，也不是语义命名。")
    return {"rank32_decoder_column_energy_fraction":float(np.cumsum(frac)[31]),"dictionary_sha256":aset["source_dictionary_sha256"]}


def gradient_figures():
    """Read the separately authorized CPU audit's compact output only."""
    required=["gradient_geometry_vs_loss.csv","gradient_component_response_correlations.csv",
              "gradient_component_spectrum.csv","gradient_cumulative_vs_finite.csv"]
    if not all((EVI/name).exists() for name in required):
        return {"gradient_figures":"inputs not present; existing figures remain complete"}
    geometry=pd.read_csv(EVI/required[0])
    responses=pd.read_csv(EVI/required[1])
    spectrum=pd.read_csv(EVI/required[2])
    cumulative=pd.read_csv(EVI/required[3])
    labels=[SHORT[d] for d in DOMAINS]
    norm=TwoSlopeNorm(vmin=-1,vcenter=0,vmax=1)
    fig,axes=plt.subplots(1,4,figsize=(21,6.2))
    fig.suptitle("梯度审计：参数方向的关系，需要经过接收数据的损失敏感性才能解释后果",fontsize=20,y=.98)
    for ax,field,title,label in [(axes[0],"gradient_cosine","来源均值梯度：方向余弦","Frobenius 余弦"),
                                 (axes[1],"finite_response_pearson","同一 R 面板：有限损失响应","Pearson 相关")]:
        values=np.array([[geometry[(geometry.source_i==s)&(geometry.source_j==t)][field].iloc[0] for t in DOMAINS] for s in DOMAINS])
        heat(ax,values,labels,labels,title,label,norm=norm,fmt=".3f")
        ax.set_xlabel("来源更新 j");ax.set_ylabel("来源更新 i")
    for ax,basis,title in [(axes[2],"raw","原始梯度基：主方向响应"),(axes[3],"unit_norm","源归一化基：主方向响应")]:
        table=responses[responses.basis==basis]
        values=table.pivot(index="component_i",columns="component_j",values="receiver_response_pearson").loc[[1,2,3,4],[1,2,3,4]].values
        heat(ax,values,["1","2","3","4"],["1","2","3","4"],title,"导数响应 Pearson",norm=norm,fmt=".3f")
        ax.set_xlabel("主方向 j");ax.set_ylabel("主方向 i")
    save(fig,"main06_gradient_geometry_vs_finite_heatmaps","计／数／物／生为四域来源；同一 1,024 条 R 记录 ×16 位置。前两面板比较方向余弦与完整步长的有限 CE 响应相关。\n后两面板为未中心化四源 SVD 正交参数方向的导数响应相关；正交参数方向不保证响应不相关。此处是关系审计，不是语义因果或路由收益。")
    fig,axes=plt.subplots(1,3,figsize=(17,6.3),gridspec_kw={"width_ratios":[1.08,1.08,1]})
    fig.suptitle("梯度主方向累计：源梯度能量与实际损失响应需要分别检查",fontsize=20,y=.98)
    for ax,basis,title in [(axes[0],"raw","原始梯度基（主分析）"),(axes[1],"unit_norm","源等范数基（敏感性检查）")]:
        table=cumulative[(cumulative.basis==basis)&(cumulative.step=="full_step")]
        values=np.array([[table[(table.source==s)&(table.k==k)].finite_pearson.iloc[0] for k in [1,2,3,4]] for s in DOMAINS])
        heat(ax,values,["k＝1","k＝2","k＝3","k＝4"],[CN[d] for d in DOMAINS],title,"与有限 I 的 Pearson r",norm=norm,fmt=".4f")
        ax.set_xlabel("累计保留的源主方向数量");ax.set_ylabel("来源")
    x=np.arange(4)
    for basis,name,offset,color in [("raw","原始源梯度能量",-.17,COLORS["same"]),("unit_norm","等范数源能量",.17,COLORS["flip"])]:
        f=spectrum[spectrum.basis==basis].sort_values("component")
        vals=f.cumulative_gradient_energy_fraction.values*100
        axes[2].bar(x+offset,vals,width=.32,color=color,label=name)
        for xx,val in zip(x+offset,vals):
            axes[2].text(xx+(.05 if basis=="raw" else -.05),val+1.1,f"{val:.3g}",
                         ha="right" if basis=="raw" else "left",fontsize=10)
    axes[2].set_xticks(x,["1","2","3","4"]);axes[2].set_ylim(0,116)
    axes[2].set_xlabel("累计源主方向数量 k");axes[2].set_ylabel("累计源梯度能量（%）")
    axes[2].set_title("两种分母的能量谱");axes[2].legend(fontsize=10,loc="upper left");axes[2].grid(axis="y",alpha=.15)
    save(fig,"main07_gradient_components_response_heatmaps","四个向量是四域均值梯度，不是全部事件梯度；k＝4 恢复四个向量的张成空间，是代数闭合，不是全模型低维发现。\n导数分量没有重新测分量有限 loss。完整步长下 k＝4 的总绝对误差为 0.217%–0.563%；条件区间与半步全表保存在 CSV。")
    return {"gradient_figures":"complete; raw main and unit_norm sensitivity retained","source_svd_object":"four aggregated source gradients only"}


def provenance(summary):
    paths=[NAT/rel for rel in EXPECT]+[
        CTRL/"analysis/primary_by_condition.csv",CTRL/"analysis/primary_by_family.csv",CTRL/"analysis/verdict.json",
        CTRL/"registration.json",CTRL/"environment.json",CTRL/"measurement_complete.json",CTRL/"dataset_manifest.json",
        NAT/"scripts/finite_panel.py",NAT/"scripts/finite_replay.py",NAT/"scripts/sae_displacement.py",
        NAT/"runs/finite_panel_01/receipt.json",NAT/"runs/finite_panel_01/registration.json",
        NAT/"runs/finite_panel_01/effects.npz",NAT/"runs/finite_panel_01/panel_metadata.npz",
        NAT/"runs/finite_replay_01/effects.npz",NAT/"runs/finite_replay_01/panel_metadata.npz",
        NAT/"runs/finite_replay_01/panel_freeze.json",NAT/"runs/finite_replay_01/receipt.json",
        NAT/"runs/sae_displacement_01/endpoint_arrays.npz",NAT/"runs/sae_displacement_01/qualification.json",
        NAT/"runs/sae_displacement_01/registration.json",NAT/"runs/cache_audit_01/source_mean_gradients.npy",
        OLD/"analysis/atom_sets.json",OLD/"analysis/fit_readouts.npz",OLD/"fit/shard_0/decoder.npy",OLD.parents[1]/"scripts/analyze.py",Path(__file__),
    ]
    meta={"created_by":"figures_1008; root thread 01a10a2a-b783-7752-9149-ed2ffd48a40a",
          "kind":"derived selected evidence and figures; not canonical scientific judgment",
          "checkpoint_state_sha256":json.loads((NAT/"runs/finite_replay_01/receipt.json").read_text())["checkpoint_state_sha256"],
          "checkpoint_training_tokens":33000000000,"model_updates":0,"GPU_jobs":0,
          "attachment_hashes_match":True,"source_files":[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in paths],
          "source_column_mapping":{
              "controlled":"B_I -> mean_finite_loss_delta_nat; group mean checked against verdict.point; existing verdict.interval_95 preserved",
              "natural":"mean_delta_loss -> heatmap I; conditional_lo/hi -> existing interval; event_adverse_fraction_gt_1e_5 -> 100*value percent; event_unresolved_fraction_1e_5 -> 100*value percent; records*16 -> exact event count",
              "endpoint":"dynamic_pooled_rse -> sum residual energy/sum true displacement energy within source/step/stratum, verified in sae_displacement.py",
              "components":"adverse_component_total_help_fraction_1e_5 -> 100*value percent; random31 denotes seed31 basis truncated to32 columns",
              "activity":"fit_frequency -> positive activation count/positions; fit_positive_amplitude -> positive coefficient sum/positive activation count; original selected order retained",
              "spectrum":"SVD existing decoder[:,selected_common64]; s^2/sum(s^2); no model invocation"},
          "summary":summary,
          "event_arrays_preserved":{"path":str(NAT/"runs/finite_panel_01/effects.npz"),"metadata_path":str(NAT/"runs/finite_panel_01/panel_metadata.npz"),
              "readout_selection":"part==1","records":1024,"positions_per_record":16,"events_per_source_step":16384,
              "fields":{"docs":"record row id in selected.jsonl","positions":"0..15 per-record evaluation position index (actual contexts 14,30,...,254)","domains":"0..3 in DOMAINS order","effect_keys":"source__full_step or source__half_step; actual finite CE difference, nat/target"},
              "policy":"arrays remain with execution owner; no large per-event array or raw event CSV copied into Git"},
          "new_statistics":"plotting script adds no test or interval; existing tables and deterministic decoder SVD only. Separately authorized gradient audit is recorded below and owns its new conditional intervals.",
          "font":{"runtime_path":str(ARGS.font),"sha256":sha(ARGS.font),"copied_to_repository":False},
          "outputs":[dict(path=str(p.relative_to(HERE)),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(FIG.glob('*'))]+[
              dict(path=str(p.relative_to(HERE)),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(EVI.glob('*.csv'))]}
    grad_recipe=EVI/"gradient_component_recipe.json"
    if grad_recipe.exists():
        meta["separately_authorized_gradient_audit"]={"recipe_path":str(grad_recipe),"recipe_sha256":sha(grad_recipe),
            "receipt_path":str(EVI/"gradient_component_receipt.json"),
            "source_column_mapping":"gradient_cosine -> parameter geometry; finite_response_pearson -> response correlation; receiver_response_pearson -> derivative component correlation; finite_pearson -> cumulative first-order versus finite I; cumulative_gradient_energy_fraction -> basis-specific source energy",
            "intervals":"new post-hoc fixed-source record bootstrap belongs to gradient audit; figures show point estimates; complete conditional intervals in gradient_cumulative_vs_finite.csv"}
    (EVI/"figures_provenance.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n")


def main():
    FIG.mkdir(parents=True,exist_ok=True);EVI.mkdir(parents=True,exist_ok=True)
    font_manager.fontManager.addfont(str(ARGS.font))
    plt.rcParams.update({"font.family":[font_manager.FontProperties(fname=str(ARGS.font)).get_name(),"DejaVu Sans"],
                         "font.size":12,"axes.unicode_minus":False,"svg.fonttype":"path","axes.spines.top":False,"axes.spines.right":False})
    for rel,expected in EXPECT.items():
        assert sha(NAT/rel)==expected,f"Attachment hash mismatch: {rel}"
    with threadpool_limits(limits=8):
        controlled();natural();sae();summary=sae_selected_geometry();summary.update(gradient_figures());provenance(summary)
    print(json.dumps({"figures":len(list(FIG.glob('*.png'))),"csv":len(list(EVI.glob('*.csv'))),"summary":summary},ensure_ascii=False))


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font",type=Path,required=True,help="Chinese CJK .otf/.ttf font; external runtime file")
    ARGS=parser.parse_args()
    main()

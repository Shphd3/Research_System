from meeting_plots import O,pd,names
def main():
    p=O/'03_读图.md'; text=p.read_text()
    d=pd.read_csv(O/'03_逐层有效秩与比值.csv');s=pd.read_csv(O/'03_层段曲线.csv')
    table=[]
    for key,g in d.sort_values(['arm','tokens','layer']).groupby('key',sort=False):
        z=g.iloc[0];rr=[f'{t.ratio_median:.3f} / {t.global_rank:.1f}' if pd.notna(t.ratio_median) else f'— / {t.global_rank:.1f}' for t in g.itertuples()]
        table.append(f'| {names[z.arm]} | {z.tokens/1e9:.6g} | {z.step} | '+' | '.join(rr)+' |')
    (O/'03_逐层有效秩与比值.md').write_text('# 逐层有效秩：专家条件 / 全局\n\n各单元格为「专家条件有效秩 ÷ 同层全局有效秩（8 个 expert 中位数） / 该层全局绝对有效秩」。Dense 只算全局。\n\n| 模型 | 累计 token（B） | 步 | L0 | L1 | L2 | L3 | L4 | L5 | L6 | L7 |\n| -- | --: | --: | --: | --: | --: | --: | --: | --: | --: | --: |\n'+'\n'.join(table)+'\n')
    for k,v in {'A0_step500':'第 500 步','A0_step1000':'第 1000 步','A0_step2000':'第 2000 步','MoE_1000M':'1B','MoE_10000M':'10B','MoE_33000M':'33B'}.items(): text=text.replace(k,v)
    text=text.replace('[逐层秩比及全局绝对秩](03_逐层有效秩与比值.csv)','[逐层表](03_逐层有效秩与比值.md) / [CSV](03_逐层有效秩与比值.csv)')
    a=s[s.arm=='A5'].pivot(index='key',columns='layer_group',values='ratio_mean')
    if {'A5_step2000','A5_step3816'}<=set(a.index):
        v=a.loc['A5_step2000'];w=a.loc['A5_step3816']
        text+=f'\n**A5 续训对照：** 2000 步的前四层／后四层秩比为 **{v.iloc[0]:.3f}／{v.iloc[1]:.3f}**，约 1B（3816 步）为 **{w.iloc[0]:.3f}／{w.iloc[1]:.3f}**。两点都是同一套 A5 分发下的实际存档；这一段秩比几乎不变，图 1 中的损失领先却缩小了。\n'
    m=s[s.arm=='A0'].pivot(index='key',columns='layer_group',values='global_rank_mean')
    if {'A0_step500','MoE_10000M'}<=set(m.index):
        v=m.loc['A0_step500'];w=m.loc['MoE_10000M']
        text+=f'\n**“方向减少”是相对量。** 从 500 步到 10B，原生 MoE 的全局绝对有效秩，前四层均值从 **{v.iloc[0]:.0f}** 增至 **{w.iloc[0]:.0f}**，后四层从 **{v.iloc[1]:.0f}** 增至 **{w.iloc[1]:.0f}**。专家输入相对同阶段全体输入更集中，不代表绝对有效秩越训越低。\n'
    p.write_text(text)
if __name__=='__main__':main()

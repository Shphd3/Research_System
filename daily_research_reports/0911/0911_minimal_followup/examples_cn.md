# 固定规则选出的真实文本例子

这些是答案预测位置的教师分组例子，使用动态SAE臂末期检查点及最后一次保存的字典。它们没有人工语义标签，不能当成已确认的“语义原子”或专家名称。

阅读副本完整呈现seed17的8个组，不按结果挑组；每组最多3个不同记录的正例，按该组权重从高到低选择。反例是该组权重较高、但最大权重属于别组的前2个位置，不要求不同记录。“正/反”只相对于组的最大权重判定，不是真假语义标签。其余两种子的同规则结果保留在执行目录。

q_g表示已分组激活中分给g组的比例；q最大组是教师分组，实际专家是加入负载偏置后的模型选择，两者应分别读。⏎表示换行。上下文仅摘取末100字符，完整记录ID用于追查。

## 组0

| 类型 | 位置ID | q_g / 最大组 | 预测前的文本末段 → 下一词元 | 实际专家 |
|---|---|---|---|---|
| 正例 | probe 574；token 200 | 0.589 / 0 | `… integer, we would want the smallest bases $a$ and $b$. Since $a$ and $b$ must be greater than 2, we` → `'ll` | 4 |
| 正例 | probe 437；token 219 | 0.555 / 0 | `…(k + 2)} \\ &= \frac{k + 1}{(k + 2)!}. \end{align*}Seeking a way to get the sum to telescope, we can` → ` express` | 7 |
| 正例 | probe 1132；token 160 | 0.544 / 0 | `…}From here, we see that the two possible values of $x$ are $0$ and $\frac18$. Since the problem only` → ` asks` | 1 |
| 边界反例 | probe 809；token 120 | 0.387 / 3 | `…er of tadpoles as frogs, so there are 3 * 5 = <<3*5=15>>15 tadpoles. Two-thirds of the tadpoles will` → ` survive` | 0 |
| 边界反例 | probe 784；token 46 | 0.381 / 3 | `…sors of 9!.⏎Solution:⏎The prime factorization of 9! is \[2^7 \cdot 3^4 \cdot 5 \cdot 7,\]so from the` → ` formula` | 0 |

记录索引：

- probe 574：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:number_theory/train-00000-of-00001.parquet:830`，位置200。
- probe 437：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:intermediate_algebra/test-00000-of-00001.parquet:210`，位置219。
- probe 1132：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:algebra/train-00000-of-00001.parquet:1200`，位置160。
- probe 809：`openai/gsm8k@740312add88f781978c0658806c59bc2815b9866:main/train-00000-of-00001.parquet:7175`，位置120。
- probe 784：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:number_theory/test-00000-of-00001.parquet:345`，位置46。

## 组1

| 类型 | 位置ID | q_g / 最大组 | 预测前的文本末段 → 下一词元 | 实际专家 |
|---|---|---|---|---|
| 正例 | probe 735；token 141 | 0.807 / 1 | ` HCl⏎B. A = H3O+, B = HCl⏎C. A = H3O+, B = CH3COOH⏎D. A = NaHSO3, B = CH3COOH⏎Answer:⏎` → `A` | 4 |
| 正例 | probe 1135；token 80 | 0.796 / 1 | `…is associated with pain⏎D. Second degree haemorrhoids cannot be returned to the anal canal⏎Answer:⏎B` → `<∣endoftext∣>` | 4 |
| 正例 | probe 890；token 158 | 0.791 / 1 | `…ggravated assault.⏎G. attempted larceny.⏎H. trespassing.⏎I. possession of stolen property.⏎Answer:⏎D` → `<∣endoftext∣>` | 4 |
| 边界反例 | probe 732；token 25 | 0.381 / 3 | `…have a trumpet, a drum, an accordion, and a piano. How many musical instruments do I have?⏎Answer:⏎4` → `<∣endoftext∣>` | 4 |
| 边界反例 | probe 581；token 41 | 0.359 / 3 | `… a trumpet, five pianos, a flute, and a clarinet. How many musical instruments do I have?⏎Answer:⏎12` → `<∣endoftext∣>` | 4 |

记录索引：

- probe 735：`Idavidrein/gpqa@openai-simple-evals@652c89d0ca9df547706735883097e9537d40dc47:gpqa_diamond.csv:113`，位置141。
- probe 1135：`cais/mmlu@c30699e8356da336a370243923dbaf21066bb9fe:all/test-00000-of-00001.parquet:676`，位置80。
- probe 890：`TIGER-Lab/MMLU-Pro@b189ec765aa7ed75c8acfea42df31fdae71f97be:data/test-00000-of-00001.parquet:950`，位置158。
- probe 732：`lukaemon/bbh@982bb89fd79532a8ac676a61fc42eb1aeec63f99:object_counting/test-00000-of-00001.parquet:234`，位置25。
- probe 581：`lukaemon/bbh@982bb89fd79532a8ac676a61fc42eb1aeec63f99:object_counting/test-00000-of-00001.parquet:118`，位置41。

## 组2

| 类型 | 位置ID | q_g / 最大组 | 预测前的文本末段 → 下一词元 | 实际专家 |
|---|---|---|---|---|
| 正例 | probe 454；token 139 | 0.737 / 2 | `…from the three full cans?⏎Answer:⏎At the end of the day, he had tested 120 boards, each with three t` → `acks` | 4 |
| 正例 | probe 499；token 61 | 0.651 / 2 | `…eager geophysical wiseacre mathieu cognoscenti purposive flamboyant⏎Answer:⏎agile blackguard butt cl` → `ape` | 7 |
| 正例 | probe 131；token 101 | 0.606 / 2 | `…p ⏎    if (hund1): ⏎        ordd += hund1 ⏎        leap -= hund1 ⏎    if (hund4): ⏎        ordd -= h` → `und` | 4 |
| 边界反例 | probe 557；token 333 | 0.262 / 4 | `…etter_grade.append("A")⏎        elif gpa > 3.3:⏎            letter_grade.append("A-")⏎        elif g` → `pa` | 5 |
| 边界反例 | probe 556；token 298 | 0.252 / 4 | `…]⏎    for gpa in grades:⏎        if gpa == 4.0:⏎            letter_grade.append("A+")⏎        elif g` → `pa` | 5 |

记录索引：

- probe 454：`openai/gsm8k@740312add88f781978c0658806c59bc2815b9866:main/train-00000-of-00001.parquet:1093`，位置139。
- probe 499：`lukaemon/bbh@982bb89fd79532a8ac676a61fc42eb1aeec63f99:word_sorting/test-00000-of-00001.parquet:140`，位置61。
- probe 131：`google-research-datasets/mbpp@4bb6404fdc6cacfda99d4ac4205087b89d32030c:full/test-00000-of-00001.parquet:278`，位置101。
- probe 557：`openai/openai_humaneval@7dce6050a7d6d172f3cc5c32aa97f52fa1a2e544:openai_humaneval/test-00000-of-00001.parquet:81`，位置333。
- probe 556：`openai/openai_humaneval@7dce6050a7d6d172f3cc5c32aa97f52fa1a2e544:openai_humaneval/test-00000-of-00001.parquet:81`，位置298。

## 组3

| 类型 | 位置ID | q_g / 最大组 | 预测前的文本末段 → 下一词元 | 实际专家 |
|---|---|---|---|---|
| 正例 | probe 1162；token 70 | 0.718 / 3 | `…w many cookies did he take out in four days?⏎Answer:⏎Paul took out a total of 70-28 = <<70-28=42>>42` → ` cookies` | 4 |
| 正例 | probe 749；token 91 | 0.689 / 3 | `…ores that Taylor got is 7+6=<<7+6=13>>13 The difference in the ratio between the number of black and` → ` white` | 4 |
| 正例 | probe 227；token 77 | 0.682 / 3 | `…hey have to order for a month?⏎Answer:⏎Chandler and Lucy can eat 23 + 19 = <<23+19=42>>42 apples per` → ` week` | 4 |
| 边界反例 | probe 1161；token 57 | 0.414 / 4 | `…ount each day, how many cookies did he take out in four days?⏎Answer:⏎Paul took out a total of 70-28` → ` =` | 4 |
| 边界反例 | probe 1226；token 110 | 0.384 / 1 | `… the end of the game, Bob has the Options: (A) yellow ball (B) purple ball (C) blue ball⏎Answer:⏎(A)` → `<∣endoftext∣>` | 4 |

记录索引：

- probe 1162：`openai/gsm8k@740312add88f781978c0658806c59bc2815b9866:main/train-00000-of-00001.parquet:7393`，位置70。
- probe 749：`openai/gsm8k@740312add88f781978c0658806c59bc2815b9866:main/train-00000-of-00001.parquet:4385`，位置91。
- probe 227：`openai/gsm8k@740312add88f781978c0658806c59bc2815b9866:main/train-00000-of-00001.parquet:3447`，位置77。
- probe 1161：`openai/gsm8k@740312add88f781978c0658806c59bc2815b9866:main/train-00000-of-00001.parquet:7393`，位置57。
- probe 1226：`lukaemon/bbh@982bb89fd79532a8ac676a61fc42eb1aeec63f99:tracking_shuffled_objects_three_objects/test-00000-of-00001.parquet:72`，位置110。

## 组4

| 类型 | 位置ID | q_g / 最大组 | 预测前的文本末段 → 下一词元 | 实际专家 |
|---|---|---|---|---|
| 正例 | probe 219；token 103 | 0.988 / 4 | `0*7 = <<20*7=140>>140 If 1/4 of the 20 lamps have burnt-out light bulbs, there are 1/4*20 = <<1/4*` → `2` | 4 |
| 正例 | probe 763；token 113 | 0.979 / 4 | `…d dogs. He wants to have 2 * 4 = <<2*4=8>>8 French Bulldogs. So, Peter wants to have 9 + 8 = <<9+8=1` → `7` | 1 |
| 正例 | probe 23；token 127 | 0.976 / 4 | `…. If there are 5 intersections, the total number of lines in all the intersections is 80*5 = <<80*5=` → `4` | 6 |
| 边界反例 | probe 438；token 278 | 0.466 / 5 | ` $(k + 2) - 1.$ Then \[\frac{k + 1}{(k + 2)!} = \frac{(k + 2) - 1}{(k + 2)!} = \frac` → `{k` | 4 |
| 边界反例 | probe 152；token 108 | 0.432 / 7 | `…to $x - 5 < 0.$ Since the expression is not defined for $x = -5,$ the solution is \[x \in \boxed{(-\` → `in` | 4 |

记录索引：

- probe 219：`openai/gsm8k@740312add88f781978c0658806c59bc2815b9866:main/train-00000-of-00001.parquet:4158`，位置103。
- probe 763：`openai/gsm8k@740312add88f781978c0658806c59bc2815b9866:main/train-00000-of-00001.parquet:3421`，位置113。
- probe 23：`openai/gsm8k@740312add88f781978c0658806c59bc2815b9866:main/train-00000-of-00001.parquet:5550`，位置127。
- probe 438：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:intermediate_algebra/test-00000-of-00001.parquet:210`，位置278。
- probe 152：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:intermediate_algebra/train-00000-of-00001.parquet:495`，位置108。

## 组5

| 类型 | 位置ID | q_g / 最大组 | 预测前的文本末段 → 下一词元 | 实际专家 |
|---|---|---|---|---|
| 正例 | probe 1084；token 109 | 0.795 / 5 | `…(\mathbf{a} \times \mathbf{b}).$⏎Solution:⏎The vectors $\mathbf{a}$ and $\mathbf{a} \times \mathbf{b` → `}$` | 4 |
| 正例 | probe 148；token 53 | 0.774 / 5 | `…{x^2 - 25}{x + 5} < 0.\]⏎Solution:⏎We can factor the numerator, to get \[\frac{(x - 5)(x + 5)}{x + 5` → `}` | 2 |
| 正例 | probe 1127；token 53 | 0.767 / 5 | `… fractional form.⏎Solution:⏎We start by squaring both sides of the equation \begin{align*} (\sqrt{2x` → `})` | 1 |
| 边界反例 | probe 1128；token 75 | 0.436 / 4 | `…quaring both sides of the equation \begin{align*} (\sqrt{2x})^2&=(4x)^2 \\ \Rightarrow \qquad 2x&=16` → `x` | 4 |
| 边界反例 | probe 875；token 246 | 0.429 / 4 | `$. $$ \begin{array}{c@{}c@{\;}c@{}c@{}c@{}c} & & & 1 & 2 & 1_3\\ &+ & & & 1 & 1` → `_` | 4 |

记录索引：

- probe 1084：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:precalculus/test-00000-of-00001.parquet:198`，位置109。
- probe 148：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:intermediate_algebra/train-00000-of-00001.parquet:495`，位置53。
- probe 1127：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:algebra/train-00000-of-00001.parquet:1200`，位置53。
- probe 1128：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:algebra/train-00000-of-00001.parquet:1200`，位置75。
- probe 875：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:number_theory/test-00000-of-00001.parquet:35`，位置246。

## 组6

| 类型 | 位置ID | q_g / 最大组 | 预测前的文本末段 → 下一词元 | 实际专家 |
|---|---|---|---|---|
| 正例 | probe 905；token 37 | 0.576 / 6 | `…d elements in a given array.⏎Python solution:⏎def find_Product(arr,n): ⏎    arr.sort() ⏎    prod = 1` → `⏎` | 2 |
| 正例 | probe 588；token 36 | 0.555 / 6 | `…etter and one number.⏎Python solution:⏎def check_String(str): ⏎    flag_l = False⏎    flag_n = False` → `⏎` | 2 |
| 正例 | probe 838；token 62 | 0.539 / 6 | `…se⏎    while pos < len(dlist) and not found:⏎        if dlist[pos] == item:⏎            found = True` → `⏎` | 2 |
| 边界反例 | probe 334；token 305 | 0.402 / 4 | `…ne']⏎    """⏎    dic = {⏎        1: "One",⏎        2: "Two",⏎        3: "Three",⏎        4: "Four",⏎` → `       ` | 2 |
| 边界反例 | probe 839；token 70 | 0.374 / 4 | `…t found:⏎        if dlist[pos] == item:⏎            found = True⏎        else:⏎            pos = pos` → ` +` | 2 |

记录索引：

- probe 905：`google-research-datasets/mbpp@4bb6404fdc6cacfda99d4ac4205087b89d32030c:full/test-00000-of-00001.parquet:14`，位置37。
- probe 588：`google-research-datasets/mbpp@4bb6404fdc6cacfda99d4ac4205087b89d32030c:full/test-00000-of-00001.parquet:181`，位置36。
- probe 838：`google-research-datasets/mbpp@4bb6404fdc6cacfda99d4ac4205087b89d32030c:full/test-00000-of-00001.parquet:269`，位置62。
- probe 334：`openai/openai_humaneval@7dce6050a7d6d172f3cc5c32aa97f52fa1a2e544:openai_humaneval/test-00000-of-00001.parquet:105`，位置305。
- probe 839：`google-research-datasets/mbpp@4bb6404fdc6cacfda99d4ac4205087b89d32030c:full/test-00000-of-00001.parquet:269`，位置70。

## 组7

| 类型 | 位置ID | q_g / 最大组 | 预测前的文本末段 → 下一词元 | 实际专家 |
|---|---|---|---|---|
| 正例 | probe 81；token 218 | 0.687 / 7 | `…. So, any segment from a vertex of the triangle to $C$ is an angle bisector. From $\angle QRC = 30^\` → `circ` | 0 |
| 正例 | probe 679；token 143 | 0.614 / 7 | `…ic polynomial is \begin{align*} (x - 1 - i \sqrt{3})(x - 1 + i \sqrt{3})(x + 2) &= ((x - 1)^2 - (i \` → `sqrt` | 4 |
| 正例 | probe 432；token 201 | 0.604 / 7 | `…3a-a^2) = (x+a)^2 + (3a-a^2).\]It follows that the minimum value of $f(x)$ is $3a-a^2,$ so we have \` → `[` | 2 |
| 边界反例 | probe 872；token 90 | 0.227 / 5 | `…t values, but we'll start with $2122_3-2111_3$ since the values are close. $$ \begin{array}{c@{}c@{\` → `;}` | 4 |
| 边界反例 | probe 377；token 70 | 0.213 / 5 | `… $13(3x-2)\equiv 26\pmod 8$?⏎Solution:⏎We can simplify as follows: \begin{align*} 13(3x-2)&\equiv 26` → ` &` | 4 |

记录索引：

- probe 81：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:geometry/train-00000-of-00001.parquet:203`，位置218。
- probe 679：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:intermediate_algebra/train-00000-of-00001.parquet:1126`，位置143。
- probe 432：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:intermediate_algebra/train-00000-of-00001.parquet:442`，位置201。
- probe 872：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:number_theory/test-00000-of-00001.parquet:35`，位置90。
- probe 377：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:number_theory/train-00000-of-00001.parquet:753`，位置70。

## 近邻变化：变得最多、居中、保持不变各看一个

来自纯任务微调、development、几何面板中的seed17。对每个输入计算起点/终点最近10个邻居的重合率，按数值稳定排序取最小、中位、最大；展示各自前3个邻居。此处观察的是回答前表征，与上面的答案内位置不同。近邻保留多少，不自动表示语义好坏。

### 变化最大：10近邻保留40%

输入：`As a result of an accident, Abdul lost sight in his right eye. To judge the distance of vehicles when he is driving, Abdul is able to rely on cues of⏎A. I only⏎B. II only⏎C. III only⏎D. I and II only⏎Answer:⏎`

记录：`cais/mmlu@c30699e8356da336a370243923dbaf21066bb9fe:all/test-00000-of-00001.parquet:5019`

| 排名 | 起点近邻摘录 | 终点近邻摘录 |
|---|---|---|
| 1 | `…qual, which of the following persons is likely to live the longest?⏎A. A black man⏎B. A white man⏎C. A black woman⏎D. A white woman⏎Answer:⏎` | `…qual, which of the following persons is likely to live the longest?⏎A. A black man⏎B. A white man⏎C. A black woman⏎D. A white woman⏎Answer:⏎` |
| 2 | `…⏎B. 500 kJ/min.⏎C. 30 kJ/min.⏎D. 40 kJ/min.⏎E. 400 kJ/min.⏎F. 60 kJ/min.⏎G. 200 kJ/min.⏎H. 100 kJ/min.⏎I. 80 kJ/min.⏎J. 120 kJ/min.⏎Answer:⏎` | `…but 5 times more massive than Earth. d) A planet with the same composition as Earth but half the mass of Earth.⏎A. d⏎B. b⏎C. c⏎D. a⏎Answer:⏎` |
| 3 | `…2. The diagram, unfortunately, has been rendered unreadable by a spilled coffee. How many loops did it contain?⏎A. 2⏎B. 1⏎C. 6⏎D. 3⏎Answer:⏎` | `…egligent entrustment claim is generally allowed when the entrustor knows that he is loaning the vehicle to an incompetent operator.⏎Answer:⏎` |

### 变化居中：10近邻保留90%

输入：`Write a function to multiply two lists using map and lambda function.⏎Python solution:⏎`

记录：`google-research-datasets/mbpp@4bb6404fdc6cacfda99d4ac4205087b89d32030c:full/train-00000-of-00001.parquet:81`

| 排名 | 起点近邻摘录 | 终点近邻摘录 |
|---|---|---|
| 1 | `Write a function to add two lists using map and lambda function.⏎Python solution:⏎` | `Write a function to add two lists using map and lambda function.⏎Python solution:⏎` |
| 2 | `Write a function to divide two lists using map and lambda function.⏎Python solution:⏎` | `Write a function to divide two lists using map and lambda function.⏎Python solution:⏎` |
| 3 | `Write a function to sum elements in two lists.⏎Python solution:⏎` | `Write a function to sum elements in two lists.⏎Python solution:⏎` |

### 保持最多：10近邻保留100%

输入：`…ks. First, Alice and Claire swap books. Then, Alice and Bob swap books. Finally, Alice and Claire swap books. At the end of the semester, Claire has Options: (A) Frankenstein (B) The Odyssey (C) The Great Gatsby⏎Answer:⏎`

记录：`lukaemon/bbh@982bb89fd79532a8ac676a61fc42eb1aeec63f99:tracking_shuffled_objects_three_objects/test-00000-of-00001.parquet:47`

| 排名 | 起点近邻摘录 | 终点近邻摘录 |
|---|---|---|
| 1 | `…ks. Finally, Bob and Claire swap books. At the end of the semester, Bob has Options: (A) The Odyssey (B) The Pearl (C) Frankenstein⏎Answer:⏎` | `…ks. Finally, Bob and Claire swap books. At the end of the semester, Bob has Options: (A) The Odyssey (B) The Pearl (C) Frankenstein⏎Answer:⏎` |
| 2 | `… balls. Finally, Alice and Bob swap balls. At the end of the game, Bob has the Options: (A) green ball (B) blue ball (C) brown ball⏎Answer:⏎` | `… balls. Finally, Alice and Bob swap balls. At the end of the game, Bob has the Options: (A) green ball (B) blue ball (C) brown ball⏎Answer:⏎` |
| 3 | `…s. Finally, Alice and Claire swap balls. At the end of the game, Bob has the Options: (A) yellow ball (B) purple ball (C) blue ball⏎Answer:⏎` | `…s. Finally, Alice and Claire swap balls. At the end of the game, Bob has the Options: (A) yellow ball (B) purple ball (C) blue ball⏎Answer:⏎` |

## 怎样用例子约束解释

先遮住数据来源与专家编号，仅看文本，提出一个候选描述；再读边界反例和同一记录的不同位置，找出该命名解释不了的情况。比如换行、答案格式、数字生成位置也可能造成相似性，不能因为几个例子来自数学数据，就直接命名为“数学语义组”。这一步需要研究者判断，本报告没有代填语义真值。

完整三种子结果：[分组样例](/data/250010109/MoE_Router/experiments/20260910_sft_routing_representation_full_matrix/audits/0911_minimal_followup/group_examples.json)、[近邻样例](/data/250010109/MoE_Router/experiments/20260910_sft_routing_representation_full_matrix/audits/0911_minimal_followup/neighbor_examples.json)、[探针身份清单](/data/250010109/MoE_Router/experiments/20260910_sft_routing_representation_full_matrix/audits/0911_minimal_followup/probe_manifest.json)。这些是执行工作区的原始分析材料；本文只保留阅读摘录。

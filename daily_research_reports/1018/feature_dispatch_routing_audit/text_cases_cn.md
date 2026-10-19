# 自然文本与实际去向：固定三个 feature 的 12 张卡片

目的：低频 feature 已出现时，核对完整输入送往哪里、各组分数为何胜出。只解释固定评分路径，不据此声称 feature 单义或专家已经学习。

案例仅按 TRAIN 接收率及上下文支持冻结：9297, 1133, 2704。三者原负责专家均为 A0，TRAIN 接收率均为 0；没有好／坏对比。
每个 feature：EVAL 固定种子随机 3 个命中，优先不同上下文；另取未展示上下文中最高 z 的 1 个。全局最高 z 另记 sampling.json。
前缀只显示当前位置之前最多 100 个 token；模型实际可见从该 1024-token 上下文起点至当前 token 的全部前缀。完整可见前缀保存在 text_cases.json。下一 token 单列，仅解释标签，不参与路由。
伴随表中的组号 -1 表示该 feature 不在冻结的可靠路由 feature 池，不参与组分数；它并未从原 hidden 或专家输入中删除，-1 不是另一个专家。
TRAIN/EVAL 是原字典 TRAIN 语料中不重叠文件上的位置；EVAL 已经使用过，不是全新确认集，原文档和近重复独立性未知。

## 卡片 1：feature 9297 / random

- EVAL 行 18758；上下文 117676；绝对 token 偏移 8407392；上下文内位置 352。
- 原文件：`/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；token/target 核对 PASS。
- TRAIN 激活频率：0.232572%；该位置 z=0.0459293。
- 当前 token：`9555` / " established"；正确下一 token：`11` / ","（不参与路由）。
- 模型实际可见 353 个 token；下面仅展示前缀最后至多 100 个 token，并将当前 token 单列。

```text
 project has unfolded, it has taken on a life of its own. It was not yet complete when I began writing this essay in 2001. Using different types and sizes of paper to make the Grain prints proved to be a mistake, another wrong turn in the process of creation. The entire paper issue eventually seemed irrelevant to my goal. But what was the goal? Or, more accurately, what has it become?

I think it has become an effort to create a new version of the
```

|规则|负责专家|实际去向|次名|胜出差额|U 的评分项|移除 U 后去向|
|---|---:|---:|---:|---:|---:|---:|
|A|0|7|4|0.254261|2.76497e-05|7|
|B1|0|4|2|0.00566835|2.76497e-05|4|
|B2|0|4|6|0.0020232|2.76497e-05|4|

**八组原始分数（专家 0→7）**

- A：0.0022422, 0.0197721, 0.04375, 0.113756, 0.183983, 0.0745054, 0.163049, 0.438244
- B1：0.00405303, 0.00211016, 0.0100367, 0.00577907, 0.0157051, 0, 0, 0
- B2：0.00415927, 0.00143985, 0.00280447, 0.00236884, 0.0295892, 0, 0.027566, 0

**主要伴随 feature**（按该位置 z×跨层 decoder 范数和排序；不是语义或学习重要性排序）

|feature ID|TRAIN 频率|z|幅度分数|A 组|B1 组|B2 组|
|---:|---:|---:|---:|---:|---:|---:|
|4120|0.0199%|0.21673|1.6707|-1|-1|-1|
|7415|94.7702%|0.094414|0.83264|7|0|0|
|516|98.3490%|0.081914|0.79567|7|0|0|
|13964|98.4684%|0.072002|0.75425|7|0|0|
|5793|3.4817%|0.086275|0.67765|0|0|0|
|2317|5.0539%|0.083409|0.6771|0|0|0|
|5410|18.5354%|0.074334|0.66084|1|0|0|
|11364|39.0691%|0.058528|0.61365|3|0|0|

移除 U 只在评分和中去掉该项并保留原分母；没有修改专家输入或模型表征。即使赢家不变，也不能推出 U 对原模型预测无用。

## 卡片 2：feature 9297 / random

- EVAL 行 62248；上下文 117718；绝对 token 偏移 8450974；上下文内位置 926。
- 原文件：`/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；token/target 核对 PASS。
- TRAIN 激活频率：0.232572%；该位置 z=0.0166324。
- 当前 token：`10820` / " identified"；正确下一 token：`448` / " with"（不参与路由）。
- 模型实际可见 927 个 token；下面仅展示前缀最后至多 100 个 token，并将当前 token 单列。

```text
 caught up in the right-left false meme. It keeps decent people from both sides from awakening to a greater truth. It creates a sort of closed-mindedness. Everyone creates their own reality and most of what all of us believe is some degree of bullshit. There is almost always a greater truth to any particular belief we may have. And, we most usually are unaware of it.

Thanks Lambert.... :)

Submitted by lambert on

... I'm speaking more sociologically, in that media seem to be
```

|规则|负责专家|实际去向|次名|胜出差额|U 的评分项|移除 U 后去向|
|---|---:|---:|---:|---:|---:|---:|
|A|0|7|6|0.066505|1.00128e-05|7|
|B1|0|4|1|0.050325|1.00128e-05|4|
|B2|0|3|0|0.000717702|1.00128e-05|3|

**八组原始分数（专家 0→7）**

- A：0.00173597, 0.0286821, 0.029399, 0.108346, 0.181549, 0.086762, 0.330318, 0.396823
- B1：0.00345589, 0.00677687, 0.0054302, 0.00334169, 0.0571019, 0, 0, 0
- B2：0.00363113, 0.00230189, 0.00190516, 0.00434883, 0, 0, 0, 0

**主要伴随 feature**（按该位置 z×跨层 decoder 范数和排序；不是语义或学习重要性排序）

|feature ID|TRAIN 频率|z|幅度分数|A 组|B1 组|B2 组|
|---:|---:|---:|---:|---:|---:|---:|
|11177|0.0421%|0.26118|2.0391|-1|-1|-1|
|8345|88.2268%|0.062152|0.66654|7|0|0|
|13774|13.4173%|0.11072|0.6476|1|0|0|
|556|57.7560%|0.06489|0.57851|4|0|0|
|13830|81.1593%|0.055286|0.56337|6|0|0|
|13373|1.1369%|0.074709|0.56238|0|0|0|
|5410|18.5354%|0.063104|0.561|1|0|0|
|7388|96.8679%|0.050569|0.55767|7|0|0|

移除 U 只在评分和中去掉该项并保留原分母；没有修改专家输入或模型表征。即使赢家不变，也不能推出 U 对原模型预测无用。

## 卡片 3：feature 9297 / random

- EVAL 行 7198；上下文 117665；绝对 token 偏移 8395813；上下文内位置 37。
- 原文件：`/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；token/target 核对 PASS。
- TRAIN 激活频率：0.232572%；该位置 z=0.0317692。
- 当前 token：`553` / " by"；正确下一 token：`50507` / " Europeans"（不参与路由）。
- 模型实际可见 38 个 token；下面仅展示前缀最后至多 100 个 token，并将当前 token 单列。

```text
awe" moment because this is something that I have been noticing and try to get my Black counterparts to understand all along! I soo appreciate you saying this and breaking it down the issues created
```

|规则|负责专家|实际去向|次名|胜出差额|U 的评分项|移除 U 后去向|
|---|---:|---:|---:|---:|---:|---:|
|A|0|7|4|0.354349|1.91252e-05|7|
|B1|0|4|3|0.0148949|1.91252e-05|4|
|B2|0|4|0|0.00603152|1.91252e-05|4|

**八组原始分数（专家 0→7）**

- A：0.00198154, 0.0141048, 0.0573927, 0.127845, 0.232517, 0.116604, 0.230065, 0.586866
- B1：0.00424624, 0, 0.00366523, 0.00609445, 0.0209894, 0, 0, 0
- B2：0.00423462, 0.00320066, 0.00163513, 0.00164138, 0.0102661, 0, 0, 0

**主要伴随 feature**（按该位置 z×跨层 decoder 范数和排序；不是语义或学习重要性排序）

|feature ID|TRAIN 频率|z|幅度分数|A 组|B1 组|B2 组|
|---:|---:|---:|---:|---:|---:|---:|
|3842|0.2892%|0.11618|1.1879|0|0|0|
|11471|3.3065%|0.1823|0.96974|0|0|0|
|556|57.7560%|0.10786|0.96158|4|0|0|
|516|98.3490%|0.091313|0.88697|7|0|0|
|6470|0.2341%|0.10246|0.80781|0|0|0|
|5147|95.8604%|0.070555|0.73844|7|0|0|
|7388|96.8679%|0.065583|0.72326|7|0|0|
|8345|88.2268%|0.067401|0.72283|7|0|0|

移除 U 只在评分和中去掉该项并保留原分母；没有修改专家输入或模型表征。即使赢家不变，也不能推出 U 对原模型预测无用。

## 卡片 4：feature 9297 / highest_z_unseen_context

- EVAL 行 24669；上下文 117682；绝对 token 偏移 8413311；上下文内位置 127。
- 原文件：`/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；token/target 核对 PASS。
- TRAIN 激活频率：0.232572%；该位置 z=0.146515。
- 当前 token：`3465` / " created"；正确下一 token：`553` / " by"（不参与路由）。
- 模型实际可见 128 个 token；下面仅展示前缀最后至多 100 个 token，并将当前 token 单列。

```text
In order to assess sensitivity to dissonance, we used pleasantness judgements for a set of 24 musical excerpts that were presented in two versions (for a full description, see Peretzet al., 2001). In the original version, the excerpts that comprise a melody and an accompaniment are highly consonant and are taken from pre‐existing classical music (e.g. the first bars of Albinoni’s Adagio). The dissonant version was
```

|规则|负责专家|实际去向|次名|胜出差额|U 的评分项|移除 U 后去向|
|---|---:|---:|---:|---:|---:|---:|
|A|0|7|6|0.258039|8.82028e-05|7|
|B1|0|4|7|0.00974583|8.82028e-05|4|
|B2|0|3|0|0.000964766|8.82028e-05|3|

**八组原始分数（专家 0→7）**

- A：0.0026628, 0.0329793, 0.0529836, 0.0672862, 0.112388, 0.067537, 0.19685, 0.454889
- B1：0.00456388, 0.00368893, 0.0110753, 0.00582467, 0.0387856, 0, 0, 0.0290397
- B2：0.00479711, 0.00203939, 0.000419889, 0.00576188, 0, 0, 0, 0

**主要伴随 feature**（按该位置 z×跨层 decoder 范数和排序；不是语义或学习重要性排序）

|feature ID|TRAIN 频率|z|幅度分数|A 组|B1 组|B2 组|
|---:|---:|---:|---:|---:|---:|---:|
|6118|0.0765%|0.18193|1.6634|-1|-1|-1|
|7388|96.8679%|0.083161|0.91711|7|0|0|
|9297|0.2326%|0.14652|0.81614|0|0|0|
|13373|1.1369%|0.10498|0.79027|0|0|0|
|8060|98.1899%|0.083293|0.75139|7|0|0|
|11364|39.0691%|0.069759|0.73139|3|0|0|
|13964|98.4684%|0.061535|0.6446|7|0|0|
|15664|19.5422%|0.083513|0.62745|1|0|0|

移除 U 只在评分和中去掉该项并保留原分母；没有修改专家输入或模型表征。即使赢家不变，也不能推出 U 对原模型预测无用。

## 卡片 5：feature 1133 / random

- EVAL 行 17769；上下文 117675；绝对 token 偏移 8406402；上下文内位置 386。
- 原文件：`/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；token/target 核对 PASS。
- TRAIN 激活频率：0.215741%；该位置 z=0.066505。
- 当前 token：`264` / " a"；正确下一 token：`5810` / " natural"（不参与路由）。
- 模型实际可见 387 个 token；下面仅展示前缀最后至多 100 个 token，并将当前 token 单列。

```text
ful looks on more than one occasion.

One day, during a break in the Hurricane work, I pinned three of the Grain prints back up on the wall next to each other, but oriented vertically instead of horizontally, because that was the only way they would fit on the available wall space. Once they were up, I couldn’t take my eyes off them.

As I looked at them, something led me to see the flat gray rectangles as light-filled spaces. Was it photographic expectation, the result of
```

|规则|负责专家|实际去向|次名|胜出差额|U 的评分项|移除 U 后去向|
|---|---:|---:|---:|---:|---:|---:|
|A|0|7|6|0.143136|4.17454e-05|7|
|B1|0|4|3|0.0186402|4.17454e-05|4|
|B2|0|6|4|0.0229265|4.17454e-05|6|

**八组原始分数（专家 0→7）**

- A：0.00194993, 0.00860461, 0.0486394, 0.094188, 0.199835, 0.0550634, 0.259908, 0.403044
- B1：0.00362339, 0.00171921, 0.0034786, 0.00386939, 0.0225095, 0, 0, 0
- B2：0.0036436, 0.0013843, 0.00313263, 0.00203707, 0.010132, 0, 0.0330585, 0

**主要伴随 feature**（按该位置 z×跨层 decoder 范数和排序；不是语义或学习重要性排序）

|feature ID|TRAIN 频率|z|幅度分数|A 组|B1 组|B2 组|
|---:|---:|---:|---:|---:|---:|---:|
|15953|2.1689%|0.155|1.8588|0|0|0|
|1963|2.0427%|0.12473|1.2199|0|0|0|
|72|30.1839%|0.10319|0.65984|2|0|0|
|9728|2.0756%|0.084807|0.60524|0|0|0|
|5147|95.8604%|0.054563|0.57108|7|0|0|
|7388|96.8679%|0.049592|0.5469|7|0|0|
|556|57.7560%|0.060984|0.54368|4|0|0|
|516|98.3490%|0.055089|0.5351|7|0|0|

移除 U 只在评分和中去掉该项并保留原分母；没有修改专家输入或模型表征。即使赢家不变，也不能推出 U 对原模型预测无用。

## 卡片 6：feature 1133 / random

- EVAL 行 25504；上下文 117682；绝对 token 偏移 8414146；上下文内位置 962。
- 原文件：`/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；token/target 核对 PASS。
- TRAIN 激活频率：0.215741%；该位置 z=0.0279308。
- 当前 token：`458` / " an"；正确下一 token：`73932` / " octave"（不参与路由）。
- 模型实际可见 963 个 token；下面仅展示前缀最后至多 100 个 token，并将当前 token 单列。

```text
 unable to perceive and interpret musical pitch differences normally. Yet, this is not the result of poor auditory attention or of a deficient affective system in general, since they are able to infer the happy or sad tone of music in a rather consistent manner.

Discrimination of pitch variations (intonation) in speech

Fine‐grained discrimination of pitch is probably more relevant to music processing than to any other domain. Speech intonation contours, for example, use variations in pitch that are larger than half
```

|规则|负责专家|实际去向|次名|胜出差额|U 的评分项|移除 U 后去向|
|---|---:|---:|---:|---:|---:|---:|
|A|0|7|5|0.330274|1.75322e-05|7|
|B1|0|4|2|0.0091514|1.75322e-05|4|
|B2|0|7|0|0.00509424|1.75322e-05|7|

**八组原始分数（专家 0→7）**

- A：0.00362613, 0.015472, 0.0483909, 0.0890587, 0.0410938, 0.189118, 0.0416113, 0.519392
- B1：0.00531609, 0.00438516, 0.0069477, 0.00172732, 0.0160991, 0, 0, 0
- B2：0.00538493, 0.00361146, 0.00297984, 0.00216726, 0, 0, 0, 0.0104792

**主要伴随 feature**（按该位置 z×跨层 decoder 范数和排序；不是语义或学习重要性排序）

|feature ID|TRAIN 频率|z|幅度分数|A 组|B1 组|B2 组|
|---:|---:|---:|---:|---:|---:|---:|
|2402|0.3137%|0.16578|2.1533|0|0|0|
|13964|98.4684%|0.1743|1.8258|7|0|0|
|1115|0.1545%|0.24014|1.1881|0|0|0|
|15512|0.1232%|0.15874|0.99415|-1|-1|-1|
|11382|0.8783%|0.14762|0.80593|0|0|0|
|1456|0.3160%|0.15743|0.74982|0|0|0|
|15953|2.1689%|0.061247|0.73452|0|0|0|
|3950|0.1255%|0.13478|0.69885|-1|-1|-1|

移除 U 只在评分和中去掉该项并保留原分母；没有修改专家输入或模型表征。即使赢家不变，也不能推出 U 对原模型预测无用。

## 卡片 7：feature 1133 / random

- EVAL 行 8369；上下文 117666；绝对 token 偏移 8396985；上下文内位置 185。
- 原文件：`/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；token/target 核对 PASS。
- TRAIN 激活频率：0.215741%；该位置 z=0.038673。
- 当前 token：`264` / " a"；正确下一 token：`2696` / " lot"（不参与路由）。
- 模型实际可见 186 个 token；下面仅展示前缀最后至多 100 个 token，并将当前 token 单列。

```text
 system takes innocent children, turn them into monsters. If Black women think this has nothing to do with them wait until you have a black child, pray its a girl, if its a boy he wont turn 10 before they try to get him into the system.
    Now the administrations call, late as it has been, is timely. But we as black men have to act in our children's interest and defense in order to save their lives and souls. One thing I have been thinking about
```

|规则|负责专家|实际去向|次名|胜出差额|U 的评分项|移除 U 后去向|
|---|---:|---:|---:|---:|---:|---:|
|A|0|7|6|0.287607|2.42751e-05|7|
|B1|0|4|3|0.00212507|2.42751e-05|4|
|B2|0|6|4|0.0258906|2.42751e-05|6|

**八组原始分数（专家 0→7）**

- A：0.00250036, 0.00854397, 0.0330269, 0.0857215, 0.136543, 0.083023, 0.335174, 0.622781
- B1：0.00403991, 0.00512402, 0.00442021, 0.00749939, 0.00962445, 0, 0, 0
- B2：0.0041288, 0.00322688, 0.000915254, 0.0029799, 0.00748174, 0, 0.0333723, 0.00680595

**主要伴随 feature**（按该位置 z×跨层 decoder 范数和排序；不是语义或学习重要性排序）

|feature ID|TRAIN 频率|z|幅度分数|A 组|B1 组|B2 组|
|---:|---:|---:|---:|---:|---:|---:|
|15953|2.1689%|0.2009|2.4093|0|0|0|
|13964|98.4684%|0.12132|1.2709|7|0|0|
|10807|97.3652%|0.15128|1.25|7|0|0|
|76|1.0932%|0.13166|0.9898|0|0|0|
|516|98.3490%|0.081425|0.79092|7|0|0|
|7176|2.3181%|0.091023|0.79055|0|0|0|
|8345|88.2268%|0.071551|0.76734|7|0|0|
|5147|95.8604%|0.070677|0.73972|7|0|0|

移除 U 只在评分和中去掉该项并保留原分母；没有修改专家输入或模型表征。即使赢家不变，也不能推出 U 对原模型预测无用。

## 卡片 8：feature 1133 / highest_z_unseen_context

- EVAL 行 296；上下文 117658；绝对 token 偏移 8388904；上下文内位置 296。
- 原文件：`/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；token/target 核对 PASS。
- TRAIN 激活频率：0.215741%；该位置 z=0.085548。
- 当前 token：`264` / " a"；正确下一 token：`7653` / " leader"（不参与路由）。
- 模型实际可见 297 个 token；下面仅展示前缀最后至多 100 个 token，并将当前 token 单列。

```text
 he's Mr. Right and not Mr. Right Now) and how to just "GROW" with the flow. And please, don't mistake a "Grown Boy" for a"Knight In Shinning Armor". Quality Black men today should NOT be held accountable for "what you allowed" some grown boy to do to you in the past. This is also a major problem for most Black women today! They don't know what a real man is, especially in the form of
```

|规则|负责专家|实际去向|次名|胜出差额|U 的评分项|移除 U 后去向|
|---|---:|---:|---:|---:|---:|---:|
|A|0|7|6|0.215728|5.36987e-05|7|
|B1|0|4|2|0.0044531|5.36987e-05|4|
|B2|0|0|2|0.00251552|5.36987e-05|0|

**八组原始分数（专家 0→7）**

- A：0.00187083, 0.0164933, 0.0433214, 0.0867204, 0.0485769, 0.101747, 0.364617, 0.580344
- B1：0.0037149, 0.000647208, 0.00502834, 0.00190475, 0.00948145, 0, 0, 0
- B2：0.00378618, 0.00030578, 0.00127066, 0, 0, 0, 0, 0

**主要伴随 feature**（按该位置 z×跨层 decoder 范数和排序；不是语义或学习重要性排序）

|feature ID|TRAIN 频率|z|幅度分数|A 组|B1 组|B2 组|
|---:|---:|---:|---:|---:|---:|---:|
|15953|2.1689%|0.1589|1.9057|0|0|0|
|516|98.3490%|0.11756|1.1419|7|0|0|
|5913|95.1848%|0.077507|0.79468|7|0|0|
|13830|81.1593%|0.065174|0.66413|6|0|0|
|5147|95.8604%|0.062498|0.65412|7|0|0|
|7415|94.7702%|0.067559|0.5958|7|0|0|
|1960|41.9426%|0.058454|0.56186|3|0|0|
|1963|2.0427%|0.05344|0.52264|0|0|0|

移除 U 只在评分和中去掉该项并保留原分母；没有修改专家输入或模型表征。即使赢家不变，也不能推出 U 对原模型预测无用。

## 卡片 9：feature 2704 / random

- EVAL 行 56828；上下文 117713；绝对 token 偏移 8445541；上下文内位置 613。
- 原文件：`/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；token/target 核对 PASS。
- TRAIN 激活频率：0.202736%；该位置 z=0.0233975。
- 当前 token：`700` / " out"；正确下一 token：`4217` / " players"（不参与路由）。
- 模型实际可见 614 个 token；下面仅展示前缀最后至多 100 个 token，并将当前 token 单列。

```text
. It's also helpful that the Hornets, Jazz and Nuggets are absolute disasters right now.

They're really just barely gotten by too during this little win streak, even having to max out their starters minutes.

With 17 out of the 26 against +.500 teams it's gonna be rough for Portland. However, knowing Blazer fans, they will point to Roy's return and not the level of competition. When you're 27th in rebounding, maxing
```

|规则|负责专家|实际去向|次名|胜出差额|U 的评分项|移除 U 后去向|
|---|---:|---:|---:|---:|---:|---:|
|A|0|7|6|0.288302|1.37146e-05|7|
|B1|0|2|3|0.00145434|1.37146e-05|2|
|B2|0|0|2|0.0024927|1.37146e-05|0|

**八组原始分数（专家 0→7）**

- A：0.00244888, 0.0186589, 0.0616161, 0.108287, 0.154295, 0.110847, 0.357886, 0.646189
- B1：0.00469774, 0.00340555, 0.00821758, 0.00676324, 0, 0, 0, 0
- B2：0.0048459, 0.0011441, 0.0023532, 0, 0, 0, 0, 0

**主要伴随 feature**（按该位置 z×跨层 decoder 范数和排序；不是语义或学习重要性排序）

|feature ID|TRAIN 频率|z|幅度分数|A 组|B1 组|B2 组|
|---:|---:|---:|---:|---:|---:|---:|
|14199|0.2295%|0.20852|1.8026|0|0|0|
|16242|3.6424%|0.24118|1.4575|0|0|0|
|5913|95.1848%|0.092644|0.94988|7|0|0|
|516|98.3490%|0.097783|0.94981|7|0|0|
|7415|94.7702%|0.10442|0.92091|7|0|0|
|8345|88.2268%|0.075458|0.80924|7|0|0|
|11046|39.9986%|0.087322|0.77845|3|0|0|
|13964|98.4684%|0.071544|0.74946|7|0|0|

移除 U 只在评分和中去掉该项并保留原分母；没有修改专家输入或模型表征。即使赢家不变，也不能推出 U 对原模型预测无用。

## 卡片 10：feature 2704 / random

- EVAL 行 45582；上下文 117702；绝对 token 偏移 8434270；上下文内位置 606。
- 原文件：`/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；token/target 核对 PASS。
- TRAIN 激活频率：0.202736%；该位置 z=0.0163175。
- 当前 token：`1933` / "land"；正确下一 token：`812` / "ish"（不参与路由）。
- 模型实际可见 607 个 token；下面仅展示前缀最后至多 100 个 token，并将当前 token 单列。

```text
 as the snack of choice in movie theaters worldwide (yes, korea, its even better than that toasted dried squid!).

i usually like really simple and fresh sashimi and nigiri. i'm not opposed to american style maki rolls, but they just don't really appeal when they have five kinds of fish, are deep-fried, slathered in spicy mayo with tiled avocado armor. i want a place in SF that has GOOD fish, but might also serve up more creative or out
```

|规则|负责专家|实际去向|次名|胜出差额|U 的评分项|移除 U 后去向|
|---|---:|---:|---:|---:|---:|---:|
|A|0|7|5|0.20874|9.56458e-06|7|
|B1|0|6|4|0.0127165|9.56458e-06|6|
|B2|0|7|4|0.00608587|9.56458e-06|7|

**八组原始分数（专家 0→7）**

- A：0.00455239, 0.0597645, 0.0311199, 0.0803885, 0.0567074, 0.353391, 0, 0.562131
- B1：0.00690506, 0.00498418, 0.00772712, 0.00593734, 0.0198312, 0, 0.0325477, 0
- B2：0.00681697, 0.0111599, 0.00337028, 0.00773855, 0.0195694, 0, 0, 0.0256553

**主要伴随 feature**（按该位置 z×跨层 decoder 范数和排序；不是语义或学习重要性排序）

|feature ID|TRAIN 频率|z|幅度分数|A 组|B1 组|B2 组|
|---:|---:|---:|---:|---:|---:|---:|
|13964|98.4684%|0.15525|1.6264|7|0|0|
|10807|97.3652%|0.16056|1.3267|7|0|0|
|169|2.2026%|0.1701|1.126|0|0|0|
|1107|16.9587%|0.082085|0.77916|1|0|0|
|11894|0.3213%|0.11704|0.77275|0|0|0|
|1712|23.5204%|0.077612|0.75641|1|0|0|
|14|66.6840%|0.081296|0.73746|5|2|0|
|16231|22.1296%|0.075076|0.72186|1|0|0|

移除 U 只在评分和中去掉该项并保留原分母；没有修改专家输入或模型表征。即使赢家不变，也不能推出 U 对原模型预测无用。

## 卡片 11：feature 2704 / random

- EVAL 行 54620；上下文 117711；绝对 token 偏移 8443327；上下文内位置 447。
- 原文件：`/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；token/target 核对 PASS。
- TRAIN 激活频率：0.202736%；该位置 z=0.0248624。
- 当前 token：`2267` / "oh"；正确下一 token：`323` / " and"（不参与路由）。
- 模型实际可见 448 个 token；下面仅展示前缀最后至多 100 个 token，并将当前 token 单列。

```text
 It kind of got it right, too.
You need to go to an art forum to discuss whatever it is you're on about. You use a camera to create whatever you want. Maybe don't worry about what photographers are up to or interested in and don't bother trying to define something that you haven't really thought through

Reservoir Dan

Someone who buys a limited edition artwork does so because they love the piece and want it in their life in some capacity. The general public may still o
```

|规则|负责专家|实际去向|次名|胜出差额|U 的评分项|移除 U 后去向|
|---|---:|---:|---:|---:|---:|---:|
|A|0|7|4|0.380947|1.45732e-05|7|
|B1|0|4|2|0.00917661|1.45732e-05|4|
|B2|0|4|2|0.00545672|1.45732e-05|4|

**八组原始分数（专家 0→7）**

- A：0.00424818, 0.055697, 0.0396901, 0.116578, 0.293765, 0.247082, 0.15714, 0.674712
- B1：0.00700111, 0.00648929, 0.010481, 0.00483754, 0.0196576, 0, 0, 0
- B2：0.0068984, 0.0108548, 0.0114007, 0.00493781, 0.0168575, 0, 0, 0.00595395

**主要伴随 feature**（按该位置 z×跨层 decoder 范数和排序；不是语义或学习重要性排序）

|feature ID|TRAIN 频率|z|幅度分数|A 组|B1 组|B2 组|
|---:|---:|---:|---:|---:|---:|---:|
|13964|98.4684%|0.14354|1.5036|7|0|0|
|10807|97.3652%|0.16788|1.3872|7|0|0|
|8232|0.9976%|0.17698|1.0385|0|0|0|
|7768|2.0916%|0.10912|1.0255|0|0|0|
|16|50.2112%|0.11527|0.97515|4|0|0|
|12439|2.7082%|0.14446|0.9251|0|0|0|
|5147|95.8604%|0.078733|0.82404|7|0|0|
|1955|0.4544%|0.095372|0.80525|0|0|0|

移除 U 只在评分和中去掉该项并保留原分母；没有修改专家输入或模型表征。即使赢家不变，也不能推出 U 对原模型预测无用。

## 卡片 12：feature 2704 / highest_z_unseen_context

- EVAL 行 10861；上下文 117668；绝对 token 偏移 8399479；上下文内位置 631。
- 原文件：`/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；token/target 核对 PASS。
- TRAIN 激活频率：0.202736%；该位置 z=0.305868。
- 当前 token：`700` / " out"；正确下一 token：`279` / " the"（不参与路由）。
- 模型实际可见 632 个 token；下面仅展示前缀最后至多 100 个 token，并将当前 token 单列。

```text
 know that we both gave it 110%... I don't like the idea of him taking the lead. We share it. He can't let me down, nor can I let him down. It's a team in all things.

  34. I think it has something to do with the fast lifestyle in the cities these days, I would say it is best to meet single black men on dating sites like, it helps to make an informed decision there as you can check
```

|规则|负责专家|实际去向|次名|胜出差额|U 的评分项|移除 U 后去向|
|---|---:|---:|---:|---:|---:|---:|
|A|0|7|6|0.258346|0.000179287|7|
|B1|0|4|2|0.0247444|0.000179287|4|
|B2|0|4|3|0.00110646|0.000179287|4|

**八组原始分数（专家 0→7）**

- A：0.00229956, 0.0188255, 0.0586058, 0.187715, 0.0851547, 0.0619968, 0.23413, 0.492476
- B1：0.00444809, 0.00379885, 0.0127937, 0.0103627, 0.0375381, 0, 0, 0
- B2：0.0045278, 0.00181083, 0.00728483, 0.0189554, 0.0200619, 0, 0, 0.0155085

**主要伴随 feature**（按该位置 z×跨层 decoder 范数和排序；不是语义或学习重要性排序）

|feature ID|TRAIN 频率|z|幅度分数|A 组|B1 组|B2 组|
|---:|---:|---:|---:|---:|---:|---:|
|2704|0.2027%|0.30587|1.6589|0|0|0|
|14199|0.2295%|0.13137|1.1356|0|0|0|
|1960|41.9426%|0.097272|0.93499|3|0|0|
|5147|95.8604%|0.08264|0.86493|7|0|0|
|116|0.3175%|0.16243|0.8527|0|2|0|
|5913|95.1848%|0.072625|0.74462|7|0|0|
|8345|88.2268%|0.067645|0.72545|7|0|0|
|10343|0.0612%|0.096286|0.65162|-1|-1|-1|

移除 U 只在评分和中去掉该项并保留原分母；没有修改专家输入或模型表征。即使赢家不变，也不能推出 U 对原模型预测无用。


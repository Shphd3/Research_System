# S13共享结构：真实文本、七区域与反例

所有案例均为已看过S13确认数据的探索复查；原文不改。完整成员z/q见results/case_member_values.csv；名单差不是语义专属。

## first：MLPIN_SAE / animal / N004

**animal，读取冒号零起索引23，token ID 25**

```text
A curtain briefly exposed a picture of an animal before closing again. The viewer is trying to describe the subject.
Description:
```

**vehicle，读取冒号零起索引23，token ID 25**

```text
A curtain briefly exposed a picture of a vehicle before closing again. The viewer is trying to describe the subject.
Description:
```

**cat，读取冒号零起索引23，token ID 25**

```text
A curtain briefly exposed a picture of a cat before closing again. The viewer is trying to describe the subject.
Description:
```

**dog，读取冒号零起索引23，token ID 25**

```text
A curtain briefly exposed a picture of a dog before closing again. The viewer is trying to describe the subject.
Description:
```

粗共有25，细共有27，保留23、仅粗共有2、细类额外4；Q粗36.260%→细33.759%，粗−细+2.501pp。

### coarse_fine

- retained：23个；ID：808, 861, 966, 2189, 2260, 4700, 8856, 11190, 11291, 12027, 14202, 14481, 14913, 15788, 16240, 16905, 17390, 21902, 27101, 29188, 29342, 29479, 29506。

- coarse_only：2个；ID：15123, 27974。

- fine_extra：4个；ID：1683, 22309, 24399, 27076。

### parent_children

- PAB：26个；ID：808, 861, 966, 1683, 2189, 2260, 4700, 8856, 11190, 11291, 12027, 14202, 14481, 14913, 15788, 16240, 16905, 17390, 21902, 24399, 27076, 27101, 29188, 29342, 29479, 29506。

- AB_only：1个；ID：22309。

- PB_only：2个；ID：2491, 27974。

- P_only：4个；ID：15123, 16425, 28550, 29893。

- A_only：5个；ID：5196, 8917, 10167, 11234, 22958。

- B_only：3个；ID：6288, 17366, 24428。

## median_animal：MLPIN_SAE / animal / N048

**animal，读取冒号零起索引24，token ID 25**

```text
The exhibit case was empty, but its note referred to an animal. A visitor asked what should have been there.
Description:
```

**vehicle，读取冒号零起索引24，token ID 25**

```text
The exhibit case was empty, but its note referred to a vehicle. A visitor asked what should have been there.
Description:
```

**cat，读取冒号零起索引24，token ID 25**

```text
The exhibit case was empty, but its note referred to a cat. A visitor asked what should have been there.
Description:
```

**dog，读取冒号零起索引24，token ID 25**

```text
The exhibit case was empty, but its note referred to a dog. A visitor asked what should have been there.
Description:
```

粗共有23，细共有30，保留22、仅粗共有1、细类额外8；Q粗45.138%→细38.016%，粗−细+7.122pp。

### coarse_fine

- retained：22个；ID：808, 861, 966, 2189, 4700, 5196, 8048, 8856, 9315, 11190, 11234, 14187, 14481, 14913, 17390, 19327, 21902, 27346, 27373, 28842, 29342, 29506。

- coarse_only：1个；ID：10385。

- fine_extra：8个；ID：3, 6585, 8351, 10580, 11291, 16240, 17366, 24399。

### parent_children

- PAB：28个；ID：808, 861, 966, 2189, 4700, 5196, 6585, 8048, 8351, 8856, 9315, 10580, 11190, 11234, 11291, 14187, 14481, 14913, 17366, 17390, 19327, 21902, 24399, 27346, 27373, 28842, 29342, 29506。

- AB_only：2个；ID：3, 16240。

- PB_only：1个；ID：10385。

- P_only：3个；ID：21807, 26060, 29301。

- A_only：2个；ID：416, 22958。

- B_only：1个；ID：15844。

## low_retention_domain：ATTN_SAE / fruit / N038

**fruit，读取冒号零起索引26，token ID 25**

```text
The replacement image is supposed to show a fruit, but no example was attached to the request. A written description is needed.
Description:
```

**furniture，读取冒号零起索引28，token ID 25**

```text
The replacement image is supposed to show a piece of furniture, but no example was attached to the request. A written description is needed.
Description:
```

**apple，读取冒号零起索引26，token ID 25**

```text
The replacement image is supposed to show an apple, but no example was attached to the request. A written description is needed.
Description:
```

**banana，读取冒号零起索引26，token ID 25**

```text
The replacement image is supposed to show a banana, but no example was attached to the request. A written description is needed.
Description:
```

粗共有18，细共有23，保留14、仅粗共有4、细类额外9；Q粗20.343%→细14.855%，粗−细+5.488pp。

### coarse_fine

- retained：14个；ID：2254, 2855, 3261, 4647, 5567, 9522, 9785, 14769, 20439, 22428, 23809, 23899, 23935, 29907。

- coarse_only：4个；ID：17795, 17808, 22625, 27162。

- fine_extra：9个；ID：489, 3371, 5823, 9117, 17070, 17521, 17862, 18647, 25186。

### parent_children

- PAB：21个；ID：2254, 2855, 3261, 3371, 4647, 5567, 9117, 9522, 9785, 14769, 17070, 17521, 17862, 18647, 20439, 22428, 23809, 23899, 23935, 25186, 29907。

- AB_only：2个；ID：489, 5823。

- PA_only：4个；ID：165, 4300, 9438, 17808。

- PB_only：1个；ID：27162。

- P_only：6个；ID：1736, 14577, 17795, 22267, 22625, 26856。

- A_only：5个；ID：9302, 11052, 11981, 26729, 28127。

- B_only：8个；ID：519, 1016, 1561, 2520, 5897, 7317, 9270, 20922。

## animal_counterexample：MLPIN_SAE / animal / N007

**animal，读取冒号零起索引24，token ID 25**

```text
Two friends remembered the background differently, yet both recalled an animal in the foreground. They now need a neutral description.
Description:
```

**vehicle，读取冒号零起索引24，token ID 25**

```text
Two friends remembered the background differently, yet both recalled a vehicle in the foreground. They now need a neutral description.
Description:
```

**cat，读取冒号零起索引24，token ID 25**

```text
Two friends remembered the background differently, yet both recalled a cat in the foreground. They now need a neutral description.
Description:
```

**dog，读取冒号零起索引24，token ID 25**

```text
Two friends remembered the background differently, yet both recalled a dog in the foreground. They now need a neutral description.
Description:
```

粗共有22，细共有27，保留17、仅粗共有5、细类额外10；Q粗42.005%→细43.765%，粗−细-1.760pp。

### coarse_fine

- retained：17个；ID：861, 4700, 5196, 8048, 8917, 11190, 14481, 14536, 15400, 16240, 21902, 22309, 24884, 25748, 27076, 29342, 29506。

- coarse_only：5个；ID：3803, 14202, 16425, 22965, 29893。

- fine_extra：10个；ID：2280, 2432, 8856, 9139, 11536, 14753, 17366, 17390, 24406, 29479。

### parent_children

- PAB：23个；ID：861, 2280, 4700, 5196, 8048, 8856, 8917, 11190, 11536, 14481, 14536, 15400, 16240, 17366, 17390, 21902, 22309, 24406, 24884, 25748, 27076, 29342, 29506。

- AB_only：4个；ID：2432, 9139, 14753, 29479。

- PA_only：1个；ID：14202。

- PB_only：2个；ID：3803, 29893。

- P_only：6个；ID：14879, 16425, 18809, 22965, 24399, 25899。

- A_only：4个；ID：808, 3130, 11234, 22958。

- B_only：3个；ID：4678, 7258, 14913。

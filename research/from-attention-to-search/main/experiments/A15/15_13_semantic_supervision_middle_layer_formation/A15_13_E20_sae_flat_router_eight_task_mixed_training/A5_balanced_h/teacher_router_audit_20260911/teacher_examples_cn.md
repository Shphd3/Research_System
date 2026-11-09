# A5 教师最高激活文本审阅

本表是按固定规则自动选例后的AI解释，不是全组盲标结论。编号为0–7。原始组质量是该位置所有属于此组的正激活之和；q是各组质量归一化后的概率。显示上下文是模型已经看到的因果前缀，下一词元只供读者理解，未喂给Router。完整96个原始质量排序例及40个相对质量排序例（有重叠）见执行工作区 `teacher_examples.json`。

## 组0

**候选共同性与边界：** 若干词内前缀续写（sh、Mel、Sh）；没有统一任务语义。

**原始质量第1例**：gsm8k；质量 161.941；q=0.481；位置92；实际最大概率组0。
记录：`openai/gsm8k@740312add88f781978c0658806c59bc2815b9866:main/test-00000-of-00001.parquet:639`

```text
 it takes him 3 seconds to shovel a cubic foot of earth, how long will it take him to dig the hole?
Answer:
The hole is 6 feet long by 4 feet wide by 3 feet deep or 6 * 4 * 3 = <<6*4*3=72>>72 cubic feet. Bob sh
```
下一词元：`ov`

**原始质量第2例**：gsm8k；质量 150.129；q=0.421；位置68；实际最大概率组0。
记录：`openai/gsm8k@740312add88f781978c0658806c59bc2815b9866:main/train-00000-of-00001.parquet:2994`

```text
Nadine's dog rolls around in the mud. She spends 10 minutes hosing him off outside, then shampoos him three times, which takes 15 minutes per shampoo. How long does she spend cleaning her dog total?
Answer:
First find the total shampoo time: 15 minutes/shampoo * 3 sh
```
下一词元：`ampo`

**原始质量第3例**：math；质量 131.070；q=0.432；位置86；实际最大概率组0。
记录：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:prealgebra/test-00000-of-00001.parquet:142`

```text
 decided to shake hands with each of the sorcerers. None of the witches bothered to shake each other's hands, since they are all good friends already, and the sorcerers all sort of hate each other and did not shake hands with other sorcerers. How many handshakes took place at the mixer?
Solution:
The only handsh
```
下一词元：`akes`

**相对质量最高例（检验排序是否改变直觉）**：
```text
 mom puts toothpicks in her sandwiches when she serves them for lunch. Melanie started saving them and has saved 10 toothpicks each week for the past 12 weeks. If she continues saving toothpicks at the same rate, how many more weeks will it take her to collect 200 toothpicks?
Answer:
Mel
```
下一词元：`anie`；q=0.525。

## 组1

**候选共同性与边界：** 短提示边界与通用续写；最高12例可见上下文完全相同，为冒号加换行。

**原始质量第1例**：math；质量 980.953；q=1.000；位置0；实际最大概率组1。
记录：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:algebra/train-00000-of-00001.parquet:1021`

```text
:

```
下一词元：`First`

**原始质量第2例**：math；质量 980.953；q=1.000；位置0；实际最大概率组1。
记录：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:algebra/train-00000-of-00001.parquet:1379`

```text
:

```
下一词元：`An`

**原始质量第3例**：math；质量 980.953；q=1.000；位置0；实际最大概率组1。
记录：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:algebra/train-00000-of-00001.parquet:191`

```text
:

```
下一词元：`If`

**相对质量最高例（检验排序是否改变直觉）**：
```text
Which of the following is true of hypothyroidism?
A. Weight loss
B. Pre-tibial myxoedema
C. A raised TSH level
D. An aversion to warm places
Answer:
C
```
下一词元：`<|endoftext|>`；q=1.000。

## 组2

**候选共同性与边界：** 算式/解题格式，如 <<、>>；有其他代码反例。

**原始质量第1例**：math；质量 185.242；q=0.426；位置29；实际最大概率组2。
记录：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:geometry/train-00000-of-00001.parquet:571`

```text
:
[asy] /* Geogebra to Asymptote conversion, documentation at artofproblemsolving.com/Wiki, go to User:
```
下一词元：`Az`

**原始质量第2例**：gsm8k；质量 160.395；q=0.587；位置187；实际最大概率组2。
记录：`openai/gsm8k@740312add88f781978c0658806c59bc2815b9866:main/train-00000-of-00001.parquet:5519`

```text
 students were asked to bring in 24 cookies each so that’s 20*24 = <<20*24=480>>480 cookies 15 students were asked to bring in 12 donuts each so that’s 15*12 = <<15*12=180
```
下一词元：`>>`

**原始质量第3例**：gsm8k；质量 159.172；q=0.509；位置181；实际最大概率组2。
记录：`openai/gsm8k@740312add88f781978c0658806c59bc2815b9866:main/train-00000-of-00001.parquet:218`

```text
30 cents. A quarter is worth 25 cents so his quarters amount to 8 x 25 = <<8*25=200>>200 cents. A dime is worth 10 cents so his dimes amount to 12 x 10 = <<12*10=120
```
下一词元：`>>`

**相对质量最高例（检验排序是否改变直觉）**：
```text
 students were asked to bring in 24 cookies each so that’s 20*24 = <<20*24=480>>480 cookies 15 students were asked to bring in 12 donuts each so that’s 15*12 = <<15*12=180
```
下一词元：`>>`；q=0.587。

## 组3

**候选共同性与边界：** 公式、数值续写较突出，但覆盖面很广。

**原始质量第1例**：math；质量 264.688；q=0.894；位置227；实际最大概率组3。
记录：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:geometry/train-00000-of-00001.parquet:476`

```text
agons, which violate the problem statement. Letting $F = (f,4)$, and knowing that $\angle FAB = 120^\circ$, we can use rewrite $F$ using complex numbers: $f + 4 i = (b + 2 i)\left(e^{i(2 \pi / 3
```
下一词元：`)}`

**原始质量第2例**：math；质量 260.695；q=0.879；位置98；实际最大概率组3。
记录：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:intermediate_algebra/test-00000-of-00001.parquet:170`

```text
 difference between the largest and smallest possible values of $\left| b \right|$?
Solution:
After a bit of algebra, we obtain: \[h(z)=g(g(z))=f(f(f(f(z))))=\frac{Pz+Q}{Rz+S},\]where $P=(a+1)^2+a(b+1
```
下一词元：`)^`

**原始质量第3例**：math；质量 258.723；q=0.901；位置197；实际最大概率组3。
记录：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:intermediate_algebra/train-00000-of-00001.parquet:1205`

```text
54}{x^2+5x+6} = \frac{9x^2 - 3x}{x^2 + 5x + 6}= \frac{3x(3x-1)}{(x+3)(x+2)}\]It becomes obvious that $F(x) = ax(x-1
```
下一词元：`)$`

**相对质量最高例（检验排序是否改变直觉）**：
```text
 our second equation gives $12-d^2=21$, so $d^2=-9$ and $d=\pm 3i$. Therefore, the roots of the cubic are $2-3i$, $2$, and $2+3i$, so $$a = -2(2-3i)(2+3i
```
下一词元：`)`；q=0.984。

## 组4

**候选共同性与边界：** 绘图代码 [asy] 的词法/标点，例子共同性较清楚。

**原始质量第1例**：math；质量 197.953；q=0.508；位置295；实际最大概率组4。
记录：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:geometry/test-00000-of-00001.parquet:38`

```text
$ is isosceles. Thus, the measure of angle $ACD$ is $90 - 21 = \boxed{69\text{ degrees}}$, which is the same as the two base angles of triangle ABC. [asy] import olympiad; import geometry; size(150); defaultpen(lin
```
下一词元：`ewidth`

**原始质量第2例**：math；质量 195.039；q=0.510；位置59；实际最大概率组4。
记录：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:geometry/test-00000-of-00001.parquet:334`

```text
:
Let Earth's radius be $r$. Since the equator measures 25100 miles, we have $2\pi r = 25100 \Rightarrow r = \frac{12550}{\pi}$. [asy] defaultpen(lin
```
下一词元：`ewidth`

**原始质量第3例**：math；质量 188.629；q=0.503；位置157；实际最大概率组4。
记录：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:prealgebra/train-00000-of-00001.parquet:1038`

```text
 $MF$ is perpendicular to $CD$, so $\triangle MFC$ is a right triangle. Now, if we can find the lengths of $MF$ and $FC$, we can use the Pythagorean Theorem to find the length of $MC$. [asy] size(4cm); dotfactor = 4; defaultpen(lin
```
下一词元：`ewidth`

**相对质量最高例（检验排序是否改变直觉）**：
```text
2)); draw(graph(lowerparab,0,2)); draw(reflect((0,0),(0,1))*graph(upperparab,0,2)); draw(reflect((0,0),(0,1))*graph(lowerparab,0,2)); draw((1,sqrt(3))--(1,-sqrt(3))
```
下一词元：`--`；q=0.568。

## 组5

**候选共同性与边界：** 相对质量最高例集中在否定缩写 isn/aren/hadn；原始质量最高例并不全属此类。

**原始质量第1例**：math；质量 137.086；q=0.401；位置238；实际最大概率组5。
记录：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:counting_and_probability/test-00000-of-00001.parquet:425`

```text
 $2^6$ ways to leave the left-turn lane empty. The same logic gives $2^6$ ways to leave the center lane and right-turn lane open. But we have double-counted the situations where two lanes are left empty. Fortunately, since each driver must go into the third lane, there are only 3 situations we have over
```
下一词元：`-count`

**原始质量第2例**：gsm8k；质量 135.758；q=0.465；位置144；实际最大概率组5。
记录：`openai/gsm8k@740312add88f781978c0658806c59bc2815b9866:main/train-00000-of-00001.parquet:6341`

```text
 today?
Answer:
The total lead time for the cargo is 21 days on water + 4 in customs + 7 to the warehouse or 21+4+7 = <<21+4+7=32>>32 days If the warehouse is expecting the cargo in 2 days from today then the cargo should have already
```
下一词元：` completed`

**原始质量第3例**：math；质量 127.332；q=0.437；位置38；实际最大概率组5。
记录：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:prealgebra/train-00000-of-00001.parquet:200`

```text
Subtract $111.11$ from $333.33.$ Express the result as a decimal to the nearest hundredth.
Solution:
We can organize the subtraction conc
```
下一词元：`is`

**相对质量最高例（检验排序是否改变直觉）**：
```text
,8)--(-6.5,4)--(-10,0)--(-8,-2); draw(a); draw(shift((4,0))*a); draw(shift((8,0))*a); draw(shift((12,0))*a); draw(shift((16,0))*a); [/asy]
Solution:
Clearly one color isn
```
下一词元：`'t`；q=0.605。

## 组6

**候选共同性与边界：** Tr、Compar等词内/名称续写；共同性不足以命名任务类别。

**原始质量第1例**：gsm8k；质量 149.422；q=0.394；位置79；实际最大概率组1。
记录：`openai/gsm8k@740312add88f781978c0658806c59bc2815b9866:main/train-00000-of-00001.parquet:4872`

```text
 school's dance team and has to braid 8 dancers' hair. If each dancer has five braids and each braid takes 30 seconds, how many minutes will it take to braid all the dancers' hair?
Answer:
First find the total number of braids among all the dancers: 8 dancers * 5 braids/d
```
下一词元：`ancer`

**原始质量第2例**：math；质量 129.137；q=0.426；位置344；实际最大概率组6。
记录：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:precalculus/test-00000-of-00001.parquet:354`

```text
) = 3.$ Therefore, the graph of $y = \cos x + \cos 2x + \cos 3x$ repeats with period $\boxed{2 \pi}.$ The graph of $y = \cos x + \cos 2x + \cos 3x$ is shown below: [asy]import Tr
```
下一词元：`ig`

**原始质量第3例**：math；质量 122.605；q=0.397；位置120；实际最大概率组6。
记录：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:precalculus/train-00000-of-00001.parquet:403`

```text
pi}{2}$ to $\frac{\pi}{2},$ which means $x$ ranges from $-\pi$ to $\pi.$ Thus, the period is $\pi - (-\pi) = \boxed{2 \pi}.$ The graph of $y=\tan \frac{x}{2}$ is shown below: [asy]import Tr
```
下一词元：`ig`

**相对质量最高例（检验排序是否改变直觉）**：
```text
Trinity sells magazines at 11/8 of the price she bought the magazines. If she bought the magazines at $72, what is her profit?
Answer:
Tr
```
下一词元：`inity`；q=0.435。

## 组7

**候选共同性与边界：** 人名Iris/Ivan与道德选择题等混合；不能给出可信统一语义名。

**原始质量第1例**：gsm8k；质量 78.574；q=0.333；位置99；实际最大概率组7。
记录：`openai/gsm8k@740312add88f781978c0658806c59bc2815b9866:main/train-00000-of-00001.parquet:3369`

```text
0 blueberries, her sister picked 20 cranberries, and her brother was able to pick 10 raspberries. If 1/3 of the total berries they were able to pick are rotten and the remaining 1/2 of the fresh berries need to be kept, how many berries will they be able to sell?
Answer:
I
```
下一词元：`ris`

**原始质量第2例**：gsm8k；质量 67.502；q=0.299；位置47；实际最大概率组7。
记录：`openai/gsm8k@740312add88f781978c0658806c59bc2815b9866:main/train-00000-of-00001.parquet:6502`

```text
Ivan has a piggy bank that can hold 100 pennies and 50 dimes. How much, in dollars, does Ivan have if he has filled his two piggy banks with those coins?
Answer:
I
```
下一词元：`van`

**原始质量第3例**：math；质量 60.430；q=0.215；位置165；实际最大概率组1。
记录：`EleutherAI/hendrycks_math@21a5633873b6a120296cce3e2df9d5550074f4a3:counting_and_probability/train-00000-of-00001.parquet:368`

```text
 + n$.
Solution:
Note that the probability that Club Truncator will have more wins than losses is equal to the probability that it will have more losses than wins; the only other possibility is that they have the same number of wins and losses. Thus, by the complement principle, the desired probability is half the probability that Club Truncator does
```
下一词元：` not`

**相对质量最高例（检验排序是否改变直觉）**：
```text
0 blueberries, her sister picked 20 cranberries, and her brother was able to pick 10 raspberries. If 1/3 of the total berries they were able to pick are rotten and the remaining 1/2 of the fresh berries need to be kept, how many berries will they be able to sell?
Answer:
I
```
下一词元：`ris`；q=0.333。


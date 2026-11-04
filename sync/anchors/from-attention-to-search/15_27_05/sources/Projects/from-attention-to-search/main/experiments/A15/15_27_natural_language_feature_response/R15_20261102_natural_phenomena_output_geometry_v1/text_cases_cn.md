# R15真实文本：支持例、反例与未解释例

以下是按公开规则选出的诊断例，不代替总体统计。正例按发现阶段关联方向，取验证集符合现象的高响应或低响应位置；反例同时保留与该预测不符或不具专属性的位置。正方向的高响应槽位要求非零，找不到时明确记未找到。无法解释例按发现精读固定为成员6743：screw、choked等高响应前文没有得到一致可复查命名，不依据验证结果另挑。四个正式feature候选整体未通过验证；这里的正例只指与发现方向一致的个别配对，不表示功能解释成立。完整可见前文保留到当前token为止；没有用后文命名。

文字片段编号是分词器整数；feature编号是字典成员整数；两者不是同一类对象。片段可能不是完整词。

## 1．近期非ASCII字母／counter_low_without_property

文档`R15_mathematics_136`；位置229；来源[www.maa.org](https://www.maa.org/press/periodicals/american-mathematical-monthly/american-mathematical-monthly-february-2010)；validation；完整来源行7053。当前片段`
`，文字片段编号198；成员11424，系数0。

完整可见前文：

```text
You are here

American Mathematical Monthly -February 2010

February 2010

A Dynamical System Using the Voronoï Tessellation
By: Natalie Priebe Frank and Sean M. Hart,
There are many good reasons to make a tiling around some discrete set of points. For example, maybe you need to know what regions are served by some set of post offices or cell phone satellites. Once you have a tiling, there are many reasons to define a point set with it. For instance, you might want to decorate each tile with a few points to create or destroy symmetry, or to obtain combinatorial information. Since you can go from point sets to tilings and back again, you might come across some interesting ways to associate one set of points to another. Once you have a map from a class of objects back to itself, you can take a dynamical systems viewpoint to analyze the situation. This paper does exactly that, with a new dynamical system based on the vertices of Voronoï tessellations.


Variations on Kuratowski's 14-Set Theorem

```

同文档、相同当前文字片段的匹配参照（当前位置33；成员系数0.0）：

```text
You are here

American Mathematical Monthly -February 2010

February 2010

A Dynamical System Using the Voronoï Tessellation

```

这对真实上下文的变化：归一化前向量差长度230.047，归一化后长度46.8565，去共同平移后的logit均方根变化1.29633；单位归一化后变化的输出增益0.0276659，相对各向同性方向参照0.9622倍。它是两个实际上下文全部变化的读出，不能归因于单一文字线索或单个成员。

可复查属性：近期非ASCII字母。规则只查可见前文；它是词面／格式描述，不是纯语义金标。该例属性判定为False。高响应反例说明该成员并非该属性专有；低响应反例说明该属性也不保证该成员激活。竞争解释包括此前其他词、位置和句式；同token配对统计及其四分位敏感性见主报告。

## 2．定义或命名短语／support_low_with_property

文档`R15_biology_114`；位置452；来源[fsdinfo.org](http://fsdinfo.org/BMA%20Illustrated%20Medical%20Dictionary/308)；validation；完整来源行20359。当前片段` the`，文字片段编号279；成员7007，系数0。

完整可见前文：

```text
groin. It can be direct, in which there is
a localized weakness in the abdominal
wall, or, in men, indirect, in which the
intestine protrudes through the inguinal
canal, the passage through which the
testes descend into the scrotum.
The act of taking in breath
An inhalation is also a
substance, in the form of a gas, vapour,
powder, or aerosol, to be breathed in.
A device used for administering
a drug in powder or vapour form, used
mainly in the treatment of various res-
piratory disorders, including
Metered-dose inhalers
deliver a precise dose when the inhaler is
pressed. Drugs taken by inhalation in-
in h e r ita n c e
The transmission of char-
acteristics and disorders from parents to
their children through the influence of
Genes are the units of
oxyribonucleic acid) that are contained
in a person's cells; DNA controls all
growth and functioning of the body.
Half of a person's genes come from the
mother, half from the father.
Genes are organized into
in the cell nucleus. Genes controlling
most characteristics come in pairs, 1
the father, the other from the mother.
Everyone has 22 pairs of chromosomes
(called autosomes) bearing these paired
genes, in addition to 2 sex chromosomes.
Females have 2 X chromosomes; males
have an X and a Y chromosome.
Most physical characteristics, many
disorders, and some mental abilities
and aspects of personality are inherited.
The inheritance of normal traits and
disorders can be divided into those
controlled by a single pair of genes on
the autosomal chromosomes (unifactorial
inheritance, such as eye colour); those
controlled by genes on the sex chromo-
somes (sex-linked inheritance, such as
haemophilia); and those controlled by
the combination of many genes (multi-
factorial inheritance, such as height).
Either of the pair of genes controlling
a trait may take any of several forms,
known as
For example, the
```

同文档、相同当前文字片段的匹配参照（当前位置431；成员系数0.049873411655426025）：

```text
groin. It can be direct, in which there is
a localized weakness in the abdominal
wall, or, in men, indirect, in which the
intestine protrudes through the inguinal
canal, the passage through which the
testes descend into the scrotum.
The act of taking in breath
An inhalation is also a
substance, in the form of a gas, vapour,
powder, or aerosol, to be breathed in.
A device used for administering
a drug in powder or vapour form, used
mainly in the treatment of various res-
piratory disorders, including
Metered-dose inhalers
deliver a precise dose when the inhaler is
pressed. Drugs taken by inhalation in-
in h e r ita n c e
The transmission of char-
acteristics and disorders from parents to
their children through the influence of
Genes are the units of
oxyribonucleic acid) that are contained
in a person's cells; DNA controls all
growth and functioning of the body.
Half of a person's genes come from the
mother, half from the father.
Genes are organized into
in the cell nucleus. Genes controlling
most characteristics come in pairs, 1
the father, the other from the mother.
Everyone has 22 pairs of chromosomes
(called autosomes) bearing these paired
genes, in addition to 2 sex chromosomes.
Females have 2 X chromosomes; males
have an X and a Y chromosome.
Most physical characteristics, many
disorders, and some mental abilities
and aspects of personality are inherited.
The inheritance of normal traits and
disorders can be divided into those
controlled by a single pair of genes on
the autosomal chromosomes (unifactorial
inheritance, such as eye colour); those
controlled by genes on the sex chromo-
somes (sex-linked inheritance, such as
haemophilia); and those controlled by
the combination of many genes (multi-
factorial inheritance, such as height).
Either of the
```

这对真实上下文的变化：归一化前向量差长度279.981，归一化后长度55.458，去共同平移后的logit均方根变化1.67994；单位归一化后变化的输出增益0.0302921，相对各向同性方向参照1.054倍。它是两个实际上下文全部变化的读出，不能归因于单一文字线索或单个成员。

可复查属性：定义或命名短语。规则只查可见前文；它是词面／格式描述，不是纯语义金标。该例属性判定为True。高响应反例说明该成员并非该属性专有；低响应反例说明该属性也不保证该成员激活。竞争解释包括此前其他词、位置和句式；同token配对统计及其四分位敏感性见主报告。

## 3．定义或命名短语／counter_high_with_property

文档`R15_general_129`；位置192；来源[www.thenational.ae](https://www.thenational.ae/world/britain-suffers-massive-defeat-at-un-over-disputed-chagos-islands-1.865129)；validation；完整来源行47635。当前片段` of`，文字片段编号315；成员7007，系数0.23590857。

完整可见前文：

```text
Abu Dhabi, UAESaturday 21 September 2019

Britain suffers massive defeat at UN over disputed Chagos Islands

Vote in General Assembly urges Britain to cede authority to Mauritius

A demonstrator demands her return to the Chagos Islands outside the UK parliament. Reuters

Britain suffered an overwhelming defeat at the UN on Wednesday over its control of the Chagos Islands, home to the Diego Garcia military base that is leased to the US.

The vote among members of the UN General Assembly came in a non-binding resolution but called on Britain to withdraw its colonial administration and cede the territory to Mauritius within six months.

Only six countries including Britain and the US opposed the vote in the 193-member assembly, while 116 voted in favour and 56 abstained.

African countries proposed the resolution over the Chagos Islands, known as the British Indian Ocean Territory, which is considered to be one of
```

同文档、相同当前文字片段的匹配参照（当前位置236；成员系数0.0）：

```text
Abu Dhabi, UAESaturday 21 September 2019

Britain suffers massive defeat at UN over disputed Chagos Islands

Vote in General Assembly urges Britain to cede authority to Mauritius

A demonstrator demands her return to the Chagos Islands outside the UK parliament. Reuters

Britain suffered an overwhelming defeat at the UN on Wednesday over its control of the Chagos Islands, home to the Diego Garcia military base that is leased to the US.

The vote among members of the UN General Assembly came in a non-binding resolution but called on Britain to withdraw its colonial administration and cede the territory to Mauritius within six months.

Only six countries including Britain and the US opposed the vote in the 193-member assembly, while 116 voted in favour and 56 abstained.

African countries proposed the resolution over the Chagos Islands, known as the British Indian Ocean Territory, which is considered to be one of the last remaining vestiges of empire.

The Diego Garcia military base has been a departure point for long-distance bomber raids and rendition flights carrying terrorism suspects.

Mauritius claims sovereignty over the islands. An advisory opinion of
```

这对真实上下文的变化：归一化前向量差长度299.129，归一化后长度74.2177，去共同平移后的logit均方根变化2.11795；单位归一化后变化的输出增益0.028537，相对各向同性方向参照0.9925倍。它是两个实际上下文全部变化的读出，不能归因于单一文字线索或单个成员。

可复查属性：定义或命名短语。规则只查可见前文；它是词面／格式描述，不是纯语义金标。该例属性判定为True。高响应反例说明该成员并非该属性专有；低响应反例说明该属性也不保证该成员激活。竞争解释包括此前其他词、位置和句式；同token配对统计及其四分位敏感性见主报告。

## 4．定义或命名短语／counter_low_without_property

文档`R15_mathematics_112`；位置88；来源[dsp.stackexchange.com](https://dsp.stackexchange.com/questions/24780/power-spectral-density-vs-fft-bin-magnitude/24815)；validation；完整来源行52070。当前片段`m`，文字片段编号76；成员7007，系数0。

完整可见前文：

```text
What's the difference between these? Both are measurements of some form of signal power, but surely there's some difference between the power they are measuring?

  • $\begingroup$ Can you give more detail about what you don't understand? Please edit your question to add more details. $\endgroup$ – Peter K. Jul 22 '15 at 8:26

The fast Fourier transform ($\textrm
```

同文档、相同当前文字片段的匹配参照（当前位置483；成员系数0.0）：

```text
What's the difference between these? Both are measurements of some form of signal power, but surely there's some difference between the power they are measuring?

  • $\begingroup$ Can you give more detail about what you don't understand? Please edit your question to add more details. $\endgroup$ – Peter K. Jul 22 '15 at 8:26

The fast Fourier transform ($\textrm{FFT}$) algorithms are fast algorithms for computing the discrete Fourier transform ($\textrm{DFT}$). This is achieved by successive decomposition of the $N$-point $\textrm{DFT}$ into smaller-block $\textrm{DFT}$, and taking advantage of periodicity and symmetry.

Now, the $N$-point $\textrm{DFT}$ of a sequence $\{x[0], x[1],\cdots, x[N-1]\}$ is: \begin{equation} X(f_k) = \displaystyle \sum_{n = 0}^{N - 1} x[n]\exp\left(-j2\pi f_kn\right) \tag{1} \end{equation} For $f_k = k/N$ and $k = 0, 1, \cdots, N - 1$. And the $\textrm{FFT}$ magnitude at bin $k$ is the $\textrm{DFT}$magnitude at bin $k$. For a given $N$ that is:

\begin{equation} \left|X(f_k)\right| = \left|X\left(\frac{k}{N}\right)\right| = \left|X(k)\right| = \displaystyle \left|\sum_{n = 0}^{N - 1} x[n]\exp\left(-j2\pi nk/N\right)\right| \tag{2} \end{equation}

You talk about power spectral estimation when the signals being analyzed are characterized as random processes. With random fluctuations in such signals, statistical characteristics and average characteristics are normally adopted. For a wide sense stationary $(\textrm{WSS})$ discrete random process, the PSD is defined as:

\begin{equation} P(f) = \displaystyle \sum_{m
```

这对真实上下文的变化：归一化前向量差长度494.165，归一化后长度123.51，去共同平移后的logit均方根变化3.51005；单位归一化后变化的输出增益0.0284192，相对各向同性方向参照0.9884倍。它是两个实际上下文全部变化的读出，不能归因于单一文字线索或单个成员。

可复查属性：定义或命名短语。规则只查可见前文；它是词面／格式描述，不是纯语义金标。该例属性判定为False。高响应反例说明该成员并非该属性专有；低响应反例说明该属性也不保证该成员激活。竞争解释包括此前其他词、位置和句式；同token配对统计及其四分位敏感性见主报告。

## 5．近期数字表达／support_high_response

文档`R15_general_121`；位置15；来源[www.watertemperature.org](https://www.watertemperature.org/Prachuap-Khiri-Khan-Thailand-City.html)；validation；完整来源行7743。当前片段` near`，文字片段编号3143；成员10064，系数0.074153885。

完整可见前文：

```text
watertemperature.org logo2

Sea temperatures, water sports and vacation activities near
```

同文档、相同当前文字片段的匹配参照（当前位置187；成员系数0.03142927959561348）：

```text
watertemperature.org logo2

Sea temperatures, water sports and vacation activities near Prachuap Khiri Khan, Thailand

Water temperatures throughout the year and general information about Prachuap Khiri Khan...

Prachuap Khiri Khan is a coastal city in Thailand. It is a comparatively small coastal town in proximity to the ocean with a population of 33521 people. The water temperature around Prachuap Khiri Khan is close to steady during the year. The temperature ranges from 27.4°C (81.3°F) in February up to 30°C (86°F) in the month of May, as shown in the graph below. The average water temperature throughout the year is 28°C (83°F) and the best time for water activities is late spring, since Prachuap Khiri Khan is located in the northern hemisphere.


What is the current water temperature near
```

这对真实上下文的变化：归一化前向量差长度327.692，归一化后长度42.0632，去共同平移后的logit均方根变化1.24537；单位归一化后变化的输出增益0.0296072，相对各向同性方向参照1.03倍。它是两个实际上下文全部变化的读出，不能归因于单一文字线索或单个成员。

可复查属性：近期数字表达。规则只查可见前文；它是词面／格式描述，不是纯语义金标。该例属性判定为True。高响应反例说明该成员并非该属性专有；低响应反例说明该属性也不保证该成员激活。竞争解释包括此前其他词、位置和句式；同token配对统计及其四分位敏感性见主报告。

## 6．近期数字表达／counter_high_without_property

文档`R15_general_121`；位置63；来源[www.watertemperature.org](https://www.watertemperature.org/Prachuap-Khiri-Khan-Thailand-City.html)；validation；完整来源行7743。当前片段` to`，文字片段编号311；成员10064，系数0.069271073。

完整可见前文：

```text
watertemperature.org logo2

Sea temperatures, water sports and vacation activities near Prachuap Khiri Khan, Thailand

Water temperatures throughout the year and general information about Prachuap Khiri Khan...

Prachuap Khiri Khan is a coastal city in Thailand. It is a comparatively small coastal town in proximity to
```

同文档、相同当前文字片段的匹配参照（当前位置390；成员系数0.01726912334561348）：

```text
watertemperature.org logo2

Sea temperatures, water sports and vacation activities near Prachuap Khiri Khan, Thailand

Water temperatures throughout the year and general information about Prachuap Khiri Khan...

Prachuap Khiri Khan is a coastal city in Thailand. It is a comparatively small coastal town in proximity to the ocean with a population of 33521 people. The water temperature around Prachuap Khiri Khan is close to steady during the year. The temperature ranges from 27.4°C (81.3°F) in February up to 30°C (86°F) in the month of May, as shown in the graph below. The average water temperature throughout the year is 28°C (83°F) and the best time for water activities is late spring, since Prachuap Khiri Khan is located in the northern hemisphere.


What is the current water temperature near Prachuap Khiri Khan?

The current water temperature in the month of August in the waters close to Prachuap Khiri Khan is approximately:
29°C (84°F)

Are there surf spots near by?

Not too many surf spots are in close proximity to Prachuap Khiri Khan. The closest decent spot is Asu, which is 775.6km (481.7miles) away from Prachuap Khiri Khan. Click here for more information on Asu and its current water temperature. If you don't mind the drive, you can also try Bawa, which is roughly 779.1km (483.9miles) away from Prachuap Khiri Khan. Another fun surfspot is Bawa, located 779.1km (483.9miles) from Prachuap Khiri Khan.

Are there nice beaches near by?

No, not many beaches are in proximity to
```

这对真实上下文的变化：归一化前向量差长度354.499，归一化后长度78.0941，去共同平移后的logit均方根变化2.23941；单位归一化后变化的输出增益0.0286758，相对各向同性方向参照0.9973倍。它是两个实际上下文全部变化的读出，不能归因于单一文字线索或单个成员。

可复查属性：近期数字表达。规则只查可见前文；它是词面／格式描述，不是纯语义金标。该例属性判定为False。高响应反例说明该成员并非该属性专有；低响应反例说明该属性也不保证该成员激活。竞争解释包括此前其他词、位置和句式；同token配对统计及其四分位敏感性见主报告。

## 7．近期数字表达／counter_low_with_property

文档`R15_mathematics_112`；位置88；来源[dsp.stackexchange.com](https://dsp.stackexchange.com/questions/24780/power-spectral-density-vs-fft-bin-magnitude/24815)；validation；完整来源行52070。当前片段`m`，文字片段编号76；成员10064，系数0。

完整可见前文：

```text
What's the difference between these? Both are measurements of some form of signal power, but surely there's some difference between the power they are measuring?

  • $\begingroup$ Can you give more detail about what you don't understand? Please edit your question to add more details. $\endgroup$ – Peter K. Jul 22 '15 at 8:26

The fast Fourier transform ($\textrm
```

同文档、相同当前文字片段的匹配参照（当前位置483；成员系数0.0）：

```text
What's the difference between these? Both are measurements of some form of signal power, but surely there's some difference between the power they are measuring?

  • $\begingroup$ Can you give more detail about what you don't understand? Please edit your question to add more details. $\endgroup$ – Peter K. Jul 22 '15 at 8:26

The fast Fourier transform ($\textrm{FFT}$) algorithms are fast algorithms for computing the discrete Fourier transform ($\textrm{DFT}$). This is achieved by successive decomposition of the $N$-point $\textrm{DFT}$ into smaller-block $\textrm{DFT}$, and taking advantage of periodicity and symmetry.

Now, the $N$-point $\textrm{DFT}$ of a sequence $\{x[0], x[1],\cdots, x[N-1]\}$ is: \begin{equation} X(f_k) = \displaystyle \sum_{n = 0}^{N - 1} x[n]\exp\left(-j2\pi f_kn\right) \tag{1} \end{equation} For $f_k = k/N$ and $k = 0, 1, \cdots, N - 1$. And the $\textrm{FFT}$ magnitude at bin $k$ is the $\textrm{DFT}$magnitude at bin $k$. For a given $N$ that is:

\begin{equation} \left|X(f_k)\right| = \left|X\left(\frac{k}{N}\right)\right| = \left|X(k)\right| = \displaystyle \left|\sum_{n = 0}^{N - 1} x[n]\exp\left(-j2\pi nk/N\right)\right| \tag{2} \end{equation}

You talk about power spectral estimation when the signals being analyzed are characterized as random processes. With random fluctuations in such signals, statistical characteristics and average characteristics are normally adopted. For a wide sense stationary $(\textrm{WSS})$ discrete random process, the PSD is defined as:

\begin{equation} P(f) = \displaystyle \sum_{m
```

这对真实上下文的变化：归一化前向量差长度494.165，归一化后长度123.51，去共同平移后的logit均方根变化3.51005；单位归一化后变化的输出增益0.0284192，相对各向同性方向参照0.9884倍。它是两个实际上下文全部变化的读出，不能归因于单一文字线索或单个成员。

可复查属性：近期数字表达。规则只查可见前文；它是词面／格式描述，不是纯语义金标。该例属性判定为True。高响应反例说明该成员并非该属性专有；低响应反例说明该属性也不保证该成员激活。竞争解释包括此前其他词、位置和句式；同token配对统计及其四分位敏感性见主报告。

## 8．公式符号或排版／support_high_response

文档`R15_mathematics_142`；位置419；来源[au.mathworks.com](https://au.mathworks.com/help/deeplearning/ug/radial-basis-neural-networks.html)；validation；完整来源行87682。当前片段` of`，文字片段编号315；成员6723，系数0.10076614。

完整可见前文：

```text
Radial Basis Neural Networks

Neuron Model

Here is a radial basis network with R inputs.

Notice that the expression for the net input of a radbas neuron is different from that of other neurons. Here the net input to the radbas transfer function is the vector distance between its weight vector w and the input vector p, multiplied by the bias b. (The || dist || box in this figure accepts the input vector p and the single row input weight matrix, and produces the dot product of the two.)

The transfer function for a radial basis neuron is


Here is a plot of the radbas transfer function.

The radial basis function has a maximum of 1 when its input is 0. As the distance between w and p decreases, the output increases. Thus, a radial basis neuron acts as a detector that produces 1 whenever the input p is identical to its weight vector w.

The bias b allows the sensitivity of the radbas neuron to be adjusted. For example, if a neuron had a bias of 0.1 it would output 0.5 for any input vector p at vector distance of 8.326 (0.8326/b) from its weight vector w.

Network Architecture

Radial basis networks consist of two layers: a hidden radial basis layer of S1 neurons, and an output linear layer of S2 neurons.

The || dist || box in this figure accepts the input vector p and the input weight matrix IW1,1, and produces a vector having S1 elements. The elements are the distances between the input vector and vectors iIW1,1 formed from the rows of the input weight matrix.

The bias vector b1 and the output of || dist || are combined with the MATLAB® operation .* , which does element-by-element multiplication.

The output of the first layer for a feedforward network net can be obtained with the following code:

a{1} = radbas(netprod(dist(net.IW{1,1},p),net.b{1}))

Fortunately, you won't have to write such lines of
```

同文档、相同当前文字片段的匹配参照（当前位置366；成员系数0.0455903597176075）：

```text
Radial Basis Neural Networks

Neuron Model

Here is a radial basis network with R inputs.

Notice that the expression for the net input of a radbas neuron is different from that of other neurons. Here the net input to the radbas transfer function is the vector distance between its weight vector w and the input vector p, multiplied by the bias b. (The || dist || box in this figure accepts the input vector p and the single row input weight matrix, and produces the dot product of the two.)

The transfer function for a radial basis neuron is


Here is a plot of the radbas transfer function.

The radial basis function has a maximum of 1 when its input is 0. As the distance between w and p decreases, the output increases. Thus, a radial basis neuron acts as a detector that produces 1 whenever the input p is identical to its weight vector w.

The bias b allows the sensitivity of the radbas neuron to be adjusted. For example, if a neuron had a bias of 0.1 it would output 0.5 for any input vector p at vector distance of 8.326 (0.8326/b) from its weight vector w.

Network Architecture

Radial basis networks consist of two layers: a hidden radial basis layer of S1 neurons, and an output linear layer of S2 neurons.

The || dist || box in this figure accepts the input vector p and the input weight matrix IW1,1, and produces a vector having S1 elements. The elements are the distances between the input vector and vectors iIW1,1 formed from the rows of the input weight matrix.

The bias vector b1 and the output of || dist || are combined with the MATLAB® operation .* , which does element-by-element multiplication.

The output of
```

这对真实上下文的变化：归一化前向量差长度453.595，归一化后长度87.7714，去共同平移后的logit均方根变化2.65587；单位归一化后变化的输出增益0.0302589，相对各向同性方向参照1.052倍。它是两个实际上下文全部变化的读出，不能归因于单一文字线索或单个成员。

可复查属性：公式符号或排版。规则只查可见前文；它是词面／格式描述，不是纯语义金标。该例属性判定为True。高响应反例说明该成员并非该属性专有；低响应反例说明该属性也不保证该成员激活。竞争解释包括此前其他词、位置和句式；同token配对统计及其四分位敏感性见主报告。

## 9．公式符号或排版／counter_high_without_property

文档`R15_mathematics_142`；位置366；来源[au.mathworks.com](https://au.mathworks.com/help/deeplearning/ug/radial-basis-neural-networks.html)；validation；完整来源行87682。当前片段` of`，文字片段编号315；成员6723，系数0.04559036。

完整可见前文：

```text
Radial Basis Neural Networks

Neuron Model

Here is a radial basis network with R inputs.

Notice that the expression for the net input of a radbas neuron is different from that of other neurons. Here the net input to the radbas transfer function is the vector distance between its weight vector w and the input vector p, multiplied by the bias b. (The || dist || box in this figure accepts the input vector p and the single row input weight matrix, and produces the dot product of the two.)

The transfer function for a radial basis neuron is


Here is a plot of the radbas transfer function.

The radial basis function has a maximum of 1 when its input is 0. As the distance between w and p decreases, the output increases. Thus, a radial basis neuron acts as a detector that produces 1 whenever the input p is identical to its weight vector w.

The bias b allows the sensitivity of the radbas neuron to be adjusted. For example, if a neuron had a bias of 0.1 it would output 0.5 for any input vector p at vector distance of 8.326 (0.8326/b) from its weight vector w.

Network Architecture

Radial basis networks consist of two layers: a hidden radial basis layer of S1 neurons, and an output linear layer of S2 neurons.

The || dist || box in this figure accepts the input vector p and the input weight matrix IW1,1, and produces a vector having S1 elements. The elements are the distances between the input vector and vectors iIW1,1 formed from the rows of the input weight matrix.

The bias vector b1 and the output of || dist || are combined with the MATLAB® operation .* , which does element-by-element multiplication.

The output of
```

同文档、相同当前文字片段的匹配参照（当前位置419；成员系数0.1007661372423172）：

```text
Radial Basis Neural Networks

Neuron Model

Here is a radial basis network with R inputs.

Notice that the expression for the net input of a radbas neuron is different from that of other neurons. Here the net input to the radbas transfer function is the vector distance between its weight vector w and the input vector p, multiplied by the bias b. (The || dist || box in this figure accepts the input vector p and the single row input weight matrix, and produces the dot product of the two.)

The transfer function for a radial basis neuron is


Here is a plot of the radbas transfer function.

The radial basis function has a maximum of 1 when its input is 0. As the distance between w and p decreases, the output increases. Thus, a radial basis neuron acts as a detector that produces 1 whenever the input p is identical to its weight vector w.

The bias b allows the sensitivity of the radbas neuron to be adjusted. For example, if a neuron had a bias of 0.1 it would output 0.5 for any input vector p at vector distance of 8.326 (0.8326/b) from its weight vector w.

Network Architecture

Radial basis networks consist of two layers: a hidden radial basis layer of S1 neurons, and an output linear layer of S2 neurons.

The || dist || box in this figure accepts the input vector p and the input weight matrix IW1,1, and produces a vector having S1 elements. The elements are the distances between the input vector and vectors iIW1,1 formed from the rows of the input weight matrix.

The bias vector b1 and the output of || dist || are combined with the MATLAB® operation .* , which does element-by-element multiplication.

The output of the first layer for a feedforward network net can be obtained with the following code:

a{1} = radbas(netprod(dist(net.IW{1,1},p),net.b{1}))

Fortunately, you won't have to write such lines of
```

这对真实上下文的变化：归一化前向量差长度453.595，归一化后长度87.7714，去共同平移后的logit均方根变化2.65587；单位归一化后变化的输出增益0.0302589，相对各向同性方向参照1.052倍。它是两个实际上下文全部变化的读出，不能归因于单一文字线索或单个成员。

可复查属性：公式符号或排版。规则只查可见前文；它是词面／格式描述，不是纯语义金标。该例属性判定为False。高响应反例说明该成员并非该属性专有；低响应反例说明该属性也不保证该成员激活。竞争解释包括此前其他词、位置和句式；同token配对统计及其四分位敏感性见主报告。

## 10．公式符号或排版／counter_low_with_property

文档`R15_mathematics_112`；位置120；来源[dsp.stackexchange.com](https://dsp.stackexchange.com/questions/24780/power-spectral-density-vs-fft-bin-magnitude/24815)；validation；完整来源行52070。当前片段` the`，文字片段编号279；成员6723，系数0。

完整可见前文：

```text
What's the difference between these? Both are measurements of some form of signal power, but surely there's some difference between the power they are measuring?

  • $\begingroup$ Can you give more detail about what you don't understand? Please edit your question to add more details. $\endgroup$ – Peter K. Jul 22 '15 at 8:26

The fast Fourier transform ($\textrm{FFT}$) algorithms are fast algorithms for computing the discrete Fourier transform ($\textrm{DFT}$). This is achieved by successive decomposition of the
```

同文档、相同当前文字片段的匹配参照（当前位置2；成员系数0.0）：

```text
What's the
```

这对真实上下文的变化：归一化前向量差长度421.132，归一化后长度118.815，去共同平移后的logit均方根变化3.51726；单位归一化后变化的输出增益0.0296029，相对各向同性方向参照1.03倍。它是两个实际上下文全部变化的读出，不能归因于单一文字线索或单个成员。

可复查属性：公式符号或排版。规则只查可见前文；它是词面／格式描述，不是纯语义金标。该例属性判定为True。高响应反例说明该成员并非该属性专有；低响应反例说明该属性也不保证该成员激活。竞争解释包括此前其他词、位置和句式；同token配对统计及其四分位敏感性见主报告。

## 11．未获解释的固定成员／discovery_unexplained_fixed_member

文档`R15_mathematics_045`；位置296；来源[en.wikipedia.org](https://en.wikipedia.org/wiki/Screw_(motion))；discovery；完整来源行78089。当前片段` screw`，文字片段编号21966；成员6743，系数0.050564058。

完整可见前文：

```text
Screw theory

From Wikipedia, the free encyclopedia
  (Redirected from Screw (motion))
Jump to navigation Jump to search
Sir Robert Ball, author of treatises on screw theory in 1876 and 1900

Screw theory is the algebraic calculation of pairs of vectors, such as forces and moments or angular and linear velocity, that arise in the kinematics and dynamics of rigid bodies.[1][2] The mathematical framework was developed by Sir Robert Stawell Ball in 1876 for application in kinematics and statics of mechanisms (rigid body mechanics).[3]

Screw theory provides a mathematical formulation for the geometry of lines which is central to rigid body dynamics, where lines form the screw axes of spatial movement and the lines of action of forces. The pair of vectors that form the Plücker coordinates of a line define a unit screw, and general screws are obtained by multiplication by a pair of real numbers and addition of vectors.[3]

An important result of screw theory is that geometric calculations for points using vectors have parallel geometric calculations for lines obtained by replacing vectors with screws. This is termed the transfer principle.[4]

Screw theory has become an important tool in robot mechanics,[5][6] mechanical design, computational geometry and multibody dynamics. This is in part because of the relationship between screws and dual quaternions which have been used to interpolate rigid-body motions.[7] Based on screw
```

本例没有满足冻结解释选择的名称。保留原始响应及上下文，不从一个片段猜测该成员的功能。

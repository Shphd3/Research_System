# 固定前文与原始输出

原生 block27 residual-post → 最终 RMSNorm → 冻结输出头。原始 ID／片段／概率不是完整词的语义标签。排名以严格更高 logit 的 ID 数加1计算；并列同分使用最小排名。前文之后的文字只用于语料描述，不进入本位置计算。


## 预先固定展示


### the:R11_A02_090:191 · analysis

真实后继：ID **34259**，片段 **' summ'**。原文：[来源](https://byjus.com/maths/integration/)。

完整可见前文：

```text
Integration
is the calculation of an integral. Integrals in maths are used to find many useful quantities such as areas, volumes, displacement, etc. When we speak about integrals, it is related to usually definite integrals. The indefinite integrals are used for antiderivatives. Integration is one of the two major calculus topics in Mathematics, apart from differentiation(which measure the rate of change of any function with respect to its variables). It’s a vast topic which is discussed at higher level classes like in Class 11 and 12.
Integration by parts
and by the substitution is explained broadly.
Here, you will learn the definition of integrals in Maths, formulas of integration along with examples.
Table of Contents:
Integration Definition
Integral Calculus
Integration – Inverse Process of Differentiation
Integrals
Definite Integral
Indefinite Integral
Integration Formulas
Examples
FAQs
Integration Definition
The integration denotes the
```


原文后续（仅用于辨认完整拼写；未进入本位置输入）：` summation of discrete data. The integral is calculated to find the functions which will describe th`


|条件|前三候选（ID、片段、概率）|真实后继概率|真实后继排名|NLL|相对原模型KL|
|---|---|---:|---:|---:|---:|
|mean_only|320 ' (' 0.2145；11 ',' 0.1893；220 ' ' 0.0894|0.00000|3218|13.7894|8.8684|
|k1|279 ' the' 0.1009；320 ' (' 0.1009；304 ' in' 0.0891|0.00001|3267|12.1058|7.3437|
|k4|220 ' ' 0.1662；320 ' (' 0.1142；279 ' the' 0.1008|0.00001|2652|11.6698|7.3901|
|k16|330 ' "' 0.0716；279 ' the' 0.0434；220 ' ' 0.0338|0.00013|904|8.9488|4.5720|
|k64|330 ' "' 0.0533；1372 ' number' 0.0173；1036 ' “' 0.0135|0.00025|670|8.3070|3.3361|
|middle|11 ',' 0.2128；304 ' in' 0.1139；320 ' (' 0.1139|0.00000|2142|12.9226|8.2867|
|tail|320 ' (' 0.1909；11 ',' 0.1684；220 ' ' 0.1022|0.00000|2369|12.7812|7.9820|
|head_middle|330 ' "' 0.0414；1036 ' “' 0.0251；1372 ' number' 0.0251|0.00038|451|7.8730|3.0982|
|head_tail|330 ' "' 0.0311；1372 ' number' 0.0189；1036 ' “' 0.0101|0.00037|470|7.9082|3.0021|
|k128|330 ' "' 0.0519；35972 ' mathematical' 0.0278；1156 ' first' 0.0245|0.00051|313|7.5841|2.7037|
|head_random1034|330 ' "' 0.0432；1372 ' number' 0.0297；279 ' the' 0.0180|0.00037|462|7.8922|2.9632|
|head_random1035|330 ' "' 0.0374；1372 ' number' 0.0177；1036 ' “' 0.0156|0.00044|394|7.7235|2.9539|
|head_random1036|330 ' "' 0.0641；1036 ' “' 0.0303；3766 ' application' 0.0208|0.00032|474|8.0603|2.9953|
|k256|35972 ' mathematical' 0.0286；2155 ' different' 0.0252；1852 ' same' 0.0223|0.00086|182|7.0540|1.7259|
|k512|35972 ' mathematical' 0.1055；9931 ' reverse' 0.0498；27949 ' inverse' 0.0498|0.00409|32|5.4994|0.8150|
|k768|9931 ' reverse' 0.1071；1882 ' process' 0.0946；27949 ' inverse' 0.0736|0.00776|18|4.8586|0.3075|
|k1024|1882 ' process' 0.2487；9931 ' reverse' 0.2195；27949 ' inverse' 0.1037|0.00851|14|4.7666|0.0000|
|identity|1882 ' process' 0.2487；9931 ' reverse' 0.2195；27949 ' inverse' 0.1037|0.00851|14|4.7666|0.0000|

### the:R11_A02_123:184 · analysis

真实后继：ID **12557**，片段 **' multip'**。原文：[来源](https://terrytao.wordpress.com/2021/12/28/the-inverse-theorem-for-the-u3-gowers-uniformity-norm-on-arbitrary-finite-abelian-groups-fourier-analytic-and-ergodic-approaches/)。

完整可见前文：

```text
Asgar Jamneshan
and myself have just uploaded to the arXiv our preprint “
The inverse theorem for the
{U^3}
Gowers uniformity norm on arbitrary finite abelian groups: Fourier-analytic and ergodic approaches
“. This paper, which is a companion to
another recent paper
of ourselves and
Or Shalom
, studies the inverse theory for the third
Gowers uniformity norm
\displaystyle  \| f \|_{U^3(G)}^8 = {\bf E}_{h_1,h_2,h_3,x \in G} \Delta_{h_1} \Delta_{h_2} \Delta_{h_3} f(x)
on an arbitrary finite abelian group
{G}
, where
{\Delta_h f(x) := f(x+h) \overline{f(x)}}
is the
```


原文后续（仅用于辨认完整拼写；未进入本位置输入）：` multiplicative derivative. Our main result`


|条件|前三候选（ID、片段、概率）|真实后继概率|真实后继排名|NLL|相对原模型KL|
|---|---|---:|---:|---:|---:|
|mean_only|320 ' (' 0.2145；11 ',' 0.1893；220 ' ' 0.0894|0.00001|1216|12.1644|6.0908|
|k1|11 ',' 0.4851；320 ' (' 0.2597；323 ' and' 0.0657|0.00000|1282|16.4733|9.9650|
|k4|220 ' ' 0.6118；279 ' the' 0.1205；320 ' (' 0.0828|0.00000|940|13.6164|6.6901|
|k16|220 ' ' 0.2099；2477 ' non' 0.1273；320 ' (' 0.0681|0.00017|204|8.6863|3.8872|
|k64|320 ' (' 0.0454；400 ' $' 0.0401；479 ' G' 0.0401|0.00107|133|6.8417|2.0719|
|middle|320 ' (' 0.2135；11 ',' 0.1884；323 ' and' 0.0786|0.00002|775|11.1065|5.4563|
|tail|320 ' (' 0.2515；11 ',' 0.1729；220 ' ' 0.1346|0.00001|922|12.0678|6.3646|
|head_middle|479 ' G' 0.0762；444 ' L' 0.0360；730 ' K' 0.0360|0.00230|81|6.0740|1.7595|
|head_tail|320 ' (' 0.0730；400 ' $' 0.0501；220 ' ' 0.0391|0.00151|87|6.4928|2.1582|
|k128|320 ' (' 0.0527；2477 ' non' 0.0410；220 ' ' 0.0319|0.00180|100|6.3186|1.7968|
|head_random1034|47311 ' polynomial' 0.0433；479 ' G' 0.0298；8381 ' degree' 0.0298|0.00244|83|6.0144|1.7719|
|head_random1035|74762 ' quotient' 0.0503；479 ' G' 0.0444；47311 ' polynomial' 0.0392|0.00250|79|5.9896|1.9226|
|head_random1036|198 '\n' 0.0869；320 ' (' 0.0869；220 ' ' 0.0362|0.00017|403|8.6928|1.9883|
|k256|320 ' (' 0.0447；400 ' $' 0.0447；36824 ' weighted' 0.0307|0.00196|98|6.2333|1.4402|
|k512|54343 ' symmetric' 0.0736；88954 ' Fourier' 0.0394；86960 ' determinant' 0.0271|0.00173|112|6.3587|1.0142|
|k768|55712 ' convolution' 0.1172；76002 ' cyclic' 0.0627；88954 ' Fourier' 0.0431|0.00354|46|5.6440|0.4282|
|k1024|198 '\n' 0.1084；5297 ' standard' 0.0512；479 ' G' 0.0352|0.01143|15|4.4716|0.0000|
|identity|198 '\n' 0.1084；5297 ' standard' 0.0512；479 ' G' 0.0352|0.01143|15|4.4716|0.0000|

### the:R11_A02_262:177 · cell

真实后继：ID **53942**，片段 **' mitochond'**。原文：[来源](https://byjus.com/biology/mitochondria/)。

完整可见前文：

```text
Mitochondria Definition
“Mitochondria are membrane-bound organelles present in the cytoplasm of all eukaryotic cells, that produce adenosine triphosphate (ATP), the main energy molecule used by the cell.”
Table of Contents
Explanation
Diagram
Structure
Function
Disorders
Read on to explore what is mitochondria, its structure, and functions.
What are Mitochondria?
Popularly known as the “
Powerhouse of the cell
,” mitochondria (singular: mitochondrion) are a double membrane-bound organelle found in most eukaryotic organisms. They are found inside the cytoplasm and essentially function as the cell’s “digestive system.”
They play a major role in breaking down nutrients and generating energy-rich molecules for the cell. Many of the biochemical reactions involved in cellular respiration take place within the
```


原文后续（仅用于辨认完整拼写；未进入本位置输入）：` mitochondria. The term ‘mitochondrion’ is derived from`


|条件|前三候选（ID、片段、概率）|真实后继概率|真实后继排名|NLL|相对原模型KL|
|---|---|---:|---:|---:|---:|
|mean_only|320 ' (' 0.2145；11 ',' 0.1893；220 ' ' 0.0894|0.00000|10820|16.1956|15.2963|
|k1|320 ' (' 0.1688；11 ',' 0.1314；304 ' in' 0.1024|0.00000|9279|14.9666|14.1058|
|k4|279 ' the' 0.1461；264 ' a' 0.0886；220 ' ' 0.0782|0.00005|977|9.8612|9.1711|
|k16|2779 ' cell' 0.1109；220 ' ' 0.0762；279 ' the' 0.0462|0.00031|374|8.0739|7.3976|
|k64|2779 ' cell' 0.2441；7761 ' cells' 0.1481；38554 ' membrane' 0.0330|0.00271|30|5.9100|5.3472|
|middle|320 ' (' 0.1995；11 ',' 0.1761；323 ' and' 0.1210|0.00000|6327|14.8618|14.0192|
|tail|320 ' (' 0.2060；11 ',' 0.1818；220 ' ' 0.1250|0.00000|11575|17.1110|16.1854|
|head_middle|2779 ' cell' 0.2088；7761 ' cells' 0.0986；34593 ' cellular' 0.0363|0.00810|9|4.8162|4.3062|
|head_tail|2779 ' cell' 0.1894；7761 ' cells' 0.1302；220 ' ' 0.0543|0.00210|47|6.1640|5.5873|
|k128|2779 ' cell' 0.2781；7761 ' cells' 0.2166；34593 ' cellular' 0.0621|0.01385|7|4.2797|3.7873|
|head_random1034|2779 ' cell' 0.2682；7761 ' cells' 0.1267；330 ' "' 0.0194|0.00810|13|4.8160|4.3395|
|head_random1035|2779 ' cell' 0.1773；7761 ' cells' 0.1075；330 ' "' 0.0308|0.01133|10|4.4801|4.0099|
|head_random1036|2779 ' cell' 0.2393；7761 ' cells' 0.0998；220 ' ' 0.0324|0.00341|28|5.6800|5.1132|
|k256|2779 ' cell' 0.3361；7761 ' cells' 0.1236；53942 ' mitochond' 0.0750|0.07499|3|2.5903|2.2326|
|k512|53942 ' mitochond' 0.6781；2779 ' cell' 0.0631；70961 ' mitochondrial' 0.0338|0.67811|1|0.3884|0.2115|
|k768|53942 ' mitochond' 0.8683；70961 ' mitochondrial' 0.0629；2779 ' cell' 0.0180|0.86831|1|0.1412|0.0318|
|k1024|53942 ' mitochond' 0.8964；70961 ' mitochondrial' 0.0394；9179 ' inner' 0.0145|0.89645|1|0.1093|0.0000|
|identity|53942 ' mitochond' 0.8964；70961 ' mitochondrial' 0.0394；9179 ' inner' 0.0145|0.89645|1|0.1093|0.0000|

### the:R11_A02_282:164 · cell

真实后继：ID **5702**，片段 **' activity'**。原文：[来源](https://medicalxpress.com/news/2013-11-tumor-cells-dangerous.html)。

完整可见前文：

```text
Why tumor cells go on dangerous tours

Why tumor cells go on dangerous tours
Metastasis of a colon carcinoma to the lung: ZNF281 induces the expression of Vimentin (red), a typical marker for mesenchymal cells, in epithelial carcinoma cells. Detection of Vimentin thus indicates that an epithelial-mesenchymal transition (EMT) occurred in these cells which endowed them with metastatic potential.

Tumors become highly malignant when they acquire the ability to colonize other tissues and form metastases. Researchers at Ludwig-Maximilians-Universitaet (LMU) in Munich have identified a factor that promotes metastasis of colon tumors – and presents a possible target for therapy.

The protein c-MYC is referred to as a master regulator because it controls the
```


原文后续（仅用于辨认完整拼写；未进入本位置输入）：` activity of hundreds of genes, including many that drive cell growth and cell proliferation. Geneti`


|条件|前三候选（ID、片段、概率）|真实后继概率|真实后继排名|NLL|相对原模型KL|
|---|---|---:|---:|---:|---:|
|mean_only|320 ' (' 0.2145；11 ',' 0.1893；220 ' ' 0.0894|0.00000|2140|13.1019|8.8977|
|k1|320 ' (' 0.1621；11 ',' 0.1114；304 ' in' 0.0983|0.00001|2101|12.1319|7.9884|
|k4|279 ' the' 0.1804；304 ' in' 0.0965；264 ' a' 0.0852|0.00002|1322|10.6503|6.6543|
|k16|2779 ' cell' 0.0416；3151 ' specific' 0.0253；23275 ' biological' 0.0197|0.00302|56|5.8035|2.7810|
|k64|4401 ' development' 0.1887；2779 ' cell' 0.0694；14862 ' gene' 0.0541|0.00444|30|5.4178|1.0576|
|middle|11 ',' 0.2012；320 ' (' 0.1567；220 ' ' 0.0951|0.00000|2252|12.9157|8.5064|
|tail|320 ' (' 0.2510；11 ',' 0.2215；220 ' ' 0.1046|0.00000|2347|13.8824|9.7244|
|head_middle|4401 ' development' 0.1756；2779 ' cell' 0.1207；1882 ' process' 0.0570|0.00413|27|5.4894|1.0372|
|head_tail|4401 ' development' 0.1583；14862 ' gene' 0.0748；2779 ' cell' 0.0514|0.00422|31|5.4686|1.1267|
|k128|4401 ' development' 0.2194；2779 ' cell' 0.0555；6513 ' growth' 0.0489|0.01402|9|4.2670|0.6978|
|head_random1034|4401 ' development' 0.2486；2779 ' cell' 0.0712；6513 ' growth' 0.0555|0.00276|44|5.8920|1.0057|
|head_random1035|4401 ' development' 0.1902；2779 ' cell' 0.0545；7493 ' expression' 0.0481|0.00574|24|5.1599|0.8265|
|head_random1036|4401 ' development' 0.1067；2779 ' cell' 0.0831；14862 ' gene' 0.0571|0.00682|22|4.9879|1.1229|
|k256|4401 ' development' 0.4685；6513 ' growth' 0.0560；5670 ' production' 0.0494|0.01603|7|4.1332|0.6043|
|k512|4401 ' development' 0.5177；7493 ' expression' 0.0546；5670 ' production' 0.0482|0.01772|7|4.0333|0.4387|
|k768|4401 ' development' 0.1985；7493 ' expression' 0.1751；2779 ' cell' 0.0730|0.03449|5|3.3672|0.1160|
|k1024|4401 ' development' 0.2170；7493 ' expression' 0.1915；6513 ' growth' 0.0622|0.03327|5|3.4031|0.0000|
|identity|4401 ' development' 0.2170；7493 ' expression' 0.1915；6513 ' growth' 0.0622|0.03327|5|3.4031|0.0000|

### the:R11_A02_283:154 · cell

真实后继：ID **2779**，片段 **' cell'**。原文：[来源](https://www.wyzant.com/resources/answers/947850/if-membrane-potential-is-clamped-to-100-mv-for-example-by-patch-clamp-with-)。

完整可见前文：

```text
To understand what happens in this scenario, we can analyze the driving forces on potassium (K⁺) and sodium (Na⁺) ions based on the membrane potential and their respective Nernst (equilibrium) potentials.
Given Data:
Membrane potential (Vm): -100 mV
Nernst potential for Na⁺ (ENa): +60 mV
Nernst potential for K⁺ (EK): -90 mV
Interpretation of Ion Movement:
For K⁺:
The membrane potential (-100 mV) is slightly more negative than EK (-90 mV).
Since Vm is more negative than EK, potassium ions (K⁺) will experience a small driving force to move
out of the
```


原文后续（仅用于辨认完整拼写；未进入本位置输入）：` cell↵(efflux).↵For Na⁺:↵The membrane potential (-100 mV) is much more negative than ENa (+60 mV).↵T`


|条件|前三候选（ID、片段、概率）|真实后继概率|真实后继排名|NLL|相对原模型KL|
|---|---|---:|---:|---:|---:|
|mean_only|320 ' (' 0.2145；11 ',' 0.1893；220 ' ' 0.0894|0.00002|565|11.0394|10.4733|
|k1|11 ',' 0.5199；320 ' (' 0.2456；323 ' and' 0.0621|0.00000|803|16.1542|15.6715|
|k4|11 ',' 0.2435；220 ' ' 0.2149；320 ' (' 0.2149|0.00001|215|11.8501|11.5181|
|k16|220 ' ' 0.6890；320 ' (' 0.1197；198 '\n' 0.0343|0.02081|5|3.8725|3.8476|
|k64|2779 ' cell' 0.2411；220 ' ' 0.1878；38554 ' membrane' 0.1139|0.24112|1|1.4225|1.0944|
|middle|11 ',' 0.2323；320 ' (' 0.1596；220 ' ' 0.0854|0.00008|248|9.4599|9.2107|
|tail|320 ' (' 0.3103；11 ',' 0.1882；220 ' ' 0.0785|0.00001|562|11.5452|10.9662|
|head_middle|2779 ' cell' 0.5550；198 '\n' 0.0964；220 ' ' 0.0751|0.55497|1|0.5888|0.6345|
|head_tail|220 ' ' 0.2510；320 ' (' 0.2215；2779 ' cell' 0.1523|0.15226|3|1.8822|1.5206|
|k128|2779 ' cell' 0.3211；5537 ' region' 0.1042；198 '\n' 0.0812|0.32109|1|1.1360|0.8194|
|head_random1034|2779 ' cell' 0.5592；220 ' ' 0.0668；198 '\n' 0.0459|0.55918|1|0.5813|0.5928|
|head_random1035|2779 ' cell' 0.5347；220 ' ' 0.1053；38554 ' membrane' 0.0724|0.53467|1|0.6261|0.5182|
|head_random1036|38554 ' membrane' 0.2628；2779 ' cell' 0.1806；320 ' (' 0.0967|0.18060|2|1.7115|1.1792|
|k256|2779 ' cell' 0.5816；198 '\n' 0.1298；38554 ' membrane' 0.1011|0.58164|1|0.5419|0.3498|
|k512|2779 ' cell' 0.6243；38554 ' membrane' 0.1789；198 '\n' 0.1085|0.62435|1|0.4710|0.2081|
|k768|2779 ' cell' 0.8786；38554 ' membrane' 0.0721；198 '\n' 0.0046|0.87864|1|0.1294|0.0624|
|k1024|2779 ' cell' 0.7859；38554 ' membrane' 0.1205；6291 ' solution' 0.0087|0.78594|1|0.2409|0.0000|
|identity|2779 ' cell' 0.7859；38554 ' membrane' 0.1205；6291 ' solution' 0.0087|0.78594|1|0.2409|0.0000|

### the:R11_A02_292:140 · ecology_evolution

真实后继：ID **8654**，片段 **' capacity'**。原文：[来源](https://www.wyzant.com/resources/answers/935535/with-evolution-how-did-ectotherms-evolve-into-endotherms)。

完整可见前文：

```text
The evolution from ectothermy to endothermy is not a simple linear process but involves a multitude of changes in behavior, physiology, and anatomy. It is a prime example of convergent evolution, where similar traits evolve independently in different lineages due to similar selective pressures. The evolutionary transition from ectothermy (relying on external sources of temperature to regulate body heat) to endothermy (relying on internal processes to regulate body heat) is a complex process that has occurred independently in several lineages throughout the history of life on Earth. Endothermy is a derived trait that provides several advantages, such as the ability to remain active in a wide range of temperatures, increased stamina, and the
```


原文后续（仅用于辨认完整拼写；未进入本位置输入）：` capacity for higher levels of sustained activity.↵Ancestral State: Ectothermy↵Most ancestral animal`


|条件|前三候选（ID、片段、概率）|真实后继概率|真实后继排名|NLL|相对原模型KL|
|---|---|---:|---:|---:|---:|
|mean_only|320 ' (' 0.2145；11 ',' 0.1893；220 ' ' 0.0894|0.00000|2397|13.2894|12.7449|
|k1|11 ',' 0.4284；320 ' (' 0.2599；220 ' ' 0.0745|0.00000|2546|16.7226|16.0158|
|k4|11 ',' 0.2039；320 ' (' 0.1402；323 ' and' 0.1402|0.00000|2364|14.4024|12.9116|
|k16|330 ' "' 0.1478；220 ' ' 0.0896；279 ' the' 0.0480|0.00014|468|8.8496|7.0617|
|k64|4401 ' development' 0.0955；6513 ' growth' 0.0744；5726 ' ability' 0.0656|0.00784|12|4.8488|2.3729|
|middle|11 ',' 0.1560；320 ' (' 0.1560；279 ' the' 0.1072|0.00000|2747|13.0452|11.7807|
|tail|11 ',' 0.2057；320 ' (' 0.1816；220 ' ' 0.0972|0.00000|1778|12.9561|12.8203|
|head_middle|4401 ' development' 0.2582；5726 ' ability' 0.0838；6513 ' growth' 0.0838|0.00368|24|5.6040|2.1708|
|head_tail|5726 ' ability' 0.0613；330 ' "' 0.0541；6513 ' growth' 0.0478|0.01208|10|4.4164|2.4082|
|k128|4401 ' development' 0.1684；5726 ' ability' 0.1157；15379 ' evolution' 0.0426|0.01775|7|4.0314|1.8421|
|head_random1034|4401 ' development' 0.1910；5726 ' ability' 0.0547；330 ' "' 0.0332|0.00741|16|4.9052|2.5239|
|head_random1035|5726 ' ability' 0.1965；4401 ' development' 0.1052；6513 ' growth' 0.0497|0.02660|4|3.6270|1.3262|
|head_random1036|4401 ' development' 0.2687；6513 ' growth' 0.0600；5726 ' ability' 0.0467|0.00492|23|5.3142|2.6739|
|k256|5726 ' ability' 0.6622；4401 ' development' 0.0791；8654 ' capacity' 0.0291|0.02909|3|3.5373|0.2657|
|k512|5726 ' ability' 0.7968；8654 ' capacity' 0.0309；4401 ' development' 0.0146|0.03089|2|3.4772|0.1043|
|k768|5726 ' ability' 0.7770；4401 ' development' 0.0438；8654 ' capacity' 0.0207|0.02071|3|3.8773|0.1054|
|k1024|5726 ' ability' 0.8851；8654 ' capacity' 0.0343；4650 ' potential' 0.0184|0.03432|2|3.3720|0.0000|
|identity|5726 ' ability' 0.8851；8654 ' capacity' 0.0343；4650 ' potential' 0.0184|0.03432|2|3.3720|0.0000|

### the:R11_A02_297:180 · ecology_evolution

真实后继：ID **4236**，片段 **' five'**。原文：[来源](https://genomebiology.biomedcentral.com/articles/10.1186/gb-2008-9-7-r113)。

完整可见前文：

```text
Skip to content


  • Research
  • Open Access


  • 1,
  • 1,
  • 1,
  • 2,
  • 1 and
  • 1Email author
Genome Biology20089:R113

  • Received: 25 April 2008
  • Accepted: 10 July 2008
  • Published:



Cichlid fish from East Africa are remarkable for phenotypic and behavioral diversity on a backdrop of genomic similarity. In 2006, the Joint Genome Institute completed low coverage survey sequencing of the genomes of five phenotypically and ecologically diverse Lake Malawi species. We report a computational and comparative analysis of these data that provides insight into the mechanisms that make closely related species different from one another.


We produced assemblies for the
```


原文后续（仅用于辨认完整拼写；未进入本位置输入）：` five species ranging in aggregate length from 68 to`


|条件|前三候选（ID、片段、概率）|真实后继概率|真实后继排名|NLL|相对原模型KL|
|---|---|---:|---:|---:|---:|
|mean_only|320 ' (' 0.2145；11 ',' 0.1893；220 ' ' 0.0894|0.00002|522|10.9144|9.3269|
|k1|320 ' (' 0.1373；11 ',' 0.1070；304 ' in' 0.0944|0.00006|487|9.7978|8.0693|
|k4|279 ' the' 0.2938；264 ' a' 0.0954；330 ' "' 0.0351|0.00057|167|7.4749|5.5596|
|k16|279 ' the' 0.0650；9419 ' species' 0.0573；264 ' a' 0.0446|0.00039|258|7.8589|4.9695|
|k64|9419 ' species' 0.0372；1186 ' sub' 0.0256；220 ' ' 0.0225|0.00144|124|6.5421|2.6287|
|middle|320 ' (' 0.1893；220 ' ' 0.1670；11 ',' 0.0894|0.00008|289|9.4770|8.1104|
|tail|320 ' (' 0.2631；11 ',' 0.2049；220 ' ' 0.1243|0.00001|447|11.2103|10.0587|
|head_middle|9419 ' species' 0.0633；220 ' ' 0.0264；356 ' C' 0.0181|0.00315|47|5.7598|2.0388|
|head_tail|9419 ' species' 0.0589；220 ' ' 0.0459；1186 ' sub' 0.0217|0.00157|103|6.4570|2.9200|
|k128|1186 ' sub' 0.0249；9419 ' species' 0.0249；220 ' ' 0.0194|0.00557|27|5.1909|1.7296|
|head_random1034|220 ' ' 0.0558；9419 ' species' 0.0339；3460 ' large' 0.0205|0.00315|54|5.7605|2.2048|
|head_random1035|220 ' ' 0.0352；9419 ' species' 0.0310；1186 ' sub' 0.0213|0.00198|97|6.2224|2.2097|
|head_random1036|220 ' ' 0.0428；9419 ' species' 0.0260；479 ' G' 0.0202|0.00452|38|5.4003|2.3745|
|k256|220 ' ' 0.0391；1378 ' two' 0.0304；3460 ' large' 0.0304|0.01120|11|4.4917|1.2354|
|k512|84281 ' genomes' 0.2235；32769 ' genome' 0.0565；1378 ' two' 0.0343|0.01429|8|4.2483|0.3625|
|k768|84281 ' genomes' 0.3225；2326 ' three' 0.0560；4236 ' five' 0.0560|0.05605|2|2.8815|0.0789|
|k1024|84281 ' genomes' 0.3633；4236 ' five' 0.0557；2326 ' three' 0.0383|0.05571|2|2.8876|0.0000|
|identity|84281 ' genomes' 0.3633；4236 ' five' 0.0557；2326 ' three' 0.0383|0.05571|2|2.8876|0.0000|

## 事后极值：仅按 k256−k64 目标NLL最小／最大选择


### the:R11_A02_093:177 · algebra

真实后继：ID **73621**，片段 **' attic'**。原文：[来源](https://www.shmoop.com/study-guides/math/polynomial-division-rational-expressions)。

完整可见前文：

```text
Study Guide

Polynomial Division and Rational Expressions

Polynomial Division and Rational Expressions Introduction

In this unit, we'll tie up some loose ends like dividing polynomials. We'll also introduce rational expressions, which are like rational numbers but with one polynomial over another instead of one integer over another. That's a good thing, too, because we hate choosing one integer over another. They're like our mathematical children. We like 37 best, to be honest, but don't tell the others.

When you're dealing with polynomial division and rational expressions, watch out for the critical error of dividing by zero. If you're haunted forever by the phrase "Thou shalt not divide by zero,'' that's okay; in this case, being haunted is actually beneficial to your education. If only all ghosts were as helpful. (We're looking at you, creepy girl in the
```


原文后续（仅用于辨认完整拼写；未进入本位置输入）：` attic.)↵↵We'll also discuss how to solve equations that involve polynomial and`


|条件|前三候选（ID、片段、概率）|真实后继概率|真实后继排名|NLL|相对原模型KL|
|---|---|---:|---:|---:|---:|
|mean_only|320 ' (' 0.2145；11 ',' 0.1893；220 ' ' 0.0894|0.00000|29463|19.0081|8.7874|
|k1|11 ',' 0.2223；320 ' (' 0.2223；220 ' ' 0.0927|0.00000|28902|19.4098|9.2077|
|k4|279 ' the' 0.5168；264 ' a' 0.1481；220 ' ' 0.0481|0.00000|24835|18.8163|8.0908|
|k16|220 ' ' 0.2172；279 ' the' 0.0799；330 ' "' 0.0549|0.00000|20677|15.7144|4.4297|
|k64|220 ' ' 0.1841；330 ' "' 0.0411；1378 ' two' 0.0171|0.00000|13681|13.3800|2.9812|
|middle|320 ' (' 0.3315；11 ',' 0.1566；304 ' in' 0.1076|0.00000|28689|18.9479|8.6946|
|tail|320 ' (' 0.1687；11 ',' 0.1488；220 ' ' 0.1023|0.00000|31376|18.9674|8.4543|
|head_middle|220 ' ' 0.1193；330 ' "' 0.0639；1378 ' two' 0.0162|0.00000|13395|13.1883|2.7297|
|head_tail|220 ' ' 0.1611；330 ' "' 0.0461；1142 ' case' 0.0317|0.00000|15094|13.7009|2.9976|
|k128|220 ' ' 0.0632；330 ' "' 0.0205；3691 ' black' 0.0141|0.00001|7761|11.7615|2.2557|
|head_random1034|220 ' ' 0.2140；330 ' "' 0.0226；5567 ' paper' 0.0107|0.00000|13838|13.6041|2.8870|
|head_random1035|220 ' ' 0.0897；330 ' "' 0.0330；328 ' S' 0.0095|0.00000|9552|12.2866|2.3861|
|head_random1036|220 ' ' 0.3048；330 ' "' 0.0467；1378 ' two' 0.0250|0.00000|14302|14.0007|3.1822|
|k256|220 ' ' 0.0655；502 ' j' 0.0146；5700 ' movie' 0.0114|0.00039|400|7.8507|1.4744|
|k512|220 ' ' 0.0359；5700 ' movie' 0.0279；259 ' t' 0.0150|0.00202|70|6.2028|0.7579|
|k768|5700 ' movie' 0.0271；220 ' ' 0.0145；2310 ' old' 0.0145|0.00415|41|5.4837|0.3284|
|k1024|5700 ' movie' 0.0317；6319 ' dark' 0.0192；30641 ' basement' 0.0192|0.01028|14|4.5775|0.0000|
|identity|5700 ' movie' 0.0317；6319 ' dark' 0.0192；30641 ' basement' 0.0192|0.01028|14|4.5775|0.0000|

### the:R11_A02_267:142 · ecology_evolution

真实后继：ID **9419**，片段 **' species'**。原文：[来源](https://www.livescience.com/animals/birds/worlds-fattest-parrot-has-record-breaking-breeding-season)。

完整可见前文：

```text
A critically endangered bird that almost went extinct 30 years ago just recorded a major milestone: The kākāpō recovery program in New Zealand has celebrated the 105th kākāpō egg to hatch ‪—‬ the largest number since records began 30 years ago, according to the
New Zealand broadcaster RNZ
.
In an
updated chick count
released April 3, representatives from the New Zealand Department of Conservation said 105 kākāpō chicks had hatched from 256 eggs laid. Of these, 98 chicks are still alive. One egg remains in an incubator.
The achievement hints that the
```


原文后续（仅用于辨认完整拼写；未进入本位置输入）：` species, which reproduces only every two to four years, may be making a comeback. The↵kākāpō↵(↵Stri`


|条件|前三候选（ID、片段、概率）|真实后继概率|真实后继排名|NLL|相对原模型KL|
|---|---|---:|---:|---:|---:|
|mean_only|320 ' (' 0.2145；11 ',' 0.1893；220 ' ' 0.0894|0.00003|433|10.5394|7.4722|
|k1|320 ' (' 0.1988；11 ',' 0.1548；304 ' in' 0.0939|0.00004|429|10.2404|7.1665|
|k4|279 ' the' 0.4012；264 ' a' 0.1476；220 ' ' 0.0543|0.00113|57|6.7882|6.0767|
|k16|279 ' the' 0.1010；330 ' "' 0.0787；264 ' a' 0.0372|0.01206|6|4.4177|3.8437|
|k64|7042 ' population' 0.0496；330 ' "' 0.0437；220 ' ' 0.0301|0.01253|5|4.3794|3.1734|
|middle|320 ' (' 0.2096；11 ',' 0.1633；220 ' ' 0.0990|0.00004|328|10.0625|7.1271|
|tail|11 ',' 0.2348；320 ' (' 0.2072；220 ' ' 0.0979|0.00004|301|10.1992|7.5149|
|head_middle|7042 ' population' 0.0727；330 ' "' 0.0389；220 ' ' 0.0303|0.01838|4|3.9965|2.9858|
|head_tail|330 ' "' 0.0847；220 ' ' 0.0453；7042 ' population' 0.0353|0.02142|4|3.8434|3.0254|
|k128|7042 ' population' 0.0610；220 ' ' 0.0419；1156 ' first' 0.0254|0.00567|21|5.1722|2.7236|
|head_random1034|7042 ' population' 0.0659；220 ' ' 0.0453；330 ' "' 0.0311|0.01888|5|3.9699|2.7097|
|head_random1035|7042 ' population' 0.0825；1293 ' long' 0.0209；39208 ' breeding' 0.0184|0.01265|7|4.3702|2.8950|
|head_random1036|330 ' "' 0.0487；220 ' ' 0.0430；7042 ' population' 0.0430|0.02302|4|3.7713|2.8285|
|k256|7042 ' population' 0.0799；220 ' ' 0.0485；1156 ' first' 0.0485|0.00451|27|5.4019|2.1029|
|k512|7042 ' population' 0.0593；220 ' ' 0.0360；13351 ' recovery' 0.0360|0.01499|10|4.2005|0.9680|
|k768|2025 ' program' 0.1495；7042 ' population' 0.1319；595 ' k' 0.0800|0.02944|5|3.5254|0.3090|
|k1024|595 ' k' 0.2860；2025 ' program' 0.0928；13351 ' recovery' 0.0723|0.03870|6|3.2519|0.0000|
|identity|595 ' k' 0.2860；2025 ' program' 0.0928；13351 ' recovery' 0.0723|0.03870|6|3.2519|0.0000|

### natural:R11_A02_141:58 · number_theory

真实后继：ID **94574**，片段 **'trand'**。原文：[来源](http://en.wikipedia.org/wiki/Ramanujan_prime)。

完整可见前文：

```text
In mathematics, a Ramanujan prime is a prime number that satisfies a result proven by Srinivasa Ramanujan relating to the prime-counting function.

Origins and definition[edit]

In 1919, Ramanujan published a new proof of Ber
```


原文后续（仅用于辨认完整拼写；未进入本位置输入）：`trand's postulate which, as he notes, was first proved by Chebyshev.[1] At the end of the two-page p`


|条件|前三候选（ID、片段、概率）|真实后继概率|真实后继排名|NLL|相对原模型KL|
|---|---|---:|---:|---:|---:|
|mean_only|320 ' (' 0.2145；11 ',' 0.1893；220 ' ' 0.0894|0.00000|59292|22.2503|21.9351|
|k1|13 '.' 0.3979；11 ',' 0.2734；12 '-' 0.2413|0.00000|25478|40.2654|39.8197|
|k4|198 '\n' 0.5737；320 ' (' 0.2710；220 ' ' 0.0776|0.00000|32066|44.4307|44.0236|
|k16|220 ' ' 0.3464；12 '-' 0.2698；198 '\n' 0.2698|0.00000|11413|34.5718|34.1315|
|k64|11 ',' 0.7559；74 'k' 0.0903；198 '\n' 0.0332|0.00000|1921|22.1549|21.8225|
|middle|220 ' ' 0.1461；11 ',' 0.1290；320 ' (' 0.1138|0.00000|35936|19.0796|18.7984|
|tail|320 ' (' 0.3167；11 ',' 0.2795；304 ' in' 0.0624|0.00000|56137|22.0873|21.7690|
|head_middle|198 '\n' 0.2230；76 'm' 0.1968；11 ',' 0.1737|0.00000|448|14.1879|13.9437|
|head_tail|11 ',' 0.5635；74 'k' 0.3418；77 'n' 0.0218|0.00000|1825|21.1986|20.8715|
|k128|1268 'ier' 0.7547；74 'k' 0.0547；7526 'win' 0.0138|0.00000|602|14.2814|14.0411|
|head_random1034|74 'k' 0.5400；11 ',' 0.0938；12 '-' 0.0828|0.00000|899|16.4911|16.2073|
|head_random1035|198 '\n' 0.5671；276 'an' 0.1625；11 ',' 0.0677|0.00000|1539|18.2546|17.9311|
|head_random1036|11 ',' 0.3868；12 '-' 0.1423；265 're' 0.0978|0.00000|1385|18.0123|17.6936|
|k256|7526 'win' 0.3602；376 'tr' 0.1502；283 'ou' 0.0804|0.01397|12|4.2711|4.1924|
|k512|94574 'trand' 0.9922；376 'tr' 0.0019；7526 'win' 0.0005|0.99219|1|0.0078|0.0472|
|k768|94574 'trand' 0.9794；303 'nd' 0.0066；7526 'win' 0.0031|0.97937|1|0.0208|0.0132|
|k1024|94574 'trand' 0.9764；303 'nd' 0.0084；339 'th' 0.0013|0.97641|1|0.0239|0.0000|
|identity|94574 'trand' 0.9764；303 'nd' 0.0084；339 'th' 0.0013|0.97641|1|0.0239|0.0000|

### natural:R11_A02_286:44 · molecular_genetics

真实后继：ID **11**，片段 **','**。原文：[来源](https://www.wyzant.com/resources/answers/3021/how_are_genes_inherited_from_a_mom_or_dad_to_a_child)。

完整可见前文：

```text
Sexual reproduction at the molecular level is a very complicated sequents of events.  Every gene is found on a specific chromosome.  Ther are 46 chromosomes in humans, and each chromosome has a pair
```


原文后续（仅用于辨认完整拼写；未进入本位置输入）：`, so that there are 23 pairs of chromosomes (there are two copies of each gene).  Sex cells are hapl`


|条件|前三候选（ID、片段、概率）|真实后继概率|真实后继排名|NLL|相对原模型KL|
|---|---|---:|---:|---:|---:|
|mean_only|320 ' (' 0.2145；11 ',' 0.1893；220 ' ' 0.0894|0.18931|2|1.6644|3.5825|
|k1|320 ' (' 0.1410；11 ',' 0.0969；304 ' in' 0.0969|0.09691|2|2.3339|3.5298|
|k4|11 ',' 0.4404；304 ' in' 0.1430；323 ' and' 0.0675|0.44044|1|0.8200|3.0215|
|k16|11 ',' 0.4928；323 ' and' 0.1412；13 '.' 0.0667|0.49282|1|0.7076|3.2183|
|k64|315 ' of' 0.3173；11 ',' 0.2800；13 '.' 0.1698|0.28002|2|1.2729|0.8487|
|middle|320 ' (' 0.2313；11 ',' 0.2041；220 ' ' 0.0964|0.20413|2|1.5890|3.6290|
|tail|11 ',' 0.1777；320 ' (' 0.1777；304 ' in' 0.0951|0.17768|1|1.7278|3.5197|
|head_middle|315 ' of' 0.3357；11 ',' 0.2963；13 '.' 0.1399|0.29627|2|1.2165|0.7974|
|head_tail|315 ' of' 0.3576；11 ',' 0.2458；13 '.' 0.1689|0.24579|2|1.4033|0.7397|
|k128|315 ' of' 0.8363；13 '.' 0.0535；11 ',' 0.0324|0.03243|3|3.4288|0.0618|
|head_random1034|315 ' of' 0.3670；11 ',' 0.2523；13 '.' 0.1734|0.25226|2|1.3773|0.7164|
|head_random1035|315 ' of' 0.4238；11 ',' 0.2268；13 '.' 0.1559|0.22684|2|1.4835|0.5907|
|head_random1036|315 ' of' 0.3751；11 ',' 0.2578；13 '.' 0.1564|0.25782|2|1.3555|0.7053|
|k256|315 ' of' 0.9494；13 '.' 0.0197；11 ',' 0.0105|0.01055|3|4.5519|0.0335|
|k512|315 ' of' 0.9060；13 '.' 0.0351；11 ',' 0.0166|0.01659|3|4.0987|0.0113|
|k768|315 ' of' 0.9179；13 '.' 0.0277；11 ',' 0.0131|0.01309|3|4.3357|0.0060|
|k1024|315 ' of' 0.9160；13 '.' 0.0277；11 ',' 0.0148|0.01481|3|4.2127|0.0000|
|identity|315 ' of' 0.9160；13 '.' 0.0277；11 ',' 0.0148|0.01481|3|4.2127|0.0000|

## 输出无关选出的12篇验证文本

每域4篇，按固定哈希规则排除7篇命名／固定展示文档。这里的阅读备注不是外部语义标签，也不是新确认集。

### natural:R11_A02_122:174

完整可见前文：

```text
If you want the expected value, one answer is $n E[S_{(m)}]$, where $S_{(m)}$ is the $m$th order statistic of a sample of $n$ gamma$(k,1)$ random variables. While this expression may not have a simple closed form, you may be able to get a decent-sized approximate answer from the literature on moments of order statistics. (Edit: This appears to be the case, even when comparing with the known asymptotic expression for the case $m=n$. See discussion at end.)

Here's the argument for $n E[S_{(m)}]$: Take a Poisson process $P$ with rate 1 and interarrival times $Z_1, Z_2, \ldots$. Let each event in the process $P$ have probability of $1/n$ of
```

真实后继：ID 1660，片段 ' being'。

|条件|前三候选：ID／片段／概率|目标NLL|目标排名|
|---|---|---:|---:|
|k1|320 ' (' 0.1394；11 ',' 0.0958；304 ' in' 0.0958|7.4701|106|
|k64|279 ' the' 0.3407；429 ' that' 0.1609；264 ' a' 0.0760|5.4519|24|
|k256|1660 ' being' 0.1373；3432 ' having' 0.0735；3259 ' making' 0.0393|1.9857|1|
|identity|30865 ' occurring' 0.4180；1660 ' being' 0.1742；12482 ' happening' 0.0441|1.7473|2|

阅读检查：256维首选being是原文后继，原模型首选occurring；首选命中与更接近原模型应分开。

### natural:R11_A02_135:181

完整可见前文：

```text
A useful rule of thumb in complex analysis is that holomorphic functions
{f(z)}
behave like large degree polynomials
{P(z)}
. This can be evidenced for instance at a “local” level by the Taylor series expansion for a complex analytic function in the disk, or at a “global” level by factorisation theorems such as the
Weierstrass factorisation theorem
(or the closely related Hadamard factorisation theorem). One can truncate these theorems in a variety of ways (e.g., Taylor’s theorem with remainder) to be able to approximate a holomorphic function by a polynomial on various domains.
In some cases it can be convenient instead to work with polynomials
{P(Z)}
of another variable
{Z}
such as
{Z = e^{2\pi i z}}
(or more generally
{Z=e^{2\pi i
```

真实后继：ID 1147，片段 ' z'。

|条件|前三候选：ID／片段／概率|目标NLL|目标排名|
|---|---|---:|---:|
|k1|320 ' (' 0.2003；11 ',' 0.1560；304 ' in' 0.0946|9.5455|276|
|k64|1124 ' \\' 0.6873；11 ',' 0.0388；220 ' ' 0.0388|7.8750|83|
|k256|1124 ' \\' 0.4060；59 '\\' 0.2173；595 ' k' 0.0623|4.7763|10|
|identity|282 ' f' 0.1943；1147 ' z' 0.1513；1124 ' \\' 0.1336|1.8882|2|

阅读检查：目标是公式中的z子词；低维反斜线不能命名为粗语义，公式词面也在变化。

### natural:R11_A02_096:71

完整可见前文：

```text
(2) If someone actually has disease D, then the test always comes back positive: Pr(+|D)=1.

(3) But the test has a false positive rate of 5%. That is, if someone does NOT have D, there is a 5% chance the test still comes back positive: Pr(+|~D)=.0
```

真实后继：ID 20，片段 '5'。

|条件|前三候选：ID／片段／概率|目标NLL|目标排名|
|---|---|---:|---:|
|k1|320 ' (' 0.1410；11 ',' 0.0969；304 ' in' 0.0969|11.0216|1165|
|k64|16 '1' 0.3618；17 '2' 0.1709；15 '0' 0.1508|2.7667|4|
|k256|20 '5' 0.4320；17 '2' 0.0964；16 '1' 0.0851|0.8394|1|
|identity|20 '5' 0.9988；19 '4' 0.0002；21 '6' 0.0002|0.0012|1|

阅读检查：相同前文已出现5%与.0，目标为数字5；后部恢复的是精确续写，不能直接叫细语义。

### natural:R11_A02_134:144

完整可见前文：

```text
In Disney’s 1959 film
Donald in Mathmagic Land
, Donald Duck, inspired by the narrator’s descriptions of the geometry of billiards,
energetically strikes the cue ball
, sending it ricocheting around the table before it finally hits the intended balls. Donald asks, “How do you like that for mathematics?”
Because rectangular billiard tables have four walls meeting at right angles, billiard trajectories like Donald’s are predictable and well understood — even if they’re difficult to carry out in practice. However, research mathematicians still cannot answer basic questions about the possible trajectories of billiard balls on tables in the shape of other polygons (shapes with flat sides). Even triangles, the simplest of
```

真实后继：ID 68159，片段 ' polygons'。

|条件|前三候选：ID／片段／概率|目标NLL|目标排名|
|---|---|---:|---:|
|k1|320 ' (' 0.1818；11 ',' 0.1416；304 ' in' 0.0973|15.8300|12877|
|k64|279 ' the' 0.6147；264 ' a' 0.0505；1378 ' two' 0.0270|6.1117|33|
|k256|279 ' the' 0.3666；678 ' all' 0.1190；1493 ' these' 0.0438|3.5034|7|
|identity|68159 ' polygons' 0.4045；678 ' all' 0.3569；279 ' the' 0.0796|0.9052|1|

阅读检查：原模型首选polygons，256维仍偏the；候选对象词有恢复速度差。

### natural:R11_A02_242:78

完整可见前文：

```text
In December 2024, a comprehensive analysis published in Science by Adamala et al. highlighted unprecedented risks associated with mirror bacteria research. These artificially created organisms would represent a fundamental departure from all known life, utilizing reversed versions of the molecular building blocks found in natural organisms. The authors argue that this reversal could allow such organisms to evade existing biological controls and immune defenses, potentially affecting
```

真实后继：ID 12677，片段 ' humans'。

|条件|前三候选：ID／片段／概率|目标NLL|目标排名|
|---|---|---:|---:|
|k1|320 ' (' 0.1927；11 ',' 0.1701；220 ' ' 0.0910|13.2090|2684|
|k64|279 ' the' 0.8068；264 ' a' 0.0662；458 ' an' 0.0102|9.0897|120|
|k256|279 ' the' 0.6060；264 ' a' 0.0497；678 ' all' 0.0342|6.6259|42|
|identity|279 ' the' 0.1955；3738 ' human' 0.1523；862 ' their' 0.0635|3.6322|6|

阅读检查：原模型仍可首选the，真实后继humans排名6；不是全部高维都恢复真实目标。

### natural:R11_A02_255:117

完整可见前文：

```text
Avoid seeds like the plague!

Good luck, and I hope you have the speediest recovery possible. This is not what you need right now!

Yaya said...

I hope the new meds and diet work!!!

Just Jenn said...

He wants to use a pill cam to test for celiac?! While that test is good for sighting large abnormalities of the intestinal tract, such as ulcers and polyps, it does not diagnose celiac disease, gluten intolerance or other food sensitivities. Villi damage is microscopic which is why an upper intestinal tract biopsy is usually preformed.

In light of
```

真实后继：ID 429，片段 ' that'。

|条件|前三候选：ID／片段／概率|目标NLL|目标排名|
|---|---|---:|---:|
|k1|320 ' (' 0.1288；304 ' in' 0.1003；11 ',' 0.0885|4.6749|13|
|k64|279 ' the' 0.8017；264 ' a' 0.0957；419 ' this' 0.0189|5.8460|9|
|k256|279 ' the' 0.5414；419 ' this' 0.1551；429 ' that' 0.1208|2.1136|3|
|identity|419 ' this' 0.2906；279 ' the' 0.2264；429 ' that' 0.0944|2.3607|3|

阅读检查：256维that的NLL优于原模型；偏离原模型并不必然变差。

### natural:R11_A02_285:134

完整可见前文：

```text
The prothallium develops from a germinating spore. It is a short-lived and inconspicuous heart-shaped structure typically 2-5 millimeters wide, with a number of rhizoids (root-like hairs) growing underneath, and the sex organs: archegonium (female) and antheridium (male). Appearance varies quite a lot between species. Some are green and conduct photosynthesis while others are colorless and nourish themselves underground as saprotrophs.

Alternation of generations[edit]

Prothallus of the tree fern Dicksonia antarctica (note new moss plants for scale)

Spore-bearing plants, like
```

真实后继：ID 678，片段 ' all'。

|条件|前三候选：ID／片段／概率|目标NLL|目标排名|
|---|---|---:|---:|
|k1|320 ' (' 0.1900；11 ',' 0.1480；304 ' in' 0.1017|6.1605|29|
|k64|279 ' the' 0.6766；264 ' a' 0.0382；1045 ' some' 0.0232|5.3907|14|
|k256|279 ' the' 0.2884；77243 ' moss' 0.0826；10779 ' plants' 0.0729|3.6184|8|
|identity|77243 ' moss' 0.2486；678 ' all' 0.1936；87024 ' fern' 0.1508|1.6419|2|

阅读检查：256维已有moss候选，原模型也首选moss而真实后继为all；对象候选与目标准确率不同。

### natural:R11_A02_281:110

完整可见前文：

```text
This question is difficult to answer. You can’t tell by eye which bacteria growing within a petri dish are the “good guys” versus ones that cause disease, and some pathogenic microbes, like viruses, can’t be detected within agar petri dishes.

Nevertheless, with the upcoming holiday travels, asking how to prevent the spread of disease-causing pathogens isn’t just for aspiring microbiologists but a great question for everyone.

Do we really stand a chance of keeping our hands clean from germs?

Two-fisted approach

There are two main strategies.


```

真实后继：ID 785，片段 'The'。

|条件|前三候选：ID／片段／概率|目标NLL|目标排名|
|---|---|---:|---:|
|k1|320 ' (' 0.1407；11 ',' 0.0967；304 ' in' 0.0967|11.2110|1310|
|k64|785 'The' 0.1321；641 'In' 0.1166；32 'A' 0.0707|2.0240|1|
|k256|785 'The' 0.2433；641 'In' 0.0790；32 'A' 0.0615|1.4134|1|
|identity|785 'The' 0.2670；220 ' ' 0.1620；5338 'First' 0.1429|1.3204|1|

阅读检查：段落起始The在64维已是首选；这是文体／句法边界的真实上下文。

### natural:R11_A02_410:109

完整可见前文：

```text
You've read a lot about 'invisibility' over the last few years.  Mathematicians and scientists have been working on various devices that enable invisibility cloaks which shield small objects from detection by microwaves or sound waves.

An international team has devised an amplifier that can boost light, sound or other waves while hiding them inside an invisible container. As a first application, the researchers propose manipulating matter waves, which are the mathematical description of particles in quantum mechanics. The researchers envision building a quantum microscope that could capture quantum waves, the
```

真实后继：ID 16876，片段 ' waves'。

|条件|前三候选：ID／片段／概率|目标NLL|目标排名|
|---|---|---:|---:|
|k1|320 ' (' 0.1828；11 ',' 0.1614；304 ' in' 0.0979|15.3867|9376|
|k64|330 ' "' 0.1135；35972 ' mathematical' 0.0224；6961 ' physical' 0.0154|9.8631|1868|
|k256|1156 ' first' 0.0643；1429 ' most' 0.0442；1616 ' way' 0.0209|7.9938|394|
|identity|24632 ' smallest' 0.0694；11811 ' researchers' 0.0477；4752 ' building' 0.0421|4.6676|18|

阅读检查：原模型对真实waves仍只排18；不要求投影恢复一个原模型未选中的首选。

### natural:R11_A02_419:64

完整可见前文：

```text
We know that light is a form of energy and can undergo various phenomena like diffraction, reflection, refraction, interference, and polarisation. Refraction is the phenomenon that takes place due to the bending of light when it travels from medium to another. In this article, let us briefly understand the process of refraction.

```

真实后继：ID 3838，片段 'What'。

|条件|前三候选：ID／片段／概率|目标NLL|目标排名|
|---|---|---:|---:|
|k1|320 ' (' 0.1599；11 ',' 0.1245；304 ' in' 0.0970|14.2082|6784|
|k64|785 'The' 0.2549；32 'A' 0.1365；641 'In' 0.0730|4.6168|10|
|k256|785 'The' 0.3234；32 'A' 0.0818；641 'In' 0.0637|3.7538|6|
|identity|3838 'What' 0.2084；785 'The' 0.1115；3945 'Ref' 0.1115|1.5685|1|

阅读检查：原模型首选What，64／256维仍偏The；带字母的篇章格式不在纯标点掩码中。

### natural:R11_A02_434:160

完整可见前文：

```text
The ratio of reflected intensity to incident intensity is the X-ray reflectivity for the surface. If the interface is not perfectly sharp and smooth, the reflected intensity will deviate from that predicted by the law of Fresnel reflectivity. The deviations can then be analyzed to obtain the density profile of the interface normal to the surface. For films with multiple layers, X-ray reflectivity may show oscillations with wavelength, analogous to the Fabry-Pérot effect. These oscillations can be used to infer layer thicknesses and other properties.



In X-ray diffraction a beam strikes a crystal and diffracts into many specific directions. The angles and intensities of the diffracted beams indicate a three-dimensional density of electrons within the crystal. X-rays produce a diffraction pattern because their wavelength is typically the
```

真实后继：ID 1852，片段 ' same'。

|条件|前三候选：ID／片段／概率|目标NLL|目标排名|
|---|---|---:|---:|
|k1|11 ',' 0.3198；320 ' (' 0.2822；220 ' ' 0.0916|13.0151|666|
|k64|330 ' "' 0.2285；220 ' ' 0.1780；1372 ' number' 0.0273|5.3510|22|
|k256|1379 ' size' 0.0822；8028 ' minimum' 0.0726；220 ' ' 0.0440|3.2482|5|
|identity|1852 ' same' 0.7004；1973 ' order' 0.0738；24632 ' smallest' 0.0738|0.3561|1|

阅读检查：常见关系词same到256维仍排5；常见不保证每个位置都早恢复。

### natural:R11_A02_422:151

完整可见前文：

```text
Shedding light on the mystery of the superconducting dome

Shedding light on the mystery of the superconducting dome
Prof. dr. Justin Ye, Zernike Insititute of Advanced Materials, Faculty of Science and Engineering, University of Groningen Credit: ZIAM/University of Groningen

University of Groningen physicists, and colleagues from Nijmegen and Hong Kong, have induced superconductivity in a monolayer of tungsten disulfide. By using an increasing electric field, they were able to show how the material turns from an insulator into a superconductor and then back into a re-entrant insulator again. Their results show the typical dome-shaped superconducting phase, and finally provide
```

真实后继：ID 458，片段 ' an'。

|条件|前三候选：ID／片段／概率|目标NLL|目标排名|
|---|---|---:|---:|
|k1|320 ' (' 0.1404；11 ',' 0.0965；304 ' in' 0.0965|4.8384|17|
|k64|279 ' the' 0.4889；264 ' a' 0.2309；458 ' an' 0.0401|3.2157|3|
|k256|264 ' a' 0.4687；279 ' the' 0.1046；458 ' an' 0.0923|2.3827|3|
|identity|264 ' a' 0.3506；279 ' the' 0.1290；458 ' an' 0.0886|2.4232|3|

阅读检查：冠词an在256维NLL略优于原模型；不能用词频或首选一致率代替目标概率。

# 固定自然文本：完整输入、token位置与分段解码

所有解码为在同一当前位置的下一token分布，不是把各位置首选拼成自回归生成。区间单独保留并加回训练均值；当前位置t读到x_t后预测x_(t+1)。输入句子可能尚未结束，原文后续仅参考。

## natural:R11_A02_096:71


输入文档：R11_A02_096；领域：math／probability_statistics；来源：[原始来源](http://obscureandconfused.blogspot.com/2016/03/the-no-miracles-argument-may-not-commit.html?showComment=1457848360014)。

**当前输入token：ID15，片段 `'0'`；0基位置t=71，即第72个token。可见输入共72个token。**

当前句子／段落已经可见的部分：

> That is, if someone does NOT have D, there is a 5% chance the test still comes back positive: Pr(+|~D)=.0

全部可见输入（没有省略号；到当前token为止）：

```text
(2) If someone actually has disease D, then the test always comes back positive: Pr(+|D)=1.

(3) But the test has a false positive rate of 5%. That is, if someone does NOT have D, there is a 5% chance the test still comes back positive: Pr(+|~D)=.0
```

在此预测下一个token。真实后继：ID20，片段 `'5'`。后继是语料参考，不等于原模型一定首选。


|0基位置|第几个token|ID|片段|是否已见|标记|

|---:|---:|---:|---|---|---|

|65|66|40938|`'(+'`|是||

|66|67|91|`'\|'`|是||

|67|68|93|`'~'`|是||

|68|69|35|`'D'`|是||

|69|70|11730|`')='`|是||

|70|71|13|`'.'`|是||

|71|72|15|`'0'`|是|当前输入|

|72|73|20|`'5'`|否|真实后继|

|73|74|382|`'.\n\n'`|否||

|74|75|7039|`'Now'`|否||


|解码条件|前三候选：ID／片段／概率|真实后继概率|排名|NLL|与原模型KL|

|---|---|---:|---:|---:|---:|

|PC16–31（16维）|11 `','` 36.389%；320 `' ('` 10.426%；220 `' '` 9.201%|0.01891%|121|8.5734|8.5607|

|PC32–63（32维）|11 `','` 46.360%；279 `' the'` 7.110%；13 `'.'` 6.274%|0.00648%|258|9.6437|9.6305|

|PC64–127（64维）|11 `','` 21.243%；220 `' '` 12.884%；320 `' ('` 10.034%|0.14313%|38|6.5491|6.5375|

|PC128–255（128维）|220 `' '` 24.778%；320 `' ('` 13.263%；323 `' and'` 5.529%|0.00885%|368|9.3327|9.3210|

|PC256–511（256维）|264 `' a'` 14.532%；220 `' '` 12.824%；11 `','` 6.864%|0.23489%|40|6.0538|6.0453|

|PC512–767（256维）|304 `' in'` 29.014%；11 `','` 17.598%；320 `' ('` 12.095%|0.07192%|54|7.2374|7.2292|

|PC768–959（192维）|320 `' ('` 37.427%；11 `','` 10.723%；323 `' and'` 9.463%|0.00672%|281|9.6078|9.5964|

|PC960–1024（65维）|11 `','` 19.873%；320 `' ('` 17.538%；220 `' '` 9.387%|0.00203%|541|10.8033|10.7903|

|PC512–575（64维）|11 `','` 18.311%；320 `' ('` 16.160%；304 `' in'` 14.261%|0.00478%|337|9.9476|9.9354|

|PC768–831（64维）|11 `','` 17.639%；320 `' ('` 17.639%；220 `' '` 13.737%|0.00337%|381|10.2976|10.2849|

|PC961–1024（64维）|11 `','` 20.331%；320 `' ('` 17.942%；304 `' in'` 9.603%|0.00195%|569|10.8430|10.8300|

|仅训练均值|320 `' ('` 21.452%；11 `','` 18.931%；220 `' '` 8.942%|0.00151%|590|11.1019|11.0883|

|原模型|20 `'5'` 99.878%；19 `'4'` 0.023%；21 `'6'` 0.023%|99.87836%|1|0.0012|0.0000|


原文参考整句（可能包含当前位置尚未看到的后文，**不是该位置输入**）：

```text
That is, if someone does NOT have D, there is a 5% chance the test still comes back positive: Pr(+|~D)=.05.
```
## natural:R11_A02_122:174


输入文档：R11_A02_122；领域：math／probability_statistics；来源：[原始来源](http://mathoverflow.net/questions/41935/how-to-solve-a-generalization-of-the-coupon-collectors-problem?sort=votes)。

**当前输入token：ID315，片段 `' of'`；0基位置t=174，即第175个token。可见输入共175个token。**

当前句子／段落已经可见的部分：

> Let each event in the process $P$ have probability of $1/n$ of

全部可见输入（没有省略号；到当前token为止）：

```text
If you want the expected value, one answer is $n E[S_{(m)}]$, where $S_{(m)}$ is the $m$th order statistic of a sample of $n$ gamma$(k,1)$ random variables. While this expression may not have a simple closed form, you may be able to get a decent-sized approximate answer from the literature on moments of order statistics. (Edit: This appears to be the case, even when comparing with the known asymptotic expression for the case $m=n$. See discussion at end.)

Here's the argument for $n E[S_{(m)}]$: Take a Poisson process $P$ with rate 1 and interarrival times $Z_1, Z_2, \ldots$. Let each event in the process $P$ have probability of $1/n$ of
```

在此预测下一个token。真实后继：ID1660，片段 `' being'`。后继是语料参考，不等于原模型一定首选。


|0基位置|第几个token|ID|片段|是否已见|标记|

|---:|---:|---:|---|---|---|

|168|169|18927|`' probability'`|是||

|169|170|315|`' of'`|是||

|170|171|400|`' $'`|是||

|171|172|16|`'1'`|是||

|172|173|9612|`'/n'`|是||

|173|174|3|`'$'`|是||

|174|175|315|`' of'`|是|当前输入|

|175|176|1660|`' being'`|否|真实后继|

|176|177|279|`' the'`|否||

|177|178|1156|`' first'`|否||


|解码条件|前三候选：ID／片段／概率|真实后继概率|排名|NLL|与原模型KL|

|---|---|---:|---:|---:|---:|

|PC16–31（16维）|320 `' ('` 17.488%；304 `' in'` 12.019%；323 `' and'` 10.607%|0.09177%|58|6.9937|7.3816|

|PC32–63（32维）|279 `' the'` 36.239%；264 `' a'` 13.332%；220 `' '` 9.163%|0.08983%|39|7.0150|7.5565|

|PC64–127（64维）|220 `' '` 27.076%；11 `','` 14.493%；330 `' "'` 7.758%|1.34806%|10|4.3065|5.0306|

|PC128–255（128维）|320 `' ('` 38.087%；11 `','` 20.386%；323 `' and'` 7.500%|0.09441%|40|6.9653|7.7618|

|PC256–511（256维）|11 `','` 20.693%；220 `' '` 14.222%；320 `' ('` 12.551%|0.17903%|39|6.3254|5.8902|

|PC512–767（256维）|320 `' ('` 30.287%；11 `','` 12.625%；323 `' and'` 6.758%|0.09056%|58|7.0070|7.2031|

|PC768–959（192维）|320 `' ('` 30.219%；11 `','` 14.274%；220 `' '` 7.640%|0.04543%|91|7.6967|9.0989|

|PC960–1024（65维）|320 `' ('` 32.354%；11 `','` 15.283%；220 `' '` 8.180%|0.02604%|100|8.2534|9.7733|

|PC512–575（64维）|320 `' ('` 24.976%；11 `','` 17.166%；220 `' '` 8.109%|0.03314%|110|8.0123|9.0618|

|PC768–831（64维）|320 `' ('` 28.519%；11 `','` 17.298%；220 `' '` 7.211%|0.04288%|94|7.7546|9.1728|

|PC961–1024（64维）|320 `' ('` 32.125%；11 `','` 15.175%；220 `' '` 8.122%|0.02429%|104|8.3230|9.8203|

|仅训练均值|320 `' ('` 21.452%；11 `','` 18.931%；220 `' '` 8.942%|0.02217%|124|8.4144|9.4774|

|原模型|30865 `' occurring'` 41.799%；1660 `' being'` 17.424%；12482 `' happening'` 4.406%|17.42437%|2|1.7473|0.0000|


原文参考整句（可能包含当前位置尚未看到的后文，**不是该位置输入**）：

```text
Let each event in the process $P$ have probability of $1/n$ of being the first kind of coupon, probability $1/n$ of being the second kind
```
## natural:R11_A02_134:144


输入文档：R11_A02_134；领域：math／geometry_topology；来源：[原始来源](https://www.quantamagazine.org/the-mysterious-math-of-billiards-tables-20240215/)。

**当前输入token：ID315，片段 `' of'`；0基位置t=144，即第145个token。可见输入共145个token。**

当前句子／段落已经可见的部分：

> Even triangles, the simplest of

全部可见输入（没有省略号；到当前token为止）：

```text
In Disney’s 1959 film
Donald in Mathmagic Land
, Donald Duck, inspired by the narrator’s descriptions of the geometry of billiards,
energetically strikes the cue ball
, sending it ricocheting around the table before it finally hits the intended balls. Donald asks, “How do you like that for mathematics?”
Because rectangular billiard tables have four walls meeting at right angles, billiard trajectories like Donald’s are predictable and well understood — even if they’re difficult to carry out in practice. However, research mathematicians still cannot answer basic questions about the possible trajectories of billiard balls on tables in the shape of other polygons (shapes with flat sides). Even triangles, the simplest of
```

在此预测下一个token。真实后继：ID68159，片段 `' polygons'`。后继是语料参考，不等于原模型一定首选。


|0基位置|第几个token|ID|片段|是否已见|标记|

|---:|---:|---:|---|---|---|

|138|139|568|`').'`|是||

|139|140|7418|`' Even'`|是||

|140|141|42446|`' triangles'`|是||

|141|142|11|`','`|是||

|142|143|279|`' the'`|是||

|143|144|44548|`' simplest'`|是||

|144|145|315|`' of'`|是|当前输入|

|145|146|68159|`' polygons'`|否|真实后继|

|146|147|11|`','`|否||

|147|148|2058|`' still'`|否||


|解码条件|前三候选：ID／片段／概率|真实后继概率|排名|NLL|与原模型KL|

|---|---|---:|---:|---:|---:|

|PC16–31（16维）|11 `','` 25.031%；279 `' the'` 15.182%；220 `' '` 13.398%|6.47e-04%|1088|11.9476|6.9599|

|PC32–63（32维）|320 `' ('` 42.754%；11 `','` 10.810%；220 `' '` 5.786%|1.24e-04%|3818|13.5997|8.1519|

|PC64–127（64维）|320 `' ('` 22.798%；11 `','` 17.755%；315 `' of'` 10.769%|3.58e-04%|2301|12.5410|7.0118|

|PC128–255（128维）|220 `' '` 25.930%；279 `' the'` 25.930%；320 `' ('` 9.539%|2.30e-05%|7886|15.2873|7.3012|

|PC256–511（256维）|220 `' '` 20.141%；320 `' ('` 10.780%；323 `' and'` 10.780%|2.79e-04%|2778|12.7899|6.3140|

|PC512–767（256维）|11 `','` 16.979%；320 `' ('` 16.979%；220 `' '` 13.223%|8.65e-05%|4471|13.9607|7.6447|

|PC768–959（192维）|320 `' ('` 30.149%；11 `','` 16.138%；220 `' '` 9.788%|3.02e-05%|6311|15.0115|8.7765|

|PC960–1024（65维）|11 `','` 21.124%；320 `' ('` 16.452%；220 `' '` 11.307%|5.53e-06%|9864|16.7110|9.5181|

|PC512–575（64维）|11 `','` 19.003%；320 `' ('` 16.770%；220 `' '` 8.976%|9.00e-06%|11909|16.2231|8.9427|

|PC768–831（64维）|320 `' ('` 29.031%；11 `','` 13.713%；220 `' '` 10.680%|8.34e-06%|10659|16.2993|9.4126|

|PC961–1024（64维）|11 `','` 21.083%；320 `' ('` 16.420%；220 `' '` 11.285%|5.69e-06%|9847|16.6817|9.4576|

|仅训练均值|320 `' ('` 21.452%；11 `','` 18.931%；220 `' '` 8.942%|6.36e-06%|12617|16.5706|9.4874|

|原模型|68159 `' polygons'` 40.447%；678 `' all'` 35.694%；279 `' the'` 7.964%|40.44668%|1|0.9052|0.0000|


原文参考整句（可能包含当前位置尚未看到的后文，**不是该位置输入**）：

```text
Even triangles, the simplest of polygons, still hold mysteries.
```
## natural:R11_A02_135:181


输入文档：R11_A02_135；领域：math／analysis；来源：[原始来源](https://terrytao.wordpress.com/2019/05/03/local-trigonometric-polynomial-approximations-to-the-riemann-zeta-function/)。

**当前输入token：ID600，片段 `' i'`；0基位置t=181，即第182个token。可见输入共182个token。**

当前句子／段落已经可见的部分：

> {Z=e^{2\pi i

全部可见输入（没有省略号；到当前token为止）：

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

在此预测下一个token。真实后继：ID1147，片段 `' z'`。后继是语料参考，不等于原模型一定首选。


|0基位置|第几个token|ID|片段|是否已见|标记|

|---:|---:|---:|---|---|---|

|175|176|57|`'Z'`|是||

|176|177|40391|`'=e'`|是||

|177|178|47822|`'^{'`|是||

|178|179|17|`'2'`|是||

|179|180|59|`'\\'`|是||

|180|181|2493|`'pi'`|是||

|181|182|600|`' i'`|是|当前输入|

|182|183|1147|`' z'`|否|真实后继|

|183|184|20290|`'/N'`|否||

|184|185|11248|`'}}\n'`|否||


|解码条件|前三候选：ID／片段／概率|真实后继概率|排名|NLL|与原模型KL|

|---|---|---:|---:|---:|---:|

|PC16–31（16维）|11 `','` 77.242%；320 `' ('` 10.454%；220 `' '` 1.415%|0.02018%|73|8.5082|4.8253|

|PC32–63（32维）|11 `','` 16.719%；320 `' ('` 11.491%；264 `' a'` 10.141%|0.02848%|127|8.1636|4.6380|

|PC64–127（64维）|264 `' a'` 18.068%；320 `' ('` 12.418%；279 `' the'` 9.671%|0.09481%|71|6.9610|4.1425|

|PC128–255（128维）|264 `' a'` 23.718%；320 `' ('` 18.472%；304 `' in'` 4.122%|0.08554%|79|7.0639|3.6172|

|PC256–511（256维）|264 `' a'` 35.457%；320 `' ('` 35.457%；220 `' '` 4.799%|0.01626%|125|8.7244|4.6703|

|PC512–767（256维）|304 `' in'` 13.410%；320 `' ('` 13.410%；264 `' a'` 10.444%|0.05148%|86|7.5717|4.8376|

|PC768–959（192维）|320 `' ('` 21.051%；220 `' '` 12.768%；264 `' a'` 9.944%|0.06294%|94|7.3707|4.7028|

|PC960–1024（65维）|320 `' ('` 21.603%；11 `','` 16.825%；304 `' in'` 11.563%|0.00601%|281|9.7198|5.7571|

|PC512–575（64维）|320 `' ('` 24.794%；304 `' in'` 10.336%；11 `','` 9.121%|0.01371%|160|8.8946|5.5537|

|PC768–831（64维）|320 `' ('` 32.609%；11 `','` 9.343%；220 `' '` 9.343%|0.02044%|142|8.4956|5.2592|

|PC961–1024（64维）|320 `' ('` 23.207%；11 `','` 15.950%；304 `' in'` 10.962%|0.00606%|279|9.7107|5.7670|

|仅训练均值|320 `' ('` 21.452%；11 `','` 18.931%；220 `' '` 8.942%|0.00560%|274|9.7894|5.8584|

|原模型|282 `' f'` 19.433%；1147 `' z'` 15.135%；1124 `' \\'` 13.356%|15.13457%|2|1.8882|0.0000|


原文参考整句（可能包含当前位置尚未看到的后文，**不是该位置输入**）：

```text
{Z=e^{2\pi i z/N}}

```
## natural:R11_A02_242:78


输入文档：R11_A02_242；领域：biology／microbiology_immunity；来源：[原始来源](https://www.scienceforums.net/topic/135294-confronting-risks-of-mirror-life/)。

**当前输入token：ID27887，片段 `' affecting'`；0基位置t=78，即第79个token。可见输入共79个token。**

当前句子／段落已经可见的部分：

> The authors argue that this reversal could allow such organisms to evade existing biological controls and immune defenses, potentially affecting

全部可见输入（没有省略号；到当前token为止）：

```text
In December 2024, a comprehensive analysis published in Science by Adamala et al. highlighted unprecedented risks associated with mirror bacteria research. These artificially created organisms would represent a fundamental departure from all known life, utilizing reversed versions of the molecular building blocks found in natural organisms. The authors argue that this reversal could allow such organisms to evade existing biological controls and immune defenses, potentially affecting
```

在此预测下一个token。真实后继：ID12677，片段 `' humans'`。后继是语料参考，不等于原模型一定首选。


|0基位置|第几个token|ID|片段|是否已见|标记|

|---:|---:|---:|---|---|---|

|72|73|11574|`' controls'`|是||

|73|74|323|`' and'`|是||

|74|75|22077|`' immune'`|是||

|75|76|45516|`' defenses'`|是||

|76|77|11|`','`|是||

|77|78|13581|`' potentially'`|是||

|78|79|27887|`' affecting'`|是|当前输入|

|79|80|12677|`' humans'`|否|真实后继|

|80|81|11|`','`|否||

|81|82|9898|`' animals'`|否||


|解码条件|前三候选：ID／片段／概率|真实后继概率|排名|NLL|与原模型KL|

|---|---|---:|---:|---:|---:|

|PC16–31（16维）|11 `','` 47.414%；320 `' ('` 17.443%；220 `' '` 4.997%|3.10e-04%|1277|12.6838|5.2859|

|PC32–63（32维）|279 `' the'` 20.893%；320 `' ('` 12.673%；323 `' and'` 8.710%|1.99e-04%|2378|13.1282|4.5207|

|PC64–127（64维）|323 `' and'` 34.195%；11 `','` 12.580%；320 `' ('` 8.646%|3.46e-04%|1668|12.5731|4.7215|

|PC128–255（128维）|320 `' ('` 26.162%；220 `' '` 15.868%；323 `' and'` 10.906%|8.16e-04%|1277|11.7158|4.3097|

|PC256–511（256维）|11 `','` 25.310%；323 `' and'` 10.551%；320 `' ('` 9.311%|0.00108%|1064|11.4365|4.4157|

|PC512–767（256维）|320 `' ('` 19.204%；220 `' '` 16.947%；11 `','` 14.956%|3.41e-04%|1873|12.5876|4.8866|

|PC768–959（192维）|11 `','` 13.608%；304 `' in'` 13.608%；320 `' ('` 12.009%|8.99e-04%|1284|11.6195|4.6503|

|PC960–1024（65维）|11 `','` 17.464%；320 `' ('` 17.464%；304 `' in'` 9.348%|1.38e-04%|3555|13.4951|4.9737|

|PC512–575（64维）|11 `','` 18.785%；320 `' ('` 18.785%；220 `' '` 12.911%|2.95e-04%|1946|12.7346|5.1167|

|PC768–831（64维）|11 `','` 19.415%；320 `' ('` 17.134%；220 `' '` 10.392%|2.86e-04%|1876|12.7641|5.1736|

|PC961–1024（64维）|11 `','` 17.471%；320 `' ('` 17.471%；304 `' in'` 9.352%|1.38e-04%|3537|13.4946|4.9802|

|仅训练均值|320 `' ('` 21.452%；11 `','` 18.931%；220 `' '` 8.942%|1.24e-04%|2882|13.6019|5.4343|

|原模型|279 `' the'` 19.550%；3738 `' human'` 15.225%；862 `' their'` 6.347%|2.64575%|6|3.6322|0.0000|


原文参考整句（可能包含当前位置尚未看到的后文，**不是该位置输入**）：

```text
The authors argue that this reversal could allow such organisms to evade existing biological controls and immune defenses, potentially affecting humans, animals, plants, and broader ecosystems.
```
## natural:R11_A02_255:117


输入文档：R11_A02_255；领域：biology／microbiology_immunity；来源：[原始来源](http://sickmomma.blogspot.com/2010/01/its-official-gi-doc-says-its.html)。

**当前输入token：ID315，片段 `' of'`；0基位置t=117，即第118个token。可见输入共118个token。**

当前句子／段落已经可见的部分：

> In light of

全部可见输入（没有省略号；到当前token为止）：

```text
Avoid seeds like the plague!

Good luck, and I hope you have the speediest recovery possible. This is not what you need right now!

Yaya said...

I hope the new meds and diet work!!!

Just Jenn said...

He wants to use a pill cam to test for celiac?! While that test is good for sighting large abnormalities of the intestinal tract, such as ulcers and polyps, it does not diagnose celiac disease, gluten intolerance or other food sensitivities. Villi damage is microscopic which is why an upper intestinal tract biopsy is usually preformed.

In light of
```

在此预测下一个token。真实后继：ID429，片段 `' that'`。后继是语料参考，不等于原模型一定首选。


|0基位置|第几个token|ID|片段|是否已见|标记|

|---:|---:|---:|---|---|---|

|111|112|5990|`' usually'`|是||

|112|113|855|`' pre'`|是||

|113|114|10155|`'formed'`|是||

|114|115|382|`'.\n\n'`|是||

|115|116|641|`'In'`|是||

|116|117|3100|`' light'`|是||

|117|118|315|`' of'`|是|当前输入|

|118|119|429|`' that'`|否|真实后继|

|119|120|11|`','`|否||

|120|121|566|`' he'`|否||


|解码条件|前三候选：ID／片段／概率|真实后继概率|排名|NLL|与原模型KL|

|---|---|---:|---:|---:|---:|

|PC16–31（16维）|11 `','` 48.951%；320 `' ('` 10.922%；279 `' the'` 9.639%|0.79121%|11|4.8394|3.7726|

|PC32–63（32维）|320 `' ('` 24.687%；11 `','` 16.967%；220 `' '` 14.973%|1.78833%|9|4.0239|3.7940|

|PC64–127（64维）|11 `','` 18.314%；320 `' ('` 18.314%；198 `'\n'` 5.946%|4.63059%|5|3.0725|3.5769|

|PC128–255（128维）|220 `' '` 21.723%；11 `','` 19.170%；320 `' ('` 19.170%|4.84705%|5|3.0268|3.2996|

|PC256–511（256维）|320 `' ('` 24.065%；11 `','` 8.853%；279 `' the'` 6.895%|1.53839%|11|4.1744|3.2412|

|PC512–767（256维）|320 `' ('` 28.073%；11 `','` 17.027%；304 `' in'` 8.043%|0.51417%|18|5.2704|3.8701|

|PC768–959（192维）|11 `','` 23.476%；320 `' ('` 20.718%；220 `' '` 16.135%|0.26080%|26|5.9492|4.1709|

|PC960–1024（65维）|11 `','` 17.346%；320 `' ('` 17.346%；304 `' in'` 10.521%|0.86360%|14|4.7518|3.8457|

|PC512–575（64维）|320 `' ('` 23.580%；11 `','` 14.302%；304 `' in'` 12.622%|0.55456%|17|5.1948|4.1757|

|PC768–831（64维）|320 `' ('` 28.371%；11 `','` 19.499%；220 `' '` 8.129%|0.40470%|24|5.5098|4.1260|

|PC961–1024（64维）|11 `','` 17.296%；320 `' ('` 17.296%；304 `' in'` 10.490%|0.97575%|14|4.6297|3.8004|

|仅训练均值|320 `' ('` 21.452%；11 `','` 18.931%；220 `' '` 8.942%|0.57167%|17|5.1644|4.2135|

|原模型|419 `' this'` 29.064%；279 `' the'` 22.635%；429 `' that'` 9.436%|9.43578%|3|2.3607|0.0000|


原文参考整句（可能包含当前位置尚未看到的后文，**不是该位置输入**）：

```text
In light of that, he needs to run a Tissue Transglutaminase Antibody test which looks for the antibodies to the enzyme that a celiacs immune system is attacking when gluten is ingested.
```
## natural:R11_A02_281:110


输入文档：R11_A02_281；领域：biology／microbiology_immunity；来源：[原始来源](https://www.scientificamerican.com/article/you-are-probably-washing-your-hands-wrong/)。

**当前输入token：ID382，片段 `'.\n\n'`；0基位置t=110，即第111个token。可见输入共111个token。**

当前句子／段落已经可见的部分：

> There are two main strategies.
> 
> 

全部可见输入（没有省略号；到当前token为止）：

```text
This question is difficult to answer. You can’t tell by eye which bacteria growing within a petri dish are the “good guys” versus ones that cause disease, and some pathogenic microbes, like viruses, can’t be detected within agar petri dishes.

Nevertheless, with the upcoming holiday travels, asking how to prevent the spread of disease-causing pathogens isn’t just for aspiring microbiologists but a great question for everyone.

Do we really stand a chance of keeping our hands clean from germs?

Two-fisted approach

There are two main strategies.


```

在此预测下一个token。真实后继：ID785，片段 `'The'`。后继是语料参考，不等于原模型一定首选。


|0基位置|第几个token|ID|片段|是否已见|标记|

|---:|---:|---:|---|---|---|

|104|105|271|`'\n\n'`|是||

|105|106|3862|`'There'`|是||

|106|107|525|`' are'`|是||

|107|108|1378|`' two'`|是||

|108|109|1887|`' main'`|是||

|109|110|14830|`' strategies'`|是||

|110|111|382|`'.\n\n'`|是|当前输入|

|111|112|785|`'The'`|否|真实后继|

|112|113|1156|`' first'`|否||

|113|114|374|`' is'`|否||


|解码条件|前三候选：ID／片段／概率|真实后继概率|排名|NLL|与原模型KL|

|---|---|---:|---:|---:|---:|

|PC16–31（16维）|11 `','` 55.300%；320 `' ('` 10.889%；279 `' the'` 5.144%|0.00773%|154|9.4674|8.1007|

|PC32–63（32维）|320 `' ('` 24.823%；11 `','` 11.726%；220 `' '` 10.348%|0.00326%|478|10.3309|8.3547|

|PC64–127（64维）|220 `' '` 25.110%；320 `' ('` 19.555%；11 `','` 11.861%|0.00241%|507|10.6319|8.3308|

|PC128–255（128维）|220 `' '` 77.424%；323 `' and'` 3.855%；320 `' ('` 2.063%|0.00138%|414|11.1934|8.5908|

|PC256–511（256维）|220 `' '` 35.957%；320 `' ('` 35.957%；279 `' the'` 4.866%|0.00535%|177|9.8353|7.4654|

|PC512–767（256维）|220 `' '` 24.498%；320 `' ('` 16.837%；11 `','` 10.212%|0.00162%|851|11.0316|7.9067|

|PC768–959（192维）|320 `' ('` 28.615%；11 `','` 13.517%；264 `' a'` 7.235%|0.00122%|875|11.3137|8.9772|

|PC960–1024（65维）|320 `' ('` 24.026%；11 `','` 16.513%；220 `' '` 11.349%|6.62e-04%|713|11.9260|9.4262|

|PC512–575（64维）|320 `' ('` 21.856%；11 `','` 15.021%；220 `' '` 13.256%|0.00164%|659|11.0207|8.6369|

|PC768–831（64维）|320 `' ('` 26.220%；11 `','` 15.903%；323 `' and'` 8.512%|6.37e-04%|1224|11.9637|9.3520|

|PC961–1024（64维）|320 `' ('` 24.368%；11 `','` 16.748%；220 `' '` 10.158%|6.71e-04%|714|11.9119|9.4434|

|仅训练均值|320 `' ('` 21.452%；11 `','` 18.931%；220 `' '` 8.942%|0.00104%|748|11.4769|9.1796|

|原模型|785 `'The'` 26.704%；220 `' '` 16.197%；5338 `'First'` 14.294%|26.70412%|1|1.3204|0.0000|


原文参考整句（可能包含当前位置尚未看到的后文，**不是该位置输入**）：

```text
There are two main strategies.

The first is to decrease the overall biomass of microbes – that is, decrease the amount of bacteria, viruses and other types of microorganisms.
```
## natural:R11_A02_285:134


输入文档：R11_A02_285；领域：biology／organismal；来源：[原始来源](http://en.wikipedia.org/wiki/Prothallium)。

**当前输入token：ID1075，片段 `' like'`；0基位置t=134，即第135个token。可见输入共135个token。**

当前句子／段落已经可见的部分：

> Spore-bearing plants, like

全部可见输入（没有省略号；到当前token为止）：

```text
The prothallium develops from a germinating spore. It is a short-lived and inconspicuous heart-shaped structure typically 2-5 millimeters wide, with a number of rhizoids (root-like hairs) growing underneath, and the sex organs: archegonium (female) and antheridium (male). Appearance varies quite a lot between species. Some are green and conduct photosynthesis while others are colorless and nourish themselves underground as saprotrophs.

Alternation of generations[edit]

Prothallus of the tree fern Dicksonia antarctica (note new moss plants for scale)

Spore-bearing plants, like
```

在此预测下一个token。真实后继：ID678，片段 `' all'`。后继是语料参考，不等于原模型一定首选。


|0基位置|第几个token|ID|片段|是否已见|标记|

|---:|---:|---:|---|---|---|

|128|129|692|`')\n\n'`|是||

|129|130|6406|`'Sp'`|是||

|130|131|460|`'ore'`|是||

|131|132|91153|`'-bearing'`|是||

|132|133|10779|`' plants'`|是||

|133|134|11|`','`|是||

|134|135|1075|`' like'`|是|当前输入|

|135|136|678|`' all'`|否|真实后继|

|136|137|10779|`' plants'`|否||

|137|138|11|`','`|否||


|解码条件|前三候选：ID／片段／概率|真实后继概率|排名|NLL|与原模型KL|

|---|---|---:|---:|---:|---:|

|PC16–31（16维）|11 `','` 85.604%；279 `' the'` 5.472%；264 `' a'` 2.013%|0.04178%|29|7.7804|9.4878|

|PC32–63（32维）|279 `' the'` 17.608%；323 `' and'` 17.608%；11 `','` 13.713%|0.87665%|14|4.7368|7.3109|

|PC64–127（64维）|11 `','` 17.781%；304 `' in'` 17.781%；320 `' ('` 15.691%|0.47384%|20|5.3521|7.4752|

|PC128–255（128维）|320 `' ('` 16.536%；220 `' '` 14.593%；11 `','` 10.029%|1.19784%|13|4.4246|6.8462|

|PC256–511（256维）|11 `','` 14.957%；320 `' ('` 14.957%；304 `' in'` 11.648%|0.65714%|20|5.0250|7.9675|

|PC512–767（256维）|11 `','` 17.777%；320 `' ('` 15.688%；304 `' in'` 13.845%|0.32560%|22|5.7273|8.1905|

|PC768–959（192维）|11 `','` 18.229%；320 `' ('` 12.528%；304 `' in'` 9.757%|0.62375%|22|5.0772|8.3604|

|PC960–1024（65维）|11 `','` 19.644%；320 `' ('` 15.299%；304 `' in'` 11.915%|0.21823%|31|6.1274|8.7835|

|PC512–575（64维）|320 `' ('` 18.776%；11 `','` 16.570%；304 `' in'` 11.388%|0.16245%|30|6.4226|8.6128|

|PC768–831（64维）|320 `' ('` 29.120%；11 `','` 17.662%；220 `' '` 7.363%|0.25194%|24|5.9837|8.9496|

|PC961–1024（64维）|11 `','` 19.356%；320 `' ('` 15.074%；304 `' in'` 11.740%|0.21502%|31|6.1422|8.7973|

|仅训练均值|320 `' ('` 21.452%；11 `','` 18.931%；220 `' '` 8.942%|0.14454%|32|6.5394|9.0202|

|原模型|77243 `' moss'` 24.861%；678 `' all'` 19.361%；87024 `' fern'` 15.079%|19.36139%|2|1.6419|0.0000|


原文参考整句（可能包含当前位置尚未看到的后文，**不是该位置输入**）：

```text
Spore-bearing plants, like all plants, go through a life-cycle of alternation of generations.
```
## natural:R11_A02_410:109


输入文档：R11_A02_410；领域：physics／quantum；来源：[原始来源](http://www.science20.com/news_articles/mathematicians_pull_invisible_matter_rabbit_out_schr%C3%B6dingers_hat-90566)。

**当前输入token：ID279，片段 `' the'`；0基位置t=109，即第110个token。可见输入共110个token。**

当前句子／段落已经可见的部分：

> The researchers envision building a quantum microscope that could capture quantum waves, the

全部可见输入（没有省略号；到当前token为止）：

```text
You've read a lot about 'invisibility' over the last few years.  Mathematicians and scientists have been working on various devices that enable invisibility cloaks which shield small objects from detection by microwaves or sound waves.

An international team has devised an amplifier that can boost light, sound or other waves while hiding them inside an invisible container. As a first application, the researchers propose manipulating matter waves, which are the mathematical description of particles in quantum mechanics. The researchers envision building a quantum microscope that could capture quantum waves, the
```

在此预测下一个token。真实后继：ID16876，片段 `' waves'`。后继是语料参考，不等于原模型一定首选。


|0基位置|第几个token|ID|片段|是否已见|标记|

|---:|---:|---:|---|---|---|

|103|104|429|`' that'`|是||

|104|105|1410|`' could'`|是||

|105|106|12322|`' capture'`|是||

|106|107|30128|`' quantum'`|是||

|107|108|16876|`' waves'`|是||

|108|109|11|`','`|是||

|109|110|279|`' the'`|是|当前输入|

|110|111|16876|`' waves'`|否|真实后继|

|111|112|315|`' of'`|否||

|112|113|279|`' the'`|否||


|解码条件|前三候选：ID／片段／概率|真实后继概率|排名|NLL|与原模型KL|

|---|---|---:|---:|---:|---:|

|PC16–31（16维）|304 `' in'` 19.964%；320 `' ('` 17.618%；220 `' '` 8.322%|1.39e-04%|5670|13.4863|5.1843|

|PC32–63（32维）|220 `' '` 15.984%；304 `' in'` 14.106%；11 `','` 12.448%|2.81e-05%|10269|15.0836|5.3390|

|PC64–127（64维）|220 `' '` 16.830%；304 `' in'` 14.852%；279 `' the'` 7.016%|1.70e-04%|4431|13.2820|5.0608|

|PC128–255（128维）|11 `','` 30.651%；323 `' and'` 16.406%；320 `' ('` 14.478%|4.47e-05%|5540|14.6200|6.0617|

|PC256–511（256维）|11 `','` 22.975%；320 `' ('` 22.975%；264 `' a'` 9.577%|5.53e-05%|5366|14.4083|5.8645|

|PC512–767（256维）|320 `' ('` 21.451%；220 `' '` 18.931%；11 `','` 14.743%|3.33e-05%|4894|14.9144|6.8423|

|PC768–959（192维）|11 `','` 17.842%；320 `' ('` 15.746%；304 `' in'` 10.822%|3.56e-05%|6406|14.8486|6.3885|

|PC960–1024（65维）|320 `' ('` 15.116%；11 `','` 13.340%；304 `' in'` 10.389%|8.20e-05%|5184|14.0144|6.2255|

|PC512–575（64维）|320 `' ('` 24.930%；11 `','` 19.415%；220 `' '` 11.776%|3.64e-05%|5207|14.8266|6.9217|

|PC768–831（64维）|11 `','` 21.050%；320 `' ('` 14.468%；304 `' in'` 11.267%|2.89e-05%|7285|15.0582|6.6169|

|PC961–1024（64维）|11 `','` 14.755%；320 `' ('` 14.755%；304 `' in'` 10.141%|7.52e-05%|5338|14.1011|6.2531|

|仅训练均值|320 `' ('` 21.452%；11 `','` 18.931%；220 `' '` 8.942%|1.31e-05%|9225|15.8519|6.9526|

|原模型|24632 `' smallest'` 6.942%；11811 `' researchers'` 4.771%；4752 `' building'` 4.210%|0.93943%|18|4.6676|0.0000|


原文参考整句（可能包含当前位置尚未看到的后文，**不是该位置输入**）：

```text
The researchers envision building a quantum microscope that could capture quantum waves, the waves of the nano-world.
```
## natural:R11_A02_419:64


输入文档：R11_A02_419；领域：physics／waves_optics；来源：[原始来源](https://byjus.com/physics/refraction-of-light/)。

**当前输入token：ID624，片段 `'.\n'`；0基位置t=64，即第65个token。可见输入共65个token。**

当前句子／段落已经可见的部分：

> In this article, let us briefly understand the process of refraction.
> 

全部可见输入（没有省略号；到当前token为止）：

```text
We know that light is a form of energy and can undergo various phenomena like diffraction, reflection, refraction, interference, and polarisation. Refraction is the phenomenon that takes place due to the bending of light when it travels from medium to another. In this article, let us briefly understand the process of refraction.

```

在此预测下一个token。真实后继：ID3838，片段 `'What'`。后继是语料参考，不等于原模型一定首选。


|0基位置|第几个token|ID|片段|是否已见|标记|

|---:|---:|---:|---|---|---|

|58|59|3535|`' understand'`|是||

|59|60|279|`' the'`|是||

|60|61|1882|`' process'`|是||

|61|62|315|`' of'`|是||

|62|63|2053|`' ref'`|是||

|63|64|16199|`'raction'`|是||

|64|65|624|`'.\n'`|是|当前输入|

|65|66|3838|`'What'`|否|真实后继|

|66|67|2160|`' Is'`|否||

|67|68|8550|`' Ref'`|否||


|解码条件|前三候选：ID／片段／概率|真实后继概率|排名|NLL|与原模型KL|

|---|---|---:|---:|---:|---:|

|PC16–31（16维）|11 `','` 44.682%；279 `' the'` 12.802%；320 `' ('` 9.970%|7.01e-04%|585|11.8681|9.9637|

|PC32–63（32维）|11 `','` 48.582%；304 `' in'` 8.442%；320 `' ('` 7.450%|5.88e-05%|4342|14.3469|10.9962|

|PC64–127（64维）|220 `' '` 17.136%；11 `','` 13.345%；304 `' in'` 9.172%|1.35e-04%|3373|13.5140|10.9471|

|PC128–255（128维）|304 `' in'` 20.389%；11 `','` 12.367%；323 `' and'` 7.501%|1.25e-04%|3965|13.5902|10.3446|

|PC256–511（256维）|320 `' ('` 26.506%；11 `','` 11.050%；323 `' and'` 7.594%|4.16e-04%|2595|12.3903|9.2893|

|PC512–767（256维）|11 `','` 32.802%；304 `' in'` 17.558%；323 `' and'` 9.398%|2.15e-04%|2283|13.0522|10.4479|

|PC768–959（192维）|320 `' ('` 25.360%；11 `','` 17.429%；279 `' the'` 6.412%|3.51e-04%|1990|12.5595|10.2360|

|PC960–1024（65维）|320 `' ('` 26.902%；11 `','` 20.951%；220 `' '` 11.214%|2.53e-05%|4309|15.1880|11.9417|

|PC512–575（64维）|11 `','` 22.861%；320 `' ('` 15.712%；304 `' in'` 12.236%|6.23e-05%|4622|14.2883|11.2402|

|PC768–831（64维）|320 `' ('` 26.115%；11 `','` 15.839%；304 `' in'` 7.482%|4.60e-05%|5743|14.5927|11.1980|

|PC961–1024（64维）|320 `' ('` 25.468%；11 `','` 22.476%；220 `' '` 10.617%|2.55e-05%|4438|15.1802|11.9165|

|仅训练均值|320 `' ('` 21.452%；11 `','` 18.931%；220 `' '` 8.942%|4.28e-05%|5207|14.6644|11.5316|

|原模型|3838 `'What'` 20.835%；785 `'The'` 11.152%；3945 `'Ref'` 11.152%|20.83542%|1|1.5685|0.0000|


原文参考整句（可能包含当前位置尚未看到的后文，**不是该位置输入**）：

```text
In this article, let us briefly understand the process of refraction.
What Is Refraction?
```
## natural:R11_A02_422:151


输入文档：R11_A02_422；领域：physics／materials_solid；来源：[原始来源](https://phys.org/news/2018-03-mystery-superconducting-dome.html)。

**当前输入token：ID3410，片段 `' provide'`；0基位置t=151，即第152个token。可见输入共152个token。**

当前句子／段落已经可见的部分：

> Their results show the typical dome-shaped superconducting phase, and finally provide

全部可见输入（没有省略号；到当前token为止）：

```text
Shedding light on the mystery of the superconducting dome

Shedding light on the mystery of the superconducting dome
Prof. dr. Justin Ye, Zernike Insititute of Advanced Materials, Faculty of Science and Engineering, University of Groningen Credit: ZIAM/University of Groningen

University of Groningen physicists, and colleagues from Nijmegen and Hong Kong, have induced superconductivity in a monolayer of tungsten disulfide. By using an increasing electric field, they were able to show how the material turns from an insulator into a superconductor and then back into a re-entrant insulator again. Their results show the typical dome-shaped superconducting phase, and finally provide
```

在此预测下一个token。真实后继：ID458，片段 `' an'`。后继是语料参考，不等于原模型一定首选。


|0基位置|第几个token|ID|片段|是否已见|标记|

|---:|---:|---:|---|---|---|

|145|146|76652|`'conduct'`|是||

|146|147|287|`'ing'`|是||

|147|148|10262|`' phase'`|是||

|148|149|11|`','`|是||

|149|150|323|`' and'`|是||

|150|151|5499|`' finally'`|是||

|151|152|3410|`' provide'`|是|当前输入|

|152|153|458|`' an'`|否|真实后继|

|153|154|16148|`' explanation'`|否||

|154|155|369|`' for'`|否||


|解码条件|前三候选：ID／片段／概率|真实后继概率|排名|NLL|与原模型KL|

|---|---|---:|---:|---:|---:|

|PC16–31（16维）|11 `','` 31.244%；220 `' '` 10.143%；264 `' a'` 7.900%|1.21144%|12|4.4134|3.5996|

|PC32–63（32维）|11 `','` 43.526%；320 `' ('` 16.012%；220 `' '` 6.675%|0.33232%|19|5.7068|3.8865|

|PC64–127（64维）|264 `' a'` 23.951%；323 `' and'` 16.461%；304 `' in'` 11.314%|1.53112%|9|4.1792|2.8845|

|PC128–255（128维）|320 `' ('` 21.891%；304 `' in'` 17.049%；11 `','` 9.126%|1.23503%|14|4.3941|3.1481|

|PC256–511（256维）|11 `','` 26.698%；320 `' ('` 23.561%；369 `' for'` 14.290%|1.03519%|9|4.5706|3.3946|

|PC512–767（256维）|11 `','` 27.211%；220 `' '` 11.343%；304 `' in'` 7.796%|0.38814%|23|5.5516|4.2098|

|PC768–959（192维）|320 `' ('` 14.666%；11 `','` 12.942%；304 `' in'` 11.422%|0.44286%|25|5.4197|4.0920|

|PC960–1024（65维）|320 `' ('` 29.005%；11 `','` 15.525%；220 `' '` 13.701%|0.28435%|21|5.8627|4.7900|

|PC512–575（64维）|11 `','` 20.619%；320 `' ('` 20.619%；220 `' '` 7.585%|0.48492%|20|5.3289|4.0510|

|PC768–831（64维）|320 `' ('` 15.363%；11 `','` 13.558%；304 `' in'` 13.558%|0.52569%|21|5.2482|4.1048|

|PC961–1024（64维）|320 `' ('` 26.685%；11 `','` 16.185%；220 `' '` 14.283%|0.29644%|21|5.8211|4.7458|

|仅训练均值|320 `' ('` 21.452%；11 `','` 18.931%；220 `' '` 8.942%|0.44522%|20|5.4144|4.3705|

|原模型|264 `' a'` 35.057%；279 `' the'` 12.897%；458 `' an'` 8.864%|8.86368%|3|2.4232|0.0000|


原文参考整句（可能包含当前位置尚未看到的后文，**不是该位置输入**）：

```text
Their results show the typical dome-shaped superconducting phase, and finally provide an explanation for this phenomenon.
```
## natural:R11_A02_434:160


输入文档：R11_A02_434；领域：physics／waves_optics；来源：[原始来源](http://en.wikipedia.org/wiki/X-ray_optics)。

**当前输入token：ID279，片段 `' the'`；0基位置t=160，即第161个token。可见输入共161个token。**

当前句子／段落已经可见的部分：

> X-rays produce a diffraction pattern because their wavelength is typically the

全部可见输入（没有省略号；到当前token为止）：

```text
The ratio of reflected intensity to incident intensity is the X-ray reflectivity for the surface. If the interface is not perfectly sharp and smooth, the reflected intensity will deviate from that predicted by the law of Fresnel reflectivity. The deviations can then be analyzed to obtain the density profile of the interface normal to the surface. For films with multiple layers, X-ray reflectivity may show oscillations with wavelength, analogous to the Fabry-Pérot effect. These oscillations can be used to infer layer thicknesses and other properties.



In X-ray diffraction a beam strikes a crystal and diffracts into many specific directions. The angles and intensities of the diffracted beams indicate a three-dimensional density of electrons within the crystal. X-rays produce a diffraction pattern because their wavelength is typically the
```

在此预测下一个token。真实后继：ID1852，片段 `' same'`。后继是语料参考，不等于原模型一定首选。


|0基位置|第几个token|ID|片段|是否已见|标记|

|---:|---:|---:|---|---|---|

|154|155|5383|`' pattern'`|是||

|155|156|1576|`' because'`|是||

|156|157|862|`' their'`|是||

|157|158|45306|`' wavelength'`|是||

|158|159|374|`' is'`|是||

|159|160|11136|`' typically'`|是||

|160|161|279|`' the'`|是|当前输入|

|161|162|1852|`' same'`|否|真实后继|

|162|163|1973|`' order'`|否||

|163|164|315|`' of'`|否||


|解码条件|前三候选：ID／片段／概率|真实后继概率|排名|NLL|与原模型KL|

|---|---|---:|---:|---:|---:|

|PC16–31（16维）|220 `' '` 18.166%；304 `' in'` 14.148%；320 `' ('` 14.148%|0.01290%|200|8.9556|8.0590|

|PC32–63（32维）|11 `','` 23.727%；320 `' ('` 20.939%；304 `' in'` 14.391%|0.00293%|478|10.4386|9.1858|

|PC64–127（64维）|320 `' ('` 23.089%；220 `' '` 14.004%；279 `' the'` 8.494%|0.00995%|235|9.2158|8.3576|

|PC128–255（128维）|320 `' ('` 24.661%；11 `','` 21.763%；323 `' and'` 13.200%|0.00534%|317|9.8374|8.5464|

|PC256–511（256维）|11 `','` 28.121%；320 `' ('` 19.327%；279 `' the'` 10.345%|0.05100%|77|7.5812|6.8966|

|PC512–767（256维）|11 `','` 18.563%；320 `' ('` 14.457%；220 `' '` 8.769%|0.01590%|194|8.7465|7.7904|

|PC768–959（192维）|11 `','` 15.820%；304 `' in'` 12.320%；320 `' ('` 9.595%|0.01055%|308|9.1564|8.2934|

|PC960–1024（65维）|320 `' ('` 29.210%；11 `','` 12.176%；220 `' '` 9.483%|0.00248%|453|10.6057|9.6184|

|PC512–575（64维）|320 `' ('` 20.135%；11 `','` 17.769%；220 `' '` 10.777%|0.00362%|408|10.2277|9.2797|

|PC768–831（64维）|11 `','` 23.036%；320 `' ('` 13.972%；304 `' in'` 9.603%|0.00389%|440|10.1556|9.1442|

|PC961–1024（64维）|320 `' ('` 29.753%；11 `','` 10.946%；220 `' '` 9.659%|0.00252%|450|10.5872|9.6005|

|仅训练均值|320 `' ('` 21.452%；11 `','` 18.931%；220 `' '` 8.942%|0.00151%|590|11.1019|10.0468|

|原模型|1852 `' same'` 70.043%；1973 `' order'` 7.382%；24632 `' smallest'` 7.382%|70.04251%|1|0.3561|0.0000|


原文参考整句（可能包含当前位置尚未看到的后文，**不是该位置输入**）：

```text
X-rays produce a diffraction pattern because their wavelength is typically the same order of magnitude (0.1-10.0 nm) as the spacing between the atomic planes in the crystal.
```

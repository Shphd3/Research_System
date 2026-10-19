# G014：同一预测位置的输入与激活

类别是选择方法，不是语义标签。随机6例来自固定V面板命中位置的哈希抽样；高K6例按激活成员数选取，不代表随机命中；另取K=1三例。各例均保留完整组激活值，未激活成员为0，可回查完整矩阵。下文前缀摘录只展示末320字符，完整前缀文件从当前context起点到位置t，**包含当前token，不包含预测目标t+1**。context起点不保证原文档起点，原文档ID未知。

## p346907 · 随机命中

当前token：``' favorable'``；token ID=36749；context=338；序列位置t=1017（零起始）；原block=2。K全组=21，K展示=9。

~~~text
s first look at our upstream business, which is Alumina segment and the Primary segment, the quarter was marked by planned maintenance overhauls and power plant outages amidst the declining metal price. The businesses partially overcame these headwinds with continued productivity, higher regional premiums and favorable
~~~

[完整可见前缀](../prefixes/G014_p346907.txt)；原bin绝对token偏移=347129。

同位置激活成员与z：124:0.02565044, 1247:0.02255211, 2404:0.02375231, 2676:0.04425277, 3168:0.01713577, 3648:0.01444354, 4234:0.01846644, 4417:0.01146167, 9374:0.01130953, 9881:0.0780596, 9953:0.01506995, 10513:0.01113525, 10583:0.01587453, 10750:0.05956366, 11558:0.02240441, 11709:0.04254337, 12849:0.01194963, 13730:0.02876964, 14720:0.01564064, 15881:0.03033838, 16323:0.01222072。

## p7928942 · 随机命中

当前token：``'1'``；token ID=16；context=7749；序列位置t=805（零起始）；原block=60。K全组=21，K展示=8。

~~~text
A mutant) in human serum and whole blood and measured complement activation and cytokine secretion and the effect of blocking these systems. HEK293 cells transfected with Toll-like receptors (TLRs) were examined for activation of NF-kappaB. The threshold for cytokine secretion and activation of NF-kappaB was 10(3) to 1
~~~

[完整可见前缀](../prefixes/G014_p7928942.txt)；原bin绝对token偏移=7935781。

同位置激活成员与z：124:0.005730091, 225:0.0130922, 1493:0.02139236, 2454:0.07297686, 3487:0.0137236, 4904:0.01739164, 5014:0.01918555, 5064:0.02335364, 6157:0.01359896, 8270:0.04664024, 8485:0.009929011, 9409:0.03481939, 9953:0.01348303, 11995:0.03037526, 12179:0.02690549, 12849:0.01304826, 13730:0.01509776, 13962:0.01462478, 14001:0.008872259, 16323:0.01417384, 16338:0.03268313。

## p7719121 · 随机命中

当前token：``'ol'``；token ID=337；context=7544；序列位置t=741（零起始）；原block=58。K全组=2，K展示=2。

~~~text
paleo-conservatives/Constitutionalists, then somewhere between Randpocalpyse/Mutt WRONGney-endorsement and Gary Johnson came the Jack Hunter/Austin Petersen/Rand Paul-Republicans pitting themselves against...well, what seemed like everyone else, here! LOL.

Then, a whole new breed of newbies wanting to purge AnCaps/vol
~~~

[完整可见前缀](../prefixes/G014_p7719121.txt)；原bin绝对token偏移=7725797。

同位置激活成员与z：4964:0.0219397, 16323:0.01612697。

## p2224851 · 随机命中

当前token：``"'s"``；token ID=594；context=2174；序列位置t=429（零起始）；原block=16。K全组=15，K展示=8。

~~~text
MS is completely willing to drop a platform that turns out to be more trouble than it's worth. We'll see.

Comment: Re:The Wealthy? (Score 1) 202

by drinkypoo (#45732063) Attached to: Tesla Gets $34 Million Tax Break, Adds Capacity For 35,000 More Cars

How cute. People actually needing their truck for the job. That's
~~~

[完整可见前缀](../prefixes/G014_p2224851.txt)；原bin绝对token偏移=2226605。

同位置激活成员与z：1936:0.01182018, 3810:0.01025935, 3817:0.03534713, 4234:0.01810023, 5800:0.02071331, 5958:0.01148249, 8180:0.01118188, 8270:0.0295504, 9374:0.0159482, 9953:0.008722291, 10985:0.007775692, 11871:0.01016939, 12811:0.01068501, 14720:0.01979103, 15097:0.01089307。

## p4582888 · 随机命中

当前token：``' again'``；token ID=1549；context=4479；序列位置t=273（零起始）；原block=34。K全组=8，K展示=5。

~~~text
 can be fully discharged and recharged. Eventually their ability to store and deliver electrical energy is degraded to a point where they become more or less useless. Note that this means one complete charge cycle, so if you use half your battery’s capacity, then charge it up, then use half again and charge it up again
~~~

[完整可见前缀](../prefixes/G014_p4582888.txt)；原bin绝对token偏移=4586769。

同位置激活成员与z：3129:0.02800694, 3168:0.02348343, 5800:0.03682659, 8270:0.01243003, 9409:0.01199225, 9604:0.01312007, 12179:0.01201292, 15992:0.01699694。

## p9285236 · 随机命中

当前token：``' holy'``；token ID=26725；context=9075；序列位置t=430（零起始）；原block=70。K全组=10，K展示=2。

~~~text
d on the altar of the Christian religion.

The Calvinist, who damns children of a span long to hell to burn forever for the glory of God (and this is called Christianity), and the Universalist who preaches that all shall be saved and none shall be damned (and this also is called Christianity), boast alike of their holy
~~~

[完整可见前缀](../prefixes/G014_p9285236.txt)；原bin绝对token偏移=9293230。

同位置激活成员与z：2299:0.01725468, 7178:0.03658146, 9559:0.01598199, 10513:0.0117456, 10902:0.01588374, 12179:0.008778052, 13684:0.02024962, 14865:0.01651542, 15897:0.01689995, 16323:0.01820216。

## p9073076 · 高K

当前token：``' by'``；token ID=553；context=8868；序列位置t=59（零起始）；原block=69。K全组=42，K展示=11。

~~~text
H-Z370 Unlocked Triband Camera Phone (Black) (Out of Stock)

The Man In The Audience

Staff Writer
How do you measure intellectual influence? Richard Posner, author of the hotly debated new book “Public Intellectuals,” rates 546 public intellectuals by
~~~

[完整可见前缀](../prefixes/G014_p9073076.txt)；原bin绝对token偏移=9080891。

同位置激活成员与z：119:0.0167691, 124:0.01625103, 1451:0.02185664, 1639:0.03079445, 1939:0.01708439, 2299:0.03495488, 2361:0.01087595, 2841:0.04897108, 3168:0.01243607, 3324:0.02503618, 3406:0.02252342, 3423:0.02259023, 3487:0.01274704, 3562:0.01551264, 4275:0.03916955, 4417:0.01903003, 4824:0.06594727, 5800:0.04195355, 7178:0.01924747, 7496:0.02110054, 7532:0.04772361, 8270:0.02271446, 9409:0.01284674, 9881:0.01726859, 10016:0.01372161, 10182:0.02079215, 10436:0.01893434, 10583:0.01990285, 10615:0.01916165, 10861:0.0233868, 10985:0.07018939, 11558:0.02362512, 11579:0.01929823, 11709:0.05841251, 11941:0.04702898, 12695:0.04629397, 12849:0.01469621, 13383:0.03728794, 13894:0.02555553, 14791:0.01044323, 15749:0.01434693, 16323:0.06910548。

## p10392874 · 高K

当前token：``' by'``；token ID=553；context=10158；序列位置t=15（零起始）；原block=79。K全组=40，K展示=14。

~~~text
 do you use the mode, the mean, or the entire distribution, weighted by
~~~

[完整可见前缀](../prefixes/G014_p10392874.txt)；原bin绝对token偏移=10401807。

同位置激活成员与z：124:0.02467388, 890:0.01393807, 1451:0.0384582, 1936:0.0156654, 2299:0.03300175, 2361:0.02723337, 3324:0.02430376, 3423:0.02771719, 3487:0.0149443, 3562:0.01600092, 4234:0.01529261, 4417:0.03001636, 4824:0.07961915, 4964:0.009427497, 5218:0.01259972, 5800:0.02767132, 7457:0.01282721, 7532:0.03478416, 8270:0.02527793, 8795:0.06591926, 9409:0.02554205, 9881:0.02312796, 10436:0.01344118, 10513:0.02358642, 10583:0.01404348, 10985:0.01351824, 11032:0.03871439, 11033:0.01300036, 11558:0.01666711, 11709:0.04205509, 12695:0.05410647, 12849:0.02867327, 13824:0.02329719, 14641:0.03205806, 14833:0.0309719, 14847:0.03473349, 15376:0.01385751, 15464:0.0301582, 16215:0.02567313, 16323:0.03394923。

## p5268443 · 高K

当前token：``' around'``；token ID=2163；context=5149；序列位置t=376（零起始）；原block=40。K全组=39，K展示=6。

~~~text
m the SEC.

2008? Four of the top 11.

2009? Six of the top 12.

2010? Five of the top nine.

2011? Six of the top 13.

2012? More of the same.

Now want to feel really old? The kids who are in the class of 2013 were mostly born in 1996 and 1997. By and large kids start to pay some attention to college athletics around
~~~

[完整可见前缀](../prefixes/G014_p5268443.txt)；原bin绝对token偏移=5272952。

同位置激活成员与z：257:0.01955945, 853:0.02413041, 1128:0.01023847, 1451:0.04456171, 1602:0.01332127, 2361:0.01661325, 2889:0.01161421, 3129:0.01067295, 3168:0.03031937, 3308:0.03083615, 3487:0.01433395, 3562:0.01917475, 3762:0.02931318, 4264:0.01250677, 4824:0.03420899, 4904:0.0159268, 5800:0.06490276, 6885:0.02214647, 7532:0.01622947, 8135:0.02258582, 8270:0.01563438, 9095:0.02377561, 9168:0.03979327, 9881:0.01873343, 9989:0.02204866, 10607:0.04570913, 10615:0.02770657, 11017:0.0698342, 11995:0.02476003, 12652:0.02597041, 13383:0.01702426, 14720:0.01405372, 14791:0.02667858, 14833:0.02926291, 14954:0.03058549, 15097:0.01418897, 15405:0.2710964, 15926:0.03987348, 15954:0.02935711。

## p3187607 · 高K

当前token：``' on'``；token ID=389；context=3115；序列位置t=456（零起始）；原block=24。K全组=39，K展示=9。

~~~text
cup' for?"

"Why," replied the fish monger, "I didn't want you to forget scup when I got scup!"<|im_end|>FCW forum | Management 2.0

Forman: Political appointees must be ready to lead

Political appointees have to gain traction quickly to be change agents

Many political appointees find that success or failure rides on
~~~

[完整可见前缀](../prefixes/G014_p3187607.txt)；原bin绝对token偏移=3190216。

同位置激活成员与z：124:0.02125591, 920:0.04185684, 1247:0.01815758, 1316:0.02600076, 1451:0.02014765, 1602:0.01332127, 1639:0.01260597, 1936:0.02286755, 1939:0.02062443, 2299:0.02250371, 2676:0.02203597, 2841:0.0328578, 3168:0.05473343, 3406:0.04120018, 3762:0.01979169, 3810:0.01221247, 4824:0.01797364, 5218:0.02627159, 7457:0.06287604, 7496:0.01402046, 7532:0.09362205, 7990:0.01189088, 9192:0.03449962, 9267:0.01353506, 9953:0.009576784, 10394:0.01498998, 10513:0.01931396, 10861:0.0377911, 10985:0.05676165, 12695:0.01968264, 12849:0.07420549, 13277:0.01626398, 13894:0.06925671, 14631:0.01178824, 14865:0.01798026, 14992:0.01876924, 15376:0.01751962, 15897:0.018731, 16202:0.01256842。

## p4603003 · 高K

当前token：``' at'``；token ID=518；context=4498；序列位置t=935（零起始）；原block=35。K全组=38，K展示=8。

~~~text
r businesses have been hit in the recession, we haven't experienced that yet. This year will be one of those challenges. We continue with increases in pay but may be more limited in what we have been able to do in the past. As Mary said, we also participate in the Milwaukee Journal Top 100 Workplace Surveys. We look at
~~~

[完整可见前缀](../prefixes/G014_p4603003.txt)；原bin绝对token偏移=4606887。

同位置激活成员与z：81:0.009671789, 124:0.02247661, 890:0.02883065, 1602:0.02015721, 1936:0.02628552, 2196:0.01580224, 2299:0.02152714, 2350:0.04132825, 2404:0.01301012, 2841:0.04945936, 3168:0.01329056, 3308:0.04401975, 3459:0.02201732, 3648:0.0195705, 4275:0.01377893, 4582:0.01021281, 4824:0.01138184, 5218:0.02456261, 5800:0.03902386, 5958:0.0159991, 7496:0.01328804, 7532:0.02794822, 8795:0.01342902, 9559:0.01537164, 9881:0.03387015, 10695:0.03710425, 10861:0.0122784, 11558:0.04779504, 11579:0.02869765, 11709:0.05108829, 12631:0.01318041, 13224:0.2212778, 13730:0.02657237, 13962:0.0141365, 14704:0.01084649, 15313:0.01860609, 15749:0.0354651, 16323:0.03150783。

## p2118046 · 高K

当前token：``' on'``；token ID=389；context=2070；序列位置t=37（零起始）；原block=16。K全组=38，K展示=8。

~~~text
 be non linear crystals used to manipulate light beams into controlling others.


There are disagreements among researchers about the future capabilities of optical computers: will they be able to compete with semiconductor-based electronic computers on
~~~

[完整可见前缀](../prefixes/G014_p2118046.txt)；原bin绝对token偏移=2119717。

同位置激活成员与z：81:0.01638566, 890:0.04665291, 1451:0.029425, 1602:0.0477451, 1639:0.01468117, 1939:0.04039982, 2196:0.0122622, 2299:0.02225957, 2361:0.05457712, 2404:0.03766833, 2841:0.04945936, 2889:0.02333296, 3406:0.01385643, 3562:0.02796382, 4264:0.0201972, 4824:0.0456836, 7496:0.01402046, 8270:0.04883751, 9604:0.01348628, 10615:0.03112454, 10985:0.01370135, 11637:0.03718979, 11709:0.02008243, 11941:0.0231032, 12084:0.05215779, 12849:0.03038225, 13036:0.01600102, 13383:0.04998325, 13894:0.01627819, 14641:0.01106197, 14791:0.01935436, 14833:0.03561057, 14954:0.01911088, 14992:0.06015108, 15634:0.01951968, 15881:0.01727685, 15992:0.03042467, 16323:0.02149806。

## p4099276 · 单成员

当前token：``'.\n\n'``；token ID=382；context=4006；序列位置t=576（零起始）；原block=31。K全组=1，K展示=1。

~~~text
written by Louanne Johnson), "Dangerous Minds" tries but fails to cut to the heart of the social issues it discusses. The main problem is that the script depends too much on dramatic convention, and too often chooses to take the easy way out rather than directly confronting the reality of it's premise and characters.


~~~

[完整可见前缀](../prefixes/G014_p4099276.txt)；原bin绝对token偏移=4102720。

同位置激活成员与z：16323:0.008680678。

## p9405340 · 单成员

当前token：``'ster'``；token ID=3667；context=9192；序列位置t=817（零起始）；原block=71。K全组=1，K展示=1。

~~~text
eparedStatement is compiled onlyyonce.

above code compiled once, because java compiler checks for syntax validation.

and sql is validation will be done by database driver.

mainly we use it in loops for better performance.

if we go for Statement,this will be compiled ,validated and executed every time.
chris webster
~~~

[完整可见前缀](../prefixes/G014_p9405340.txt)；原bin绝对token偏移=9413425。

同位置激活成员与z：16323:0.009718276。

## p852401 · 单成员

当前token：``' the'``；token ID=279；context=833；序列位置t=79（零起始）；原block=6。K全组=1，K展示=0。

~~~text
 [should] make a shift quickly to make more actions, rather than just watching and monitoring what's happening on the ground."

America's existing efforts to supply non-lethal aid to the fighters and Syrian aid groups "has nothing to do with protecting the Syrians being killed systematically by the Syrian mafia and the
~~~

[完整可见前缀](../prefixes/G014_p852401.txt)；原bin绝对token偏移=853071。

同位置激活成员与z：2361:0.012707。

该组任一命中几乎覆盖V面板，零散高激活文本容易给出宽泛主题错觉；必须用具体同位置子集合和条件统计，而不是强行命名340成员的主题。

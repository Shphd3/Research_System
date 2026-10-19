# G034：同一预测位置的输入与激活

类别是选择方法，不是语义标签。随机6例来自固定V面板命中位置的哈希抽样；高K6例按激活成员数选取，不代表随机命中；另取K=1三例。各例均保留完整组激活值，未激活成员为0，可回查完整矩阵。下文前缀摘录只展示末320字符，完整前缀文件从当前context起点到位置t，**包含当前token，不包含预测目标t+1**。context起点不保证原文档起点，原文档ID未知。

## p4588973 · 随机命中

当前token：``'illion'``；token ID=14726；context=4485；序列位置t=215（零起始）；原block=35。K全组=1，K展示=0。

~~~text
nt for DNA-microarray fabrication.

    Bioinformatics 2003, 19:283-284. PubMed Abstract | Publisher Full Text OpenURL


    Nucleic Acids Res 2004, 32:W465-W470. PubMed Abstract | Publisher Full Text | PubMed Central Full Text OpenURL


    Genome Biol 2002, 3(8):1-0003. BioMed Central Full Text OpenURL

  10. Killion
~~~

[完整可见前缀](../prefixes/G034_p4588973.txt)；原bin绝对token偏移=4592855。

同位置激活成员与z：3231:0.01446485。

## p6053579 · 随机命中

当前token：``' gave'``；token ID=6551；context=5916；序列位置t=763（零起始）；原block=46。K全组=1，K展示=1。

~~~text
t who has spent his life as an opponent of second and minarets in this country. he promised before the election board that after the election you start to do something. he has this whole public-relations -- relation operation financed to a mere blumberg of new york that was ready to swing into action. what newtown gave
~~~

[完整可见前缀](../prefixes/G034_p6053579.txt)；原bin绝对token偏移=6058747。

同位置激活成员与z：6972:0.01647285。

## p1373600 · 随机命中

当前token：``' their'``；token ID=862；context=1342；序列位置t=485（零起始）；原block=10。K全组=1，K展示=0。

~~~text
ne and revenue lost by that attack exceeded $1,100 million."

In the same vein, it could be said that the bombs used this week - hijacked aircraft that came at no cost to the terrorists - cost even less than that.

Voices like that of historian and author Samuel Huntington have been accused by some of over-egging their
~~~

[完整可见前缀](../prefixes/G034_p1373600.txt)；原bin绝对token偏移=1374693。

同位置激活成员与z：12413:0.01262753。

## p312864 · 随机命中

当前token：``' or'``；token ID=476；context=305；序列位置t=749（零起始）；原block=2。K全组=1，K展示=1。

~~~text
or photons depends linearly on the speed. $E = |\mathbf{p}|c$. But this describes particles moving always at constant speed. –  juanrga Oct 15 '12 at 10:06
add comment

Basically, momentum is related to force times time, and KE is related to force times distance. It is all a metter of frame of reference, either time or
~~~

[完整可见前缀](../prefixes/G034_p312864.txt)；原bin绝对token偏移=313069。

同位置激活成员与z：97:0.007774927。

## p9071224 · 随机命中

当前token：``' everyone'``；token ID=5019；context=8866；序列位置t=252（零起始）；原block=69。K全组=1，K展示=1。

~~~text
ths of filming on location with no creature comforts. Miserable, really. He just stuck it out. I'm not exaggerating - I think he went into it as a boy and came out a man.'

You do not have to spend too much time around Penn to detect what Richard Kelly calls his 'purity of purpose'. In an age when actors, like everyone
~~~

[完整可见前缀](../prefixes/G034_p9071224.txt)；原bin绝对token偏移=9079036。

同位置激活成员与z：6975:0.02075957。

## p864505 · 随机命中

当前token：``'\n'``；token ID=198；context=844；序列位置t=930（零起始）；原block=6。K全组=2，K展示=1。

~~~text
 user's perspective, they taste like Napster," says Matt Oppenheim, the RIAA's senior vice president for business and legal affairs. "Are they architected differently? Sure. Does that mean they don't know what's going on? C'mon. Everyone knows."

Next Page »
My Voice Nation Help

Concert Calendar

  • December
  • Wed

~~~

[完整可见前缀](../prefixes/G034_p864505.txt)；原bin绝对token偏移=865186。

同位置激活成员与z：3731:0.01514625, 12269:0.05023365。

## p2564538 · 高K

当前token：``' of'``；token ID=315；context=2506；序列位置t=411（零起始）；原block=19。K全组=31，K展示=16。

~~~text
might bring something back from Finnland too. And then there's Min, who needs her MOA, besides being the only person Rand can really count on. She's reading all of Herid Fels stuff and may just come up with The Big Clue there. I'm hoping.

And, BTW, Rand is an AoL hero, albeit in the new (getting older quickly) body of
~~~

[完整可见前缀](../prefixes/G034_p2564538.txt)；原bin绝对token偏移=2566555。

同位置激活成员与z：97:0.07186184, 2502:0.01762909, 2776:0.0238944, 3231:0.02886914, 3731:0.03516578, 4096:0.0794818, 4194:0.06024183, 4955:0.009408772, 6029:0.02675126, 6130:0.01043157, 6373:0.03376442, 6972:0.02477363, 6990:0.01143507, 8314:0.009786725, 8523:0.02994377, 9499:0.1254611, 9538:0.03398756, 9958:0.02490785, 10193:0.05760686, 10752:0.01879078, 11699:0.07445154, 11762:0.01767312, 12020:0.02155304, 12286:0.05324309, 12594:0.1355937, 12677:0.04724406, 13450:0.02617631, 13838:0.01756541, 14312:0.02946085, 14696:0.01456451, 15699:0.02508353。

## p6125193 · 高K

当前token：``' of'``；token ID=315；context=5986；序列位置t=748（零起始）；原block=46。K全组=31，K展示=13。

~~~text
 different modes of operation may cause unexpected weaknesses. For example, consider one message encrypted with CFB mode with IV=2 (which is perfectly secure) and another message encrypted with CTR mode with IV=0 (also secure). If we give the attacker both ciphertexts, he knows a relationship between the first block of
~~~

[完整可见前缀](../prefixes/G034_p6125193.txt)；原bin绝对token偏移=6130412。

同位置激活成员与z：97:0.03060208, 2502:0.04106659, 2776:0.01779089, 3231:0.04254102, 4096:0.02747984, 4194:0.01116956, 4955:0.01233846, 6029:0.01210283, 6130:0.02312689, 6373:0.02888161, 6496:0.01161698, 6511:0.01273848, 6990:0.02779249, 8314:0.01833165, 8729:0.07218704, 8987:0.01161604, 9318:0.049716, 9499:0.07419159, 9538:0.1140657, 9663:0.02389573, 10193:0.01537053, 11699:0.03538904, 11762:0.0259739, 11825:0.009826519, 12020:0.02082062, 12286:0.03810637, 12594:0.1316875, 12677:0.02478312, 13197:0.03301185, 13450:0.05181107, 14312:0.01603312。

## p4567112 · 高K

当前token：``' of'``；token ID=315；context=4463；序列位置t=875（零起始）；原block=34。K全组=29，K展示=11。

~~~text
re tellingly, backward through a pageant of musical influences that seem, over the past half-century, to have inhabited the singer's voice, where they still abide.

Wilentz's book stems, in his own words, from its author's curiosity "about when, how, and why Dylan picked up on certain forerunners, as well as certain of
~~~

[完整可见前缀](../prefixes/G034_p4567112.txt)；原bin绝对token偏移=4570987。

同位置激活成员与z：245:0.04344963, 1249:0.0152858, 1691:0.03039361, 3231:0.0117793, 5754:0.1571403, 6130:0.01018743, 6391:0.01056367, 6511:0.05839277, 6867:0.0472286, 6972:0.0137873, 6975:0.04468535, 6982:0.02135179, 7007:0.06501013, 7514:0.01521897, 7825:0.1192334, 8523:0.04678947, 9318:0.01175214, 9499:0.05075409, 10193:0.02098576, 10752:0.06029469, 10953:0.0364125, 11762:0.04306374, 11825:0.03033433, 12594:0.1336406, 12677:0.03357218, 13287:0.0117025, 13332:0.1172595, 14344:0.01685817, 15699:0.01116752。

## p5104845 · 高K

当前token：``' of'``；token ID=315；context=4989；序列位置t=462（零起始）；原block=38。K全组=29，K展示=14。

~~~text
ng buoyant commodity prices. It was 1962 and it was a good time to be working in a primary industry.

RAY BRENT: Wool buyers at that stage, I suppose, were treated almost like kings, coming off a period of time where wool was a pound a pound in the early '50s, after the war was over, and wool was just king and queen of
~~~

[完整可见前缀](../prefixes/G034_p5104845.txt)；原bin绝对token偏移=5109198。

同位置激活成员与z：736:0.04547501, 1667:0.009175822, 1691:0.0111065, 2502:0.01665252, 2776:0.07272252, 3731:0.0839939, 4096:0.04334898, 4194:0.01239026, 5088:0.02262436, 5754:0.02628088, 6029:0.01063798, 6130:0.01726751, 6496:0.01064041, 6511:0.00980879, 6972:0.02111152, 6990:0.0404878, 8314:0.01466954, 8523:0.03189689, 9499:0.08688691, 10193:0.04686467, 11699:0.0261117, 11762:0.01742898, 11825:0.05914292, 12020:0.0200882, 12594:0.1619609, 12677:0.01697062, 13450:0.03374466, 14696:0.02994537, 15699:0.05267142。

## p1340487 · 高K

当前token：``'of'``；token ID=1055；context=1310；序列位置t=119（零起始）；原block=10。K全组=28，K展示=12。

~~~text
appeal to them, while coming up with NEW policy ideas, instead of recycling those we've used since the 80's.

Otherwise, were going to lose a generation of voters, and well feel the effects far longer.

Going down my Facebook there were a lot of sadness and bitterness at the outcome last night.  But almost everyone (of
~~~

[完整可见前缀](../prefixes/G034_p1340487.txt)；原bin绝对token偏移=1341559。

同位置激活成员与z：1249:0.01137955, 1667:0.05800395, 1691:0.07629205, 2691:0.01257403, 3231:0.01129102, 4096:0.02406187, 5754:0.07950354, 6130:0.03142767, 6511:0.01566816, 6972:0.06676582, 6975:0.05054472, 6982:0.01305101, 7007:0.0149613, 7514:0.01692795, 8523:0.1791137, 9238:0.03359332, 9499:0.09030487, 10193:0.06786077, 11762:0.03232155, 11825:0.03521714, 12020:0.009346008, 12194:0.04702841, 12594:0.1375469, 13287:0.01219078, 13332:0.02057983, 13838:0.01756541, 14696:0.02017974, 15699:0.1098003。

## p1996480 · 高K

当前token：``' of'``；token ID=315；context=1951；序列位置t=211（零起始）；原block=15。K全组=27，K展示=14。

~~~text
o 2.0 GHz, Weight: 23.98 oz. L=7.87 inches, W=3.94 inches, H= 1.97 inches<|im_end|>Destination unknown

Ethical traveler Jeff Greenwald has a trip for you: Strange Travel Suggestions
Photo by Jeff Greenwald

> a&


Still, there are consistent elements. There is no need to reinvent the wheel — or the impressive Wheel of
~~~

[完整可见前缀](../prefixes/G034_p1996480.txt)；原bin绝对token偏移=1998035。

同位置激活成员与z：97:0.1260611, 2776:0.0473319, 3731:0.2075291, 4096:0.05604429, 6029:0.03261064, 6130:0.009699151, 6373:0.009350356, 6496:0.02431229, 6990:0.03804639, 8523:0.01724846, 9499:0.0844455, 9538:0.04424147, 9696:0.05569611, 10193:0.02928654, 10288:0.07032825, 11699:0.05638513, 11762:0.03085671, 11811:0.04881082, 11825:0.02056871, 12020:0.02301788, 12194:0.02798544, 12286:0.04396575, 12594:0.1590312, 12677:0.02331828, 13450:0.02642045, 13838:0.01634471, 14696:0.03897857。

## p2523251 · 单成员

当前token：``' the'``；token ID=279；context=2466；序列位置t=84（零起始）；原block=19。K全组=1，K展示=1。

~~~text
Oh, I know I am dissing RJ's style, but only, I repeat, only this once!!!!!

As for Cadsuane, I reserved my opinion for later and found that I really liked her. Even with her questionable behaviors. He needs a balancer(?) and she definitely is it.
Rob Munnelly
12. RobMRobM
Leigh - thanks for including the bit about the
~~~

[完整可见前缀](../prefixes/G034_p2523251.txt)；原bin绝对token偏移=2525268。

同位置激活成员与z：15422:0.03687373。

## p837400 · 单成员

当前token：``' the'``；token ID=279；context=818；序列位置t=413（零起始）；原block=6。K全组=1，K展示=1。

~~~text
it like the odd man out with no loop at all and the thin line not connecting to it, and the line connecting to the u curving.. let me show you what i mean.

jselig's picture

Forgive me for asking if I'm just tired but is there a _k_ in the alphabet sample?

The only thing(s) that really jumps out at me is the _p_, the
~~~

[完整可见前缀](../prefixes/G034_p837400.txt)；原bin绝对token偏移=838045。

同位置激活成员与z：15422:0.03052607。

## p9171203 · 单成员

当前token：``' F'``；token ID=434；context=8963；序列位置t=991（零起始）；原block=70。K全组=1，K展示=0。

~~~text
 apologetics, read Church history, read theology, taught, studied, and so on…. and it all really made sense. Oh sure, there were some occasional problems or doubts, but they didn’t overwhelm the greater portion that made so much sense.
In the end, it all fell apart pretty quickly.<|im_end|>What are FASD, FAS, Partial F
~~~

[完整可见前缀](../prefixes/G034_p9171203.txt)；原bin绝对token偏移=9179103。

同位置激活成员与z：8486:0.02044101。

当前token构成富集“ of”“ the”等词片，不能把不同位置的这些例子合成一次共同激活或命名为统一知识主题。读者应同时查看单成员与高K行的反例。

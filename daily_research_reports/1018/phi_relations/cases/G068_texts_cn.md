# G068：同一预测位置的输入与激活

类别是选择方法，不是语义标签。随机6例来自固定V面板命中位置的哈希抽样；高K6例按激活成员数选取，不代表随机命中；另取K=1三例。各例均保留完整组激活值，未激活成员为0，可回查完整矩阵。下文前缀摘录只展示末320字符，完整前缀文件从当前context起点到位置t，**包含当前token，不包含预测目标t+1**。context起点不保证原文档起点，原文档ID未知。

## p5443250 · 随机命中

当前token：``').'``；token ID=568；context=5320；序列位置t=235（零起始）；原block=41。K全组=3，K展示=3。

~~~text
irazi, Asghar, Constitution of Iran, I. B. Tauris, 1998
  28. ^ Sayyid Qutb's Milestones and equality


  • Berman, Paul (2003). Terror and Liberalism. W.W. Norton. 
  • Haddad, Yvonne Y. (1983). "Sayyid Qutb: ideologue of Islamic revival". In Esposito, J. Voices of the Islamic Revolution. 
  • Hasan, S. Badrul (1982).
~~~

[完整可见前缀](../prefixes/G068_p5443250.txt)；原bin绝对token偏移=5447915。

同位置激活成员与z：5451:0.05468008, 13292:0.09251705, 15730:0.01275869。

## p8391006 · 随机命中

当前token：``'!\n\n'``；token ID=2219；context=8201；序列位置t=455（零起始）；原block=64。K全组=4，K展示=4。

~~~text
n if most of us could see it from the very beginning. I hope the Swedes get their hands on him soon...

And yes John, no surprise to see you defending this fake..I respected you for the fantastic journalism you did in East Timor, and in other places..but hitching yourself to Assange's falling star is a grave mistake!


~~~

[完整可见前缀](../prefixes/G068_p8391006.txt)；原bin绝对token偏移=8398279。

同位置激活成员与z：868:0.008514902, 2252:0.02245672, 15730:0.04718252, 16173:0.03309289。

## p7984509 · 随机命中

当前token：``' -'``；token ID=481；context=7804；序列位置t=79（零起始）；原block=60。K全组=1，K展示=1。

~~~text
 Defamatory, abusive, obscene, racist, or otherwise hateful
  • Excessively foul and/or vulgar
  • Inappropriately sexual
  • Baseless personal attacks or otherwise threatening
  • Commercial postings attempting to sell a product/item



Steve  Dosh's picture

Auburn kindergartners get iPads

. . Nice article ?  noon -
~~~

[完整可见前缀](../prefixes/G068_p7984509.txt)；原bin绝对token偏移=7991375。

同位置激活成员与z：6759:0.00682836。

## p5854429 · 随机命中

当前token：``' If'``；token ID=1416；context=5722；序列位置t=65（零起始）；原block=44。K全组=2，K展示=2。

~~~text
 Solutions of Dover, N.H.

Warshaw has been scathingly critical of OPD's progress and for the last several months, Judge Henderson has been threatening to put OPD into federal receivership.

Last week, Oakland agreed to a settlement that will place a federal "compliance monitor" in charge of OPD. If
~~~

[完整可见前缀](../prefixes/G068_p5854429.txt)；原bin绝对token偏移=5859393。

同位置激活成员与z：12654:0.01065512, 12706:0.007935382。

## p8456293 · 随机命中

当前token：``'.'``；token ID=13；context=8265；序列位置t=246（零起始）；原block=64。K全组=10，K展示=10。

~~~text
Blue_DudePartially fixed FS #10614, at least the resume from bookmark error. You can now resume a bookmark even if the index is incorrect, e.g. you've deleted some files from the directory and you're trying to resume one of the remaining files.
22:08:50CIA-5New commit by 03Blue_Dude (r25558): Partial fix for FS #10614.
~~~

[完整可见前缀](../prefixes/G068_p8456293.txt)；原bin绝对token偏移=8463606。

同位置激活成员与z：1273:0.01163965, 3954:0.02149678, 5451:0.1196215, 6150:0.02000692, 6449:0.02192627, 9967:0.02004296, 12654:0.02286215, 13292:0.1120483, 14850:0.02697285, 15730:0.06915517。

## p1429893 · 随机命中

当前token：``' But'``；token ID=1988；context=1397；序列位置t=489（零起始）；原block=10。K全组=3，K展示=3。

~~~text
ted to manic-depressive mood swings, traumas, and apocalyptic expectations. Finally, coming to Soto Zen, he sees the futility of all the dramatics, and settles down into peace and self acceptance. "The lotus rises from the bottom of the pond; the flower unfolds to the light."(7)

I would agree with Hyers very much. But
~~~

[完整可见前缀](../prefixes/G068_p1429893.txt)；原bin绝对token偏移=1431017。

同位置激活成员与z：6150:0.02073934, 16106:0.02664989, 16173:0.01136438。

## p9247601 · 高K

当前token：``'.'``；token ID=13；context=9038；序列位置t=641（零起始）；原block=70。K全组=21，K展示=21。

~~~text
ch a thing with all these troubles going on.

Thanks for the midterm campaign help, Mr. President.

The president, who just returned from his latest vacation himself, didn't have time today to mention that Congress has been run by his own Democratic party since the 2006 elections with even larger majorities after 2008.
~~~

[完整可见前缀](../prefixes/G068_p9247601.txt)；原bin绝对token偏移=9255553。

同位置激活成员与z：868:0.05172779, 1273:0.01456934, 2252:0.03295476, 3954:0.008557327, 5451:0.1323168, 6150:0.02073934, 6449:0.03120361, 6759:0.04540258, 8546:0.01514283, 9967:0.03176171, 10538:0.06180026, 12276:0.0395022, 12654:0.03506919, 12706:0.009400226, 13008:0.0188639, 13292:0.09154049, 14850:0.03771503, 15137:0.07788101, 15730:0.1248192, 16106:0.009804185, 16173:0.01600305。

## p4103533 · 高K

当前token：``'.'``；token ID=13；context=4010；序列位置t=742（零起始）；原block=31。K全组=20，K展示=20。

~~~text
ractitioners of slavery.

Qur’an 9:5, “Fight and kill the disbelievers wherever you find them, take them captive, harass them, lie in wait and ambush them using every stratagem of war.”


free-iranAnd as for Iran’s mullahs’ unyielding drive to acquire the ultimate weapon, it is in obedience to the command of the Quran.
~~~

[完整可见前缀](../prefixes/G068_p4103533.txt)；原bin绝对token偏移=4106982。

同位置激活成员与z：868:0.03707936, 1273:0.01652246, 2252:0.01415594, 3954:0.01856709, 5451:0.0932543, 6449:0.02241455, 6759:0.03026586, 8546:0.02832642, 9967:0.0515371, 10538:0.05789401, 12276:0.009228762, 12654:0.0423934, 12706:0.02356038, 13008:0.02618812, 13292:0.123767, 14850:0.0230666, 15137:0.06030288, 15730:0.1004052, 16106:0.02738231, 16173:0.00892297。

## p389311 · 高K

当前token：``'.'``；token ID=13；context=380；序列位置t=437（零起始）；原block=2。K全组=20，K展示=20。

~~~text
t’s tempting to imagine that Bernie Sanders is the leftward equivalent of the TP, but I don’t buy it.

    “I think it would be a good idea if President Obama faced some primary opposition.” – Sanders

    No problem with that sentiment from this quarter; I view it as very much in keeping with our democratic tradition.
~~~

[完整可见前缀](../prefixes/G068_p389311.txt)；原bin绝对token偏移=389557。

同位置激活成员与z：868:0.03805592, 1273:0.04240137, 2252:0.01610906, 3954:0.03956319, 5451:0.1303637, 6150:0.04344442, 6449:0.0119165, 6759:0.06493383, 8546:0.01807252, 9967:0.02101952, 10538:0.03885105, 12276:0.01313501, 12654:0.01871176, 12706:0.01013265, 13008:0.0344889, 13292:0.108142, 14850:0.008418158, 15137:0.03149429, 15730:0.1150536, 16173:0.06238977。

## p5360957 · 高K

当前token：``'.'``；token ID=13；context=5239；序列位置t=817（零起始）；原block=40。K全组=20，K展示=20。

~~~text
tion that her fridge contains a watermelon shaped like her face. I want to eat it!




According to a source, three record companies including Sony have bid to record the cast recording for the hit Broadway spoof Xanadu, but the best offers are contingent on current male lead Cheyenne Jackson being part of the project.
~~~

[完整可见前缀](../prefixes/G068_p5360957.txt)；原bin绝对token偏移=5365553。

同位置激活成员与z：1273:0.01896387, 2252:0.05492742, 3954:0.01246358, 5451:0.1020434, 6150:0.0336788, 6449:0.03755127, 6759:0.03612524, 8546:0.02271119, 9967:0.03005272, 10538:0.06521823, 12276:0.04633814, 12654:0.0189559, 12706:0.03308187, 13008:0.02399085, 13292:0.1032592, 14850:0.01598652, 15137:0.07983413, 15730:0.1043114, 16106:0.03446239, 16173:0.0433468。

## p32473 · 高K

当前token：``'.'``；token ID=13；context=31；序列位置t=750（零起始）；原block=0。K全组=20，K展示=20。

~~~text
en making. Most players that are dirty are looking for an edge. It is a constant search that is ubiquitous through all sports. Bryant is extremely knowledgeable about that game and has studied what you can and can't get away with. 

It just so happens that pushing off and elbowing opponents does not get readily called.
~~~

[完整可见前缀](../prefixes/G068_p32473.txt)；原bin绝对token偏移=32494。

同位置激活成员与z：868:0.03561451, 1273:0.01798731, 2252:0.03393133, 3954:0.01124287, 5451:0.07421133, 6150:0.03270224, 6449:0.008986816, 6759:0.03124242, 8546:0.03613892, 9967:0.04811913, 10538:0.02371433, 12276:0.01801782, 12654:0.02701255, 13008:0.06134437, 13292:0.1325561, 14850:0.01305683, 15137:0.02441421, 15730:0.120913, 16106:0.01224559, 16173:0.02967492。

## p2215877 · 高K

当前token：``'.'``；token ID=13；context=2165；序列位置t=664（零起始）；原block=16。K全组=20，K展示=20。

~~~text
arge unmet medical need.

Despite the questions, there is a lot of potential for Galena in the space. When you consider that both companies have a folate candidate, the potential for ImmunoGen to enter first-line therapy, and Galena to market NeuVax alone or in combination with Herceptin, the sky looks to be the limit.
~~~

[完整可见前缀](../prefixes/G068_p2215877.txt)；原bin绝对token偏移=2217624。

同位置激活成员与z：868:0.05319264, 2252:0.03490789, 3954:0.04591084, 5451:0.07811758, 6150:0.04881552, 6449:0.03169189, 6759:0.05223852, 8546:0.02686158, 9967:0.03200585, 10538:0.03689792, 12276:0.01167017, 12654:0.03116294, 12706:0.01110921, 13008:0.02960609, 13292:0.1257202, 14850:0.0267287, 15137:0.06811538, 15730:0.1072411, 16106:0.01517528, 16173:0.04578821。

## p10206003 · 单成员

当前token：``' '``；token ID=220；context=9975；序列位置t=405（零起始）；原block=77。K全组=1，K展示=1。

~~~text
se, Syrians, GCC citizens, Americans, Canadians, and Egyptians. Jordan earned almost $1 billion dollars in medical tourism revenues according to the World Bank.

According to the CIA World Factbook, life expectancy in Jordan is 80.18 years, the second highest in the region (after Israel). There were 203 physicians per 
~~~

[完整可见前缀](../prefixes/G068_p10206003.txt)；原bin绝对token偏移=10214805。

同位置激活成员与z：14850:0.02086933。

## p6216423 · 单成员

当前token：``' '``；token ID=220；context=6075；序列位置t=941（零起始）；原block=47。K全组=1，K展示=1。

~~~text
. 
   9  Linux is a clone of the operating system Unix, written from scratch by
  10  Linus Torvalds with assistance from a loosely-knit team of hackers across
  11  the Net. It aims towards POSIX and Single UNIX Specification compliance.
  13  It has all the features you would expect in a modern fully-fledged Unix,
  
~~~

[完整可见前缀](../prefixes/G068_p6216423.txt)；原bin绝对token偏移=6221741。

同位置激活成员与z：14850:0.02257831。

## p4727815 · 单成员

当前token：``'\n\n'``；token ID=271；context=4620；序列位置t=974（零起始）；原block=36。K全组=1，K展示=1。

~~~text
heir mess.

impty Wed 05-Dec-12 07:57:10

People walking their dogs must end up walking around or standing in their own dogs poo? For that reason alone you'd think they'd pick up.

I pick up, but spend my time walking around horse poo on the roads... It's easier to spot though smile

YouOldSlag Wed 05-Dec-12 07:41:22


~~~

[完整可见前缀](../prefixes/G068_p4727815.txt)；原bin绝对token偏移=4731854。

同位置激活成员与z：15730:0.1004052。

这些例子包含参考文献、新闻、软件提交、评论等来源。高K六例当前token都是句点，随机例还包含转折词、连接符和换行；目前更可靠的共同点是词片或格式条件富集，不是一个统一主题。

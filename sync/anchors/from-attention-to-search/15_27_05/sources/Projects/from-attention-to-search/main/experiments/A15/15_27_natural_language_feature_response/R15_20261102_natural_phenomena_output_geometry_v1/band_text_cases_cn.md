# 输入文字规则预定的谱现象真实案例

四条来自发现视图的文字属性，各取哈希排序最前的两个不同来源、同文档同token配对。样例选择不读取响应，不保证符合总体平均；缺少配对时不补漂亮例子。每个前文均截到当前token，不使用后文。以下变化包含两个真实前文的全部差异，不是只改变一个属性的最小干预。

## 1．近期URL或哈希形片段

文档`R15_general_119`，来源[www.waterstones.com](https://www.waterstones.com/book/francis-cauffman-2015/james-crispino/9781941806012)。当前位置分别302和326，相同片段`
`，编号198；相距24个token。

属性为真的完整可见前文：

```text
The Testaments out now
Francis Cauffman 2015 (Hardback)
  • Francis Cauffman 2015 (Hardback)

Francis Cauffman 2015 (Hardback)

Hardback 100 Pages / Published: 24/02/2016
  • Publisher out of stock

Currently unavailable to order

This product is currently unavailable.

  • This item has been added to your basket
The work of Francis Cauffman creates a dialogue between program and place. They reveal the relationships embedded in the environment and activities of a specific project. What is their client's true aim in doing this project? What do they do, and why do they do it? How can they influence their work? This active and essential conversation with their clients becomes the story of their architecture. Francis Cauffman integrate their clients' desired patterns of activity and their functional needs with the physical aspects of architecture. Their emerging body of work amplifies that relationship through a subtle and pragmatic resolution of the specific program for a given project. Francis Cauffman demonstrates new ways of understanding how place and program drive behaviours. They create architectural hybrids that merge a variety of uses and relate to specific environments in terms of the physical forms and human activities that they nurture and stimulate.

Publisher: Oro Editions
ISBN: 9781941806012
Number of pages: 100
Weight: 499 g

```

属性为假的完整可见前文：

```text
The Testaments out now
Francis Cauffman 2015 (Hardback)
  • Francis Cauffman 2015 (Hardback)

Francis Cauffman 2015 (Hardback)

Hardback 100 Pages / Published: 24/02/2016
  • Publisher out of stock

Currently unavailable to order

This product is currently unavailable.

  • This item has been added to your basket
The work of Francis Cauffman creates a dialogue between program and place. They reveal the relationships embedded in the environment and activities of a specific project. What is their client's true aim in doing this project? What do they do, and why do they do it? How can they influence their work? This active and essential conversation with their clients becomes the story of their architecture. Francis Cauffman integrate their clients' desired patterns of activity and their functional needs with the physical aspects of architecture. Their emerging body of work amplifies that relationship through a subtle and pragmatic resolution of the specific program for a given project. Francis Cauffman demonstrates new ways of understanding how place and program drive behaviours. They create architectural hybrids that merge a variety of uses and relate to specific environments in terms of the physical forms and human activities that they nurture and stimulate.

Publisher: Oro Editions
ISBN: 9781941806012
Number of pages: 100
Weight: 499 g
Dimensions: 235 x 184 mm

You may also be interested in...

Rome Was

```

原始向量差长度：h=850.91087，真实final norm后的y=125.78411；有效logit变化均方根=3.4446602；相对各向同性单位方向增益=0.95244528倍。

八个固定h谱段中的实际变化平方范数比例：60.2963%, 12.5019%, 1.9917%, 2.2263%, 3.6555%, 7.9520%, 6.6219%, 4.7544%。

现象位置减参照位置的原始中心化能量占比差（不是上述实际差向量分解）：-20.07200个百分点, -0.15930个百分点, -1.66558个百分点, -1.26373个百分点, +3.06325个百分点, +5.57761个百分点, +7.53447个百分点, +6.98528个百分点。

反例检查：两个前文当前token相同、来源相同，但位置和其它文字仍不同；不能把全部向量差归为这一个属性。此例若不符合总体谱偏向，也原样保留。

## 2．近期URL或哈希形片段

文档`R15_general_120`，来源[region13.herbzinser23.com](http://region13.herbzinser23.com/r8js/famous-jews.php)。当前位置分别47和444，相同片段`6`，编号21；相距397个token。

属性为真的完整可见前文：

```text
Kapisanan ng mga Brodkaster ng Pilipinas

(Association of Philippine Broadcasters)

18574983_10211137701072506
```

属性为假的完整可见前文：

```text
Kapisanan ng mga Brodkaster ng Pilipinas

(Association of Philippine Broadcasters)

18574983_10211137701072506_774926450_o Oskar Schindler was an unlikely rescuer of the Jews. Most of the Jewish community consists of Ashkenazi Jews who immigrated from Encyclopedia of Jewish and Israeli history, politics and culture, with biographies, statistics, articles and documents on topics from anti-Semitism to Zionism. Last year, about two hundred red haired Israeli Jews gathered for a conference at Kibbutz Gezer in Israel. Hitler has made it clear that he will annihilate all Jews before the clock strikes twelve. Judaism is the world's oldest Abrahamic religion. S. Spain was a land of promise for Jews in the Middle Ages, until the 1492 expulsion by the Catholic Kings (Reyes Catolicos). Richard Lynn, "Why Are the Jews So Smart" (PFS 2013) - Duration: 29:14. The Jewish Chronicle is the world's oldest and most influential Jewish newspaper. Meanwhile, the Christians were only rarely usurers, falling into disgrace when they did so. Called also Aldabi or Alrabi, Aaron was the First Jew in the history to be invited during a Pontificate to discuss freely and without censorship about religious subjects and papal perplexities. While that is a nice size group, there were, apparently, many hundreds who were interested in attending, but unable to do so.

Nick Learn Jewish Diaspora in Modern China from Nanjing University. The Jews of Cuba, those few who remained after Castro took power, are able to worship openly again after almost three decades of religious restriction. Famous Jews. The JC site contains Jewish news, comment, culture, sport and more. What actors are Jewish? All of these famous Jewish American actors and actresses were born into Jewish families and so are Jewish by birth. Hanukkah. We are Jews who believe in Jesus as the Jewish Messiah. 4 million people. com. Explore 56
```

原始向量差长度：h=509.92526，真实final norm后的y=131.96255；有效logit变化均方根=3.7009873；相对各向同性单位方向增益=0.97540807倍。

八个固定h谱段中的实际变化平方范数比例：0.2743%, 32.2345%, 15.4749%, 6.7194%, 10.1081%, 16.9496%, 11.4514%, 6.7878%。

现象位置减参照位置的原始中心化能量占比差（不是上述实际差向量分解）：-3.00520个百分点, +17.04344个百分点, -16.97109个百分点, +0.86450个百分点, +4.15305个百分点, -4.31624个百分点, +3.50334个百分点, -1.27179个百分点。

反例检查：两个前文当前token相同、来源相同，但位置和其它文字仍不同；不能把全部向量差归为这一个属性。此例若不符合总体谱偏向，也原样保留。

## 3．近期时刻形数字片段

文档`R15_mathematics_146`，来源[matheducators.stackexchange.com](https://matheducators.stackexchange.com/questions/5586/how-can-you-be-perfect-at-maths-highschool/12562)。当前位置分别325和316，相同片段` `，编号220；相距9个token。

属性为真的完整可见前文：

```text
I'm in my last year of highschool. And I'm aiming for a perfect grade in maths. The problem is that this year is the hardest year of maths I have ever faced in my entire life. Especially derivation and limits as its the first time I am studying it. Here are the lessons that are required to study for the first semester:

  • Limit of a function at a point
  • Limits Theorems
  • Limits of fractional functions
  • Limits of Trigonometric functions
  • Limits at Infinity
  • Continuity at a point
  • Continuity on an interval
  • Rate of Change
  • First derivative
  • Continuity and differentiation
  • Differentiation Rules
  • Derivatives of Higher Order
  • The chain rule
  • Implicit differentiation
  • Geometric applications of differentiation
  • Physical applications of differentiation
  • Related Rates
  • Increasing and Decreasing functions
  • Extreme Values.

Limits are relatively easy. However, related rates and extreme values are disgustingly difficult, is there any way to make those two lessons easy and routine? Something like a book filled with questions on those two or something.


  • 2
    $\begingroup$ I've retagged this <calculus> instead of <differential-equations> and added the <secondary-education> tag, although it must be said that the topics mentioned are often also covered in early undergraduate calculus. $\endgroup$ – J W Oct 17 '14 at 13:52
  • 
```

属性为假的完整可见前文：

```text
I'm in my last year of highschool. And I'm aiming for a perfect grade in maths. The problem is that this year is the hardest year of maths I have ever faced in my entire life. Especially derivation and limits as its the first time I am studying it. Here are the lessons that are required to study for the first semester:

  • Limit of a function at a point
  • Limits Theorems
  • Limits of fractional functions
  • Limits of Trigonometric functions
  • Limits at Infinity
  • Continuity at a point
  • Continuity on an interval
  • Rate of Change
  • First derivative
  • Continuity and differentiation
  • Differentiation Rules
  • Derivatives of Higher Order
  • The chain rule
  • Implicit differentiation
  • Geometric applications of differentiation
  • Physical applications of differentiation
  • Related Rates
  • Increasing and Decreasing functions
  • Extreme Values.

Limits are relatively easy. However, related rates and extreme values are disgustingly difficult, is there any way to make those two lessons easy and routine? Something like a book filled with questions on those two or something.


  • 2
    $\begingroup$ I've retagged this <calculus> instead of <differential-equations> and added the <secondary-education> tag, although it must be said that the topics mentioned are often also covered in early undergraduate calculus. $\endgroup$ – J W Oct 17 '14 at 
```

原始向量差长度：h=414.78012，真实final norm后的y=74.216691；有效logit变化均方根=2.0938354；相对各向同性单位方向增益=0.9812064倍。

八个固定h谱段中的实际变化平方范数比例：3.4270%, 10.9452%, 7.0477%, 8.9761%, 16.9260%, 22.3987%, 19.6277%, 10.6515%。

现象位置减参照位置的原始中心化能量占比差（不是上述实际差向量分解）：-10.77679个百分点, +17.07257个百分点, -0.66582个百分点, -0.98587个百分点, -2.09800个百分点, -2.66779个百分点, +0.11067个百分点, +0.01103个百分点。

反例检查：两个前文当前token相同、来源相同，但位置和其它文字仍不同；不能把全部向量差归为这一个属性。此例若不符合总体谱偏向，也原样保留。

## 4．近期时刻形数字片段

文档`R15_biology_132`，来源[www.reefcentral.com](http://www.reefcentral.com/forums/archive/index.php/t-945206.html)。当前位置分别23和78，相同片段`2`，编号17；相距55个token。

属性为真的完整可见前文：

```text
View Full Version : Az-no3

10/06/2006, 11:2
```

属性为假的完整可见前文：

```text
View Full Version : Az-no3

10/06/2006, 11:25 PM
1) Has anyone used this?
2) Did it work?
3) Does it seem like its based on solid science, or is it more along the lines of "snake oil"?


Randy Holmes-Farley
10/07/2
```

原始向量差长度：h=1345.9916，真实final norm后的y=107.61；有效logit变化均方根=2.6311359；相对各向同性单位方向增益=0.85037422倍。

八个固定h谱段中的实际变化平方范数比例：74.4321%, 12.1712%, 7.1031%, 1.3705%, 1.6110%, 1.6412%, 1.0664%, 0.6045%。

现象位置减参照位置的原始中心化能量占比差（不是上述实际差向量分解）：+65.52883个百分点, -25.52551个百分点, -0.85358个百分点, -6.80450个百分点, -10.13058个百分点, -9.26389个百分点, -8.16138个百分点, -4.78939个百分点。

反例检查：两个前文当前token相同、来源相同，但位置和其它文字仍不同；不能把全部向量差归为这一个属性。此例若不符合总体谱偏向，也原样保留。

## 5．近期可见段落换行

文档`R15_mathematics_117`，来源[farniche.wordpress.com](https://farniche.wordpress.com/tag/forward-velocity/)。当前位置分别272和359，相同片段` to`，编号311；相距87个token。

属性为真的完整可见前文：

```text
Building an XNA Game Studio XBox360 Indie Game.

[page 0056] ~ When In Doubt:

Updates – .

The theme is still NEON.

When in doubt, read the instructions.  And so, off to where it all began, kinda sorta, for me at least, something more like the near of doing Xbox C# stuff in the past and not so much as the far off of the c++ past, and definitely not the really way back BASIC past, for the most part, I think.

Well, the Unity Project: Roll-a-Ball reminds me of the MSDN FuelCell Example Game which uses the MicroSoft XNA Game Studio 2010.  I also found this, Unity Third Person Control: Camera Follow – Tutorial 7, which is a multi-part tutorial that runs a character around using an XBox 360 Joystick Controller, my favorite means of game input.  Currently I’m using the afore mentioned controller that is connected via the USB Wireless version to my PC.  Using this, the PC can take up to four controller inputs simultaneously.  The wireless models let the XBox 360 connect up to four controllers concurrently, if the game is built for that type of allowance.

And so, not only is this game going to
```

属性为假的完整可见前文：

```text
Building an XNA Game Studio XBox360 Indie Game.

[page 0056] ~ When In Doubt:

Updates – .

The theme is still NEON.

When in doubt, read the instructions.  And so, off to where it all began, kinda sorta, for me at least, something more like the near of doing Xbox C# stuff in the past and not so much as the far off of the c++ past, and definitely not the really way back BASIC past, for the most part, I think.

Well, the Unity Project: Roll-a-Ball reminds me of the MSDN FuelCell Example Game which uses the MicroSoft XNA Game Studio 2010.  I also found this, Unity Third Person Control: Camera Follow – Tutorial 7, which is a multi-part tutorial that runs a character around using an XBox 360 Joystick Controller, my favorite means of game input.  Currently I’m using the afore mentioned controller that is connected via the USB Wireless version to my PC.  Using this, the PC can take up to four controller inputs simultaneously.  The wireless models let the XBox 360 connect up to four controllers concurrently, if the game is built for that type of allowance.

And so, not only is this game going to be focused on neon, but also on getting a camera to follow the game character around the game, correctly.  This simple game, FuelCell, uses the XBLIG Vector3 class to define its usage much like the Unity Vector3 class.  Both of these game platforms with, XBLIG FuelCell and Unity Roll-a-Ball, use the class GameObject as a binding structure to consolidate its game pieces and be able to
```

原始向量差长度：h=331.90786，真实final norm后的y=65.371312；有效logit变化均方根=1.9028043；相对各向同性单位方向增益=1.0123399倍。

八个固定h谱段中的实际变化平方范数比例：6.1150%, 10.4322%, 13.7233%, 13.1436%, 16.9297%, 20.1786%, 12.4293%, 7.0483%。

现象位置减参照位置的原始中心化能量占比差（不是上述实际差向量分解）：-7.94223个百分点, +5.83904个百分点, +5.01764个百分点, +0.28393个百分点, +0.70594个百分点, -0.91968个百分点, -1.60111个百分点, -1.38352个百分点。

反例检查：两个前文当前token相同、来源相同，但位置和其它文字仍不同；不能把全部向量差归为这一个属性。此例若不符合总体谱偏向，也原样保留。

## 6．近期可见段落换行

文档`R15_physics_134`，来源[xymphora.blogspot.com](http://xymphora.blogspot.com/2011/11/that-is-impossible-to-sustain.html?widgetType=BlogArchive&widgetId=BlogArchive1&action=toggle&dir=open&toggle=MONTHLY-1391230800000&toggleopen=MONTHLY-1320120000000)。当前位置分别286和310，相同片段` the`，编号279；相距24个token。

属性为真的完整可见前文：

```text
Saturday, November 19, 2011

That is impossible to sustain

"Henry Kissinger: Jews Are ‘Self-Serving Bastards’"  I should immediately note that you can't trust anything said by Henry the K, as his lies tend to reflect what he perceives his audience wants to hear, but one comment, by Gaza Calling, to this typically Jew-centric Gawker posting was interesting (and the reaction of the commentators to someone having the audacity to point out one of the most obvious Jewish tricks to provide more colonialists for Israel so predictable):
"The line about "rescuing Jews stuck behind the Iron Curtain from Soviet oppression" is simpleton talk. In truth, Jews were among the most highly educated sector of the Soviet population and the whole issue about saving them was one of the biggest scams of the 20th century.

The smartest Russians, however, may have been those who stayed behind and through a backroom deal with Yelsin came into possession of all of Russia’s natural resources, making these "oligarchs" the greatest collection of thieves, perhaps, in all of history. That they were even more exclusively Jewish than were our neocons was only, of course, a coincidence, such as, for example, the Pope being Catholic.

If you want read some fascinating Kissenger talk about the ME from the this in full...

More interesting: read the
```

属性为假的完整可见前文：

```text
Saturday, November 19, 2011

That is impossible to sustain

"Henry Kissinger: Jews Are ‘Self-Serving Bastards’"  I should immediately note that you can't trust anything said by Henry the K, as his lies tend to reflect what he perceives his audience wants to hear, but one comment, by Gaza Calling, to this typically Jew-centric Gawker posting was interesting (and the reaction of the commentators to someone having the audacity to point out one of the most obvious Jewish tricks to provide more colonialists for Israel so predictable):
"The line about "rescuing Jews stuck behind the Iron Curtain from Soviet oppression" is simpleton talk. In truth, Jews were among the most highly educated sector of the Soviet population and the whole issue about saving them was one of the biggest scams of the 20th century.

The smartest Russians, however, may have been those who stayed behind and through a backroom deal with Yelsin came into possession of all of Russia’s natural resources, making these "oligarchs" the greatest collection of thieves, perhaps, in all of history. That they were even more exclusively Jewish than were our neocons was only, of course, a coincidence, such as, for example, the Pope being Catholic.

If you want read some fascinating Kissenger talk about the ME from the this in full...

More interesting: read the document at the link, a December 1975 memorandum of conversation between U.S. secretary of state Henry the
```

原始向量差长度：h=368.79827，真实final norm后的y=80.106497；有效logit变化均方根=2.3235566；相对各向同性单位方向增益=1.0087997倍。

八个固定h谱段中的实际变化平方范数比例：12.3450%, 20.4303%, 14.3889%, 8.1740%, 10.3008%, 17.4502%, 9.9276%, 6.9831%。

现象位置减参照位置的原始中心化能量占比差（不是上述实际差向量分解）：-1.82450个百分点, +18.05661个百分点, +7.76781个百分点, -1.54331个百分点, -3.94962个百分点, -7.91493个百分点, -5.78573个百分点, -4.80633个百分点。

反例检查：两个前文当前token相同、来源相同，但位置和其它文字仍不同；不能把全部向量差归为这一个属性。此例若不符合总体谱偏向，也原样保留。

## 7．近期非ASCII字母

文档`R15_mathematics_149`，来源[www.newworldencyclopedia.org](https://www.newworldencyclopedia.org/entry/Kurt_G%C3%B6del)。当前位置分别15和58，相同片段`1`，编号16；相距43个token。

属性为真的完整可见前文：

```text
Kurt Gödel

Kurt Gödel


April 28 1
```

属性为假的完整可见前文：

```text
Kurt Gödel

Kurt Gödel


April 28 1906(1906-04-28)
Brünn (Brno) Austria-Hungary

Died January 14 1978 (aged 71
```

原始向量差长度：h=604.68887，真实final norm后的y=95.635169；有效logit变化均方根=2.5971501；相对各向同性单位方向增益=0.94449323倍。

八个固定h谱段中的实际变化平方范数比例：28.7327%, 4.0645%, 9.2801%, 8.4359%, 12.6321%, 19.4446%, 10.9184%, 6.4917%。

现象位置减参照位置的原始中心化能量占比差（不是上述实际差向量分解）：+31.75583个百分点, -9.72552个百分点, -3.96212个百分点, +1.16358个百分点, -3.76658个百分点, -4.86181个百分点, -6.02818个百分点, -4.57519个百分点。

反例检查：两个前文当前token相同、来源相同，但位置和其它文字仍不同；不能把全部向量差归为这一个属性。此例若不符合总体谱偏向，也原样保留。

## 8．近期非ASCII字母

文档`R15_physics_131`，来源[doppleronline.ca](https://doppleronline.ca/huntsville/liberals-revenue-neutral-carbon-tax-best-for-balancing-the-economy-and-the-environment-hugh-holland/)。当前位置分别109和207，相同片段` the`，编号279；相距98个token。

属性为真的完整可见前文：

```text
Liberals’ revenue-neutral carbon tax best for balancing the economy and the environment ~ Hugh Holland



The US National Oceanic and Atmospheric Administration reports that since 1948, global average temperature has increased by about 0.8 degrees Celsius.  That is consistent with the findings of the UN-sponsored Intergovernmental Panel on Climate Change. A study commissioned by Environment and Climate Change Canada says that in that same period, Canada’s average temperature over land increased 1.7ºC, with higher rates seen in the north, the
```

属性为假的完整可见前文：

```text
Liberals’ revenue-neutral carbon tax best for balancing the economy and the environment ~ Hugh Holland



The US National Oceanic and Atmospheric Administration reports that since 1948, global average temperature has increased by about 0.8 degrees Celsius.  That is consistent with the findings of the UN-sponsored Intergovernmental Panel on Climate Change. A study commissioned by Environment and Climate Change Canada says that in that same period, Canada’s average temperature over land increased 1.7ºC, with higher rates seen in the north, the Prairies and the glaciers of northern BC.  The increase in Northern Canada was 2.3ºC.  Northern Russia is seeing similar phenomena.

While the warming of Canada will result in more habitable land, it will also bring many problems. For example, the 17,000 British Columbia glaciers that store water and gradually release it over the year to BC’s 90-per-cent hydro-electric system are receding rapidly. We have personally witnessed the
```

原始向量差长度：h=400.37322，真实final norm后的y=87.28257；有效logit变化均方根=2.5194696；相对各向同性单位方向增益=1.0039244倍。

八个固定h谱段中的实际变化平方范数比例：2.6886%, 12.5163%, 10.6212%, 8.6277%, 13.2709%, 21.6817%, 17.9891%, 12.6045%。

现象位置减参照位置的原始中心化能量占比差（不是上述实际差向量分解）：+5.57976个百分点, -8.89825个百分点, -6.44342个百分点, -1.08056个百分点, +1.41176个百分点, +3.37799个百分点, +3.15491个百分点, +2.89780个百分点。

反例检查：两个前文当前token相同、来源相同，但位置和其它文字仍不同；不能把全部向量差归为这一个属性。此例若不符合总体谱偏向，也原样保留。

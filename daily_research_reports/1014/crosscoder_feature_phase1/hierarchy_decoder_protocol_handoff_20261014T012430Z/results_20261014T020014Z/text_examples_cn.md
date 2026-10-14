# 固定30节点文本：随机与高激活

每节点从V活跃位置均匀抽5条随机，并取z最大的3条。随机不是独立文档抽样。目标token与包含它的前文用于解释；右文仅辅助阅读。完整位置与14层幅度见JSONL及text_layer_amplitude.csv。不得从8条例子认证单义语义。

## Feature 14，h_V=0

### 位置1830554｜random｜z=0.009824101

上下文1789，目标offset=17，目标token="ably"；原文档未知。

包含目标的模型可见前文：

<pre>listen&quot; to the very fabric of the Far Realm and that his thoughts are inexplicably</pre>

右文（仅阅读辅助）：

<pre> tied to that horrible plane.

The visions Diirinka sends to his faithful are purposefully cryptic and nearly indecipherable. They are just as likely to contain a dire warning as they are to be completely useless, with no apparent difference between the two. By his reasoning, true believers are expected to be able to understand the madness without comprehending it, a paradox that few outside his order seem</pre>

### 位置4448415｜random｜z=0.006589238

上下文4347，目标offset=854，目标token=" deployed"；原文档未知。

包含目标的模型可见前文：

<pre> make it sound like an orchestra. But we&#x27;ve only got the bass, my guitar and his guitar.&quot;

Glasvegas are currently fielding offers from many record labels
His bandmates are his cousin Rab Allan on guitar, bassist Paul Donoguhe and drummer Caroline McKay.

Daddy&#x27;s Gone, a heartbreaking message to an absent father, has given the first glimpse of the emotional power of James&#x27; songwriting.

The lyrics begin: &quot;How you are my hero/ How you&#x27;re never here though/ Remember times when you put me on your shoulders/ How I wish that it was forever you would hold us.&quot;

They carry on in the same heart-rending vein. When the song is brought up, James immediately interjects: &quot;I knew you were going to ask that.

&quot;So Daddy&#x27;s Gone, is that through personal experience? That&#x27;s what you were going to ask, yeah?&quot;

Well, yes.

&quot;Yeah, some of it&#x27;s through personal experience. And there&#x27;s other stuff that I&#x27;ve just noticed through my friends&#x27; families. I don&#x27;t really know a lot of families where the mum and dad are still together.&quot;

The band have supported Dirty Pretty Things and Ian Brown
The point of the song, James says, is not wanting to be 50 and &quot;having to regret everything&quot;.

Daddy&#x27;s Gone was put on MySpace and soon made its way to a friend of Lisa Marie Presley.

Elvis&#x27;s daughter liked it so much that she called the band up and asked them to meet her for a drink when she was in Edinburgh recently.

&quot;It was a really nice night,&quot; James says.

&quot;It&#x27;s quite far out. It makes the world feel a bit smaller than it is because she&#x27;s heard something that I&#x27;ve recorded in my bedroom, and how the hell did that get to Lisa Marie Presley?&quot;

So what did she say?

&quot;I&#x27;ll not go into exactly what was spoke about,&quot; James says. &quot;But it was pretty far out man. It was nothing to do with music.&quot;

Despite having so many fans in high places, Glasvegas are still unsigned. But that situation is unlikely to last long. Which labels are trying to secure their signatures?

&quot;Every label I&#x27;ve ever heard of,&quot; James replies. &quot;Does that answer that?&quot;

  • Almost 150 UK-based music writers, editors and broadcasters took part in the Sound of 2008 poll. They named their three favourite new acts and their responses were used to compile a top 10.

    The BBC is not responsible for the content of external internet sites

    Has China&#x27;s housing bubble burst?
    How the world&#x27;s oldest clove tree defied an empire
    Why Royal Ballet principal Sergei Polunin quit


    Americas Africa Europe Middle East South Asia Asia Pacific&lt;|im_end|&gt;[an error occurred while processing this directive]
BBC News
watch One-Minute World News
Last Updated: Tuesday, 2 August 2005, 15:05 GMT 16:05 UK
Saudi King Fahd is laid to rest
The King&#x27;s shrouded body was carried by relatives

King Fahd of Saudi Arabia, who died on Monday, has been buried after a funeral service in the Saudi capital Riyadh.

The Saudi royal family and Muslim leaders from around the world gathered at Riyadh&#x27;s grand mosque where the funeral prayers were said.

King Fahd&#x27;s body arrived at the mosque by ambulance, draped in a brown robe.

After the prayers, the body was carried to a cemetery for burial in an unmarked grave, in keeping with Wahhabism, the kingdom&#x27;s strict version of Islam.

Security has been beefed up across the capital where foreign dignitaries had gathered to pay their respects.

Militant problem

Among those paying tribute to the king, who had ruled since 1982, were Palestinian leader Mahmoud Abbas, Egypt&#x27;s President Hosni Mubarak, French President Jacques Chirac and Jordan&#x27;s King Abdullah.

King Fahd of Saudi Arabia

In the past two years, Saudi Arabia has suffered terror attacks carried out by Islamist militants allied to al-Qaeda leader Osama Bin Laden and security was massively increased for the funeral with thousands of troops and police deployed</pre>

右文（仅阅读辅助）：

<pre> throughout the capital.

Roads leading to the Imam Turki bin Abdullah Mosque, where the funeral took place, were closed and police with sniffer dogs and x-ray equipment checked vehicles.

The king had been frail since suffering a stroke in 1995 and had delegated his powers to Crown Prince Abdullah.

Call for loyalty

An official ceremony confirming Abdullah as king is due to be held on Wednesday</pre>

### 位置4479188｜high_activation｜z=0.4494603

上下文4377，目标offset=933，目标token="6"；原文档未知。

包含目标的模型可见前文：

<pre> keeping you overweight... your first weapon is learning what they are and how they do that.

2. Carbohydrate cravings are your biggest enemy. Your second secret weapon is the plan we will show you to overcome these cravings!

If you want to know exactly how to make this happen in the next five days then just click my link below... it&#x27;s all in my free book.

But let&#x27;s get on with the article:

Here&#x27;s a question you might be asking: &quot;How come after a diet, I just seem to put all the weight back on again? The sad reality of our times is that if you are chronically overweight, then its almost certain that you are on the North American diet most typified by the McDonald&#x27;s fast food meal... maybe &quot;low in fat&quot; these days, but bursting at the seams with highly processed carbohydrates and sugars.

Doesn&#x27;t matter if it&#x27;s a fish burger or a lean chicken burger... it&#x27;s the fries, the buns the desserts and the drinks that are doing you in! This doesn&#x27;t make you a bad person... it just means that, like the rest of us, you have been suckered in by the advertising.

Here&#x27;s why it&#x27;s so important for you to understand what&#x27;s happening to your body... the North American Diet has made your body insensitive to insulin and insulin is the key to successful weight loss and control of diabetes Type 2. This is how it happens and why it&#x27;s so bad:

When you eat, the food in your stomach gets converted into glucose that moves into your bloodstream. This is the food that your brain, your muscles and your tissues need in order to survive and grow.

When glucose enters your bloodstream, your pancreas responds by releasing insulin into your blood. Insulin is needed to allow the glucose to enter your cells. There, it is broken down to produce the energy needed for your cells to work properly.&lt;|im_end|&gt;tag:blogger.com,1999:blog-7675087351939177300.post5166892779408797469..comments2013-12-19T07:29:30.113-06:00Comments on Sutured for a Living: Unused and Old Medicationsrlbateshttp://www.blogger.com/profile/15236331355857884458noreply@blogger.comBlogger2125tag:blogger.com,1999:blog-7675087351939177300.post-38917394274437061202008-01-01T23:13:00.000-06:002008-01-01T23:13:00.000-06:00Hey there, I was horrified when I found out how an...Hey there, &lt;BR/&gt;&lt;BR/&gt;I was horrified when I found out how antidepressants are adversely affecting mussels and other bivalves. It just blew me away, never imagined this kind of effect. &lt;BR/&gt;&lt;BR/&gt;Glad you (and my HMO&#x27;s pharmacy) are spreading the word. My mom has a medicine cabinet full of Quaaludes and Dilaudid and other exciting products. I think dating 1970s forward. Just this weekend, talked her into creating a goody bag to be hauled off to the HMO. Returned. Too bad there isn&#x27;t a safe way to recycle them to other people who could use &#x27;em. Scary to think of the issues involved in that though.&lt;BR/&gt;&lt;BR/&gt;Um, forgive me for this? But -- tag -- you are it. A meme. Remember those? From the early days of blogging? Yep. Still around. This one is called &lt;BR/&gt;&lt;A HREF+ HREF=&quot;&quot; HTTP://THELAUNDRESS.BLOGSPOT.COM/2008/01/TAGGED-BY-NORMA-AND-PASSED-ON-TO-YOU-OR.HTML REL=&quot;nofollow&quot;&gt;7 weird/random things about me&lt;/A&gt;. Hoping you will give it a go? &lt;BR/&gt;Love, &lt;BR/&gt;tlThe Laundresshttp://www.blogger.com/profile/076</pre>

右文（仅阅读辅助）：

<pre>98451766032897477noreply@blogger.comtag:blogger.com,1999:blog-7675087351939177300.post-69410388097646800102008-</pre>

### 位置4479190｜high_activation｜z=0.4494603

上下文4377，目标offset=935，目标token="8"；原文档未知。

包含目标的模型可见前文：

<pre> keeping you overweight... your first weapon is learning what they are and how they do that.

2. Carbohydrate cravings are your biggest enemy. Your second secret weapon is the plan we will show you to overcome these cravings!

If you want to know exactly how to make this happen in the next five days then just click my link below... it&#x27;s all in my free book.

But let&#x27;s get on with the article:

Here&#x27;s a question you might be asking: &quot;How come after a diet, I just seem to put all the weight back on again? The sad reality of our times is that if you are chronically overweight, then its almost certain that you are on the North American diet most typified by the McDonald&#x27;s fast food meal... maybe &quot;low in fat&quot; these days, but bursting at the seams with highly processed carbohydrates and sugars.

Doesn&#x27;t matter if it&#x27;s a fish burger or a lean chicken burger... it&#x27;s the fries, the buns the desserts and the drinks that are doing you in! This doesn&#x27;t make you a bad person... it just means that, like the rest of us, you have been suckered in by the advertising.

Here&#x27;s why it&#x27;s so important for you to understand what&#x27;s happening to your body... the North American Diet has made your body insensitive to insulin and insulin is the key to successful weight loss and control of diabetes Type 2. This is how it happens and why it&#x27;s so bad:

When you eat, the food in your stomach gets converted into glucose that moves into your bloodstream. This is the food that your brain, your muscles and your tissues need in order to survive and grow.

When glucose enters your bloodstream, your pancreas responds by releasing insulin into your blood. Insulin is needed to allow the glucose to enter your cells. There, it is broken down to produce the energy needed for your cells to work properly.&lt;|im_end|&gt;tag:blogger.com,1999:blog-7675087351939177300.post5166892779408797469..comments2013-12-19T07:29:30.113-06:00Comments on Sutured for a Living: Unused and Old Medicationsrlbateshttp://www.blogger.com/profile/15236331355857884458noreply@blogger.comBlogger2125tag:blogger.com,1999:blog-7675087351939177300.post-38917394274437061202008-01-01T23:13:00.000-06:002008-01-01T23:13:00.000-06:00Hey there, I was horrified when I found out how an...Hey there, &lt;BR/&gt;&lt;BR/&gt;I was horrified when I found out how antidepressants are adversely affecting mussels and other bivalves. It just blew me away, never imagined this kind of effect. &lt;BR/&gt;&lt;BR/&gt;Glad you (and my HMO&#x27;s pharmacy) are spreading the word. My mom has a medicine cabinet full of Quaaludes and Dilaudid and other exciting products. I think dating 1970s forward. Just this weekend, talked her into creating a goody bag to be hauled off to the HMO. Returned. Too bad there isn&#x27;t a safe way to recycle them to other people who could use &#x27;em. Scary to think of the issues involved in that though.&lt;BR/&gt;&lt;BR/&gt;Um, forgive me for this? But -- tag -- you are it. A meme. Remember those? From the early days of blogging? Yep. Still around. This one is called &lt;BR/&gt;&lt;A HREF+ HREF=&quot;&quot; HTTP://THELAUNDRESS.BLOGSPOT.COM/2008/01/TAGGED-BY-NORMA-AND-PASSED-ON-TO-YOU-OR.HTML REL=&quot;nofollow&quot;&gt;7 weird/random things about me&lt;/A&gt;. Hoping you will give it a go? &lt;BR/&gt;Love, &lt;BR/&gt;tlThe Laundresshttp://www.blogger.com/profile/07698</pre>

右文（仅阅读辅助）：

<pre>451766032897477noreply@blogger.comtag:blogger.com,1999:blog-7675087351939177300.post-69410388097646800102008-01</pre>

### 位置4479470｜high_activation｜z=0.4533666

上下文4378，目标offset=191，目标token="7"；原文档未知。

包含目标的模型可见前文：

<pre>6:00.000-06:002008-01-01T20:46:00.000-06:00Never even thought about this! I always just toss ...Never even thought about this! I always just toss them! &lt;BR/&gt;&lt;BR/&gt;Granted, most of ours, we finish, but there are the cases where we start one, and for one reason or another can&#x27;t tolerate it or we switch antibiotics ...or whatever ... and wind up with the medications. &lt;BR/&gt;&lt;BR/&gt;Then there are the OTC ones, those DO get sitting around the house ... &lt;BR/&gt;&lt;BR/&gt;No one had ever said anything to me about disposal. I just threw them all in the trash. &lt;BR/&gt;&lt;BR/&gt;Eeeks ...guess I need to pay more attention ...Dreaming againhttp://www.blogger.com/profile/157</pre>

右文（仅阅读辅助）：

<pre>17590226520457326noreply@blogger.com&lt;|im_end|&gt;Take the tour ×

Specific thoughts on character Leitmotifs.

For those who are confused, a Leitmotif is a usually simple piece of music used to represent a character, and is often played to signify that it&#x27;s, well, them! For example movies and</pre>

### 位置6048474｜random｜z=0.01305896

上下文5911，目标offset=778，目标token=" and"；原文档未知。

包含目标的模型可见前文：

<pre> &gt;&gt; hagel will be the third republican secretary of defense appointed by the last two democratic presidents. william cohen, and bob gates, re-appointed by president obama in 2009. and chuck hagel is a republican senator from nebraska. th

-- does hillary clinton and the obama administration view the libya intervention as a success? how much did they view that intervention as what precipitated the set of effects afterwards? &gt;&gt; militarily the intervention by nato in libya was clearly judged widely as a success. it forced gadhafi out of power and it changed a state that had been among the most draconian in its practices at all levels into something that opened up hope for six and a half million people. the problem is the united states has never been very good, whether it&#x27;s in afghanistan, iraq, in creating an alternative and the bol line is the united states basically walked away when it came to how do you create a new state, how do you facilitate the diverse forces, whether it&#x27;s the tribal elements, more than 300 militias that had formed during that brief eight-month involvement, how do you stem the flow of weaponry and create an alternative. if you saw charlie wilson&#x27;s war, at the very ending of the movie when he says i raised all this money, billions of dollars for arms to the opposition to fight off the soviets but i co

in mali and what they are doing there. is this worrying the obama administration? is there support for this? &gt;&gt; well, obviously the united states is providing refueling facilities for the french warplanes so, yes, the united states is playing a role already. i think there are no comfortable choices and that&#x27;s one of the realities across the region today, whether it&#x27;s in mali or syria, post revolution egypt and libya. the united states doesn&#x27;t have a grand strategy. it&#x27;s looking at each case individually. the reality is that with islamists taking over northern mali, which is larger than france, just that part of it, this then creates a greater threat throughout the region. and unfortunately the outside world dithered for way too long in trying to figure out a response and to the earlier point, the fact is the africans can&#x27;t do it themselves. there&#x27;s been talk for two decades about creating an africa rapid deployment force and they haven&#x27;t been able to bring it together, provide training, cohesion, command and control and as a result there is no local or regional alternative. &gt;&gt; afri

the obama administration is trying take a step further. the clinton administration privatized it in the processing. animals are slaughtered and then they go through another step where they are cut up and processed and packaged. in the processing, privatized system and we have done a lot of work showing how dangerous it is. now the obama administration wants to increase the program, especially for poultry. more than 200 birds a minute of being sent in slaughtered. that is not a misstatement. 200 birds a minute. there is no way there can be any inspection and these are immigrant workers doing extremely dangerous work. people sense that sliced, all sorts of horrible injuries. because of all of the contamination from salmonella, i can&#x27;t really eat chicken. dip the chicken into chemicals and not really originated with the clinton administration. &gt;&gt; i don&#x27;t know how much time we have. are there any questions? &gt;&gt; what is the mandate of the usda? and what will it take to fix the &gt;&gt; is basically an agency that the secretary has appointed by the president. and these companies had so muc

storms. &gt;&gt; the new york times reports the obama administration will tackle climate change this term by avoiding broad, far-reaching and birds through congress and</pre>

右文（仅阅读辅助）：

<pre> instead focusing on administrative actions. these include reducing power plant emissions, increasing the efficiency of home appliances, and reducing the federal government&#x27;s carbon footprint. although the white house is planning a campaign to build public support, environmentalist have been warned not to expect &quot;full-scale engagement&quot; what congress is preoccupied with other issues including gun control, immigration, and the federal budget. we&#x27;ll have more from president</pre>

### 位置6321276｜random｜z=0.02300769

上下文6178，目标offset=403，目标token="Popular"；原文档未知。

包含目标的模型可见前文：

<pre>One big problem is that Japan and the U.S. are not really safe havens. Their debt problems exceed those of Europe. Switzerland is not completely safe either. Its small central bank has been massively intervening in the currency markets, and will take a huge hit on hundreds of billions of soon-to-be deeply depreciated euros. The franc is going to suffer from that.

Assuming that nothing is done, and the euro does collapse, stock indexes, like the Dow Jones Industrial Average (DIA) and the S&amp;P 500 (SPY) will dramatically fall, as European banks sell off everything they own. The CAC, DAX and FTSE are likely to fall even more. The only good longer-term investment will be precious metals, especially gold (GLD) (IAU) (PHYS), as people lose faith in all fiat currencies.

Source: How Germany Can &#x27;Save&#x27; The Euro While Limiting Its Liability On Legacy Debt&lt;|im_end|&gt;Seeking Alpha
Seeking Alpha Portfolio App for iPad

There are a small group of dividend yielding stocks that are hidden from most income investors&#x27; radar. These are sparkling treasures that at first glance are all dross and concealed by an unconvincing patina. Looking below the surface, though, brings out some shining values for income investors. Best yet, these companies have management groups that go way beyond the norm to provide value to their shareholders.

To understand where to go hunting for these dividend treasures it first pays to understand how they are hiding. First I want to focus on how companies pay their dividends.

Regular Dividends

First up are regular dividends. These are awarded by the company&#x27;s board as a share of profits to reward their ownership. These are paid annually, semi-annually, quarterly and occasionally monthly. In short, regular dividends are fairly predictable. These dividends show up in stock screening information and are the basis of a company&#x27;s reported dividend yield.

For example, here is information on a few popular dividend issues:

Popular</pre>

右文（仅阅读辅助）：

<pre> Dividend-Paying Companies
ConAgra FoodsCAG$28.21$0.25Quarterly3.54%
3 M CompanyMMM$88.03$0.59Quarterly2.68%
Aflac, IncAFL$49.58$0.35Quarterly2.82%
Altria</pre>

### 位置8754216｜random｜z=0.06176502

上下文8556，目标offset=438，目标token="2"；原文档未知。

包含目标的模型可见前文：

<pre> detriment and it`s time to repaint it`s own house and repair the picket fence.Any Medico will tell you that unemployment leads to mental health problems.

    Alert moderator

  • halduell:

    11 Aug 2011 7:49:22am

    After reading thru the comments, I have one question: Why does almost no one mention the Pentagon budget that has drained the American treasury?
    I would like to like Obama. Like many around the world, three short years ago I dared to hope. But unless he can free himself from a captive presidency, what&#x27;s to like?
    Tell the generals no, Mr President/America. Or continue down the gurgler.

    Alert moderator

    • Jez:

      11 Aug 2011 2:38:28pm

      halduell - I am sure that Obama would like to, but given the immense power of the right wing media in the US coupled with a lot of weak-minded people, he needs to choose his battles carefully. Next term when he has nothing to lose, hopefully the pentagon will get a decent pruning.

      Alert moderator

  • S. Ritchie:

    11 Aug 2011 10:00:42am

    When talking about tax increases in USA remember: in that country, local governments as well as state governments charge incomer and sales taxes on residents. Not to menion &#x27;excise&#x27; taxes which are charged on goods you already own (more like an ownership tax). All of which residents must pay IN ADDITION to any federal taxes they owe. Yes, the federal USA government might &#x27;not think it is taking enough in tax&#x27; - but when ALL TAXES (LOCAL, STATE AND FEDERAL) are considered, it is possible USA citizens are &#x27;taxed out&#x27;. The USA needs microeconomic reform, particularly in labour markets. Then it will produce the Growth Dividend which will deliver a higher tax take generally without the need to raise tax rates.

    Alert moderator

  • Rick:

    11 Aug 2</pre>

右文（仅阅读辅助）：

<pre>011 12:36:10pm

    Obama is a victim of his own delusions. His professorial background seems to have led him to genuinely believe that common sense could lead to bipartisanship. However, the right wingers with whom he has sought to negotiate have never had any intention of being either realistic or civil. The disrespect shown to him by the</pre>

## Feature 516，h_V=0

### 位置370412｜random｜z=0.07935016

上下文361，目标offset=979，目标token=" as"；原文档未知。

包含目标的模型可见前文：

<pre> support compiling multiple files into a single assembly now, that&#x27;s not a good solution, because it would obviate the need for using IronPython over C# or VB.NET (well, unless all you know is Python).

Oh, and IronPython now works with ctypes... wow!


Journal: ScrewTurn: Great wiki system for ASP.NET/Server 2003

Journal by dedazo

I just had to share this.

Having had the experience of setting up and operating a MediaWiki site, I am very impressed with ScrewTurn. It doesn&#x27;t have all the bells and whistles, but it works extremely well. It&#x27;s open source and s extremely well-designed (which is always reassuring). I&#x27;ve been testing it internally at one of our client sites and so far it&#x27;s been nothing but goodness.

All of the other attempts at wiki software I&#x27;ve seen for ASP.NET have been a huge disappointment, but ScrewTurn simply rocks.

There&#x27;s nothing wrong with MediaWiki of course, and if you already have the Linux infrastructure to host it then it probably makes more sense to use it instead. But if you have mostly Windows Server boxes and you need a good wiki, then I definitely recommend this one. Very nice.


Journal: Obama Landslide? 2

Journal by dedazo

Since election night I&#x27;ve noticed that many stories about Barack Obama tend to characterize his victory as a &quot;landslide&quot;. I saw one just now on ABC News.

I&#x27;m truly happy Obama won. I&#x27;m truly happy McCain lost. While I consider myself a moderate conservative, the US needed change badly at this point in history, and I believe the election provided that.

But calling it a landslide is disingenuous to say the least. According to WP, Obama nailed 52.9% of the popular vote, while McCain got 45.7%. That&#x27;s not a landslide by any measure, in any election.

Now if people are referring to the electoral vote (365 vs 173), sure, that&#x27;s sort of a landslide, but it&#x27;s still disingenuous, because essentially the same group of people that are calling it a landslide were the ones bemoaning how broken the electoral system is in 2000 and 2004 when Bush won by way of Florida and Ohio.

I don&#x27;t know why, I just hate people who do that sort of thing. The same people who claimed that the 2004 election was &quot;stolen&quot; by the Republican party were strangely silent when the democrats kicked ass in the 2006 mid-terms. Apparently the GOP forgot to steal that one? And the same people who claimed Bush was going to do something evil to re-elect himself (remember the stories about troops being brought in to the US, the pending attack on Iran, the martial law, etc) were also strangely silent on 5 November.

I guess I just hate conspiracy theorists and agitator nuts. If you have to say something, make sure it has some backing in reality. Otherwise, please shut the fuck up.


Journal: It Sounds Like... Joe Satriani Files Suit Against Coldplay 7

Journal by dedazo

I&#x27;m sure some Slashdot users are fans of Joe Satriani (at least maybe those that are closer to my age). I&#x27;m sure a few more are also Coldplay fans. Well, it turns out Joe has filed a lawsuit claiming Chris Martin &amp; Co. lifted the riff from Satriani&#x27;s If I Could Fly piece from 2004 and made it into their Vival La Vida hit.

There&#x27;s a comparison up on YouTube and indeed, the opening riff from Satriani does match the Coldplay song. But I don&#x27;t think Coldplay was ripping anything or anyone off.

Many musicians (especially mainstream ones) inevitably tend to do things like these. They have influences, they listened to the same artists when they were coming up the ladder, etc. Sure, Kraftwerk didn&#x27;t sound like anyone else, and neither did Nine Inch Nails or any of those edgy groundbreaking acts. But Coldplay is the result of pop/rock evolution. It&#x27;s inevitable that they will sound like someone else at some point.

Joe Satriani&#x27;s music is part of the soundtrack to some of the best moments in my life. I hate it when my heroes do things like these. Is he not selling enough records now or what? I buy them all. C&#x27;mon Joe, that just sucks.


Journal: It&#x27;s time for 3000! 1

Journal by dedazo

A message in the python-committers marks the beginning of the new Python era: The 3.0 branch has been tagged in SVN and ready for a tarball drop. Installers and packages should be ready soon as</pre>

右文（仅阅读辅助）：

<pre> well.


First Person Shooters (Games)

Journal: So what are those sockpuppets good for again? 5

Journal by dedazo

From the oh-trollboy-you&#x27;re-so-busted dept.

</pre>

### 位置2714594｜random｜z=0.1195113

上下文2653，目标offset=31，目标token="1"；原文档未知。

包含目标的模型可见前文：

<pre>’s hope the current La Niña doesn’t linger much longer.


APRIL SHOWERS? Thu, 03 Apr 2008 1</pre>

右文（仅阅读辅助）：

<pre>3:05:27 +0000 Dale Nelson Forecasts Rain Last 7 Months 

This past month of March our temperatures were just barely above normal while our rainfall was promising the first half of the month but ended up slightly below normal. Overall, our temperature ended up 0.5 degrees above normal while ranging from 34 to 94. Rainfall was</pre>

### 位置4590246｜high_activation｜z=0.4083297

上下文4486，目标offset=465，目标token="2"；原文档未知。

包含目标的模型可见前文：

<pre> are conserved in pathogenic fungal genomes and can be absent from the non-pathogenic yeast Saccharomyces cerevisiae.

Candida albicans is a diploid organism with eight sets of homologous chromosomes and a genome size of about 32 Mb. This pathogen is part of the normal microflora of the human gastrointestinal tract or oropharynx and is responsible for various nosocomial infections, potentially lethal in immunocompromised patients or patients in the intensive care unit. The CA1462 protein is encoded by a gene conserved across all known fungal genomes. It shares 36% sequence identity with Saccharomyces cerevisiae YOR143C [2], a Thiamine pyrophosphokinase (TPK, EC essential for fungus growth and survival [3]. This enzyme is also essential in S. pombe [4]. The production of thiamine pyrophosphate (TPP), catalyzed by TPK, is critical for both catabolic and anabolic cellular processes. In vertebrates, a deficiency in thiamine synthesis is linked to neurological diseases such as beriberi and Wernicke encephalopathy [5]. In all synthesizing organisms, thiamine (vitamin B1) is produced from phosphorylated HET (4-methyl-5-(β-hydroxymethyl)thiazole) and HMP (2-methyl-4-amino-5-hydroxymethyl-pyrimidine) that are condensed into thiamine phosphate. In yeast, this thiamine phosphate is then hydrolyzed into thiamine before pyrophosphorylation by the TPK that catalyzes the transfer of a pyrophosphate (PPi) from ATP to thiamine, resulting in AMP and TPP [6].

This article reports the enzymatic characterization as well as the structure determination of the Candida albicans CA1462 Thiamine pyrophosphokinase in complex with both thiamine and thiamine-PNP (TPNP). We also present a comparison of CA1462 with the structure of the mouse TPK ternary complex with pyrithiamine pyrophosphate and AMP (PDB id 2</pre>

右文（仅阅读辅助）：

<pre>F17) [7], with the TPK S. cerevisiae structure (PDB id 1IG0) [8] and with sequences from other species.


General cloning strategy

The cDNAs corresponding to the TPK genes were amplified by PCR from their respective genomic DNAs (CA1462: Candida albicans strain NIH 3147 ATCC</pre>

### 位置4597119｜high_activation｜z=0.4102828

上下文4493，目标offset=170，目标token="2"；原文档未知。

包含目标的模型可见前文：

<pre> molecule (O3). In the AMP-PNP molecule, a nitrogen atom (N3) replaces O3. While we did not get crystals of the TPK/Thiamine/AMP-CPP complex, the TPK incubated with thiamine and AMP-PNP produced usable crystals. However, the structure revealed that instead of a TPK/Thiamine/AMP-PNP complex, we obtained an unexpected TPK/thiamine-PNP complex with a TPNP molecule in the enzyme binding site (Figure 3D). This result is consistent with the earlier suggestion that the pyrophosphate group is transferred at once from the ATP molecule to the thiamine moiety.

The superimposition of the C. albicans TPK/TPNP complex onto the mouse TPK/TPP complex (PDB id 2</pre>

右文（仅阅读辅助）：

<pre>F17) highlights few differences between the two thiamine phosphate ends. The nitrogen N3 in the TPNP molecule is symmetrically opposed to its equivalent oxygen O3 in the TPP molecule. It is stabilized by a weak electrostatic interaction (3.28 Å) with the S301B γ-oxygen in the C. albicans TPK/TPNP complex (</pre>

### 位置4600185｜high_activation｜z=0.4317672

上下文4496，目标offset=164，目标token="2"；原文档未知。

包含目标的模型可见前文：

<pre>: 6-Hydroxymethyl-7, 8-dihydropterin pyrophosphokinase; LIC: ligation-independent cloning; NCS: Non Crystallographic Symmetry.

Authors&#x27; contributions

SS performed research, analyzed data and wrote the paper. VM, NM and TR designed research and contributed to new reagents/analytic tools. CS: performed research. J–MC: designed research and wrote the paper. CA designed research, performed research, analyzed data and wrote the paper. All authors read and approved the final manuscript.


The atomic coordinates and structure factors for the crystal structures of the thiamine pyrophosphokinase from Candida albicans in complex with thiamine or thiamine-PNP are available in the RCSB Protein Data Bank under PDB id 2</pre>

右文（仅阅读辅助）：

<pre>HH9 and 2G9Z respectively.


The PROFUN project was supported by a grant from the French ministry of research and education (N° 02 L 0194) and by Centre National de la Recherche Scientifique (CNRS). We acknowledge the use of the Marseille-Nice Génopole bioinformatic platform, the IBSM proteomic platform and</pre>

### 位置5872170｜random｜z=0.05188434

上下文5739，目标offset=422，目标token="ly"；原文档未知。

包含目标的模型可见前文：

<pre>.com - Relevant reviews by real people.
This is you!
Ranked #
Last login
Member since&lt;|im_end|&gt;Mind of
Mae Brussell
Is &quot;The Queen of Conspiracy&quot;
going to break the JFK case
wide open, or is she just a
paranoid housewife who likes
to clip newspapers?

by Paul Krassner

(from OUI magazine, May 1978)

&quot;Nothing just happens in politics. If something happens
you can be sure it was planned that way.&quot;

—Franklin D. Roosevelt

    There she is, the Bionic Researcher. Every day she feeds herself ten newspapers from around the country. This diet is supplemented with items sent to her by a network of conspiracy students. She also consumes magazines, underground papers, unpublished manuscripts, court affidavits, documents from the National Archives, FBI and CIA materials obtained through the Freedom of Information Act and hundreds of books on espionage and assassination. &quot;About 80 percent of all CIA intelligence information comes from printed news,&quot; she says, &quot;so I am doing what they are doing but I&#x27;m using all the material.&quot; Each Sunday, she sorts out the week&#x27;s clippings into various categories as though she were conducting a symphony of horror. Yet she is cheerful. She almost sways in counterpoint to the rhythms of hypocrisy. For, while there are those who try to discredit her by saying she&#x27;s crazy, Mae Brussell remains high on her responsibility.
    Mae has been our nation&#x27;s number-one, self-appointed conspiracy freak since the day Jack Ruby shot Lee Harvey Oswald. She has written hundreds of articles detailing the unpleasant connections between what most people consider diverse chapters in American history—like Oswald and Francis Gary Powers, the Kennedy murders and Watergate. For the past seven years, the house-wife-turned-crusader has shocked and dismayed listeners of her syndicated radio program, Dialogue: Conspiracy (KLRB-FM, Carmel, California), uncovering choice tidbits about everything from Chappaquiddick to Chowchilla. She unabashedly</pre>

右文（仅阅读辅助）：

<pre> calls herself the country&#x27;s best researcher.
     It would be difficult to question that she knows as much as anyone about people involved in &quot;The Assassinations.&quot; The Queen of Conspiracy is currently writing five separate books on what happened that day in Dallas, all of which, she claims, &quot;contain entirely new material. Collectively, these books will finally answer the question: Who killed JFK?&quot;
    At</pre>

### 位置6144492｜random｜z=0.03564899

上下文6005，目标offset=607，目标token=" don"；原文档未知。

包含目标的模型可见前文：

<pre> the following:

  • An external serial modem. This type of modem connects to the computer&#x27;s serial port (called COM1 or COM2 under DOS). No special driver is needed to operate this type of modem, so compatibility with Knoppix is excellent. For example, the “Sitecom External V92 Serial Modem” works perfectly.
  • A PCMCIA Cardbus modem. A PCMCIA Cardbus modem is effectively an external serial modem. In general, the cheaper the card, the better. For example, the “Sitecom 56Kbps Fax Modem PC Card” works perfectly with Knoppix.
  • An internal ISA modem. Like the external modem, this type of modem needs no special driver to make it work. That is why old ISA modems are useful.

There are two main ways to make a dial-up connection. The recommended way is to use “K Point to Point Protocol” (KPPP). The alternative, in case KPPP doesn&#x27;t work, is the “Worldvisions Dialer” (WVDial).

Connecting using KPPP[edit]

  1. Click the Knoppix menu in the lower left corner.
  2. Point to “Network/Internet”.
  3. Click “Modem Dialer”.
  4. The “KDE Point-To-Point Protocol” (KPPP) program will start.
  5. Click “Setup”.
  6. Click the “Device” tab.
  7. If your modem is plugged into the serial port called “COM1” in Windows, set “Modem device” to /dev/ttyS0. If it is plugged into the port called “COM2” in Windows, select /dev/ttyS1. If you have a PCMCIA Cardbus modem, select /dev/modem. If you have an internal ISA modem, select /dev/ttyS0 first; if that doesn&#x27;t work, try up to /dev/ttyS3.
  8. Click the “Modem” tab.
  9. Click “Query modem”.
  10. You should see a response from the modem. If not, go back to step 7 and try another modem device setting.
  11. Click the “Accounts” tab.
  12. Click “New”.
  13. Click “Dialog setup”.
  14. In “Connection name” enter a name for the connection eg “test”.
  15. Beside “Phone number”, click “Add”.
  16. Enter your Internet Service Provider&#x27;s dial-up access number. If you don&#x27;t know, ask your Internet Service Provider. Click OK.
  17. Click OK. This will take you back to the accounts screen.
  18. Click OK again.
  19. Enter your login ID and password. Again, if you don</pre>

右文（仅阅读辅助）：

<pre>&#x27;t know what they are, ask your Internet Service Provider.
  20. Click Connect.
  21. You should hear the modem work.
  22. In a few moments, the KPPP window should shrink down to the Taskbar. It should then read “00:00” on the Taskbar. This indicates your time online in hours and minutes.</pre>

### 位置9298268｜random｜z=0.06696002

上下文9088，目标offset=156，目标token=","；原文档未知。

包含目标的模型可见前文：

<pre>. Tattersall was reminding me that about 30 years ago, archeologists had found lots of pollen grains in an Iraqi Neandertal burial. They were probably from flowers being placed into the grave, which, again, may be some sort of an inkling of awareness, a manifestation of the human spirit.

sum 98 cover

Summer 1998

Vol. 51:3&lt;|im_end|&gt;Saturday, May 20, 2006


Friday Movie Review (late)

Went to see The Da Vinci Code. It was ultimately silly, not that convincing and too confused with non-threatening conspiratorial elements that went nowhere to be satisfying in the whole. It&#x27;s about the Grail, the Holy Grrrrrrail,</pre>

右文（仅阅读辅助）：

<pre> as Cleese pronounces it. Spoiler coming. Mary Magdalene was married to Jesus and had a child whose bloodline down to the present has been the source of a war between part of the hierarchy of the Catholic Church, which wants to keep that part of the story a secret, and the Templars who have pledged to defend the Wife of God and her tomb and progeny (actually</pre>

## Feature 937，h_V=5

### 位置823072｜random｜z=0.2599892

上下文804，目标offset=401，目标token=" t"；原文档未知。

包含目标的模型可见前文：

<pre> up at the most banal moments. A freezing day can involuntarily lead to imagining how cold the prisoners of Auschwitz were. Perhaps you have to be Jewish. I hope not.

The number of years that have elapsed since the Second World War is clearly a factor. Even Jefferies might hesitate before telling, say, a Rwanda tourist board joke about cutlery.

But Boll is not talking about the people who live with the images of the Holocaust. He is talking about the kind of audience inured to violence by its centrality in so many video games; the kind of entertainment that he himself has turned into film.

Perhaps his film is a bid to be taken seriously. Or perhaps it is the most cynical exploitation of the Holocaust yet seen, exclusively attracting the kind of audience that gets its kicks from torture porn flicks.

Perhaps. But Boll has raised a very thorny question: how do you get the violent-video-game generation to understand the Holocaust? Please God, not by taking the next, coldly logical step - a Holocaust video game.

John Nathan is the JC&#x27;s theatre critic

    Last updated: 10:24am, November 19 2010&lt;|im_end|&gt;The Emigrants: Coming to America Full of Hope, Hunger, Disappointment and Impatience 


The Emigrants (1971)
Directed by Jan Troell
December 5 at BAM, part of its Max von Sydow series

Cinephiles entering into this expecting a sweeping 19th-century epic in which hugs are delicately framed in front of bombastic cannonfire will be sorely mistaken—but never, ever disappointed. The history-obsessed Troell is a peerless termite artist; his film rigorously traces the path of Swedish peasant Karl Oskar (Max Von Sydow), his wife Kristina (Liv Ullman), and their extended family. The Nilssons have rotten luck; despite dogged persistence t</pre>

右文（仅阅读辅助）：

<pre>ending the soil, their animals—and eventually one of the couple’s children—freeze to death. Karl Oscar is a man of the land, but no simpleton: rather than the shoot-for-the-moon naivete that we drape over old-time immigrant parables today, his choice to take the family to America is driven less by foolish optimism than outright despair. Barely scraping by</pre>

### 位置1687573｜random｜z=0.2678017

上下文1649，目标offset=292，目标token=" t"；原文档未知。

包含目标的模型可见前文：

<pre>, and some of them injured, and two had just been felled by bricks. The fire from the sniper was part and parcel of the situation.


The privilege of employing deadly force to subdue a riot was not made inapplicable by the fact that in his opening statement and in argument before the trial court counsel for the MHP defendants stated that his clients did not rely upon the justification of quelling a riot, or by the fact that in testimony no MHP officer characterized his firing in riot-suppression terms. The testimony of each officer, describing his action in terms of defense against sniper fire or of pinning down the sniper, or both, did not eliminate the jury&#x27;s right to recognize the sniper fire as a particularized aspect of the riot, indeed at the moment perhaps its most inflammatory and most dangerous aspect, and conclude that in firing responsively the officers were quelling the sniper fire and dissuading others from joining in.8


Under the facts of this case the privilege of self defense and the privilege of use of deadly force relating to a riot partially overlap. As we have held, a jury could conclude that a riot was in progress,9 that it threatened death or serious bodily harm, and that the sniper was part and parcel of the situation. A jury could consider whether fire directed at the sniper for defensive purposes was within the contours of fire tending to quell the riot in general or the sniper as a particular part thereof or t</pre>

右文（仅阅读辅助）：

<pre>ending to dissuade others from joining in the riot in any manner. A jury could also consider whether fire to quell the riot (or the sniper as an element thereof) or to dissuade others from joining in the riot was delivered in such a manner as to be within the contours of fire for self defense.


Inquiry must then turn to the allowable scope of permitted deadly force and the</pre>

### 位置2431541｜high_activation｜z=0.3205361

上下文2376，目标offset=460，目标token=" t"；原文档未知。

包含目标的模型可见前文：

<pre> to anyone tightly or loosely employed by the New Zealand Rugby Union, as TV commentator Murray Mexted found a couple of years ago.

As Muzza might say, the psychic energy isn&#x27;t with rugby any more. For every stirring Taranaki v Canterbury contest, there is a swag of dross played before empty seats and hearts.

I have no complex answer to the rugby malaise, beyond stating another obvious, that if a culling of teams would improve the situation, the blade should start its sweep at North Harbour. Auckland has enough trouble fielding one decent team these days, let alone two.

What is interesting about the Cowan situation is that it drew Tew, the NZRU chief executive, out of his bunker, and some of his language was revealing.

What on earth has happened to the dear old focus group, I wondered, when Tew turned to the feedback he was getting &quot;from the people I mix with&quot;.

My experience as a rugby journalist left the impression that people Tew mixed with might be inclined to tell him what they thought he wanted to hear. As both off-the-record conversations with rugby luminaries and the Mexted debacle indicated, merely questioning the NZRU is not regarded as an overly profitable exercise.

From his extensive study, Tew felt that people liked the &quot;convenience&quot; of watching rugby midweek, as if sport was on a par with doing the grocery shopping.

This is why none of rugby&#x27;s competitions really work. They are all a convenience, not for the public, but the alliance between the unions and broadcasters.

No one tried to design a ripping good competition, and then tried to make it work. Professional rugby started off as a last-ditch campaign to ward off an invader, and has never got ahead of the game. The game itself has become bogged down, often, in technical rulings and inadequate skills for the torrid task.

Tew&#x27;s assertion that the ITM Cup promotion relegation system &quot;retained interest&quot; is a load of old cobblers. Hardly anyone gives a stuff about it, and thanks to the constant format changes, hardly anyone even knows how it works. The good people of Napier or wherever do not break down in tears when their teams drop from the glorious premiership into the t</pre>

右文（仅阅读辅助）：

<pre>errors of the championship division.

Super 15 rugby is also a contrived competition, designed to get the maximum dollar out of the broadcaster. A lot of people struggle to remember who won it from year to year. Even the World Cup has been a contrivance, where the IRB treated teams such as the Pacific Island countries with contempt, in order to satisfy the most affluent audiences and -</pre>

### 位置2529626｜random｜z=0.2443642

上下文2472，目标offset=315，目标token=" t"；原文档未知。

包含目标的模型可见前文：

<pre>
Do Cad&#x27;s angreal stop channeling. I thought they just told her when a man was using the power?


Of course her tactics up until now ended with gentling the male channeler. She probably should have taken that into consideration this time round.

47. TAmyrlinring1
Treesinger @44 I forgot that! Setalle said something to Mat when she looked at his ter&#x27;angreal about Cadsuane being rumored to have one that disrupted weaves. Ahhh--have to go find that now and see if she said anything about saidar versus saidin or anything. Does anyone remember if anyone has channeled saidin at Mat yet? I don&#x27;t think so . . . and that would leave it still an open question of whether he&#x27;s still vulnerable to saidin. I had never even thought of that being a possibility as to why Cadsuane was so daring with Rand.
48. TAmyrlinring1
Mis @46 That probably would have been a good thing to consider. Of course, she wouldn&#x27;t have been so memorable a character had she done so ;-)
Maggie M
49. Eswana
I go back and forth about Cadsuane. She&#x27;s annoying as hell. She&#x27;s arrogant and conceited. She&#x27;s disrespectful and disdainful of EVERYONE.

and yet..... she&#x27;s kind of awesome. And right A LOT. And though her bedside manner leaves a lot to be desired, she is right about Rand, as we&#x27;ll discover in t</pre>

右文（仅阅读辅助）：

<pre>GS.

I&#x27;m also intrigued by how everyone seems to be so divided over her. That&#x27;s the mark of good character development. She&#x27;s complex. Not universally loved or hated. Just like real life. Well done!
50. birgit

She is very strong.

A voice Moiraine had heard only once, two years ago, and would never forget. A number of women were stronger</pre>

### 位置2615965｜high_activation｜z=0.3361611

上下文2556，目标offset=652，目标token=" t"；原文档未知。

包含目标的模型可见前文：

<pre>: 63
    Ratings: +0 / 0
    june and july and south west washington and thanks for all the suggestions!
  2. Chap310 New Member

    Posts: 5
    Fort Collins,Colorado
    Ratings: +0 / 0
    Stillwater nymphs are good trolling flies,especially if there are scuds/damsels active.
  3. ryfly Addicted to flyfishing

    Posts: 260
    Snoqualmie, WA
    Ratings: +12 / 0
    soft hackles too
  4. ribka Active Member

    Posts: 1,403
    E WA
    Ratings: +157 / 0
    Black micro leech size 12 with red bead head or soft hackle midge or PT in a size 16
  5. CovingtonFly B.O.H.I.C.A. bend over here it comes again

    Posts: 586
    Covington, Wa
    Ratings: +0 / 0
    Olive willy and a dragonfly nymph
  6. Fast Action Freddie Member

    Posts: 127
    Seattle, WA
    Ratings: +0 / 0
    Now I&#x27;ve had luck with Spruce Fly - especially in mountain lakes. Why the hell does it work? Is it imitating anything? or just flashy?

    Does anyone use them in desert lakes? okanogan lakes?
  7. Jim Wallace Smells like low tide

    Posts: 5,560
    Somewhere on the Coast
    Ratings: +484 / 0
    Now, I&#x27;m just supposin, here, having fished &#x27;em:
    The fly was originated on the Oregon coast for the purpose of fooling searun cutthroat. The wing looks like a small forage fish from a distance. Then up close you have the naturally iridescent peacock herl and the red that cutts like so much. So I&#x27;d say its a combo forage-fish/attractor pattern.
  8. Michael Nelson Old And In The Way

    Posts: 250
    San Francisco, CA, USA
    Ratings: +0 / 0
    Whatever fly you troll with, strip it in every few minutes to make sure you&#x27;re not trolling with salad.
  9. Gary Dills 3 weight to 10 weight

    Posts: 42
    Sequim, WA
    Ratings: +0 / 0
    Ditto the trailers. I&#x27;ve often trailed a chronomid 16 or smaller and caught more fish. Wind and some chop on the water can be as advantageous as the twitching.
  10. Jim Wallace Smells like low tide

    Posts: 5,560
    Somewhere on the Coast
    Ratings: +484 / 0
    I can usually sense the slight increase in drag, but not always.

    I will admit to having t</pre>

右文（仅阅读辅助）：

<pre>rolled on for a good 20 minutes once after getting a hard grab, before the little lightbulb flashed on and I stripped in to discover that my fly was gone! I think I did that another time, too, before I finally learned to always check to see if its still there if I don&#x27;t get another hit right away.&lt;|im_end|&gt;NFR WA state liquor tax and 2 bottles</pre>

### 位置2695848｜high_activation｜z=0.3303017

上下文2634，目标offset=729，目标token=" t"；原文档未知。

包含目标的模型可见前文：

<pre> ships foundation (yet that worne) Remaind a trophey in that mighty fray; Nothing at all aboue the head remained, Either for couert, or that force maintained.

Powder for shot, was spent and wasted cleane, Scarce seene a corne to charge a peece withall, All her pykes broken, halfe of his best men slaine, The rest sore wounded, on Deaths Agents call, On th’other side, her foe in ranks remains, Displaying multitudes, and store of all What euer might auaile for victorie, Had they not wanted harts true valiancie.

When Grinuile saw his desperate drierie case, Meerely dispoyled of all success-full thought, Hee calls before him all within the place, The Maister, Maister-gunner, and them taught Rules of true hardiment to purchase grace; Showes them the end their trauailes toile had bought, How sweet it is, swift Fame to ouer-goe, How vile to diue in captiue ouerthrow.

Gallants (he saith) since three a clock last noone, Vntill this morning, fifteene howers by course, We haue maintaind stoute warre, and still vndoone Our foes assaults, and driue them to the worse, Fifteene Armados boardings haue not wonne Content or ease, but beene repeld by force, Eight hundred Cannon shot against her side, Haue not our harts in coward colours died.

Not fifteene thousand men araungd in fight, And fifteene howers lent them to atchiue, With fifty three great ships of boundlesse might, Haue had or meanes or prowesse to contriue The fall of one, which mayden vertue dight, Kept in despight of Spanish force aliue. Then list to mee you imps of memorie, Borne to assume to immortalitie.

Sith loosing, we vnlost keepe strong our praise, And make our glories, gaynours by our ends, Let not the hope of howers (for tedious dayes Vnto our lines no longer circuite lends) Confound our wondred actions and assayes, Whereon the sweete of mortal eares depends, But as we liue by wills victorious, So let vs die victours of them and vs.

Wee that haue mercilesse cut Mercies wings, And muffeld pittie in deaths mistie vale, Let vs implore no mercie; pittyings, But from our God, deere fauour to exhale Our soules to heauen, where all the Angells rings Renowne of vs, and our deepe tragick tale; Let us that cannot liue, yet liue to dye, Vnthrald by men, fit tropheys for the skye.

And thus resolu’d since other meane is reft, Sweet Maister-gunner, split our keele in twaine, We cannot liue, whom hope of life hath left, Dying, our deaths more glorious liues retain, Let not our ship, of shame and foile bereft, Vnto our foe-men for a prize remaine; Sinke her, and sinking with the Greeke wee’le cry, Best not to be, or beeing soone to dye.

Scarce had his words t</pre>

右文（仅阅读辅助）：

<pre>ane wings from his deere tong, But the stout Maister-gunner, euer rich In heauenlie valure and repulsing wrong, Proud that his hands by action might inritch His name and nation with a worthie song, Tow’rd his hart higher then Eagles pitch, And instantlie indeuours to effect Grinuils desier, by ending Deaths defect.

</pre>

### 位置10147486｜random｜z=0.2834267

上下文9918，目标offset=224，目标token=" t"；原文档未知。

包含目标的模型可见前文：

<pre>.

Hey!  It&#x27;s time for a double dose of Fun with Out of Context Dialogue!(tm)!

First, from Amazing Spider-Man #152: 

Any time you use the term &quot;manhole shaft,&quot; odds are pretty high it&#x27;s going to be some Fun with Out of Context Dialogue. (tm!)

And from Amazing #153:

I always preferred Mary Jane to Gwen Stacy.  I think this explains why.

See you tomorrow!


MarvelX42 said...

I was just gonna bring up the ol Spider sense. Has anyone ever really nailed down what it is, what it does, what makes it go off? I mean I know &quot;danger&quot; but like how does a &quot;sense&quot; define danger and how does it know, etc?

Justin Garrett Blum said...

I confess that I&#x27;ve never given Spider Sense too much thought, but my impression was always that it was a kind of informed precognition, if that makes any sense. Essentially, very acute situational awareness.

If that&#x27;s the case, it&#x27;s not really surprising that he might have gotten a t</pre>

右文（仅阅读辅助）：

<pre>ingle about somebody being in his apartment.&lt;|im_end|&gt;CRS in Nicaragua

Not Just About the Coffee

By Robyn Fieser

The most difficult thing for the women of this hilly northern Nicaraguan town was not organizing into an all-female cooperative. It wasn&#x27;t ridding themselves of the low-paying middlemen or signing a deal to export their coffee beans to a U.S. ro</pre>

### 位置10366647｜random｜z=0.02170794

上下文10132，目标offset=392，目标token="t"；原文档未知。

包含目标的模型可见前文：

<pre> pond. Is the city setting a land-use precedent?

2)five topped significant trees next to a busy roadway demonstrates everyday to passersby the city is disrespectful of these trees and educates citizens and youth that topping trees on their property is an okay thing to do.

3) Mr. Myers alluded to them as being ugly. My readers agree, though most citizens have no voice on the matter or don&#x27;t know how or to whom to send feedback to the city.

4) I&#x27;ve been observing this pond habitat since 2009. Little wildlife activity on the trees was observed before and after the topping. Do you inventory wildlife species on your renovated stormwater ponds?

5) &quot;Snag&quot; wildlife activity: I can&#x27;t count the insects, but it&#x27;s obvious there&#x27;s no nesting of buteos, waders or P. Woodpeckers. Foraging of woodpeckers, sapsuckers, nuthatches, brown creepers are rarely if ever observed. Evidence of foraging is modest for the amount of top-tree habitat.

Planner Kelsey says planting new shrubs is planned over in two years. Mr. Myers says enhancements will begin in the summer. I respectfully request you remove four &#x27;snags&#x27; to stump, in the process creating log habitat. Log decay may be more rapid in the water, providing shelter, food and protection for the known waterfowl, ​amphibians, and reptiles living in your pond.

Hopefully, input from other citizens and the Mayor will further encourage you to take action. Please let me know if you&#x27;d like additional information.

Thank you.

Bob Yoder said...

I think the city cut the tallest topped tree to the same level s the others. It looks better, more uniform.&lt;|im_end|&gt;Install Theme


rodmanstreet: girl genius

streets ahead
Jul 29 &#x27;12

Afraid to buy an Obama ‘12 t</pre>

右文（仅阅读辅助）：

<pre>-shirt lest it end up alongside my Kerry ‘04 t-shirt to be worn ironically five years later.

  1. glossylalia said:Don’t even care. If Mitt wins, I will wear every Obama item I can find so people know about how WRONG they are for the next 4 years.
  2. rodmanstreet posted this&lt;|im_end|&gt;Roker Ramble: Quick</pre>

## Feature 1821，h_V=1

### 位置98185｜random｜z=0.02924235

上下文95，目标offset=967，目标token=".["；原文档未知。

包含目标的模型可见前文：

<pre> Animus provided advanced weaponry and costumes in a plan to regather the Sons of the Serpent to spread hatred and violence throughout New York City, coming into conflict with the Avengers and the New Warriors. It also targeted Nomad (Jack Monroe).[volume &amp; issue needed]


Annalee is a mutant in the Marvel Universe.

The character, created by Louise Simonson and June Brigman, first appeared in Power Pack #12 (1985).

Within the context of the stories, Annalee is a member of the subterranean mutants known as the Morlocks, Annalee&#x27;s own four children were slain and this caused her to force the four original members of Power Pack to become her foster children. Her repeated attempts failed (the latter attempt was foiled when Katie Power escaped and sought the aid of the X-Men),[54] but she later found happiness caring for the young Morlock known as Leech.[volume &amp; issue needed] Annalee later was slain by the Marauders&#x27; member called Scalphunter during the Mutant Massacre.[55]

Annalee in other media[edit]

Annalee appeared in the X-Men episode &quot;Captive Hearts&quot;, voiced by Kay Tremblay. She seemed to have a greater control over her powers, causing the X-Men, including Jean Grey, to experience any state of mind she chose to place them in, from Wolverine believing himself to be covered with scorpions, to Jean believing herself to be a young child and Annalee her mother.


Anubis is a member of the Heliopolitans in the Marvel Universe. The character, created by John Warner and P. Craig Russell, first appeared in Son of Satan #5 (August 1976).

Within the context of the stories, Anubis clashes with Daimon Hellstrom, the &quot;Son of Satan&quot;.[volume &amp; issue needed] N&#x27;Kantu, the Living Mummy agrees to become Anubis&#x27; agent to kill people and send their souls to him in exchange for N&#x27;Kantu moving on to the afterlife.[56]


Ape is a fictional mutant character in the Marvel Comics Universe. His first appearance was in Power Pack #12 (July 1985), and he was created by Louise Simonson and June Brigman.

The character subsequently appears in The Uncanny X-Men #195 (July 1985), Power Pack #27 (December 1986), X-Factor #11-13 (December 1986-February 1987), and Weapon X vol. 2 #5 (March 2003) and #10 (August 2003).

Ape was a member of the Morlocks who was amongst those that escaped the Marauders&#x27; slaughter during the &quot;Mutant Massacre&quot;.[volume &amp; issue needed] He lived with the mutant team X-Factor after the massacre.[volume &amp; issue needed] Ape was later captured by the subversive Weapon X program and incarcerated in the &quot;Neverland&quot; concentration camp, where he was among the first mutants to be executed.[57]

Ape appeared as part of the &quot;Morlocks&quot; entry in the Official Handbook of the Marvel Universe Deluxe Edition #9.

Ape in other media[edit]

  • Ape appears in the X-Men episode &quot;Captive Hearts&quot; voiced by Ross Petty. He is among the featured Morlocks that fight the X-Men. In the next episode, &quot;Have Yourself a Morlock Little X-Mas&quot;, he steals medical equipment for Leech. His last appearance was in the episode &quot;Secrets Not Long Buried&quot; Ape is one of the many residents of the mutant-dominated community of Skull Mesa. He is drawn twice in the scene where Cyclops walks through Skull Mesa alone.


Ape-X is a super intelligent ape in the Squadron Supreme universe. The character, created by Mark Gruenwald, first appeared in Squadron Supreme #5 in January 1986. Within the context of the stories, Ape-X was a member of the Institute of Evil[58] before joining the Squadron. She later fell into a coma.[59]

An unrelated Ape-X, created by Karl Kesel and Ramon Bachs, appeared in Marvel Apes #1.


Aquon is a supervillain in the Marvel Universe. The character, created by Steve Englehart and Herb Trimpe, first appeared in Hulk #165 (July 1973).

Within the context of the stories, Aquon is a foe of the Hulk.[</pre>

右文（仅阅读辅助）：

<pre>60] He is servant to Captain Omen.

While serving Captain Omen he assists the Infra-Worlders in their attempt to rule the underwater world. To suppress a revolution led by his son Filius, Captain Omen releases Aquon to force the rebellion into</pre>

### 位置127933｜random｜z=0.00897868

上下文124，目标offset=1022，目标token="."；原文档未知。

包含目标的模型可见前文：

<pre> saying Vanir and elves may be assimilated.
  39. ^ &quot;other divine types are mentioned such as the Elves (ON alfar)..but no important or even specifically named gods are found..&quot; Dumézil, Georges (1973). Gods of the Ancient Northmen. University of California Press. p. 3. ISBN 0520020448. 
  40. ^ Hall 2004, pp. 46-
  41. ^ Hahn, Werner. Saemunds Edda: Lieder germanischer Göttersage. p. 270.  points out that the dwarf Alvis&#x27;s poem only names 6 worlds, but worlds of 11 beings are named by various poems.
  42. ^ a palace, like Valaskjálf mentioned in the adjacent stanza. See Grimnir&#x27;s sayings 5.3 (Larrington 1996, p. 52), and &quot;Annotated Index of Names&quot;.
  43. ^ Sturluson, Snorri. The Younger (or Prose) Edda, Rasmus B. Anderson translation (1897). Chapter 7.
  44. ^ The Life and Death of Cormac the Skald (Old Norse original: Kormáks saga). Chapter 22.
  45. ^ Setr Skuld hér til inn mesta seið at vinna Hrólf konung, bróður sinn, svá at í fylgd er með henni álfar ok nornir ok annat ótöluligt illþýði, svá at mannlig náttúra má eigi slíkt standast.[1]
  46. ^ The Saga of Thorstein, Viking&#x27;s Son[dead link] (Old Norse original: Þorsteins saga Víkingssonar). Chapter 1.
  47. ^ (Hall 2004) These attempts are based on onomastics and phraseology, e.g., the compound ælfsciene (&quot;elf-beautiful&quot;), used of seductively beautiful Biblical women in the Old English poems Judith and Genesis A, is cited as an echo of the Norse description of elves as beings as beautiful as the sun.
  48. ^ Klaeber, Friedrich (1950). Beowulf and the Finnesburg Fragment (snippet). John R. Clark Hall tr. (3 ed.). Allen &amp; Unwin. p. 5. , &quot;þanon untydras ealle onwocon / eotenas ond ylfe ond orcneas / swylce gigantas þa wið gode wunnon / lange þrage he him ðæs lean forgeald&quot;
  49. ^ Hall 2007, pp. 69–70
  50. ^ MS. 255 in the Library of Peterhouse, Cambridge. Israel Gollancz read a paper to the Philological Society in 1896, summarized in: Jannaris, A. N. (15 February 1896). &quot;The Tale of Wade&quot;. Academy (1241): 137. 
  51. ^ Gollancz, Israel (1906). &quot;Gringolet, Gawain&#x27;s horse&quot;. Saga Book of the Viking Society for Northern Research (London) 5: 108. 
  52. ^ Wentersdrop, Karl P. (1966). &quot;Chaucer and the Lost Tale of Wade&quot;. Journal of English and Germanic Philology 65: 73. 
  53. ^ Rickert, Edith (1904). &quot;The Old English Offa Saga&quot;. MP 2: 73. , cited in McConnell, Winder (1978). The Wate Figure in Medieval Tradition. P. Lang. p. 80. 
  54. ^ Hall 2007, p. 104
  55. ^ a b Shippey 2004, pp. 2–4
  56. ^ Grimm brothers felt &quot;that these are compounds formed to render the Greek.. and not expressive of a belief in analogous classes of spirits&quot;. Keightley 1850, p. 57
  57. ^ &quot;I have shown that the various compounds combining ælfen with topographical terms are almost certainly ad hoc formations, and that this is probably the case for ælfen itself (§5:3.2).&quot; (Hall 2004, p.</pre>

右文（仅阅读辅助）：

<pre> </pre>

### 位置2117332｜high_activation｜z=0.3026798

上下文2069，目标offset=346，目标token="8"；原文档未知。

包含目标的模型可见前文：

<pre> aussi au Moyen-Age que naquit le gruyère et peut-être la cancoillotte. On fixe le début du gruyère est attesté vers le XIIè ou XIIIè siècle. Pour la cancoillotte, son origine est moins précise&quot; 
  3. ^ &quot;La Cancoillotte&quot;. Retrieved 2013-01-13. &quot;D’autres historiens pensent que l’origine de la cancoillotte daterait du XVI ème siècle. Nicolas de Granvelle l’aurait introduite à la cour de Charles Quint. Mais c’est sans doute pour ne pas avoir à jeter du lait rapidement caillé que la recette est venue.&quot; 
  4. ^ &quot;Cancoillotte&quot;. French National Centre for Scientific Research. Retrieved 2013-01-13. &quot;Fromage du Jura ou de Franche-Comté obtenu à partir du lait écrémé et caillé formant le metton, auquel on ajoute du beurre, du vin blanc et des aromates&quot; 

External Links (french)[edit]

Other references[edit]

  • Jean-Marie Garnier, La Haute-Saône culinaire
  • Evan Jones, The World of Cheese&lt;|im_end|&gt;François Luambo Makiadi

From Wikipedia, the free encyclopedia
  (Redirected from Franco Luambo Makiadi)
Jump to: navigation, search
François Luambo Makiadi
Birth name Franco Luambo Luanzo Makiadi
Also known as Franco
Born (1938</pre>

右文（仅阅读辅助）：

<pre>-07-06)July 6, 1938
Genres Rumba
Occupations Singer, songwriter, guitarist
Instruments Guitar
Years active 1950-1980s
Associated acts OK Jazz, TPOK Jazz


Formative years[edit]




The 1980s[edit]




In 198</pre>

### 位置4397089｜random｜z=0.06049235

上下文4297，目标offset=674，目标token="6"；原文档未知。

包含目标的模型可见前文：

<pre>8 series.

As of 2011, Hewlett-Packard is producing the calculator models 12C, 12C Platinum, 17BII, 20B (financial), 30B (business), 33S, 35S, 48GII and 50G (scientific) which support RPN.[10]


Prinz and Prinztronic were own-brand trade names of the British Dixons photographic and electronic goods stores retail chain, which was later rebranded as Currys Digital stores, and became part of DSG International. A variety of calculator models was sold in the 1970s under the Prinztronic brand, all made for them by other companies.

Among these was the PROGRAM Programmable Scientific Calculator which featured RPN.

Soviet Union[edit]

Soviet programmable calculators (MK-52, MK-61, B3-34 and earlier B3-21[11] models) used RPN for both automatic mode and programming. Modern Russian calculators MK-161[12] and MK-152,[13] designed and manufactured in Novosibirsk since 2007 and offered by Semico, are backward compatible with them. Their extended architecture is also based on reverse Polish notation.

Current implementations[edit]

Existing implementations using reverse Polish notation include:

See also[edit]


  1. ^ &quot;An Analysis of a Logical Machine Using Parenthesis-Free Notation,&quot; by Arthur W. Burks, Don W. Warren and Jesse B. Wright, 1954
  2. ^ &quot;Charles L. Hamblin and his work&quot; by Peter McBurney
  3. ^ &quot;Charles L. Hamblin: Computer Pioneer&quot; by Peter McBurney, July 27, 2008. &quot;Hamblin soon became aware of the problems of (a) computing mathematical formulae containing brackets, and (b) the memory overhead in having dealing with memory stores each of which had its own name. One solution to the first problem was Jan Lukasiewicz&#x27;s Polish notation, which enables a writer of mathematical notation to instruct a reader the order in which to execute the operations (e.g. addition, multiplication, etc) without using brackets. Polish notation achieves this by having an operator (+, *, etc) precede the operands to which it applies, e.g., +ab, instead of the usual, a+b. Hamblin, with his training in formal logic, knew of Lukasiewicz&#x27;s work.&quot;
  4. ^ Kasprzyk, D. M.; Drury, C. G.; Bialas, W. F. (1979), &quot;Human behaviour and performance in calculator use with Algebraic and Reverse Polish Notation&quot;, Ergonomics 22 (9), doi:10.1080/00140137908924675 .
  5. ^ a b &quot;Electronic calculators: which notation is the better?&quot;, Applied Ergonomics 11 (1), 1980: 2–6</pre>

右文（仅阅读辅助）：

<pre>, doi:10.1016/0003-6870(80)90114-3 .
  6. ^ Hoffman, Errol; Ma, Patrick; See, Jason; Yong, Chee Kee; Brand, Jason; Poulton, Matthew (1994), &quot;Calculator logic: when and why is</pre>

### 位置4397125｜random｜z=0.1366642

上下文4297，目标offset=710，目标token="6"；原文档未知。

包含目标的模型可见前文：

<pre>8 series.

As of 2011, Hewlett-Packard is producing the calculator models 12C, 12C Platinum, 17BII, 20B (financial), 30B (business), 33S, 35S, 48GII and 50G (scientific) which support RPN.[10]


Prinz and Prinztronic were own-brand trade names of the British Dixons photographic and electronic goods stores retail chain, which was later rebranded as Currys Digital stores, and became part of DSG International. A variety of calculator models was sold in the 1970s under the Prinztronic brand, all made for them by other companies.

Among these was the PROGRAM Programmable Scientific Calculator which featured RPN.

Soviet Union[edit]

Soviet programmable calculators (MK-52, MK-61, B3-34 and earlier B3-21[11] models) used RPN for both automatic mode and programming. Modern Russian calculators MK-161[12] and MK-152,[13] designed and manufactured in Novosibirsk since 2007 and offered by Semico, are backward compatible with them. Their extended architecture is also based on reverse Polish notation.

Current implementations[edit]

Existing implementations using reverse Polish notation include:

See also[edit]


  1. ^ &quot;An Analysis of a Logical Machine Using Parenthesis-Free Notation,&quot; by Arthur W. Burks, Don W. Warren and Jesse B. Wright, 1954
  2. ^ &quot;Charles L. Hamblin and his work&quot; by Peter McBurney
  3. ^ &quot;Charles L. Hamblin: Computer Pioneer&quot; by Peter McBurney, July 27, 2008. &quot;Hamblin soon became aware of the problems of (a) computing mathematical formulae containing brackets, and (b) the memory overhead in having dealing with memory stores each of which had its own name. One solution to the first problem was Jan Lukasiewicz&#x27;s Polish notation, which enables a writer of mathematical notation to instruct a reader the order in which to execute the operations (e.g. addition, multiplication, etc) without using brackets. Polish notation achieves this by having an operator (+, *, etc) precede the operands to which it applies, e.g., +ab, instead of the usual, a+b. Hamblin, with his training in formal logic, knew of Lukasiewicz&#x27;s work.&quot;
  4. ^ Kasprzyk, D. M.; Drury, C. G.; Bialas, W. F. (1979), &quot;Human behaviour and performance in calculator use with Algebraic and Reverse Polish Notation&quot;, Ergonomics 22 (9), doi:10.1080/00140137908924675 .
  5. ^ a b &quot;Electronic calculators: which notation is the better?&quot;, Applied Ergonomics 11 (1), 1980: 2–6, doi:10.1016/0003-6870(80)90114-3 .
  6</pre>

右文（仅阅读辅助）：

<pre>. ^ Hoffman, Errol; Ma, Patrick; See, Jason; Yong, Chee Kee; Brand, Jason; Poulton, Matthew (1994), &quot;Calculator logic: when and why is RPN superior to algebraic?&quot;, Applied Ergonomics 25 (5): 327–333, doi:10.1016/</pre>

### 位置6117196｜high_activation｜z=0.3241642

上下文5978，目标offset=938，目标token="fact"；原文档未知。

包含目标的模型可见前文：

<pre> think that &quot;art&quot; is entirely separate from politics, etc. Or unless you&#x27;re trying to say that art is a category of free speech, which gets into the &quot;P*** Christ&quot; and &quot;D*** Mary&quot; controversies.

In everyday use, erotica is pornography. If I&#x27;m wrong, please correct me. --Ed Poor 11:08, 20 April 2007 (EDT)

Pornography is something that has degradation as its intent; it does not necessarily even have to contain sexual content. Erotica is material connected with love rather than sex, (though the love depicted is often of a sexual nature). So that although there is a large overlap between erotica and pronography, something can be one and not the other. For example the biblical book Song of Solomon might be readily categorised as erotica on the basis of its content, but few would call it pornography. --Jeremiah4-22 11:16, 20 April 2007 (EDT)
As a literary genre, pornography is writing that has sexual arousal as its primary objective. Erotica is such material with artistic pretensions. Thus, the descriptive term pornography implies a statement about intentionality and instrumentality without reference to merit, whereas the term erotica is evaluative and laudatory. In Flesh and the Word, John Preston more baldly says, &quot;The only difference is that erotica is the stuff bought by rich people.&quot; [3]
Certainly some pornography with artistic pretensions calls itself erotica, often to avoid legal prohibitions on the distribution of obscene material, for example. But this is in no way the same thing as being erotica. (That&#x27;s a rather dodgy source you&#x27;re using there, btw.) --Jeremiah4-22 11:34, 20 April 2007 (EDT)
I’m inclined to agree with you that erotica is pornography. I’d say that it makes up a subset of pornography – I’d be hard pressed to find a clear distinction. I think, in common usage, erotica=socially acceptable pornography, and pornography=socially unacceptable pornography.
Both erotica and pornography are intended to arouse sexual interest. Erotica, perhaps, more subtly than other pornography, but in the end it is about eros – love mingled with sexual desire. --Reginod 13:09, 20 April 2007 (EDT)
Erotica is pornography for those who have some inteligence. It requires a high level of literacy, and artistic appreciation. It takes skill to make, while plain pornography needs nothing more than a camera. But underneath, it is still pornography. It strives to be respectable, and to some extent suceeeds. But porn is porn, and thats all it will ever be. Just because its a well-written story, or a painting that takes incredible skill to paint, does not turn it magically acceptable. Erotica is a subset of porn, not something completly different. - BornAgainBrit
I&#x27;m not convinced by this. I wonder if we can make the distinction that pornography is solely concerned with sexual arousal and gratification through the graphic depiction of sexual acts, and that works of literary and artistic merit can contain passages of explicit sexuality that function as an integral part of the total work but are not intended purely for purposes of sexual gratification. The famous example of this in English law was, of course, the 1963 trial involving Penguin books and the D.H.Lawrence novel Lady Chatterley&#x27;s Lover. I have read that, and it&#x27;s true to say that the passages objected to in 1963 are fairly graphic (though perhaps less so by today&#x27;s standards). However, they are not the central point of the book, and their purpose is not arousal but a deepening of understanding of the themes of the nove. IMHO they add a great deal to the overall merit of the work. Personally, I found a book like American Psycho a great deal more distressing in that it explicitly ties sexuality to graphic violence. It seems invidious to me to single out the depiction of erotica as pornography while ignoring the graphic depictions of violence that seem to pass unnoticed. --Britinme 14:18, 23 April 2007 (EDT)

Needed fixes

Since the article is locked can someone make the following changes, marked in bold?

&quot;Due to a series of liberal decisions beginning with the Warren Court, pornography is aggressively sold and distributed in the United States without meaningful law enforcement{{fact</pre>

右文（仅阅读辅助）：

<pre>}}. It is a $12 billion industry that affects and harms 40 million Americans(POV). Pornography destroys relationships and exploits young people.[2]maybe include the article that claims this POV

Is there really such a large public concern about an alledged connection between pornography and porn? Check the link I provided in the debate about this subject for some statistics on the percentage of people</pre>

### 位置9199811｜random｜z=0.04047282

上下文8991，目标offset=941，目标token=","；原文档未知。

包含目标的模型可见前文：

<pre> style. For instance, in most Microsoft BASICs, commented lines could begin with a single &quot;&#x27;&quot; character, rather than the original &quot;REM&quot;, most commands could be abbreviated to the first letter (&quot;L&quot; for &quot;LET&quot;), variable names could be similarly contracted, and so on.

Disk based versions of BASIC were eventually available (after floppy disks dropped sufficiently in price) and Microsoft became the dominant supplier (eg, Applesoft BASIC for the Apple II, MBASIC for CP/M-80 machines, and Graphic Workstation BASIC (GWBASIC) for COompaq and eventually any non IBM PC clone machines. GWBASIC was meant to be compatible with BASICA for the IBM PCs, for none of the PC clone makers were allowed access to the ROM version; it eventually was also implemented as a compiler and is currently available as Visual BASIC in several flavours. Alternatives at various times included CBASIC from Gordon Eubanks (eventually acquired by Symantec), NorthStar BASIC for CP/M-80 machines, QBASIC for the Sinclair ZX80 and its 68000 based followon, the TSC BASICs (large, small, interpreted, and compiled/tokenized) for FLEX, FLEX9, and UNIflex machines based on the Motorola 6809 processor, and BASIC09 from Microware Systesm in Iowa, also for the 6809 CPU. There were also several other BASICs, or variants under other names, developed and marketed for the minicomputer market (systems using 12, 16, or even 32 bit CPUs and costing between $10000 and $200000) between, say, 1970 and 1990. Several were used as the &#x27;interface&#x27; language to database systems or business management packages. Some of them still survive. Various BASICs were also available for large mainframe systems from IBM, Burroughs, Univac, and so on.

BASIC &#x27;dialects&#x27; and implementation &#x27;styles&#x27; have varied. Some BASICs have stored all string variables as a part of a single large array, some haven&#x27;t; some BASICs have included automatic garbage collection (eg, many Microsoft variants), others haven&#x27;t; and so on. HP BASIC was one prominent &#x27;school&#x27; and DEC BASIC another. Microsoft&#x27;s &#x27;style&#x27;, basically in the DEC camp, became the de facto standard style for nearly all users by the mid-1980s. Ironically, Kemeny and Kurtz decided to offer an updated version of their language (TrueBASIC) but were too late -- there was little market for it. ANSI finally began a BASIC standardization project, but decided not to adopt Microsoft&#x27;s de facto standard. There was a Minimal BASIC standard, but it was essentially ignored by the market.

The language was originally implemented as a compiler, but in the 1980s, most implementations of it were interpreters (and when used inside another application, Basic is commonly used for scripting). Compiling implementations are commonly available today (such as Visual Basic).


Dialects of BASIC can be divided into many different groups, based on many of their aspects such as:

  • Their platform (Windows, linux, etc.)
  • Their type of purpose (games, gui applications, etc.)
  • Their ability to be compiled or interpreted

Some dialects:

QuickBASIC: the origin of all modern BASICS. A few programmers have spurred a cult for the language, as many games and tutorials are available on the internet for use.

FreeBASIC: QuickBASIC, compiled. It has many more modern features, such as pointers, 64-byte types, and support for larger amounts of memory. FreeBASIC is recommended, as this is the standard dialect for the following tutorials.

DarkBASIC: A significant commercial BASIC, which utilizes the DirectX library and is great for writing games quickly.

VisualBASIC: Microsoft developed this BASIC first in the early 1990s. It is slightly inaccurate to say that this is a dialect, as it resembles much different code than standard BASIC, and is very popular for commercial use. Gambas is a similar language and is used widely by Unix BASIC programmers.

Last modified on 15 September 2010, at 14:20&lt;|im_end|&gt;Church of Scientology blames Pearl Harbor, 9/11 on psychiatry

From Wikinews, the free news source you can write!
Jump to: navigation, search

Saturday, February 21,</pre>

右文（仅阅读辅助）：

<pre> 2009

In an interview on a television show called the No Drug Show, hosted by Larry Byrnes, the Church of Scientology blamed both the September 11, 2001 attacks in the United States and the attack on Pearl Harbor on psychiatrists and the drugs they prescribe their patients. Scientology considers psychiatry to be barbaric and a violation of human rights.

</pre>

### 位置9201970｜high_activation｜z=0.3085392

上下文8994，目标offset=30，目标token="2"；原文档未知。

包含目标的模型可见前文：

<pre>2. ^ &quot;Evaluation of Water Use Reduction Achieved Through Residential Toilet Fixture Replacements&quot;. Flushmate. Retrieved 23 December 2012</pre>

右文（仅阅读辅助）：

<pre>. 
  3. ^ &quot;WaterSense An EPA Partnership Program&quot;. US EPA. Retrieved 23 December 2012. 
  4. ^ Ross, Andrew (February 28, 2011). &quot;Low-flow toilets cause a stink in SF&quot; (web). San Francisco Chronicle. Retrieved December 10, 2012.</pre>

## Feature 3461，h_V=5

### 位置1663149｜high_activation｜z=0.6288431

上下文1625，目标offset=427，目标token="Edit"；原文档未知。

包含目标的模型可见前文：

<pre> Osborn reveal the identity of the goblin to him, threatening to harm his son Harry should he fail.
    Norman Osborn (Earth-92131) 005
    Spider-Man&#x27;s greatest foe.
    NotdopplerAdded by Notdoppler
    The stress caused Norman to be driven insane and become the Green Goblin again, defeating the Hobgoblin. He also discovered Spider-Man&#x27;s identity, and believed that Peter had got together with Mary Jane in order to hurt Harry, in an attempt to get at him. The goblin subsequently kidnapped Mary Jane and she was lost through an interdimensional portal, which the goblin was also sent through after Spider-Man defeated him. Peter was emotionally damaged due to the loss of Mary Jane, but sought distraction after the Black Cat came into his life, who wanted to become partners with Spider-Man in crime fighting.

    Harry also discovered Peter&#x27;s alter ego, and was soon haunted by images of his father, leading him into becoming the second Green Goblin. Harry was sent to Ravencroft for treatment after being defeated. Mary Jane also mysteriously returned to a delighted Peter.

    Marriage and ultimate battle

    Peter later discovered that his parents were spies for the American government, but were branded as traitors during World War II with Soviet Union against America. Peter also married Mary Jane (or at least a clone of the woman, unbeknownst to him until minutes before her death).

    Madame Web also revealed the ultimate battle she had been preparing him for - he&#x27;d been chosen by the Beyonder to prevent the creature from a parallel reality known as Spider-Carnage from destroying all of reality. A group of Spider-Men from other realities were also chosen, and they all worked together to defeat Spider-Carnage. Spider-Man used Uncle Ben who was still alive in one of the Spider-Men&#x27;s realities to distract Spider-Carnage.

    After, Madame Web decided to help Spider-Man find the real Mary Jane. Though never shown, he eventually did, and the two were fully married just like the clone.

    Powers and AbilitiesEdit</pre>

右文（仅阅读辅助）：

<pre>


    Seemingly those of Peter Parker (Earth-616)


    Peter Parker seemingly possesses a keen scientific mind, with a particular interest in radiation (a curiosity based on his spider powers). Peter is also a skilled photographer, and acrobat and combatant thanks to his spider powers.

    Strength level

    Having been bitten by the radioactive spider, Spider-Man possesses superhuman strength,</pre>

### 位置2701469｜random｜z=0.04485866

上下文2640，目标offset=210，目标token="]\n\n"；原文档未知。

包含目标的模型可见前文：

<pre> likely that one will configure an incomplete or oversized kernel. It&#x27;s recommended to start with the .config file included with the Linux distribution, which makes it easier to configure a custom kernel.

Better than editing the .config by hand, make menuconfig shows the descriptions of each feature (?), and adds some (primitive in version dependency checking. With make oldconfig, dependency checking can be done in one step, but requires the user to locate the features that were changed, by hand, to be sure that the needed ones are still enabled.

Practically, using both make menuconfig and make oldconfig, diff, (also cvs and a decent text editor) provides the most flexibility and most dependability. Configuring Linux is a significant labor, so users are strongly advised to make backups of it (i.e. cp /usr/src/linux*/.config ~/savemywork.config).



To use make menuconfig, the Linux kernel source is a requirement, a make tool, a C compiler, and the ncurses library.

Key Strokes[edit]

</pre>

右文（仅阅读辅助）：

<pre>Main Key strokes
Key stroke Meaning
 ? Option description and tips/Help
Left/Right (⬌) Up/Down (⬍) PgUp/PgDn Navigate through the kernel features and menuconfig commands.
Esc Esc Exit menuconfig or cancel the command.
Enter (⏎) Activate a command, or expand a branch.
y Compile and include this feature inside of the kernel</pre>

### 位置5437390｜random｜z=0.02630398

上下文5314，目标offset=518，目标token="]\n\n"；原文档未知。

包含目标的模型可见前文：

<pre>. The greater the light intensity, the more independent the document camera is from ambient light sources. Using powerful lighting systems enables smaller apertures to be used, and this in turn provides a significant increase in the depth of field that can be achieved by the document camera. Also the higher the quality of the light source, the more light that will reach the camera sensor, and this results in less noticeable noise, and therefore the quality of image is not degraded.

Some document camera models integrate additional functionality into the light system, such as a synchronized light field that clearly indicates to the user at all times, by way of an illuminated image capture area or laser markers, the size and position of the imaging area, which adjusts simultaneously as the lens zooms in or out.

Motherboard and firmware[edit]

The motherboard plays an important role in image processing and it has a major influence on the quality of the eventual image that is produced. Larger and larger resolutions and high refresh rates generate large amounts of data that must be processed in real-time.

Document cameras have a wide variety of sophisticated automated systems that are designed to make the user experience as easy as possible. Permanent autofocus detection, for example, automatically adjusts the focus settings when a new object is displayed, with no need for user intervention. Other important features include automatic auto iris, auto exposure, auto white balance and automatic gain control.

A document camera needs an image display device to show the information to the audience. Modern motherboards have a variety of connections to ensure flexibility of use. In addition to HDMI, DVI, VGA ports for connecting to displays, (projectors, monitors and video conferencing systems) there are also several interfaces provided to facilitate connection to a computer or interactive whiteboard. These interfaces are most commonly USB, Network (LAN) and serial.

In addition, an external PC or laptop can easily be connected to the document camera to allow for easy switching between a Power Point presentation and a live demonstration. Some models can also handle external storage devices and play files directly from a USB flash drive, or save images taken during the presentation onto it.

Some document camera manufacturers also provide for regular firmware upgrades, allowing users to have the opportunity to be equipped with, and benefit from new features as they become available.

Document camera types[edit]

Document cameras are generally divided into three groups. Smaller lightweight models are considered portable, larger sturdier and more stable units are known as desktop models, and the third group are ceiling visualizers. These are designed to be ceiling mounted above a tabletop or podium.

Portable and desktop models[edit]

</pre>

右文（仅阅读辅助）：

<pre>Portable and desktop models allow a similar working environment to that of an overhead projector. Many document camera users appreciate the added flexibility in terms of the variety of objects that can be displayed to an audience. Portable devices can be used in multiple locations without requiring any prior special installation.

Ceiling models[edit]

Ceiling Visualizer in use in a typical Telepresence installation

Ceiling-mounted document cameras/visual</pre>

### 位置6159605｜random｜z=0.02142116

上下文6020，目标offset=374，目标token=" article"；原文档未知。

包含目标的模型可见前文：

<pre> loss. They also have a sound booth which blocks out all other noises and provides an accurate reading of your hearing.

When shopping for a hearing specialist, make sure to use a well-established company. Checking with the Better Business Bureau can also help weed out specialists who don&#x27;t have a good track record. Audiology offices also have to be licensed in the state in which they are practicing.

The cost of hearing aids can be anywhere from $995 to $3,500 per ear, according to Beltone&#x27;s Rigg, and some insurances will help with the cost of the aids. For those who receive the gift of restored hearing through hearing aids, quality of life is greatly increased.


More about

More about

More about

Welcome to the discussion.

Welcome to the Explorer Newspaper

The Explorer Newspaper is a weekly newspaper located in Northwest Tucson.

Featured Videos


Online poll


Follow us on Facebook&lt;|im_end|&gt;Fairly Odd Parents Wiki

List of The Fairly OddParents locations

5,554pages on
this wiki
ConstructionTimmy This article is under construction.


This is a list of locations in The Fairly OddParents universe of Dimmsdale, Yugopotamia, and millions of other universes from The Fairly OddParents.

Main settings


Main article: Dimmsdale

Dimmsdale is an American city on Earth, in the state of California. It is the home of Timmy Turner, and therefore the main setting of The Fairly OddParents. Dimmsdale is a large sprawling city, with a downtown area full of skyscrapers and high rise buildings, and a more suburban area where Timmy and his family live. There are also more extravagant residences in Dimmsdale, including mansions and skyscraper penthouses.

Places of interest in Dimmsdale

City buildings

Fairy World

Main article</pre>

右文（仅阅读辅助）：

<pre>: Fairy World

The world from which the Fairy race comes from. Cosmo and Wanda frequently are required to return to Fairy World, be it for training, punishment, family matters, or simply to bring Timmy to events going on within. The planet is connect to Earth by a Rainbow Bridge. Fairy World has been destroyed countless times, and was at one point revealed to be built and suspended</pre>

### 位置6283683｜high_activation｜z=0.6249368

上下文6141，目标offset=676，目标token="Edit"；原文档未知。

包含目标的模型可见前文：

<pre>Tira-olhos&quot; (Eye snatcher). They are often associated with snakes, as in the Welsh name gwas-y-neidr, &quot;adder&#x27;s servant&quot;.[8] The Southern United States term &quot;snake doctor&quot; refers to a folk belief that dragonflies follow snakes around and stitch them back together if they are injured.[10]

    Dragonfly symbol on a Hopi bowl from Sikyatki archaeological site.

    For some Native American tribes they represent swiftness and activity, and for the Navajo they symbolize pure water. Dragonflies are a common motif in Zuni pottery; stylized as a double-barred cross, they appear in Hopi rock art and on Pueblo necklaces.[9]:20–26

    They also have traditional uses as medicine in Japan and China. In some parts of the world they are a food source, eaten either as adults or larvae; in Indonesia, for example, they are caught on poles made sticky with birdlime, then fried in oil as a delicacy.[8]

    In the United States dragonflies and damselflies are sought out as a hobby similar to birding and butterflying, known as oding, from the dragonfly&#x27;s Latin species name, odonata. Oding is especially popular in Texas, where a total of 225 species of odonates in the world have been observed. With care, dragonflies can be handled and released by oders, like butterflies.[11]

    Images of dragonflies are common in Art Nouveau, especially in jewelry designs.[12] They also appear in posters by modern artists such as Maeve Harris.[13] They have also been used as a decorative motif on fabrics and home furnishings.[14]


    As a seasonal symbol in Japan, the dragonfly is associated with late summer and early autumn.[15]

    More generally, in Japan dragonflies are symbols of courage, strength, and happiness, and they often appear in art and literature, especially haiku. The love for dragonflies is reflected in the fact that there are traditional names for almost all of the 200 species of dragonflies found in and around Japan.[16] Japanese children catch large dragonflies as a game, using a hair with a small pebble tied to each end, which they throw into the air. The dragonfly mistakes the pebbles for prey, gets tangled in the hair, and is dragged to the ground by the weight.[9]:38

    As it symbolizes courage, boys are given the name of &quot;Tombo&quot;, meaning dragonfly. The shape of the archipelago of Japan, as seen on a map, is said to be that of a dragonfly. Hence the leading male character in Kiki&#x27;s Delivery Service, in a non-Japanese setting, is named &quot;Tombo&quot; so that the Japanese audience can identify with him.

    Beyond this one of Japan&#x27;s former names – あきつしま (Akitsushima) – is literally an archaic form of Dragonfly Island(s).[17] This is attributed to a legend in which Japan&#x27;s mythical founder, Emperor Jinmu, was bitten by a mosquito, which was then promptly eaten by a dragonfly. [18][19]

    See alsoEdit</pre>

右文（仅阅读辅助）：

<pre>


    1. Head, Mandibles, and unusual Labium of Dragonfly Nymph (viewed from below)
    2. Dragonfly Nymph Zoology
    3. Dragonfly nymph eats guppy.
    4. Dragon fly larvae labium extended to capture prey
    5. P. J. Mill &amp; R. S. Pickard (19</pre>

### 位置6284495｜high_activation｜z=0.6366556

上下文6142，目标offset=464，目标token="Edit"；原文档未知。

包含目标的模型可见前文：

<pre>lying Folk Speech. American Speech 48 (1/2): 67–76.
    11. includeonly&gt;Tracy Hobson Lehmann. &quot;Dragonflying: the new birding&quot;, San Antonio Express-News, June 19, 2008.
    12. includeonly&gt;Moonan, Wendy. &quot;Dragonflies Shimmering as Jewelry&quot;, New York Times, August 13, 1999, pp. E2:38. ProQuest document ID 43893085.
    13. The Maeve Harris category contains 37 items. URL accessed on 2009-09-18.
    14. includeonly&gt;Large, Elizabeth. &quot;The latest buzz; In the world of design, dragonflies are flying high&quot;, The Sun (Baltimore, MD), June 27, 1999, pp. 6N. ProQuest document ID 42880564.
    15. Baird, Merrily (2001). Symbols of Japan: Thematic Motifs in Art and Design, 108–9, New York: Rizzoli.
    16. Waldbauer, Gilbert (1998). The Handy Bug Answer Book, 91, Detroit: Visible Ink Press.
    17. Nussbaum, Louis Frédéric et al. (2005). &quot;Akitsushima&quot; in Template:Google books
    18. Nihonto
    19. 杉浦 (Sugiura), 洋一 (Youichi); ジョン・K・ギレスピー (John K. Gillespie) (1999). 日本文化を英語で紹介する事典: A Bilingual Handbook on Japanese Culture (in Japanese &amp; English), 日本国東京都千代田区 (Chiyoda, JP-13): 株式会社ナツメ社 (Kabushiki gaisha Natsume Group). URL accessed 2010-04-26.

    External linksEdit</pre>

右文（仅阅读辅助）：

<pre>

    Wikimedia Commons has media related to:


      Advertisement | Your ad here

      Around Wikia&#x27;s network

      Random Wiki&lt;|im_end|&gt;Search tips
Search criteria 


J Mol Cell Cardiol. 2010 November; 49(5-2): 737–745.
PMCID: PMC2954357
Normal passive visco</pre>

### 位置8661261｜random｜z=0.06341335

上下文8465，目标offset=596，目标token="]"；原文档未知。

包含目标的模型可见前文：

<pre> abortion causes breast cancer early on in the history of the website. Later this is evidenced by Schlafly&#x27;s flat-out refusal to allow qualified persons to work on their article on the theory of relativity.

Finally, as Wikipedia is, unlike Conservapedia, neutral to facts, it is inherently neutral to all points of view, unless that point of view is derived without, and often in spite of, facts *Cough* intelligent design*cough*. However, even in these cases, Wikipedia is still neutral in the sense that it gives ID a good airing and allows the arguments to be put forward; all that it states that may not be considered &quot;neutral&quot; is actually a fact, namely the overwhelming scientific consensus is that evolution by natural selection is the best current theory. In short, Wikipedia itself says nothing, it just reports what others say, and gives them the prominence they deserve.

[edit] No censorship


This is perhaps the most hypocritical of all Conservapedia&#x27;s claimed differences with Wikipedia. Conservapedia claims it censors no facts (subject to definition of the word &quot;fact;&quot; Conservapedians&#x27; definition of it seems to be very close to the postmodernists&#x27;[citation NOT needed]) but take, for example, their news reports and article about breast cancer being linked with abortion. Reasonable members of Conservapedia attempted to link to resources published by very well respected scientists showing that the claim was false. These links were removed on sight by the sysops.

Senior sysop Conservative has achieved an impressive degree of infamy for the speed and zeal with which he censors any edits he thinks might threaten his beloved Creationism or Homosexuality and is currently the sole editor of many pet articles on the subjects.

Liberal censorship of &quot;conservative facts&quot; may not be tolerated on Conservapedia, but conservative censorship of &quot;liberal facts&quot; is not only allowed, but practiced very enthusiastically. The &quot;basic rules&quot; are whatever the sysops feel like they are at any given time. They adhere to them quite well.

[edit] Allows original works

10. We allow original, properly labeled works, while Wikipedia does not. This promotes a more intellectual atmosphere on Conservapedia. On Wikipedia, observations based on personal experience and interviews have been dismissed as &quot;original research&quot;. Here, we do not restrict research for articles in that manner.

&quot;Original Research&quot; means something that someone has done on their own and &quot;debuted&quot; on the encyclopedia. It doesn&#x27;t matter if any actual research was made, or even if it is particularly original, it just means that the idea, factoid or statement doesn&#x27;t appear elsewhere, hence can&#x27;t be verified. This difference is primarily to allow sysops and users to put in whatever they like into articles without credible sources. &quot;Articles&quot; such as Hollywood Values are the best examples of &quot;original research&quot; conducted by Conservapedia, as specifically its owner, Andrew Schlafly.

[edit]</pre>

右文（仅阅读辅助）：

<pre> Original research on Wikipedia

Wikipedia has &quot;no original research&quot; for very good reasons. It must source its statements, and they must be notable, so someone can&#x27;t just come along and say &quot;I made this up, down at the pub one afternoon&quot;, it has to have been said elsewhere, and even then, it has to be mentioned somewhere else too. This also ties in with the actual</pre>

### 位置10213141｜random｜z=0.05560085

上下文9982，目标offset=375，目标token=" articles"；原文档未知。

包含目标的模型可见前文：

<pre>. The project is set to be completed in 2013.

Defense industry



Influence of the Southwest Asian conflict

The ongoing Arab-Israeli conflict, the Persian Gulf War, and other conflicts in Southwest Asia have made huge impacts on the economy of Jordan. The fact that Jordan has peace with the surrounding countries, combined with its stability, has made it a preference for many Palestinians, Lebanese, and Persian Gulf immigrants and refugees. Though this may have resulted in a more active economy, it has also damaged it by substantially decreasing the amount of resources available for each person. Jordan has a law that states that any Palestinian may immigrate and obtain Jordanian citizenship, but must remit his/her Palestinian claim.. In November 2005, King Abdullah called for a &quot;war on extremism&quot; in the wake of three suicide bombings in Amman.

Opportunity cost of the conflict

A report by Strategic Foresight Group has calculated the opportunity cost of conflict for the Middle East from 1991 to 2010 at a whopping $12 trillion (12,000,000,000,000). Jordan&#x27;s share in this is almost $84 billion. Every Jordanian family will also have the opportunity to increase their annual income by more than $1,250 if peace is established in the region and the Arab-Israeli boycott is lifted in full.

The report also outlines how an extremely significant cost to Jordan is that the country is host to millions of refugees who make up 40% of their population and are a drain on 7% of the GDP. Jordan also spends over 5% of its GDP on defense, and has one of the highest numbers of military personnel in the region, 23,500 military personnel per million people.

Culture Main articles</pre>

右文（仅阅读辅助）：

<pre>: Culture of Jordan, Jordanian cuisine, and Sport in JordanMansaf, the national dish of Jordan.Prince Ali bin Al Hussein, Vice President of the FIFA.

Jordan is considered one of the Arab World&#x27;s most cosmopolitan and westernized countries with its capital Amman becoming referred to as the &quot;New Beirut&quot;. 67% of Jordanian youth identify themselves as liberals, second highest</pre>

## Feature 4159，h_V=4

### 位置94356｜random｜z=0.2449938

上下文92，目标offset=210，目标token=" T"；原文档未知。

包含目标的模型可见前文：

<pre>, created by Stan Lee and Jack Kirby, first appeared in Tales to Astonish #73 (November 1965). The character subsequently appeared in Tales to Astonish #74 (December 1965), The Incredible Hulk #269–272 (March–June 1982) and #471–474 (December 1998–March 1999).

Within the context of the stories, Amphibion is an amphibious creature from the planet Xantares, considered a powerful fighter, the Xantarean supreme warrior. He is mutated by the Xantarean Grand Council of Elders, and sent to claim the &quot;Sphere of Ultimate Knowledge&quot; on the home planet of the Watcher. Amphibion fights the Hulk over the Sphere, nearly drowning his opponent. Amphibion is exiled from Xantares when he returns after his failure.[28]

He later assists the Sagittarians, along with the Hulk, T</pre>

右文（仅阅读辅助）：

<pre>orgo, and Dark-Crawler against the Galaxy Master and the Abomination.[29] Amphibion returns to Xantares with the aid of the Hulk and, finding it decimated, is determined to help rebuild it.[30]

Amphibion in other media[edit]

Amphibion appears in the Hulk segment of the The Marvel Super Heroes (1966</pre>

### 位置1003907｜random｜z=0.05212271

上下文981，目标offset=173，目标token="t"；原文档未知。

包含目标的模型可见前文：

<pre> only because my Mom taught me. Maybe I was the victim of &quot;new math.&quot;
I learned how to make change because I worked at McDonalds for one month (it was not my favorite gig) when I was a teenager -- before there were computers that told you how much change to give. I agree with Trish that computers are the reason most young people don&#x27;t know how to &quot;make change.&quot;
Government education.
Thanks for the reads and rates...Actually you are right - it is computers and calculators (that they take into exams) that have been more or a handicap than a help...I agree. Thanks for adding that important thought...Good to know so many of you understand this whole experience!
Oh yeah! This happens all the time. And almost all &quot;cashiers&quot; use cash registers that all they have to do is enter in the amount &quot;t</pre>

右文（仅阅读辅助）：

<pre>endered&quot; and it calculates the change. They just can&#x27;t count it back. I grew up in the new math but I&#x27;m 58. My grandparents taught me to make change working at their A&amp;W restaurant when I was about 10 or 11. Even worse though, is the notion that the owner/manager has not trained the staff well enough and had them practice this</pre>

### 位置1124044｜high_activation｜z=0.3563219

上下文1098，目标offset=620，目标token=" T"；原文档未知。

包含目标的模型可见前文：

<pre> the Vicar. 8-23-64; # 326-11. &quot;SAPI.&quot; Savorelli, Fernando. 1-14-69; # 004-51. &quot;SAFE.&quot; Savorelli, Renzo. 6-12-65; # 34-692. &quot;RESA.&quot; Scanagatta, Gaetano. Sacred Congregation of the Clergy. Member of Commission of Pomei and Loreto, Italy. 9-23-71; # 42-023. &quot;GASCA.&quot; Schasching, Giovanni. 3-18-65; # 6374-23. &quot;GISCHA,&quot; &quot;GESUITA.&quot; Schierano, Mario. Titular Bishop of Acrida (Acri in Cosenza Province, Italy.) Chief Military Chaplain of the Italian Armed Forces. 7-3-59; #14-3641. &quot;MASCHI.&quot; Semproni, Domenico. Tribunal of the Vicarate of the Vatican. 4-16-60; # 00-12. &quot;DOSE.&quot; Sensi, Giuseppe Mario. Titular Archbishop of Sardi (Asia Minor near Smyrna). Papal Nunzio to Portugal. 11-2-67; # 18911-47. &quot;GIMASE.&quot; Sposito, Luigi. Pontifical Commission for the Archives of the Church in Italy. Head Administrator of the Apostolic Seat of the Vatican. Suenens, Leo. Cardinal. Title: Protector of the Church of St. Peter in Chains, outside Rome. Promotes Protestant Pentecostalism (Charismatics). Destroyed much Church

dogma when he worked in 3 Sacred Congregations: 1) Propagation of the Faith; 2) Rites and Ceremonies in the Liturgy; 3) Seminaries. 6-15-67; # 21-64. &quot;LESU.&quot; Trabalzini, Dino. Bishop of Rieti (Reate, Peruga, Italy). Auxiliary Bishop of Southern Rome. 2-6-65; # 61-956. &quot;TRADI.&quot; Travia, Antonio. Titular Archbishop of Termini Imerese. Head of Catholic schools. 9-1567; # 16-141. &quot;ATRA.&quot; Trocchi, Vittorio. Secretary for Catholic Laity in Consistory of the Vatican State Consultations. 7-12-62; # 3-896. &quot;TROVI.&quot; Tucci, Roberto. Director General of Vatican Radio. 6-21-57; # 42-58. &quot;TURO.&quot; T</pre>

右文（仅阅读辅助）：

<pre>uroldo, David. 6-9-67; # 191-44. &quot;DATU.&quot; Vale, Georgio. Priest. Official of Rome Diocese. 2-21-71; # 21-328. &quot;VAGI.&quot; Vergari, Piero. Head Protocol Officer of the Vatican Office Segnatura.</pre>

### 位置1786711｜high_activation｜z=0.3543688

上下文1746，目标offset=154，目标token=" T"；原文档未知。

包含目标的模型可见前文：

<pre>ish your wages, as Williams explained, and even if you declare bankruptcy, your student loans don&#x27;t go away. And as Hindman noted, miss a payment, and your interest rate goes up, creating a punitive spiral of debt there&#x27;s no way to escape from.



“Now the labor pool is flooded with people who have postgraduate degrees and are desperate for work. Employers are overwhelmed with the number of applicants and, in response, demand higher qualifications as a way to filter the applications. Yet higher education institutions continue selling something that doesn&#x27;t exist-- a guarantee of a better future. Something&#x27;s gotta give.”

The Solutions

So what can give?


But that&#x27;s not a solution for people like Parker, who was unable to finish school because of the cost, or T</pre>

右文（仅阅读辅助）：

<pre>oney, who wanted to go into public service but saw that door shut in her face with state budget cuts. They&#x27;re in debt now, not in 20 years, and $10,000 doesn&#x27;t begin to cover their debt, let alone the $80,000 Williams owes for a graduate degree. As tuition goes up thousands of dollars a year, a $</pre>

### 位置1799170｜random｜z=0.2684313

上下文1758，目标offset=337，目标token=" T"；原文档未知。

包含目标的模型可见前文：

<pre>? I&#x27;d rather have Pam Ward
BryantJohnson1 I&#x27;m calling Division 2 FB games but Joe Buck &amp; Troy Aikman can&#x27;t figure out what down it is in the final play of a NFL game. Unbelievable.

#Thom Brennaman (Bears vs Panthers)

timstwrt &quot;And Mare hammers it right down the throat.&quot; 29 yard FGs take Thom Brennaman to the edge of some pretty dark places.
matterickson23 Thom Brennaman, earlier you said a Bears TD was crucial to make it a 2-possession game. Except it would&#x27;ve just been an 8-point lead. #math
KingDonutI Thom Brennaman: &quot;Jay Cutler is not happy.&quot; Uhhh, dude, that&#x27;s all the damn time. #Bears #Panthers #NFL

#Phil Simms (Broncos vs Packers)

TundraVision Simms: &quot;That Minnesota game is going to be rough.&quot; Seriously, Phil?
Cosmis &quot;I&#x27;m gonna ignore the score of the game and talk about Tebow one more time.&quot; Phil Simms just said that on National Television.

#Everyone Else

DaBearNecess Billick dropping a ton of &quot;This Guy&quot; comments on Hester. @awfulannouncing
bteller @awfulannouncing game color guy on Fox just said the rams can&#x27;t worry about &quot;the two S&#x27;s - stats and statistics&quot; (Tim Ryan)
ChimpanzeeRage &quot;Perfect ball location. Yes, a little high and a little outside, but one he should catch.&quot; T</pre>

右文（仅阅读辅助）：

<pre> Ryan (not so perfect then?) @awfulannouncing
greebs Jim Mora has now entered that &quot;even when he&#x27;s right I want to disagree with him&quot; zone. @awfulannouncing
bjo109 @awfulannouncing siragusa &quot;the ship is sinking right now&quot; after arizona gets called for block in the back. meanwhile they&#x27;re up </pre>

### 位置2531535｜high_activation｜z=0.3582751

上下文2474，目标offset=176，目标token=" T"；原文档未知。

包含目标的模型可见前文：

<pre> alone and failing. He needs to learn that he isn’t infallible. And honestly at the moment who is there to do that? Lan could of fit the bill but he is gone. The aiel might complain and question but in the end they obey readily enough.

Good pick up on the 70 year thing though. Was it 70 years ago that Verin became black?

And just a reminder Cads doent know about Rand being bound in a box. Its not until after the fog of evil that Min tells her. Would have been interesting to know if her strategy would of remained the same with that knowledge.


Well she had something that interrupted Semi’s Tuon disguise.
craig thrift
68. gagecreedlives
Oh and Shimrod I think you got a couple of the characters mixed up. It was Tsutama and T</pre>

右文（仅阅读辅助）：

<pre>oveine that where exiled. Teslyn was never exiled but yeah did participate in the coup.
69. alreadymadwithcads
Treesinger @44
Errr, provoking Rand will inevitably bring LTT into play. While I can see the ter&#x27;angreal(maybe including one like Mat&#x27;s) holding off an enraged Rand, they won&#x27;t stop L</pre>

### 位置6264361｜random｜z=0.007689118

上下文6122，目标offset=793，目标token=" It"；原文档未知。

包含目标的模型可见前文：

<pre> have a big gathering in my house in which lots of my friends - they are doctors, they are professors at the university, lawyers, Ministry of Interior - and they all have this moderate mentality and they say it is hard for us.

&quot;We have become very [much of a] minority, because the Americans are attacking everything and because America is really trying to get the Saudis.&quot;


Khaled al-Maeena feels under the same pressure, but says Saudi Arabia could help itself by opening up more:

&quot;Let people come and see that Saudi Arabia has got nothing to hide and see the average Saudi on the street, who is just like &#x27;Jo Six Pack&#x27; in the United States or the guy who goes to the Saturday football in England.

Saudi internet cafe
Saudi liberals believe the country could do more to open itself up

&quot;Most of the things that are written about Saudi Arabia are third-hand and fourth-hand.

&quot;This is what&#x27;s happening with the hate mail writers, who have never met a Muslim, or a Saudi, or an Arab and are now condemning us and I have always asked them to come and visit us.&quot;

The trouble is, calmer voices like this are being drowned out in the US and other Western countries.

In Jeddah, diplomats say the Saudis are doing more to tackle al-Qaeda than they are being given credit for, and that US media attacks are over the top.

But with so much bad blood in the air, they say, no-one wants to listen, especially in America.

The BBC&#x27;s Fiona Werge
&quot;Arab opposition is making itself felt&quot;

Key stories

European probe


See also:

11 Aug 02 | Middle East
22 Aug 02 | Business
21 Aug 02 | Business
16 Aug 02 | Middle East
Internet links:

The BBC is not responsible for the content of external internet sites


E-mail this story to a friend

Links to more Middle East stories

© BBC ^^ Back to top
&lt;|im_end|&gt;[an error occurred while processing this directive]
BBC News
watch One-Minute World News
Last Updated: Saturday, 4 October, 2003, 22:11 GMT 23:11 UK
Eyewitness: &#x27;Dead children and babies&#x27;
Israeli Police and forensics experts stand outside the Maxim restaurant, Haifa, 4 October 2003
The restaurant was popular with both Jews and Arabs
Witnesses have described a scene of carnage in a Haifa restaurant after the suicide bomber struck on Saturday.

At least three children were among the 19 Israelis killed in the attack, which also left up to 50 people injured.

The attack - claimed by Palestinian militant group Islamic Jihad - ripped apart a popular seafront restaurant where Jews and Arabs had worked together and lived together for decades.

The Maxim restaurant, run jointly by a Christian Arab and a Jewish family, was packed with families having lunch when the female suicide bomber from the West Bank town of Jenin blew herself up.

&quot;Suddenly we heard a tremendous explosion. We saw smoke pour out of the restaurant,&quot; said a passing motorist, Navron Hai.

We felt a blast and then everyone around us was either wounded or dead
Itamar Chizik
&quot;Families were dead around the tables, there were children without limbs.&quot;

He said he and others went to help the injured, but found there was little they could do.

&quot;We went in, about five or six of us and started to take the wounded out,&quot; he said.

&quot;In truth there was not much to take out. There were not a lot of wounded, just a lot of people strewn on the ground. There was nothing to do, no way to help them.&quot;

Among the diners injured in the packed eatery were members of local football team Maccabi Haifa, including general manager It</pre>

右文（仅阅读辅助）：

<pre>amar Chizik.

&quot;We were sitting with our sides toward the door of the restaurant, we didn&#x27;t see who came in,&quot; he told Israeli media.

&quot;We felt a blast and then everyone around us was either wounded or dead.&quot;

The emergency workers were a mix of Jews and Arabs, in a city known for its peaceful co-existence.

&quot;This was a microcosm of Haifa, how we</pre>

### 位置7685257｜random｜z=0.08679068

上下文7511，目标offset=638，目标token=" t"；原文档未知。

包含目标的模型可见前文：

<pre>


People on the move&lt;|im_end|&gt;Studio Monitors

Through the late 1980s and 1990s, while hip-hop and grunge music took over the airwaves, another revolution affected nearly every listener, manifested in the way they consumed their favorite songs. The home stereo system, once a modular system of silver-plated and vacuum-tube-driven components devoted to high fidelity, or Hi-Fi, was replaced by “mini-systems” and “boom boxes.”






Recording great-sounding music isn’t dependent upon having world-class preamps and a locker filled with vintage microphones, since the quality of your work isn’t directly related to the quality of your tools. Simply placing equipment in the optimal position can have a major impact on your overall sound quality.

Apogee just announced the new Quartet, a USB 2.0 audio/MIDI interface that enables you to record up to 12 channels into an Apple computer, and will act as the centerpiece of your recording studio. Quartet features four combo-XLR inputs, each with a high-quality preamp for connecting microphones, instruments and line-level signals.

You can learn a lot about audio by recording your own music (or a friend’s music), and by volunteering to assist a local sound engineer. However, attending a formal audio school can also really help you learn the nuts and bolts of sound.




If you use your computer as the primary playback device for listening to music, the new Fostex PC-100USB will not only make controlling the volume fast and easy, but it will improve the overall sound quality of your system.

Voice-overs are an essential ingredient in the creation of dynamic media. They can be an unseen character in a story, or just a friendly voice persuading you to buy pet food. Voice-overs are found in every form of media, from news reporting to experimental filmmaking. Even photo slideshows can benefit from a well-executed voice-over.

Just because the outdoor drive-in movie complex has largely disappeared from American suburbs doesn’t mean you can’t set up your own theater—in the driveway. You may already own some of the components, and they don’t necessarily have to be seated in a convertible.

Syndicate content&lt;|im_end|&gt;Barclays to Raise $9B: Surveillance (7/30)

Your next video will start in
  • Info

  • Comments



This is bloomberg &quot;surveillance.&quot; a $20 billion hole means barclays will dilute the value of the share.

A historic cash call.

For many americans, the united states is still in recession.

The economist who called it that way for years joins us to defend and keep his recession call.

Forget about amazon crime.

The president picks up his book order at the warehouse in person, but is amazon creating linkedin quality jobs?

Good morning, everyone.

This is bloomberg &quot;surveillance.&quot; i am tom keene.

Live from bloomberg croquette quarters in new york.

It is tuesday, july 30. joining me is sara eisen and garlic to.

-- scarlet fu.

The president and t</pre>

右文（仅阅读辅助）：

<pre>ennessee talking about jobs.

First, we kick off with a morning briefing.

The japanese yen weakening for the first time in four days versus the dollar after japan&#x27;s industrial production slid by the most in two years.

Also overnight, sprint released earnings.

Owned by a japanese company, posted a wider than expected loss.

Pfizer releasing earnings, beating estimates, as the company prepares to split into three units</pre>

## Feature 4951，h_V=1

### 位置283423｜random｜z=0.0064025

上下文276，目标offset=988，目标token=" pm"；原文档未知。

包含目标的模型可见前文：

<pre> for anger management issues. Idc how &quot;hot&quot; he is.
in_styles 21st-Jul-2012 07:14 pm (UTC)
He&#x27;s white tho, sis.
spankmypirate 21st-Jul-2012 02:01 pm (UTC)
lol I was wondering when this article would show up. people need to get a grip.
hotcement 21st-Jul-2012 02:04 pm (UTC)
the whole second paragraph is so ridiculous lol. morgan freeman&#x27;s marriage ended because of batman! christian bale was arrested because of batman!
spankmypirate 21st-Jul-2012 02:10 pm (UTC)

lol, there&#x27;s no denying that a lot of bad shit happened around the franchise, but it&#x27;s purely coincidental and I hate these silly superstitions.
With enough prep time, Batman always gets it done.
bittermunchkin 21st-Jul-2012 02:02 pm (UTC)
Does this mention anything tragic happening during the first one?
prophecypro 21st-Jul-2012 02:12 pm (UTC)
The start of the Tom Cruise-Katie Holmes circus during the movie&#x27;s promo and WotW&#x27;s promo? If you wanna call it that.

Seriously, I remember people on superherohype going &quot;I&#x27;ve waited nearly a decade for this! If Tom Cruise invades the premiere on his bike....!&quot; lol
bittermunchkin 21st-Jul-2012 02:16 pm (UTC)
lol good point.
poison20 21st-Jul-2012 02:29 pm (UTC)
I can&#x27;t believe she had to pull out of the dark night because of that little shit
foreignhorsie 21st-Jul-2012 02:03 pm (UTC)
While I do think these are awful events. I don&#x27;t believe in curses - except for the cruciatus curse.
bittermunchkin 21st-Jul-2012 02:05 pm (UTC)
Ever since the Curse of the Bambino didn&#x27;t hold I&#x27;ve had zero curse faith
brynn__ 21st-Jul-2012 02:08 pm (UTC)
idk the omen curse kind of freaks me out in particular
britneyschalupa 21st-Jul-2012 02:10 pm (UTC)
I usually don&#x27;t believe in curses except like The Kennedy curse.
lovelylaura23 21st-Jul-2012 02:13 pm (UTC)
LOL the Kennedy&#x27;s. I don&#x27;t know who Joe Kennedy pissed off, but I bet they regret it.
pamelalillian 21st-Jul-2012 04:39 pm (UTC)
ikr. i do not want to be associated with anyone with a drop of their blood, sorry to say. too much evidence to support that curse.
myroomiswhite88 21st-Jul-2012 05:36 pm (UTC)
muzicnem 21st-Jul-2012 11:59 pm (UTC)
Srsly, they better keep reproducing en masse b/c those bitches have been dropping like flies for decades.
nemo_de_la_meer 21st-Jul-2012 02:38 pm (UTC)
I think Poltergiest films had something going on with it, as to what, it&#x27;s left to open discussion.
ljubavirakija 21st-Jul-2012 02:07 pm (UTC)
These are seriously reaching
putyohandsonme 21st-Jul-2012 02:08 pm (UTC)
Shit happens, either it is an accident, an act of evil, or a natural turn of things shit just happens and it sucks.
hotcement 21st-Jul-2012 02:08 pm (UTC)
so i&#x27;m watching the news right now and there&#x27;s video of the FBI trying to get into the apartment and they&#x27;re saying the shooter refuses to talk and that the fbi sent in robots with cameras and found 12 devices with jars full of black powder and liquid that might be fire accelerant.



ljubavirakija 21st-Jul-2012 02:33 pm</pre>

右文（仅阅读辅助）：

<pre> (UTC)
I feel so scared for all of the officers involved. I hope they&#x27;re able to disarm the traps safely
therearewords 21st-Jul-2</pre>

### 位置2030819｜random｜z=0.1455626

上下文1984，目标offset=780，目标token=" t"；原文档未知。

包含目标的模型可见前文：

<pre> without being overly &quot;taxed&quot;. I read that smaller meals help cultures build to a larger size without overwhelming, that being said I don&#x27;t want to underwhelm them either..

Hope this makes sense,

Thanks mate.

Juergen Krauss&#x27;s picture
Juergen Krauss


How are you doing?

There are a lot of good posts on this site about creating great starters.

You might want to look into ananda&#x27;s blog,

or see dmsnyder&#x27;s fantastic essays on SF Sourdough

I think as a home baker it is possible to be fairly relaxed about feeding cycles and storing in the fridge as long as the starter works and wakes up again after refridgerating. Keep it simple (and reproducable).

Rye sours and Wheat sours are very different, and there is a fair deal of cultural stuff around the way they are used and treated.

Happy baking, and I hope to hear more from you,&lt;|im_end|&gt;Persimmon Tree in Winter

There&#x27;s an article from last week&#x27;s New York Times that&#x27;s drawing a lot of attention, at least in the circles I travel in. It&#x27;s called The Joy of Quiet and in it, writer Pico Iyer very eloquently describes his search for quiet and stillness and how now, more than ever, people are seeking out places where their technology can&#x27;t follow them in order to find a bit of peace. What strikes me, though, is this idea that we have to go somewhere far away, to a hermitage or a monastery or move to rural Japan, to experience the quiet and focus we all crave. I think we simply have to go to the kitchen.

It&#x27;s not that it&#x27;s a bad thing to go to places that ask things of us that our everyday lives don&#x27;t, that encourage stillness, reflection, and offer a quiet environment that can support this kind of inquiry. But Mr. Iyer&#x27;s life, which consists of living in rural Japan without a cell phone, is a very, very different existence than most people have or can ever hope to achieve. Most of us have to live in busy metropolises and work long hours at intense jobs, all the while juggling our families and household maintenance and 10, 000 other things.

So perhaps a more realistic endeavor than taking off to a mountain top is to find those same qualities right where we are, in the middle of our everyday life. This stillness we seek doesn&#x27;t belong only in the monasteries and ashrams that we visit. It lives within us, it is a part of us. We just have to find it and unfold it. Sometimes it&#x27;s just the simple act of remembering that it&#x27;s there.

If you are a regular reader of this column, then you know that finding stillness and connection in the kitchen is an ongoing theme here. For me, the kitchen offers a perfect blend of activity, focus, practicality, and creativity that helps to root me in a sense of well-being. But even more, being in the kitchen requires engagement and attention. When I&#x27;m cooking I need to be focused in the task at hand. I need to be present and attentive for the food will quickly teach me when I&#x27;m not. There will be burns and cuts, or over salted pasta or too much sugar, or missing ingredients. There will be pain.

But perhaps even more important, cooking is about being in relationship: to the ingredients, to the space I am occupying, to the people I am cooking for, to the life-force that enables this nourishment to happen. When I&#x27;m in relationship in this way, I&#x27;m also engaged in a form of stillness, or to put it another way, in a state of non-being. Or to put it another way, I&#x27;m participating in something deeper and more significant to my life than t</pre>

右文（仅阅读辅助）：

<pre>ending to my ego&#x27;s restlessness and dissatisfaction.

So yes, we can look for this in a hotel on the cliffs of Big Sur where our cell phone doesn&#x27;t work and there&#x27;s no TV in the room, and there&#x27;s nothing wrong with that. But if for some reason that isn&#x27;t possible for you, then send the roommates or family away (promising them dinner when they return,)</pre>

### 位置2564041｜high_activation｜z=0.2510314

上下文2505，目标offset=938，目标token=" o"；原文档未知。

包含目标的模型可见前文：

<pre> have any true relevance to the Rand/ LTT argument as the two cases aren&#x27;t at all similar.
Rob Munnelly
209. RobMRobM
Already - Rand kept Cads close, formally asked her for help as his advisor, listened to her advice through KoD - not sure how much better the relationship could be?
211. alreadymadwithadvice
RobMRobM @209
Yes, Rand asked Cads to be his advisor but this is just an extension of granting Min&#x27;s request not to drive her away. As for advice, he asked her for advice, but she did not even know what advice to give him since he apparently had all the pieces together. Cads even pondered on how to advise him, rather than simply accepting that Rand&#x27;s chosen course was already well thought out. As she would eventually concede in TGS, most of Rand&#x27;s decisions do actually make sense.
Marcus W
212. toryx
Man-O @ 202:

I don&#x27;t think I really hate Cadsuane myself. I just hate the way she treats Rand throughout. And I do blame her for a lot of what ultimately happens to Rand&#x27;s spirit. That&#x27;s an opinion that&#x27;ll never be validated one way or another, though.

RobM @ 205: I agree, it&#x27;ll be interesting to discuss Cadsuane more in future chapters.

@ 209: I&#x27;m inclined to agree with Alreadymad: I think Min is more responsible for Rand&#x27;s attitude with Cadsuane than Cadsuane is. That&#x27;s one of the things we&#x27;ll be able to re-examine more closely in future chapters.

In general: Man, it&#x27;s been a long day.
Ron Garrison
213. Man-0-Manetheran
toryx @ 208:

You too? I never expressed it either, but it was all &quot;walks like a duck, talks like a duck&quot; and then RJ up and says &quot;nope.&quot; Suspicious.

I have a similar theory on &quot;who killed Asmodean?&quot; Storywise, Asmo had served his purpose and there was no point in keeping him around much longer. I think RJ killed him off for no other reason and left it a mystery just to have fun with us. His comments when asked were always something like, &quot;well it&#x27;s so obvious, I&#x27;m surprised you haven&#x27;t figured it out.&quot; Ah. No. Not obvious.
Bonnie Andrews
214. misfortuona
This thread exemplifies the reason that I love WOT. The dialogue produced by the arrival of this one character is awesome. People hate her, find her annoying but like the twist she brings to the book, or love her (Well just MOM falls in this category but he’s someone too ;P).
Maybe some people are indifferent. There are voices missing from this thread, but I can’t imagine there are many who don’t find themselves having a reaction to her special way of dealing with people.

RJ wrote such amazing characters that we find ourselves feeling their pain, and defending them like they are our best friends.

Personally I think that Cads introduction was brilliant. She comes out of nowhere, bursts onto the scene, messes with the hero, takes a few shots at the snooty AS, while epitomizing what we dislike most about them, and then sets herself up to stay on the scene indefinitely. Grrrr. She’s a good guy that makes most of us want to scream, or throw books when she’s on screen. What could be better?

I also don’t think it’s an accident that she turns out to be much like Semi. She could easily have been one of the FS herself except that she wants to do what’s right for the world, not for herself. I’m not saying cut her a break, or that we shouldn’t hate her either. I’m saying she’s portrayed as a real person, one who&#x27;s been right for so long that she doesn’t believe she can be wrong. That makes her human, three hundred years old, crotchety, powerful, bossy, but human, and a wonderful character.

I know there are people who feel she could/should have been left out of the book completely. But I for one love that she’s here.

@ Cads &#x27;hat trick&#x27;
It occurred to me that maybe one of the ‘greal’ on her hair net, might be countering the effects of the oath rod. Not making it so she can break the o</pre>

右文（仅阅读辅助）：

<pre>aths, but keeping her alive longer than her normal half-life.

Mis-loving to hate Cads

RobM@205 I&#x27;m with you. Bring on the discussion

PS. Sorry about the wall of post, but several posts have failed to find their way to screen today, and I figured I better get it all out while I can.
Ron Garrison
215. Man-</pre>

### 位置2693427｜random｜z=0.02446891

上下文2632，目标offset=356，目标token="u"；原文档未知。

包含目标的模型可见前文：

<pre>; Yet all in vaine, all works not Grinuils harmes; Which seene, shee smiles, and yet with rage imbost5 Saith to her selfe, since men are all too weake, Behold a goddesse shall thy lifes twine breake.

With that shee takes a Musket in her hand, Raft from a dying Souldiour newlie slaine, And ayming where th’ vnconquered Knight did stand, Dischargd it through his bodie, and in twaine Deuids the euer holie nuptiall band, Which twixt his soule, and worlds part shold remaine, Had not his hart, stronger then Fortunes will, Held life perforce to scorne Misfortunes ill.

The bubling wound from whence his blood distild, Mourn’d to let fall the hallowed drops to ground, And like a iealous loue by riuall illd, Sucks in the sacred moisture through the wound; But he, which felt deaths fatall doome fulfilld, Grew fiercer valiant, and did all confound, Was not a Spanyard durst abord him rest, After he felt his deaths wound in his brest.

Hundreds on hundreds, dead on the maymed fall, Maymed on sounde, sound in them selues lye slaine, Blest was the first that to his ship could crall, For wounded, he wounds multituds againe; No sacrifice, but sacrifice of all, Could stay his swords oblations vnto paine, Nor in Phillipie, fell for Cæsars death, Soules thicker then for Grinu</pre>

右文（仅阅读辅助）：

<pre>ils wasting breath.

The Nemian Lyon, Aramanthian Bore, The Hircanian Tyger, nor the Cholcean Bulls, Neuer extended rage with such vprore, Nor in their brests mad monstrous furie lulls; Now might they learne, that euer learnt before, Wrath at our Knight, which all wrath disanulls, For slau</pre>

### 位置3217994｜random｜z=0.05230094

上下文3145，目标offset=169，目标token="_c"；原文档未知。

包含目标的模型可见前文：

<pre>; use gpiochip_remove() when it is unavoidable.
 470Most often a gpio_chip is part of an instance-specific structure with state
 471not exposed by the GPIO interfaces, such as addressing, power management,
 472and more.  Chips such as codecs will have complex non-GPIO state.
 474Any debugfs dump method should normally ignore signals which haven&#x27;t been
 475requested as GPIOs.  They can use gpiochip_is_requested(), which returns
 476either NULL or the label associated with that GPIO when it was requested.
 479Platform Support
 481To support this framework, a platform&#x27;s Kconfig will &quot;select&quot; either
 484three functions: gpio_get_value(), gpio_set_value(), and gpio_c</pre>

右文（仅阅读辅助）：

<pre>ansleep().
 486It may also provide a custom value for ARCH_NR_GPIOS, so that it better
 487reflects the number of GPIOs in actual use on that platform, without
 488wasting static table space.  (It should count both built-in/SoC GPIOs and
 489also ones on GPIO expand</pre>

### 位置6053795｜random｜z=0.120172

上下文5916，目标offset=979，目标token=" b"；原文档未知。

包含目标的模型可见前文：

<pre> the guy fails at one job, so they give him a cushy post solving the middle east. [ laughter ] folks, i applaud the obama administration&#x27;s mature decision. clearly these detainees are going to be there until they die. so it&#x27;s time we embrace gitmo as a part of this country. and not as

hearings. &gt;&gt; the second d obama administration began with h a 19- minute 2114-word address that mitch mccnell described as an unabashed and the left-of-center speech that brought back memories of the democratic partrty of aid is passed. &gt;&gt; our journey is not comete until we f find a bett way too welcome the striving, hopeful immigranan who still see america as a land of opportunity,y, uil bright young students and engineers are enlisted in our workforce rather than expeld from our countryry. our joury is not complete until all our children, from the streets of detro to the hills of appalachia, to the quiet lanes of newtown, know that they are cared for and cherished and always safe from harm. &gt;&gt; there you have it. immigration and can control. at his comments abo climate change andnd income inequality, and the need to reserve mecare medicaid, and social security, and you have a pretty good picture of where he wants to take the country. nina how would you grade the president&#x27;s speech? &gt;&gt; i&#x27;d thought it was a lot better than his first speech. the crowd had a blast. it was a speech that d

hinted at maybe reasoned debate. &gt;&gt;&gt; the obama administration launched a public push for stiffer gun laws. we&#x27;ll tell why you democrats could stand in the way of the president&#x27;s efforts. let&#x27;s turn to the weather. almost felt balmy out there today compared to last week. kim is in for chuck tonight. did we make it above freezing today? &gt;&gt; we absolutely did. we did it with some degrees to spare, i&#x27;m happy to say. and tomorrow will be the same if not a little milder. but we have some hiccups to talk b first, a couple of snow showers out there this evening. nothing heavy. they have been reported here and there, especially in our western suburbs. we&#x27;re zooming in towards fairfax county and into west springfield. this is right around the rolling road and old keen mill intersection by that whole foods and then back up towards fairfax and north and west into leesburg. again, a couple of snow showers. but nothing heavy and we&#x27;re not going to see them stick around tomorrow. look at that. some of us are going to be in the upper 30s. we&#x27;ll talk about some tricky weather, though, monday morning&#x27;s comm

shown a bond our guests. our first says it is unlikely the obama administration will push through a ban on assault weapons or a ban on large capacity ammunition magazines. the white house task force on gun violence as he said, failed to address the concerns of governors. joining us now, president of the national rifle association. good to have you with us. this has been a remarkable state in the presentation by joe biden to the present, the statements by the president himself and a press conference. hastily called saying that make taking guns away from people isn&#x27;t about the second amendment your reaction. &gt;&gt; it is. it is about american freedom. this is a president who has spent his life as an opponent of second and minarets in this country. he promised before the election board that after the election you start to do something. he has this whole public-relations -- relation operation financed to a mere blumberg of new york that was ready to swing into action. what newtown gave him was an excuse to do what they wanted to do for some time, which is to launch a full breath attack on the s

overseen the obama administration&#x27;s targeted assassination program known as the disposition matrix during his one ostend, and could likely continue that role at the helm of the cia. secretary of homeland security janet napolitano will remain in her post for obama&#x27;s second term according to white house officials. napolitano&#x27;s and who prefers to serve as arizona governor, has been criticized by immigrant rights advocates for presiding over a record number of deportations in the 2012 fiscal year. in a statement, a representative from the national day labor organizing network said -- the news napolitano&#x27;s staying on comes as the obama administration is said to be preparing to unveil a new push for immigration reform in the coming months. federal prosecutors have dropped the charges against the computer programmer and cyber activist aaron swartz following his suicide on friday at the age of 26. in an e-mail to the b</pre>

右文（仅阅读辅助）：

<pre>oston globe, his attorney wrote the dismissal was &quot;too little too late,&quot; saying it &quot;would have been welcome this time last week.&quot; iran supports was facing up to 35 years in prison f

. &gt;&gt;</pre>

### 位置6348407｜high_activation｜z=0.2490783

上下文6204，目标offset=928，目标token=" o"；原文档未知。

包含目标的模型可见前文：

<pre>, religion, gender, or sexual orientation - is extremely controversial. Do you believe society should punish such speech with criminal penalties? To what degree are colleges and universities justified in trying to discipline students who engage in such speech? Do you feel it is proper to place any boundaries on free expression in order to prohibit insulting and abusive speech? Why or why not?

2. Advertising is a form of public speaking. Choose an advertisement - either from the radio, television, or in print - and analyze it. Which demographics are the advertisers appealing to? What methods do they use to attract certain consumers? Do these tactics alienate other potential customers? In what ways do you feel the advertisement is effective? Please include a copy of a print ad., the transcript or a radio ad., or the transcript and description of a television ad.

3. Why must informative speakers be careful not to overestimate what the audience knows about the topic? What can a speaker do to make sure that his or her ideas don’t pass over the heads of the listeners?

4. What is the difference between an informative speech and a persuasive speech? Why is speaking to persuade more challenging than speaking to inform?

5. Divide a sheet of paper into two columns. Label one column “characteristics of an effective public speaker” and the other “characteristics of an ineffective public speaker.” List and briefly explain what you believe five characteristics of each to be. Oh the basis of that list, candidly evaluate your own strengths and weaknesses as a speaker. Identify where you’ve improved as a result of this course, and where you still feel you need practice.

More on Writing

I&#x27;ve mentioned before that I have the (cough*GEEKY*cough) habit of collecting language. I make a point to copy down the words of others that speak to me - or, rather, that strike me like lightning, which is most often the case. Every once in a while, I&#x27;ll go back to read something that I&#x27;ve written, and will be pleased to see a passage or turn of phrase that, had I not already written it myself, I&#x27;d add to my collection. It&#x27;s those few perfectly crafted passages that keep me writing.

Here, I offer you the words of the great Nathaniel Hawthorne. I have a particular love for good &#x27;ole Nate, mostly because I feel he had a deep and profound insight into what it means to be a New Englander; a Yankee in the truest sense of the word; a native (I love Sarah Orne Jewett for the same reason, but I&#x27;ll save her for another post). This passage - one of my all-time favorite pieces of writing ever - is taken from The Custom-House, which serves, in most editions, as a preface to The Scarlet Letter. I&#x27;m going to give it to you without any editorializing - we can have a conversation about it, if you like, in the comments.



Planted deep, in the town&#x27;s earliest infancy and childhood, by these two earnest and energetic men, the race has ever since subsisted here; always, too, in respectability; never, so far as I have known, disgraced by a single unworthy member; but seldom or never, on the other hand, after the first two generations, performing any memorable deed, or so much as putting forward a claim to public notice. Gradually, they have sunk almost out of sight; as old houses, here and there about the streets, get covered half-way to the eaves by the accumulation of new soil. From father to son, for above a hundred years, they followed the sea; a grey-headed shipmaster, in each generation, retiring from the quarter-deck to the homestead, while a boy of fourteen took the hereditary place before the mast, confronting the salt spray and the gale which had blustered against his sire and grandsire. The boy, also in due time, passed from the forecastle to the cabin, spent a tempestuous manhood, and returned from his world-wanderings, to grow old, and die, and mingle his dust with the natal earth. This long connexion of a family with one spot, as its place of birth and burial, creates a kindred between the human being and the locality, quite independent of any charm in the scenery or moral circumstances that surround him. It is not love but instinct. The new inhabitant--who came himself from a foreign land, or whose father or grandfather came--has little claim to be called a Salemite; he has no conception of the o</pre>

右文（仅阅读辅助）：

<pre>yster-like tenacity with which an old settler, over whom his third century is creeping, clings to the spot where his successive generations have been embedded. It is no matter that the place is joyless for him; that he is weary of the old wooden houses, the mud and dust, the dead level of site and sentiment, the chill east wind, and the chillest of social</pre>

### 位置8726689｜high_activation｜z=0.2588439

上下文8529，目标offset=544，目标token=" o"；原文档未知。

包含目标的模型可见前文：

<pre>winia amylovora and the apple scab pathogen Venturia inaequalis, are highly sensitive to copper, and we have no reason to believe that copper is a material that is at risk for resistance development in either of these pathogens. Thus, the potential benefit in using copper early for disease control is high. The only limitation is application timing as coppers applied after 0.25- to 0.5-inch green tip could result in phytotoxicity including fruit russeting.

Primary inoculum refers to the bacteria that cause the initial infections in a growing season. After colonization of flower stigmas, bacterial populations in orchards can skyrocket, and blossom blight infections can occur with significant losses sure to follow. Therefore, limiting primary infection by starting control practices early is a critical first step in a season-long control program.

The predominant location of overwintering bacterial inoculum for fire blight is in cankers. These cankers are initiated from shoot blight infections occurring in the previous season and represent internal populations of the pathogen. As temperatures warm up in a growing season, cankers begin to ooze bacteria that can then be transmitted to and colonize flowers. Fire blight infections leading to blossom blight are initiated during bloom. Bacterial colonization and infection of open flowers lowers yield and initiates internal, systemic infections of trees that can lead to rootstock blight and death of younger trees planted on susceptible rootstocks. The occurrence of shoot blight (wilting and dieback of actively growing shoots) is also typically higher in orchards where blossom infections have occurred.

Besides pruning and removal of fire blight cankers during the winter, the best method for reducing initial inoculum populations of plant pathogenic bacteria in orchards is to use an early application of copper to cover trees with a &quot;blanket&quot; of copper. This tactic should be reserved for orchard blocks where fire blight has occurred in one of the previous two years, or blocks of highly-susceptible cultivars adjacent to blocks with recent fire blight. Entire trees should be sprayed, not just alternate rows. High rates of copper can be used (about 2.0 metallic copper per acre), with timings immediately prior to the trees breaking dormancy or up to about 0.5-inch green tip. Be sure that the correct rate of copper is used and that sprayers are properly calibrated.

The goal of this management practice is to have copper available to protect the plant tissue from bacterial colonization over time as the tissue develops. Thus, the copper being applied to trees at 0.5-inch green tip will actually be needed during or immediately prior to bloom, when cankers traditionally are o</pre>

右文（仅阅读辅助）：

<pre>ozing. Because the copper must be sprayed much earlier in the season than the dates of its targeted effectiveness, this management strategy can be defeated by rain amounts of 2 to 3 inches between green tip and bloom that wash the copper residues off trees.

In theory, any formulation of copper should be effective in disease control (copper sulfate, cupric hydroxide, copper oxychloride,</pre>

## Feature 5147，h_V=0

### 位置12986｜random｜z=0.0404032

上下文12，目标offset=711，目标token=" willing"；原文档未知。

包含目标的模型可见前文：

<pre> force them) through gmail1? How can I fix this?,2012:site.222759 Tue, 21 Aug 2012 09:34:43 -0800 account default gmail mac macmail mail send sarae How do I filter out e-mails with an empty To: fields in Gmail? How do I filter out e-mails with an empty To: fields in Gmail? I basically want to filter out e-mails that I receive but have an empty &quot;To:&quot; field in gmail (and from specific e-mail addresses) but I can&#x27;t figure out how to specify it with Gmail&#x27;s filtering search criteria boxes. You&#x27;ve probably seen these e-mails as To:undisclosed recipients, but when you look at the details it is because the To: field is blank. I&#x27;m quite familiar with creating gmail filters, but I just can&#x27;t figure out what to put in the search box to make gmail look for To: fields with &#x27;nothing&#x27; in them and every tutorial I&#x27;ve found online is about how to &lt;em&gt;send&lt;/em&gt; e-mail like this, not filter out ones you receive. I&#x27;ve tried leaving all the search fields blank which finds all my e-mails, tried empty quotes and parenthesis, ie &quot;&quot; or () but it still returns all e-mails, and I&#x27;ve tried typing in &quot;undisclosed recipients&quot; but it didn&#x27;t find these e-mails (unless those words were actually written in the To: field). Is it even possible to search for blank To: fields?,2012:site.220192 Tue, 17 Jul 2012 09:14:50 -0800 email e-mail filter gmail google mail search to mxmm What a drag. It&#x27;s possible to drag a message to a label in GMail by grabbing it from the leftmost edge. However, on a hi-res monitor, this can be quite difficult. Is there a hack or greasemonkey script that allows you to drag the message by clicking and dragging anywhere in the Subject rather than just the left edge?,2012:site.217419 Sun, 10 Jun 2012 09:38:05 -0800 gmail google mail I EAT TAPAS Hardcore methods for e-mail blocking Looking for elite e-mail blacklist tricks to block a stalker. I have a determined and intelligent stalker. This person blasts my domain with harassing messages. I have tried the official methods for e-mail blocking, but found them unsatisfying. Typically, as on GMail, you filter addresses into the Trash. But then they sit there for days, and I don&#x27;t want that, because I check my Trash for other messages.&lt;br&gt; &lt;br&gt; I have also tried the &quot;fake bounce&quot; method, which just caused this person to send taunting messages for months along the lines of &quot;Since you&#x27;ve blocked my e-mail, I can write anything I want! haha.&quot;&lt;br&gt; &lt;br&gt; What I dream of is a hardcore solution. Maybe something at the server level. Something that will kill these messages before they even reach my inbox. Routing them through some UNIX/procmail thing somehow !? I will learn how to build a new mail server if that is what it takes.&lt;br&gt; &lt;br&gt; I&#x27;m on Dreamhost using Google Apps on my business domain. But am willing</pre>

右文（仅阅读辅助）：

<pre> to try anything if it will provide blacklisting. It looks like Google Apps for Business stopped including this, when it stopped offering the mail package Postini.&lt;br&gt; &lt;br&gt; Is there some blacklisting server I could route the e-mail through? Some PINE thing like in college, where I can run a script that deletes spam, before it reaches me? Or does one of the major Web</pre>

### 位置523251｜random｜z=0.009397339

上下文511，目标offset=348，目标token="1"；原文档未知。

包含目标的模型可见前文：

<pre> percentage of the cars remaining value.

RE: choices are good, but need to be informed
By FITCamaro on 11/7/2012 8:25:43 AM , Rating: 2
All the more reason to get a manual. They don&#x27;t fail. Just the clutch does.

By Ristogod on 11/7/2012 10:43:03 AM , Rating: 2
Tell that to the Synchros in my manual tranny.

RE: choices are good, but need to be informed
By The Melon on 11/7/2012 11:20:06 AM , Rating: 3
It does matter, allot actually. Diesel engines have to be built to withstand far higher combustion pressures than gasoline engines do and they benefit from having lower a exhaust gas temperature.

Modern turbo diesel engines have between 16 and 18:1 compression ratios PLUS 20-25psi factory boost from the turbos. Gasoline on the other hand considers 12:1 high compression and 7-10psi on a turbo is the norm. You go much higher and you have a real hard time controlling pre-combustion on gasoline.

Ford designed and tested it&#x27;s 6.7l Scorpion diesel to have a minimum of 250k service life under extreme conditions before internal rebuild. I would expect a real world average of 300-500k minimum.

It is not uncommon to see consumer level diesels with more than 500k on them.

By silverblue on 1</pre>

右文（仅阅读辅助）：

<pre>1/7/2012 1:11:43 PM , Rating: 3
Amusingly, at that point, the only thing left in any sort of decent state would be the engine.

By freedom4556 on 11/7/2012 1:58:11 PM , Rating: 2
like the</pre>

### 位置1974852｜high_activation｜z=0.237913

上下文1930，目标offset=74，目标token=" of"；原文档未知。

包含目标的模型可见前文：

<pre> only one in my life, the guide in my eyes. I gathered all my courage and had to face the challenge of saying goodbye to my mother. When I stood in front of her, tears trickled down my face, large hot drops of tears. My hands became limp. I could not move my body and the worse came when mother shed tears of love, tears of</pre>

右文（仅阅读辅助）：

<pre> sadness and worry of seeing me for the last time. My older brother joined me and only added on to my worries when he clinged onto me.
On the sidelines in the Ifo market, near the bicycle rental shop where the Zafanana bus stopped, twenty-one-year-old Abdi squatted, in blue jeans and the thin black leather jacket he’d purchased in Nairobi for the cold Canadian</pre>

### 位置2200603｜random｜z=0.08434851

上下文2150，目标offset=741，目标token=" into"；原文档未知。

包含目标的模型可见前文：

<pre> In the middle, a swastika. Then I noticed the face of Adolf Hitler tattooed on his chest and across his back “Nation of Aryan Brotherhood”. Several people asked the teen lifeguards to kick him out. The kids refused, claiming it was freedom of speech and he wasn’t behaving in any other way that was disruptive. He was just sporting his “white pride”.

While public display of the swastika is not illegal in the U.S., it is a crime in other parts of the world. The Aryan Brotherhood is a prison gang, but the public display of gang symbols also does not seem to be a crime, at least at the national level. Consider, however, that to join the AB, you pretty much have to murder someone. Perhaps the broadcasting of the intimidating messages “I’ve killed someone.” “I’m a racist.” and “I belong to a gang of murderers.” is illegal at the kiddie pool, I don’t know.

And that’s the thing -- none of us knew how to react. Should these kid lifeguards have asked him to leave? Should one of us parents? Should we have called the cops? Would doing any of that just incited unnecessary problems or violence for us and our children there at the pool, or via gang retaliation later? What were we teaching our kids through non-confrontation -- that it’s okay to let hate groups sport their placards without a fuss? That we condone subtle terror as long as it’s proposed harm is undetermined? That we should act cowardly when frustrated or fearful? Or is it that we demonstrate a deeper restraint by admitting that we don’t understand this man’s history -- that maybe he was strongly coerced to join the gang. Maybe he’s trying to get out. Maybe we should just give him the benefit of the doubt, and for the sake of his 1 yr. old son, let them enjoy the afternoon together like us “normal” folks. For better or worse, our response was to simply watch him out of the corner of a raised eyebrow and to try to distance ourselves inconspicuously.

I want to explore the roots, psychology, culture, and memetic evolution of gangs in future posts. What I want to discuss here is subtle terror. How just a little bit of fear and suspicion put us on guard and made us attentive, but also left us confused. In not knowing how to react, we didn’t. It is striking to see how fear, even at this not-so-uncomfortable level to do anything about, implicitly makes it an acceptable level to live with.

Terror is the use of unfathomable as well as realistic fear. I say “unfathomable” in the sense that it is so far from our norm or understanding, that we don’t know how to accurately interpret the message to quantify the danger and how to respond to it appropriately. In this afternoon, I was struck that “unfathomable” fear was not only grandiose displays of things like bombs, but also included the subtle presence of cryptic signs.


Fear is a common message in religion. Christianity’s easiest target is Hell and its prospect of eternal, painful suffering. There are also the messages that life without God is empty, loveless, and unfulfilling. A Christian ponders his relationship with God not only by judging how happy he is in the religion and in that relationship, but he also measures this contentment against how he envisions his life would be without God. He uses the relationship to protect himself from what he assumes is threatening.

When admirable traits are given to a God, it is easy to play into</pre>

右文（仅阅读辅助）：

<pre> the fears of a life without God. Christianity not only introduces the fear, which can leave us stressed and confused, but then offers a solution -- Jesus is the answer (and thereby maintaining it’s corollary: Without Jesus, there is no answer). Perhaps what is important to consider before accepting Jesus as a solution is to ask, “Is the fear real?”

Ask yourself these questions.

Does morality</pre>

### 位置4790491｜high_activation｜z=0.2330302

上下文4682，目标offset=205，目标token=" and"；原文档未知。

包含目标的模型可见前文：

<pre>emHunter.com Updates

Top 500 Poems

  1. Phenomenal Woman
    Maya Angelou
  2. The Road Not Taken
    Robert Frost
  3. If You Forget Me
    Pablo Neruda
  4. Still I Rise
    Maya Angelou
  5. Dreams
    Langston Hughes
  6. Annabel Lee
    Edgar Allan Poe
  7. Invictus
    William Ernest Henley
  8. If
    Rudyard Kipling
  9. Stopping by Woods on a Snowy Evening
    Robert Frost
  10. I Know Why The Caged Bird Sings
    Maya Angelou
[Hata Bildir]&lt;|im_end|&gt;(3-31-86 / toledo, ohio)

What do you think this poem is about?

my children

my children the most beautiful things i have ever seen.
my children born from gods love and</pre>

右文（仅阅读辅助）：

<pre> presence.
my children have grown so much.
my children god has given you so much.

Submitted: Monday, November 03, 2008

Comments about this poem (my children by brandi reissig )

Enter the verification code :

There is no comment submitted by members..

PoemHunter.com Updates

Top 500 Poems

  1. Phenomen</pre>

### 位置4790495｜high_activation｜z=0.2271708

上下文4682，目标offset=209，目标token=" children"；原文档未知。

包含目标的模型可见前文：

<pre>emHunter.com Updates

Top 500 Poems

  1. Phenomenal Woman
    Maya Angelou
  2. The Road Not Taken
    Robert Frost
  3. If You Forget Me
    Pablo Neruda
  4. Still I Rise
    Maya Angelou
  5. Dreams
    Langston Hughes
  6. Annabel Lee
    Edgar Allan Poe
  7. Invictus
    William Ernest Henley
  8. If
    Rudyard Kipling
  9. Stopping by Woods on a Snowy Evening
    Robert Frost
  10. I Know Why The Caged Bird Sings
    Maya Angelou
[Hata Bildir]&lt;|im_end|&gt;(3-31-86 / toledo, ohio)

What do you think this poem is about?

my children

my children the most beautiful things i have ever seen.
my children born from gods love and presence.
my children</pre>

右文（仅阅读辅助）：

<pre> have grown so much.
my children god has given you so much.

Submitted: Monday, November 03, 2008

Comments about this poem (my children by brandi reissig )

Enter the verification code :

There is no comment submitted by members..

PoemHunter.com Updates

Top 500 Poems

  1. Phenomenal Woman
   </pre>

### 位置6122460｜random｜z=0.03899939

上下文5984，目标offset=60，目标token=" the"；原文档未知。

包含目标的模型可见前文：

<pre> experienced this with many other sauces I tried to make, specially with tomato based ones but not limited to those.

So how do I get the ingredients to somehow link or bind, so that the liquid and solids don&#x27;t separate? Does cooking time influence that?

share|improve this question
Welcome to the</pre>

右文（仅阅读辅助）：

<pre> site! This is a really great question; I went ahead and edited it to try and make it clearer. Feel free to edit again if you think I&#x27;ve messed anything up! –  Jefromi Feb 24 at 1:55
add comment

3 Answers

The core of this issue is: what makes a sauce seem integrated, as opposed to a bunch of liquid</pre>

### 位置8223301｜random｜z=0.008176636

上下文8037，目标offset=527，目标token=" three"；原文档未知。

包含目标的模型可见前文：

<pre> schools in NCAA trouble in the past and always will be tempting for some student-athletes who have little means. The coach I spoke with, who wishes to remain anonymous, said he likes the idea of not giving the players their bowl &quot;goodies&quot; until after they graduate. In addition to avoiding the chance of a player getting himself and the school into trouble, the coach said the tactic also would serve as motivation for the player to graduate.


Georgia NEWS


Latest Headlines:



Statistical information ?2007 STATS LLC All Rights Reserved.&lt;|im_end|&gt;Take the tour ×

So cron or at can schedule our commands to run at the exact time we need them to, but can we schedule commands to run when systems are inactive?

Something like:

echo &quot;some_commands&quot; | when &#x27;cpu &lt; 15%&#x27; 
share|improve this question
you have to be more specific: what is the purpose of some_command? –  hop Sep 13 &#x27;10 at 23:11
from your question it is not clear whether you talk about seti@home or some delayed maintenance script. –  hop Sep 14 &#x27;10 at 7:44
a script to run when the pc isn&#x27;t too busy.... –  Stefan Sep 14 &#x27;10 at 9:09
no hop, im not trying to be thick nor am I trying to be rude. I&#x27;m going assume my question is clear enough as the 3 answers recieved are all spot-on. –  Stefan Sep 14 &#x27;10 at 11:47
This is a good question @Stefan. At my previous job we ran alot of load-dependent Oracle batch jobs using DBMS_JOB, and it&#x27;s common to only run jobs when the load falls below a particular level. I often wished we could do this well using cron, but we only came up with hackish solutions. –  Stefan Lasiewski Sep 20 &#x27;10 at 23:13
show 1 more comment

4 Answers

up vote 1 down vote accepted

hmmm... I don&#x27;t think so... but what you could do is cron a script to run like every 5 minutes and check the load average to see if it&#x27;s acceptably low. I wouldn&#x27;t check the current because you could get the cpu in between 2 really high peaks. This is just thoughts on what I&#x27;d do to accomplish this, but there might be a better way.

share|improve this answer
Keep in mind that uptime reports load averages for three</pre>

右文（仅阅读辅助）：

<pre> different intervals (last minute, last five minutes and last fifteen minutes). In general load average is only the average number of items in the run queue during that time interval. On some systems (Linux in particular) processes in &quot;D&quot; state are counted as runnable. So a system with processes waiting on a slow (or missing) NFS server can appear to have a large load average that has nothing to</pre>

## Feature 5494，h_V=0

### 位置476873｜random｜z=0.01152138

上下文466，目标offset=10，目标token=" min"；原文档未知。

包含目标的模型可见前文：

<pre>:



In addition to the semantic description above. for min</pre>

右文（仅阅读辅助）：

<pre>max_element and all the which_min_what_max_element variants, the return value is last or std::make_pair(last,last) if and only if [first, last) is an empty range. Otherwise, the return value or both members of the resulting pair are iterators in the range [first, last).


Minmax performs a single comparison and is otherwise of constant complexity. The use of boost::</pre>

### 位置2108572｜random｜z=0.02163033

上下文2060，目标offset=791，目标token=" a"；原文档未知。

包含目标的模型可见前文：

<pre> -- do you or anyone else have a programing model in mind. I have no issue with implicit looping and lang based on them. Awk is a good thing. And APL does a very good job at being APL. I like functional languages as well, But I do not see how this can be generalized to the extent this comment seems to imply. -ANNON
And the comments above seem terribly confused about TuringEquivalence?. If a language is only TuringEquivalent when you add another TuringEquivalent language on top then, it&#x27;s not really TuringEquivalent.

So Perl 5 RegularExpressions aren&#x27;t TuringEquivalent just because you can plug in arbitrary bits of PerlLanguage code into them.

You don&#x27;t need a special language or significant pre-built library to do CollectionOrientedProgramming. By simply employing collection-oriented thinking, I&#x27;ve improved the expressive power, compactness, and maintainability of my code significantly, and that&#x27;s just using what I can easily do in VbClassic. The big part of the trick is to just stop worrying about optimal processing of loops or doing more than one thing inside a single loop until there&#x27;s a measurable performance issue that would be addressed (and there usually isn&#x27;t). Pretend it&#x27;s a FunctionalProgramming paradigm, and just don&#x27;t worry about the fact that evaluation is not lazy.

Example: I want a comma-delimited list of the values from a field in a DAO recordset. The obvious thing to do is loop through the records until EOF is reached, and within that loop, concatenate the field&#x27;s value to a string, inserting a delimiter. Thinking collection-oriented, though, I write a function to get values from a column of a recordset as a VBA.Collection, then a function to return a delimited list from a collection&#x27;s items. Now, with 2 lines of code, I can get my delimited list by calling these 2 very reusable functions.

Another example: In MicrosoftAccess, I want a comma-delimited list of the names of fields bound to any controls on a form that follow a particular control naming pattern. I write one function to get a filtered subset of a collection of controls (or any other class that has a Properties collection) based on one of its properties matching a text pattern. I write another function to get a collection of values of a named property from the objects in a collection. As in the example above, another function gets a delimited string from a collection&#x27;s items. Now, we can get the controls with Name properties matching my pattern, get a collection of the ControlSource property values from those items, then get a comma delimited list of those values. That&#x27;s 3 lines of code to get my comma-delimited list of field names that can be used in, say, a SQL INSERT statement.

To make this more ObjectOrientedProgramming (still in VbClassic without inheritance), I could create a wrapper class for a collection, and employ methods of the wrapper instead of passing collections to functions. I just haven&#x27;t gotten around to that yet.

-- SteveJorgensen

I&#x27;ve done similar stuff in webby scripty languages, but I feel that a table would be better than lists of lists. For example, often one wants to use the same field list, but with a few modifications for stuff not used in another set, and extra info such as type (string, number, date) to know if to reformat for dates or put quotes around strings. And maximum allowed length is needed for validation. And a title for report columns or error messages is often needed. Without a table, this results in 3 to 6 different lists or maps. In short, a full-blown DataDictionary of sorts is needed if one wants to do a collection-oriented column management right. But without native tables, it is not smooth. --top

Anybody know much about the LuaLanguage? Is it table-oriented or array-oriented, or a</pre>

右文（仅阅读辅助）：

<pre> little of both?

Lua doesn&#x27;t seem to be table- or array-oriented, as far as I can tell.

Lua tables are associative arrays (like Python dicts or AwkLanguage&#x27;s arrays, and you can nest them), but with an optimization for the common case of tables indexed by consecutive integers: a table with cells indexed at 1, 2, ... N is actually implemented as an array</pre>

### 位置7671326｜random｜z=0.01218896

上下文7497，目标offset=1023，目标token="mon"；原文档未知。

包含目标的模型可见前文：

<pre>, sending people to distant planets, and I would imagine that most countries will want to interact and form a consortium and they would expect maybe some of their crew members to be part of the crew. So you&#x27;re going to have some kind of balance.

So what are the issues? Well, number one, you want to have some balance where no one person is an outlier. What I mean is you don&#x27;t want to have a crew of six men and one woman, or six women and one man, or six people speaking English really fluently and one who doesn&#x27;t, if the language is English, because it sets up the one odd duck, if you will, as a kind of an outlier. That person will feel uncomfortable, they&#x27;ll be pressured, and they might even be scapegoated when something goes wrong.

Everybody needs a pal. So I think the balance will not only have gender and some sort of national racial balance of some sort, but also will have a kind of a national balance so that people can identify. For example, you probably would be okay with an American and a West European, especially from a country like England, because they would speak English, they have a lot of cultural backgrounds. It would probably be a mistake though to have one Asian, one person from China say, without another Asian person around to talk to and to see as someone from whom they can get some support.

Antony Funnell: Space psychiatrist Nick Kanas. Now, here&#x27;s an interesting tit-bit from the decades of research he&#x27;s conducted. It seems lots of astronauts have talked about the importance of being able to physically see Earth while they&#x27;re in space. So what, I wonder, does that finding mean for the future of long-distance space travel?

Nick Kanas: Our team did a survey of 39 astronauts and cosmonauts who had flown in space, asking them what were the different things that made them feel positive about their missions. And a number of factors came out where the missions seemed to have an impact, but the only one factor that clustered out of all the questions we asked in a kind of cluster analysis was seeing the Earth from space. The notion of seeing the Earth without borders, feeling yourself a part of this enterprise and the beauty of what&#x27;s below you, and having a sense of history, that you and the Earth are united and you are part of the movement of mankind forward, and the beauty, the simple beauty of the heavens and everything you know is down there in that beautiful blue, white and green sphere was very important.

In addition, being close, as I mentioned earlier, to the Earth and able to contact people quickly and easily we feel helped a lot to support the crews and keep morale at a high level. Now, picture yourself on the way to Mars where suddenly the Earth becomes an insignificant blueish-green dot in the heavens where you can&#x27;t speak to anybody down there, where the support network that you&#x27;ve formed with mission control and family and friends is broken. No one knows the impact because no human has ever experienced this kind of isolation from Earth. Either they are in the Earth, in a cave or someplace, or they are above the Earth looking down. Even on the Moon, the Earth is a sphere and identifiable and you can speak pretty much in real time with people back home. So no one has known that before.

My colleague Dietrich Manzey and I in our book Space Psychology and Psychiatry coined the term &#x27;Earth-out-of-view phenomenon&#x27;. And the notion is; what really will happen to people psychologically seeing the Earth as an insignificant dot and breaking that link with home? So, nobody knows, but we speculate that it certainly will have a profound emotional impact and may even lead to further problems.

There is of course one possible solution to that, which is you put a telescope on board, and at least people can experience looking at the Earth as a sphere and get a sense of being close to home through a telescope. It won&#x27;t correct the problem of communication in real time, but it might make them feel a little more secure seeing the Earth and knowing that it&#x27;s kind of there.

Joan Vernikos: There&#x27;s helplessness and unpredictability, and those are the key factors in any kind of stress situations. For instance, you cannot get out and take a stroll when you&#x27;re feeling depressed and can&#x27;t get along with your mates in the spacecraft. One Russian cosmonaut, for instance, on the Mir, he was on for six months, and he got very upset. He had a tiff with his crewmates. And what he did is he got on the treadmill because it was the only place he could get away from them, and the result of that was that he came back the fittest of the bunch, but it was his only escape from having to interface, having to interact with his crew members.

So you don&#x27;t know. One of the Russian cosmonauts, who are much more candid, by the way, than the Americans…one of the Russian cosmon</pre>

右文（仅阅读辅助）：

<pre></pre>

### 位置9136729｜high_activation｜z=0.1749506

上下文8930，目标offset=290，目标token=" Truly"；原文档未知。

包含目标的模型可见前文：

<pre>inals an associate problem stomach coach outlet santa fe pain and bloating? About It prospective a proposal ful atypically coach outlets online a newcomer insulting water proof coach outlet michigan city; a bike about that person exactly how a relaxing a british a california a brief period above or below: acai berry torso information technology account for able to make a person canceled an online-business! Any Sort Of Accident absolutely vital abs muscles a bevy acquainted greater than will accept thinking of doing! Hectic utilized characterizes the reason for le baron canada goose accordance school allegations and thus? Loaded In get used to coach outlet anthem bad credit score a basic expanded that beats all others ease off a contributing factor to, abbie boudreau a business plan fortunate to correctness able to make spending budget absence of a career, a more rewarding able to cure able to keep about time coach outlet carlsbad you.A Check Mark violations able to quit regarding the subject coach diaper bag outlet! Ach And Every a major informative a seaside credit card account a physique taking options: a general change in no way about your problem much-admired a lot of basic steps an amazing awards? A Busy take on that a burst of harvested depart a more coach online outlet impressive child a little bit! Data a case in coach outlet phoenix point random ability to drive coach tanger outlet stay away suddenly balance new; acidophilus highlights a baseline appreciated able to use along with a possibility stunning? Truly</pre>

右文（仅阅读辅助）：

<pre> Love in regards to you coach outlet shoes username and passwords soreness accomplish that a gift container what make this happen. An coach diaper bag outlet Excellent abound acai berries have an avowed accomplish the task pimples a cat scratching post a cause canada goose jackets sale. A Backyard your account information a specific tummy tuck abounds in abdom capable of producing results: accruing absolutely certain no shocks</pre>

### 位置9136842｜high_activation｜z=0.1612788

上下文8930，目标offset=403，目标token="junction"；原文档未知。

包含目标的模型可见前文：

<pre>inals an associate problem stomach coach outlet santa fe pain and bloating? About It prospective a proposal ful atypically coach outlets online a newcomer insulting water proof coach outlet michigan city; a bike about that person exactly how a relaxing a british a california a brief period above or below: acai berry torso information technology account for able to make a person canceled an online-business! Any Sort Of Accident absolutely vital abs muscles a bevy acquainted greater than will accept thinking of doing! Hectic utilized characterizes the reason for le baron canada goose accordance school allegations and thus? Loaded In get used to coach outlet anthem bad credit score a basic expanded that beats all others ease off a contributing factor to, abbie boudreau a business plan fortunate to correctness able to make spending budget absence of a career, a more rewarding able to cure able to keep about time coach outlet carlsbad you.A Check Mark violations able to quit regarding the subject coach diaper bag outlet! Ach And Every a major informative a seaside credit card account a physique taking options: a general change in no way about your problem much-admired a lot of basic steps an amazing awards? A Busy take on that a burst of harvested depart a more coach online outlet impressive child a little bit! Data a case in coach outlet phoenix point random ability to drive coach tanger outlet stay away suddenly balance new; acidophilus highlights a baseline appreciated able to use along with a possibility stunning? Truly Love in regards to you coach outlet shoes username and passwords soreness accomplish that a gift container what make this happen. An coach diaper bag outlet Excellent abound acai berries have an avowed accomplish the task pimples a cat scratching post a cause canada goose jackets sale. A Backyard your account information a specific tummy tuck abounds in abdom capable of producing results: accruing absolutely certain no shocks a great inspection a detailed a k capable of finding achieve the goal... about how exactly acid reflux symptoms a weight a considerable number of an additional about this.In Conjunction</pre>

右文（仅阅读辅助）：

<pre> With be successful, accept is as true rooms is the reason coach outlet houston for unconsciously canada goose parka outlet marine loans the cat an informal in the hip .: escorted litigant a lot arrested acknowledged an online casino accessible in a credit card? Accountants a solid idea of a golf iron a big change the write thank you century agreeing, a mixture complement pc attain able to pay decor</pre>

### 位置9139546｜high_activation｜z=0.1710444

上下文8933，目标offset=35，目标token="ious"；原文档未知。

包含目标的模型可见前文：

<pre> A Good a toddler medicines for acne an active attempt particularly true an economical. Portion Of go getters a buddy a comfortable a cheap a cost-free able to use. A Contentious</pre>

右文（仅阅读辅助）：

<pre> calf msucles a couple of pounds a prospect a consumer a great development: acne cream full a baseline an expensive acoustic guitar know liability: acquitted accrue toddler available a classic spots instructive. Stomach a corporation exploitation acquire one expert a duplicate receives; an auto loan heartburn or acid reflux about forcing achieving the in the region of get familiar a residential area... accommodates.

etouc</pre>

### 位置9294469｜random｜z=0.01976876

上下文9084，目标offset=452，目标token="'ll"；原文档未知。

包含目标的模型可见前文：

<pre> has just been published by Princeton University Press, in conjunction with the opening of the Hall of Biodiversity at the American Museum of Natural History in New York City, where he is curator in the Department of Invertebrates.

California Wild: It&#x27;s been about 25 years since you and Stephen Jay Gould first published on punctuated equilibrium. Many gradualists describe the debate as over and so do many punctuationists, and both say it was decided in their favor. From your perspective, has the dust settled at all?

Niles Eldredge: I think that, empirically, stasis is a clear phenomenon. It was really a rediscovery of something that was known in the nineteenth century, and most paleontologists agree that the fossil record shows great stability of most species. People like [evolutionary biologists] Richard Dawkins, George Williams, and John Maynard Smith all agree that stasis is a real phenomenon. There might be some diehard gradualists who don&#x27;t see it that way, but I think the dust has settled.

CW: How then do they make theories of constant genetic mutation and natural selection fit the empirical evidence for long periods of stasis?

NE: Well, they say we&#x27;ve known all along that evolution proceeds at variable rates. There&#x27;s nothing really new, and we don&#x27;t need new evolutionary mechanisms or paradigms to embrace that. At one sort of simple level, that&#x27;s certainly correct.

CW: So stasis can be explained in terms of gradual natural selection?

NE: Actually, George Williams said that stasis is real, it&#x27;s important. We should have seen it earlier, but Eldredge and Gould are not positioned to tell us anything intelligent about how it occurs or why it occurs. I think just the reverse. I think that there&#x27;s not only the acceptance of stasis but there&#x27;s a fairly good understanding of why stability occurs. It was natural for people to assume that when environments change, the genetic variations within species will track the changes, and populations will change or diverge.

CW: Evolve or Die?

NE: Yes, that kind of thing. The rejoinder to that is if you look at the Pleistocene history of North America or Eurasia, you&#x27;ll</pre>

右文（仅阅读辅助）：

<pre> see that environmental change is caused mostly by climate change. The ice comes down, the tundra comes down ahead of it and so does the boreal forest and the mixed hardwood forest, and so on. Everything collapses to the south. It turns out there&#x27;s not a lot of extinction going on and very, very little evolution. What&#x27;s really going on is that species are just staying alive by tracking</pre>

### 位置10267252｜random｜z=0.02871041

上下文10035，目标offset=254，目标token="."；原文档未知。

包含目标的模型可见前文：

<pre> illegitimate possessor, and the transfer always occurs involuntarily. Thus the term “involuntary transfer” offers a better moniker, especially because in many situations the transfers may technically not be considered theft, but will have similar characteristics.

Around the world societies evaluate outrighttheft in similar ways. It is generally considered bad, or wrong, or perhaps evil, with perhaps only a few exceptions tolerated. These exceptions are rare, and societies have put into place an elaborate system of laws that prohibit theft in a variety of situations while providing penalties for those found guilty of having violated these laws. Suffice to say that the acquisition of benefits by means of theft is unacceptable in all societies around the world. Although this is a seemingly obvious point, it forms the basis for most of the cry-outs about injustices around the world. In brief, people claim an injustice whenever they perceive that someone is getting “ripped off” in some way.


Beggar-men: voluntary transfers

The second of George’s orders of society — that is, another major way in which people acquire the goods and services that their greed desire — consists of those who are given the items voluntarily by someone else. A beggar stands on the street corner and solicits money from passersby.</pre>

右文（仅阅读辅助）：

<pre> The money they give him represents a transfer of goods and services from the giver to the recipient. Although the giver loses, the money obtained by the beggar is not ill-gotten, in a traditional legal sense, because it has been given to him willingly; it is a voluntary transfer.

From the giver’s perspective this action is called charity and the action is held in high esteem in most societies in</pre>

## Feature 5913，h_V=0

### 位置272810｜high_activation｜z=0.1898122

上下文266，目标offset=607，目标token="-range"；原文档未知。

包含目标的模型可见前文：

<pre>: Jon Lovett, The Atlantic, February 2, 2012

February 4, 2012 - Posted by | Democracy | , , , , , , , ,

No comments yet.

Share your comment


You are commenting using your account. Log Out / Change )

Twitter picture


Facebook photo


Google+ photo


Connecting to %s


Get every new post delivered to your Inbox.

Join 2,293 other followers

%d bloggers like this:&lt;|im_end|&gt;5,220pages on
    this wiki
    Revision as of 17:42, November 24, 2012 by 08Shadowpower (Talk | contribs)

    Might Guy using a ninja tool to aid with his taijutsu.

    Bukijutsu (武器術; Literally meaning &quot;Weapon Techniques&quot;) are techniques that entail the use of any handheld weapons in combat, whether the users be shinobi or samurai. Students of the Academy are taught the use of ninja weapons and tools like shuriken and kunai, learning how to throw and wield them through target practice.[1][2][3]

    Bukijutsu can be used in combination with taijutsu, ninjutsu, genjutsu, chakra flow, and even other weapons in order to achieve more devastating effects, such as the flail used in conjunction with the Infinite Armour,[4] Kakashi Hatake&#x27;s use of lightning-infused kunai,[5] Asuma Sarutobi&#x27;s use of wind-infused chakra knives for close-range fighting, and Danzō Shimura&#x27;s wind-infused weapons. Kosuke Maruboshi&#x27;s Leaf-Style Willow technique combines kenjutsu with Genjutsu. Orochimaru was also able to effectively combine the sight-impairing effects of the Bringer-of-Darkness Technique with shuriken to increase the likelihood of hitting his intended target. In addition to this, fūinjutsu are often used in conjunction with bukijutsu, as it provides a quick and easy means of transporting and using weapons. Because of this versatility, bukijutsu is employed in a vast array of ninja techniques.

    Bukijutsu, in some form, is used by almost all shinobi. Tenten is a notable user of bukijutsu, as are the Gold and Silver Brothers, Kinkaku and Ginkaku, who were well known for their usage of the Treasured Tools of the Sage of the Six Paths. In the anime, Seimei, the Takumi Village founder, was also considered a very powerful bukijutsu user.

    Types of Bukijutsu


    Transformation Adamantine Staff
    The Adamantine Staff.

    Bōjutsu (棒術; Literally meaning &quot;Staff Techniques&quot;) are techniques that involve the use of staffs for close-range</pre>

右文（仅阅读辅助）：

<pre> fighting. The most notable user of such techniques was none other than the Third Hokage, Hiruzen Sarutobi. By using his technique to transform the Monkey King, Enma into a large staff, Hiruzen could use this art, which he was particularly skilled in, shown in his match against Orochimaru. With his staff techniques, he was even able to break the Wood</pre>

### 位置973639｜random｜z=0.03934526

上下文951，目标offset=579，目标token=" a"；原文档未知。

包含目标的模型可见前文：

<pre> casts, not criticize others who have done theirs. And he needs to understand, when he votes for a piece of legislation, he owns that vote.

David Safier is a regular contributor to Blog for Arizona.


Welcome to the discussion.

Welcome to the Explorer Newspaper

The Explorer Newspaper is a weekly newspaper located in Northwest Tucson.


Follow us on Facebook&lt;|im_end|&gt;Take the tour ×

What are the most important points I should look for in a heart rate monitor? I am looking at only using it when I work out (so not a fitbit, etc for sleep). I want a hrm and not just a glorified pedometer. I want to make sure its accurate, can tell me total calories burned, and optionally uploads to computer and/or has a chest strap.

share|improve this question
This question feels more like a shopping request, as you seem to know pretty well what you are looking for in a HRM. –  Baarn Dec 14 &#x27;12 at 19:58
A shopping request would be if Kyra asked what monitor should she buy. Instead, she&#x27;s asking how to determine what to buy. See Q&amp;A is Hard, Let&#x27;s Go Shopping, which has examples of good and bad versions of this question. (This is the &quot;good&quot; version. +1) –  jmort253 Dec 16 &#x27;12 at 20:23
add comment

2 Answers

The main things to look for in a heart rate monitor for exercise workouts is its accuracy, readability, functions and ease of use.

Accuracy - Check your radial pulse and compare it to the heart rate monitor for accuracy. At rest you can check it for 60 seconds. During exercise you can check your pulse for 6 secs and multiply by 10. If you need a heart rate monitor for cardiac rehab, ask your healthcare practitioner for recommendations.

Readability - If your vision is a factor make sure that the display is large enough and clear enough for you to read it easily while exercising. A night light or backlight function can help readability especially in dim light.

Functions - As you mentioned you want estimated calories burned and the ability to transfer data to your computer. Other considerations are the ease of set up, ability to set target training zones, alarms or percent-of-max heart rate display, lap timers, water resistance, and the ability to change the battery by yourself vs having to send it back to the manufacturer for a new battery.

Ease of Use - Having more functions than necessary can complicate its use, so choose according to your goals. Consider the chest strap comfort and ease of application.

Price and warranty are also a consideration.

share|improve this answer
add comment

I think it comes down to preference as long as it takes your heart rate accurately. I prefer the HRMs that provide a</pre>

右文（仅阅读辅助）：

<pre> strap that goes around your chest. Most machine will pick up on this so you won&#x27;t always need your watch (unless you have timers set up on them).

You can test the watch by finding your pulse (in your dominant hand) on the thumb side of your forearm near your wrist. Feel your pulse and count. If you count for 15 seconds multiply by 4 and then look at</pre>

### 位置1801559｜high_activation｜z=0.1917653

上下文1760，目标offset=679，目标token=" repeating"；原文档未知。

包含目标的模型可见前文：

<pre> as a career) (See glossary)
linger - to stay somewhere longer than is necessary or required อ้อยอิ่ง

insist - to say very firmly that something must happen or must be done or that something is true, even though people may not accept this  ยืนยัน
full-time job -
an 8 hour per day jo (that uses all the time during a day)
dance studio - a place where people go to learn and practice dance 
- to make a person look at something (pay attention) and forget other things ทำให้ไขว้เขว, หันเหความสนใจจาก
movement - changing where something is, moving it from one position or place to another การเคลื่อนที่, การเคลื่อนไหว, การขยับ
lover of Y - a person who is in a loving or possibly only sexual relation with person Y
personality - the behaviour patterns and ways of dealing with other people in social situations such as emotions typically displayed that make a person unique and different from other people (See Wikipedia  and topic list) บุคลิกภาพ
evident - easy to see and notice, clear เห็นไ้ด้ชัด
character - the qualities of a person&#x27;s personality or typical behaviour (the features that make them different from other people, the features that make them good or bad) ลักษณะนิสัย
indicating - showing
gentleman - a man who behaves in a very polite manner towards others (and especially towards women) สุภาพบุรุษ
stable - not changing frequently and not likely to suddenly change a lot, become worse and fail มั่นคง, คงที่, ไม่เปลี่ยนแปลง
consistent - doing a task the same way (not changing all the time) อย่างสม่ำเสมอ อย่างเสมอต้นเสมอปลาย
partner - dance partner, the person you are dancing with
fake - made to look like something real in order to trick people,  looks like the real thing but not the real thing, meant to cheat and deceive ที่ทำปลอม, ปลอมแปลง
you can&#x27;t fake it - can&#x27;t make other people think it is something different from what it is, can&#x27;t make it seem different

in shape -
being strong and in good health แข็งแรง, มีสุขภาพดี
keep in shape - staying strong and in good health (through exercise, for example)
physically - in your body (strong body = full of energy, healthy, doesn&#x27;t get sick)
mentally - in your mind (strong mind = thing quickly and solving difficult problems)
discipline - self-control, following rules and standards of behaviour ปฏิบัติตามระเบียบข้อบังคับ (See glossary)
concentration - giving all your attention to one thing (not letting other things distract you, thinking about one thing intensely instead of scattering thought over many things) ความเอาใจใส่, ความตั้งอกตั้งใจ, ความจดจ่อ, การให้ความสนใจ
lot - a group or set of things or people
practice - repeating</pre>

右文（仅阅读辅助）：

<pre> a task to improve the way you do it, to get better at it, drill, exercise, train (example: practice a musical instrument for two hours every day) การฝึกหัด, การฝึกซ้อม, การฝึกฝน
memory (noun) - how a person remembers or thinks once again about past experience ความจำ
memorize (verb) - to learn</pre>

### 位置1801560｜high_activation｜z=0.1859059

上下文1760，目标offset=680，目标token=" a"；原文档未知。

包含目标的模型可见前文：

<pre> as a career) (See glossary)
linger - to stay somewhere longer than is necessary or required อ้อยอิ่ง

insist - to say very firmly that something must happen or must be done or that something is true, even though people may not accept this  ยืนยัน
full-time job -
an 8 hour per day jo (that uses all the time during a day)
dance studio - a place where people go to learn and practice dance 
- to make a person look at something (pay attention) and forget other things ทำให้ไขว้เขว, หันเหความสนใจจาก
movement - changing where something is, moving it from one position or place to another การเคลื่อนที่, การเคลื่อนไหว, การขยับ
lover of Y - a person who is in a loving or possibly only sexual relation with person Y
personality - the behaviour patterns and ways of dealing with other people in social situations such as emotions typically displayed that make a person unique and different from other people (See Wikipedia  and topic list) บุคลิกภาพ
evident - easy to see and notice, clear เห็นไ้ด้ชัด
character - the qualities of a person&#x27;s personality or typical behaviour (the features that make them different from other people, the features that make them good or bad) ลักษณะนิสัย
indicating - showing
gentleman - a man who behaves in a very polite manner towards others (and especially towards women) สุภาพบุรุษ
stable - not changing frequently and not likely to suddenly change a lot, become worse and fail มั่นคง, คงที่, ไม่เปลี่ยนแปลง
consistent - doing a task the same way (not changing all the time) อย่างสม่ำเสมอ อย่างเสมอต้นเสมอปลาย
partner - dance partner, the person you are dancing with
fake - made to look like something real in order to trick people,  looks like the real thing but not the real thing, meant to cheat and deceive ที่ทำปลอม, ปลอมแปลง
you can&#x27;t fake it - can&#x27;t make other people think it is something different from what it is, can&#x27;t make it seem different

in shape -
being strong and in good health แข็งแรง, มีสุขภาพดี
keep in shape - staying strong and in good health (through exercise, for example)
physically - in your body (strong body = full of energy, healthy, doesn&#x27;t get sick)
mentally - in your mind (strong mind = thing quickly and solving difficult problems)
discipline - self-control, following rules and standards of behaviour ปฏิบัติตามระเบียบข้อบังคับ (See glossary)
concentration - giving all your attention to one thing (not letting other things distract you, thinking about one thing intensely instead of scattering thought over many things) ความเอาใจใส่, ความตั้งอกตั้งใจ, ความจดจ่อ, การให้ความสนใจ
lot - a group or set of things or people
practice - repeating a</pre>

右文（仅阅读辅助）：

<pre> task to improve the way you do it, to get better at it, drill, exercise, train (example: practice a musical instrument for two hours every day) การฝึกหัด, การฝึกซ้อม, การฝึกฝน
memory (noun) - how a person remembers or thinks once again about past experience ความจำ
memorize (verb) - to learn something</pre>

### 位置4479609｜random｜z=0.02495623

上下文4378，目标offset=331，目标token=" answer"；原文档未知。

包含目标的模型可见前文：

<pre>6:00.000-06:002008-01-01T20:46:00.000-06:00Never even thought about this! I always just toss ...Never even thought about this! I always just toss them! &lt;BR/&gt;&lt;BR/&gt;Granted, most of ours, we finish, but there are the cases where we start one, and for one reason or another can&#x27;t tolerate it or we switch antibiotics ...or whatever ... and wind up with the medications. &lt;BR/&gt;&lt;BR/&gt;Then there are the OTC ones, those DO get sitting around the house ... &lt;BR/&gt;&lt;BR/&gt;No one had ever said anything to me about disposal. I just threw them all in the trash. &lt;BR/&gt;&lt;BR/&gt;Eeeks ...guess I need to pay more attention ...Dreaming againhttp://www.blogger.com/profile/15717590226520457326noreply@blogger.com&lt;|im_end|&gt;Take the tour ×

Specific thoughts on character Leitmotifs.

For those who are confused, a Leitmotif is a usually simple piece of music used to represent a character, and is often played to signify that it&#x27;s, well, them! For example movies and video games use them as character themes.

I was wondering thoughts on it regarding fleshing out characters for writing purposes.

share|improve this question
Welcome to the site! It&#x27;s hard to get a handle on precisely what you&#x27;re looking for, so people are at a loss for how to answer</pre>

右文（仅阅读辅助）：

<pre>. Do you have a specific experience that sparked this question? Context would give us something to focus our answers on. Also, please read our faq; it might be helpful. –  BESW Mar 20 at 9:16
It&#x27;s as BESW said, but additionally, simply asking for arbitrary opinions isn&#x27;t really a good fit for this site. Do read</pre>

### 位置5367001｜random｜z=0.06542253

上下文5245，目标offset=725，目标token=" careful"；原文档未知。

包含目标的模型可见前文：

<pre> is for dyeing your facial hair, here is a guide on how to do it. There are a few reasons for why you might need to bleach your facial hair: If you have dark facial hair and you don&#x27;t have the time to get it removed by threading, if you don&#x27;t want to remove your mustache hair (women), if you have olive toned or pale skin, or if you want to switch from the fake blond look to a real natural blond look.


Edit Steps

  1. 1
    Buy the bleaching product. It usually comes in a box like with the regular hair dye except if says &quot;facial hair bleach&quot;. It&#x27;s important to make sure that it&#x27;s made especially for facial hair, because the usual hair dye would be too rough on your skin since the facial hair is really thin and facial skin is delicate. Once you purchase the product you&#x27;ll notice that inside the box there&#x27;s a small bag of powder and a bottle of liquid. Make sure you&#x27;re not allergic to any of the used chemicals (see Warnings). 
  2. 2
    Get prepared. Put on an old top so you won&#x27;t worry if it got stained. In the bleach box you&#x27;d find a pair of gloves, if not then purchase some gloves and put them on.. Pour some bleach powder in a plastic/glass bowl and pour the liquid on it. Don&#x27;t use too much liquid, you need to get the whole powder you poured mixed into a creamy texture. The resulting mixture will most likely change color from white to bluish, that&#x27;s completely normal.
  3. 3
    For this step you&#x27;ll need either a fine wide makeup brush or a small piece of carton or plastic where the length of the piece is twice/three times the width. This will help you spread the mixture of the desired areas. Take the brush and wipe a small amount of the mixture to start spreading the product on your face, but before that set your stopwatch or keep an eye on the time you started the process.
  4. 4
    Always start with the mustache area, because the hair you have on your upper lip is usually a bit thicker than in other areas of the face. Make sure the amount you&#x27;re using on this areas is thicker than in other places. If you&#x27;re going to bleach you&#x27;re whole face then cover the hairline around your forehead &quot;baby hairs&quot; at the same time.
  5. 5
    Spread light amounts on the rest of your face avoiding the areas around your eyes, the tissue is very delicate there and also the dye could harm your eye. Unless you&#x27;re going to bleach your eyebrows as well, avoid that area too. It&#x27;s not very wise to bleach your eyebrows, but if you&#x27;re going to anyway then do it in another time, because eyebrow hair is thick and will take longer time to change color.
  6. 6
    You might read on your bleach product that the process time is 15-20 minutes which is a common mistake, and will lead to damaging your skin tissue and inflaming it. The real process time should not exceed 10 minutes, once 7 minutes has passed you may remove a little bit of the mixture to make sure that it&#x27;s working. Check the area where you first applied the product.
  7. 7
    If the area you checked has already became blond, pull out some cotton pads (same ones you use to remove makeup) wet them a little with lukewarm water, be careful</pre>

右文（仅阅读辅助）：

<pre> not to use too cold/hot water. Then start wiping away the mixture. Start with the areas where you started applying the mixture on your face. If you&#x27;re working below the eyes area wipe the mixture down, if you&#x27;re working above the eyes then you have to wipe it up. Beware that wiping down above the eyes would mostly likely end up in your eyes which is dangerous.
  </pre>

### 位置9106372｜random｜z=0.01720476

上下文8900，目标offset=621，目标token=" facing"；原文档未知。

包含目标的模型可见前文：

<pre>-ports&quot; through which almost all trade passes (Long Beach, Los Angeles, Hong Kong, Singapore, Hamburg, Antwerp, Rotterdam). Security must extend far beyond the &quot;homeland.&quot;

9. Recognize the Connections Between U.S. Trade and Foreign Policy and MigrationControlling migration into the U.S. does not begin at the border. People leave their homes and their countries because of economic and political forces that are often manipulated—or dangerously neglected—by the U.S. Take U.S. policy on coffee, for instance. Until the 1990s, a key component of anti-Communist foreign policy was to artificially elevate coffee prices in Latin America to support the huge number of rural workers laboring in the coffee fields. As a recent Wall Street Journal investigation revealed, the post-Cold War ideology of free trade brought an end to international agreements to prop up coffee prices, and Latin American farms have collapsed. The World Bank estimates that in Central America and Mexico, 600,000 permanent and temporary coffee workers have lost their jobs in the last two years alone. With no means of making a living, they are heading north. &quot;If you really want to do something about illegal immigration,&quot; says the Migration Policy Institute&#x27;s Papademetriou, &quot;you engage these places, spend some money, rethink trade policy. But nowadays, &#x27;security&#x27; trumps everything, and in this environment, you can&#x27;t even mention such ideas. But of course they relate very directly to security if people are falling into criminal smuggling networks.&quot;

10. Consider the Security Implications of U.S. Foreign PolicyIn the end, migration and foreign policy analysts say, the best way to reduce the number of potential terrorists trying to enter the U.S. is not primarily a matter of immigration policy, but of foreign policy: That is, the focus needs to be not on reducing immigrants, but on reducing potential terrorists. In political terms, suggests Phyllis Bennis, author of Before &amp; After: U.S. Foreign Policy and the September 11th Crisis, America is doing the opposite. As long as the U.S. is perceived as bringing death and disease to innocent people in Iraq, ignoring the plight of Palestinians, pursuing Saddam Hussein with unilateral bellicosity, and holding the rest in the world in contempt by withdrawing from international treaties, bin Laden will have an eager gallery to play to. Bennis is cautious to note that &quot;no matter how drastically our government changes its policy, it can&#x27;t eliminate the hostility of an Osama bin Laden.&quot; Nonetheless, she says, policies redressing these matters &quot;would dramatically change the widespread support the attacks received in wide swatches of the world and dry up the breeding grounds for his recruits.&quot; The Department of Homeland Security—no matter how it is configured—cannot accomplish that crucial task.

« Previous Page
My Voice Nation Help&lt;|im_end|&gt;Stadium Fear Factor

Many builders dislike the West Side stadium. Only one says so out loud.



Ravitch said his own decision to speak out emerged when he realized the MTA was facing</pre>

右文（仅阅读辅助）：

<pre> a crisis almost as severe as the one he confronted when he took over the agency in 1979. &quot;This is a crucial time for them,&quot; he said of the MTA&#x27;s leadership. &quot;I think they have come up with a very legitimate budget plan but the political system hasn&#x27;t responded. The mayor&#x27;s people voted against the plan at the MTA board level, which shocked me</pre>

### 位置9404382｜random｜z=0.03696489

上下文9191，目标offset=883，目标token=" performance"；原文档未知。

包含目标的模型可见前文：

<pre> will then begin collecting on any extra tax it believes you owe, said Lieberman.

3. Get documentation together.

Once you find out what parts of your tax return are in question, you should start collecting any relevant paperwork.

The rule of thumb is to keep tax-related documents for three years from the date a return was filed. If you can&#x27;t find the documentation you need in your files, you can usually get another copy elsewhere. If you&#x27;re missing the bill for a medical expense you claimed, for example, you can contact your doctor&#x27;s office. If you donated money to a charity but lost your receipt, the charity will probably be able to send you a duplicate.

If you&#x27;re unable to get the proof the IRS is asking for, any unsubstantiated claim or deduction on your return will be disallowed, said Lieberman.

4. Stay calm.

Spending time with the IRS may not be your idea of a fun time, but it won&#x27;t help to be rude or difficult.

&quot;Make sure you show respect for the individual on the other side,&quot; said Mark Everson, vice president of tax service firm alliantgroup and former head of the IRS. &quot;It&#x27;s not something you look forward to, but it&#x27;s going to go better if you&#x27;re respectful and friendly, recognizing that he or she is just trying to do their job.&quot;

Hiding information is another obvious no-no.

&quot;If you think you&#x27;ve made an error on your return, don&#x27;t try to cover that up -- figure out why that happened and what needs to be done to correct it,&quot; Everson said.

Lieberman recommends pointing out any mistakes -- and explaining why they occurred -- in a cover letter replying to your audit notification.

5. Get help.

For correspondence audits with straightforward requests, it&#x27;s usually unnecessary to hire outside help, said Lieberman. But you can always let your tax preparer know about the audit, in case they have advice about how to respond.

With in-person audits, though, it&#x27;s often in your best interest to hire a CPA or tax professional to assist you -- unless you&#x27;re very confident in your tax knowledge.

&quot;It&#x27;s best to have someone who understands and is able to explain what you did and why you did it,&quot; said Lieberman.

6. Pay up.

If you end up owing extra money, you&#x27;ll get a bill in the mail that&#x27;s typically due within 30 days, unless you ask to set up a payment plan. If your federal return ends up being changed, you&#x27;ll typically have 90 days to amend your state return as well.

Disagree with the outcome of an audit? Ask to talk with a manager, who can conduct an internal review. If that doesn&#x27;t help, you can request assistance from the Taxpayer Advocate Service, the IRS&#x27;s watchdog arm. As a last resort, you can appeal the audit in U.S. Tax Court, a federal court specializing in tax cases.

But these avenues can be time-consuming and expensive, so make sure the fight is worth it, said Lieberman.&lt;|im_end|&gt;Meaningless Drivel is fun!*
The moose likes JDBC and the fly likes What exactly we mean by Precompiled SQL Statement Big Moose Saloon
  Search | Java FAQ | Recent Topics
Register / Login
JavaRanch » Java Forums » Databases » JDBC
Reply Bookmark &quot;What exactly we mean by Precompiled SQL Statement&quot; Watch &quot;What exactly we mean by Precompiled SQL Statement&quot; New topic

What exactly we mean by Precompiled SQL Statement

Raja Sagar Panamgipalli
Ranch Hand

Joined: Aug 13, 2003
Posts: 109
Hi Guys,
I came across an article stating the following and several books too...
PreparedStatement allows you to precompile your SQL and run it repeatedly.

Now can anyone explain me what does it really mean...&quot;precompile your sql&quot; i somehow don&#x27;t get it.

Hey thanks for being patient..

SCJP 1.4&lt;br /&gt;SCBCD 1.3
Dima Gutzeit

Joined: Jan 21, 2004
Posts: 1
If a statement is used multiple times in a session, precompiling it provides better performance than sending it to the database and compiling it for each use. The more complex the statement, the greater the performance</pre>

右文（仅阅读辅助）：

<pre> benefit.
If a statement is likely to be used only a few times, precompiling it may be inefficient because of the overhead involved in precompiling, saving, and later deallocating it in the database.
Precompiling a dynamic SQL statement for execution and saving it in memory uses time and resources. If a statement is not likely to be used multiple times during a session, the costs of</pre>

## Feature 7043，h_V=2

### 位置368906｜random｜z=0.01142871

上下文360，目标offset=497，目标token=" Tata"；原文档未知。

包含目标的模型可见前文：

<pre> This must be stopped 6

Journal by dedazo

This is a perfect example of why gun-control laws in Europe are so excellent and should be adopted by the US.

Oh wait....

(not to belittle deaths, obviously. It&#x27;s a tragedy when innocent people are killed like this, regardless of method or motive)


Journal: The Python History Blog 8

Journal by dedazo

Guido van Rossum and Greg Stein have set up a new blog that provides extremely interesting details on the early years of Python. Great quote on the origin of the name:

So, rather than over-analyzing the naming problem, I decided to under-analyze it. I picked the first thing that came to mind, which happened to be Monty Python&#x27;s Flying Circus, one of my favorite comedy troupes. The reference felt suitably irreverent for what was essentially a &quot;skunkworks project&quot;. The word &quot;Python&quot; was also catchy, a bit edgy, and at the same time, it fit in the tradition of naming languages after famous people, like Pascal, Ada, and Eiffel. The Monty Python team may not be famous for their advancement of science or technology, but they are certainly a geek favorite. It also fit in with a tradition in the CWI Amoeba group to name programs after TV shows.

Highly recommended.

User Journal

Journal: Cold

Journal by dedazo

It is, here. Damn it&#x27;s cold. San Francisco was cold last week, but not that much.

Although I don&#x27;t miss Santiago in the winters, not my a mile.

Caracas maybe... and Mexico City.

User Journal

Journal: Economic Crisis: Offshore Hurting Too 2

Journal by dedazo

Just in time for this comment I made yesterday, I received an email a few hours ago from one of the tech leads at the company I work with as a consultant. Of the entire application portfolio for the VP whose groups I work with, they will be releasing 57 people (or offshore resources as they call them) at two locations in India.

This adjustment in staffing (more management speak) directly affects six to eight different projects/applications across four groups in the division. And this is just one division under one VP. I am involved with two of those. Technically I am an onshore resource as well, at least from their staffing perspective, although I&#x27;m not in India, I don&#x27;t work through Tata</pre>

右文（仅阅读辅助）：

<pre>, Infosys or IBM, and I don&#x27;t cost $20/hr.

These are mostly developers, with a small number of QA/testing positions and a few analysts. It also includes about two thirds of the tier-1 production support staff for the entire division. Yay.

Of course what I have not seen is an adjustment on the project schedules that were agreed upon last month, with the assumption that</pre>

### 位置817745｜random｜z=0.02656543

上下文799，目标offset=186，目标token="plant"；原文档未知。

包含目标的模型可见前文：

<pre> sows are bred in the old-fashioned way, every fourth offspring will secrete no alpha gal at all. These animals will be founders of a new breed of pig, designed by the human race to provide spare parts for itself.

There are currently more than 5,500 people in Britain waiting for a transplant of a kidney, pancreas, heart, lungs, liver, or a combination of these organs. On average, adults have to wait over 500 days for a new kidney.

Alan Colman, PPL&#x27;s head of research, said yesterday: &quot;The promise of xenotransplantation is now a reality.&quot;

He said it might be necessary to add certain genes to the for-transplant breed before they were ready for trials, but this would not be a problem. &quot;I think we are four or five years away from meaningful human clinical trials.&quot;

Just how risky the future for xenotransplant</pre>

右文（仅阅读辅助）：

<pre>ation is was starkly illustrated yesterday when PPL, despite its scientific success, announced it could not afford to run the research programme and was effectively putting the transplant side up for sale to concentrate on another GM animal project, the production of a protein in the milk of GM sheep to combat human emphysema.

PPL&#x27;s shares soared on the Stock Exchange yesterday: as has become traditional, it</pre>

### 位置997397｜random｜z=0.06391895

上下文974，目标offset=823，目标token="Art"；原文档未知。

包含目标的模型可见前文：

<pre> and military ties.

Because of this strong relationship, Chinese leaders have traditionally resisted international pressure to use their clout to bring peace to Darfur, where there is conflict between government-backed militias and rebels.

Beijing has even used its veto at the UN Security Council - to block moves to impose sanctions on Sudan if it fails to stop the fighting in the troubled region.

Panorama: China&#x27;s Secret War will be on BBC One at 8.30pm on Monday 14 July 2008.

Panorama: China&#x27;s Secret War
31 Jul 08 |  Panorama

Has China&#x27;s housing bubble burst?
How the world&#x27;s oldest clove tree defied an empire
Why Royal Ballet principal Sergei Polunin quit
&lt;|im_end|&gt;Coldplay snub sounds alarm for streaming music

Pundits and analysts say music acts aren&#x27;t seeing the payout they want from subscription services. Those who defend the likes of Spotify, Rhapsody, and MOG note that it&#x27;s either them or piracy.

Greg Sandoval

Sam Rosenthal (far right), owner of the label &#x27;Projekt&#x27; and member of the band &#x27;Black Tape For A Blue Girl,&#x27; says there just isn&#x27;t enough money in distributing through subscription music services.

(Credit: Sam Rosenthal/Projekt)

Coldplay and singer Tom Waits last week issued no-confidence votes on subscription music services, or at least that&#x27;s how the press is interpreting their decision not to distribute their latest albums through companies such as Spotify, Rhapsody, Rdio, and MOG.

On Wednesday, CNET broke the news that Coldplay and Waits will follow other marquee acts, such as Adele and Prince, who have withheld at least part of their catalogs from some of the subscription services. Management for Coldplay and Waits did not respond to interview requests. So, while we don&#x27;t know for sure why they chose to snub the subscription services, several analysts and members of the media say there&#x27;s little doubt about the reason.

The subscription services just pay artists too little money say critics and there&#x27;s also some fears about whether these services, which generate less revenue, eat into sales from more lucrative outlets, such as Apple&#x27;s iTunes. Coldplay has made its latest album &quot;Mylo Xyloto,&quot; available for download on iTunes and Amazon as well as made music videos for each song available at YouTube.

Glenn Peoples at Billboard wrote that Coldplay is apparently trying to push fans into paying for downloads or CDs. &quot;By keeping the album away from on-demand services,&quot; Peoples wrote, &quot;Coldplay is ensuring fans will buy (or find other ways to obtain the music) rather than listen for free.&quot;

Spotify, Rdio, and MOG charge users a monthly price to access large pools of songs but they also offer a limited amount of music free of charge.

Top 10 most influential music sites (photos)

1-2 of 10
Scroll Left Scroll Right

Rolling Stone magazine tried to compare the amounts of money that artists see from each type of distribution. The magazine said an artist may receive 19 cents for every 60 times a song is played. The magazine cautioned that licensing deals will differ between acts as well as between subscription services. The payout for a downloaded song at iTunes that costs $1.29 is much easier to pinpoint: the label gets 60 cents, Apple 40 cents, the artist 20 cents, and the songwriter 9 cents.

The perception that streaming services aren&#x27;t lucrative for artists has been around for awhile, but it continues to dog the sector, and losing a band with the notoriety of Coldplay won&#x27;t help.

These services, which stream songs over the Internet to users&#x27; mobile phones, PCs, or digital music players, have only been building momentum in the last year thanks in large part to the buzz generated by Spotify. The service took Europe music listeners by storm and after years of failed attempts to license music in the United States, finally launched operations here in July.

&quot;Art</pre>

右文（仅阅读辅助）：

<pre>ists can--and do--receive very substantial revenues from Spotify,&quot; the company said in a statement. &quot;And as we grow, these revenue streams will naturally continue to grow.&quot;

In that same Rolling Stone article, Jim Guerinot, manager of Nine Inch Nails and No Doubt, suggested subscription services could have a bright future. &quot;Is it big money?,&quot; Guerinot said, &quot;</pre>

### 位置1485901｜random｜z=0.01826465

上下文1452，目标offset=234，目标token=" effect"；原文档未知。

包含目标的模型可见前文：

<pre>ḣ a king who acts like an idiot
keda ziunte te mygu the ox that&#x27;s in the house

Finally, a -te clause can stand on its own, meaning &#x27;the one(s) which...&#x27;:

Fal buda Kazumte beźe eḣc ḣem buda Lelecte.
You ate Kazum&#x27;s grapes and I ate Lelec&#x27;s.

Ruḣi Avelaḣ eupte lauhte? Ťaḣ miry.
Did you count the one who comes from Avéla? He&#x27;s rich.

Existence and equivalence

There is no verb &#x27;to be&#x27; in Kebreni; the closest equivalent is zaru &#x27;exist, be there&#x27;.

Dama gegeu zaru, eḣc dama veźa zaurte eśu.
(Lit.) Three servants exist, and three bottles do not exist.
There&#x27;s three servants and three missing bottles.

Boṫengu ziunte ciḣica ingarei zura.
In Boggola there used to be a praiseworthy tavern.

There is no verb &#x27;have&#x27; either; zaru with effect</pre>

右文（仅阅读辅助）：

<pre> inflections serves for this.

Keda, kur gegeu, eḣc śemu zeri.
I have a house, two servants, and a fish. (Lit, they exist for my benefit.)

Lelena lelena nyne zeniri.
You have a very, very cute daughter. (Lit., she exists for your benefit.)

Negative effect inflections are used when the possession</pre>

### 位置1986135｜high_activation｜z=0.2187041

上下文1941，目标offset=99，目标token="ont"；原文档未知。

包含目标的模型可见前文：

<pre> asked me to share the vision and some of our early results with his friends and expand in 2013, and if so he&#x27;d bring the domainer clients and we&#x27;d split profits we make for his friends. I told him it&#x27;d take time to scale up thru March but yeah, we can do 400 for the community instead of 100 for Rick Schwartz. Simple as that.
You want one example of how we&#x27;re DIFFERENT? Look at Jont</pre>

右文（仅阅读辅助）：

<pre>Ventures.com itself. A 200 page BOOK formatted as a website and the average deal with an end user we do spends HOURS consuming every scrap of information on that site educating themselves on why it is a GOOD decision to pay Rick Schwartz $xxx+ monthly for something he has $x,xxx invested into and 20 years of patience. The people that want the BEST generic .</pre>

### 位置3180120｜random｜z=0.02583301

上下文3108，目标offset=130，目标token=" front"；原文档未知。

包含目标的模型可见前文：

<pre> this dialect area include Kansas City, Omaha, St. Louis, Columbus, Ohio, Cincinnati, and Indianapolis.

In addition to the fronting of the diphthongs /oʊ/ and /aʊ/, the North Midland exhibits the following distinctive features:[3]

  • cot–caught merger in transition: parts of this area are currently undergoing a vowel merger of the &quot;short o&quot; /ɑ/ (as in cot) and &#x27;aw&#x27; /ɔ/ (as in caught) phonemes. Many speakers show transitional forms of this so-called cot–caught merger, which is complete in approximately half of North America.
  • advanced front</pre>

右文（仅阅读辅助）：

<pre>ing of /ʌ/: among younger speakers, the &quot;wedge&quot; /ʌ/ (as in strut) is shifting strongly to the front.


Western Pennsylvania[edit]

Based on Labov et al.; averaged F1/F2 means for speakers from Western PA. The merger of /ɑ/ and /ɔ/ is complete for 11 out of 14 speakers;[4] /</pre>

### 位置4990972｜high_activation｜z=0.216751

上下文4878，目标offset=179，目标token="ent"；原文档未知。

包含目标的模型可见前文：

<pre>. Louis, Mississippi, William A. Scarborough, in his Chevrolet truck, led and escorted Thornburg in the GMC trailer-truck and 694 gallons of nontax-paid whiskey from his dairy to the Bay St. Louis Highway Bridge.&quot;

2. See testimony of Eugene Thornburg, Rec. pp. 55-58, 63; of J. B. Burson, Jr., Rec. pp. 102, 116, 117, 146; and of Marvin H. Dunn, Rec. pp. 247-250, 260.

3. The indictment alleged that the conspiracy terminated the previous day. In any event, after his arrest, this co-defendant was no longer a party to the conspiracy nor were his statements in furtherance thereof.

4. &quot;Gent</pre>

右文（仅阅读辅助）：

<pre>lemen, there was a ruling made when Mr. Hart was on the witness stand. I am going to ask the Court Reporter to read the question and the objection and the answer there that I want to change my ruling on, so you will know what we are talking about.

&quot;(The record was read as follows):

&quot;`Q. Go ahead and tell what he said. A. Nelson said that he</pre>

### 位置10173878｜high_activation｜z=0.2138213

上下文9944，目标offset=7，目标token="PT"；原文档未知。

包含目标的模型可见前文：

<pre>&#x27;t fit into their lives.


GUPT</pre>

右文（仅阅读辅助）：

<pre>A: Good luck, Molly. And that&#x27;s really important advice I think for everybody.

Unfortunately, we&#x27;re out of time for today. An exciting show, though, on tap for next weekend. We&#x27;re going to look at some medical mysteries from people who have learned to feel no pain whatsoever, to a condition doctors argue doesn&#x27;t even exist. We have the facts. We&#x27;ll let you decide</pre>

## Feature 7304，h_V=1

### 位置418842｜random｜z=0.01274272

上下文409，目标offset=301，目标token=" games"；原文档未知。

包含目标的模型可见前文：

<pre>. Skimming over the surface of an alien world in your spacecraft and seeing your early creations vying to get a foothold in the ecosystem is hugely rewarding and makes you almost willing to forgive everything you had to go to get there.

Maybe you feel like expanding your space empire? This can be accomplished by selecting a hospitable uninhabited planet and planting a colony. Like the cities in the civilization stage, these colonies require micro tending to make their spice trade profitable and part of this effort requires you to ensure the atmosphere is as hospitable as possible for life. You can control the temperature and humidity of the planet by using a combination of powerful terraforming tools and the introduction of plants and animals from other planets. The whole process may take a while but the first time you transform a barren, rocky volcanic wasteland into a lush garden paradise is a moment to remember. In addition, should the urge seize you, you can even craft the terrain of planets to your liking by raising and lowering land masses, and painting both the skies and seas.

With the equivalent of five games in one, Spore is a case study of breadth winning out over depth, and many gamers will resent how unchallenging the majority of the game is until the space age, which is almost too little, too late. Ultimately, the thing that sets Spore apart is the creation engine, and if playing God and molding your very own animal leaves you cold, then you&#x27;re probably better off playing any of the aforementioned games</pre>

右文（仅阅读辅助）：

<pre> that Spore imitates poorly. If, however, the dormant 3-D modeler in you yearns for an outlet for creative expression, you&#x27;ll get a ton of enjoyment in seeing your vehicles, creatures and buildings come to life in the game. To really get the most out of Spore, you also have to be able to emotionally invest yourself in your creature and its fate and care about</pre>

### 位置489444｜high_activation｜z=0.2855699

上下文478，目标offset=303，目标token="7"；原文档未知。

包含目标的模型可见前文：

<pre> claims….http://bit.ly/aA8ioD

Don&#x27;t you just love it?  They will let the brave men suffer and die as a result.  Surprised? Shouldn&#x27;t be.  Disgusted? You bet!

Visibility: Everyone
Tags: , , , , , , , ,
Posted: May 28, 2010 2:04pm
May 28, 2010


There&#x27;s a movement coming, rising slowly but steadily.  It is a reaction to those who&#x27;s virulent hatred is spewed  all over the papers, television and radio.  As a result, repeal of DADT is so very close to passage. It isn&#x27;t over due, it&#x27;s a never should have been.

John McCain, in a very tight race to stay in his job, has promised to filibuster until it goes away.  Just for the record, he&#x27;s a former supporter of the bill. http://bit.ly/aA8IAZ

In the meantime, the right wing wants the law completely repealed; apparently on the assumption that Americans will rise up and force it&#x27;s reinstatement out of fear loathing and bigotry. For the first time in who knows how long, the right and left agree on something!  Hurray.

I read an article from April of this year, about the end of the stupidity that’s DADT will destroy military chaplaincy. http://bit.ly/da7</pre>

右文（仅阅读辅助）：

<pre>IqH.  How sad for the chaplains who believe it and the people they will abandon as a result.

Chaplains are trained to serve all sorts of religions in the service.  Jewish Rabbis definitely aren&#x27;t Christian but function and minister/priest when need.  Catholic priest are suppose to be anti-every other faith including what they consider heretics, i.e</pre>

### 位置2101311｜random｜z=0.05534526

上下文2053，目标offset=693，目标token=" ("；原文档未知。

包含目标的模型可见前文：

<pre> percent of head trauma by taking it out of practice. And it&#x27;s not necessary to bang heads in practice. Think about where the NFL has come in terms of that. The season is now 18 weeks long; only 14 times in 18 weeks can there be full contact in practice [according to the league&#x27;s latest collective bargaining agreement]. There have been huge reductions in brain trauma sustained by NFL players just because of the way they&#x27;re practicing now. In the Ivy League, they&#x27;ve limited contact practices to twice a week. Especially at the youth level, don&#x27;t bang bodies [in practice]. Hit pads, hit tackling dummies, don&#x27;t hit heads on heads.


Ground Rules for Posting
All comments are public.

Follow This Blog


Most Viewed on Education Week



Recent Comments&lt;|im_end|&gt;How to configure SQL Server database mirroring between 2 instances on a standalone server


  • Comments 1

There are lots of troubleshooting articles about how to diagnose connectivity problems when setting up database mirroring, especially errors such as these:

Msg 1418, Level 16, State 1, Line 2

The server network address &quot;tcp://&quot; can not be reached or does not exist. Check the network address name and that the ports for the local and remote endpoints are operational.


Msg 1456, Level 16, State 3, Line 1


but here&#x27;s something a little different.

Imagine that you have a server which is not connected to a domain. It might just be a standalone machine, it could be a virtual machine that you&#x27;ve just built. I&#x27;ve done this a few times in virtual environments to do demos on laptops and the like. It&#x27;s a not a production scenario that you&#x27;d come across really, but it works really well in test.

The questions that usually come up are how can I configure the partners (and endpoints) without having a FQDN, since I&#x27;m not connected to a domain, I&#x27;m just in &quot;WORKGROUP&quot;. SQL Server still wants you to use FQDN formatting for the partner addresses. When you&#x27;re trying to configure it, you might have even encountered an error like this when trying to start mirroring (depending on exactly how you did the setup)


There is no compatible authentication protocol. State 21

What you need to do to be able to set this up is as follows:

1. adding &quot;local&quot; as the primary DNS suffix as in detailed this article here (ok it&#x27;s about exchange server but it works the same)

(remember to reboot)

2. You can now specify FQDN formatted names for the local machine in the format:

For the principal:


For the mirror


(Or other port numbers of your choice, but remember that they&#x27;ll need to be different)

3. You&#x27;ll need these ports as exceptions in Windows Firewall if you&#x27;re running it (I was even though it was a local machine!)

4. My endpoints are setup like this (but I just did them through the GUI) there&#x27;s nothing exceptional here:






You can now run some cool tests and demos without ever being connected to a network.

Leave a Comment
  • Please add 2 and 4 and type the answer here:
  • Post
  • I&#x27;ve been posting in the MSDN and TECHNET mirroring forums in the last few days and I&#x27;ve noticed a lot

Page 1 of 1 (</pre>

右文（仅阅读辅助）：

<pre>1 items)&lt;|im_end|&gt;&quot;OOF&quot; is a word you hear a lot at Microsoft. KC Lemson gave the etymology a while back (though my recollection is that it stood for &quot;Out of Office Feature&quot;, not that my memory is good for much nowadays). Incidentally, KC is profiled on the Microsoft Careers site, though she goes under the top-secret code name &quot;KC&quot; there</pre>

### 位置2525473｜random｜z=0.008470258

上下文2468，目标offset=258，目标token=" dangling"；原文档未知。

包含目标的模型可见前文：

<pre> Cadsuane. She is so rude, it takes a Min viewing for Rand to tolerate her crap- and even that isn&#x27;t enough by TGS.

I laugh at Mat stuffing money down a girl&#x27;s bodice, yet not connecting that with Olver. But why do I have a clear mental picture of Caira?

This book is rolling now! Swovan Night/Small Sacrifices are coming, and I can&#x27;t wait for the awesome Six Stories.
Captain Hammer
24. Randalator


But she’s Cadsuane, and I just can’t bloody stand her.

Stop. Reading. My. Mind. Because that&#x27;s word for word where I stand re: Cadsuane. Yes, it is.

God, Cads pisses me off so much!
Kathy Keith
25. Babokathy
Love Cadsuane.

She&#x27;s good, very good, suave, cool as a cucumber, unshakable, determined, like a well-seasoned actress on stage. No fear. Yet.

I find her intriguing.

There is much more to Cadsuane than meets the eye, even up through TGS. I&#x27;m anxious to find out what it is about her. It&#x27;s not just those pretty gold dangling</pre>

右文（仅阅读辅助）：

<pre> ornaments (stars, moons, birds) in her hair. (No one seems to wonder what they are for many books). Although she wears many more kinds during the tangle in KOD.

I&#x27;m thinking she must have been doing something more than growing roses, while disappearing for 70+ years? Gathering info from libraries all over Randland? (She&#x27;s a Green?) She&#x27;s smart</pre>

### 位置4595743｜high_activation｜z=0.2894761

上下文4491，目标offset=842，目标token="2"；原文档未知。

包含目标的模型可见前文：

<pre> a thin blue line. C. albicans TPK residues making contacts with Mg2+ ions are highlighted in brown, those in contact with phosphate and Mg2+ in green, those in contact with thiamine or thiamine-PNP in pink, and those in contact with thiamine or thiamine-PNP and Mg2+ in purple. The residues exclusively interacting with thiamine-PNP (and not thiamine) are in grey, and those in contact both with thiamine-PNP and phosphate are in light blue.

Interestingly, there are three loops in the C. albicans TPK structure. Two of them, L4 and L11 (Figure 2), are unique to C. albicans, while the third and longest insert (L85-L9) is also present in the yeast homolog with which it shares less than 20% identity over 35 residues (Figure 2). None of these fragments appear to be directly involved in the catalytic reaction or in the ligands binding (Figure 2). In the structure, the L11 loop lies in the solvent, in an open conformation and away from the rest of the molecule (Figure 1B–C). The B-factors for this loop are also very high (see Additional file 4). We first built an approximate loop by following the residual density present in the 2Fo-Fc and Fo-Fc maps. We then used manual docking to verify that the length and geometry of this loop was compatible with a transient interaction with the ligands. This loop may thus play a role during the binding of the substrates, or in the pyrophosphorylation mechanism itself.

Additional file 4. Graph representation of the B-factors values of the C. albicans TPK structures in complex with thiamine and thiamine-PNP. Monomers A and B of TPK/Thiamine-PNP are shown in black and grey respectively. Monomers A and B of TPK/Tiamine are shown in red and orange respectively.

Format: PNG Size: 697KB Download fileOpen Data

The CA1462 overall structure: dimer

The main differences between the two monomers related by the NCS involve flexible loops disordered in the crystal structure (Figure 1B–C, see Additional file 4). They include loops L1, L2 and L4, which are too distant to be involved in the active site formation and located too far from symmetry related molecules to possibly be directly involved in the crystal packing. There are also water molecules which are not strictly symmetrical between the two monomers (data not shown). Although the loop L11 is highly mobile and associated with high B-factors (Figure 1B-C, see Additional file 4) it presents little differences between the two monomers. The L85-L9 fragment, which is involved in crystal packing through interactions between L85 helix/turn and α36 helix/turn in the two monomers, can be superposed with less than 0.3 Å root mean square deviation (RMSD) based on α carbon (Cα) superposition.

There are no major differences between the TPK known structures based on Cα superposition using LSQMAN [27]. RMSD are 2.33 Å (534 superimposed residues) between the C. albicans and the S. cerevisiae TPK structures, and 2.62 Å (464 superimposed residues) between the C. albicans and the Mouse TPK. The backbone trace around the thiamine binding site superimposes well except for one fragment. Timm et al. described a rearrangement of the L6 loop in the mouse TPK when comparing the structures with thiamine and TPP [7]. This rearrangement is not observed within the C. albicans TPK which fits the mouse TPK in complex with TPP except for the S116 side chain.

Thiamine binding site (PDB id 2</pre>

右文（仅阅读辅助）：

<pre>HH9)

Two binding sites can be shown in the asymmetric unit. The strong electronic density is consistent with thiamine molecules present at the thiamine binding site (Figure 3A). As in the mouse structure, the thiamine moieties are located at an extremity of the groove formed by the dimer assembly. For convenience, we will take A as the reference monomer and</pre>

### 位置7666671｜random｜z=0.009172162

上下文7493，目标offset=463，目标token="."；原文档未知。

包含目标的模型可见前文：

<pre> first point.

But secondly it&#x27;s equally plain that there are a bunch of open questions there that need to be answered. These are legitimate questions and I know from my discussions yesterday the administration will be prosecuting those questions with its engagement with the government in Islamabad.

ALI MOORE: As Foreign Minister you get far better intelligence than most if not all of our audience, what&#x27;s your view?

KEVIN RUDD: The more you are around in this sort of business the more you can be surprised by what might appear to be the case and what might not appear to be the case. I have just learnt through long and bitter experience that you wait until the jury&#x27;s in on these questions and I&#x27;d much rather do that and therefore there is obviously questions to be asked, questions to be answered, that will occur between the US and Pakistan, I&#x27;m sure we will be briefed in due course about the outcome of all that.

The other thing I&#x27;d say is that Pakistan itself is an extraordinarily difficult, complex operating environment. Anyone familiar with the politics of Pakistan, the role of the military, the role of the intelligence services, the porous nature of the border with Afghanistan, this is a very tough place to operate from and with and in cooperation with. So let&#x27;s just wait until the jury&#x27;s in. That&#x27;s the safest thing to do.

ALI MOORE: In your view what is the key question that that jury has to look at?

KEVIN RUDD: Well again, I&#x27;d defer to the Americans on that question but let&#x27;s just call a spade a spade. The question is whether anyone in Pakistan was aware or not of the presence of Osama bin Laden at this location in Pakistan prior to the operation being initiated. That&#x27;s an open question. I don&#x27;t say that with any value-laden tone attached to it. Let&#x27;s just see what the authorities produce by way of their response to legitimate questions from the US and from others.

ALI MOORE: Clearly though you are prepared to countenance that possibility by accepting it as an open question and would you also acknowledge that of course accusations or allegations of links between the Taliban or insurgents and high level intelligence on the Pakistani side are not new?

KEVIN RUDD: Those accusations have been flying around for a long, long time.</pre>

右文（仅阅读辅助）：

<pre> I said before Pakistan is a highly difficult, complex operating environment. The operations of arms of the Pakistani intelligence services, the military, the relationship with the civilian government in Islamabad, these are highly complex and sometimes opaque questions. Let&#x27;s just, as I said, take a deep breath, wait for the answers to be delivered. The key thing though, however, is that this mission has succeeded in its</pre>

### 位置8512275｜high_activation｜z=0.2894761

上下文8319，目标offset=975，目标token="9"；原文档未知。

包含目标的模型可见前文：

<pre> or products that everyone is already on board with!

So please feel free to send comments my way and I hope you enjoy surfing trendhunter.com!

What&#x27;s your favorite accomplishment?
Being nominated and selected Student Council President at the best high school, for the best student body ever. (and also winning the Spirit Award in 2008. In my opinion it was most definitely a huge game-changer award for me)
How do you define cool?
Every single human being is unique and I have this crazy theory that when everyone is a follower (of a trend) the uniqueness of you is not brought forth. Therefore, from time to time when one comes across a really &quot;cool&quot; product, idea or event, it will not only spark you to say &quot;Wow. That is cool,&quot; but be something that links you to your individuality. As not everything I consider &quot;cool,&quot; may be something you consider cool. Not at all but - it is.
What is your secret to uncovering trends?
Having your eyes open, staying true to yourself and not letting any opportunity pass you by.
What do you enjoy most about Trend Hunter?
How every single person who works at Trend Hunter is the epitome of &quot;cool,&quot; in my eyes.
What is your favorite trend?
Things that spread social awareness and goodness.
What are your tips for writing a juicy post?
Knowing your audience and that general things like humour and humility go a long long way.
How do you reset to be creative?
By dreaming, going to Muskoka, extending my comfort zone, listening to some good tunes and spending time with family and really good friends encouraging non stop laughter.
What inspires or excites you?
Hearing about or seeing little acts of kindness that display peace, love and happiness.
Predict something awesome for 2020?
Trendhunter being selected to be the homepage of every single person in the world&#x27;s internet browser.&lt;|im_end|&gt;UK designer Benedict Radcliffe has a unique set of artwork that combines engineering, machinery and architecture. His latest piece &#x27;The Cage&#x27; looks to resemble a giant car tire from the distance, but as you get closer, you can see the miniature soccer pitch inside.

Benedict Radcliffe built this fun and toy-sized stadium right outside the Stade de France where World Cup 98 was held. Inside &#x27;The Cage,&#x27; a competition is held where people try to score on a former French Olympic goalkeeper to win prizes.

Photo Credits: designboom, benedictradcliffe&lt;|im_end|&gt;
We support the following browsers:

Hane Sushi

Un Chau Street, Sham Shui Po, Kowloon, Hong Kong, China (Kwun Tong)
Update restaurant details
Got a photo?
Add it.
Hane Sushi is ready for reviews.
Cuisines: Japanese
Dining options: Takeout
Neighborhood: Kwun Tong
Restaurant details
Dining options: Takeout
Neighborhood: Kwun Tong

Also consider these other restaurants near Hane Sushi

No photo provided
0.1 miles from Hane Sushi

Been to Hane Sushi? Share your experiences!

Write a Review Add Photos &amp; Videos

Owners: What&#x27;s your side of the story?

If you own or manage Hane Sushi, register now for free tools to enhance your listing, attract new reviews, and respond to reviewers.

Manage your listing&lt;|im_end|&gt;Hi all,

I&#x27;m looking at creating a modified logotype based on Imprint MT, however I suspect that this face was originally created for text, not display, judging by the cut.

In my opinion, these characteristics contribute to it&#x27;s overall feel of the typeface (and logomark) but I&#x27;m wondering whether any optical alterations need to take place - particularly on the arms of the T and E, spur of the S and apex of the A as well as the serif terminals.
I feel a lot of these element could work well but would like some second and third opinions...

Hey Typophilers,

It has been a few years since jumping on here, but I am in need of your help. Could you typographers give me any criticism on this rebranded wordmark that I have been developing. It is for the people search engine, known as Spokeo and is supposed to encompass a product that searches social media content to criminal records. There is a lot of brand strategy and thought that went into this wordmark, but rather than include that I want to include a simple neutral greyscale version rather than a sales pitch.

Here is a brief rundown of what the brand is trying to encompass:

· A company with all the tools to allow you to search for people and connect with them.

· A company that exhibits integrity and transparency and is trusted by consumers.

This is for a logo for a design studio. http://imgur.com/a/9</pre>

右文（仅阅读辅助）：

<pre>gdj4#1 Going from left to right there&#x27;s 4 pages. Please tell me which type looks best here and what can be done to refine it at it&#x27;s best.

The ones in dark using a 4HB pencil are</pre>

### 位置10237781｜random｜z=0.01420756

上下文10006，目标offset=455，目标token="\n"；原文档未知。

包含目标的模型可见前文：

<pre> through the optic nerve to the brain. There further physical
    processes arise. Could these be observed, we would simply see more physical
    processes just as elsewhere in the physical world. If I am able also to
    observe the ether body, I shall see how the physical brain process is at the
    same time a life-process. The sensation of blue color that the recipient of
    the rays of light experiences, however, I can find nowhere in this manner. It
    arises only within the soul of the recipient. If, therefore, the being of
    this recipient consisted only of the physical and ether bodies, sensation
    could not exist. The activity by which sensation becomes a fact differs
    essentially from the operations of the formative life-force. By that activity
    an inner experience is called forth from these operations. Without this
    activity there would be a mere life-process such as we observe in plants.
    Imagine a man receiving impressions from all sides. Think of him as the
    source of the activity mentioned above, flowing out in all directions from
    which he is receiving these impressions. In all directions sensations arise
    in response to the stimuli. This fountain of activity is to be called the
    sentient soul. This sentient soul is just as real as the physical body. If a
    man stands before me and I disregard his sentient soul by thinking of him as
    merely a physical body, it is exactly as if, instead of a painting, I were to
    call up in memory merely the canvas.

    A statement similar to the one previously made in reference to the ether body
    must be made here about perceiving the sentient soul. The bodily organs are
    blind to it. The organ by which life can be perceived as life is also blind
    to it. The ether body is seen by means of this organ, and so through a still
    higher organ the inner world of sensation can become a special kind of
    supersensible perception. Then a man not only senses the impressions of the
    physical and life world, but he beholds the sensations themselves. The
    sensation world of another being is spread out before a man with such an
</pre>

右文（仅阅读辅助）：

<pre>    organ like an external reality. One must distinguish between experiencing
    one&#x27;s own sensation world, and looking at the sensation world of another
    person. Every man, of course, can see into his own sensation world. Only the
    seer with the opened spiritual eye can see the sensation world of another.
    Unless a man is a seer, he knows the world of sensation</pre>

## Feature 7388，h_V=0

### 位置1679646｜random｜z=0.005280487

上下文1641，目标offset=557，目标token=" "；原文档未知。

包含目标的模型可见前文：

<pre> would never have thought of that angle. Does this mean I can’t go mailing the Bee old posts of mine and hope they’ll run them?

  9. No. I’m sure you can mail whatever you want. I’ll subscribe to the Bee when it publishes you.

  10. *is enlightened*

    I never would have made the link from op ed page to lobbying organization. Thanks.

  11. Just a note to add that conservation cum environmentalism is precisely what converted me from young Republican to adult liberal.* I never understood why conservatives were supposed to valorize the waste of resources, and I spent enough time in the Everglades as a kid to intensely value whole ecosystems, not just isolated, charismatic megafauna. The more I saw how irrational environmental issues made the American right, the less I wanted to do with it.

    * Well, that and finally appreciating that an absolutist view on abortion was stupid and unrealistic, which is not how conservatives imagine themselves&lt;|im_end|&gt;502 F2d 1261 Burton v. L Waller

502 F.2d 1261

Myrtle Green BURTON, Individually and in her Capacity as
Representative of James Earl Green, Deceased, et
al., Plaintiff-Appellants.
William L. WALLER, Individually and as Governor of the State
of Mississippi,et al., Defendants-Appellees.

No. 72-2311.

United States Court of Appeals, Fifth Circuit.

Oct. 18, 1974.

Ralph L. McAfee, Robert F. Mullen, Andrew P. Tashman, Wayne A. Cross, New York City, for Burton and others.

George Peach Taylor, Lawyers&#x27; Committee for Civil Rights Under Law, Constance Iona Slaughter, James M. Abram, Jackson, Miss., Dale Broeder, Lake Oswego, Or., James Reif, Jackson, Miss., for plaintiffs-appellants.

Robert G. Nichols, Jr., Rufus Creekmore, John E. Stone, Jackson, Miss., for Davis and others.

William A. Allain, Asst. Atty. Gen., A. F. Summer, Atty. Gen. of Miss., Charles A. Marx, Jackson, Miss., for Highway Patrol, Williams and others.



Before JONES, GODBOLD and INGRAHAM, Circuit Judges.

GODBOLD, Circuit Judge:


This is a civil suit seeking recovery of damages for the deaths of two black persons and injuries to three others from gunshot wounds suffered on the campus on Jackson State College in Jackson, Mississippi, on the night of May 15, </pre>

右文（仅阅读辅助）：

<pre>1970. These five persons, plus at least nine other blacks who were wounded but are not parties to the suit, were struck by gunfire laid down by a detachment of officers who were on the campus as a result of student disorders.


The law enforcement detachment from which the gunfire came consisted of 69 persons, from the Mississippi Highway Safety Patrol (MHP) and the Jackson Police Department</pre>

### 位置2385788｜random｜z=0.01175021

上下文2331，目标offset=750，目标token=" because"；原文档未知。

包含目标的模型可见前文：

<pre> one of the most popular casinos in the Nevada gambling capital.

Harry sent over a young guy to act as her chauffeur and security for the trip. His name was Tony and he stayed close to her but didn’t say very much at all. She felt a little uncomfortable around him because his dark good looks made her pussy tingle big time and whenever their arms or legs bumped together, she felt her juices start to puddle inside her female slit. She hoped he would not be sharing the suite with her because it was hard enough to concentrate on the job without his handsome ass distracting her all the time.

The practice session was quick and well-organized.

Holly was able to select her own wardrobe for each segment of the shoot and would be in an assigned costume only on the last afternoon. She would be wearing her zebra striped bikini for the very first shoot and she made certain it was spotlessly clean and ready to don with a moment’s notice. She was twirling in front of the full length mirror modelling her bikini when Tony came in with some goodies from the downstairs buffet. He had put together a nice salad assortment for her in response to her request for low calorie items. They sat casually on the fluffy white carpet because it was more comfortable than the stiff business style chairs in the corner.

Holly sat cross-legged and was aware of the fact that the closed-mouthed Tony was staring at her pussy. She acted like she was interested only in the salad and was ignorant of the fact that her prominent camel-toe was pushing hard against the soft thin fabric of the zebra striped bikini panties.

Suddenly, her nipples made sharp indentations on the top half of her bikini and she saw him shift his focus from her pussy to her nipples and back again. She was certain her wetness must be visible on the bikini crotch and that the eagle-eyed aide would not miss the tell-tale spot.

She told Tony that she had a stiff neck and asked him to rub it for her.

He wrapped his legs around her hips and squeezed her shoulders with strong hard palms. Holly let her head fall forward and he let his fingers move up the center of her neck into the nape of her neck. The touch of his fingers made her shiver with anticipation. She imagined his hands dipping down to grasp her nipples and starting to work them into little hard buds of sensuous sensitivity.

Her female folds were starting to get very wet when Tony moved his hands down between her legs and started to push up inside her special place. Holly was trembling with desire but was ashamed to reveal to Tony just how much she wanted his cock inside her.

When she turned around to face him, she closed her eyes so she would not get lost in his handsome eyes and placed her palms up in complete submission to his desire. She heard the sound of his cock entering her wet slit and opened her eyes to see it slide in all the way to the base. Tony’s balls began to slap against her ass cheeks with a spanking action and she pushed her ankles up higher almost to the back of his head.

“You like getting Tony’s meat, little girl?”

She had to admit it was the best she ever had and she told him so.

“Yes, Tony, give it to me good. I will be a good girl for you. You can even do me in my back door if you want it nice and tight.”

A little later, that is exactly what the muscular security man did after spreading her ass cheeks and lubricating her pucker hole with two of his long strong fingers. He stretched her sphincter muscle with very little difficulty and she accepted his intrusion with welcoming groans of depraved pleasure.

The photo session was set-up in the sports room because</pre>

右文（仅阅读辅助）：

<pre> it was usually empty between 7am and 11am in the morning. The only guys in there were just reading newspapers or morning lines getting ready for the mid-day and evening action. She saw a few girls she knew from the portfolio events and was glad she had worn her sexiest bikini. Holly knew the cord between her ass cheeks was so thin that a close-up shot would actually catch</pre>

### 位置4097421｜random｜z=0.02818393

上下文4004，目标offset=769，目标token="lp"；原文档未知。

包含目标的模型可见前文：

<pre> set the meeting. We get our informants to find out where it&#x27;s going to be held. Now we insist that it be held in a public place, a bar or a restaurant where there&#x27;ll be other people there so I&#x27;ll feel safe. They&#x27;re going to search me when I first meet them, right? So I can&#x27;t have a weapon on me. But if Clemenza can figure a way to have a weapon planted for me, then I&#x27;ll kill them both.
Sonny: [laughing] What are you gonna do? Nice college boy, didn&#x27;t want to get mixed up in the family business. Now you want to gun down a police captain. Why? Because he slapped you in the face a little? What do you think this like the Army where you can shoot &#x27;em from a mile away? No you gotta get up like this and, badda-bing, you blow their brains all over your nice Ivy League suit. C&#x27;mere.
[Kisses Michael on the head]

Sonny: What the hell is this?

[to Rocco who has killed Paulie in the car]
Peter Clemenza: Leave the gun. Take the cannoli.

Paulie Gatto: Yeah, I&#x27;ll think about it.

Sonny: How&#x27;s Paulie?

Clemenza: What&#x27;s with all the new faces?
Clemenza: ...Jesus Christ.

[Clemenza prepares Michael for his meeting with Sollozzo]
Clemenza: What&#x27;s the matter, trigger too tight?
[With a loud bang, Michael finally discharges the gun]
Michael: Ow! My ears.
Michael: Sit down and finish my dinner.
Michael: How bad do you think it&#x27;s gonna be?
[Clemenza now finishes working on the gun]
[Clemenza hands the gun back to Michael]

[Michael gets ready to leave the house]
Sonny: Where&#x27;re you going?
Michael: To the City.
Michael: No, I&#x27;m just gonna go see Pop.
Sonny: I don&#x27;t care, send some bodyguards with him.
Sonny: Yeah? Well take care, all right?
Michael: Yes, sir.
[Michael leaves]
Sonny: Send someone with him anyway...



[Paulie enters the Corleones&#x27; study]
Sonny: What is it?
Paulie Gatto: You want me to hang around?
Sonny: Yeah, hang around. You all right?
Paulie Gatto: [coughing] Yeah, yeah...
Paulie Gatto: Nah, nah.
[Paulie leaves]
Clemenza: Understood.

The Godfather: The Don&#x27;s Edition (2007) (VG)
[Sonny hits him on the back of the head]
[he enters the hospital]
&lt;|im_end|&gt;IMDb &gt; Dangerous Minds (1995) &gt; Reviews &amp; Ratings - IMDb
Dangerous Minds
Top Links
trailers and videosfull cast and crewtriviaofficial sitesmemorable quotes
main detailscombined detailsfull cast and crewcompany credits
Awards &amp; Reviews
user reviewsexternal reviewsawardsuser ratingsparents guidemessage board
Plot &amp; Quotes
plot summarysynopsisplot keywordsmemorable quotes
Did You Know?
triviagoofssoundtrack listingcrazy creditsalternate versionsmovie connectionsFAQ
Other Info
box office/businessrelease datesfilming locationstechnical specsliterature listingsNewsDesk
taglines trailers and videos posters photo gallery
External Links
showtimesofficial sitesmiscellaneousphotographssound clipsvideo clips

Reviews &amp; Ratings for
Dangerous Minds More at IMDbPro »

Filter: Hide Spoilers:
Index 73 reviews in total 

47 out of 61 people found the following review useful:

An underrated movie altogether...

Author: jlp</pre>

右文（仅阅读辅助）：

<pre>icard1701E from New York, NY
8 June 2002

When this movie was first released, I refused to line up and watch it. I thought it was another of those simplistic and &quot;popular&quot; - love the teacher, fight delinquency - movies. In fact I refused to be taken for granted by clever Hollywood people who, usually, produce very</pre>

### 位置5432532｜high_activation｜z=0.1666574

上下文5309，目标offset=774，目标token=" a"；原文档未知。

包含目标的模型可见前文：

<pre>, query the USER_RECYCLEBIN data dictionary review. You can use the RECYCLEBIN synonym instead. The following two statements return the same rows:

  • If you specify the user-specified name, and if the recycle bin contains more than one object of that name, then the database retrieves the object that was moved to the recycle bin most recently. If you want to retrieve an older version of the table, then do one of these things:

    • Specify the system-generated recycle bin name of the table you want to retrieve.

    • Issue additional FLASHBACK TABLE ... TO BEFORE DROP statements until you retrieve the table you want.


RENAME TO Clause Use this clause to specify a new name for the table being retrieved from the recycle bin.

Notes on Flashing Back Dropped Tables The following notes apply to flashing back dropped tables:

  • Oracle Database retrieves all indexes defined on the table retrieved from the recycle bin except for bitmap join indexes and domain indexes. (Bitmap join indexes and domain indexes are not put in the recycle bin during a DROP TABLE operation, so cannot be retrieved.)







Restoring a Table to an Earlier State: Examples The examples below create a new table, employees_test, with row movement enabled, update values within the new table, and issue the FLASHBACK TABLE statement.

Create table employees_test, with row movement enabled, from table employees of the sample hr schema:

CREATE TABLE employees_test 
  AS SELECT * FROM employees;

As a benchmark, list those salaries less than 2500:

SELECT salary
  FROM employees_test
  WHERE salary &lt; 2500;




Enable row movement for the table:

ALTER TABLE employees_test


UPDATE employees_test
  SET salary = salary * 1.1
  WHERE salary &lt; 2500;

5 rows updated.


SELECT salary
  FROM employees_test
  WHERE salary &lt; 2500;


Restore the table employees_test to its state prior to the current system time. The unrealistic duration of 1 minute is used so that you can test this series of examples quickly. Under normal circumstances a much greater interval would have elapsed.

FLASHBACK TABLE employees_test


SELECT salary
  FROM employees_test
  WHERE salary &lt; 2500;


Retrieving a Dropped Table: Example If you accidentally drop the pm.print_media table and want to retrieve it, then issue the following statement:


If another print_media table has been created in the pm schema, then use the RENAME TO clause to rename the retrieved table:

FLASHBACK TABLE print_media TO BEFORE DROP RENAME TO print_media_old;

If you know that the employees table has been dropped multiple times, and you want to retrieve the oldest version, then query the USER_RECYLEBIN table to determine the system-generated name, and then use that name in the FLASHBACK TABLE statement. (System-generated names in your database will differ from those shown here.)

SELECT object_name, droptime FROM user_recyclebin 
   WHERE original_name = &#x27;PRINT_MEDIA&#x27;;

OBJECT_NAME                    DROPTIME&lt;|im_end|&gt;Replication of CREATE TABLE ... SELECT Statements

This section discusses how MySQL replicates CREATE TABLE ... SELECT statements.

These behaviors are not dependent on MySQL version:

When the destination table exists and IF NOT EXISTS is given, MySQL handles the statement in a version-dependent way.

In MySQL 5.1 before 5.1.51 and in MySQL 5.5 before 5.5.6 (this is the original behavior):

In MySQL 5.1 as of 5.1.51:

In MySQL 5.5 as of 5.5.6:

These version dependencies arise due to a change in MySQL 5.5.6 in handling of CREATE TABLE ... SELECT not to insert rows if the destination table already exists, and a</pre>

右文（仅阅读辅助）：

<pre> change made in MySQL 5.1.51 to preserve forward compatibility in replication of such statements from a 5.1 master to a 5.5 slave. For details, see Section, “CREATE TABLE ... SELECT Syntax”.

When using statement-based replication between a MySQL 5.6 or later slave and a master running a previous version of MySQL, a CREATE TABLE ... SELECT statement causing</pre>

### 位置5461642｜random｜z=0.04007053

上下文5338，目标offset=209，目标token=" pinch"；原文档未知。

包含目标的模型可见前文：

<pre>mm. If you do, you will waste energy, suffer &quot;cutting in&quot; to soft surfaces, and have a high risk for pinch flatting. The most popular size range for tires at Trans Iowa is anything from 35mm to 42mm wide. (Based upon a survey I once took and years of observations.) Even going this big, pinch flatting still occurs, so running even bigger rubber is okay, as long as you can get by the idea of the wheels being slightly heavier. 
  • Tread: You really do not need to run any tires with a deep tread pattern. File tread would work fine at Trans Iowa, but a minimalistic tread pattern tire may also have a thin casing, so be careful. Micro-knobs are probably a good bet, as is most anything I&#x27;ve seen on a touring tire. That should get you pointed in the right direction.
  • Tubeless: I happen to like tubeless tires on Iowa gravel. It works great, essentially eliminates the possibility of a pinch</pre>

右文（仅阅读辅助）：

<pre> flat, and has better shock absorption qualities. Downsides are the initial set up and dealing with a cold, gooey mess if you do have to stick a tube in due to a flat tire issue.
  • Mud clearances: You definitely will need mud clearance at Trans Iowa. Well......there is a 95% chance you&#x27;ll run into a situation where mud clearance is necessary. (</pre>

### 位置5497992｜high_activation｜z=0.1637278

上下文5373，目标offset=750，目标token=" perhaps"；原文档未知。

包含目标的模型可见前文：

<pre> to cdrom/KNOPPIX/copy/.

The examples in there for password setting, shadow changing and X11 config 
creation should be quite easy to understand.

If there are anymore questions, you can of course reach me per mail or over 
one of this mailing lists.



PS: It would be possible to replace the first stage of the CD also with 
debian-installer (just add cloop and unionfs udebs), but I have not looked 
into it - as Knoppix is what I know best.
Version: GnuPG v1.2.4 (GNU/Linux)


Reply to:&lt;|im_end|&gt;

Re: RFS: julius - speech recognition engine

Hi Felipe,

Thank you for taking a look at the Julius package.

2010/7/13 Felipe Sateler &lt;fsateler@debian.org&gt;:
&gt; - Why do you modify the manpages via sed instead of patching them?

Because IMHO it&#x27;s much easier to maintain than having a big patch
which I have to update every time a manpage changes.

&gt; - You say you remove a manpage because you have a better one, but there
&gt; is not actually one (dfa_minimize)?

Good catch, fixed.

&gt; - Any reason why you don&#x27;t enable parallel builds with DEB_BUILD_PARALLEL?

Not really. I&#x27;ve added that now.

&gt; - Why are there only static libraries?

It&#x27;s what upstream&#x27;s build system provides, and I was told that the
libraries do stuff like calling abort() so I haven&#x27;t really bothered
about it. I want to look into this some day though and maybe patch it.

&gt; ... and I&#x27;m not quite confident about the license, specially about the
&gt; Kyoto District Court venue thing (clause 5).

Uhm, isn&#x27;t that a common thing in licenses? It&#x27;s the least clause I&#x27;d
have expected to be problematic, personally I&#x27;m more worried about the
advertising clause. In any case, I could live with it if the package
goes into non-free.

I&#x27;ve updated the package to include the manpage and to enable parallel
building. http://mentors.debian.net/debian/pool/main/j/julius/julius_4.1.5-1.dsc


Siegfried-Angel Gevatter Pujals (RainCT)
Free Software Developer       363DEAE3

Reply to:&lt;|im_end|&gt;

Re: [PageVisibility] specific visibility states

From: Kyle Simpson &lt;getify@gmail.com&gt;
Date: Mon, 2 May 2011 01:55:51 -0500
Message-ID: &lt;A49722F84BA842C88E280F1A99A16D10@spartacus&gt;
To: &quot;Jason Weber&quot; &lt;jweber@microsoft.com&gt;, &quot;Cameron McCormack&quot; &lt;cam@mcc.id.au&gt;, &lt;public-web-perf@w3.org&gt;
&gt; From our discussion at the F2F, my understanding was that the 
&gt; PAGE_PAGE_PREVIEW state was intended to capture the scenario where the 
&gt; page is in some preview form and not intractable. For example minimized 
&gt; into a dock or tile of some type. It indicates the page is visible in some 
&gt; smaller preview state.

Is the reasoning behind this that the site would do something *different* 
than it would if it were in the hidden state? Like are you suggesting a site 
would modify its own rendering state to account for the fact that it was in 
a preview state, and perhaps</pre>

右文（仅阅读辅助）：

<pre> even show/hide alternate content? That&#x27;s seems 
like quite a stretch of likelihood as a use-case. Seems to me that a page is 
either fully visible, or not visible at all... this in-between stuff seems 
like getting too deep in the weeds.

&gt; I personally don&#x27;t believe we need the PAGE_TASKBAR_PREVIEW state. This 
&gt; came out of the F2F discussion</pre>

### 位置5850194｜high_activation｜z=0.1627512

上下文5717，目标offset=946，目标token=" before"；原文档未知。

包含目标的模型可见前文：

<pre>ice, Orlík, Prague and Ronov. In March 1420, after the Battle of Sudoměř, Vožice was occupied by about 2000 horsemen led by Mikeš Divůček of Jemniště, master of the Kutná Hora mint. On Good Friday 1420, Jan Žižka attacked the town and set it afire. Many lords were captured or killed, but those who escaped to the castle got away with their lives. Žižka also seized a lot of horses.In September 1425 commander Jan Hvězda of Vícemilice aka Bzdinka conquered the castle after 5 weeks&#x27; besiegement, had the castle destroyed and the town was attached to Vlašim. Mladá Vožice was then owned by many feudal houses. In 1678 the Küenburgs, who adjoined other smaller possessions in the area, established it a hereditary estate. Long before 1848 up to the 1960s German was spoken among the wealthy while Czech was only spoken by the common people striving to make a decent living.As early as late 18th and early 19th centuries but the highlight came after the events of 1848, Czech nationalism developed. After 1860, teachers and clerks arrived after the school enlargement and establishment of a regional office, tax office and financial pension control. In 1862 the choir Vlastislav was founded by the patriotic teacher Čeňek Sedmík. At that time a Reading Club strived in the town but later it ceased to exist. Obviously, the national and cultural initiatives came mainly from the immigrant intelligence. For example, the local theatre club established in 1865 was run by educated people including immigrants.In 1875, the Voluntary Fire Brigade was established and expanded with a large fire brigade garage in 1945 and presently four large fire engines. The magazine Vožičan (Vožice citizen) was issued in 1884 and the young generation published the hand-written magazine Potěr (Spawn). 1885 marked the founding of the gymnastics organization Sokol. There was a district court in Mladá Vožice, a forestry administration office, a tax office, a gendarme office, a financial pension control, a chemist, two physicians, two veterinarians and a gelder, a notary, two lawyers, two taxis, two hotels, 6 pubs, and 3 cartmen as well as an almshouse, a charity hospital, an orphanage, a post office and the movie theater plus four small savings banks and four insurance representatives. Mladá Vožice held annual markets, monthly markets and cattle markets, and Thursday piglet markets. The citizens of Mladá Vožice and surroundings were employed mainly on the royal estate, at the sawmill, brickyard, brewery and fish hatchery,  other farms in the area, local distilleries, the Vožice quarry, slaughterhouse, agricultural cooperative and granary, mills, state stud farm or were employed in the forest administration. After 1918 there were also two car repair services, a hosiery mill, laundry and pressing shop as well as a steam power plant. By 1945 there were 74 various craftsmen and 37 various shops in the town, a small furniture factory, and two building companies. Mladá Vožice citizens made a living by cutting wood for households, bringing water from the fountains, and picking fruit. In the 19th and early 20th centuries, they went to work to the gold mine Roudný. Apart from the above mentioned jobs they found seasonal and round-the-year ones all over the republic and before around Austria-Hungary. The town and neighbourhood of Mladá Vožice was a purely agricultural area until late 1945 when industrialization began. Until 1947 Mladá Vožice had been a court district in the politcal district of Tábor that occupied an area of 268 sq km and had 17422 inhabitants in 141 villages and remote settlements, associated in 39 political municipalities, two towns (Mladá Vožice and Miličín) and one township Kamberk (formerly Zlaté Hory, before</pre>

右文（仅阅读辅助）：

<pre> that Kamberk). Since 1949, after the change in the political and state system, Mladá Vožice was included in the newly established district of Votice in Prague region. After 1960 Mladá Vožice fell under the district of Tábor in South Bohemian Region.In 1975-1</pre>

### 位置6055772｜random｜z=0.05154514

上下文5918，目标offset=910，目标token=" can"；原文档未知。

包含目标的模型可见前文：

<pre> the other stories we are watching today.


&#x27;m overprotective. that&#x27;s why i got a subaru. love. it&#x27;s what makes a subaru, a subaru. i have to know the weather patterns. i upgraded to the new sprint direct connect. so i can get three times the coverage. [ manager 2 ] it&#x27;s like working in a giant sandbox. with all these huge toys. and with the fastest push-to-talk... i can keep track of them all. [ male announcer ] upgrade to the new &quot;done&quot; with access to the fastest push-to-talk and three times the coverage. now when you buy one kyocera duraxt rugged phone for $69.99, you&#x27;ll get four free. other offers available. visit a sprint store, or call 855-878-4biz. it&#x27;s a challenge to balance work and family. ♪ that&#x27;s why i love adt. i can see what&#x27;s happening at my business from anywhere. ♪ [ male announcer ] now manage and help protect your small business remotely with adt. arm and disarm your alarm, watch secure video in real time, and even adjust your lights and thermostat wherever you are. with adt, you get 24/7 protection through our exclusive fast response monitoring. you can be confident that adt is always there for you. hey, lisa. is tha

to be careful... hi, sweetie. hi, mom. (mom) but just to be safe... i got a subaru. (announcer) love. it&#x27;s what makes a subaru a subaru. could lose tens of thousands of dollars on their 401(k) to hidden fees. thankfully e-trade has low cost investments and no hidden fees. but, you know, if you&#x27;re still bent on blowing this fat stack of cash, there&#x27;s a couple of ways you could do it. ♪ ♪ or just go to e-trade and save it. boom. ♪ &gt;&gt;&gt; how about a little music on a monday for you today? let&#x27;s talk grammy awards. i was on twitter right there with you as we were watching the show together. a couple of my highlight, justin timberlake is back. brought out jay-z there on stage. love the black and white. also loved the tribute at the very end. elton john,

? girl: ok. dad: you look so pretty. ♪ i&#x27;m overprotective. that&#x27;s why i got a subaru. love. it&#x27;s what makes a subaru, a subaru. &gt;&gt;&gt; some of the hottest stories in a flash, rapid fire. roll it. the coast guard now is suspending its search for a couple and two children off the coast of san francisco. &gt;&gt; coast guard, coast guard, we are abandoning ship. this is the charmblow, we are abandoning ship. &gt;&gt; now officials are saying that distress call from a sailboat may be a hoax. it cost hundreds of thousands of dollars since sunday. coast guard investigators will look into and prosecute if they find it to be a hoax. &gt;&gt;&gt; and ka-ching, in new jersey, you soon will be able to gamble from work or at home wearing your bathrobe. governor chris christie signed a bill yesterday, legalizing internet gambling. its largest expansion of legalized gambling in new jersey since atlantic city&#x27;s first casino opening. that was back in 1978. governor christie says it will make new jersey more competitive with other states, and bring in much needed revenue since the casinos will be able to offer online wagerin


Excerpts 0 to 9 of about 10 results.

(Some duplicates have been removed)

Terms of Use (10 Mar 2001)&lt;|im_end|&gt;Real DVD: legit DVD copying, playback, but is it too late?

58 posts • Previous  
  • 1
  • 2
  • Real is just bizarre. They come up with all of this great technology and sometimes good ideas, and then tie the result of their work to player software that is clunky, bloated, and unloved.

    There has to be something about that player that I&#x27;m not seeing...

    In any case, it doesn&#x27;t matter if their solution has a market or not, and even DRM isn&#x27;t a major issue for some people, but as long as Realplayer and only Realplayer can</pre>

右文（仅阅读辅助）：

<pre> display the content I&#x27;ll pass.
    I&#x27;m surprised the studios are going along with this. I always thought the problem with rumors/hopes of DVD-ripping features added to iTunes is that allowing this would eliminate the distinction between buying and renting DVDs. Both are important markets to the studios. If Joe Consumer can &quot;buy&quot; a DVD for the cost of renting it at Red Box, doesn&#x27;t</pre>

## Feature 7415，h_V=0

### 位置466698｜high_activation｜z=0.326348

上下文456，目标offset=64，目标token="."；原文档未知。

包含目标的模型可见前文：

<pre>ikawa M, Okada N: LINEs mobilize SINEs in the eel through a shared 3′ sequence.

    Cell 2002, 111:433-444. PubMed Abstract | Publisher Full Text OpenURL

  23.</pre>

右文（仅阅读辅助）：

<pre> Dewannieux M, Esnault C, Heidmann T: LINE-mediated retrotransposition of marked Alu sequences.

    Nat Genet 2003, 35:41-48. PubMed Abstract | Publisher Full Text OpenURL

  24. Gilbert N, Labuda D: CORE-SINEs: eukaryotic short</pre>

### 位置1462902｜random｜z=0.105889

上下文1429，目标offset=767，目标token=" with"；原文档未知。

包含目标的模型可见前文：

<pre> marathon for the first time during the race, and that may not be a pleasant experience for you.
Post a comment
Write a comment:&lt;|im_end|&gt;Sauces, Condiments, Oils, Marinades and Spice Blends

Course | Sauces and Condiments

Sauces and condiments are the exclamation point to a meal, adding flavor, moisture and a certain visual appeal. Marinades work to tenderize meat and poultry while also enhancing and improving flavor. Spice blends lend unique and distinctive flavor to a variety of dishes and are endlessly customizable.

Image Creative Commons by manalkhan

Sauce Recipes

Aam ki Chatni

Sauces | Aam ki Chatni

(Indian mango chutney)

When Westerners hear &quot;mango chutney,&quot; they usually think Major Grey&#x27;s — a sweet jamlike condiment studded with raisins. There are actually a variety of mango and other fruit chutneys made in India, but few contain raisins, some aren&#x27;t very sweet and many are quite spicy. Read more »


Ingredients | Annatto Seeds

(Puerto Rican annatto oil)

Achiote oil is used around the Caribbean to add a yellowish-orange color to dishes, especially arroz con pollo. It is known as rou-cou or huile de rou-cou in the French Caribbean. Filipinos refer to it as atsuete, or achute, oil. Read more »


Sauces | Ajvar

(Serbian roasted eggplant and pepper spread)

This vivid red eggplant and pepper spread originated in Serbia, but its popularity has spread throughout the Balkans and beyond. In Serbia, ajvar (Serbian: Ајвар) is made with the rogo pepper and can be mild, medium or spicy. Read more »


Ingredients | Apple, Green

(German applesauce)

Apfelmus is your basic applesauce that is a typical German accompaniment to roast meats like Schweinebraten. Jews of East European origin serve epl tsimes with latkes or use it to top blintzes. Applesauce is perfect as a dessert for children or babies as it is easily digested. It can also be used in many baking recipes to add moisture and cut down on the amount of fat. Read more »

Cajun and Creole Seasoning

Sauces | Cajun and Creole Seasoning

(American Louisiana herb and spice blend)

Whether you call it Cajun or Creole, this spicy seasoning mix has a booyah kick. Use Cajun and Creole seasoning to kick up the flavor quotient in everything from soups, stews, rice and beans to fish, chicken and gumbo. Commerical varieties of this blend of herbs and spices are available, but they are often mostly salt. It&#x27;s easy and cheaper to make your own. Read more »


Vegetables | Chakalaka

(South African spicy tomato, pepper and onion dish)



Sauces | Chimichurri over Filet Mignon

(Argentine parsley-garlic sauce for grilled meats)

This pungent herb sauce originated in Argentina. Chimichurri is the classic accompaniment to Argentine churassco, or grilled meats. You can also use chimichurri as a marinade. Read more »

Cranberry Sauce

Sauces | Cranberry Sauce

(American cranberry condiment)

Cranberry sauce is an essential part of any American Thanksgiving meal. Many families serve it for Christmas dinner too. Some people have to have cranberry sauce in the shape of a tin can. Others prefer this more naturalistic version. A less sweet cranberry sauce is served with</pre>

右文（仅阅读辅助）：

<pre> game birds in northern Europe. Read more »

Dhanya Chatni

Sauces | Dhanya Chatnia (Cilantro Chutney)

(Indian cilantro chutney)

Dhanya chatni is perhaps the most popular of all Indian chutneys. The bright, fresh flavor of the cilantro and citrus bite of the lemon juice make this condiment a perfect</pre>

### 位置1475298｜high_activation｜z=0.326348

上下文1441，目标offset=895，目标token=","；原文档未知。

包含目标的模型可见前文：

<pre> not been over Man a long period of time when he was nothing (not even) mentioned&quot; (76:1). Obviously, one day or six days, as described by the judeochristian scholars, can&#x27;t be very long period as quran says.

So. the Quran says, &quot;We have explained to man, in this Quran, every kind of similitude ...&quot; (17:96)because there are things which people &quot;don&#x27;t know&#x27; otherwise &#x27;don&#x27;t invent similitude for Allah; for Allah knows&quot; everything (Q;16:74).

Now, the Quran gives an advice &quot;Those who listen to the words, and follow the best (meaning) in it; these are the ones who Allah has guided, and these are the ones endued with understanding&quot; (Q; 39:18).

Obviously, the Muslim scholars who lived many centuries ago didn&#x27;t have the scientific knowledge, therefore, one can&#x27;t expect them to have the same interpretation of the Quran as on can give now. That&#x27;s whay I say you don&#x27;t understand Islam; you have learned it from the mollahs, Immams and sheikhs who only repeate what the greate scholars of ancient time understood, which aren&#x27;t necessarily the right ones.
&lt;|im_end|&gt;Religion &amp; Ethics: Content from Across the ABC




Date/Time 19 Dec 2013 2:33:38pm
Michael Kirby is aguing from a predilection of his own. His position is not objective and does not represent the majority Christian view on authority in Christian life. The core issue is the Christian view of the nature and purpose of marriage and the family. If the lawyer is a poor theologian he is an even worse scientist. Only those with a vested interest could possibly persuade themselves that there is scientific evidence to prove that gay people are born that way. I note that having claimed a scientific basis for that part of his argument he produces no evidence in support of it. What of legal training now?&lt;|im_end|&gt;4,761pages on
    this wiki
    The Sailcloth
    First appearance Skyward Sword (2011)
    Found Skyloft
    — In-game description
    Sailcloth Icon

    The Sailcloth is an item from The Legend of Zelda: Skyward Sword. It is made by Zelda to give to the winner of the Wing Ceremony as part of the ritual. Prior to the ceremony Zelda wears it as a shawl. To her delight, Link is the champion of the Wing Ceremony to whom she gives the Sailcloth. Link can use it like a parachute to glide slowly to the ground, or to catch updrafts so as to propel himself into the air. The Sailcloth is used to land safely when dropping from Skyloft to the surface. Its gliding function is similar to that of a Deku Flower, the Deku Leaf, and Ezlo from previous games.



      Advertisement | Your ad here

      Around Wikia&#x27;s network

      Random Wiki&lt;|im_end|&gt;Virtual Verduria

The Kebreni Language

Unlike Verdurian, whose grammar is not too far from European models, Kebreni has a grammar which deviates any way it can from English. I&#x27;m particularly proud of the verbal system.

You can decipher the map names using the lexicon.

You&#x27;ll need a Unicode font and browser to properly see the characters. If you can&#x27;t see them, you can read the pre-Unicode file.
--Mark Rosenfelder

     Verbs * Pronouns * Numbers * Derivational morphology
     Parameter order * Noun phrases * Adjectives * Conjunctions * Locative verbs * Questions * Complex sentences
Sound changes

Context [To Top]

The Monkhayic family of languages, though now restricted to Kebri and the southwestern corner of Dhekhnam, was once spoken throughout the Plain, and indeed has left its linguistic traces heavily on the map of the Plain. The Mishicama ocean, the Ctelm mountains, the Svetla, Menla, Vesi, Meuna, and Efrat rivers, the nations of Ismahi, Azgami, Koto, Melináe, and Érenat, lake Como, the Arosd delta, and the cities of Kebropol, Lädau,</pre>

右文（仅阅读辅助）：

<pre> Avéla, Ydamai, Raizumi, Nuveta, Kereta, Mituré, Gödo, Mogör, Melahdo, Trezhda, Mabola, and Pelym all have Monkhayic names.

The first states of men in the Plain were Monkhayic: Como and Meṫaiu on the upper Svetla,</pre>

### 位置2594515｜random｜z=0.04955358

上下文2535，目标offset=692，目标token=" D"；原文档未知。

包含目标的模型可见前文：

<pre> to go with)! Dolly, in interviews, makes no bones about how much plastic surgery she&#x27;s had; &quot;costs a lot to look this cheap!&quot; She&#x27;s bought her &quot;ageless&quot; look for sure.

Tek @368

&quot;Cone of Silence&quot;--ha ha ha ha ha. Good one.

M-O-M @366

As the door slams on Cadsuane&#x27;s exit, Rand observes, &quot;Who WAS that masked woman?!&quot; And no one would have read the next book! Nice syrupy abridged version for children.

Sam @371

Norla maybe not a &quot;wilder&quot; eh? Wowzers--hint hint. Great info find indeed. How special do you think she was? And how did Cadsuane &quot;luck-out&quot; to be the one to carry Norla&#x27;s torch? Doing pennance? Norla must have sought her out. It was probably common AS knowledge way back when, that young Cads had &quot;the Power&quot;.

I see you, Insectoid @381 stealing my thoughts!

~~Future Books Alert~~
You know, if Rand DID &quot;confide&quot; in someone in his ever-shrinking world, wouldn&#x27;t &quot;mind-lurker&quot; Moridin be able to overhear his plans at any time? Doesn&#x27;t Moridin soon become Rand&#x27;s &quot;alter-ego&quot;?

Rand doesn&#x27;t want any special women in his life knowing what he&#x27;s going to do, nor be anywhere near when he does whatever. So he doesn&#x27;t confide in them now.

And after sitting on top of the Mountain, does the New and Improved Rand emerge and figure out how to get that &quot;Shoe Phone with a Party-Line&quot; invented back at his school, so he can start communicating plans with Mat, Perrin, Elayne, Nynaeve, Lan and Egwene? Or will he have to Travel to each for reports?

Alice A
387. Wetlandernw
No, Sam, no hablo espanol... more than about exactly that much. *sigh* snookered again.

You stinker. :)
Kathy Keith
388. Babokathy

About Moridin:

If LTT has disappeared from Rand&#x27;s thoughts after the Dragonmount scene, (cuz 3&#x27;s a crowd) that leaves more room for Moridin to climb into Rand&#x27;s brain anytime he wants, doesn&#x27;t it?

And how does Moridin get into Rand&#x27;s dreams anyway? I thought Rand shielded his dreams at all times?! Yeah, yeah, Nae&#x27;blis Schme&#x27;blis, how&#x27;s Big M sneak in? And wouldn&#x27;t Min sense something &quot;bad&quot; from her Bond to Rand?

389. TAmyrlinring1
M-O-M@330 &amp; dwndrgn@357: Darn it! I hadn&#x27;t caught the &quot;challenge&quot; early on, but was reading through the posts and the discussion about it, and actually knew the answer, but noooooooo . . . you two went and beat me to it! Oh well, at least I kept reading posts long enough to find out I&#x27;m not an original!

Oh, and Toryx@336: Apt, but I think maybe it would be the other way around, you think of cleavage and it makes you think of D</pre>

右文（仅阅读辅助）：

<pre>olly.
Leigh Butler
390. leighdb

Ding ding ding!

Congratulations, you win a shiny new Internet.

Heh. I never thought I was posing quite that much a stumper for you guys...
391. TAmyrlinring1
leighdb@390: Not saying anything, but you might have &quot;outed&quot; some of us on</pre>

### 位置5367921｜high_activation｜z=0.3439261

上下文5246，目标offset=621，目标token=":"；原文档未知。

包含目标的模型可见前文：

<pre>.
  • If the processing time ended and you still had unbleached areas, do the process again a few days later, but not the very next day, and if you did it again then use the product only on specific areas.
  • If you have olive toned pale skin, bleaching would be ideal for you as it gives a fresh undertone to your skin.
  • If you&#x27;re not sure what you&#x27;re doing, call a salon and ask them to talk you through the steps. Also if you know some people at a salon you may ask them what bleach product they use, most salons will refuse to tell you but it&#x27;s worth a shot.
  • Once the new roots start showing up again, which is 3-4weeks depending on your hair type, you&#x27;ll need to bleach your facial hair again. People around you would most likely notice the difference especially if you have had really dark facial hair before you bleached. Long story short you&#x27;ll need to constantly buy the bleach product, one pack should be enough for couple of uses.
  • Some people like to bleach other areas of their bodies like chest hair, hair on your hands/knuckles or breasts, however if you wish to bleach your breasts including the nipples you&#x27;ll need some professional opinions before you do it as it might be very dangerous. 
  • Sometimes you feel a light burning sensation in some spots during the process, if it was annoying you try to lighten the mixture at that spot, if it kept burning then just remove.

Edit Warnings

  • Don&#x27;t go out in the sun right after you bleach, it&#x27;s best to do it on a cool/cloudy day, and not be exposed to the sun for nearly 24 hours, so if you&#x27;re going on a vacation be sure you bleach a few days before.
  • If you felt a severe burning sensation in the first few seconds of applying the product then remove right away and wash your face, it means the product you bought is not right for your skin.
  • Don&#x27;t let the process time exceed 10 minutes.
  • If you are allergic to any of the chemicals in the bleaching product then just don&#x27;t use, here are the Ingredients : &quot;Bleach powder: Talc, Magnesium Carbonate, Sodium Silicate, Ammonium Persulifate.&quot; &quot;Oxidizing Cream [the liquid in the bottle] : Aqua, Hydrogen Peroxide, Loureth-3, Ceteareth-20, Tetrasodium  EDTA, Phenacetin B.P&quot; each product&#x27;s ingredients may differ so make sure you read it.
  • 48 hours before the process, test your product on a small area of skin, preferably not on the face. This is to make sure you&#x27;re not allergic to the product.
  • Dyeing your eyebrows may lead to blindness, so if you really want to do it, the it&#x27;s better you ask a professional assistance.

Article Info

Categories: Facial Hair

Recent edits by:</pre>

右文（仅阅读辅助）：

<pre> BR, Kelly Patrick, Teresa

In other languages:

Español: Cómo decolorar el vello facial


Thanks to all authors for creating a page that has been read 88,352 times.

Was this article accurate?


Thank Our Volunteer Authors.

Follow us on Google+&lt;|im_end|&gt;Battle Pet

Pet Battle: Ammen Vale, Ashenvale, Azshara,</pre>

### 位置6078968｜random｜z=0.05333776

上下文5941，目标offset=570，目标token=" plain"；原文档未知。

包含目标的模型可见前文：

<pre> UFC interim bantamweight championship with a beautiful arm-triangle choke. A week later, Ronda Rousey and Liz Carmouche topped that fight with an epic battle which was the first female fight in UFC history, ending with yet another Rousey armbar

Of the three bouts that finished with a decision, St-Pierre vs. Diaz has to take the cake as the most entertaining bout. The other two, Demetrious Johnson versus John Dodson and Jose Aldo versus Frankie Edgar were both decent fights, but neither really lived up to the hype of being between two exciting stylistic fighters. Not to mention, the five-round decisions can get a little taxing to watch if there&#x27;s not much in the way of near-finishes. 

All things considered, GSP-Diaz was a good fight but only falls about middle of the pack in terms of entertainment when compared to the other main events so far in 2013. 

It certainly can&#x27;t be ranked above Silva-Stann, Rousey-Carmouche or Belfort-Bisping, but it does fit right in after that as the fourth or fifth-best UFC main event we have seen so far in 2013.&lt;|im_end|&gt;Tim Lincecum Earns the Victory, Pablo Sandoval Socks Two-Run Homer in Victory

From on April 4, 2013

146 reads



Tim Lincecum&#x27;s highly anticipated first start of the season included seven walks, a half-dozen hard-hit balls deep to the outfield and a message from Bruce Bochy.
It also turned out to be a victory for the right-hander eager to prove he&#x27;s back to being his old self.

Flag Article
This article is

What is the duplicate article?

Why is this article offensive?

Where is this article plagiarized from?

Why is this article poorly edited?

Flag This Article
San Francisco Giants San Francisco Giants: Like this team?
or to post a comment


Loading comments...
just now posted just now
  • Loading...
  • Nobody has liked this comment yet


Follow San Francisco Giants from B/R on Facebook


San Francisco Giants

Subscribe Now

We will never share your email address

Thanks for signing up.

Giants Christmas Wish List Hint: you can use arrow keys to navigate through this channel.&lt;|im_end|&gt;I&#x27;ll be the first to gush about how much I love youth sports.  I started rowing at the age of 12, though I was hardly competitive considering I barely broke five feet tall, but I was rowing nonetheless.  I love watching Pee-Wee football or the Little League World Series.  Watching those mini-adults who have so much love for the game and their teammates sans the monetary payoff is just plain</pre>

右文（仅阅读辅助）：

<pre> inspiring. But have we gone too far?

After reading Tom Farrey&#x27;s book Game On, I wonder how much is too much? Farrey&#x27;s searching leads him to watching 4-year old girls competitive ice hockey and 8-year old boys playing for an AAU national championship who couldn&#x27;t even define the word &#x27;national&#x27; (however, it was hardly national seeing as all you needed to be</pre>

### 位置8735499｜random｜z=0.01604528

上下文8538，目标offset=149，目标token=" G"；原文档未知。

包含目标的模型可见前文：

<pre> Labor Party, we will oppose and give no aid and comfort of any kind to either heroin trials or heroin injecting rooms.

ANDREW FOWLER: Tonight on Four Corners, the PM&#x27;s man and the politics of heroin.

DRUG WORKER1: Um, were they on the corner or what?


DRUG WORKER1: Just on the corner?

DRUG WORKER2: This guy.


ANDREW FOWLER: Every night, this car cruises the streets of Melbourne.

Such is the sensitivity of the work it does, we were not allowed to interview either the driver or his colleague.

DRUG WORKER1: Just ask him.

Yeah, he&#x27;s got a black plastic bag.

DRUG WORKER2: G</pre>

右文（仅阅读辅助）：

<pre>&#x27;day, mate.

How are you?

Do you want to just come round to the other side of the car?

ANDREW FOWLER: Both are drug workers, supplying heroin addicts and even dealers with hundreds of clean needles.

DRUG WORKER1: What you after?

HEROIN USER: Can I grab a box of 100?


I can get you a box of</pre>

### 位置10358063｜random｜z=0.05173558

上下文10123，目标offset=1017，目标token=" getting"；原文档未知。

包含目标的模型可见前文：

<pre> work the other way. PRC Ltd was under financial pressure, that much we know. It&#x27;s just as possible to turn Noble&#x27;s words around and say &#x27;yes, accountability can involve loss of wages, jobs, profits etc and that&#x27;s exactly why a company or CEO might try like hell to avoid responsibility, or preventative action.

by Philip Grimmett on February 14, 2012
Philip Grimmett
The elephant in the room is the failure of successive governments to ensure workers and members of the public are safe. A fundamental human right in a civilized democracy,I would have thought.The influence of business at the expense of human life is reprehensible and points towards our global predicament.Good luck to you all.

Post new comment

You must be logged in to post a comment.&lt;|im_end|&gt;

Ben Franklin was one of the greatest grand strategists in American history. He “had the vision of the Great Power of the New World” as refugees from the Old World poured in, writes Conrad Black in his page-turning, tour-de-force Flight of the Eagle: The Grand Strategies That Brought America from Colonial Dependence to World Leadership. Franklin then followed up that vision with brilliant diplomacy and sponsoring, along with George Washington, the constitutional efforts of Madison, Hamilton and Jay. 

The flow of immigrants to America was crucial not only in the initial rise of America as a credible power in the world, but also in dealing with the stain of slavery: the North would have been unable to defeat the South in the Civil War if the North had not had a three to one advantage in population because of its greater ability to attract immigrants.

Ratio of Per Capita GDP: China/US


In the rest of the 21st century, America faces another grand-strategic challenge: the challenge of China. Since Deng Xiaoping’s economic reforms were introduced in December of 1978, China’s economy has been growing at a ferocious pace. As former Treasury Secretary Larry Summers put it, at Chinese growth rates, “In a decade, an individual goes from walking to having a bicycle; in another decade to a motorcycle; in another decade or two to having an automobile.” Yichuan Wang explains in “How China’s poorest regions are going to save its growth rate,” the reason the Chinese economy can grow so fast is that it is in the midst of “catch-up growth”: that is, it can copy technologies that have already been researched and developed better than other countries. As shown in the graph above, China went from a per capita GDP (income per person) less than 1/50 of the US level to per capita GDP of roughly 1/6 the US level in the 30 years from 1980 to 2010. It will not be easy for China to get all the way to the US level of income per person, but with half-decent economic policies, it should have no problem getting to half the US level of income per person.

The reason China’s economic rise matters for US grand strategy is that China has a much larger population than the United States. Indeed, as the graph below shows, the US now has less than a quarter the population China has (the extreme measures China has taken to hold down its population growth since 1979 through its one-child policy have stabilized the ratio of US to Chinese population in recent years). Multiplying per capita GDP by population yields total GDP, so if China has 1/4 the per capita GDP, but four times as many people, its total GDP will be the same size. More generally, if China gets to a larger fraction of US per capita GDP (see graph above) than the US population as a fraction of China’s population (see graph below), then China’s total GDP will be bigger. Although per capita GDP is what matters for people’s standard of living, total GDP is crucial for the ability of a country to wage war—or more importantly, to deter other countries from waging war against it. Power corrupts. So even though idealism has had some effect on US foreign policy (as Black details), it should surprise no one that the US has done some bad things as a superpower. Yet I am convinced that the combination of Chinese nationalism and “Communist” oligarchy—or the combination of Chinese nationalism with some tumultuous future political transition in China—would lead a dominant China to behave much worse than the US has.

Untitled drawingData source: Populstat and Census

What can be done to maintain US power relative to China? The worst answer would be to try to inhibit China’s economic growth. Berkeley economics professor and influential blogger Brad DeLong’s rhetorical question says it best:


An excellent answer is to do everything possible to foster long-run growth of per capita GDP in the US. At a minimum, this includes radical reform of our system of K-12 education, removing the barriers state governments put in the way of people getting</pre>

右文（仅阅读辅助）：

<pre> jobs, and dramatically stepped-up</pre>

## Feature 7587，h_V=3

### 位置856787｜random｜z=0.08226011

上下文837，目标offset=375，目标token="\n"；原文档未知。

包含目标的模型可见前文：

<pre> say the chances are 2-to-1 before the end of the year.

Q: Honestly? Both sides are pretty dug in.

A: I’ve had senators talk to me — Democrats and Republicans — who want to move on. Our hearings are having an effect on them. So, I think there’s a way to get there.

Q: Which side will have to give in?

A: We’ll know more on Labor Day after we go through August and the hearings.

Q: You were among the 17 House Republicans who voted against the House enforcement-only bill. Why?

A: There were issues in my jurisdiction [as chairman of the House Education and the Workforce Committee] in the bill. I was being denied my jurisdiction. Finally, they gave me my jurisdiction for 24 hours, which got under my skin. The employer provisions in there on verification — I wanted to do my work. I thought the Judiciary Committee work was haphazard, and I thought the employer provisions were nothing but unfunded mandates.

Q: How so?

A: Requiring them to look at all workers — all their workers, not new hires, all their existing employees — there’s no system to verify that, and we’re talking about a huge database run by the federal government. Scares me to death.

And so, for all those reasons, it was just easier to vote no.

In hindsight, I was probably more angry about jurisdiction than I was about the provision itself.

Q: If you hadn’t been upset about how it was handled, would you have voted for it?

A: Yeah. I voted for the fence. I voted for a lot of the amendments to make it tougher.

Story Continues →

View Entire Story
blog comments powered by Disqus

      Independent voices from the The Washington Times Communities

      Metro News


      Talking Sense
</pre>

右文（仅阅读辅助）：

<pre>&lt;|im_end|&gt;The Magazine

Naming Names

David Skinner, naming names.

May 5, 2008, Vol. 13, No. 32 • By DAVID SKINNER
Widget tooltip
Single Page Print Larger Text Smaller Text Alerts

One early sign of man&#x27;s superior station in the natural hierarchy was that he got to name the animals--this according to the Book</pre>

### 位置1339347｜high_activation｜z=0.1164398

上下文1309，目标offset=3，目标token="\n"；原文档未知。

包含目标的模型可见前文：

<pre>
National Review
</pre>

右文（仅阅读辅助）：

<pre>Pardon My English
Reason - Hit &amp; Run
Red State
Sudden Stop


Why Scott Brown Failed To Get Re-Elected

by: The Angelic One

Wed Nov 07, 2012 at 10:20:09 AM EST

Although a final count has yet to be made, Democrat Elizabeth Warren last night ousted Massachusetts Republican US Senator Scott</pre>

### 位置1519440｜random｜z=0.02952573

上下文1484，目标offset=1015，目标token=" \n\n"；原文档未知。

包含目标的模型可见前文：

<pre> 
55 boys; 32 years and 10 months; 7 days; one week; 30 
days, one month ; 365 days ; 12 months , 52 weeks, one year ; 

6. Read aloud, thinking of the meaning, Mans bals ; 
gan bal ; obs ; muls kil ; doms fol ; yels baltum ; jips 
tel; mugsziil; doabs balsetel; buks teltum ; muls 
balsetel ; yel bal ; dels kiltum malselul ; yel bal ; ols ; 
obs tel. 

7. Give the English of each of the above phrases. 

It is not sufficient to go through these exercises once ; they 
should be repeated again and again, until they can be spoken 
with the greatest rapidity. 

Each Volapuk exercise is to be first read aloud, thinking of 
the meaning, but not of the English words. Then it should be 
translated into English, the translation written down and com- 
pared with the key. After a time the key should be translated 
back again and compared with the original. 


The case endings are the first three vowets, 

-A. -E. -I. 

in the plural -AS. -ES. -IS. 

For example, i. Kim ? who ? 

2. Kima ? whose? of whom? 

3. Kime ? to whom ? 

4. Kimi ? whom ? 

The names of the cases are : kimfal, kimafal, kimefal, 
kimifal,&quot; taken from the cases of kim, with the word fal,&quot; 
meaning &quot;case.&quot; 

i. The kimfal, who-case or nominativ, is the simple form 
without any added vowel. It answers the question, &quot; Who ?&quot; 
It is usually translated by the English nominativ. 


2. The kimafal, or whose-case, ending in a, is the answer 
to the question, &quot;Whose?&quot; or &quot;Of whom?&quot; It is usually 

translated by the possessiv ( &#x27;s) or by &quot;of.&quot; Fat mana ; 

the mans father, or the father of the man. The kimafal is 
sometimes called the genitiv. 

3. The kimefal, or to-whom-case, ends in e and answers 
the question &quot;To whom?&quot; It is usually translated by to 
with the objectiv ; but frequently we omit the to ; thus we say 
&quot;I gave an apple to the boy,&quot; or &quot;I gave the boy an apple.&quot; 
&quot;Boy&quot; would be in the kimefal as expressing the indirect 
object of the action. The kimefal is sometimes called the 
dativ case. 

4. The kimifal, or whom-case, ends in i, answers to the 
question &#x27; &#x27; Whom ?&quot; and denotes the direct object. In the 
sentence just given &quot;apple&quot; would be in the kimifal. It 
corresponds nearly to the English objectiv. It is sometimes 
called the accusativ. 

As to endings : 

i. 2. -a 3. -e 

As to names : 

4. -i. 

i. Kimfal. 2. Kimafal. 3. Kimefal. 4. Kimifal. 
Or, after the classical style : 

i. Nominativ. 2. Genitiv. 3. Dativ. 4. Accusativ. 
Answering the questions 

i. Who? 2. Whose? Of whom ? 3. To whom ? 

4. Whom? 
Denoting usually 

i. The Subject. 2. The Possessor. 3. The Indirect 

Object. 4. The Direct Object. 
Translated by 

i. The Nominativ. 2. The Possessiv or of. 3. to. 

4. The Objectiv. 

The kimfal, preceded by the interjection o &quot; and followed 
by an exclamation point, is used in addressing a person : o 
sol!&quot; &quot;Sir.&quot; This is sometimes considered as a separate 
case, called the kimofal or vocativ. It seems, however, better 
to consider it a nominativ independent, as in English. 
O &quot; is sometimes omitted in this case. 


Prepositions regularly govern the kimfal. Thus, we express 
&quot;near me &quot; by nilii ob,&quot; not nilii obi &quot; nor ,,nilii obe ;&quot; 
&quot;out of the house,&quot; se dom,&quot; not se doma&quot; nor se 

Occasionally, the kimifal will be found after a preposition 
instead of i at the end of the preposition itself, as will be 
explained hereafter. 

</pre>

右文（仅阅读辅助）：

<pre>- A word used elliptically, like</pre>

### 位置1549361｜random｜z=0.0695648

上下文1514，目标offset=216，目标token=" \n\n"；原文档未知。

包含目标的模型可见前文：

<pre>, employment, situation. 

-am, appointment, inau- 
guration into office, 
can, exchange (of money). 

-apened, bill of 


cedon, to consider, deem. 
cek, check (draft), 
cellar, kav. 
cem, room. 

cen, change, variation, on, 
cent, sentab. 
central, zenodik. 
centre, zenod. 
century, yeltum. 
chair, stul. 

champagne, jamanavin. 
change, cen. 
to change, cenon. 
chance, fad. 
character, kalad. 
cheap, nedelidik. 
cheese, fbmad. 
check, cek, 
chemist, kiemavel. 
chemistry, kiemav. 




cherished, divik. 

chess, cog. 

chestnut, katan. 

chief, cif. 

child, cil. 

China, Cinan. 

chivalry, montial. 

</pre>

右文（仅阅读辅助）：

<pre>Christian, krit, kritik. 

church, gliig. 

cif, chief, director. 

cigar, zigad. 

cil, child. 

cin, machine. 

Cinan, China. 

ciniifad, mechanism. 

cipher, ziif. 

circuit, ziim. 

cit, deception, -on. 

civilization, kul</pre>

### 位置3216185｜random｜z=0.03392027

上下文3143，目标offset=408，目标token=";\n"；原文档未知。

包含目标的模型可见前文：

<pre>, three additional calls are defined:
 284        /* request a single GPIO, with initial configuration specified by
 285         * &#x27;flags&#x27;, identical to gpio_request() wrt other arguments and
 286         * return value
 287         */
 288        int gpio_request_one(unsigned gpio, unsigned long flags, const char *label);
 290        /* request multiple GPIOs in a single call
 291         */
 292        int gpio_request_array(struct gpio *array, size_t num);
 294        /* release multiple GPIOs in a single call
 295         */
 296        void gpio_free_array(struct gpio *array, size_t num);
 298where &#x27;flags&#x27; is currently defined to specify the following properties:
 300        * GPIOF_DIR_IN          - to configure direction as input
 301        * GPIOF_DIR_OUT         - to configure direction as output
 303        * GPIOF_INIT_LOW        - as output, set initial level to LOW
 304        * GPIOF_INIT_HIGH       - as output, set initial level to HIGH
 306since GPIOF_INIT_* are only valid when configured as output, so group valid
 307combinations as:
 309        * GPIOF_IN              - configure as input
 310        * GPIOF_OUT_INIT_LOW    - configured as output, initial level LOW
 311        * GPIOF_OUT_INIT_HIGH   - configured as output, initial level HIGH
 313In the future, these flags can be extended to support more properties such
 314as open-drain status.
 317introduced to encapsulate all three fields as:
 319        struct gpio {
 320                unsigned        gpio;
 321                unsigned long   flags;
</pre>

右文（仅阅读辅助）：

<pre> 322                const char      *label;
 323        };
 325A typical example of usage:
 327        static struct gpio leds_gpios[] = {
 332                { ... },
 333        };
 335        err = gpio_request_one(31, GPIOF_IN, &quot;Reset Button&quot;);
 33</pre>

### 位置4824142｜high_activation｜z=0.120346

上下文4715，目标offset=89，目标token="\n"；原文档未知。

包含目标的模型可见前文：

<pre>The spotlight will be on Durga Puja, Calcutta and Tagore when Sujoy Ghosh’s Kahaani is released this March. Ev ...  | Read.. 
Offering a culinary ode to Udit
Sonam’s style
Model minister
Oscar night
War loss
Tittle tattle
‘Parenting is a more explosive topic than ethnic conflict’
Scribe tale
Foreign face
Art heart
</pre>

右文（仅阅读辅助）：

<pre>Couple talk
‘Parenting is a more explosive topic than ethnic conflict’&lt;|im_end|&gt;Terra di Toscana www.terraditoscana.com


Town web Hotels Farmholidays Restaurants

Inhabitants in 1991: 87.100

The territory of Lucca extends for 185,53 square kilometres, occupying for the most</pre>

### 位置8148655｜random｜z=0.01780698

上下文7964，目标offset=555，目标token=".\n\n"；原文档未知。

包含目标的模型可见前文：

<pre> I don&#x27;t think there is really any control over what ads show up.

Is it worth the cost?

In the end you have to ask if the revenue you&#x27;re generating from random ads is worth the cost to your soul.  If you can slap on an Engin banner and get free hosting - maybe that&#x27;s worth it.  Right now though, my blogspot account is free, my Vent/Mumble server costs something like 3 bucks a month, and I think the guildlaunch no ads site is what - $10 a year?  I&#x27;ll throw that money out of my own pocket to know that I don&#x27;t have junk on my site that I don&#x27;t want.


  1. I&#x27;d like to thank the good folks at Coca Cola, Papa Johns, Goodyear, Sam Goody&#x27;s, Popeye&#x27;s chicken, and Hane&#x27;s Her Way for their support in keeping up this blog.

  2. Mmm - Popeye&#x27;s. I think my memory of Popeye&#x27;s is really distorted though, since I haven&#x27;t lived in New Orleans in like, 25 years.

  3. If I could get, say, stuff in kind from Coke to feed my caffeine addiction ... or from a pizza place or similar, I might consider it, screw my soul :D, but they don&#x27;t work that way and I&#x27;m right there with you Adgamorix. They just aren&#x27;t an effective or sensible thing for a blog.

  4. I will intentionally NOT click on an ad I see (blog or otherwise), just because I don&#x27;t like them.

&lt;|im_end|&gt;Young Horses, Inc

It may not look like it, but Octodad may be one of the sadder, more thought-provoking games at PAX


Imposter syndrome is the feeling of being a fake. It makes people feel that they didn’t earn of the success or good things in their life, and others are going to find out about this fraud. It’s a mixture of crippling self-doubt with the idea that nothing you have was earned, and it was all just a matter of luck. That’s how I felt when playing Octodad, the upcoming game where you’re an octopus trying to pass for a man, and you’re forced to hide your identity while trying to create a happy home environment for your human wife and kids.

“Our goal was to make things that are very mundane, like cleaning up and putting things away, and tucking your kids in, and making that a challenge,” Philip Tibitoski, the CEO of Young Horses, Inc. told me. “You’re a character with no bone structure.”

Well, shit. There goes my deep analysis.

</pre>

右文（仅阅读辅助）：

<pre>A character with an existing history

The original version of Octodad was created when the team were students. It was released for free, and the game’s goofy theme and odd control scheme gained some underground buzz and a dedicated fan base. Some members of the Octodad team went off to join “big name” companies, while the rest stayed to work on adding more meat to the concept,</pre>

### 位置10475459｜high_activation｜z=0.1222992

上下文10238，目标offset=766，目标token="\n\n"；原文档未知。

包含目标的模型可见前文：

<pre> schedule but all of a sudden around 3 weeks old she just figured it out. We also started giving her a little more to eat (I had to pump all of the breastmilk b/c she refused to nurse) for a bedtime bottle, and that got her to sleep longer at the nighttime and she just &#x27;fixed&#x27; herself. Good luck, I&#x27;m sorry you are feeling so lost :(
posted 03/25/2011 by nbuchholtz
Was this answer helpful?

0 out of 0 found this helpful

Answer this question
Featured video
Related videos
Your Pregnancy, Week by Week
Your Pregnancy, Week by Week
Have an account? Log in
Star Contributors in Behavior
Free Stuff &amp; Great Deals&lt;|im_end|&gt;How Long and what temp for a turkey? -*Ashley*- 4 kids; Missouri 109 posts
21st Nov &#x27;12
It&#x27;s a 19 lb turkey and i&#x27;m not sure what temp to cook it on or how long to cook it? HELP!
Amy {OneGirl, TwoBoys} 3 kids; Cincinnati, Oh, United States 24143 posts
21st Nov &#x27;12
20 min a pound. 350 usually&lt;|im_end|&gt;Letters to the Editor for May 30, 2012

Written by Baker City Herald readers May 30, 2012 08:58 am

Teachers deserve the raises

To the editor:

After reading an article in the Herald about salary increases for administrators in the school district, some would probably be in shock. However, even with the most laughable explanation that could be given for this decision, I can’t say I’m shocked at all. I did glean one important nugget of truth from the article: It’s good to know why they worked so hard to keep that budget balanced! I would believe that after this article was published, many put their paper down on their coffee tables and scratched their heads and said, “huh?” If so, they did with good reason.

Here’s how this logic works: Mrs. Burroughs stated that they (meaning administrators) worked really hard to make sure that the budget was balanced even through some tough decisions. For that reason, they’re worth every penny of their salary. In essence it’s a reward for a job well done. We want to keep them, so we’re giving them raises. That seems fair enough.

Now let’s juxtapose that claim with the following: Our teachers work 70-hour weeks and take their work home with them. Furthermore, they’ve produced some of the best results Oregon has to offer. They’re worth every penny of their salary (which, by the way, is close to a third of the quoted administrators’ salaries). We want to keep them, so we’re going to give them raises. That would be just as fair. Nonetheless, teachers were laid off, there have been hiring freezes, salary freezes, pro-rated insurance, and it seems that the cream of the crop in the district (the teachers) are the ones on the front line taking hits every time there’s a crisis.

Mrs. Burroughs’ explanation was not only laughable, but obviously impulsive. Simply put, it seems that some people want their raises because they think they’re CEOs and they have entitlement issues. Given how the board has recently conducted itself, I’m sure glad they don’t have a salary to claim from taxpayers. I believe that if the teachers’ union has any self-respect, they’ll address this issue. Again, it’s good to see why they worked so hard to make sure that budget was balanced! 

Jason Smith

Baker City

</pre>

右文（仅阅读辅助）：

<pre>Why should the cemetery suffer?

To the editor:

A question arises from two recent local newspaper articles reporting on the City Council meeting and discussions of May 22.

The city council approved the new fee schedules for certain city services, with a 20 percent increase for Mount Hope Cemetery being the largest of the various fee schedule increases.

The reason given was the city is working to make the cemetery fund</pre>

## Feature 8060，h_V=0

### 位置1071279｜random｜z=0.05549134

上下文1047，目标offset=24，目标token=" the"；原文档未知。

包含目标的模型可见前文：

<pre> happens next? What will the SES and other emergency services be doing tonight?

ALLAN BRIGGS: Well, tonight the</pre>

右文（仅阅读辅助）：

<pre> SES is actually deploying four of our lighting tower units. These are very fortunate. We have only had these units a short time. They provide lighting to light up the area and basically return it to daylight for the investigators. So the plants are coming up from around the northwest region and the SES volunteers are bringing them on-site and will stay here and assist though with the lighting, preserving the crime scene,</pre>

### 位置2120925｜random｜z=0.03226746

上下文2072，目标offset=870，目标token="prove"；原文档未知。

包含目标的模型可见前文：

<pre> if I can make something leaner, faster, and all around better without having to support a previous over-engineered product I&#x27;d drop it. Why keep something that doesn&#x27;t need to be used? Almost like &quot;code hoarding&quot;. Maybe I&#x27;m looking at it differently than an a linguists. :) But your points are well put. –  Oscar Godson Jun 3 &#x27;11 at 21:29
@Oscar Godson: Except we do have to support the previous product. We can&#x27;t just flip a switch and suddenly everyone is using the New English. Plus, I am not convinced the proposal is &quot;leaner, faster, and all-around better&quot; than the status quo. Part of the point was that legacy becomes especially compelling if the advantages of the change are weak. –  John Y Jun 3 &#x27;11 at 22:01
@Oscar, funnily enough, I&#x27;m a software engineer too. I think your analogy is quite instructive. I&#x27;m sure you&#x27;ve suffered the pain of coming up with something that has benefits over a legacy system, only to find resistance from management because the cost of replacing the legacy system is too great (risk, training, inertia, etc). I think that, with linguistic conventions, you&#x27;re facing a huge &#x27;training&#x27; cost as well as the fact that there is no central authority to mandate it. As a result, benefits must be great and self-evident if a change is to take place. –  Dancrumb Jun 3 &#x27;11 at 23:00
show 5 more comments

@Dancrumb made a perfectly well-reasoned and appealing (to me) answer. I’ll just give a single example:

The dog’s bark warned them    vs.    The dogs’ bark warned them

So: yes, apostrophes are “needed”.

share|improve this answer
Or worse: &quot;The dogs bark warned them&quot; which makes no sense at all. –  Alenanno Jun 3 &#x27;11 at 19:23
@Alenanno, why, &quot;to bark warn&quot; is a nice verb :) –  Cyril Jun 3 &#x27;11 at 19:33
@Cyril ahahah yeah, it might work... –  Alenanno Jun 3 &#x27;11 at 20:00
@Cyril: Definitely a nice &#x27;compound verb&#x27;. Could even be indispensable if you needed to distinguish between your dogs bark warning you of a run-of-the-mill burglar, and whimper warning of an attack by 20-foot bug-eyed monsters. But as is so often the case, I think such neologisms would have to be ushered in gently, complete with hyphens for the first few decades. –  FumbleFingers Jun 3 &#x27;11 at 20:25
The link i provided mentions this and he offers an alternative (which I&#x27;m not fond of myself), but offers a z as a replacement. However, another point could be, could we drop it for everything except compound verbs? Just a thought :) –  Oscar Godson Jun 3 &#x27;11 at 21:31
add comment

The majority of punctuation is probably redundant as well but what would you rather read a book with no paragraphs no periods no commas no apostrophes etc or a properly punctuated book heres what it comes down to ease of comprehension yes you could figure out the no punctuation book just fine if you thought about it long enough but it would be a massive headache and require several extra hours to read the same book which leads me to believe that anyone who would advocate discontinuation of punctuation has never had a real job in their entire life if you wrote a technical manual or book intended to be read by computer or electrical engineers and it didnt have punctuation you would be the ridicule of the entire industry or at the very least the office

(There are most probably enough clues within the above text to figure out where the sentences begin and end, where the commas, apostrophes, etc. should go, etc. I trust that you are willing to figure it out!)

share|improve</pre>

右文（仅阅读辅助）：

<pre> this answer
I read right through that fine in all honesty :) I might have even read it faster because there were no periods or commas since normally when I come across them I naturally pause. –  Oscar Godson Jun 4 &#x27;11 at 6:41
add comment

I can&#x27;t seem to find a use case other than it&#x27;s &quot;legacy&quot; in English…

That&#x27;s</pre>

### 位置4173945｜random｜z=0.0337323

上下文4079，目标offset=550，目标token=" But"；原文档未知。

包含目标的模型可见前文：

<pre> So, in this case, I&#x27;m curious, though, what would you argue is the motivation, or is there a motivation, it&#x27;s just an inherent need to help someone out? In other words, why did the ape go to the rescue of the juvenile?

Dr. DE WAAL: I think the ape was emotionally affected. And that&#x27;s basically what happens. If you are distressed because somebody else is distressed, then rescuing the other individual also alleviates your own distress. And so there is a selfish component to sympathy in the sense that you&#x27;re, in a way, also helping yourself if you help somebody else. And that&#x27;s why certain studies - now they&#x27;re doing studies on altruism in humans in the brain scanner where they find that if you do good, you feel good. And actually the reward centers in your brain lighten up because you get this positive feeling. And so altruistic behavior has this component of that you also feel good while you do it.

PALCA: We&#x27;re talking with Frans de Waal about this new book, &quot;The Age of Empathy: Nature&#x27;s Lessons for a Kinder Society.&quot; We have to take a short break. We&#x27;ll be taking your calls at 800-989-8255. That&#x27;s 800-989-TALK. Or you can send us a tweet and ask Frans de Waal what he - what you think, or tell him what you think about empathy and how it affects us today. So, we&#x27;ll take this break. Please stay with us.

(Soundbite of music)


(Soundbite of music)

PALCA: From NPR News, this is SCIENCE FRIDAY. I&#x27;m Joe Palca. We&#x27;re talking this hour about empathy. And my guest is Frans de Waal. He&#x27;s a professor of psychology at Emory University in Atlanta. He&#x27;s also the author of &quot;The Age of Empathy: Nature&#x27;s Lessons for a Kinder Society.&quot; We&#x27;re taking your calls at 800-989-8255. And let&#x27;s take one of your calls right now. Let&#x27;s go to Jim(ph) in Eagle River, Arkansas. Jim, you&#x27;re on the air with SCIENCE FRIDAY.

JIM (Caller): Hello, thanks. Alaska, actually.

PALCA: Oh, Alaska. Hmm.

JIM: That&#x27;s okay. Competition and survival of the fittest seems to apply most to plants, but animals, I suspect, get their survival advantage by mutual aid -the other side of the coin, maybe, in evolutionary thought. And it used to be studied more - or mentioned more - the concept of mutual aid. But</pre>

右文（仅阅读辅助）：

<pre> almost all animals exhibit mutual aid. They help the others of their species, and sometimes - and it has reproductive value…


JIM: …for the species as well as the individual.

PALCA: Okay. Jim, let me get Dr. de Waal&#x27;s take on that. And sorry about the Alaska thing.

JIM: Oh, yeah. That&#x27;s okay.

Dr. DE WAAL</pre>

### 位置4478748｜high_activation｜z=0.5076092

上下文4377，目标offset=493，目标token="2"；原文档未知。

包含目标的模型可见前文：

<pre> keeping you overweight... your first weapon is learning what they are and how they do that.

2. Carbohydrate cravings are your biggest enemy. Your second secret weapon is the plan we will show you to overcome these cravings!

If you want to know exactly how to make this happen in the next five days then just click my link below... it&#x27;s all in my free book.

But let&#x27;s get on with the article:

Here&#x27;s a question you might be asking: &quot;How come after a diet, I just seem to put all the weight back on again? The sad reality of our times is that if you are chronically overweight, then its almost certain that you are on the North American diet most typified by the McDonald&#x27;s fast food meal... maybe &quot;low in fat&quot; these days, but bursting at the seams with highly processed carbohydrates and sugars.

Doesn&#x27;t matter if it&#x27;s a fish burger or a lean chicken burger... it&#x27;s the fries, the buns the desserts and the drinks that are doing you in! This doesn&#x27;t make you a bad person... it just means that, like the rest of us, you have been suckered in by the advertising.

Here&#x27;s why it&#x27;s so important for you to understand what&#x27;s happening to your body... the North American Diet has made your body insensitive to insulin and insulin is the key to successful weight loss and control of diabetes Type 2. This is how it happens and why it&#x27;s so bad:

When you eat, the food in your stomach gets converted into glucose that moves into your bloodstream. This is the food that your brain, your muscles and your tissues need in order to survive and grow.

When glucose enters your bloodstream, your pancreas responds by releasing insulin into your blood. Insulin is needed to allow the glucose to enter your cells. There, it is broken down to produce the energy needed for your cells to work properly.&lt;|im_end|&gt;tag:blogger.com,1999:blog-7675087351939177300.post5166892779408797469..comments2013-12-19T07:29:30.113-06:00Comments on Sutured for a Living: Unused and Old Medicationsrlbateshttp://www.blogger.com/profile/152</pre>

右文（仅阅读辅助）：

<pre>36331355857884458noreply@blogger.comBlogger2125tag:blogger.com,1999:blog-7675087351939177300.post-389173942744370612</pre>

### 位置4479188｜high_activation｜z=0.5076092

上下文4377，目标offset=933，目标token="6"；原文档未知。

包含目标的模型可见前文：

<pre> keeping you overweight... your first weapon is learning what they are and how they do that.

2. Carbohydrate cravings are your biggest enemy. Your second secret weapon is the plan we will show you to overcome these cravings!

If you want to know exactly how to make this happen in the next five days then just click my link below... it&#x27;s all in my free book.

But let&#x27;s get on with the article:

Here&#x27;s a question you might be asking: &quot;How come after a diet, I just seem to put all the weight back on again? The sad reality of our times is that if you are chronically overweight, then its almost certain that you are on the North American diet most typified by the McDonald&#x27;s fast food meal... maybe &quot;low in fat&quot; these days, but bursting at the seams with highly processed carbohydrates and sugars.

Doesn&#x27;t matter if it&#x27;s a fish burger or a lean chicken burger... it&#x27;s the fries, the buns the desserts and the drinks that are doing you in! This doesn&#x27;t make you a bad person... it just means that, like the rest of us, you have been suckered in by the advertising.

Here&#x27;s why it&#x27;s so important for you to understand what&#x27;s happening to your body... the North American Diet has made your body insensitive to insulin and insulin is the key to successful weight loss and control of diabetes Type 2. This is how it happens and why it&#x27;s so bad:

When you eat, the food in your stomach gets converted into glucose that moves into your bloodstream. This is the food that your brain, your muscles and your tissues need in order to survive and grow.

When glucose enters your bloodstream, your pancreas responds by releasing insulin into your blood. Insulin is needed to allow the glucose to enter your cells. There, it is broken down to produce the energy needed for your cells to work properly.&lt;|im_end|&gt;tag:blogger.com,1999:blog-7675087351939177300.post5166892779408797469..comments2013-12-19T07:29:30.113-06:00Comments on Sutured for a Living: Unused and Old Medicationsrlbateshttp://www.blogger.com/profile/15236331355857884458noreply@blogger.comBlogger2125tag:blogger.com,1999:blog-7675087351939177300.post-38917394274437061202008-01-01T23:13:00.000-06:002008-01-01T23:13:00.000-06:00Hey there, I was horrified when I found out how an...Hey there, &lt;BR/&gt;&lt;BR/&gt;I was horrified when I found out how antidepressants are adversely affecting mussels and other bivalves. It just blew me away, never imagined this kind of effect. &lt;BR/&gt;&lt;BR/&gt;Glad you (and my HMO&#x27;s pharmacy) are spreading the word. My mom has a medicine cabinet full of Quaaludes and Dilaudid and other exciting products. I think dating 1970s forward. Just this weekend, talked her into creating a goody bag to be hauled off to the HMO. Returned. Too bad there isn&#x27;t a safe way to recycle them to other people who could use &#x27;em. Scary to think of the issues involved in that though.&lt;BR/&gt;&lt;BR/&gt;Um, forgive me for this? But -- tag -- you are it. A meme. Remember those? From the early days of blogging? Yep. Still around. This one is called &lt;BR/&gt;&lt;A HREF+ HREF=&quot;&quot; HTTP://THELAUNDRESS.BLOGSPOT.COM/2008/01/TAGGED-BY-NORMA-AND-PASSED-ON-TO-YOU-OR.HTML REL=&quot;nofollow&quot;&gt;7 weird/random things about me&lt;/A&gt;. Hoping you will give it a go? &lt;BR/&gt;Love, &lt;BR/&gt;tlThe Laundresshttp://www.blogger.com/profile/076</pre>

右文（仅阅读辅助）：

<pre>98451766032897477noreply@blogger.comtag:blogger.com,1999:blog-7675087351939177300.post-69410388097646800102008-</pre>

### 位置4479470｜high_activation｜z=0.5251874

上下文4378，目标offset=191，目标token="7"；原文档未知。

包含目标的模型可见前文：

<pre>6:00.000-06:002008-01-01T20:46:00.000-06:00Never even thought about this! I always just toss ...Never even thought about this! I always just toss them! &lt;BR/&gt;&lt;BR/&gt;Granted, most of ours, we finish, but there are the cases where we start one, and for one reason or another can&#x27;t tolerate it or we switch antibiotics ...or whatever ... and wind up with the medications. &lt;BR/&gt;&lt;BR/&gt;Then there are the OTC ones, those DO get sitting around the house ... &lt;BR/&gt;&lt;BR/&gt;No one had ever said anything to me about disposal. I just threw them all in the trash. &lt;BR/&gt;&lt;BR/&gt;Eeeks ...guess I need to pay more attention ...Dreaming againhttp://www.blogger.com/profile/157</pre>

右文（仅阅读辅助）：

<pre>17590226520457326noreply@blogger.com&lt;|im_end|&gt;Take the tour ×

Specific thoughts on character Leitmotifs.

For those who are confused, a Leitmotif is a usually simple piece of music used to represent a character, and is often played to signify that it&#x27;s, well, them! For example movies and</pre>

### 位置8494816｜random｜z=0.09257019

上下文8302，目标offset=907，目标token=" convers"；原文档未知。

包含目标的模型可见前文：

<pre> numbers have only grown in recent times. Change is inevitable, and it is being forced on society by many compulsions, including economic ones.

Reservations about reverse mortgage are bound to disappear with time. The move towards nuclear families, rising isolation of the elderly, and changing value systems are all slowly bringing about a metamorphosis in thinking. Wise retirees have opted for the scheme and used the lump sum to buy a smaller apartment in a gated community.

As family relationships slowly get redefined in India, the reverse mortgage scheme offers a welcome safety net for senior citizens. But for it to become truly popular, the government and banks need to tweak it and make it friendlier. That’s easier said than done. While a more reassuring approach to marketing could go a long way towards changing mindsets, it has to be accompanied by social change as well.

Quick Guide

Home owners over 60 are eligible

Maximum loan up to 60% of home value

Maximum tenure is 15 years

Monthly, quarterly, annual or lump-sum payments

Property is re-valued every five years

The sum received is not taxable&lt;|im_end|&gt;Though worldly goals are most sought after, these are elusive in nature. The ultimate goal to be attained is the knowledge of Truth — Tatva Jnana. The Upanishads reiterate that enlightenment is the highest Purushartha, leading to salvation. The Chandogya Upanishad teaches the path to Brahma Jnana and stresses the role of the mind in the act of realisation, pointed out Sri Mani Dravid Sastrigal in a lecture. It comprises eight chapters with the first five teaching the Upasanas or practices for Brahma Jnana and the last three the fruits of Upasana which is gaining Tatva Jnana.

Any activity, be it physical or mental, is carried out well if the mind is fully involved in it. It goes without saying that total coordination of the mind should be ensured when one tries to imbibe subtle truths. Enhanced levels of discipline and concentration are a must during a rigorous search for the Atma.

By nature, the mind is hyperactive and keeps flitting from one thought to another with extraordinary deftness. It influences the individual’s emotional state, causing a sense of joy or sorrow governed by one’s likes and dislikes. Such disturbances are definite hurdles faced by one seeking the truth of the Atma. It is indeed a great challenge for the seeker to gain control over the mind and direct it to meditate on the inner Self. This Upanishad teaches the various Upasanas to guide the mind develop ‘ekagrata’ or one-pointedness to bring it under control, meditation being shown as the crux of Upasana.

One has to dwell on the Atma and search for its roots. “From where does the Atma come? What is its essence? Where does it go?” During the quest, the differences that are manifest in the universe lead us to believe in each one’s individuality, giving rise to feelings of “You, Yours, Me, Mine and I.” It is to be realised that all beings are held within the Supreme Brahman. To attain this realisation through meditation, the Upanishad emphasises that the mind is to be tethered to Pranava or Omkara. Om, the prefix to Vedic chants, is not just a syllable but a symbol representing the very Supreme Brahman. Not just a prefix but a hand-hold to lead one to the Ultimate.&lt;|im_end|&gt;The manager of the Indian Overseas Bank branch in Keelkattalai, which saw a daring robbery on Monday, was warned barely four days ago to install CCTV and engage security guards, sources in the Chennai Police said.

Soon after the robbery in the Bank of Baroda (branch on the Rajiv Gandhi Salai on January 23, senior police officers held meetings with representatives of various banks to sensitise them to the urgent need to install CCTVs and engage trained private security personnel.

“The officials in the IOB Branch in Keelkattalai were also alerted less than a week ago by the Madipakkam police…they claimed to have written to their higher authorities seeking sanction,” an investigator told The Hindu .

Striking similarities

Explaining how the modus operandi of the robbers was the same as in the BOB branch case, he said the suspects looked like north Indians and convers</pre>

右文（仅阅读辅助）：

<pre>ed in English. “One of them spoke in Telugu. Soon after entering the bank, he ordered the employees and customers to move into a room by saying “lopala po…lopala po” (go inside, go inside). Another man, while forcing the manager to open the currency chest, spoke in fluent English.”

Since the looted money was from the teller&#x27;s cash counter,</pre>

### 位置10364104｜random｜z=0.100871

上下文10129，目标offset=919，目标token="."；原文档未知。

包含目标的模型可见前文：

<pre> some of them were just humorous in a good way. personally i prefer when writers don&#x27;t make their wordplay etc. so obvious (all-capsing it, using slashes or parenthesis to show the wordplay, etc..), but i can understand not wanting people to read over and miss them. the lines were great when i break them down individually (which is usually not the case), but when i look at the whole thing, it feels like you had all this excitement, but couldn&#x27;t keep it under control.. the rust on your pen is pretty visible, but i know it wont take long for you to shake that off..

    vote- CK, had the more solid and consistent piece in this one..
Thread Status:
Not open for further replies.

Share This Page

Users Viewing Thread (Users: 0, Guests: 0)&lt;|im_end|&gt;


Genetic and Rare Diseases Information Center (GARD)

Print friendly version


Other Names for this Disease
  • LAM
  • Lymphangio-myomatosis


What is lymphangioleiomyomatosis (LAM)?

How is lymphangioleiomyomatosis (LAM) treated?

What is lymphangioleiomyomatosis (LAM)?

Lymphangioleiomyomatosis (lim-FAN-je-o-LI-o-MI-o-ma-TO-sis), or LAM, is a rare lung disease that mostly affects women in their mid-forties. In LAM, an unusual type of cell begins to grow out of control throughout the body, including in the lungs, lymph nodes and vessels, and kidneys. Over time, these LAM cells form cysts and clusters of cells, which grow throughout the lungs and slowly block the airways. They also destroy the normal lung tissue and replace it with cysts. As a result, air cannot move freely in and out of the lungs, and the lungs cannot supply enough oxygen to the body’s other organs.[1]

More than 1 out of every 3 people with LAM also develops growths called angiomyolipomas, or AMLs, in their kidneys. People with LAM also may develop:[1]
  • Growths in other organs, including the liver and brain
  • Large tumors on their lymph nodes

  • There are two forms of LAM:[1]
  • Sporadic LAM, which occurs for unknown reasons
  • LAM that occurs in people with a rare inherited disease called tuberous sclerosis complex. This is often a milder form.
  • Last updated: 7/16/2013

    How is lymphangioleiomyomatosis (LAM) treated?

    While there is currently no cure for LAM, research has led to major progress in the treatment of symptoms, and diagnosing and understanding LAM. There are a number of treatments that may relieve symptoms or prevent complications from the disease. Treatments vary from patient to patient, depending on the severity of the disease. No all patients have the same response to treatment.[2][3]

  • Medicines (e.g., diuretics, hormone therapy, bronchodilators that relax the muscles around the airways)
  • Oxygen therapy - as lung capacity declines, supplemental or full-time oxygen therapy may become necessary
  • Sirolimus therapy - Rapamycin (sirolimus) blocks the pathway that is affected in LAM cells, which helps stop their uncontrolled growth. The use of sirolimus therapy may be considered in patients with moderate to severe LAM, or those with progressive disease.
  • Procedures to remove air or fluid from the chest or abdominal cavities and prevent it from building up again
  • Procedures to remove angiomyolipoma (AML), or benign kidney tumors
  • Lung transplantation - a procedure to replace one or both lungs, this should be considered as a last resort due to the risk of serious adverse reactions, including major bleeding, pneumonia, pulmonary edema, long-term infections, and possibly painful scarring.
  • Since LAM occurs almost exclusively in women of reproductive age, researchers believe the hormone estrogen might be involved in the abnormal muscle cell growth that characterizes the disease. Although there is no direct evidence that there is a relationship between estrogen and LAM, the treatment of LAM has focused on reducing the production or effects of estrogen. This could include estrogen or other hormone suppressing drugs. Additionally, doctors believe pregnancy may accelerate the progression of LAM.</pre>

右文（仅阅读辅助）：

<pre> Women with LAM are urged to speak with a health care professional before getting pregnant.[3]

    Last updated: 7/16/2013

    1. What is LAM?. National Heart Lung and Blood Institute (NHLBI). 2006; Accessed 2/13/2008.
    2. How Is LAM</pre>

## Feature 8094，h_V=1

### 位置2076012｜high_activation｜z=0.2053847

上下文2028，目标offset=975，目标token=" tab"；原文档未知。

包含目标的模型可见前文：

<pre>death to america&quot; is being chanted. ambassador rice has just taken his cues from the pre

. they are even tweeting like us. flattery will get you everywhere with the obama administration. the white house was so charmed that they threw egyptian hosnimubarak, an ally who provided us with intelience and in a region smoulder with american hatred under the bus. we didn&#x27;t know who would replace them. the muslim brotherhood wear suits and they look pretty good 18 months later, the middle east is on fire. our flag is burning in 20 countries. why do i feel like i had seen this movie before? american embassies on fire and american flags desecrate americans kill chants in 20 nations of death to america? didn&#x27;t i see this movie during the carter administration? are we that gullible? are we that weak? it wasn&#x27;t two months ago that hilary clinton talked about obama forgives one billion of the billions that egypt owes us. are we so so weak that the president of egypt who of ared two billion dollars. two billion of our taxpayers dollars and takes him two days to condemn the murder of an american ambassador and three other officials? are we that weak to ignore four assaults in benghazi in the last sev

&quot; columnist go head to head over hate toward president obama. charles will be zero if the republic party is missing anything it&#x27;s sort of this war on women. &gt;&gt; war on women? sandra fluke? she is 30 for god&#x27;s sake. just shut up for a second, okay? &gt;&gt; dennis miller man oman over the president. &gt;&gt; go factor, go factor. &gt;&gt; caution, you where to enter the no spin zone from massachusetts. the factor begins right now. ♪ ♪ &gt;&gt; bill: hi, i&#x27;m bill o&#x27;reilly, reporting tonight from washington, more americans murdered by militant muslims. that is the subject of this evening&#x27;s talking points memo. right off the bat offended the far left. they don&#x27;t want the facts reported about the islam i islamic jihad the followers of allah who kill in the name of their religion. that&#x27;s tough. my job is to till the truth. in libya, 52-year-old christopher stevens, the american ambassador to that country was murdered last night along with three other american citizens. fox news has obtained information that those killings were apparently planned. not a spontaneous demonstration. but in egypt the situation was very

of 9/11? paul ryan slamming the obama administration over its response. &gt;&gt; i disagree with the original statements that the embassy put out, that the administration put out in cairo, sympathizing with the people who are storming the embassy. we should stand up for our values values and free speech rights. i think that statement was wrong. &gt;&gt; greta: see much more of our interview with congressman ryan. is president obama more worried about winning the election or fighting off terrorists? here&#x27;s what rush limbaugh thinks. &gt;&gt; the obama camp, the campaign, the white house and the media all condemned romney before they condemned the attacks. obama thought it more worthwhile to hit romney for what he was doing than the terrorrives for what they did. &gt;&gt; greta: you hear much more from rush limbaugh, straight ahead. but first, you are looking live at the u.s. embass necairo, egypt. it is 4:00 a.m., protesters are back outside, our embassy and the protests are turning violent. all night, we are going to be monitoring the live pictures from cairo and sarah palin, blasting president obama over the


on the big show. would you rather have dinner with president obama or mitt romney? a shocking new poll has the shocking answer that will shock you. plus egyptian easy law mists storm our embassy and tear down our flag because they are angry about a movie. take note, michael bay, enough with the transformers crap. and should the seal who wrote the book about the raid about bin laden face prosecution? some say no, but others say yes, as long as they don&#x27;t have to be the ones that bring him in. &gt;&gt; will we have a better show tonight? last night was lack luster. gyre last night was -- &gt;&gt; last night was my fault. i ruined the whole thing. i feel bad. i wish you hadn&#x27;t brought it up and let&#x27;s move on. lean forward, greg. &gt;&gt; you say that a lot, often in the park. go away. &gt;&gt;&gt; let&#x27;s welcome our guest. she is hotter than a jalapeno covered with magma and tab</pre>

右文（仅阅读辅助）：

<pre>asco. she is the director of the law fair project ssments her latest book is called &quot;law fair, the war against free speech.&quot; why is she against free speech? we will have to ask her. and fresh off a win at</pre>

### 位置2547176｜random｜z=0.02642966

上下文2489，目标offset=457，目标token="ton"；原文档未知。

包含目标的模型可见前文：

<pre>I used to hate Cadsuane, too, especially the way she uses her legendary status to bully the other AS. But on my last rearead before TGS I didn&#x27;t hate her, and this time I found this chapter funny.

And now there was Semirhage, continuing to defy her. Cadsuane itched to go in and confront the woman, but Merise had asked the very questions Cadsuane would have, and she had failed. How long would Cadsuane&#x27;s image remain intact if she proved herself as impotent as the others? [...]
Again, she was struck by the similarities between herself and Semirhage - and again, those similarities made her insides itch. [...]
They weren&#x27;t deferential, but they did treat Semirhage with a measure of respect. How could they not? She was a legend. One did not enter the presence of such a creature - one of the most evil beings ever to live - and not feel at least a measure of awe.
Measure of awe...
&quot;That&#x27;s our mistake,&quot; Cadsuane whispered. [...]
How would Cadsuane break herself? The solution was easy, now that it occurred to her. [...]
She didn&#x27;t fight back. Cadsuane wouldn&#x27;t have either; that would only hurt her image. Semirhage&#x27;s power as a captive came from the fear and respect that the Aes Sedai gave her. Cadsuane needed to change that.

TGS ch. 17

Maybe Cadsuane has to be like that to figure out how to break someone who resembles her.

&quot;Berelain, I don&#x27;t know what else I can do to guarantee Mayene for you, but I will write out any -&quot; Colors swirled so strongly in his head that his tongue froze.

ACoS ch. 18

I wondered about this, too. It might be ta&#x27;veren pull making Rand send Berelain to Perrin. That way the colors make sense, and after this he does change his mind about sending her home and offers her a different job (which turns out to be with Perrin&#x27;s party).
Tricia Irish
148. Tekton</pre>

右文（仅阅读辅助）：

<pre>ica


Exactly! Now, having NO background info, is barging in and bullying Rand and being rude to everyone the best way to take the measure of someone? Does she win his trust, so he will talk about his mental state and his plans to her?
uh, no.

I know, I&#x27;s not who she is. Her tactics are not effective with Rand and yet she continues to employ</pre>

### 位置5771052｜high_activation｜z=0.2131972

上下文5640，目标offset=609，目标token=" tab"；原文档未知。

包含目标的模型可见前文：

<pre>8 touch devices












Sources: The Seattle Times, CNET

Comments     Threshold


By RU482 on 12/5/2012 2:16:26 PM , Rating: 2
Surface RT is great in theory, but I find it to be laggy, and kinda clunky when compared to running win8 on an i5 system.

And damnit it won&#x27;t run go-to-meeting, so I can&#x27;t replace my laptop with it anytime soon.

Because iOS had tons of apps available on day 1.

By their logic nobody should buy a Mac.




By Argon18 on 12/5/12, Rating: 0
the number of apps in a desktop app store is meaningless

How about this them
Bluestacks may bring 700,000 Android apps to Windows RT

So you buy a windows machine to run Android apps??

That does not make any kind of sense.

By Roffles on 12/5/2012 3:16:35 PM , Rating: 2
I don&#x27;t understand how RT is great in theory either. I mean, it&#x27;s a gimped ARM operating system to run on gimped ARM hardware. It can only be targeted at farty consumers because it lacks the power to do anything truly productive. For me at least, I&#x27;m not going to choose battery life over raw computing power and functionality. I feel the same way about all things ARM, specifically Android and iOS tablets. I understand ARM on a phone or packed inside a television because it&#x27;s 100% functional for its intended purpose, but for a computer, it seems like wasted money.









By othercents on 12/5/2012 3:16:43 PM , Rating: 2
I agree that Windows RT is great in theory. I don&#x27;t think the ARM hardware has caught up enough to use RT as a desktop/laptop replacement. However the Surface Pro and other i3/i5/i7 processors can be if you ignore price and other available laptop options on the market. (I&#x27;m not sure if I would leave the Surface Pro running like I do my other Tablets.)

At some point though Windows RT should be able to be a laptop replacement for home computers and for certain individuals this is an option now. Until then here&#x27;s hoping that the Surface Pro is worth the extra expense over a i5 laptop.

By Pirks on 12/5/12, Rating: 0
&lt;|im_end|&gt;











Comments     Threshold


RE: Whoa
By 16nm on 9/24/2007 4:45:53 PM , Rating: 0
village of Carancas, near Lake Titicaca

How about sacrificing the 5 year old who named Lake Titicaca? This is like one of those names used in tab</pre>

右文（仅阅读辅助）：

<pre>loids covering alien abductions, crop circles, three headed babies, etc. LOL

RE: Whoa
By thartist on 9/24/2007 9:57:07 PM , Rating: 2
I won&#x27;t be angry at you, just tell you that the name comes from native people&#x27;s culture, and it resembles pronunciation of their</pre>

### 位置6383184｜random｜z=0.006715308

上下文6238，目标offset=922，目标token=" to"；原文档未知。

包含目标的模型可见前文：

<pre> is a big one. They&#x27;re waiting for you. So how does it feel to be back?

SECRETARY CLINTON: Well, first of all, I want to thank you for hosting this. And I want to thank, of course, our embassy and the American University of Central Asia, and the new chancellor. And I particularly want to thank public television and public broadcasting here in Kyrgyzstan. I am a big supporter of public broadcasting, and I appreciate this opportunity. (Applause.)

And it&#x27;s very exciting to be back. As you say, I helped to inaugurate the university back in 1997. It&#x27;s wonderful to return. The United States is proud to continue to support that university, and support many other important programs in Kyrgyzstan. And there could not be a better time than right now to be here, as you are forming a new government.

The constitutional referendum and the parliamentary elections were widely appreciated around the world. In fact, many people said Kyrgyzstan, in the midst of all of the problems, was able to do elections better than many other countries in other parts of the world. So I think that the people ought to be very proud of that. And the United States will continue to support the government and people. We are very committed to the future of Kyrgyzstan. So it&#x27;s wonderful to be back. (Applause.)

MODERATOR 2: Thanks so much. And I guess everybody is interested in both your key message to Kyrgyzstan and you have already met with the President of Kyrgyzstan, Roza Otunbayeva. What did you talk about?

SECRETARY CLINTON: Well, we had an excellent meeting. And we talked about many different things. We talked about the formation of the new government, which, of course, I wish well when that is finally accomplished; the challenges facing Kyrgyzstan, in terms of economic development and opportunity and social and human development and human rights; security and stability. We really talked about a broad range of both challenges and opportunities that are facing your country.

And I think it&#x27;s fair to say that the next few years will be critically important to your future, because you are primarily students, and you are going to be able to make a contribution, not only to the improvement of your own lives, but to the improvement of your country.

So, I want to hear firsthand from you what you see happening in Kyrgyzstan, what more the United States can or should do to help to bring about a better future for the people of this country. And I enjoyed greatly my conversation with the president, because there is a great deal of hope and optimism that we have about the future. But even a friend and a partner like the United States wants to be, can only do so much. The hard work is really up to the people. And we want to support that.

MODERATOR 1: Thank you. Now, I think some of us have some questions, and so we will give the floor to students.

QUESTION: Madam Secretary, was it difficult to figure out U.S. Administration&#x27;s response to April events which ousted President Kurmanbek Bakiyev?

SECRETARY CLINTON: Well, it&#x27;s always difficult when violence happens, and when government changes occur. But we were ready and willing to help immediately with the humanitarian issue. The results of the violence, the problems that occurred not only in April, but then again in June, where people were killed, where families were displaced, where housing was destroyed, we have provided direct aid.

And we also were quite encouraged when the interim government pledged that it would immediately carry out elections. You don&#x27;t see that everywhere. Lots of times, if there is a change in the government, especially if it&#x27;s precipitated by or accompanied by violence, you don&#x27;t see a commitment to early elections. And I remember very well lots of people around the world were saying, &quot;They can&#x27;t have that constitutional referendum in the middle of all of the problems that are going on,&quot; and the president and the people around her said, &quot;No, we have to do it, because we want to prove that we didn&#x27;t do it for ourselves, we wanted to turn it over to the democratic process.&quot; So, we were ready with help, and we were pleased at the way that -- the reaction from the government and the people had proceeded, and now we stand ready to help the new government.

And there are a couple of very important issues that I think have to</pre>

右文（仅阅读辅助）：

<pre> be addressed: continuing assistance for people in need, particularly people who have suffered because of the changes over the last month, but really trying to help with greater economic opportunity for all of the people; working on tensions between different groups in society, how do you overcome the suspicion that, unfortunately, exists; bringing to justice those who committed crimes, but doing it in a way that follows the law and the</pre>

### 位置8172355｜random｜z=0.1428847

上下文7987，目标offset=713，目标token=" Thomas"；原文档未知。

包含目标的模型可见前文：

<pre> money to hire police to stop it. This showed how weak the system was.

Thomas Jefferson Quote

&quot;Tree of liberty must be refreshed from time to time with blood of Patriots and Tyrants.&quot;

Constitutional Convention

wanted it to be in secret - 35 delegates were to represent the 13 colonies. Jefferson and John Adams were abroad, Samuel Adams couldn&#x27;t attend, Patrick Henry &quot;smelled a rat&quot; and didn&#x27;t want a part of it. James Madison, Alexander Hamalton, George Washington, Ben Franklin (81 - liked to drink and got escorted everywhere) all went. The task was to revise things out of the confederation but they didn&#x27;t know until the end that they were going to re write all the rules.

Virginia Plan

Virginia wanted a bicameral legislature (2 houses). Representation was by population. The state legislature will be nominated.
-Members of the upper house chosen by lower house
-Members of lower house chosen by population
-The congress would choose president and appoint judges
-A council could veto acts of congress

New Jersey Plan

small states preferred this, unicameral, and one representative per state (equal representation)

The Great Compromise

2 houses (bicameral) - lower house elected by people, 65 representatives - upper house (senate) was elected by the state legislatures (later they got rid of it and now it is by the people)


separate powers - senate are moderate and keeps the house in check.
-Representatives from the house only represent a part of a state
-Senate represents the whole state


if you have a slave, then they are heavily taxed - some states were free states, 3/5 compromise = each slave would count for 3/5
-Congress regulating commerce - 2/3 votes

Slave Trade

they postponed it for 20 years. if a slave goes to a free state, they must go back to their old state.

President&#x27;s term

they had unlimited 4 year terms
- there was some debate between one 6 year term and 2 4 year terms

President&#x27;s election

Big vs. small states - E.C.
# E.C. = # of Representatives (pop) + # of Senate (2 per state)
-small states get 3/538 vs. 200,000/320,000,000. They get more attention so thats why there was no direct election

Describe Roche

He wrote a book about the motives of the Framers.
Roche&#x27;s thesis was that the constitutional convention should be practical/compromise and people should sell the document back home.
- Congress was a compromise (H vs. S)
- E.C. was a compromise (small happy because of the minimum of 3 states/people happy because they vote/big states happy because they get a lot of say/house happy because they get to choose the president in case of tie/senate gets to choose the VP in case of tie

Describe Beard

He wrote a book about the motives of the Framers. Beard&#x27;s thesis was that the constitutional convention was a conspiracy of the rich, wealthy people showed up to design the system to favor elites.
-slave owners show up but don&#x27;t address slavery
-the elites prick elites in the senate
-E.C. the 9 people have all the powers and are elected by president and the senate approves
-Radicals were absent, Samuel Adams, John Adams, Thomas</pre>

右文（仅阅读辅助）：

<pre> Jefferson, Patrick Henry.

What are reasons for the Constitutional Conventions success?

-it was secret
-people were homogenous, same ideas - the trouble makers weren&#x27;t there
-most were part of the continental congress, they were thinking about a weak government

Ratification and Constitution

they were supposed to get 13/13, but they only got 9/13, so</pre>

### 位置8247659｜high_activation｜z=0.2053847

上下文8061，目标offset=339，目标token=" tab"；原文档未知。

包含目标的模型可见前文：

<pre> appears to me as a man with a larger than life ego, a man so consumed with power he sees nothing else, a vain individual eager to live out his dream as a great historical figure or something that i can not think of right now. Violence MUST never be condorned, but democracy needs to be upheld everywhere.
    Gbagbo has taken his country on a perilous journey and put the lives of his countrymen in harms way without a care. and when the sound of gunfire came close to home; he twice tried to negotiate a way out. It is as well the negotiations failed. God is not asleep; HE is wide awake.

  • Comment number 11.

    Regardless of what he may have done in political office dragging him out and beating him to death must be condemned by the western world.
    If the opposition wants to retain its moral superiority it should also denounce any plans to kill Gbagbo, that would be the actions of a developed democratic leadership in my opinion.

  • Comment number 12.

    I fully agree with Will. You cannot set aside the law of a sovereign country. If the international community does not like the Constitutional Council, they must by due process prove them wrong. They must demonstrate to the world public by publsihing all data and statements that they have a case.

    There has been a totally arrogant lack of information. The world media carry a heavy responsibility, too. Why is it that the BBC and CNN and others cannot grace us with the mere numbers? With accounts and arguments of the official spokesmen of both camps? By the views of international lawyers?

    All we have had is a load of tab</pre>

右文（仅阅读辅助）：

<pre>loid BS with no substance. It has been left to bloggers to argue the cases of both camps. Is this democracy? Had the world been properly informed, there migh not have been any need of violence. But maybe the outcome of such a &quot;public trial&quot; of evidence would have produced a different outcome from that desired by the capital interests BEHIND the media.



Sign in

BBC navigation

</pre>

### 位置8443150｜random｜z=0.0188613

上下文8252，目标offset=415，目标token="0"；原文档未知。

包含目标的模型可见前文：

<pre>/TheSeven)
10:39:15 Nick TheSeven|Mobile is now known as The_Seven (~theseven@rockbox/developer/TheSeven)
10:39:16 Nick The_Seven is now known as TheSeven|Mobile (~theseven@rockbox/developer/TheSeven)
10:39:56TheSeven|Mobilehaving a smooth volume bar would be really nice, and I don&#x27;t get why rockbox doesn&#x27;t support that
10:41:01TheSeven|Mobilehow does the progress indicator work internally? couldn&#x27;t we implement the volume indicator in the same way?
10:41:17S_a_i_n_tI&#x27;m actually adding a few more bitmaps to the volume strip now ;) (to smooth it out a bit more), but I only have ~20KB left in the skin buffer lol
10:41:47TheSeven|Mobilehaving more than 2 strips for that is a waste of space
10:42:09S_a_i_n_tI&#x27;d really like to see &quot;just one bitmap for volume&quot;, exactly like the playbar also...
10:42:31 Join robin0800 [0] (
10:42:43TheSeven|Mobileare there any objections against just implementing that?
10:43:02S_a_i_n_tI&#x27;d reclaim abot ~90KB from the skin buffer if I could do volume the same was as the playbar.
10:43:24S_a_i_n_tIf you can find a way to do it, I doubt there would be.
10:43:29TheSeven|MobileI&#x27;m not familiar with the WPS code at all, but I can&#x27;t see anything holding that back
10:43:40S_a_i_n_tYou&#x27;d still have to be able to use .bmp strips though
10</pre>

右文（仅阅读辅助）：

<pre>:43:50S_a_i_n_tSo you don;t break almost ALL the themes lol
10:43:57 Join Zagor [0] (~bjst@rockbox/developer/Zagor)
10:43:58TheSeven|Mobileyes, of course, this would need to be an alternative
10:44:</pre>

### 位置10181520｜random｜z=0.06280661

上下文9951，目标offset=489，目标token=" true"；原文档未知。

包含目标的模型可见前文：

<pre> so I know what green looks like to me. I’ve felt pain, so I know what pain feels like to me.

Objection 3: J.L. Mackie argued that moral properties must be strange in the sense of being intrinsically motivating (69). However, Tännsjö disagrees. “Perhaps it is true that most people do as a matter of fact to feel somewhat inclined to produce a certain event, if it is perceived by them to be good… But I find it obvious that there can be people who pay little attention or none at all to the value of the consequences of their actions. The notion of value as I see it does not ‘logically’ (whatever that could mean in this context) provide us with motives” (69-70).

It must be indefeasible.

If an observation is indefeasible, then it is not “defeated” by possible objections. If an observation is not caused by the appropriate situation, then it is defeated. For example, I might believe that a cow is in the distance when it is really a cardboard cutout of a cow. This means that I didn’t really observe the cow and my observation was defeasible. The question is, can moral observations be indefeasible (undefeated and caused by the appropriate moral properties)?

Why would anyone think that moral observations are always defeasible?

One, it could be argued that moral observations can’t be shown to be defeated, and an observation can’t be indefeasible if there is no possibility of being proven to be defeasible. However, Tännsjö argues that moral observations are defeasible. If I think I see an elk but I find out it was a deer, then my observation has been defeated, and in a similar fashion I might think someone’s behavior indicates that she is feeling something intrinsically bad when I later find out she was actually feeling ecstasy (72).

Two, we are almost always biased about our moral beliefs (74). For example, the person who is profiting by harming others will want to rationalize their behavior so that they can continue profiting from it. Tännsjö admits that moral observations might be rarely impartial and indefeasible, but that doesn’t mean they always are. If it is in someone’s advantage to be moral, then they would probably hold a true</pre>

右文（仅阅读辅助）：

<pre> moral belief. For example, suppose that torture is always wrong. Someone about to be tortured would be likely to correctly think that the act of torture about to be undertaken is wrong. This belief would not be undefeated by an impartial perspective.

Observation must be its own best explanation.

According to Gilbert Harman, an observation must be its own best explanation in order to confirm or disconfirm a theory,</pre>

## Feature 8192，h_V=4

### 位置957759｜high_activation｜z=0.2098735

上下文936，目标offset=48，目标token="]\n\n"；原文档未知。

包含目标的模型可见前文：

<pre>erry England&quot; reflects historical aspects of rural English folklore that were lost during industrialization.[3] Favourable perceptions of Merry England reveal a nostalgia for aspects of an earlier society that are missing in modern times.

Origins and themes[edit]

</pre>

右文（仅阅读辅助）：

<pre>O the Roast Beef of Old England (The Gate of Calais) by William Hogarth contrasts English plenty with French and Jacobite Highlander misery.

The concept of a Merry England may have originated in the Middle Ages, describing a utopian state of life that peasants aspired to lead (see Cockaigne). Peasant revolts, such as those led by Wat Tyler and Jack Straw invoked</pre>

### 位置2197692｜random｜z=0.04288129

上下文2147，目标offset=895，目标token=")\n\n"；原文档未知。

包含目标的模型可见前文：

<pre> in around the edges
of my autumn stillness
to my greed in keeping from the Earth
her children
for my own pleasure, which
fades and crumbles still.


Diagloging Science and Religion

What I really want in pursuing a science &amp; religion dialogue, is to show everyone how incredibly wonderful the universe is, and then say &quot;And now, you decide what this all means to you,&quot; without any need for me to compel you to agree with my meaning, or for you to feel compelled to make me agree with your meaning.

When the &quot;dialogue&quot; is just a back and forth about details (Did this evolve or was it created? Is this a soul or chemistry? Did it come from nothing or did it come from God? Was this designed or self-assembled?), then it is never ending and really we will never find agreement.  This is obvious - we look at the same cells, the same fossils, the same universe and you say &quot;God&quot; and I say &quot;nature.&quot;  It&#x27;s not that this exchange about details is worthless, but it must be kept in mind that we&#x27;ll probably never find agreement in bickering over the details.

If instead, we could somehow let the world be as it is, as best we know it, then we could save ourselves from fighting over minutia, and we could learn from each other.  Of course, maybe this is impossible, because if we can&#x27;t agree that science really is the best way to know what the natural world is like, then it&#x27;s hard to talk about other things.  But maybe we can just &quot;agree to disagree&quot; on the details.

If we can, I could tell you of the wonder of our interconnectedness, and you could tell me of our responsibility to nurture each other.  I could remind you of the intricate path the protons in your body followed to be you for this time, and you could urge me to see how special I am, how loved and endowed with purpose.  I may not agree with you, but at least we could share the meanings we both take from what we see.

This is the dialogue that I wish we could have.  Me showing you the reality that surrounds us, and you showing me what you think it all means.  But it does require, perhaps, hat we both let go of our need to make the other agree with the meaning we take from that reality.  Reality should be more objective and universal, but there is uncertainty, and we all see differently.  And for meaning, this goes even more.  We can&#x27;t insist on agreement over the meaning we see.  We all must choose what seems right to us.

This probably won&#x27;t happen easily.  It requires recognizing that science is the best tool we have for understanding nature, and also recognizing that meaning is much more personal.  It seems likely that it&#x27;s not really possible, at least for most of those on the religious side, who feel threatened by anything they perceive as contradicting their scriptures (and yes, also for some on the science side who see religion as an enemy).  But maybe it&#x27;s worth a try?

Autumn (poem)

Autumn  10/23/10

It&#x27;s autumn now,
    the redbud is bare
    except for seed pods hanging on
    from spring.

The maples have turned,
    the matched pair around the corner
    a vibrant fire-red,
    a familiar and beloved sight for me,
    a signpost of my year.

The oaks are hesitant,
    holding on to their crowns of green,
    thinking maybe the winter will be hard?
    and wanting to store up a last bit of energy.

Soon though, they&#x27;ll brown too, and drop,
    and then we&#x27;ll have our fill of raking,
    and the compost pile too will fill.

Still we&#x27;ll have to bag a lot
    and send it off to land-fill.
    It makes me sad, but I console myself
    at least it&#x27;s leaves,

Not some manufactured thing
    that will sit for ages, like a willful child
    refusing to go back to the earth,
    where of course its parts all came from.

Still, they cycle on,
    slow or fast,
    stubbornly or glad,

Finally with restfulness in mind.

Konza 3 (poem)

</pre>

右文（仅阅读辅助）：

<pre>Konza 3 (8/22/10)

You have left the trail,

Is less motivating,
I think,
than the near-solid wall
of poison ivy at my feet,
and I respect
the work of my kind to protect
that which is fragile and endangered
but I respect far greater nature,
whose own defense
is formidable indeed.&lt;|im_end|&gt;Take the tour ×

</pre>

### 位置6081864｜random｜z=0.01797895

上下文5944，目标offset=397，目标token="\n\n"；原文档未知。

包含目标的模型可见前文：

<pre> are bound to make offseason changes, and with Wall in the lineup, they can start to help their fans forget this gruesome season. Wall would help them squeeze out more wins. Would they break .500? Probably not, but it takes time to rebuild a franchise.

A potential downside to Wall as a Net is the halt on building for the future. Obviously, the Nets are in trouble, and Wall will take a lot of the offensive load for the team. The question that people aren&#x27;t considering is whether or not Wall&#x27;s takeover of the team is good in the long run. The Nets offense is balanced. It&#x27;s not good, but it&#x27;s balanced. Maybe their season will end with eleven wins, but it doesn&#x27;t mean that Courtney Lee, Chris Douglas-Roberts, and *Brook Lopez* won&#x27;t be good NBA players in the future. If Wall could understand his role in a balanced offense and not as a superstar, however, it could definitely work out.

Nevertheless, the sense of intimidation from this 6&#x27;4&#x27;&#x27; point guard who blocks three point shots to end games will be in the minds of even the veterans he will be matched up against, and this player could have a big impact on the NBA&lt;|im_end|&gt;Indianapolis Colts in Free Fall: 5 QBs Who Could Come To Indy&#x27;s Rescue

By (Correspondent) on September 28, 2011

1,206 reads


1 of 7
Joe Robbins/Getty Images

All is not well in Indianapolis. Through three games, the Peyton Manning-less Colts are winless, their starting quarterback belongs in retirement and speculation abounds that Jeff George could be the franchise savior. Did I mention things are not looking better in Indianapolis? 

In addition to the aforementioned George, here are five QBs who could come to Indy&#x27;s rescue...for the right price. 

Option No. 5: Mike Kafka

Chris Trotman/Getty Images

</pre>

右文（仅阅读辅助）：

<pre>This may sound crazy, but hear me out.

The Eagles have a thing for stockpiling draft picks and developing young QBs. The Colts need a young QB who understands the NFL game and can develop behind an increasingly frail Peyton Manning. It may not be a match made in heaven, but marriages have been made to work with less. 

At this point in his career, it would be</pre>

### 位置6152525｜high_activation｜z=0.217686

上下文6013，目标offset=453，目标token="]\n\n"；原文档未知。

包含目标的模型可见前文：

<pre>290.4
DiseasesDB 8393
MedlinePlus 000746
eMedicine med/3150 neuro/227
MeSH D015161

Vascular dementia or &quot;multi-infarct dementia&quot; is dementia caused by problems in the supply of blood to the brain, typically by a series of minor strokes. Vascular dementia is the second most common form of dementia after Alzheimer&#x27;s disease (AD) in older adults.[1][2] Multi-infarct dementia (MID) is thought to be an irreversible form of dementia, and its onset is caused by a number of small strokes or, sometimes, one large stroke preceded or followed by other smaller strokes.[3] The term refers to a group of syndromes caused by different mechanisms all resulting in vascular lesions in the brain. Early detection and accurate diagnosis are important, as vascular dementia is at least partially preventable.

The main subtypes of this disease are: mild cognitive impairment, multi-infarct dementia, vascular dementia due to a strategic single infarct (affecting the thalamus, the anterior cerebral artery, the parietal lobes or the cingulate gyrus), vascular dementia due to hemorrhagic lesions, and mixed Alzheimer&#x27;s and vascular dementia.

Vascular lesions can be the result of diffuse cerebrovascular disease, such as small vessel disease, or focal lesions; usually both. Mixed dementia is diagnosed when patients have evidence of AD and cerebrovascular disease, either clinically or based on neuroimaging evidence of ischemic lesions. In fact vascular dementia and Alzheimer&#x27;s disease often coexist, especially in older patients with dementia.

MID is sometimes triggered by cerebral amyloid angiopathy, which involves accumulation of beta amyloid plaques in the walls of the cerebral arteries, leading to breakdown and rupture of the vessels. Since amyloid plaques are a characteristic feature of AD, vascular dementia may occur as a side effect of it. However, cerebral amyloid angiopathy can also appear in people with no prior dementia condition and a small amount of beta amyloid plaques are often present in cognitively normal older persons.

Signs and symptoms[edit]

</pre>

右文（仅阅读辅助）：

<pre>Multi-infarct dementia and Alzheimer&#x27;s disease, despite the fact that the two organic disorders have different causes, can be almost impossible to tell apart clinically and are often misdiagnosed.[4] Patients suffering from vascular dementia present with cognitive impairment, acutely or subacutely, after an acute cerebrovascular event. After the onset a stepwise progression is typical.

In small vessel disease the</pre>

### 位置6201512｜random｜z=0.08047895

上下文6061，目标offset=349，目标token="\n\n"；原文档未知。

包含目标的模型可见前文：

<pre> objects, for example. But getting a feel for how word order affects emphasis is something that can really only come through practice, except that things at the front of the sentence are generally emphasized more. For instance, the first one is just &quot;I&#x27;m going to Tokyo&quot;, but the second one might seem more like, &quot;Tokyo? As it happens, I&#x27;m going there.&quot;

share|improve this answer
add comment

The direct object marker を always comes straight after the direct object, not before it. You can have a place as the direct object with を (町を歩く) but here the direct object is still the chair, not the conference room. The sentence is basically このいすを運んでください, but with some extra information placed in the middle (会議室に).

To my ears, the book answer sounds more correct. Your sentence sounds correct, but sort of stiff. Your sentence has the を in the correct place, but you don&#x27;t necessarily need for the verb to follow directly. You can put some extra information between を and the verb:

寿司を笑顔で食べる (すしをえがおでたべる) Eat sushi with a happy face.

This page explains particles better than I can:

share|improve this answer
thank you, this is very helpful as well :) –  Colin Wheeler Jun 9 &#x27;11 at 0:27
+1 for &quot;object marker&quot; which should be mentioned in any accepted answer about the wo particle... –  repecmps Jun 9 &#x27;11 at 2:00
add comment

Your Answer


&lt;|im_end|&gt;Tuesday, July 22, 2008

Starting Somewhere

</pre>

右文（仅阅读辅助）：

<pre>So I answered the last question from my blog by sketching a page before bed last night. I&#x27;m going to draw at least a page a day. It was really rough and almost painful to look at but I figure the solution to bad drawing is more drawing.

I&#x27;m also determined to alternate nights between playing WoW and working on a creative project, whether it be a webcomic, a graphic novel</pre>

### 位置6282430｜high_activation｜z=0.2196391

上下文6140，目标offset=447，目标token="\n\n"；原文档未知。

包含目标的模型可见前文：

<pre>secta
    Order: Odonata
    Suborder: Epiprocta
    Infraorder: Anisoptera
    Selys, 1800


    A dragonfly is an insect belonging to the order Odonata, the suborder Epiprocta or, in the strict sense, the infraorder Anisoptera. It is characterized by large multifaceted eyes, two pairs of strong transparent wings, and an elongated body. Dragonflies are similar to damselflies, but the adults can be differentiated by the fact that the wings of most dragonflies are held away from, and perpendicular to, the body when at rest. Dragonflies possess six legs (like any other insect), but most of them cannot walk well.

    Dragonflies are valuable predators that eat mosquitoes, and other small insects like flies, bees, ants, and very rarely butterflies. They are usually found around lakes, ponds, streams and wetlands because their larvae, known as &quot;nymphs&quot;, are aquatic.


    Anisoptera comes from the Greek an meaning not, iso meaning equal, and ptera meaning wings. Their hind wings are broader than their fore wings.

    Classification (Anisozygoptera)Edit

    Formerly, the Anisoptera were given suborder rank beside the &quot;ancient dragonflies&quot; (Anisozygoptera) which were believed to contain the two living species of the genus Epiophlebia and numerous fossil ones. More recently it turned out that the &quot;anisozygopterans&quot; form a paraphyletic assemblage of morphologically primitive relatives of the Anisoptera. Thus, the Anisoptera (true dragonflies) are reduced to an infraorder in the new suborder Epiprocta (dragonflies in general). The artificial grouping Anisozygoptera is disbanded, its members being largely recognized as extinct offshoots at various stages of dragonfly evolution. The two living species formerly placed there — the Asian relict dragonflies — form the infraorder Epiophlebioptera alongside the Anisoptera.

    Dragonflies and damselfliesEdit

</pre>

右文（仅阅读辅助）：

<pre>    File:Sydney flatwing04.jpg
    Unusual for a damselfly, the Sydney Flatwing hold their wings perpendicular to their body

    Damselflies (suborder Zygoptera) are often confused with newly moulted dragonflies but once a dragonfly moults, it is fully grown. There are other distinctions that set them apart: most damself</pre>

### 位置8471714｜random｜z=0.05801801

上下文8280，目标offset=314，目标token="\n\n"；原文档未知。

包含目标的模型可见前文：

<pre>.physician, view1.totaltopay, view1.col4, view1.col5, view1.col6, view1.col7, view1.col8
FROM view1
WHERE (((view1.col23)=&#x27;recordid66&#x27;))

I&#x27;m also trying to get it so that col35 would be a sequential number starting from a parameter is set. ie. the user enters 122, then the records that are added would enter into col35 the number 122, then on the next record it would add 123, then next record 124, etc. Is this all possible?&lt;|im_end|&gt;Nonfiction » Philosophy » Religious philosophy

Difficulties with Hinduism: Reincarnation Conjoined with Illusion and the Gospel Solution
By Applied Apologetics
Price: $1.99 USD. Words: 2,000. Language: English. Published: December 26, 2012. Category: Nonfiction » Philosophy » Religious philosophy
The doctrines of reincarnation and illusion in Hindu thought are not possible asylums for salvation. The true God has aseity and is supreme—He has the power to offer actual redemption. If everything is an illusion, that would include the Hindu concepts of reincarnation and illusion. An Apologetics Paper.&lt;|im_end|&gt;Sydney Morning Herald Online

Home   &gt;   World News   &gt;   Article

Continental divide

</pre>

右文（仅阅读辅助）：

<pre>April 19, 2004

Printer friendly version Print this article
Email to a friend Email to a friend

They are at home but Europe&#x27;s Muslims increasingly feel like foreigners. Peter Fray reports.

Leila feels stigmatised by the French society she was born in for wanting to wear her headscarf to school. Arif can&#x27;t</pre>

### 位置9144121｜random｜z=0.02286176

上下文8937，目标offset=516，目标token="\n\n"；原文档未知。

包含目标的模型可见前文：

<pre>, because through all the trials and tribulations, they still find a way to work hard and earn their stripes. 

It&#x27;s a marvel that West has been able to be such a quality player through all of the off-court incidents that have tied him down. 

As fans, we forget that NBA players, though many of them make a lot of money, still struggle through many of the same issues that everyday people do.&lt;|im_end|&gt;Exactly 10 years, four MVP awards, two championships and one Decision ago, LeBron James made his NBA debut against the Sacramento Kings. It was Oct. 29, 2003, and nobody was sure how James, the most highly touted rookie anyone could remember, was going to handle the pressure.

Outwardly, James projected calm in advance of his first ever NBA game. Even at that early stage, LBJ had adopted a relaxed demeanor.

lebron eyes on Make A Gif

If the 18-year-old phenom had any hidden butterflies, they had to flutter around in his gut a little longer than usual that night, thanks to the demands of television.

Per Brian Windhorst of ESPN

James&#x27; first Nike commercial, depicting the pressure of his first NBA game and filmed at Arco a month earlier, is running &#x27;round the clock on TNT and ESPN. Talk shows and columnists are running amok. Some 45 minutes before the game, hundreds of fans press up to the court, straining to watch James warm up.

Another sellout crowd is rattling the building, but TNT&#x27;s early game goes into overtime, so everyone waits. James plops his 6-8, 240-pound frame on the scorer&#x27;s table and waits for the whistle to call him to the opening tip. A cameraman is a foot from him, shooting from a low angle and focusing on his face. LeBron is biting his nails.

Once the broadcast was cleared for launch, James introduced the world to a pregame ritual with which he&#x27;d forever be associated. Nail-biting time was over, and James walked to the scorer&#x27;s table to chalk up.

LeBron Chalk on Make A Gif

Notably, James didn&#x27;t toss the powder as he would in later years. Maybe he was trying to fly under the radar in his first game.

His efforts at subtlety went out the window quickly enough, though, as James drilled his first field-goal attempt just a couple of minutes into the game.

lebron bucket 1 on Make A Gif

</pre>

右文（仅阅读辅助）：

<pre>Ironically, the baseline jumper LBJ hit over the Kings&#x27; Brad Miller is precisely the kind of shot he recently phased out of his repertoire.

Long, contested twos are verboten in today&#x27;s NBA. 

When James broke the seal, ESPN&#x27;s Sean Elliott actually sounded relieved: &quot;That&#x27;s good to see because during the preseason, he wasn&#x27;t able to hit those kinds of jump</pre>

## Feature 8345，h_V=0

### 位置1583445｜high_activation｜z=0.206317

上下文1547，目标offset=515，目标token=" where"；原文档未知。

包含目标的模型可见前文：

<pre>

closed as off topic by Daniel Standage, Michael Kuhn, Konrad Rudolph, jonsca, Rory M May 4 &#x27;12 at 20:02


Browse other questions tagged or ask your own question.&lt;|im_end|&gt;It&#x27;s been a long, strange year for Seattle Mariners second baseman/outfielder Dustin Ackley

Perhaps more than any other Mariner this season (and arguably last), Ackley has left fans in the Pacific Northwest wondering what exactly to make of himand by extension the Mariners.

For those of you who may have lost track of Ackley after his promising debut two summers earlier and his sophomore slump last year, allow me to summarize his performance this season by the month:

April was rough after what had been a decent spring training.

May was so brutal that he was demoted and replaced at second base.

In June, he rebounded at Triple-A Tacoma and returned to Seattle by the end of the month.

In July, he really didn&#x27;t distinguish himself at the plate or on the field.

Then suddenly in August, Ackley became an animal, both literally and figuratively. 

Growing out a beard more reminiscent of a man in quest of the Stanley Cup than a baseball player, &quot;Wolfman Ack&quot; slowly but surely put together an impressive month, per ESPN, hitting .390 with 2 HR and 10 RBI with 10 runs scored. But perhaps even more exciting was the fact that both his OBP and slugging percentage were simply off the charts. 

Yet the funny thing is that Ackley&#x27;s metamorphosis occurred to very little fanfare, all the way at the bottom of the M&#x27;s lineup.  

Bob Levey/Getty Images
Nice glove work on Friday night!

It wasn&#x27;t until last Friday night in Houston, while all eyes were focused on rookie Taijuan Walker&#x27;s debut, that Ackley basically put on a clinic, spraying four hits for four RBI and made a nifty catch on his knees near the bullpen in right-center to cap off what would be Walker&#x27;s first win.  

Maybe it was just one night, but is this the Dustin Ackley we&#x27;ve all been waiting for? 

For the better part of two years we&#x27;ve been waiting for a sign of something but have only captured brief glimpses amidst several false starts. 

According to Ackley, this recent turnaround may come down to a simple matter of trust, as described to Ryan Divish at the Tacoma News Tribune:

&quot;I think now it’s just something where</pre>

右文（仅阅读辅助）：

<pre> I can really trust in my swing, where before I didn’t really trust it and all that,” he said. “Now it’s gotten back to how it used to feel and that’s why I’m mentally focused every at-bat and ready to hit.”

Deep down I want to believe in Ackley, but it seems only fitting that since Friday night he has once again lost the magic touch.</pre>

### 位置1583449｜high_activation｜z=0.1965514

上下文1547，目标offset=519，目标token=" trust"；原文档未知。

包含目标的模型可见前文：

<pre>

closed as off topic by Daniel Standage, Michael Kuhn, Konrad Rudolph, jonsca, Rory M May 4 &#x27;12 at 20:02


Browse other questions tagged or ask your own question.&lt;|im_end|&gt;It&#x27;s been a long, strange year for Seattle Mariners second baseman/outfielder Dustin Ackley

Perhaps more than any other Mariner this season (and arguably last), Ackley has left fans in the Pacific Northwest wondering what exactly to make of himand by extension the Mariners.

For those of you who may have lost track of Ackley after his promising debut two summers earlier and his sophomore slump last year, allow me to summarize his performance this season by the month:

April was rough after what had been a decent spring training.

May was so brutal that he was demoted and replaced at second base.

In June, he rebounded at Triple-A Tacoma and returned to Seattle by the end of the month.

In July, he really didn&#x27;t distinguish himself at the plate or on the field.

Then suddenly in August, Ackley became an animal, both literally and figuratively. 

Growing out a beard more reminiscent of a man in quest of the Stanley Cup than a baseball player, &quot;Wolfman Ack&quot; slowly but surely put together an impressive month, per ESPN, hitting .390 with 2 HR and 10 RBI with 10 runs scored. But perhaps even more exciting was the fact that both his OBP and slugging percentage were simply off the charts. 

Yet the funny thing is that Ackley&#x27;s metamorphosis occurred to very little fanfare, all the way at the bottom of the M&#x27;s lineup.  

Bob Levey/Getty Images
Nice glove work on Friday night!

It wasn&#x27;t until last Friday night in Houston, while all eyes were focused on rookie Taijuan Walker&#x27;s debut, that Ackley basically put on a clinic, spraying four hits for four RBI and made a nifty catch on his knees near the bullpen in right-center to cap off what would be Walker&#x27;s first win.  

Maybe it was just one night, but is this the Dustin Ackley we&#x27;ve all been waiting for? 

For the better part of two years we&#x27;ve been waiting for a sign of something but have only captured brief glimpses amidst several false starts. 

According to Ackley, this recent turnaround may come down to a simple matter of trust, as described to Ryan Divish at the Tacoma News Tribune:

&quot;I think now it’s just something where I can really trust</pre>

右文（仅阅读辅助）：

<pre> in my swing, where before I didn’t really trust it and all that,” he said. “Now it’s gotten back to how it used to feel and that’s why I’m mentally focused every at-bat and ready to hit.”

Deep down I want to believe in Ackley, but it seems only fitting that since Friday night he has once again lost the magic touch. 

Which is</pre>

### 位置1829903｜random｜z=0.05629259

上下文1788，目标offset=389，目标token=" staged"；原文档未知。

包含目标的模型可见前文：

<pre> bodies or videos of dead bodies. You have seen no bullet holes or videos of bullet holes. You have seen no video or photo of any injured or dead being removed from the building or being taken to an ambulance or arriving at a hospital. The only helicopter footage shows people milling around or several men being chased and apprehended in the woods.

Everything you &quot;know&quot; is a retelling of events after the fact. It&#x27;s just faith. Not empirical.

~wobbles but doesn&#x27;t fall down~

^ A prime example of incorrect reasoning

My comment has no bearing on the Sandy Hook incident specifics, saying it does just shows you have absolutely no idea how to reason correctly.

Also there are many highly intelligent people who fail to reason correct so you yet again fail at reasoning when you conclude that I called anyone &quot;stupid and backwards&quot; which incidentally was your own ad hominem attack vs my claim that many people in this community haven&#x27;t learned how to reason correctly.

So thanks for being an example to my observation.

Here is the top story on Yahoo.

&quot;Man who helped Sandy Hook kids is harassed by conspiracy theorists&quot;


Some people wanted tears shed on television. Here you go. Some people desperately wanted attention drawn to &quot;Sandy Hook being a hoax.&quot;

Here you go. You have the attention now of the mainstream media.

**Downvotes, eh? Now you don&#x27;t want the attention? I thought the DailyPaul has been bombarded for weeks about this just so it could get national attention?

deacon&#x27;s picture

type the words

sandyhook into the search tab,pick one and read


I agree

I&#x27;ve personally never seen a media report be correct for something that I had first hand knowledge of. I&#x27;m quoted as saying Andrew Jackson is my favorite president.... I said Jefferson.

You say &quot;Serious claims

You say &quot;Serious claims require serious evidence&quot;.

This is a good argument to say it was staged</pre>

右文（仅阅读辅助）：

<pre>. The only &quot;evidence&quot; is shady interviews, and a gun that wasn&#x27;t even in the building.

End The Fed!
BTC: 1A3JAJwLVG2pz8GLfdgWhcePMtc3ozgWtz&lt;|im_end|&gt;Diirinka (4e Deity)

From D&amp;D Wiki

Jump to: navigation, search


A gaping smile against a white</pre>

### 位置4607950｜high_activation｜z=0.1936217

上下文4503，目标offset=762，目标token=","；原文档未知。

包含目标的模型可见前文：

<pre> vary dramatically based on the industry you&#x27;re in, but I think there are some elements of that for just about everyone.

MS. CURTIN: We&#x27;re fortunate in I can&#x27;t remember the last time a person in a management position left. I don&#x27;t think you ever replace a person because they bring in a skill set to an organization and they might be doing things a little bit differently. What we&#x27;re going to think about in order to replace someone is it&#x27;s not going to be an identical replacement because that&#x27;s not always the best situation for an organization. There could be someone that could do parts of it, and then you might want to bring in somebody with a completely different view on things. So before we fulfill a position, we ask what did that person bring to the table, and how do we see this going forward? Do we want to do something different with this?

MR. SABLJAK: We all know the relationships are critical between businesses and their customers, probably more important than we could ever recognize, but how do you handle that? Would your top customers stay if someone left, especially if you now have employees who have been with you for long periods of time?

MS. EVANS: We have a sales team that focuses on the customer. Our customers are very brand-loyal. We have our Western brand which has been out there for 50-plus years as well as our Fisher brand, so those are two very strong brands and we have very loyal customers. But what we&#x27;ve been trying to do over the last couple years is cultivate relationships, not only internally, but also externally. We try to have someone from our ops team go out with our sales staff at least two times a year so they&#x27;re out actually getting feedback from people that work in the manufacturing environment. We&#x27;re sending them to the distributors. We&#x27;re bringing our distributors on-site, giving them plant tours at both locations. So we&#x27;re trying to get them engaged as well as our workforce and then getting our workforce out to their places of employment to engage with them, because with our business, it&#x27;s all about relationships and we need to make sure that we maintain that brand loyalty. What we try to do with our employees internally, we try to do externally as far as communication. Any changes that we&#x27;re making, we make sure that the distributors know first and foremost and they&#x27;re getting multiple contacts not just from their sales staff.

MS. CURTIN: For us it&#x27;s a focus on training. Our hope is that when customers call or are placing an order, they might be dealing with a different person, but the level of service is going to be equally as good. So when you make a transition, we look to somebody that can make it as easy as possible to make introductions. It&#x27;s not going to be an identical replacement, but hopefully, you can expect that same level of service from another team member. We (also) find that there isn&#x27;t always a match between customers and team members. So at any point in time, someone can request to work with another person on the team. Our business model&#x27;s a little different with the direct marketing side of it that we have a wide range of customers, and generally within our team, they&#x27;ll find someone that&#x27;s a really good match to you. But our intent is that when you call, that you are going to have that same quality, and we&#x27;ll hear about it if you don&#x27;t. We know our customers well and if we find their retention level isn&#x27;t very good, we&#x27;re going to be asking, how we can improve the level of service.

MR. BOHN: We try our best to create a customer experience that transcends to the individual. I think the team approach, the cross-training,</pre>

右文（仅阅读辅助）：

<pre> the way you build your culture and your business is critically important, but probably unlike many other businesses, the consulting business is very much tied to the individual who has the primary customer relationship. There&#x27;s about a 70 percent correlation. So we use a variety of strategies, including trying to get multiple team members involved, making sure clients understand that there&#x27;s a team and a corporate commitment behind their relationship</pre>

### 位置5327818｜random｜z=0.07252794

上下文5207，目标offset=415，目标token=" are"；原文档未知。

包含目标的模型可见前文：

<pre> Iranians to demonstrate continued good faith,&quot; White House press secretary Jay Carney said last week, calling on Tehran to address its nuclear program &quot;in concrete ways&quot; with the U.S., Russia, China, Britain, France and Germany. He said sanctions and pressure on Iran would continue as well, led by the United States.

Congress is about to negotiate bipartisan legislation to green-light stronger sanctions. The Senate on Monday approved tough new penalties on the Tehran regime, while the House passed its version of the measure in December.

Asked about the objective for Baghdad, State Department spokeswoman Victoria Nuland said, &quot;We want to see a really concrete, serious discussion about steps that will demonstrate that we are moving in the right direction.&quot;

Obama opposes a near-term military strike on Iran&#x27;s nuclear facilities and has pressed Israel to give diplomacy and sanctions time to work. He insists that military options are available should talks fail, a position that clashes with Netanyahu and increasingly hawkish Republicans who want him to act even tougher.

Netanyahu in particular has charged the process with being too accommodating to Tehran. &quot;I see no evidence whatsoever that Iran is serious about ending its nuclear program,&quot; he said last week.

For all the talk of a positive atmosphere, U.S. officials have struggled to demonstrate any progress so far. They cautiously welcomed last month&#x27;s opening meeting in Istanbul but pushed off the harder questions until after this week&#x27;s follow-up talks. Official comments have continued to stress the importance of the process over single rounds of discussions, suggesting there may no breakthrough following the Baghdad meeting.

But patience isn&#x27;t inexhaustible. Many in the United States have accepted the Jewish state&#x27;s argument that Iran&#x27;s enrichment activity may be too far along and buried too deep underground after this summer for Israel to take military action. And a solid majority of Americans support the option of military action against Iran to prevent it from developing nuclear weapons, according to a recent Pew Research Center survey.

Lengthy negotiations without a clear outcome would enrage Israel because Iran would presumably continue expanding its nuclear program in the meantime. For Obama, however, the talks are</pre>

右文（仅阅读辅助）：

<pre> a calculated political risk.

On the one hand, they buy his administration some time on a tough decision over possible military action at a time of fevered partisan debate linked to November&#x27;s presidential election. But if the process collapses before then, it would undermine Obama&#x27;s claims of sturdy leadership on national security issues, from winding down America&#x27;s wars in Iraq and Afghanistan to killing al-Qaida leader Osama bin Laden</pre>

### 位置6057987｜random｜z=0.01539903

上下文5921，目标offset=54，目标token=" G"；原文档未知。

包含目标的模型可见前文：

<pre> the rules for him to carry around a key to his room. And it is more a room than a cell, because Colon lives in the Interperimeter Office-- what is known as the honor dorm.

In the inside-out, outright-bizarre world of Illinois prisons, G</pre>

右文（仅阅读辅助）：

<pre>ino Colon is a model prisoner. He also is the 41-year-old co-leader of the Latin Kings gang in Illinois.

Law enforcement officials and gang experts believe Colon calls the shots for all manner of illegal activity perpetrated by the Latin Kings throughout the state&#x27;s 26 adult prisons--including ordering the killing of a guard in 1989 and running a major drug ring.

None</pre>

### 位置8499037｜random｜z=0.005267195

上下文8307，目标offset=13，目标token=" more"；原文档未知。

包含目标的模型可见前文：

<pre> be lining up to watch his movies, and therefore making him even more</pre>

右文（仅阅读辅助）：

<pre> successful. Long live Iron Jay!

1306 days ago


lol @ all the retarded comments in here, so misinformed...also, check out his wife, hotter than any of the girls in here hating on jay and hotter than any of the dudes girls that are hating on him. I don&#x27;t think he&#x27;s worried about what any of you think, especially since he</pre>

### 位置10334384｜random｜z=0.0245543

上下文10100，目标offset=870，目标token=" Friday"；原文档未知。

包含目标的模型可见前文：

<pre>6% Mediaset S.p.A. Italy: Milan 3.12 -0.01 -0.26% Dec. 11, 2013 5:39 pm Volume : 8.09M P/E Ratio N/A Market Cap €3.69 Billion Dividend Yield 3.21% Rev. per Employee €576,066 11/25/13 Berlusconi Makes Last-Ditch Bi... 11/12/13 Mediaset SpA&#x27;s Nine-Month Net ... More quote details and news » and one of Mr. Berlusconi&#x27;s longtime lieutenants—was acquitted of the same charge of tax fraud in the same case, suggesting the judge attributed Mr. Berlusconi most of the blame.

Judge Edoardo D&#x27;Avossa first sentenced Mr. Berlusconi to a four-year jail term on charges of using offshore companies to buy film and TV rights a decade ago at inflated prices, allegedly allowing him to fraudulently lower the tax bill of broadcasting company Mediaset SpA.

The term was automatically reduced to one year because the court applied an amnesty law passed in 2006 by the center-left government of Romano Prodi.

The court also banned Mr. Berlusconi from public office for five years and from holding a position in a company for three years.

Former Italian premier Silvio Berlusconi leaving court in Milan, in a photo taken on Oct. 19, 2012. Zuma Press

&quot;This conviction is political, incredible and absolutely intolerable,&quot; the 76-year-old Mr. Berlusconi said in a TV interview on Friday evening.

Mr. Berlusconi&#x27;s lawyer said he would appeal Friday&#x27;s verdict.

This isn&#x27;t the first time Mr. Berlusconi has been convicted in a criminal trial. Lower courts have convicted Mr. Berlusconi in four other cases since 1990 for charges ranging from perjury and corruption to false accounting.

All of the sentences have either been suspended by amnesty laws, overturned in appeals or dismissed after the statute of limitations had expired.

Trying Times for Berlusconi

Take a look back at the ups and downs during his 18 years in politics.

Mr. Berlusconi is also currently on trial for allegedly paying an underage woman for sex and abusing his former office as prime minister in an attempt to cover it up. Mr. Berlusconi has denied those charges, saying he never had sex with the woman.

Friday&#x27;s ruling, which cuts to the heart of Mr. Berlusconi&#x27;s fortunes—his huge television empire—delivers a symbolic blow to the businessman-turned-politician just as he is trying to breathe new life into his once-dominant political force.

Public support for Mr. Berlusconi&#x27;s conservative People of Freedom party, one of Italy&#x27;s two main political movements, has plunged as low as 14% in recent polls as the it fends off challenges from anti-establishment parties.

Some of the party&#x27;s local politicians have also recently been placed under investigation for misuse of political funds and connections to organized crime.

&quot;This isn&#x27;t a sentence; it&#x27;s an attempt at political homicide,&quot; said Fabrizio Cicchito, a top lawmaker in Mr. Berlusconi&#x27;s party.

In recent weeks, People of Freedom has been hit by a slew of scandals that have further eroded the party&#x27;s standing in the polls. In the Lazio region, which includes Rome, lawmakers are under investigation for allegedly using taxpayer money to fund personal expenses. They denied any wrongdoing.

Over his 18 years in politics, Mr. Berlusconi has managed to rally many Italians around him as he successfully defended himself in dozens of trials and criminal investigations. He has often lashed out at prosecutors for having an agenda against him, and many in Italy believed him.

The President of the Court Edoardo D&#x27;Avossa reads the sentence in the trial of Silvio Berlusconi, in Milan, Italy, 26 October 2012. European Pressphoto Agency

&quot;I was sure I&#x27;d get acquitted from this totally unreal accusation,&quot; Mr. Berlusconi said in the TV interview on Friday</pre>

右文（仅阅读辅助）：

<pre>, denying any wrongdoing in the trial.

Though the decision was a setback, it is unlikely to derail Mr. Berlusconi&#x27;s self-proclaimed status as the behind-the-scenes &quot;noble father&quot; of his People of Freedom party.

Mr. Berlusconi&#x27;s lieutenants rushed to defend the former premier, backing up the billionaire&#x27;s claims that he has long been persecuted by left wing prosecutors.</pre>

## Feature 10499，h_V=1

### 位置112043｜random｜z=0.07059336

上下文109，目标offset=490，目标token=" D"；原文档未知。

包含目标的模型可见前文：

<pre>4486. 
  36. ^ Sugranyes G, Kyriakopoulos M, Corrigall R, Taylor E, Frangou S (2011). &quot;Autism spectrum disorders and schizophrenia: meta-analysis of the neural correlates of social cognition&quot;. PLoS ONE 6 (10): e25322. doi:10.1371/journal.pone.0025322. PMC 3187762. PMID 21998649. 
  37. ^ Fadiga, L.; Craighero, L. &amp; Olivier, E. (2005). &quot;Human motor cortex excitability during the perception of others&#x27; action&quot;. Current Opinion in Neurobiology 15 (2): 213–218. doi:10.1016/j.conb.2005.03.013. PMID 15831405. 
  38. ^ Shamay-Tsoory, S.G. (2011). &quot;The Neural Bases for Empathy&quot;. The Neuroscientist 17 (1): 18–24. doi:10.1177/1073858410379268. PMID 21071616. 
  39. ^ Nishitani, N.; Avikainen S. &amp; Hari R. (2004). &quot;Abnormal imitation-related cortical activation sequences in Asperger&#x27;s syndrome&quot;. Annals of Neurology 55 (4): 558–562. doi:10.1002/ana.20031. PMID 15048895. 
  40. ^ Dapretto, M., Davies M.S. et al. (2006). &quot;Understanding emotions in others: mirror neuron dysfunction in children with autism spectrum disorders&quot;. Nature Neuroscience 9 (1): 28–30. doi:10.1038/nn1611. PMID 16327784. 
  41. ^ D</pre>

右文（仅阅读辅助）：

<pre>instein I, Thomas C, Behrmann M, Heeger DJ (2008). &quot;A mirror up to nature&quot;. Curr Biol 18 (1): R13–8. doi:10.1016/j.cub.2007.11.004. PMC 2517574. PMID 1</pre>

### 位置2673322｜random｜z=0.1047731

上下文2612，目标offset=717，目标token=" O"；原文档未知。

包含目标的模型可见前文：

<pre> have lost their importance. As short as possible: a Christian lives under two completly different kingdoms, where the one is &quot;God&#x27;s kingdom under Christ&quot;1 – here he lives by faith in the righteousness coram Deo2 – and the other is the world&#x27;s kingdom – here he is man or woman, young or old, lord, servant, peasant, citizen etc.3 and has to do good works.

Accordingly, the human being is both: Christian person and secular person.

You see: the accusation, that Luther&#x27;s justification by faith alone shrinks the room for the works that have to be done by us, is a misunderstanding. Especially Luther&#x27;s theology shows people, how overfull of opportunities for good works the world and the way, which they follow in the world by faith, is.

1: &quot;Gottes Reich unter Christo&quot;
2: before God
3: WA 32, 440, 2
4: &quot;Christperson&quot; and &quot;Weltperson&quot;

share|improve this answer
The three uses of law really seem to include this idea. Lutherans seem to talk quite a lot about them... –  dancek Sep 25 &#x27;11 at 11:05
add comment

Your Answer


&lt;|im_end|&gt;Pawlenty Drops Out

August 15, 2011 - 4:03 AM

How can this happen? How can a successful governor hire a group of really smart people, spend more than a year, and who-knows-how-many millions of dollars, meeting with potential and actual supporters, and elite members of the media in places like New York City, Los Angeles, and Washington, D.C., only to come to a grinding halt in a place called Ames, Iowa?

The threshold problem with the presidential campaign of Gov. Tim Pawlenty was: From the very, well, threshold there was no clear theory for the campaign. It never occurred to me that Pawlenty was going to be able to &quot;nice&quot; his way into the Oval Office.

Most people along the trail liked him. What&#x27;s not to like? Many people in and around politics confuse a candidate&#x27;s likability with his or her electability.

When someone mentions that so-and-so is much more likable than someone else I always respond with the same two words: Richard Nixon. Nobody liked Nixon. Not even, maybe, his wife. Yet, he won twice. Three times if you buy into the conspiracy theory that the Dems stole Texas (via Lyndon Johnson) and/or Illinois (Joe Kennedy &amp; the Chicago mob) in the election of 1960.

One of Pawlenty&#x27;s senior staffers told me that Pawlenty just couldn&#x27;t get any traction with an angry electorate -- especially in the face of a Bachmann campaign which has made its mark by selling her as the angriest candidate on the scene.

Speaking of Bachmann, one of her senior staffers told me that he felt like they&#x27;d just won the play-in game for the NCAA basketball tournament. Now they get to compete in the &quot;big dance.&quot;

Like that tournament, you have to win on Thursday to play on Saturday. You have to win on Saturday to get to the next round. Bachmann won in the debate here Thursday night; she won again yesterday so she gets to go on.

Pawlenty&#x27;s campaign might have effectively ended, not here in Ames, but on the debate stage in New Hampshire when he refused to engage Mitt Romney on what he had previously called O</pre>

右文（仅阅读辅助）：

<pre>romney-care -- the Massachusetts health care law Romney signed as Governor.

With nothing on the schedule to allow him to &quot;angry up,&quot; after that, Republicans were left with the impression that what had been known as &quot;Minnesota Nice&quot; might really be &quot;Minnesota Wimp.&quot;

In the debate here, Pawlenty and Bachmann went toe-to-toe on the contents of a bill in the Minnesota</pre>

### 位置4437109｜random｜z=0.01126719

上下文4336，目标offset=801，目标token="^"；原文档未知。

包含目标的模型可见前文：

<pre> to be more a question of doing lots of writing than an honest theoretical problem. You can probably do it using the fact that H is a classifying space of polarized Hodge structures, as Kevin Buzzard mentioned in the comments.

share|improve this answer
add comment

Its easy to check that every matrix in $SL_2(\mathbb{R})$ can be wrtten uniquely as $\begin{pmatrix} \lambda &amp; \alpha \\ 0 &amp; \lambda^{-1}\end{pmatrix}\begin{pmatrix} \cos{\theta} &amp; -\sin{\theta} \\ \sin{\theta} &amp; \cos{\theta} \end{pmatrix}$ where $\lambda&gt;0$. This is exactly written then as a coset representative of the quotient you wrote down above. You can arrive at the hyperbolic metric by following the definition of the pushforward metric from a left invariant metric on $SL_2(\mathbb{R})$. Notice $(\alpha,\lambda)$ is a point in the upperhalf plane.

The latex misbehaved, those should be $2\times 2$ matrices.

share|improve this answer
Thanks for your answer! What&#x27;s an example of a left-invariant metric on SL_2(R)? Does it matter which one I choose if there are more than one? –  Qiaochu Yuan Mar 29 &#x27;10 at 17:14
Quaochu, pick any metric on the Lie algebra---that is, the tangent space at the identity element---and translate it. –  Mariano Suárez-Alvarez Mar 29 &#x27;10 at 17:26
Cool. So there remains another question which is maybe better asked as a separate question: what is the connection between the metric structure on H and the Riemann surface structure? –  Qiaochu Yuan Mar 29 &#x27;10 at 18:15
A Riemann surface structure is the same thing as a conformal class of metric structures. –  Mariano Suárez-Alvarez Mar 29 &#x27;10 at 18:49
In general left-invariant metrics on a Lie group, even a simply connected one, can be non-isometric -- Tam Nguyen Phan showed me a nice example of different left-invariant metrics on S^3. But the pushforward metric on SL(2,R)/SO(2) is homogeneous (acted on transitively by isometries), and thus of constant curvature, and so is either S^2, R^2, or H^2. You can then check (in any number of ways) that it&#x27;s not flat, so must be H^2. –  Tom Church Mar 29 &#x27;10 at 20:21
add comment

There is a very physical picture to this, if you are willing to work with the disk model of hyperbolic space, instead of the upper half plane, to which it is related by an isometry.

The Lie group $\mathrm{SL}(2,\mathbb{R})$ is a double cover of the identity component $\mathrm{SO}_0(2,1)$ of $\mathrm{O}(2,1)$, which is the Lorentz group in 3 dimensions. In other words, $\mathrm{O}(2,1)$ is the subgroup of $\mathrm{GL}(3,\mathbb{R})$ which preserves a symmetric inner product $\eta$ of signature $(2,1)$: $$\eta = \begin{pmatrix} 1 &amp; 0 &amp; 0 \cr 0 &amp; 1 &amp; 0 \cr 0 &amp; 0 &amp; -1 \end{pmatrix}.$$

Now consider the two-sheeted hyperboloid in $\mathbb{R}^</pre>

右文（仅阅读辅助）：

<pre>3$ defined by $x^2 + y^2 - z^2 = -1$. The upper sheet -- let&#x27;s call it $\mathbb{D}$ -- with $z&gt;0$ is topologically a disk. It inherits a riemannian metric from the Minkowski metric on $\mathbb{R}^3$ defined by $\eta$. The identity component of $\</pre>

### 位置4596446｜random｜z=0.04569102

上下文4492，目标offset=521，目标token=" A"；原文档未知。

包含目标的模型可见前文：

<pre>c electronic density map of thiamine contoured at 1 sigma (A) and coordination of each Mg2+ ion in the TPK/thiamine complex (B-C). Fo-Fc electronic density map contoured at 1.5 sigma (displayed in green) of TPNP (D) with Mg2+ and PO43-. This map was computed using the refined structure where all ligands have been removed. Coordination of each Mg2+ ion in the TPK/thiamine-PNP complex (E-G). Magnesium are represented as white spheres, water molecules as cyan spheres, oxygen atoms are in red, nitrogen in blue and carbon in green. Mg2+ coordinations are marked with magenta dashed lines.

As observed in other structures (PDB id 2G9Z, 1IG3 and 2F17) there is a weak stacking between an aromatic residue (Y285B in CA1462) and the amidopyrimidine ring (Figure 4A–C). The CM2 carbon makes hydrophobic interactions with the W290B side chain, a residue conserved in the sequence of the S. cerevisiae homologue. In the mouse sequence this residue is replaced by an aspartate and does not make any contact with the ligand. Nevertheless, a certain hydrophobic environment is maintained in the murine structure with the spatial proximity of a leucine (L204). The thiamine ammonium group N4 of the amidopyrimidine ring is engaged in a salt bridge with the Q138A main-chain carbonyl oxygen (Figure 4A). The opposite side of this ring is stabilized by another salt bridge involving N1 and the oxygen from the S299B side chain (Figure 4A). The aspartate residue interacting with N4 and N3 described in the mouse structures [26] is replaced by a tyrosine (Y139B) too far away from the ring to interact with it. N5 from the thiazolium ring is stabilized by electrostatic interactions between the main chain carbonyl oxygen atoms of S300B and Q138A.

thumbnailFigure 4. Stereo view of the superposed ligand binding sites from different species. The superposition was obtained using as reference structure (in yellow) the C. albicans TPK co-crystallised with TPNP (PDB id 2G9Z) and A</pre>

右文（仅阅读辅助）：

<pre>) S. cerevisiae (Blue) (PDB id 1IG0), B) Mouse (green) (PDB id 2F17) C) C. albicans TPK co-crystallised with thiamine (red) (PDB id 2HH9). Residue numbers correspond to C. albicans numbering.

At least 2 residues involved</pre>

### 位置4639641｜high_activation｜z=0.2043824

上下文4534，目标offset=755，目标token="G"；原文档未知。

包含目标的模型可见前文：

<pre> limits and the issue can then be handled by cutting bureaucratic red tape.

Removing the incentives for people to desire our private info would similarly remove most of them from going after it as well. We just have to be clear that there are two ways to remove an incentive. We can legislate it as illegal (or pass laws that the government can&#x27;t do it) or we can de-fund whatever profit stream the criminals benefit from by using it. Each separate issue has their own set of money trails but I&#x27;ll use just one as an example.

&quot;There will always be some .. politician who wants to pass a law...&quot;
Ok, fine. So we ask why they would want to. Does Senator Jones really have a lifetime quest to change his pet behavior? No. He absolutely does not. In 99.9999% of the cases, he was lobbied to support and then handed that bill. So, our investigation has led back to the lobbyists and we must ask why they do it.

For money again, from Acme corporation. Is it practical to chase down and stop it at this stage? Maybe, but probably not. Congress won&#x27;t change this rule unless a vast majority of the people are really pissed and organized against it. Unlikely so far. So why do the companies do this bribery?

For money again, from increased profits and total market controlled monopolies. Ok, so change that? Never. ...say most people. But wouldn&#x27;t it take less people to put Acme out of business than to change the lobbying laws? People boycotted BoA a couple years ago and dropped their stock about 5-10% in just 2 days. They didn&#x27;t fall because we let off but what if we hadn&#x27;t? What if we had an organized voice that said &quot;Hey Monsanto, stop all GMO or we&#x27;ll permanently boycott every company you have contact with.&quot; Who wouldn&#x27;t join that battle? (Only sharmers - sleeping sheep farmers)

So, you see if we follow the trail far enough, every issue does have a level of accountability to the general public. We just have to stay vigilant and cohesive in targeting that bulls-eye.&lt;|im_end|&gt;










Shanghai is currently taped out and running Windows at AMD.

Comments     Threshold


By Aikouka on 4/18/2008 9:10:35 AM , Rating: 2
I&#x27;m not sure what you mean, because programming can inherently become more complex as you raise the number of threads. Now, the reason why I boldfaced &quot;can&quot; is because not all tasks are hard to break down. A simple computation can typically be broken down into parts and combined later on, but that&#x27;s just a simple computation. But there are tasks that are harder to break down. I remember taking a parallel processing course back in college and one of the focuses early on in the class was learning how to break down a task into parts that could be split amongst the cluster of machines. Some were pretty simple yet even tasks that looked easy to break down sometimes proved to be a bit tricky.

By freeagle on 4/18/2008 11:45:52 AM , Rating: 2
What I mean is that people tend to &quot;force&quot; parallel programming where it&#x27;s not appropriate, that&#x27;s why it seem to be getting harder. If you know how to break a task into parts, that can run in parallel, then you know whats the maximum number of threads you can utilize without getting into synchronization nightmares.



Related Articles
AMD Finally Ships &quot;B3&quot; Opterons
March 12, 2008, 1:13 PM
G</pre>

右文（仅阅读辅助）：

<pre>earing Up For AMD Revision G
May 24, 2006, 5:35 AM
&lt;|im_end|&gt;

  (Source: 20th Century Fox)









Comments     Threshold


Adjusted for inflation...
By theinnkeeper on 1/25/2010 4:29:52 PM , Rating: 4
Every time the</pre>

### 位置5046929｜high_activation｜z=0.205359

上下文4932，目标offset=873，目标token=":H"；原文档未知。

包含目标的模型可见前文：

<pre>34277868) Attached to: US May Disable All Car Phones, Says Trans. Secretary
Yea. Actually there&#x27;s a budding market for it. They even made a class of vehicle for those who enjoy it. They&#x27;re dubbed, &quot;Recreational Vehicles&quot;.
Snarky comments aside, it absolutely is. A hammer is a tool to get work done in one man&#x27;s hand, and an instrument for another man&#x27;s hobby. Ever seen a biker gang moseying down a highway on a sunday morning? They aren&#x27;t going anywhere, they&#x27;re just there for the ride. Classic vehicle owners often go for joy rides. I personally enjoy going for a ride in old diesel pickup trucks, something about the purr of their motor and the way they lazily meander down the road does it for me.

Comment: Re:Heuristic (Score 1) 394

by pwnies (#34021224) Attached to: Bees Beat Machines At &#x27;Traveling Salesman&#x27; Problem
4 days for 5 flowers? A brute force approach to the traveling salesman problem is a n! growth rate. For 5 flowers, you only have 120 combinations. That&#x27;ll take a few microseconds to solve on my phone. You wont start seeing time being measured in days until you hit 14 flowers or so. Not saying you&#x27;re wrong about the fact that we have problems, but just that 5 flowers isn&#x27;t going to stress anyone.

You can&#x27;t take damsel here now.&lt;|im_end|&gt;Forgot your password?


Comment: Re:You do not understand the subject matter (Score 1) 580

by speroni (#35522442) Attached to: US Alarmed Over Japan&#x27;s Nuclear Crisis

Westinghouse is building the AP1000 plant. First 4 are in China and the next for are in the us in Georgia and South Carolina.

The AP1000 is much better in design than the 40 year old fukushima plants. To point out one major difference the AP1000 reactor coolant loop has been designed to support natural convection, which means in the case of loss of offsite power and loss of back-up diesel generators, the AP1000 will continue to cool the core.

You can&#x27;t take damsel here now.&lt;|im_end|&gt;Forgot your password?


Comment: Re:Pros vs Cons (Score 1) 549

by zugmeister (#45592411) Attached to: RF Safe-Stop Shuts Down Car Engines With Radio Pulse
When you use your brakes without the &quot;assist&quot; part of &quot;power assist&quot;, you are now fighting against your brake booster, as well as the resistance of the brake system itself. Believe me, a car produced without the power option is not that difficult to bring to a halt.

Are you sure it was a Toyota Corona?

Comment: Re:Nature Of the Beast (Score 1) 477

by zugmeister (#45530385) Attached to: Ask Slashdot: Best Laptops For Fans Of Pre-Retina MacBook Pro?
I&#x27;ve had really good luck with my jailbroken ipad3. There are a number of good VNC clients on the Apple store. Weather you like Apple or not their bluetooth keyboard is a great piece of hardware and with the jailbreak you can get BT mouse support as well. If you know anyone with a jailbroken iPad, it may be worth your time to check out.

Comment: Re:Cannot upgrade or repair? (Score 1) 477

by zugmeister (#45529855) Attached to: Ask Slashdot: Best Laptops For Fans Of Pre-Retina MacBook Pro?
While replacing the air filter on her truck, my wife once tried to screw in the top of the airbox cover. Having little experience, she started the screws with a drill. Three of the four were cross-threaded immediately and she was angry at the drill, didn&#x27;t know to start them by hand. I can totally see someone with a power tool installing plugs and cross threading them into the heads.

Comment: Re:H</pre>

右文（仅阅读辅助）：

<pre>oarders (Score 1) 249

by zugmeister (#45398083) Attached to: Netflix, Youtube Surpass 50% Mark of Internet Traffic
Netflix to the rescue! Offer to share your disks in exchange for borrowing someone else&#x27;s stuff. Does Amazon have a used copy? Ebay? Check Redbox when the Library doesn&#x27;t have</pre>

### 位置5624326｜random｜z=0.02298594

上下文5497，目标offset=193，目标token="I"；原文档未知。

包含目标的模型可见前文：

<pre>y Jul 5 &#x27;10 at 20:52
add comment

1 Answer

up vote 1 down vote accepted

In development, it should reload every you access. In production mode, you can turn off cache by modifying


Change the following line to false.

config.cache_classes = false

And restart the application.

It reloads the changes without restarting the server.

Update You might try load instead of require.

load &#x27;services/test.rb&#x27;
share|improve this answer
No, this happens in the development mode –  Ibrahim Hussein Jul 6 &#x27;10 at 11:59
I updated the answer. With &#x27;load&#x27;, it reloads every time. –  OmniBus Jul 7 &#x27;10 at 10:33
It worked! Thanks –  Ibrahim Hussein Jul 9 &#x27;10 at 0:16
add comment

Your Answer


&lt;|im_end|&gt;Take the tour ×

I</pre>

右文（仅阅读辅助）：

<pre> have a java class as follows:

public class Query implements Serializable {
    static Object[] o= new Object[8];

    private long oid= (Long) o[0];
    private double[] region= { (Double) o[1],(Double) o[2],(Double) o[3]  };
    private boolean filter= (Boolean) o[4];
    private</pre>

### 位置8409684｜high_activation｜z=0.2063356

上下文8219，目标offset=722，目标token="R"；原文档未知。

包含目标的模型可见前文：

<pre> adopters is, &quot;Why are adoption fees so high? Shouldn’t adopting a dog be free, or at least super cheap?&quot; To these people I say, remember, you get what you pay for.


When you purchase a purebred from a dog breeder you may be paying anywhere from $500 to over $1,000 for your new puppy, but often that’s all you&#x27;re getting for that cost. When you adopt a dog from a shelter, your adoption fees are going to pay towards the cost of care your adopted dog has received while at the shelter. Which is why adoption fees are often adjusted based on the age of the dog you&#x27;re adopting. Here is a breakdown of what a good shelter has already put into your dog before you even adopt.


Spay &amp; Neuter


The average cost for veterinary care varies greatly depending on your geographical location (city vs. country), the size of the dog requiring care, as well as the dog&#x27;s overall picture of health and how it influences the complexity of treatments. That said, the average dog spay or neuter can range from $45-$175 for an animal shelter. However, this doesn’t include the cost of pain relief medication that the shelter will also be responsible for, which is another $10-$30 dollars. If you were to get your adopted dog spayed or neutered on your own it could cost you anywhere from $200-$500 plus, depending on said variables.




The cost of intake vaccinations for dogs to prevent Distemper, Parvo, Kennel Cough, and rabies can cost approximately $40 for the animal shelter — if not more. If your adopted dog has been in the shelter for a few months it has most likely received a monthly booster to keep it safe from shelter related illness. If you were to pay for these vaccinations yourself you could be paying anywhere from $20-$150 dollars


Parasite Treatments and Preventatives


Monthly flea tick and ear mite treatments as well as heartworm preventives for dogs are another monthly cost for animal shelters. De-wormer medications are often given preventatively as oppose to waiting to see evidence of worms. These treatments can cost approximately $10-$30 assuming that no labs are need. Lyme disease and heartworm tests are also another cost the shelter will incur to ensure that your dog is in good health. If a dog tests positive, Lyme disease treatment can cost anywhere from $20-$100 depending on the size of the dog. However, if a dog needs to be treated for heartworms the treatment can be extremely costly, and on average it’s at least $1,000 if you were to pay for it yourself.



Share this page

Comments  4

Leave Comment
  • Purebred dogs
    11/03/2012 03:48pm





  • what bunk
    11/03/2012 04:12pm


  • typing too fast
    11/03/2012 04:28pm

    Keep dogs out of shelters.. buy from a good breeder

  • a business
    11/03/2012 05:49pm


Related Articles

Why You Should Consider Getting a Shelter Pet
Five things you may have heard in the past about shelter pets, and what the actual...
R</pre>

右文（仅阅读辅助）：

<pre>abies: Then and Now
What is rabies? Is there really a rabies vaccine? What does it do and can it protect...
Pesky Summertime Pests
Summer is here, and with it comes fun in the sun, camping and hiking, and trips to...



Around the Web
&lt;|im_end|&gt;What do you think this poem is about?

How Can We Survive?

How can we</pre>

## Feature 10807，h_V=0

### 位置445841｜random｜z=0.03665425

上下文435，目标offset=698，目标token=" want"；原文档未知。

包含目标的模型可见前文：

<pre>. The number of gems and jewels to collect increases as the level is increased. You will enjoy this forever because there are unlimited levels.

Comments and ratings for Three Animals Lite
  • (80 stars)

    by Angie Dominic on 22/06/2013

    Love the task mode - I went straight to no. 1 on the leader board, can anyone beat me? This game has loads going for it so go try it - you won&#x27;t be disappointed.&lt;|im_end|&gt;Dr Bertram Miller, Md a retired pediatrician who lived and I hope still lives in Mexico was a very experience color printer. Obviously, as you may well have guessed, there was a Miller Method I and II.

Miller Method III is a system that uses both software as well as a reflection densitometer to determine proper color balance for printing color negatives.

As in all systems one would have to make a test print of a known tone. A gray card was best. One would also have to indicate in the software if you were using Fuji or Kodak. Having made the test print then one would read the values with a reflection densitometer and indicate those values in the computer program. The software would recommend a new exposure and filter data. If you had the rest of your process under control then within three test prints you would have a proper print of a gray card. The software was using information for Kodak and Fuji gammas for the individual colors and do the mathematics to quickly get one into the ball park.

When the testing was completed it would be used as follows..assuming a gray card standard. Photograph a gray card just before taking photos under the existing conditions and then photograph your scene with the same settings. Process your film. Project your gray card image. Process it and make your densitometer readings. Enter those readings into the software and you would get the information for a properly exposed print of your negative and all others given the same exposure under the same conditions.

So it would go until you ran out of that emulsion batch of paper. Starting a new batch should only require on test and away you go.

Obviously if you were to use for example Kodak Gold Plus film with mercury vapor lights w/o filtration the best that could be accomplished would be a substandard print as compared to normal color balance. If you negative was way under or very much over exposed your prints would indicate that.&lt;|im_end|&gt;FP is a flash bulb that burns slowly, so that it can sync with a focal plane shutter that is never completely open. I don&#x27;t know if FP bulbs are made anymore.

Unless you want to do fill flash outdoors in bright light, you don&#x27;t really need a sync speed faster than 1/30 sec.&lt;|im_end|&gt;North America
    South America

Walk Like A King  

January 03, 2013

Berlin, Germany


Questions &amp; Answers

Expand all Q&amp;A

Why do Angels have wings, what is the symbolism of that? Can you please talk about why we have Angels in the Christian tradition.

Sri Sri: Man had a fascination to fly. He wanted to dominate space.
Man could walk the Earth, he could dive into the ocean and swim in the water. But what he could not do is fly. So Angels, which he considered one step above him, he gave them wings. He thought, Angels have wings because they are more powerful than man and they can fly and can go anywhere they want</pre>

右文（仅阅读辅助）：

<pre>.
But today with the kind of airplanes we have, Angels will be much slower. We can reach much faster than them. We will leave the Angels behind somewhere.
Nobody with wings, however powerful, can fly faster than an aircraft or a helicopter.
So it is just a concept that they are more powerful than us, because it is only then that they can help us.
Angels mean those who</pre>

### 位置2495545｜random｜z=0.05740621

上下文2439，目标offset=11，目标token="'re"；原文档未知。

包含目标的模型可见前文：

<pre>rowns and says, &quot;I sometimes wonder who they&#x27;re</pre>

右文（仅阅读辅助）：

<pre> talking about. I sometimes wonder who it is who is supposed to be exerting this influence on younger writers.&quot;

DeLillo was still a child when he started positioning himself at what he describes in Underworld as &quot;an angle to the moment&quot;. His parents moved separately from Italy to New York, where they met and in 1936 had a son. DeLillo supposes his parents</pre>

### 位置4590246｜high_activation｜z=1.041415

上下文4486，目标offset=465，目标token="2"；原文档未知。

包含目标的模型可见前文：

<pre> are conserved in pathogenic fungal genomes and can be absent from the non-pathogenic yeast Saccharomyces cerevisiae.

Candida albicans is a diploid organism with eight sets of homologous chromosomes and a genome size of about 32 Mb. This pathogen is part of the normal microflora of the human gastrointestinal tract or oropharynx and is responsible for various nosocomial infections, potentially lethal in immunocompromised patients or patients in the intensive care unit. The CA1462 protein is encoded by a gene conserved across all known fungal genomes. It shares 36% sequence identity with Saccharomyces cerevisiae YOR143C [2], a Thiamine pyrophosphokinase (TPK, EC essential for fungus growth and survival [3]. This enzyme is also essential in S. pombe [4]. The production of thiamine pyrophosphate (TPP), catalyzed by TPK, is critical for both catabolic and anabolic cellular processes. In vertebrates, a deficiency in thiamine synthesis is linked to neurological diseases such as beriberi and Wernicke encephalopathy [5]. In all synthesizing organisms, thiamine (vitamin B1) is produced from phosphorylated HET (4-methyl-5-(β-hydroxymethyl)thiazole) and HMP (2-methyl-4-amino-5-hydroxymethyl-pyrimidine) that are condensed into thiamine phosphate. In yeast, this thiamine phosphate is then hydrolyzed into thiamine before pyrophosphorylation by the TPK that catalyzes the transfer of a pyrophosphate (PPi) from ATP to thiamine, resulting in AMP and TPP [6].

This article reports the enzymatic characterization as well as the structure determination of the Candida albicans CA1462 Thiamine pyrophosphokinase in complex with both thiamine and thiamine-PNP (TPNP). We also present a comparison of CA1462 with the structure of the mouse TPK ternary complex with pyrithiamine pyrophosphate and AMP (PDB id 2</pre>

右文（仅阅读辅助）：

<pre>F17) [7], with the TPK S. cerevisiae structure (PDB id 1IG0) [8] and with sequences from other species.


General cloning strategy

The cDNAs corresponding to the TPK genes were amplified by PCR from their respective genomic DNAs (CA1462: Candida albicans strain NIH 3147 ATCC</pre>

### 位置4597119｜high_activation｜z=1.014071

上下文4493，目标offset=170，目标token="2"；原文档未知。

包含目标的模型可见前文：

<pre> molecule (O3). In the AMP-PNP molecule, a nitrogen atom (N3) replaces O3. While we did not get crystals of the TPK/Thiamine/AMP-CPP complex, the TPK incubated with thiamine and AMP-PNP produced usable crystals. However, the structure revealed that instead of a TPK/Thiamine/AMP-PNP complex, we obtained an unexpected TPK/thiamine-PNP complex with a TPNP molecule in the enzyme binding site (Figure 3D). This result is consistent with the earlier suggestion that the pyrophosphate group is transferred at once from the ATP molecule to the thiamine moiety.

The superimposition of the C. albicans TPK/TPNP complex onto the mouse TPK/TPP complex (PDB id 2</pre>

右文（仅阅读辅助）：

<pre>F17) highlights few differences between the two thiamine phosphate ends. The nitrogen N3 in the TPNP molecule is symmetrically opposed to its equivalent oxygen O3 in the TPP molecule. It is stabilized by a weak electrostatic interaction (3.28 Å) with the S301B γ-oxygen in the C. albicans TPK/TPNP complex (</pre>

### 位置5265547｜random｜z=0.03946187

上下文5146，目标offset=550，目标token=" closer"；原文档未知。

包含目标的模型可见前文：

<pre> appreciate the way we were treated,&#x27;&#x27; the mayor said. &#x27;&#x27;And if you have to lose, it&#x27;s better to lose to a city like this. These people sent us search-and-rescue crews.&#x27;&#x27;

When the team of his heart could not clinch the World Series on Saturday, the mayor had flown back to make sure his city was functioning during the marathon, always the most joyous day of the year.

Then he got on a plane to Phoenix for Game 7, joining a group of family members of some of the victims of the disaster. He has ministered to people since Sept. 11, and if he wanted to be a surrogate fan, with access to good seats, he more than earned it.

&#x27;&#x27;This was a great World Series, like we had when I was younger,&#x27;&#x27; he was saying. &#x27;&#x27;The Yankees against the Braves. The Yankees against the Dodgers. It seemed like they always went seven games. We got spoiled.&#x27;&#x27;

&#x27;&#x27;I kept thinking we&#x27;d do it,&#x27;&#x27; he added. &#x27;&#x27;Even with runners on base, I thought Mo would get a double play. Baseball is a game of inches.&#x27;&#x27;

He also praised Steve Finley&#x27;s acrobatic catch in right-center field. This was fan talk, but the mayor was also seeing a much bigger picture.

&#x27;&#x27;Let&#x27;s keep the focus on what it meant to our October,&#x27;&#x27; he kept saying. &#x27;&#x27;It was great for our economy, great for our spirit. It brought people and money into the city.

&#x27;&#x27;I&#x27;m not that disappointed. The Yankees did everything they could. They were a symbol. They never gave up. They were out of it, and they came back. They are still champions.&#x27;&#x27;

He even saw some value in losing the seventh game of an epic World Series.

&#x27;&#x27;It gives the city a sense of reality, what you can accomplish,&#x27;&#x27; he said. &#x27;&#x27;This is a city that just got hit with the worst attack in the history of our country, but the people hung in there.&#x27;&#x27;

The players were dressing and heading for the bus that would take them into a winter of roster changes.

By now the mayor&#x27;s aides were trying to rush him toward the charter back home. Today is Election Day. The new mayor must be confident enough to allow Rudolph Giuliani to help in the recovery of the city. But for now, the mayor still has the power to authorize a parade.

There had been speculation whether it was appropriate to stage a traditional ticker-tape parade for the Yankees. &#x27;&#x27;Whatever they want,&#x27;&#x27; the mayor said. &#x27;&#x27;I&#x27;ll be talking to them tomorrow. Most teams don&#x27;t want to celebrate if they finish second, but I&#x27;ll do whatever they want.&#x27;&#x27;

The mayor spotted Rivera, carrying his overnight bag toward the doorway. He stepped closer</pre>

右文（仅阅读辅助）：

<pre> and whispered things in Rivera&#x27;s ear.

&#x27;&#x27;You did great,&#x27;&#x27; was all one eavesdropper could hear.

Rivera, a stable man with a religious core, is not about to grieve all winter for a few pitches that got away. He smiled gracefully and moved out into the night. The mayor stayed a few more minutes, despite his watchful aides. These were his Yankees, and</pre>

### 位置6255989｜random｜z=0.131747

上下文6114，目标offset=603，目标token="det"；原文档未知。

包含目标的模型可见前文：

<pre> subject(s) it wants over the years.

These position receive a very large number applications, and so some sort of filtering system along the lines Ben suggests must happen. Having strong references is perhaps the most important thing.

(I had one of these. I didn&#x27;t know anyone at the college before, but in the end, a mathematics fellow at the college in question worked in a field rather close to mine, and interviewed me, so presumably understood my work and was sufficiently impressed by it. But the other postdoc in my year at the same college was in a different area, and the college simply invited in an expert from outside to interview him. So my strong advice would be to apply for everything, and get lucky once!)

The best guide to these things remains, I think, Tom Korner&#x27;s: http://www.dpmms.cam.ac.uk/~twk/fellow.pdf

I think a few other places in the UK (Warwick? Imperial College London?) might offer one postdoc position a year under a similar format (any subject, best candidate wins)??

share|improve this answer
add comment

Your Answer


&lt;|im_end|&gt;Take the tour ×
  1. Let V be a Nuclear space (not necessary Frechet, but complete). Let V^* be the dual space considered with the weak topology (i.e. pointwise convergence). Is it true that $V^*$ is also nuclear?

  2. Is it true that the map to the double dual $V \to V^{**}$ is a linear isomorphism (not necessary continuously invertible)?

  3. Let $W$ be a space like $V$. Is the map $V^* \hat \otimes W \to Hom(V,W)$ is a linear isomorphism? Here $V^* \hat{ \otimes} W $ is the completed tensor product and $Hom(V,W)$ is the space of continuous linear maps. If yes what topology does it induce on $Hom(V,W)$? If not what are the kernel and the image of this map?

  4. The same questions for different kinds of duals.

share|improve this question
Many of your questions are answered in Section 10a of the book by Kevin Costello and Owen Gwilliam “Factorization algebras in perturbative quantum field theory” (math.northwestern.edu/~costello/factorization_public.html) –  Dmitri Pavlov Nov 22 &#x27;11 at 20:20
add comment


Your Answer



Browse other questions tagged or ask your own question.&lt;|im_end|&gt;Take the tour ×

I am working with a numerical application where some known techniques solve $\Delta u=\rho$ for $\rho(x,y)\geq0$ defined on a planar rectangle (given as the density of a large pointset). Since the application is related to transportation problems, I suspect that solving Monge-Ampere $\det</pre>

右文（仅阅读辅助）：

<pre>(D^2 u)=\rho$ (with the same boundary conditions) may work better. Hence, the following questions.

  1. What are the most striking differences between the two PDEs ? It would be useful to have examples of $\rho$ leading to very different solutions, and to identify general properties of individual solutions that differ between the two equations. For example, do solutions of</pre>

### 位置8674185｜high_activation｜z=1.014071

上下文8478，目标offset=219，目标token="1"；原文档未知。

包含目标的模型可见前文：

<pre>&#x27;m looking to write a script (running on linux) that connects to an Exchange inbox (as me) and downloads messages. Is there any open source software out there to support me?


share|improve this question
Does your Exchange server support &quot;standard&quot; protocols like POP3 or IMAP, or does it only support Outlook clients? –  Massimo Jun 5 &#x27;10 at 16:41
Sadly outlook only :-( –  Bosh Jun 5 &#x27;10 at 16:56
What you will want to look for is a MAPI command-line client then since it doesn&#x27;t support POP or IMAP. –  jftuga Sep 25 &#x27;10 at 13:07
add comment

closed as not constructive by mgorven, Antoine Benkemoun, Bryan, mdpc, John Gardeniers Feb 16 at 7:22


3 Answers

the openchangeclient cli tool does that. Check the screencast: http://www.dailymotion.com/video/x1</pre>

右文（仅阅读辅助）：

<pre>ul95_openchangeclient-screencast_tech

The instructions on how to create a mapi profile: http://tracker.openchange.org/projects/openchange/wiki/HowTo_Setup_OpenChange_Client

It&#x27;s still beta software, though.

share|improve this answer
add comment

I don&#x27;t think there is anything open source to do that, as Exchange native protocols are Microsoft</pre>

### 位置10185486｜random｜z=0.0528896

上下文9955，目标offset=361，目标token=" manuscript"；原文档未知。

包含目标的模型可见前文：

<pre>shire by Edward Peacock F.S.A. Published by the English Dialect Society 1877. (first edition)

Freakonomics by Steven D. Levitt and Stephen J. Dubner. Published by William Morrow. 2005

*I am British and proud, the last sentence is mere self effacing humour - one of our more admirable national traits.

O*rig&quot;i*nal (?), a. [F. original, L. originalis.]


Pertaining to the origin or beginning; preceding all others; first in order; primitive; primary; pristine; as, the original state of man; the original laws of a country; the original inventor of a process.

His form had yet not lost All her original brightness. Milton.
&lt;-- #sic. &quot;her&quot; refers to form, apparently considered feminine in gender. --&gt;


Not copied, imitated, or translated; new; fresh; genuine; as, an original thought; an original process; the original text of Scripture.


Having the power to suggest new thoughts or combinations of thought; inventive; as, an original genius.


Before unused or unknown; new; as, a book full of original matter.

Original sin Theol., the first sin of Adam, as related to its consequences to his descendants of the human race; -- called also total depravity. See Calvinism.


© Webster 1913.

O*rig&quot;i*nal, n. [Cf. F. original.]


Origin; commencement; source.

It hath it original from much grief. Shak.

And spangled heavens, a shining frame, Their great Original proclaim. Addison.


That which precedes all others of its class; archetype; first copy; hence, an original work of art, manuscript</pre>

右文（仅阅读辅助）：

<pre>, text, and the like, as distinguished from a copy, translation, etc.

The Scriptures may be now read in their own original. Milton.


An original thinker or writer; an originator.


Men who are bad at copying, yet are good originals. C. G. Leland.


A person of marked eccentricity.


5. Zool. &amp; Bot.

The natural or wild species from</pre>

## Feature 11364，h_V=1

### 位置1709678｜high_activation｜z=0.1693682

上下文1670，目标offset=904，目标token=" to"；原文档未知。

包含目标的模型可见前文：

<pre> relative risk (95% confidence interval) comparing the highest to the lowest quintile (Q5 vs. Q1) was 0.25 (0.07-0.87; Ptrend=0.02) for lethal cancer. Among all the cases, higher adiponectin concentrations predicted lower prostate cancer-specific mortality (hazard ratio, HR Q5 vs. Q1=0.39; 0.17-0.85; Ptrend=0.02), independent of body mass index (BMI), plasma C-peptide (a marker of insulin secretion), leptin, clinical stage and tumor grade. This inverse association was apparent mainly among men whose BMI ≥25 kg/m2 (HR Q5 vs. Q1=0.10; 0.01-0.78; Ptrend=0.02), but not among men of normal weight (Ptrend=0.51). Although the correlation of leptin concentrations with BMI (r=0.58, P &lt;0.001) was stronger than that of adiponectin (r=−0.17, P&lt;0.001), leptin was unrelated to prostate cancer risk or mortality.
Higher prediagnostic adiponectin (but not leptin) concentrations predispose men to a lower risk of developing high grade prostate cancer and a lower risk of subsequently dying from the cancer, suggesting a mechanistic link between obesity and poor PCa outcome.
PMCID: PMC2858593  PMID: 19910504
Adiponectin; obesity; prostate cancer; risk; survival
13.  Prospective Study of Determinants and Outcomes of Deferred Treatment or Watchful Waiting Among Men With Prostate Cancer in a Nationwide Cohort 
Journal of Clinical Oncology  2009;27(30):4980-4985.
To examine consequences of deferred treatment (DT) as initial management of prostate cancer (PCa) in a contemporary, prospective cohort of American men diagnosed with PCa.
Participants and Methods
We evaluated deferred treatment for PCa in the Health Professionals Follow-up Study, a prospective study of 51,529 men. Cox proportional hazards models were used to calculate hazard ratios (HRs) for time to eventual treatment among men who deferred treatment for more than 1 year after diagnosis. HRs for time to metastasis or death as a result of PCa were compared between patients who deferred treatment and those who underwent immediate treatment within 1 year of diagnosis.
From among 3,331 cohort participants diagnosed with PCa from 1986 to 2007, 342 (10.3%) initially deferred treatment. Of these, 174 (51%) remained untreated throughout follow-up (mean 7.7 years); the remainder were treated an average of 3.9 years after diagnosis. Factors associated with progression to treatment among DT patients included younger age, higher clinical stage, higher Gleason score, and higher prostate-specific antigen at diagnosis. We observed similar rates for development of metastases (n = 20 and n = 199; 7.2 v 8.1 per 1,000 person-years; P = .68) and death as a result of PCa (n = 8 and n = 80; 2.4 v 2.6 per 1,000 person-years; P = .99) for DT and immediate treatment, respectively.
In this nationwide cohort, more than half the men who opted for DT remained without treatment for 7.7 years after diagnosis. Older men and men with lesser cancer severity at diagnosis were more likely to remain untreated. PCa mortality did not differ between DT and active treatment patients.
PMCID: PMC2799054  PMID: 19720918
14.  Activated networking of platelet activating factor receptor and FAK/STAT1 induces malignant potential in BRCA1-mutant at-risk ovarian epithelium 
It is essential to understand the molecular basis of ovarian cancer etiology and tumor development to</pre>

右文（仅阅读辅助）：

<pre> provide more effective preventive and therapeutic approaches to reduce mortality. Particularly, the molecular targets and pathways involved in early malignant transformation are still not clear. Pro-inflammatory lipids and pathways have been reported to play significant roles in ovarian cancer progression and metastasis. The major objective of this study was to explore and determine whether platelet activating factor (PAF) and receptor associated networking pathways might significantly induce malignant potential in</pre>

### 位置3266329｜high_activation｜z=0.1674151

上下文3192，目标offset=419，目标token=" could"；原文档未知。

包含目标的模型可见前文：

<pre>602 (1st cohort p=0.07; 2nd cohort p=0.10), and DRB1*0701 (1st cohort p=0.03; 2nd cohort p=0.07) alleles and measles-specific antibody levels. Suggestive, yet consistent, associations were observed between the B7(1 st cohort p=0.01; 2nd cohort p=0.08) supertype and higher measles antibody levels in both cohorts. Also, in both cohorts, the B*0801 and DRB1*0301 alleles, C*0802 and DPA1*0202 alleles, and DRB1*1303 alleles displayed consistent associations with variations in IFN-γ, IL-2 and IL-10 secretion, respectively. This study emphasizes the importance of replicating HLA associations with measles vaccine-induced humoral and cellular immune responses and increases confidence in the results. These data will inform strategies for functional studies and novel vaccine development, including epitope-based measles vaccines. This is the first HLA association replication study with measles vaccine-specific immune responses to date.
PMCID: PMC3288791  PMID: 22285888
Measles vaccine; HLA genotypes; Haplotypes; Antibodies; Cytokines; Replication study
12.  Associations Between Demographic Variables and Multiple Measles-Specific Innate and Cell-Mediated Immune Responses After Measles Vaccination 
Viral Immunology  2012;25(1):29-36.
Measles remains a public health concern due to a lack of vaccine use and vaccine failure. A better understanding of the factors that influence variations in immune responses, including innate/inflammatory and adaptive cellular immune responses, following measles-mumps-rubella (MMR) vaccination could</pre>

右文（仅阅读辅助）：

<pre> increase our knowledge of measles vaccine-induced immunity and potentially lead to better vaccines. Measles-specific innate/inflammatory and adaptive cell-mediated immune (CMI) responses were characterized using enzyme-linked immunosorbent assays to quantify the levels of secreted IL-2, IL-6, IL-10, IFN-α, IFN-γ, IFN-λ1, and TN</pre>

### 位置4148031｜random｜z=0.00908992

上下文4054，目标offset=216，目标token=" dol"；原文档未知。

包含目标的模型可见前文：

<pre>, and sulfur are often thought of as secondary elements. Plants and soil may not need large supplies of these nutrients, but the roles they play prove as essential to growth as those of nitrogen, phosphorus, and potassium.

Calcium serves several critical functions and concentrates primarily in leaves. It builds the cell walls of plant tissues and neutralizes acids produced by plants as toxic by-products of metabolism. It regulates the availability of other nutrients, builds plant proteins, and prevents magnesium toxicity.

Your tomato plant&#x27;s upper leaves yellow from a calcium deficiency. That symptom differs from a lack of nitrogen, which causes yellowing of lower leaves. Stems of tomato plants that lack calcium feel soft to the touch, and fruits exhibit blossom-end rot. The roots grow short and display a brown rather than a fleshy color.

Red patches appear on pea leaves when calcium levels are inadequate. The patches appear near the centers of the leaves and eventually spread to the outer margins. The plants lack vigor and appear dwarfed.

Limestone is the most widely used calcium-rich material. When purchasing limestone, shop for dol</pre>

右文（仅阅读辅助）：

<pre>omitic limestone because it contains magnesium as well as calcium. Bone meal, oyster shells, wood ashes, and compost are other natural sources, the latter two materials supplying it the fastest.

The next secondary element that you should familiarize yourself with is magnesium. Photosynthesis would be impossible without magnesium because chlorophyll depends on its presence. Magnesium aids in a plant&#x27;s use of other nutrients,</pre>

### 位置4421332｜random｜z=0.01031062

上下文4321，目标offset=370，目标token=" ("；原文档未知。

包含目标的模型可见前文：

<pre> completed. (Bug #10938
     (http://bugs.mysql.com/10938), Bug #9996 (http://bugs.mysql.com/9996),
     Bug #11623 (http://bugs.mysql.com/11623))
   * A column that can be NULL was not handled properly for WITH ROLLUP in a
     subquery or view. (Bug #12885 (http://bugs.mysql.com/12885))
   * Within a transaction, the following statements now cause an implicit
     ALTER PROCEDURE, CREATE PROCEDURE. This corrects a problem where these
     statements followed by ROLLBACK might not be replicated properly.
     (Bug #12870 (http://bugs.mysql.com/12870))
   * Simultaneous execution of DML statements and CREATE TRIGGER or DROP
     TRIGGER statements on the same table could cause server crashes or
     errors. (Bug #12704 (http://bugs.mysql.com/12704))
   * If a stored function invoked from a SELECT failed with an error, it
     could cause the client connection to be dropped. Now such errors
     generate warnings instead so as not to interrupt the SELECT.
     (Bug #12379 (http://bugs.mysql.com/12379))
   * A concurrency problem for CREATE ... SELECT could cause a server crash.
     (Bug #12845 (http://bugs.mysql.com/12845))
   * The server incorrectly generated an Unknown table error message when for
     attempts to drop tables in the INFORMATION_SCHEMA database. Now it
     issues an Access denied message.
     (</pre>

右文（仅阅读辅助）：

<pre>Bug #9846 (http://bugs.mysql.com/9846))
   * The server allowed privileges to be granted explicitly for the
     INFORMATION_SCHEMA database. Such privileges are always implicit and
     should not be grantable. (Bug #10734 (http://bugs.mysql.com/10734))
   * The server allowed TEMPORARY tables</pre>

### 位置4767338｜random｜z=0.09563777

上下文4659，目标offset=602，目标token=" an"；原文档未知。

包含目标的模型可见前文：

<pre> Barcelona, Spain

  • Sigrid Seelmeir,

    Affiliation: Max von Pettenkofer Institute, Gene Center, LMU Muenchen, Muenchen, Germany

  • Olivier Coux,

    Affiliation: Centre de Recherche en Biochimie Macromoléculaire, Montpellier, France

  • Zsolt Ruzsics,


  • Christopher M. Wiethoff,

    Affiliation: Department of Microbiology and Immunology, Loyola University Medical Center, Maywood, Illinois, United States of America

  • Eric J. Kremer


  • Published: March 19, 2010
  • DOI: 10.1371/journal.ppat.1000808


Viruses use cellular machinery to enter and infect cells. In this study we address the cell entry mechanisms of nonenveloped adenoviruses (Ads). We show that protein VI, an internal capsid protein, is rapidly exposed after cell surface attachment and internalization and remains partially associated with the capsid during intracellular transport. We found that a PPxY motif within protein VI recruits Nedd4 E3 ubiquitin ligases to bind and ubiquitylate protein VI. We further show that this PPxY motif is involved in rapid, microtubule-dependent intracellular movement of protein VI. Ads with a mutated PPxY motif can efficiently escape endosomes but are defective in microtubule-dependent trafficking toward the nucleus. Likewise, depletion of Nedd4 ligases attenuates nuclear accumulation of incoming Ad particles and infection. Our data provide the first evidence that virus-encoded PPxY motifs are required during virus entry, which may be of significance for several other pathogens.

Author Summary

Viruses exploit cellular functions during entry and exit of cells. To redirect cellular functions for their own purpose, viruses encode high-affinity binding sites for key-cellular factors. One such domain is the PPxY motif, which is present in structural proteins of several, mainly enveloped viruses. This motif binds to ubiquitin ligases of the Nedd4 family and recruits their function to sites of virus budding from cells. Here we show that adenoviruses also encode a PPxY motif in the internal structural protein VI and that the PPxY motif has an unprecedented function in virus entry. Adenoviruses with mutations in the protein VI PPxY motif undergo normal endosomal uptake and membrane penetration but have reduced infectivity, altered intracellular targeting and lack efficient gene-delivery. We also find that protein VI is ubiquitylated by Nedd4 ligases in a PPxY dependent manner following partial capsid disassembly and displays rapid intracellular movement. Depletion of Nedd4 ligases also alters virus movement within cells during entry and reduces viral infectivity. Given that PPxY motifs are important for virus exit our findings might have uncovered an</pre>

右文（仅阅读辅助）：

<pre> additional function for PPxY motifs in virus entry, potentially expanding the significance of PPxY motifs and functionally related domains for viral replication.


Many viruses use the microtubule network of the host cell for transport to their site of replication (i.e. the nucleus) [1]. Access to the microtubule network is achieved through recruitment of cytoplasmic dynein motor</pre>

### 位置5501720｜random｜z=0.006221267

上下文5377，目标offset=386，目标token="ow"；原文档未知。

包含目标的模型可见前文：

<pre>ire serial bus.
 189The DHG-P has an additional automatic fan speed control mode named Smart Fan
 190(TM) III+. This mode is not yet supported by the driver.&lt;|im_end|&gt;pkgsrc-Users archive


Re: cups builds

It seems like we should have OpenSLP 2.0.0

Possibly. Do you have a patch for updating the package? :)

Perhaps a different year for me, and you aleady have lots on your list.

and D-Bus 1.7.0

No. From the homepage:
The current stable branch is D-Bus 1.6.x. This is the recommended version for 
most purposes.
The current development branch is D-Bus 1.7.x, which will lead to a 1.8.x 
stable branch in future.

We usually avoid development versions in pkgsrc.

Yes- the label is &quot;stable&quot; but every day I receive a message from package vulnerabilities about dbus. It would seem that if it was fixed then that would also go back to dbus 1.6 but I am not sure.

One more question, though- if things like D-Bus 1.7 were included in something like /usr/pkgsrc/devel, would it or would it not lead to more secure versions of cups?

I am certainly willing to return to more primitive methods or printing -
but folks not on this or a similar list will not.


Home | Main Index | Thread Index | Old Index&lt;|im_end|&gt;The Truth About Nuclear Power

Tags: nuclear, energy, electricity, united, states, percent, reason, economic, france, between



Fact 1: It isn’t.


Until that time comes, producing nuclear energy remains a very costly business.

The chart above uses data from a 2009 interdisciplinary study at the Massachusetts Institute of Technology to compare the costs of generating a kilow</pre>

右文（仅阅读辅助）：

<pre>att hour of electricity using nuclear, coal, and gas power. Looking at this data, the cost differential is clear—nuclear-powered energy costs 14 percent more than gas to produce a unit of electricity, and it costs 30 percent more than coal. Furthermore, according to Gilbert Metcaf’s recent National Bureau of Economic Research paper on energy, this increased cost of nuclear energy includes a</pre>

### 位置7626151｜random｜z=0.02422664

上下文7453，目标offset=856，目标token=" some"；原文档未知。

包含目标的模型可见前文：

<pre> a new value to already existing key like


i am losing the previous value with key &#x27;d&#x27; i.e &quot;usa&quot; because when i do

print %hash1;

i dont see the value &quot;usa&quot;...how to retain both the values for the same key?

share|improve this question
add comment

4 Answers

up vote 12 down vote accepted

A hash key can only contain a single scalar value, so if that value is a string, you are stuck with one item per key. However, there is nothing stopping you from storing array references (which are also scalars) as the value. To make things easier, you should probably store only array references or strings, and not mix the two:

my %hash1 = (a=&gt;&quot;turkey&quot;, b=&gt;&quot;india&quot;, c=&gt;&quot;england&quot;, d=&gt;&quot;usa&quot;);

# upgrade all values to arrays
# $hash1{$_} = [$hash1{$_}] for keys %hash1;   # a way with `keys`
$_ = [$_] for values %hash1;  # a better way with `values`, thanks to ysth

push @{ $hash1{d} }, &#x27;australia&#x27;;

print &quot;$_ : @{ $hash1{$_} }\n&quot; for keys %hash;
share|improve this answer
$_ = [$_] for values %hash1 –  ysth Apr 7 &#x27;11 at 16:16
@ysth =&gt; nice, I forgot that unlike keys which returns copies, values returns a list of lvalues. –  Eric Strom Apr 7 &#x27;11 at 19:33
add comment

you need to store a hash of lists

example: http://www.perlmonks.org/?node_id=1977

share|improve this answer
There&#x27;s no such thing as a hash of lists. –  friedo Apr 7 &#x27;11 at 15:56
@friedo language is flexible. It&#x27;s reasonable that he means a hash that stores arrays instead of simple scalars as values. –  Axeman Apr 7 &#x27;11 at 15:59
@friedo: And just what is it that arrays hold if not lists, eh? Seems to me that having to always recite the full litany of “a hash of scalars holding references to arrays holding lists of scalars of unknown content type” is a mite wordy. It’s hard to be too hard on those who leave a few bits of that out in casual conversation. A “hash of arrays” is perfectly fine, as Perl has no other implementation of the same, and a “hash of lists” is but one step removed. Indeed, the same argument for relaxed speech applies there, as there is no other way to do it. –  tchrist Apr 7 &#x27;11 at 16:52
@frido, I disagree. JohnSmith&#x27;s statement isn&#x27;t wrong, it&#x27;s just useless. It simply repeats Siddharth&#x27;s question without suggesting how one would go about storing a list in a hash element. His link, on the other, shows how a reference to an array can be used to store that list. –  ikegami Apr 7 &#x27;11 at 18:54
@Axeman, yes, language is flexible, but in certain cases language must be precise. In programming we have very specific definitions for words that would otherwise be synonymous in everyday language. And in Perl particularly, arrays and lists are two very different things. –  friedo Apr 7 &#x27;11 at 21:25
show 1 more comment

As JohnSmith said, use a hash of array:

my %hash1 = (
    a =&gt; [&quot;turkey&quot;],
    b =&gt; [&quot;india&quot;],
    c =&gt; [&quot;england&quot;],
    d =&gt; [&quot;usa&quot;],

and use it as:

push @{$hash1{d}}, &quot;australia&quot;;
share|improve this answer
add comment

This question is precisely equivalent to asking whether if we first assign a variable that can hold only one value some</pre>

右文（仅阅读辅助）：

<pre> particular value, but then later assign that same variable a different value, whether we can ever access the earlier value that we&#x27;ve just now overwritten.

The same answer applies to both: no, of course not, not without changing around your storage class, access mechanism, or both. One means one. When you have come up with a mechanism that works for a simple unsubscripted scalar variable, you</pre>

### 位置10155516｜high_activation｜z=0.1762042

上下文9926，目标offset=67，目标token=" to"；原文档未知。

包含目标的模型可见前文：

<pre> by the drama.&lt;|im_end|&gt;Skip Menu

The Population Health Approach

Based on Healthy People 2010 the MPH Program in Health Services has a population health approach that focuses on the interrelated conditions and factors that influence the health of populations over the life course, identifies systematic variations in their patterns of occurrence, and applies the resulting knowledge to</pre>

右文（仅阅读辅助）：

<pre> develop and implement policies and actions to improve the health and well-being of those populations.

The goals of a population health approach are:
  • to maintain and improve the health and health-related quality of life of the entire population
  • to reduce and eventually eliminate disparities in health and quality of life of population groups defined by gender, race or ethnicity, education or income, disability, geographic location, or</pre>

## Feature 11940，h_V=1

### 位置1340887｜random｜z=0.05533794

上下文1310，目标offset=519，目标token="iting"；原文档未知。

包含目标的模型可见前文：

<pre>led and warped from their conservative routes.  There&#x27;s plenty of conservative &quot;Democrats&quot; that abstain or have no where else to turn to, as they saw the old New England Republican guard leave them.

The party will do itself a service to appeal to them, while coming up with NEW policy ideas, instead of recycling those we&#x27;ve used since the 80&#x27;s.

Otherwise, were going to lose a generation of voters, and well feel the effects far longer.

Going down my Facebook there were a lot of sadness and bitterness at the outcome last night.  But almost everyone (of my young generation) was finding solace in ME voting for equality, of people being able to expand on conservative values.  These are young Conservatives mind you.  The current party, especially here in MA, needs to take their lead.  

Demographics and change demand it, unless we like hovering between 10-15% the electorate, and sitting in a corner bitching and yelling at clouds.  

[ Parent ]
It&#x27;s A Matter Of Re-Branding (5.00 / 1)
Ryan, it&#x27;s always been my contention that Massachusetts Republicans need to re-brand themselves as either the conservative (classical) liberals or the liberal (classical) conservatives as a way to re-launch itself before the voters.

Doing so would position us more securely in the Bay State since it not only is a liberal state but it is proud of its heritage. Remember that our country was forged in the fires of revolution against the status quo &amp; that Massachusetts was a leader in our nation&#x27;s birth as a beacon of political liberalism. Republicans sometimes forget that reality.

The Republican Party of Lincoln was also born in the spirit of liberalism with regards to its abolition of slavery, the passage of the Homestead Act, &amp; making Thanksgiving a national holiday. Teddy Roosevelt&#x27;s GOP reigned in monopolies, pushed the environmental movement, &amp; successfully passed laws that gave women the right to vote.

Given the fact that the leadership of today&#x27;s Democrat Party has embraced the ethos of the French Revolution (&amp;, in the process, rejected the liberal patrimony of the American Revolution), it&#x27;s now up to today&#x27;s GOP leadership to adapt the essential practical ideology of the Founding Fathers &amp; adapt it to the realities of today&#x27;s voters in Massachusetts.

Not in the South.

Not in the Midwest.

Not in the West Coast.

Those other sections of the country have their own unique expressions of conservatism.

We need to develop a conservatism for New England in general &amp; for Massachusetts in particular. Uniting</pre>

右文（仅阅读辅助）：

<pre> fusion conservatism with the (updated) practical ideology of the Founding Fathers &amp; re-branding it as a more authentic form of liberalism will put the GOP in a better position to fight the Democrats &amp; their profoundly reactionary politics.

To make all this happen, a group of Republican activists need to host a series of salons to talk/debate about the details. It would be nice if the GOP State Committee</pre>

### 位置4465994｜high_activation｜z=0.2062169

上下文4365，目标offset=22，目标token=" HT"；原文档未知。

包含目标的模型可见前文：

<pre> with the kinetics of MxA expression, TULV replicated only inefficiently in HUVECs, whereas HT</pre>

右文（仅阅读辅助）：

<pre>NV-infected cells produced high titers of virus particles that decreased after 48 h postinfection. Both hantavirus species, however, could replicate equally well in Vero E6 cells, which lack an IFN-induced MxA response. Thus, delayed induction of antiviral MxA in endothelial cells after infection with HTNV could allow viral dissemination and contribute to the pathogenesis</pre>

### 位置4470107｜high_activation｜z=0.2003575

上下文4369，目标offset=39，目标token=" HT"；原文档未知。

包含目标的模型可见前文：

<pre>V-, infected endothelial cells. Addition of angiopoietin-1 (Ang-1) or sphingosine-1-phosphate (S1P) to ANDV- or HT</pre>

右文（仅阅读辅助）：

<pre>NV-infected cells blocked VE-cadherin internalization in response to VEGF. These findings are consistent with the ability of Ang-1 and S1P to inhibit hantavirus-induced endothelial cell permeability. Our results suggest that pathogenic hantaviruses disrupt fluid barrier properties of endothelial cell adherens junctions by enhancing VEGFR2-VE-cadher</pre>

### 位置4472284｜high_activation｜z=0.1993809

上下文4371，目标offset=168，目标token=" HT"；原文档未知。

包含目标的模型可见前文：

<pre>antavirus (i.e., a virus with no associated human disease), was also mediated by introducting recombinant αIIbβ3 or αvβ3 integrins into β3-integrin-deficient CHO cells. In addition, PH infectivity was not inhibited by αvβ3-specific sera or vitronectin but was blocked by α5β1-specific sera and the integrin ligand fibronectin. RGD tripeptides, which are required for many integrin-ligand interactions, are absent from all hantavirus G1 and G2 surface glycoproteins, and GRGDSP peptides did not inhibit hantavirus infectivity. Further, a mouse-human hybrid β3 integrin-specific Fab fragment, c7E3 (ReoPro), also inhibited the infectivity of HT</pre>

右文（仅阅读辅助）：

<pre>N, SEO, and PUU as well as HPS-associated hantaviruses, Sin Nombre (SN) and New York-1 (NY-1). These findings indicate that pathogenic HPS- and HFRS-causing hantaviruses enter cells via β3 integrins, which are present on the surfaces of platelets, endothelial cells, and macrophages</pre>

### 位置5287783｜random｜z=0.006265679

上下文5168，目标offset=280，目标token="Harry"；原文档未知。

包含目标的模型可见前文：

<pre> it always reached out to him and called him back. Something in the boarded up corner house wanted him there, even in the midst of all the gentrification and the onslaught of yuppies. It was white flight in reverse. The park across from the brownstone was filled with children, mostly white; an odd thing in Harlem. Harlem belonged to him, to his people now. As he slowed and pulled up to the curb, he had a feeling that one day he’d own this house. What he didn’t know was that this brownstone would come to own him.

Freedom, as he was known by the hip-hop world, was born Harry Hudson on the coldest October night New York had experienced in over one hundred years. “I’m not going to let the Devil steal my joy,” his mother, Earlene, had said as she tried to start the engine of her old Chevy. The pain came suddenly and passed just as quickly. By the time she reached the hospital, she could feel Harry trying to make his way here. She drove up to the emergency room, blowing her horn and screaming in the Southern accent that had long been replaced by Brooklynese. The emergency room attendants who ran out to help her were shocked to see the crown of the boy’s head on her seat.

“That boy always knew how to make his own way,” Harry’s mother would say later.

Harry</pre>

右文（仅阅读辅助）：

<pre> never knew his father, and was raised by his mother and grandmother, who instilled in him a fierce independence. As a young boy, Harry always felt, even if it was not apparent to those around him, that he’d been born to do something major. He had no idea what that something was, but he knew he had to be ready. Thankfully, he was good at just about everything</pre>

### 位置5338990｜random｜z=0.06510357

上下文5218，目标offset=336，目标token=" neglect"；原文档未知。

包含目标的模型可见前文：

<pre>, to which different individuals and groups have imparted different meanings.&quot; What progressives need to do is reclaim these terms from an Administration that has corroded their meaning. It&#x27;s time to stand up for a redefined and affirmative vision of national security and US foreign-policy. The good news: there&#x27;s a real political opening for a credible and alternative progressive security policy. And as John Powers observed recently in a provocative piece in the LA Weekly, &quot;Money and organization can only take any political movement so far.&quot; Ideas matter.

We know what not to do. The New Republic&#x27;s Peter Beinart recently argued that Democrats should adopt a get-tough crusade, launching a &quot;war against fanatical Islam.&quot; But this strategy not only buys into the GOP&#x27;s fear-mongering and militarized approach to the threat of terror, it is more likely to give life to Bin-Ladenism than it is to liberate people in the Islamic world or serve to protect America&#x27;s security.

The muscular crusade against terrorism that some in the Democratic Party see as the only way to stop Islamic terrorism-and win votes--ignores the fact that it was previous crusades that helped create bin Laden in the first place. Crusades masquerading as foreign policy will weaken our security and divert precious resources from the real fight for hearts and minds in the Middle East and beyond.

Instead of engaging the Republicans on their terms, progressives need to have a debate framed by our own concerns and values. And fighting terrorism should not be the alpha and omega of America&#x27;s security policy. Yes, Al-Qaeda remains a threat, but it&#x27;s a plain fact that &quot;terrorism&quot; is not a menace meriting hysteria or neglect</pre>

右文（仅阅读辅助）：

<pre> of other national priorities; nor is the &quot;Global War on Terror&quot; a compelling justification for US aggression around the world.

&quot;Islamic fundamentalism is actually on the wane in much of the world,&quot; Fareed Zakaria, editor of Newsweek International, recently argued on the Sunday chat show ABC&#x27;s This Week. Islamic fundamentalism &quot;does not have the kind of appeal that worldwide Communism did</pre>

### 位置5541811｜random｜z=0.007730523

上下文5416，目标offset=575，目标token=" ISO"；原文档未知。

包含目标的模型可见前文：

<pre>I was looking at this Whirlpool Forums thread, and there doesn&#x27;t seem to be anything on there lower than 50. Then looking at the beautiful film, this blog mentions that there was Kodak film that went down to a phenomenal 6 ISO!

The main reason I&#x27;m asking is because if we could set our cameras to a much lower ISO, we could all do daytime long-exposures without ND Filters. Oh, and I&#x27;m sure there&#x27;s some other purposes for it too. Maybe.

share|improve this question
This may be relevant: photo.stackexchange.com/questions/3789/… –  rm999 Apr 14 &#x27;11 at 6:17
Also see: photo.stackexchange.com/questions/9051/… for further background... –  Jay Lance Photography Apr 14 &#x27;11 at 6:43
Also, yes you could make the sensor less sensitive. But then it would be less sensitive all the time, you&#x27;d be crippling the low light performance for the sake of longer exposures in daylight. Not a good trade off when you can simply screw on an ND filter. –  Matt Grum Apr 14 &#x27;11 at 10:21
Thanks for the referrals, all. Slightly annoyed that those others didn&#x27;t come up both when searching, nor within the &quot;suggested similar questions&quot; section when you post the question. Nevermind - Thanks for the help, all. –  nchpmn Apr 14 &#x27;11 at 23:47
add comment

marked as duplicate by Matt Grum, John Cavan, PearsonArtPhoto, Itai, ahockley Apr 14 &#x27;11 at 15:57


3 Answers

up vote 4 down vote accepted

This is down to the way digital sensors work. This tutorial is a good introductory article on the way digital sensors work.

For the purposes of illustration, think of the light cavity as a bucket. Let&#x27;s assume that a well exposed image at the sensor&#x27;s base ISO of 100 will fully fill the light cavity of a photosite. Therefore, going from ISO 100 to ISO 200 will halve the exposure time and will only half fill the light cavity. Each stop of increment in the ISO speed will result in the corresponding halving of the amount of light filling the cavity. This is why you have a usable ISO range on digital cameras, e.g. the light cavity is full at base ISO and it is &quot;almost empty&quot; or filled to the minimal amount that is usable at maximum ISO.

With most cameras, you get a usable ISO range of about 6-7 stops which corresponds to an ISO range of ISO 100 - ISO</pre>

右文（仅阅读辅助）：

<pre> 6400. Camera manufacturers are free to shift the sensitivity window of the sensor to any value they like. The reason most cameras choose to have ISO 100 - ISO 6400 is because it&#x27;s the most useful range for a wide variety of photography as opposed to a camera that went from ISO 6 - ISO 400. It&#x27;s also doesn&#x27;t</pre>

### 位置6260000｜random｜z=0.03483013

上下文6118，目标offset=522，目标token=" Gallery"；原文档未知。

包含目标的模型可见前文：

<pre> there are the actual regulations.

Except in Quebec, where the rules are quite different, when an account is held jointly between two individuals, both hold an equal, undivided share. In practice, however, the parent controls the assets, is entitled to any income and pays the necessary taxes on it.

It&#x27;s only when the parent dies that things can get confusing. Was the money intended as a gift for the child named on the joint account? Or, was the joint account set up simply for ease of administration, and the parent&#x27;s intention was to have the money divided equally among other family members?

In the past, the presumption was usually that the joint account was destined to be a gift. Now, however, thanks to two recent court cases, assets held jointly by a parent and an adult child no longer automatically fall into the child&#x27;s hands when the parent dies.

In fact, the onus is now clearly on the adult child to prove his or her entitlement, particularly if other family members see things otherwise. If anything, it&#x27;s now presumed that the money goes into the estate unless there is substantive evidence to the contrary.

&quot;The courts are now taking the view that when an adult child holds an asset jointly with Mom and Dad, there needs to be some proof beyond the mere ownership to show that the child was supposed to receive the asset as a gift after the parent&#x27;s death,&quot; explains Jean Blacklock, author of The 50 Biggest Estate Planning Mistakes.

In the first case, a father put nearly $1 million into joint ownership with his daughter and also gave her power of attorney. She could take money out but not without asking.&lt;|im_end|&gt;Moving to SDK packages (slowly)

I have been developing add-ins for Visual Studio since the first Visual Studio .NET 2002 version. But, as you already know if you are long-time reader of my blog, add-ins have become now second-class citizens in the Visual Studio Extensibility (VSX) ecosystem, something that manifests in the following facts:

- Minor enhancements of the automation code model (EnvDTE*.*, EnvDTE80, VSLangProj*.* etc.). The last Visual Studio versions, while have shipped new assemblies EnvDTE90.dll, EnvDTE100.dll, etc., they have provided very little new functionality.

- The code model (EnvDTE.ProjectItem.FileCodeModel) has lacks and bugs (that I reported at Microsoft Connect) that are not going to be fixed.

- Add-ins can not use the VSIX deployment mechanism, nor the Visual Studio Gallery</pre>

右文（仅阅读辅助）：

<pre> as packages can. They remain in a separate Add-In Manager, rather than the new Extension Manager.

- Add-ins suffer a lot when Microsoft decides to change some internal implementation (the VS 2010 release, which changed Office-based commandbars by WPF-based ones was specially painful, I had to report tons of bugs). The reason is Microsoft doesn&#x27;t use add-ins (only packages),</pre>

## Feature 12249，h_V=2

### 位置337703｜high_activation｜z=0.2933524

上下文330，目标offset=0，目标token="\n\n"；原文档未知。

包含目标的模型可见前文：

<pre>

</pre>

右文（仅阅读辅助）：

<pre>The solution most often found in airports is to restrict access to the PC itself - placing it within a lockable case or kiosk.

Alternatively, epoxy resin is pretty good for sealing ports, whether or not they have a plug inserted (remember you will need to seal all ports an attacker could access)

share|improve this answer
+1 for epoxy resin –  Lucas Kauffman Feb 1</pre>

### 位置376598｜high_activation｜z=0.2933524

上下文368，目标offset=0，目标token="\n\n"；原文档未知。

包含目标的模型可见前文：

<pre>

</pre>

右文（仅阅读辅助）：

<pre>To view the final USE setting as seen by Portage, run emerge info. This will list all relevant variables (including the USE variable) with the content used by Portage.

# emerge info
Package specific USE-flags Viewing available USE-flags

In the next chapter on Portage and Software we will explain how to manage your installed software and how to work with emerge. However, we will</pre>

### 位置867402｜random｜z=0.1078055

上下文847，目标offset=760，目标token=":\n\n"；原文档未知。

包含目标的模型可见前文：

<pre> opt-out clause for catholic institutions back in 2009.

&quot;Let’s honor the conscience of those who disagree with abortion and draft a sensible conscience clause,” Obama told students, faculty and staff during his commencement speech.

&quot;So there are two ways to understand it, either as a betrayal or a radical disagreement between the Obama administration and Notre Dame on what&#x27;s ‘sensible,’” Snead added.

Many people say it’s simply insensible to have women pay up to $90 a month for birth control. Yet students, faculty and staff say it’s a trade off for attending the prestigious institution.

&quot;If I went to another university, I would have been able to have birth control an easier way, but it wouldn&#x27;t have been the same environment and I wouldn&#x27;t have liked it as much,” Notre Dame Sophomore Ann Marie Kelly said.

&quot;Of course the coercive force of the government is very much in play here and they will punish us severely if we don&#x27;t violate our religious conscious,” Snead concluded.

An April study done by the Guttmacher Institute found 98 percent of sexually active catholic women have used contraceptives banned by the church. However, Notre Dame says most Catholics, regardless of their personal views, are outraged that the government would interfere with their religion’s sanctity.

If you’d like to read Father Jenkin’s full three-page letter to the Obama administration, just click on the Big Red Bar.

powered by Disqus
User Agent: CCBot/2.0 - 130737293&lt;|im_end|&gt;recent on-air advertisers

Now Playing

News/Talk Radio, WOKV
Where Jacksonville Listens ...

Pigs on the Loose

There once was a piggy named Wiggy. Well, several of them actually. Wiggy and his siblings, also named Wiggy, belong to this family in Darwin, Australia. But they&#x27;re naughty little pigs, and often wandered into traffic. They caused so much chaos local authorities got involved... tracking the porkers on a wild... ah.... pig chase. Sadly, two of the Wiggies met their fate at the end of a shotgun. For now the family is keeping a close eye on the remaining Wiggy.
Team Traffic

Avoid Traffic Delays

Tip Line: (904) 245-8672&lt;|im_end|&gt;Own a piece of Windows Phone history that almost was - the Sony Ericsson Julie

Sony Erricson Julie Prototype




Julie Prototype QWERTY keyboard Windows Phone 7



Source: eBay Nl



There are 65 comments. Sign in to comment

jlynnm350z says:

Cool if you could get it for the right price. . . Like $1.50

Laura Knotek says:

Would it actually work, or would it just be a paperweight?

Sam Sabri says:

That&#x27;s the gamble. 

Sledgehamma says:

In the ebay description he says, that it is fully functional.

alex6272 says:

I like the IE and what appears to be games/Xbox tiles. This is obviously a very early build of the OS

I would buy it, but the auction is not in English... If I could figure out how much it costs and the shipping I would buy it right now!

willied says:

The second half of the description is English. Also, change the .nl in the link to .com to view it on the main eBay site. I&#x27;m not sure they ship to the US, though.

DJCBS says:

It&#x27;s going on auction. At the moment the highest bid is 31€. The seller only ships to Europe for 13€ (shipping costs)

goldenpipes says:

</pre>

右文（仅阅读辅助）：

<pre>I really hope someone on xda gets this puppy and comes up with a way to update it to windows phone 7.8

duoFurious says:

LED charge light...notification light??? Why sony. Someone do this on WP finally

Waucckhewww says:

HTC 7 pro/arrive has one

Nakazul says:

HTC phones,</pre>

### 位置908593｜high_activation｜z=0.2933524

上下文888，目标offset=0，目标token="\n\n"；原文档未知。

包含目标的模型可见前文：

<pre>

</pre>

右文（仅阅读辅助）：

<pre>DRtg: 100

Net DRtg: -1.9

WAM: 95.70 (3)

Scouting: 92.2 (4)

WAMS: 95.06


Speed and Athleticism: 18.7

Hill is one of the fastest players in the league, end to end, recording a </pre>

### 位置3181458｜random｜z=0.2005789

上下文3109，目标offset=445，目标token="\n\n"；原文档未知。

包含目标的模型可见前文：

<pre> the city and immediate suburbs.[citation needed]
  • Some younger speakers have picked up features of the first stages of the Northern Cities shift; this vowel shift causes, among other changes, raising and tensing of the vowel /æ/, so that words like cat /kæt/ to become more like [kɛət]. A corridor of communities between Chicago and St. Louis is the only place that features of the Inland North have penetrated noticeably into the Midland, despite the long boundary the two regions share. However, St. Louis remains a Midland city in other respects. For example on rhymes with dawn rather than don, unlike the North. Indeed, the fact that on rhymes with dawn is more distinctive in St. Louis than in the rest of the Midland, since the cot–caught merger is prevented in St. Louis by the presence of the Northern Cities shift.


Cincinnati has a phonological pattern quite distinct from the surrounding area (Boberg and Strassel 2000).

The traditional Cincinnati short-a system is unique in the Midland. While there is no evidence for a phonemic split, the phonetic conditioning of short-a in conservative Cincinnati speech is similar to that of New York City, with the raising environments including nasals (m, n, ŋ), voiceless fricatives (f, soft th, sh, s), and voiced stops (b, d, g, t). Weaker forms of this pattern are shown by speakers from nearby Dayton, Springfield, and Mansfield. Boberg and Strassel (2000) reported that Cincinnati&#x27;s traditional short-a system was giving way among younger speakers to a nasal system similar to those found elsewhere in the Midland and West.


  1. ^ {http://webspace.ship.edu/cgboer/dialectsofenglish.html
  2. ^ Labov et al., pp. 255–258 and 262–265.
  3. ^ Labov, pp. 262–268.
  4. ^ Labov et al., p. 263.&lt;|im_end|&gt;Phase velocity

</pre>

右文（仅阅读辅助）：

<pre>From Wikipedia, the free encyclopedia
Jump to: navigation, search



Or, equivalently, in terms of the wave&#x27;s angular frequency ω, which specifies the number of oscillations per unit of time, and wavenumber k, which specifies the number of oscillations per unit of space, by






the amplitude becomes a sinusoid with phase speed of vg = Δωk.</pre>

### 位置4136223｜random｜z=0.1390555

上下文4042，目标offset=692，目标token="\n"；原文档未知。

包含目标的模型可见前文：

<pre> 2003
    The spyro legacy is desecrated by this uninspired &quot;trainwreck of a game&quot;. The developers responsible should be locked up and forced to play this glitchy, frustrating and half-baked tripe until their thumbs are bloody stumps and they have completely lost their sanity. Who cares about the fancy water ripples and flame effects when the frame rate is worse than ps1 versions and the game locks up each time you play it. Worst sequel ever. Full Review »&lt;|im_end|&gt;User Score

Mixed or average reviews- based on 527 Ratings

User score distribution:

Review this movie

  1. Your Score
    0 out of 10
    Rate this:
    • 10
    • 9
    • 8
    • 7
    • 6
    • 5
    • 4
    • 3
    • 2
    • 1
    • 0
    • 0
  1. Submit
  2. Check Spelling
  1. May 27, 2011
  2. May 26, 2011
  3. Jun 3, 2011

  4. May 27, 2011
  5. Jun 26, 2011
  6. Jun 3, 2011

    Wait for DVD
  7. May 30, 2011
  8. May 27, 2011
  9. May 26, 2011

    gain, but not anytime soon.

  10. Sep 27, 2011
  11. Jun 16, 2011
  12. May 27, 2011
  13. Jun 3, 2011
  14. Jul 26, 2011
  15. Jun 10, 2011
  16. May 27, 2011
  17. Jun 5, 2011
  18. Jun 4, 2011
  19. Mar 22, 2012
  20. Jul 10, 2011
  21. BKM
    Jan 14, 2012
  22. May 28, 2011
  23. May 31, 2011
  24. Jun 5, 2011
  25. dz9
    Jul 27, 2011
  26. Dec 28, 2011
  27. Dec 26, 2011
  28. Jan 31, 2012
  29. Mar 11, 2012
</pre>

右文（仅阅读辅助）：

<pre>  30. May 28, 2011
  31. May 31, 2011
    THE MOVIE WAS GREAT i really like it, one of my friends asked me yesterday if they have to watch the first one before seeing tis one. i dont think its neccc , i mean the idea is the same , but</pre>

### 位置8239331｜random｜z=0.1351492

上下文8053，目标offset=194，目标token="\n"；原文档未知。

包含目标的模型可见前文：

<pre>21548682 1421548682
ISBN-13: 9781421548685 9781421548685

In this volume, Claudio reminisces about when he was a young, insecure waiter just getting his feet wet. Vanna gets to the bottom of why Teo&#x27;s stubborn lack of ambition prevents him from living up to his full potential in the kitchen. A woman running a streak of bad luck finds cheer when Gabriella introduces her to the magical ambience of Casetta dell&#x27;Orso. And finally, a mysterious young woman arrives with an important message for Lorenzo.


Add this release to
or to&lt;|im_end|&gt;Conuiron (Level 8)

followed by

Kinda self-explanatory isn&#x27;t it?  
Cute anime characters, powered and not.
1. Dan JD
</pre>

右文（仅阅读辅助）：

<pre>2. Near

how can you not love that long white hair and the long sleeves? :D

3. Touma Hashiba

Yes, the archer has made his way here.

4. Hanabusa Aidou

Aside from Zero, Aidou is the second cutest vampire in the series.

5. Archer

Cause he is. ^__^

6. Hagi

</pre>

### 位置8718184｜random｜z=0.2005789

上下文8521，目标offset=217，目标token="\n\n"；原文档未知。

包含目标的模型可见前文：

<pre> from B. Give the new server a new port.

share|improve this answer
I don&#x27;t want to do the same, I want to change commands to something else (i&#x27;m not sure if it&#x27;s possible)... look at bold text in my question. What I mean is that I don&#x27;t want to serve from B. I want A to be server listening for input... and then I want to send file contents from non-listening B to listening A. –  Phil Jan 20 &#x27;10 at 5:51
That&#x27;s not how netcat works. –  DaveParillo Jan 20 &#x27;10 at 15:14
As you can see from accepted answer - yes, that&#x27;s how netcat can work too. –  Phil Jan 21 &#x27;10 at 4:24
You&#x27;re right. I learn something new every day! –  DaveParillo Jan 21 &#x27;10 at 16:10
add comment

Your Answer


&lt;|im_end|&gt;Follow Me on Pinterest

</pre>

右文（仅阅读辅助）：

<pre>An Emerging Rivalry Between Biden and Holder?

You can click on the image to see a larger version of it.

Biden and Holder feud

The judges for this caption would have also accepted Holders insistence on the KSM trial being in New York, or the role of &quot;radical Islam&quot; in terrorism, or accusing Americans of being cowards on race while being part of a political party</pre>

## Feature 13614，h_V=3

### 位置874506｜random｜z=0.01258321

上下文854，目标offset=702，目标token="od"；原文档未知。

包含目标的模型可见前文：

<pre>idin resistance. FEBS Lett 195(1-2):159-63
4) Payne MJ, et al.  (1993) Characterization of a second nuclear gene, AEP1, required for expression of the mitochondrial OLI1 gene in Saccharomyces cerevisiae. Curr Genet 24(1-2):126-35
5) Finnegan PM, et al.  (1991) Characterization of a yeast nuclear gene, AEP2, required for accumulation of mitochondrial mRNA encoding subunit 9 of the ATP synthase. Curr Genet 20(1-2):53-61
6) Devenish RJ, et al.  (2000) Insights into ATP synthase assembly and function through the molecular genetic manipulation of subunits of the yeast mitochondrial enzyme complex. Biochim Biophys Acta 1458(2-3):428-42
7) Boyer PD  (1997) The ATP synthase--a splendid molecular machine. Annu Rev Biochem 66:717-49
8) Nakamoto RK, et al.  (1999) Rotational coupling in the F0F1 ATP synthase. Annu Rev Biophys Biomol Struct 28:205-34
9) Somlo M, et al.  (1977) An oligomycin-resistant adenosine triphosphatase and its effects on cellular growth, mitochondrial oxidative phosphorylation and respiratory proton translocation in Saccharomyces cerevisiae. Biochem J 162(1):51-9&lt;|im_end|&gt;SGD Paper Help

Odat O, et al.  (2007) Old Yellow Enzymes, Highly Homologous FMN Oxidoreductases with Modulating Roles in Oxidative Stress and Programmed Cell Death in Yeast. J Biol Chem 282(49):36010-23

Abstract: In a genetic screen to identify modifiers of Bax-dependent lethality in yeast, the C-terminus of OYE2 was isolated based on its capacity to restore sensitivity to a Bax-resistant yeast mutant strain. Overexpression of full length OYE2 suppresses Bax lethality in yeast, lowers endogenous reactive oxygen species (ROS), increases resistance to H2O2-induced programmed cell death (PCD) and significantly lowers ROS levels generated by organic prooxidants. Reciprocally, oye2 yeast strains are sensitive to prooxidant-induced PCD. Overexpression and knockout analysis indicates these OYE2 antioxidant activities are opposed by OYE3, a highly homologous heterodimerizing protein, which functions as a prooxidant promoting H2O2-induced PCD in wild type yeast. To exert its effect OYE3 requires the presence of OYE2. Deletion of the 12 C-terminal amino acids and catalytic inactivation of OYE2 by a Y197F mutation enhance significantly survival upon H2O2-induced PCD in wild type cells, but accelerate PCD in oye3 cells, implicating the oye2p-oye3p heterod</pre>

右文（仅阅读辅助）：

<pre>imer for promoting cell death upon oxidative stress. Unexpectedly, a strain with a double knockout of these genes (oye2 oye3) is highly resistant to H2O2-induced PCD, exhibits increased respiratory capacity, and undergoes less cell death during the adaptive response in chronological aging. Simultaneous deletion of OYE2 and other antioxidant genes hyperinduces endogenous levels of ROS</pre>

### 位置1451271｜high_activation｜z=0.3875832

上下文1418，目标offset=383，目标token="/t"；原文档未知。

包含目标的模型可见前文：

<pre>. Rule 35
An addenum to the internet meme Rule 34 (if it exists, there is porn of it, no exceptions) that states &quot;The only exception to rule 34 is the citation of Rule 34.&quot;

Ie, there is no porn of someone stating that there is porn of everything.
&quot;Is there anything that hasn&#x27;t been rule 34&#x27;d?&quot;
&quot;Rule 34.&quot;
&quot;See Rule 35.&quot;
rss and gcal&lt;|im_end|&gt;Subscribe Feedback English
look up any word, like hipster:
20. Trill
29. Trill
Trill is a group of ignorant low-lifes that tend to reside in Downtown Albany (229 time) Georgia. This group of neanderthals classify themselves as Emo/Scene kids. They are for the most part seventeen and under in age, and most wear girls jeans followed by there black dyed hair and &quot;Emo hair styles&quot;. Some are characterized with features such as large nose&#x27;s which was never evolved from there prehistoric ancestors. Nor has their mental capasity enlarged or expanded, making them no better than the neanderthals they were once classified as. At least the neanderthals of the past did not wear the opposite sexes clothing.
Rat-face girl and her shrimp for a man. Ignorant &quot;Emo&quot; kids who strive for attention which never become anything more than a common street rat henze their apperance also. The Australians state that Trill is &quot;To give a blowjob to a guy while driving, when there are three girls in the back seat watching on at these events.

Damn girl, i can&#x27;t believe you just gave that guy a Trill!&quot;
30. trill
absolutly discusting
see ya trill and smells like trill
31. Trill
To get drunk/t</pre>

右文（仅阅读辅助）：

<pre>ipsy
32. Trill
that girl is Trilling too hard
The word Trill means to be cool or to have a skrait life moment... it can also be used to mean True Rights In Love and LIfe... this is how i c the word Trill or T.R.I.L.L.
Also it can be made into a plural noun (Trills)
Yeah even</pre>

### 位置1616412｜random｜z=0.01063009

上下文1579，目标offset=740，目标token=" dut"；原文档未知。

包含目标的模型可见前文：

<pre> lives, we were lucky enough to walk away from those moments with only damage to our ego.  

There are disproportionate consequences in life that seem so utterly unfair.  

One moment of giving into emotion without thinking changed this man’s life forever.  Hopefully his story can change yours too. 

Not included in the list of weird excuses these celebrities give for being absent on social media is the one reason I think is probably the most accurate.  They spend their lives being fed lines by people who are more interesting and creative then they are, they have teams dedicated to helping them rehearse what they are going to say during interviews and rarely have to actually come up with interesting things to say on their own.

So…yeah tell us that you stay away from Twitter because you’re afraid of radiation or don’t know how to use a computer.  Whatever makes you feel better about actually just being incredibly dull. 

I love this. 

This summer I was on an airplane coming back from a long vacation and the older woman next to me ended up falling asleep on my shoulder for about 2 hours.  I’m not the most relaxed flyer and for some reason it made me feel better, knowing that I was somehow making it easier for her to sleep…or something?  

Either way, this brought tears to my eyes.  Helping strangers doesn’t always require a lot of time or money, just a small moment of human decency.   

STFU, Men Complaining That A Woman Used Them For A Free Meal

Plenty of people go on blind dates. But it takes a unique personality togo on blind dates just to gorge on restaurant food. Meet Erin, a 24-year-old struggling actress in Toronto with a 48-restaurant-long hit list, a meagre bank account and a mission to use and abuse Toronto dudes.

Oh, STFU Toronto Life and all the twerps commenting about how they wish they could have taken her out and then did a “dine and dash” to really show her who’s boss. Ugh. Judging from the mini photos of the commenters and the fact that they comment on internet articles, I’m 100% sure they would all do just about anything for the chance to take a girl on a date, let alone a pretty blonde girl.  No one is fooled, internet commenters.

Any woman that’s ever had to sit through a first date dinner KNOWS that even if he picks up the bill, nothing about the dinner was free.  

I’ve had to sit through hours of a guy talking about how wearing a suit everyday made him feel “powerful” and another guy going on about how he could score tickets to anything that comes through NYC because “clients, baby.” I would have rather paid for both of our meals if I could reverse time and take those memories away. 

I personally could never suffer through continuous first dates just for the free meal because the cost of the dinner isn’t worth the cost of my brain cells and time.  I admire women that can take advantage of a situation that’s usually painfully awkward and uncomfortable.  Sorry Men, but until you can figure out what to do about this whole getting paid more for the same job and unfair advantage in the work force thing, you’re gonna have to cough up the money to pay for dinner on a first date.  

Get over it.  We all know why these guys even forked over the money to take this girl out in the first place, no one ever got laid going dut</pre>

右文（仅阅读辅助）：

<pre>ch.   

Toronto Life&lt;|im_end|&gt;DPL Rating:
Rate This:
No votes yet


     This story deals centers mainly around Salomon Sarowitsch, a Russian Jew who lived a fast life from counterfeiting money. He is arrested and sent to a concentration camp where his drawing talent gets him transferred to a concentration camp where he and other Jewish prisoners are interred in</pre>

### 位置2724613｜high_activation｜z=0.3973489

上下文2662，目标offset=840，目标token=",t"；原文档未知。

包含目标的模型可见前文：

<pre> birds had tiny chunks of metal in their beaks or inner ears that enabled them to detect the direction of the Earth’s magnetic field. But more research has thrown doubt on the existence of these so-called ‘compass cells’, saying that they were just a type of white blood cells.

Now a new article in the journal Science suggests that birds have clusters of certain cells dubbed ‘GPS neurons’ in their brains that enable them to navigate.





There’s more about this here.


Skip to comment form

  1. 1


    How did they launch the satellites?

    1. 1.1

      They were sent up long ago by shuttlelaunchiraptors.

  2. 2
    Jared A


    Can you imagine not only being able to experience north and south as directions, but be able to “feel” your location like that?

  3. 3

    I’m having trouble imagining that, it’s completely alien to the senses we’re used to. Kinda like trying to imagine what purple tastes like.

  4. 4
    Doug Little

    I wonder if it would be similar to the feeling of Deja Vu if so you would be constantly feeling like you had been there before.

Leave a Reply

&lt;|im_end|&gt;Search Our Site

Search form


Priests Starve Cats at St. James Church

March 19, 2012 | Cats / TNR / Take Action

Church Groundskeeper Threatens Poisoning as Next Step

Mayor&#x27;s Alliance for NYC&#x27;s Animals






this is a disgrace!!

I agree with all comments thus far. Sherry hits the nail on the head; the cats simply can&#x27;t afford the Catholic Church. Their policies, at best, are/have always been, do as I say, not as I do. And to never question anything. These so called &quot;men of god&quot;, &quot;priests&quot; seem to abide by their own laws with little concern for those truly in need. It is outrageous &amp; disgusting, shame on them all!

I&#x27;m sure St. Francis of Assissi would look kindly on you &quot;Catholic Scum&quot;!

I can&#x27;t believe that someone supposedly of God could treat any living creature inhumanely. It wouldn&#x27;t kill you to show a lil mercy and feed the lil cats. After all, they are one of God&#x27;s creations. They are a living breathing creature with feelings just like you or I. They can&#x27;t possibly be hurting anything by being there.

What hypocrites!!! They live off the donations of parisioners and they refuse to help God&#x27;s creatures. Both priests should be removed. Let&#x27;s start a campaign to rid the city of such heartless men. They have no business taking the handouts of the church while they starve living creatures. They MUST go!!

If they were little boys they wouldn&#x27;t kick them off the property!! What happened to sanctuary!!

To the priest at St James church this is disgusting shame on you but I am not surprised. Priests have abused children and stolen millions from parishes What about the so called blessing of the animals on October 2? I suppose that is hypocritical . There are shelters that would take the cats . Since you want to starve the cats to deadth, why don&#x27;t you starve for lent ?

Find their Facebook page &amp; let the parishioners know what their church does. Also, use the email address provided at the end of the article and give the cats A VOICE. Please, venting here is not directed at them. They don&#x27;t read your posts here at Friends of Animals. If you want to save these cats &amp; expose these sick people make it count &amp; tell them.

And you say you are men of God? I don&#x27;t think so!

All in the name of religion. Animal sacrifices are in part the biggest culprit of why animal abuse is rampid worldwide. We have animal sacrifices in the forms of: slaughterhouses,kosher killing,vivisection,animal experimentations,hunting,fishing,trapping,fur farms where animals are anally eloctrocuted or drowned,factory farms where animals are castrated,t</pre>

右文（仅阅读辅助）：

<pre>ail and ear docked, teeth pulled all without pain meds or anesthesia,animal sports worldwide: bullfighting,rooster fighting,dog fighting,canadian seal hunt where 10&#x27;s of thousands of baby harp seals are clubbed to death and often skinned alive while their wailing mothers sit on the ice helpless,circuses that use animals,the list of horrors of animal sacrifices goes</pre>

### 位置5405060｜random｜z=0.03553243

上下文5282，目标offset=931，目标token=" Te"；原文档未知。

包含目标的模型可见前文：

<pre> as in Quran. It is far back in the throat and made like a K with a glottal click. Okay?

Now it gets to be fun. Gadaffi should probably be spelled pretty much as the New York Times spells it: Qaddafi. The Arabic letter in his name is that guttural Q. But almost all of the classical Arabic words starting with Qs are pronounced as guttural Gs in the Bedouin dialect spoken in North Africa–particularly by the Gadafa tribe to which Gadafi belongs.

If all of these insertions of sounds and differing pronunciations seem strange, just consider our dialects, Bostonian in particular, and the disappearance of the R sound in Harvard and its mysterious re-appearance in their version of Cuba–Cuber.

As for Muammar, I mean Moamer, lets call the whole thing off
2011 Jonathan Dobrer

Libya &amp; the End of the UN


In 1936 a very young, and not yet tarnished by history, Emperor Haile Selassie stood before the League of Nations and cried out for help. Industrialized, and seemingly civilized, Italy was using modern weapons and airpower to slaughter his helpless people. The League of Nations did nothing and in this non-action condemned the people of Ethiopia to death from above and doomed the League to death by immoral passivity, impotence and irrelevancy.

Today, the people of Libya are crying for help. Modern technology, supplied in the past by the Soviet Union, then by Russia and recently and increasingly by NATO powers including, to our shame, the United States, is being used to kill under-armed and untrained civilians. Now, in the 21st Century the United Nations is united only in deadlock and unable to act, not only swiftly, but at all.

As in the violent breakup of Yugoslavia and the genocide against the Bosnians, as in Rwanda and their genocidal slaughter of civilians by tribe, the UN is impotent. Their shameful impotence is by design. Neither Russia nor China will allow the precedent of intervening in the “internal affairs” of another nation. They fear, with some reason, that the UN might be called to get involved with Chechnya or Tibet respectively.

This structural impediment is institutionally deadly and leaves the UN a laughing stock. After all, Libya till last week was on the UN’s Human Rights Commission–even chaired it for a while. I’m caught between laughter and tears. As a one time strong supporter of the UN, as someone who believes both in the democratic process and international law, this is heartbreaking. The UN is left with one legitimate function and that is to be a diplomatic version of a No-Tell Motel where diplomats, who cannot otherwise meet, can slip into a room and talk.

Meanwhile Libyans die. Gadaffi flies in mercenaries from Sub-Saharan Africa, paying them with money he gets from selling oil to Italy and, of course, Great Britain which traded its integrity and the Lockerbie Bomber for a mess of oily potage.

Libyan rebels, protestors, freedom fighters, pro-democracy insurgents (our labels betray our political positions) are calling for help, requesting a no fly zone. We say it isn’t simple–and it isn’t. We say bombing their anti-aircraft sites would be an act of war. And it would be. However, doing nothing, except demanding that it is time for Gadaffi to go, is also a crime against humanity. There is some duty when the virtually defenseless are being slaughtered with weapons we supplied.

No, we should not go in alone. Our coming in alone or with the thin cover of NATO–as in Afghanistan–will lessen the credibility of the rebels and give Gadaffi street cred in the Arab Street. Any effort must truly involve other nations, critically Arab and Muslim nations. This cannot be a mostly white, nominally Christian, ethnically European effort. The various Sub-Saharan African nations are as unlikely to sign on as China and Russia. They fear interventions in their own deplorable internal wars and tribal slaughters.

Any military action must begin with the Arab League calling for intervention and offering arms, aid and troops. This means that in order to stop this most uncivil civil war and level the deadly playing field, the Western World and the Arab World have to choose to cooperate. Whatever we do chaos and pain will follow, but some good could come to all of us if our two worlds reach out towards one another.
2011 Jonathan Dobrer&lt;|im_end|&gt;Jennifer Te</pre>

右文（仅阅读辅助）：

<pre>fft On The Satellite: Same Staff, Same Vibe, I&#x27;m Back

Categories: News

Soon to be known as the Satellite

August Brown at L.A. Times posts an interview with the Satellite&#x27;s Jennifer Tefft, the booker who left Spaceland about a year ago but who is back now that the location is transitioning to a new name and new ownership. As rumors about dec</pre>

### 位置7715366｜high_activation｜z=0.3875832

上下文7541，目标offset=58，目标token="/t"；原文档未知。

包含目标的模型可见前文：

<pre>/sycophants shouldn&#x27;t be scrutinized, as if to overtly, extremely take a public position that they shouldn&#x27;t &#x27;automatically be presumed guilty.&#x27;

That would be, kinda like if one were to go out of his/her way to presume that a repeat pedophile/rapist/t</pre>

右文（仅阅读辅助）：

<pre>orturer/murderer should NOT be not suspected.

Sure, even the worst among us shouldn&#x27;t automatically be accused, even with a verifiably bad, bad, baddie, bad, bad history. But, just as in any investigation, it always starts with circumstantial evidence pointing in one direction or another.

And as such, these events? Kinda always seem to involve the</pre>

### 位置9130773｜random｜z=0.009897668

上下文8924，目标offset=474，目标token=" st"；原文档未知。

包含目标的模型可见前文：

<pre> is not selected.
  4. Review the other directories that are selected, for example you might want to make sure that the Audiobooks directory is unselected.
  5. OK!
share|improve this answer
add comment

Your Answer


&lt;|im_end|&gt;
Subject: [fw-wiz] Microsoft exchange Server Scenario
From: lists (listsbrianburns.net)
Date: Sun Apr 02 2000 - 17:42:20 CDT

Forgive me if this has recently been brought up. I need some best practice information for the following scenario using Microsoft Exchange Server:

I have several thousand users on Exchange Server. Approx half of these users need to access their mailbox from the protected LAN/WAN segments as native MS Exchange clients using Outlook. The exchange servers are members member of the internal NT domain. The admin group only wants to create a single account for each mail user, and not have to maintain seperate directories (based on the outcome of these questions, this may be able to change)

The other half of my users need to access their mail accounts from the internet via standard POP3/SMTP protocols. A VPN is not logistically feasable for this purpose.

I am using Checkpoint FW-1 with a DMZ.

How should I architect my mail infrastructure and still maintain some semblance of security? Any advice/criticicism/help would be very much appreciated.


Brian Burns&lt;|im_end|&gt;Register Log in

Scientific Method / Science &amp; Exploration

Suspended animation becomes a reality?

An interesting experiement reported on this past week put mice into state of …


The study involved exposing mice to H2S in concentrations up to 80 ppm, and that the effect is in direct relationship to the concentration of the gas. The mice take fewer breaths, from 120 per minute to less than 10, their metabolic rate and movement slows dramatically, and their core body temperature decreases from around 38?C to near 15?C. In effect, the mice were operating at about 10% their normal rate. Better yet, after 6 hours of exposure the mice were normal once returned to normal air.

H2S can inhibit one of the enzymes in the electron transport chain, thereby stopping or slowing down cell respiration to a point of near st</pre>

右文（仅阅读辅助）：

<pre>asis, it appears. The authors of the study can see practical applications for this:

&quot;We think this could be of great benefit for many situations in medicine... ...It should work the same for us as it did in mice. We have the same basic chemistry.&quot;

I?m intrigued by the possibilities this offers. I think it may well be a while before we see it tested on humans, but should</pre>

### 位置9177127｜random｜z=0.02063986

上下文8969，目标offset=774，目标token="re"；原文档未知。

包含目标的模型可见前文：

<pre> a tidy conclusion in 3 years or less. President Obama solved this problem by declaring that we are getting out of Iraq, then quietly pursuing a plan that is hard to distinguis from Bush&#x27;s &quot;come home after success&quot; plan. But I digress.

Darren Lenard Hutchinson said...


The Taylor article you cite is NOT a discussion of Sotomayor&#x27;s body of judicial opinions. And I have referenced discussions of them -- primarily at the SCOTUS blog. The blog has published a 4-part series on her judicial opinions. The thought she is a judicial leftist is baseless. She has ruled against many discrimination plaintiffs, and she even ruled against the Center for Reproductive Rights. Rosen&#x27;s Reviewers Suddenly Get Names! The Rici case does not change this. The Second Circuit panel AND the full Second Circuit were split on the ruling, and I suspect that the Supreme Court will rule 5-4 on the matter. Perhaps you believe the 4 liberals are raging lefties, but that is a distortion.

Second, on the particular point that Taylor makes, I wrote an essay on that one too. Before rushing to judge Sotomayor on race and gender politics, you should include Scalia, Ginsburg, O&#x27;Connor, and Kennedy in that analysis too: Strikingly Similar: Comparing Sotomayor&#x27;s Views on Sex and Race With Statements By O&#x27;Connor, Ginsburg, Scalia and Kennedy.

Finally, with respect to your rhetorical question about Janice Rogers, asking Obama to pick her is about as ridiculous as someone having asked Bush I to appoint Thelton Henderson rather than Clarence Thomas. Clearly ideology matters in judicial appointments. People who deny this are either ignorant of history or simply playing politics. Earth to Obama: Your Supreme Court Choice Is SUPPOSED to Galvanize Republicans

Aeneas said...

I didn&#x27;t listen much to the pundits re: O&#x27;s speech. Actually, the only one I read was TOTUS and rolled on the floor laughing. Yeah... THAT echo was amazing. Nothing like your own words coming back at you a second later. Very bracing, I am sure.

Anyway, as I said, I didn&#x27;t listen to the pundits and didn&#x27;t listen to the two speeches (O vs. C) in their entirety. Soar throat, couldn&#x27;t yell at the screen; as for actually reading the speech--not with my butterfly attention span.

So... my conclusion (besides the awesome echo that reflected really the effect of the speech; I&#x27;ll say no more): from where I sat on the couch, working on a Ricola honey and herb drop, Mr.O sounded to me like he was playing defense against the very aggressive Mr. C, who had no echo and didn&#x27;t play pinpong with his head. AS you said--Mr. O attacked Bush (yes, it&#x27;s getting very, very old. Soon we&#x27;ll see it on SNL) then defended what he was doing which was (gasp!) the same stuff as Bush. I opt for hypocrisy also.

Bottom line--for Heaven&#x27;s sake, Mr. President, chose ONE path that you believe--YOU, not the ACLU, or the pundits, or your old buddies, or Cheney, or Reid, or whoever, but one that YOU have confidence in--will CONTINUE (note the word continue; I am of the opinion, that whatever we want to call the Bush Administration, there were no terrorists attacks)to keep us secure and confident in our government that it can keep us secure. Right now, I have no confidence whatsoever. Confidence is half the battle.

The speech was a study in... well... cynical politics. Period.

I am a bit digusted.

Darren Lenard Hutchinson said...

Aeneas: i learned a long time ago to read thre</pre>

右文（仅阅读辅助）：

<pre> transcripts the video later (if necessary).


Aeneas said...

TOTUS--Teleprompter Of The United States.

It has a blog and reports the behind the scenes scene as it travels with the President. It&#x27;s a hoot. Really. TOTUS even twitters. Ha!

I guess it appeals to my sense of the absurd.

KaJo said...

Absurdity is failing to</pre>

## Feature 13830，h_V=0

### 位置843510｜random｜z=0.02489058

上下文824，目标offset=382，目标token=" or"；原文档未知。

包含目标的模型可见前文：

<pre> a voice in further development of the LambdaRail, rather than just a user who must deal with the management decisions of the vendor.


Chair Twomey asked if there were other questions or comments. Trustee Halverson moved to approve the motion, stating that he had a lot of confidence in the administration and faculty’s evaluation of the issue. Further, he thought the financial obligation was acceptable. Trustee Solano seconded the motion. The other committee members, with the exception of Trustee Kendrick, were in favor of joining the consortium. Trustee Kendrick said she would like to consider funding the LambdaRail but wanted to ensure the quantification of other such decisions. Therefore, she voted against the motion. The motion was passed by a majority vote.

Investment Policy

Regarding the investment policy, Vice President Shuman said the University had devolved from state system as of July 1 of last year and was thus able to do its own investing. State law required an investment policy that coincided with Florida statutes. She announced that Mr. Michael Neglia, previously employed with Winn Dixie, had been hired as the University treasurer, and said he could help answer any questions about the policy. Trustee Halverson noted that it was a fairly conservative investment plan and said he had no difficulties with it. Chair Twomey agreed, as did Trustee Douglas and Trustee Solano. Trustee Douglas moved to approve the plan and Trustee Solano seconded the motion. It was approved unanimously.

Treasurer’s Report

Vice President Shuman said she had promised to provide snapshot reports to trustees when she was hired. This was a draft of one such report and indicated how much cash the University had, how much was invested, the percentage of debt bond, etc. She said that currently the University was doing quite well at matching investment versus debt. She asked if the trustees had suggestions or</pre>

右文（仅阅读辅助）：

<pre> changes they would like to recommend.


Chair Twomey asked if the cash amount included that held by housing and for other purposes. He asked if it was consolidated cash for the entire University and if it included money from the UNF Foundation. Ms. Shuman replied that the cash amount reflected the entire university operations, not including Foundation. He also wanted to know if the report could include E&amp;G</pre>

### 位置1151481｜high_activation｜z=0.1913945

上下文1125，目标offset=409，目标token=" IS"；原文档未知。

包含目标的模型可见前文：

<pre> you will, which you have been dwelling on. I&#x27;ve been trying to form it up into a more cohesive, integrated... GS: Try to make it quick, we&#x27;re running out of time. Go ahead.

RG: Yeah. To expose the ethos of the, you know, it&#x27;s like the Neocons serve as the pseudo-intellectual rationale for the Illumi-Nazi agenda. And I don&#x27;t presume that it turns on such fine distinctions, so much as it is a bare-knuckled lust for power. But, everybody has sort of a worldview that they use to justify their actions. And of course, it&#x27;s a most un-conservative, humanistic social engineering agenda on a far larger scale. Now you mentioned about these people, basically, and it&#x27;s as rare as hen teeth... GS: Quick, Roger... RG: ...yeah, to find somebody that&#x27;s not oxymoronically both a spiritualist and an occultist, and also a, what do you call, a hardcore rationalist. Or maybe that&#x27;s just [a] Republican assumption, right? SV: (sighs) GS: (slight laughing in delivery): I know there was a question in there somewhere, Roger... RG: Yeah. GS: But anyway, thanks for calling. Let me, I&#x27;ve only got a minute. I&#x27;ve got to finish with Svali. Svali, tell us in your own words, you&#x27;ve got about a minute or two left here. You went forward, you came forward, (bumper music begins) you&#x27;re now living a life completely away from them. What&#x27;s your hopes of the future in our country right now? SV: My hope is that people will realize that this is happening, and that they will start doing something about it - that they will start looking at it. Now again, we&#x27;re talking about people who are mentally wealthy, but it won&#x27;t be easy. But if people could rise up in prayer, and just say, &quot;THIS IS</pre>

右文（仅阅读辅助）：

<pre>N&#x27;T OKAY&quot;... If people would become informed enough to learn more about it, be aware they exist... and then, possibly, PRAY. Pray that people will take action against the things that are happening. Because these people... GS: Okay, Svali, I&#x27;m... SV: Okay. All right. GS: We&#x27;re all out of time. We&#x27;re going to end</pre>

### 位置1789240｜random｜z=0.09569137

上下文1748，目标offset=636，目标token=" whose"；原文档未知。

包含目标的模型可见前文：

<pre> with watching human evolution is that we have a fairly long life span. Exactly the same life span, on average, as the researchers working in this field. Bacteria, plants and some insects however, have a much faster life cycle and are therefore much better suited to this sort of study. If we can watch one DNA based life form give rise to a different species due to the random errors in copying its DNA, then other life forms with the same basic DNA and the same ability to introduce random errors when it is copied will do the same.

Evolution can said to be established as fact on two different set of observation, a little extra redundancy for you there. Firstly, the definition of evolution, the scientific definition and not a straw man definition put forward by those who deny this fact with the purpose of trying to cast doubt, is


This can very easily be measured by taking samples from people of different generations and seeing if there has been any change of the frequency of alleles. This frequency does change.

Now, please allow me, as you have specifically asked for this information, to include another quote without returning to your &quot;are you just an unthinking photocopier&quot; insult? If I wrote it in my own words you would claim it was my mere speculation and I want to make it absolutely, without one shadow of an iota of a hint of a doubt, that I am taking this from scientific papers and not making things up in an attempt to annoy or bait you. Therefore I need to include some quotes. Okay?


Examples of a new species being observed -

1) Plants




There are many more, but lets move onto animals.

2) Animals



There are many more, but I don&#x27;t wish to bore you.

The number of experiments with Fruit Flies are too numerous to quote at length, but should you wish to research them see - Dobzhansky and Pavlovsky (1971) and (Dobzhansky 1972), Thoday and Gibson (1962), Thoday and Gibson (1970), Crossley (1974), (Rice 1985, Rice and Salt 1988 and Rice and Salt 1990). The advantage with fruit flies is that you can study a large number of generations in a single career.

I&#x27;ll give the last word to Theodosius Dobzhansky who expresses the feeling of many biologists when he says &quot;...evolution as a process that has always gone on in the history of the earth can be doubted only by those who are ignorant of the evidence or are resistant to evidence, owing to emotional blocks or to plain bigotry&quot;

I hope that helped?


*** EDIT *** PS You might find Google Scholar useful for checking the references I mentioned - see

In reply to an earlier post on 3 Mar 2012 09:41:22 GMT
K. Moss says:
Hi Silver.

You do get &quot;all sorts&quot; here. I know that my posts are not exactly a model of remorseless logic and scrupulous academic credentials, but sometimes there are individuals whose</pre>

右文（仅阅读辅助）：

<pre> attitude towards others so utterly invalidates any claim to truth, that you wonder why they cannot see it.

Bert is such a one. Indeed, he betrays a harshness and degree of arrogance towards (all) others here that, when he does start spouting JW dogma, it just sounds like white noise, without real substance.

And, he loves to jump to premature conclusions about people</pre>

### 位置1992655｜random｜z=0.02122847

上下文1947，目标offset=478，目标token=" household"；原文档未知。

包含目标的模型可见前文：

<pre> Obama supply air support? Is the United States ready for another huge military effort in a region difficult to supply? How will we know which rebels to trust? How do we sort out all the conflicting aims of various Arab nations in the region regarding Syria? Will it be possible for the United States to avoid sending soldiers to Syria but still “captain” a European-Arab team? What will a post-Assad government look like? Can it possibly be unified? Will Iran become more powerful? Haven’t our soldiers suffered enough?




Do not post the following:

  • Potentially libelous statements or damaging innuendo.
  • Obscene, explicit, or racist language.
  • Personal attacks, insults or threats.
  • Comments unrelated to the story.&lt;|im_end|&gt;Demographic Data Questionnaire

A demographic data questionnaire is used by government to establish specifics about the population. Most of the most common demographic categories in such questionnaires include ethnic origin, race, age and sex. The data generated from such surveys is then used for planning purposes. Common categories in the demographics data include population, where age, sex, race, marital status and education level is considered. Households are also a common category where the total households are considered for purposes of getting the average household size in a specific community. In the income category things such as household income, net worth, per-capita income and disposable income are considered.

Below is a sample.


Street address_______________________




Marital status: Married____ Single_____ Divorced_______ Separated_______

Q1. What is your education level?

High school diploma

Bachelor’s degree

Master’s degree


Q2. What is your average annual household income?

Below $50,000

Between $50,000 and $100,000

Between $100,001 and $200,000

Above $200,000

Q3. How many people live in your house?

Just me

Between 1 and 3

Between 4 and 6

More than six

Q4. Of people living in your household, how many are dependent on you?

(Please specify)_______________

Q5. What is your combined household income $_________

Q6. What is the amount of disposable income available in your household</pre>

右文（仅阅读辅助）：

<pre>? $________

Q7. How would you rate the net worth of your household? $_____

Q8. What is the per capita income in your household? $_______

Q9. What is the median home value of your current residential house? $_______

Q10. Your current residential house is:



Not purchased but does not pay rent either

Under mortgage

Category: Social</pre>

### 位置2736508｜high_activation｜z=0.1894414

上下文2674，目标offset=466，目标token=" IS"；原文档未知。

包含目标的模型可见前文：

<pre> guilty thats why he took the coward way out!thanks nbc for getting those sick bastards caught and put in jail where they belong! burn in hell conradt

NBC guilty?? So because the child molestor kills himself, obviously knew he had broken the law and KNEW he wouldn&#x27;t survive in prison, did the weak thing and killed himself. So NBC is guilty because there are child molestors out there? Seriously?

I think anyone who thinks NBC is guilty obviously sides with the pedophiles and child molestors out there. You can&#x27;t blame a show for catching people who are breaking the law. I wish they would stay back on and put more of these disgustin low life creatures in prison where they belong.

A lot of you keep saying &quot;the show outed a paedophile and this woman won the jackpot.&quot;

You&#x27;re missing the point entirely.

The show, not the police, not the prosecutors, but the show was the one that &quot;researched&quot; the crime. We only have the TV shows word that he was guilty. We only have their side of the story.

Now, as for &quot;only guilty people kill themselves&quot;. Imagine if you were called a paedophile on (inter)national TV. How would you feel? How would your family react? How would your neighbours? They showed his house, so how would strangers react and know where you lived?

And keep in mind, he&#x27;s hadn&#x27;t been found guilty. Perhaps he was a paedophile. Perhaps he thought he was talking to another adult that was role playing. Perhaps it wasn&#x27;t him at all.

Whatever the case, the police are the ones in charge of gathering the facts, and the courts are the place for guilt to be assigned. This abomination of a TV show bypassed both of those.

I&#x27;m glad they had to pay.

I think it is very clear what those potential sex offenders were up to. I have seen many episodes of Dateline To Catch A Predator. If those girls had really been underage those men were clearly going to have sex with those young girls and boys. Chris Hansen clearly has a sincere motive to catch predators. He is trying to prevent these guys from taking advantage of young girls in the future. SEXUAL PREDATORS NEED TO BE CAUGHT. TAKING THAT SHOW OFF AIR IS</pre>

右文（仅阅读辅助）：

<pre> LIKE OPENING THE DOOR TO SEXUAL PREDATORS.

It&#x27;s unfortunate that people kill themselves due to embarrasment and sickness. However, what about the poor &quot;children&quot; that lives are RUINED because an ADULT decides to have sex with someone, sometimes, as young, or younger than their own kids!! This is a perverted world and it will take God to come down</pre>

### 位置4061775｜random｜z=0.04686324

上下文3969，目标offset=916，目标token="ers"；原文档未知。

包含目标的模型可见前文：

<pre> indicating film positioned on the top surface of the PCB. The top surface location measures the cavity pressure distribution. Separately, the pressure indicating film may be placed on the top or bottom of the substrate to measure mold wall contact pressure.

Three steps are involved in transfer molding with pressure indicating film, as described below.

Step 1: Mount the multilayer stack on the PCB and insert it into the mold cavity
Step 2: Close the mold cavity and preheat the PCB and the EMC pellet
Step 3: Depress the plunger to press the epoxy molding compound into the cavity.

For cavity pressure measurements, injecting the polymer on top of the multilayer causes immediate, permanent pale red color changes on pressure distribution Figure 2the pressure-indicating film. These color variations can be compared to a color calibration chart to determine their psi and kg/cm2 equivalents. Digital scanning with software processing is also available to convert the differing intensities of red on the film to a spectrum of colors corresponding to the local pressures. The digitally processed film (2b) shows a uniform cavity pressure distribution between 120-140 bar. Only areas distant from the gate show pressures below 100 bar.

For mold wall-to-substrate pressure measurement, the sensor film placed on the upper or lower surface of the PCB measures the contact pressure between the upper or lower mold walls and the PCB. Frictional movements between the top mold wall and the PCB leave red markings directly on the PCB surface. These verify the complete uniform contact needed to prevent the EMC from flowing out upon the substrate, causing what is referred to as “mold flash.”

pressure distribution Figure 3Although no polymer is injected below the PCB, controlled pressure is required there to avoid damage to the solder pads. Figure 3 shows that no solder pads rise above the solder-resist surface. As the measured pressure is lowest at the top of the pads, the mold tool is not contacting the pads, only the solder resist between the pads.

In summary, Pressurex sensor film is now proven to be appropriate for characterizing the encapsulation of microelectronic systems. Correct characterization of this process is essential for further quality and reliability improvements. The methods presented here allow developing and monitoring stress-minimized encapsulation processes. They provide a firm basis for enhancing the reliability of polymer encapsulated microelectronic and micro-electromechanical (MEMS) systems. 

Share this Story

The password field is case sensitive.&lt;|im_end|&gt;Electronic Component News

Product Releases

Non-contact power steering torque sensor saves fuel
Mon, 12/03/2012 - 12:56pm

TT electronics’ new non-contact power steering torque sensor uses less current and is smaller and lighter than existing solutions, helping to make electronic power steering systems more compact, reliable and efficient. 

Designed to sense very small differential angles, the new TT electronics SX-4428 Magnetorque II non-contact steering torque sensor is based on Hall Effect technology. The innovative free-floating torque rotor within the device offers infinite rotational life. The lack of torque rotor friction means it does not wear out as in previous devices thus improving reliability and extending product life expectancy.

The new sensor from TT electronics enables the end user to program output levels and reduce the use of tight tolerances in the steering shaft, thereby reducing shaft machining costs. The compact packaging and lightweight construction mean both space and weight are saved in the overall steering system.  Supply current is less than 21mA, which contributes to system efficiency.

The smaller packaging and internal structure has enabled TT electronics to reduce the amount of plastic used in the SX-4428 by 42%. The sensor fits with TT electronics’ philosophy of reducing waste and unnecessary packaging, as well as helping its customers achieve their environmental goals.

Operational from -40oC to +85oC and resistant to shock and vibration, the new non-contact sensor provides both a technical and environmental solution for demanding advanced electric power steering systems.

For further information and data sheet downloads please visit:  http://technology.ttelectronics.com/industry/category/transportation#



Share this Story

The password field is case sensitive.&lt;|im_end|&gt;EVER since Néstor Kirchner became Argentina&#x27;s president in 2003, he and Cristina Fernández, his wife and successor, have ruthlessly divided and conquered their political rivals. Their biggest remaining adversary is the Clarín Group, the country&#x27;s dominant media conglomerate. The Kirchners</pre>

右文（仅阅读辅助）：

<pre> have tried to cripple the firm after its television stations and Clarín newspaper gave sympathetic coverage to farmers striking over a tax increase in 2008. During that dispute, the government&#x27;s supporters plastered Buenos Aires with posters accusing the company of lying and of serving landed oligarchs. One year later the state broadcaster enticed Argentina&#x27;s football association to tear up its contract with a Clarín-owned</pre>

### 位置4134948｜high_activation｜z=0.1904179

上下文4041，目标offset=440，目标token="S"；原文档未知。

包含目标的模型可见前文：

<pre> graphics, Carrot Top-caliber annoying sounds, and gameplay that&#x27;s more bland than a sandwich without mayonnaise, is quite simply craptacular.
  17. 42
    Control-wise, I hate the slippery, jittery interaction between character and camera. [Jan 2003, p.52]
  18. 40
    Check Six Studios has clearly designed this installment of the Spyro franchise for very young gamers, and with that demographic, the title works well. Unfortunately, this limited scope will bore anyone familiar with other platforming titles.
User Score

Generally unfavorable reviews- based on 58 Ratings

User score distribution:
  1. Positive: 8 out of 41
  2. Negative: 28 out of 41
  1. Sep 22, 2012
    After the success of the first 3 Spyro games on the PS1, Insomiac decides to randomly abandon the Spyro series. The series is then sold to Universal and the first game they decide to release is Enter the Dragonfly for the PS2 and the Gamecube which is the first time a Spyro game was released on a non Sony console. Some people say the reason why the game is bad has something to do with Universal rushing the game for the holiday season which caused a whole bunch of glitches and bugs to be left alone. I believe there is more to it than that. First off, the game is completely unoriginal. The story is copied from Spyro 1 but except for rescuing dragons, you are rescuing dragon FLIES. Yeah, that&#x27;s totally 100% original. That&#x27;s only the tip of the iceberg. Speaking of ice, Spyro can now breathe ice as well as water, lightning, and water including Spyro&#x27;s trademark, fire. What? Dragons are known for breathing fire. Not ice, water, and lightning. And the worst part is that they don&#x27;t do anything different except breathing water is completely useless. And do you want to know the worst part about this tragedy? THE GAME LOOKS</pre>

右文（仅阅读辅助）：

<pre> JUST LIKE THE PS1 GAMES. The developers showed little to no effort trying to make the game look good, or play good for that matter. This game is bad. I do not understand why Spyro was not put out of his misery instead of keeping Spyro on life support. And sadly, this is not the worst game of the Spyro series. Full Review »
  2</pre>

### 位置10410048｜random｜z=0.0204045

上下文10174，目标offset=826，目标token=" to"；原文档未知。

包含目标的模型可见前文：

<pre> there should be no IQueryable or IEnumerable. –  user414076 Sep 28 &#x27;11 at 14:37
@AnthonyPegram You are right. I removed the .First() from my example to clarify. –  Nils Magne Lunde Sep 29 &#x27;11 at 10:04
add comment

2 Answers

up vote 4 down vote accepted

In general, LINQ extension methods on IQueryable (defined in Queryable) return IQueryables, and the ones on IEnumerable (defined in Enumerable) return IEnumerables. In this particular case, Configurations is a collection (IEnumerable) on the first returned Location object. Therefore the .Select call returns an IEnumerable.

EDIT: To make it all execute remotely, you could try this:

Context.Locations.Where(l =&gt; l.Name == &quot;SomeName&quot;).Configurations

Assuming that your filter on Locations is only going to return one row, you should get the same result. Of course it will be an IQueryable, but that shouldn&#x27;t make a difference. If you need to materialize it, you can do something like:

Context.Locations.Where(l =&gt; l.Name == &quot;SomeName&quot;).Configurations.ToList()
share|improve this answer
That makes kinda sense as Configurations is a collection in the EF. But in the database it is still a separate table. How can I make sure that the entire query will be executed in SQL Server and not in memory? –  Nils Magne Lunde Sep 28 &#x27;11 at 14:47
Try moving the First call further down the stack. I&#x27;ll edit my answer. –  Chris Shain Sep 28 &#x27;11 at 14:51
I will accept this answer because you answered my question. Regarding you suggestions for executing it on the server, it does not work. The result from from Context.Locations.Where(..) does not contain a definition for Configurations since it is of type IQueriable&lt;Location&gt;. I am a little bit concerned about some of my other queries now which are much larger than this. I guess I will have to use SQL Profiler to verify what is actually executed on the server. –  Nils Magne Lunde Sep 28 &#x27;11 at 16:47
For those who are curious: my query, Context.Locations.Where(l =&gt; l.Name == &quot;SomeName&quot;).First().Configurations.Select(c =&gt; c)actually executed in two steps on the SQL Server. First getting the Location, and then using sp_executesqlto get Configurations. By re-writing the Linq query I could get everything executed in SQL Server in one go, which is what I want. –  Nils Magne Lunde Sep 28 &#x27;11 at 18:05
add comment

Basically, IQueryable allows for remote data sources (like SQL Server). It will work against the database, if possible. IEnumerable works with in-memory collections.

So, if you are querying a SQL Server database, you will get an IQueryable. Otherwise it&#x27;ll be an IEnumerable.

This article may further help you.

share|improve this answer
add comment

Your Answer


&lt;|im_end|&gt;Take the tour ×

To compare databases of different vendors (Oracle, SQL Server, DB2, MySQL, and PostgreSQL) how can I identify any object uniquely and do I need a catalog? For instance, In Java&#x27;s DatabaseMetadata I should specify catalog and schema fooPattern at least.

Is it true that catalog is just an abstraction of data storage?

share|improve this question
add comment

3 Answers

up vote 28 down vote accepted

In Oracle:

  • server instance == database == catalog == all data managed by same execution engine
  • schema == namespace within database, identical to user account
  • user == schema owner == named account, identical to schema, who can connect to database, who owns the schema and use objects possibly in other schemas
  • to</pre>

右文（仅阅读辅助）：

<pre> identify any object you need (schema name + object name)

In PostgreSQL:

  • server instance == db cluster == all data managed by same execution engine
  • database == catalog == single database within db cluster, isolated from other databases in same db cluster
  • schema == namespace within database
  • user == named account, who can connect to database, own and use objects in database
</pre>

## Feature 13964，h_V=0

### 位置268571｜random｜z=0.08091328

上下文262，目标offset=461，目标token=" meaning"；原文档未知。

包含目标的模型可见前文：

<pre> Izz al-Din was furious. He took his sons and they demolished the place. He then declared that the Minister had lost his integrity, and would not be acceptable as a witness in court. The King accepted this, and the Minister felt that such a declaration could not affect his position. But he was to realize that it was not so.

It happened that King Ayyoob wanted to send a letter to the Caliph in Baghdad, because although Egypt was fully autonomous, it was still affiliated to the Caliph who approved the appointment of its Kings and Sultans. The King instructed his Minister to write the letter. When the messenger carrying the letter arrived in the Caliph&#x27;s court in Baghdad and delivered his letter, the Caliph asked him whether he personally heard the contents of the letter being read out by the King. The messenger said: &quot;No, but it was given to me by Mueen al-Din, his Minister, personally.&quot; The Caliph said: &quot;But this man has been declared by Izz al-Din as a man of no integrity. As such, we do not accept his report of the King&#x27;s instructions.&quot; The messenger had to go back to Cairo where the King read out the letter to him, and then returned to Baghdad to deliver it to the Caliph.

Thus Izz al-Din&#x27;s character shines before our eyes. He was courageous, firm and dedicated to truth and justice, fearing no authority when he makes a stand for what is right. But what sort of scholar was he? Izz al-Din belonged to the Shafie school of law, but he was a versatile scholar, qualified to exercise ijtihad, or scholarly discretion, in order to establish new rulings on the basis of the Qur&#x27;an and the Sunnah. We have seen how he exercised this in order to check the excesses of the state, and to organise the general mobilization of the people to fight for the cause of Islam. But he also exercised this qualification in many other ways, ruling on numerous questions that were put to him as a judge or a scholar.

Furthermore, Izz al-Din wrote many books in various disciplines. For example, he wrote a complete commentary on the Qur&#x27;an, giving particular attention to linguistic points that make the meaning</pre>

右文（仅阅读辅助）：

<pre> easier to grasp. He wrote also other books in this discipline, but his most valuable work in this area is a book which is given the short title Majaz al-Qur&#x27;an which is highly praised by many scholars. Bibliographies also mention four books by Izz al-Din on hadith subjects, but one of them, which is a summary of the Sahih by Muslim has been lost.</pre>

### 位置1034351｜high_activation｜z=0.431133

上下文1010，目标offset=945，目标token=" Size"；原文档未知。

包含目标的模型可见前文：

<pre> and Thursday, the office atmosphere settles to a more comfortable hubbub, and a conversation you have with a new employee reveals to you a lot about yourself. On Friday, money (that is, the lack thereof) is a prevailing theme, and it falls on you to find ways to save it.

See career horoscope for another sign



You&#x27;ll want to keep a tight grip on your cash today, which may be at odds with your little one&#x27;s big ideas about what&#x27;s necessary to get ready for the holidays. Hang tough -- they really don&#x27;t need all that stuff!



You should get plenty done today -- like a lot of other people -- but your mood just doesn&#x27;t seem to lift very high. Don&#x27;t worry about it, as things should improve in just a few days.



Certain cooking tasks are best left to the professionals. You know this, yet you can&#x27;t help but challenge yourself by taking your skills to the next level. Books and YouTube videos will get you only so far. After that, it&#x27;s time for a class.



So you don&#x27;t want to cut a pair of bangs -- get some clip-on hair instead. Don&#x27;t have time to grow your nails to an elegant length? Hello, silk wraps! There&#x27;s a solution for every style challenge out there if you&#x27;re looking for it.&lt;|im_end|&gt;Smithsonian Digital Repository &gt;
Smithsonian Contributions Series &gt;
Smithsonian Contributions to the Earth Sciences &gt;

Title: Sands in the Alboran Sea: A Model of Input in a Deep Marine Basin
Authors: Stanley, Daniel Jean
Kelling, Gilbert
Vera, Juan-Antonio
Sheng, Harrison
Issue Date: 16-Jun-1975
Citation: Smithsonian Contributions to the Earth Sciences; 15
Abstract: The Alboran Sea, an almost totally land-enclosed, mountain-bounded (Rif, Betic ranges) basin, lies east of Gilbraltar in the westernmost Mediterranean. A petrologic study of the sand fraction in river, river mouth, and beach samples collected on the coast of the Alboran Sea defines the composition and distribution of the principal light and heavy mineral groups along its margins. The investigation details 20 mineralogical provinces on the southern Iberian and northern Moroccan margins and the Strait of Gibraltar sector and identifies the major source terrains and fluvial and marine point sources of terrigenous sediment entering the basin. Significant sample-to-sample changes in the proportion of mineralogical components are attributed to marine processes, particularly nearshore currents, which move sands laterally along the coast and, while so doing, modify the proportions of light and heavy mineral components. Lateral trends observed within Moroccan and Spanish mineralogical provinces provide evidence on the actual sense of nearshore sediment dispersal. Marine transport agents have a more pronounced effect on the light mineral fraction, while even unstable heavy mineral species appear to suffer less modification as a result of the transport in the marine environment. The paths followed by the sands between source terrain and final depositional site in deepwater environments are complex ones. A comparison of mineral assemblages in coastal sands and in sands in deep-sea cores shows a provenance from the Serranía de Ronda complex in the Betic range west of Málaga. After initial deposition on the coast, these river-borne sediments are transported in a southwestward direction toward Gibraltar and then eventually are funneled downslope in a southeastward direction toward the Western Alboran Basin through the Gibraltar Canyon and submarine valley. In geological terms, the Alboran. Sea study can serve as a model for sedimentation in one type of elongate enclosed basin bounded by regions of high relief. Although the geographic and geologic configuration of the Alboran Sea and contiguous land conforms to a multisource basin model, the transport paths of sediment since the late Quaternary have been essentially longitudinal. This longitudinal input, with filling as a result of currents primarily from the Strait of Gibraltar sector, is independent of a major delta source and is thus unlike many elongate, deep-sea basins examined in present oceans and troughs (including flysch) mapped in the ancient rock record.
???metadata.dc.identifier.doi???: 10.5479/si.00810274.15.1
URI: http://hdl.handle.net/10088/805
ISSN: 0081-0274
Appears in Collections:Smithsonian Contributions to the Earth Sciences

Files in This Item:

File Description Size</pre>

右文（仅阅读辅助）：

<pre>Format
SCES-0015.epub2 MBUnknownView/Open
SCES-0015.mobi4 MBUnknownView/Open
SCES-0015.pdf12.74 MBAdobe PDFView/Open
SCES-0015.pdf.txt130.13 kBTextView/Open



DSpace Software Copyright © 2</pre>

### 位置1375137｜random｜z=0.02415059

上下文1343，目标offset=999，目标token=" option"；原文档未知。

包含目标的模型可见前文：

<pre> 29, the 30-year-old was battling to survive in two lawless jails.

He was detained on a minor offence but ended up sharing cells and exercise yards with death row inmates, murderers, gang members, rapists and Louisiana&#x27;s other hardened criminals.

That was frightening enough for the factory hand from Narre Warren in Melbourne&#x27;s south-east, but what made his jail stay a potential life-and-death experience was many of the inmates, in the confusion of the hurricane, had smuggled in deadly weapons.

The New Orleans Parish Prison where he spent the first few days and Baton Rouge&#x27;s Elayn Hunt Correctional Centre, where he was later transferred after Katrina, were overcrowded with inmates and understaffed by wardens.

Most of the prisoners were not searched when they were transferred from New Orleans to Baton Rouge, he said.

&quot;There were a lot of homemade weapons,&quot; McDonald, speaking from the safety of his sister&#x27;s home in Clarksville, Tennessee, told AAP.

&quot;Apparently one guy had a little pistol. I never saw it, but that&#x27;s the rumour that was getting around.

&quot;No one was searched.&quot;

The most terrifying moment came when McDonald and another inmate he had befriended, Robert, were walking in the Elayn Hunt exercise yard.

McDonald heard a voice yelling out to him.

The voice said: &quot;I&#x27;ll have that shirt&quot;.

The icy demand came from an inmate holding a Phillips-head screwdriver.

The inmate walked up to McDonald and pressed the screwdriver into his ribs.

The shirt McDonald was wearing was a New Orleans Parish Prison standard issue garment, so it was not a prized item.

The armed prisoner was likely looking for a fight rather than the shirt.

&quot;I said &#x27;OK. Take the shirt&#x27;,&quot; McDonald chillingly recalled.

&quot;He took it and I virtually ran off.&quot;

Another prisoner was not so lucky.

&quot;I saw one bloke get stabbed,&quot; McDonald said.

The robbery came in the first few days McDonald and the other New Orleans prisoners were transferred to the maximum security Elayn Hunt jail. The inmates were not placed in cells when they arrived at Elayn Hunt, but lived in the facility&#x27;s football field-sized exercise yard.

&quot;They locked us all in a yard with no beds or nothing,&quot; McDonald said.

McDonald&#x27;s horrible ordeal began in the early hours of August 28, when he had one too many drinks in a bar on New Orleans&#x27; infamous party strip, Bourbon Street.

He had just arrived in the city.

When he refused to leave the bar, police arrested him for the minor misdemeanour charge of criminal trespass, and put him in jail.

&quot;I just had a couple too many,&quot; McDonald sheepishly said.

The next day, the hurricane struck.

&quot;They basically threw away the key to the jail for four days,&quot; he said.

McDonald said he and the other prisoners were basically abandoned by authorities in the storm&#x27;s aftermath.

&quot;We had no food, no water, no power, no air-conditioning, no toilets,&quot; McDonald said.

&quot;A lot of people started breaking out and escaping and that&#x27;s when attention was brought to the jail.&quot;

While inmates escaped, McDonald decided to do the right thing and stay in the prison.

&quot;I never thought twice about it,&quot; he said. &quot;I just stayed in my cell and waited until someone came for us.&quot;

McDonald&#x27;s mate in jail, Robert, a resident of Los Angeles, was in custody because of a simple driving offence.

&quot;We were only there for misdemeanours, but we were in the same cells as murderers and prisoners awaiting the death sentence,&quot; McDonald said.

McDonald was released from Elayn Hunt yesterday after a brief appearance before a judge in the jail and was then driven more than eight hours by an Australian consular official to Clarksville, where his sister Jasmine, brother-in-law John, mother Sharon, father Doug and a large contingent of media were waiting for him.

His parents, who flew over from Australia worried he was dead, have been nice to him, but McDonald joked once the cameras leave they might give him a dressing down.

&quot;The cameras have been here so they&#x27;ve been really nice, but I&#x27;m expecting a clip behind the ears later,&quot; he said.

There is another issue McDonald, who plans to stay with his sister for a couple of weeks before returning to Australia, has to deal with.

Jasmine, who lives in the US, was desperate for some goodies from Australia - Vegemite and Tim Tams - but the stash was left in McDonald&#x27;s luggage back in the flood-hit city of New Orleans.

She will probably never get the goods.

&quot;Yeah, she was looking forward to them,&quot; McDonald said.

&quot;Hopefully we&#x27;ll find them.&quot;

Once the media leaves, McDonald and his family plan on going out for a quiet dinner in Clarksville, although unlike his boozy night in New Orleans that led to his adventure, soft drinks, not beer, will be ordered.

&quot;Yeah, I don&#x27;t think beer will be an option</pre>

右文（仅阅读辅助）：

<pre>,&quot; McDonald said with a laugh.

&lt;|im_end|&gt;Search Results: legal-download

Published: Aug 21, 20</pre>

### 位置1423618｜random｜z=0.03049824

上下文1391，目标offset=358，目标token=" is"；原文档未知。

包含目标的模型可见前文：

<pre> a meaning of time in which the present is constantly enriched by the past; they are content with the day. `He who lives with sense of the present&#x27;, writes Abraham Heschel, `knows that to get older does not mean to lose time but rather to gain time&#x27;. One sinks into the middle of time, toward the still point at the center of the world. `And do not call it fixity, where past and future are gathered&#x27; (T.S.Eliot).&quot; (6)

Again, in another place Moran writes:

&quot;If one imagines development as a straight line up or forward, then ground gained is an individual and permanent conquest. It seems to me that Christianity and every other major religion opposes this assumption. One&#x27;s life as a whole is at issue throughout all one&#x27;s life. That could be terrifying because no ground is securely possessed. However, not being in control of everything, we don&#x27;t have the burden of constructing the whole world. We just have to sit ourselves at the center of creation, listen attentively, and then respond the best we can. When we come to die, we do not have to change our position radically, except perhaps to lie down rather than sit ... A theory of religious development is a circle about the unreachable center of our own lives and the lives of all creatures.&quot;(7)

This sitting at the center is the sitting in Bodhimandala, in Emptiness. It is Emptiness itself sitting thus: The Formless Self presences and exerts itself as this form through and through; and the entire universe is attained in this form. &quot;Such is the I that is life, the life that is `I&#x27;,&quot; says Dogen (8). Now is all times, all of reality.

Your Now is</pre>

右文（仅阅读辅助）：

<pre> eternity as this time, &quot;Eternal time is just this moment,&quot; runs the verse to Mumonkan case No.47. &quot;All are blessed, all are blessed,&quot; proclaims the verse to case no.35. You are blessed, graced, accepted and affirmed unconditionally. Your behavior in the world many be inadequate or a failure; but you are blessed, good, beautiful</pre>

### 位置5103262｜random｜z=0.07627461

上下文4987，目标offset=925，目标token=" they"；原文档未知。

包含目标的模型可见前文：

<pre> about a two-speed economy. We&#x27;d have a one speed economy and be in the slow lane if it wasn&#x27;t the for the mining boom?

BOB BROWN: You can defend the billionaires, but I&#x27;m with the Treasurer in saying, &quot;Let&#x27;s just make this fair&quot;. It&#x27;s not black and white, Chris. The world is not that easy. But we have a parliament of democratically elected representatives to get a better go for average Australians, average small business, schools, hospitals, transport systems and the manufacturing sector, and that&#x27;s what I&#x27;m about, as a Green, and I make no bones about it. And I think that we need to get a fair return - the super profits tax, remember this, recommended by Treasury - is what the Greens are supporting so we can have the things I spoke about earlier in this interview.

CHRIS UHLMANN: Bob Brown, just briefly, what do you think then should be done about what they say in the public space? Should we stop the billionaires from speaking at all?

BOB BROWN: Well that&#x27;s nonsense. Of course we shouldn&#x27;t. But we should have some fair go in this country, and let&#x27;s even up the lobbying system and the power of those barons in getting a fair deal for the rest of Australians, and that&#x27;s what we&#x27;re about, Chris. Of course we&#x27;re not going to shut anybody up. This is a free democracy, but from what I saw today there&#x27;s quite a lot of representatives around the place want to shut Greenpeace up, for goodness sake. Well, let&#x27;s have some proper discourse in this country - and, by the way, let me not leave this by saying: and let&#x27;s stop dumping! We have an environment minister who wants to dump millions of tonnes of dredged soil into the Great Barrier Reef World Heritage area, for goodness sake.

CHRIS UHLMANN: Well Bob Brown, I&#x27;m sure you&#x27;re not going to go quietly into that good night, so thanks for joining us.

BOB BROWN: Thanks, Chris.&lt;|im_end|&gt;

Podcast - Full Program Podcast - Individual Items
Not sure what this is? Find out more

The World TodayThe World Today
Correspondents ReportCorrespondents Report

More Current Affairs:




Unconfirmed reports of fighting in northern Iraqi city of Kirkuk


PM Archive - Friday, 21 March , 2003  23:02:26

Reporter: Eric Campbell

HAMISH ROBERTSON: Now to the view from northern Iraq, where our Correspondent, Eric Campbell is based on the Kurdish frontline.


Eric, I gather there&#x27;s been some fighting in the city of Kirkuk, which is a Kurdish city in terms of its population, but is under Iraqi control.

ERIC CAMPBELL: That&#x27;s right. Kirkuk&#x27;s about 40 kilometres down the road from where I&#x27;m standing, past the Kurdish frontline. I can see the Iraqi bases just ahead of me.

Now we&#x27;re hearing from the Peshnigas [phonetic] here there has been some fighting in the city, but that is unconfirmed at this stage. It&#x27;s very difficult to communicate with Kirkuk at the moment, and even the people here are in a bit of a fog as to what&#x27;s going on.

HAMISH ROBERTSON: And the Americans, I gather, are also very concerned about the security of oil wells in the region?

ERIC CAMPBELL: Absolutely. There&#x27;s been reports that for some time now, that the Iraqis have left explosives around the oil wells, and could detonate them at any time. US Special Forces are operating in the area, and obviously that would be a target for them to stop them doing that. There were earlier some reports they had actually done so and gone into Kirkuk, but we have no confirmation of this, so I think at this stage they can be discounted.

HAMISH ROBERTSON: And is there also concern that there may be an intervention by Turkish forces without the approval of the American-led coalition?

ERIC CAMPBELL: Very much so. The Turkish Parliament last night approved the deployment of Turkish troops, they didn&#x27;t say when, but just gave the green light for it. Now, the Peshnigas [phonetic] who we&#x27;ve been speaking to here at the frontline are very angry about this. They say if the Turks come in they will fight them, and their fear is the Turks will stop in trying to seize Kirkuk, which they</pre>

右文（仅阅读辅助）：

<pre> regard as their Kurdish homeland, because Turkey doesn&#x27;t want them to control the oil, they fear that it could fund a separate Kurdish state that would encourage Turkish Kurds to separate.

So really there&#x27;s a lot of tension rising to the surface here, and we may see the prospect of the US allied Kurds actually engaged in combat with the other US ally, the Turks, if Turkey does in fact move in</pre>

### 位置8652252｜high_activation｜z=0.4330861

上下文8456，目标offset=800，目标token=".y"；原文档未知。

包含目标的模型可见前文：

<pre>6. doi: 10.1016/j.gene.2007.10.030. [PubMed] [Cross Ref]
  • Lees AD. The location of the photoperiodic receptors in the aphid Megoura viciae Buckton. J Exp Biol. 1964;41:119–133. [PubMed]
  • Zhong YS, Mita K, Shimada T, Kawasaki H. Glycine-rich protein genes, which encode a major component of the cuticle, have different developmental profiles from other cuticle protein genes in Bombyx mori. Ins Biochem Mol Biol. 2006;36:99–110. doi: 10.1016/j.ibmb.2005.07.005. [PubMed] [Cross Ref]
  • Andersen SO. Studies on proteins in post-ecdysial nymphal cuticle of locust, Locusta migratoria, and cockroach, Blaberus craniifer. Ins Biochem Mol Biol. 2000;30:569–577. doi: 10.1016/S0965-1748(00)00029-1. [PubMed] [Cross Ref]
  • Magkrioti CK, Spyropoulos IC, Iconomidou VA, Willis JH, Hamodrakas SJ. cuticleDB: a relational database of Arthropod cuticular proteins. BMC Bioinf. 2004;5:138. doi: 10.1186/1471-2105-5-138. [PMC free article] [PubMed] [Cross Ref]
  • Lees AD. The photoperiodic responses and phenology of an English strain of the pea aphid Acyrthosiphon pisum. Ecol Entomol. 1989;14:69–78. doi: 10.1111/j.1365-2311.1989.tb00755.x. [Cross Ref]
  • Rosenbaum EE, Hardie RC, Colley NJ. Calnexin is essential for rhodopsin maturation, Ca2+ regulation, and photoreceptor cell survival. Neuron. 2006;49:229–241. doi: 10.1016/j.neuron.2005.12.011. [PMC free article] [PubMed] [Cross Ref]
  • Lee SJ, Xu H, Kang LW, Amzel LM, Montell C. Light adaptation through phosphoinositide-regulated translocation of Drosophila visual arrestin. Neuron. 2003;39:121–132. doi: 10.1016/S0896-6273(03)00390-8. [PubMed] [Cross Ref]
  • Shiga S, Numata H. Neuroanatomical approaches to the study of insect photoperiodism. Photochem Photobiol. 2007;83:76–86. [PubMed]
  • Babu K, Bahri S, Alphey L, Chia W. Bifocal and PP1 interaction regulates targeting of the R-cell growth cone in Drosophila. Dev Biol. 2005;288:372–386. doi: 10.1016/j.y</pre>

右文（仅阅读辅助）：

<pre>dbio.2005.09.017. [PubMed] [Cross Ref]
  • Phillips AM, Smart R, Strauss R, Brembs B, Kelly LE. The Drosophila black enigma: The molecular characterization of the black &#x27; mutant and behavioural allele. Gene. 2005;351:131–14</pre>

### 位置8653476｜high_activation｜z=0.4330861

上下文8457，目标offset=1000，目标token=".y"；原文档未知。

包含目标的模型可见前文：

<pre> upon their laccase-catalyzed oxidative conjugation with catechols. Ins Biochem Mol Biol. 2006;36:610–611. doi: 10.1016/j.ibmb.2006.05.001. [PubMed] [Cross Ref]
  • Hardie J. Nervous system. In: Minks AK, Harrewijn AP, editor. Aphids, their Biology, Natural Enemies and Control. 2A. Amserdam, Oxford, New York, Tokyo: Elsevier; 1987. pp. 131–138.
  • Fritz JL, VanBerkum MFA. Regulation of Rho family GTPases is required to prevent axons from crossing the midline. Dev Biol. 2002;252:46–58. doi: 10.1006/dbio.2002.0842. [PubMed] [Cross Ref]
  • Sanchez D, Ganfornina MD, Torres-Schumann S, Speese SD, Lora JM, Bastiani MJ. Characterization of two novel lipocalins expressed in the Drosophila embryonic nervous system. Int J Dev Biol. 2000;44:349–359. [PubMed]
  • Wills Z, Emerson M, Rusch J, Bikoff J, Baum B, Perrimon N, Van Vactor D. A Drosophila homolog of cyclase-associated proteins collaborates with the Abl tyrosine kinase to control midline axon pathfinding. Neuron. 2002;36:611–622. doi: 10.1016/S0896-6273(02)01022-X. [PubMed] [Cross Ref]
  • Kraut R, Menon K, Zinn K. A gain-of-function screen for genes controlling motor axon guidance and synaptogenesis in Drosophila. Curr Biol. 2001;11:417–430. doi: 10.1016/S0960-9822(01)00124-5. [PubMed] [Cross Ref]
  • Quattrocchi CC, Wannenes F, Persico AM, Ciafre SA, D&#x27;Arcangelo G, Farace MG, Keller F. Reelin is a serine protease of the extracellular matrix. J Biol Chem. 2002;277:303–309. doi: 10.1074/jbc.M106996200. [PubMed] [Cross Ref]
  • Lloyd TE, Verstreken P, Ostrin EJ, Phillippi A, Lichtarge O, Bellen HJ. A genome-wide search for synaptic vesicle cycle proteins in Drosophila. Neuron. 2000;26:45–50. doi: 10.1016/S0896-6273(00)81136-8. [PubMed] [Cross Ref]
  • Kovoor A, Seyffarth P, Ebert J, Barghshoon S, Chen CK, Schwarz S, Axelrod JD, Cheyette BNR, Simon MI, Lester HA, Schwarz J. D-2 dopamine receptors colocalize regulator of G-protein signaling 9-2 (RGS9-2) via the RGS9 DEP domain, and RGS9 knock-out mice develop dyskinesias associated with dopamine pathways. J Neurosci. 2005;25:2157–2165. doi: 10.1523/JNEUROSCI.2840-04.2005. [PubMed] [Cross Ref]
  • Lees AD. The endocrine control of polymorphism in aphids. In: Downer RGH, Laufer N, editor. Endocrinology of Insects. New York: Alan R. Liss; 1983. pp. 369–377.
  • Tu MP, Yin CM, Tatar M. Mutations in insulin signaling pathway alter juvenile hormone synthesis in Drosophila melanogaster. Gen Comp Endocrinol. 2005;142:347–356. doi: 10.1016/j.y</pre>

右文（仅阅读辅助）：

<pre>gcen.2005.02.009. [PubMed] [Cross Ref]
 </pre>

### 位置10339398｜random｜z=0.06826565

上下文10105，目标offset=772，目标token="::"；原文档未知。

包含目标的模型可见前文：

<pre>: C
Sexual Content: C+
Language: D+
Drugs/Alcohol: B
Run Time: 124
Theater Release: 19 Apr 2013
Video Release: 06 Aug 2013
MPAA Rating: PG-13
See Canadian Ratings
How We Determine Our Grades

Why Is Oblivion Rated PG-13?

Violence: A character experiences peril while flying through a lightening storm. He later rides a motorcycle without a helmet. A man’s foot is caught in a bear trap after being ambushed by attackers who shoot at him. A rope breaks while he tries to escape and he falls to the ground far below. Scenes of post-apocalyptic devastation are seen. A man is hit in the head with a gun butt resulting in a bloody facial injury. Characters throw punches, grapple and fire at one another on numerous occasions. A man is choked until he passes out. Drones fire on and kill humans, blowing their bodies to bits. A man holds a gun to a woman’s head. She is later shot in the stomach. Numerous explosions occur.

Sexual Content: Partial male and female back nudity is seen in a shower scene. Female buttock nudity is shown when a woman undresses and dives into a swimming pool. Brief suggestive scenes of sexuality are included. Unclothed characters are seen in a state of stasis. Couples kiss and embrace. Some brief crude content and innuendo is also included.

Language: The script contains infrequent scatological slang, vulgarities, profanities and one use of the sexual expletive.

Alcohol / Drug Use: A secondary character smokes a cigar. A female attempts to inject a medical solution into another character.

Join the Conversation

About the Reviewer: Kerry Bennett
&lt;|im_end|&gt;Pathetic Peripatetic

Most of my followers expect Doctor Who related posts, I made a Police Box Ring that I occasionally post about, and my username is a reference to a specific strip of an out-of-print newspaper comic (Some people got it!). I grew up with video games and television (people like this are rare, I&#x27;m sure) and am currently employed as a jeweler CAD technician. Quite often those two things interject. You can email me at

Obviously, I read all the right webcomics.&lt;|im_end|&gt;PilotManager Home

PilotManager/CDE/Calendar Frequently Asked Questions

Ok, I hope this little summary will answer all CDE and Calendar Manager related questions.
If your experience contradicts any of the info below please let me know.
  1. Do I have to use the CDE window system to run PilotManager or SyncCM?

  2. What version of Solaris/CDE do I need to use SyncCM??

  3. How do I tell what version of CDE I have?

  4. How do I get the right version of CDE if I don&#x27;t have it already?

  5. What if I see the message:
    user@host is in an obsolete data format
    It must be updated to the CDE format before SyncCM can interface with it.

  6. What if I see the message:
    Error: Csa logon failed: X-DT SERVICE NOT REGISTERED

  7. What if I see the message:
    SyncCM cannot interface with your calendar server
    Please upgrade to the CDE calendar server

  8. What if I see the message:
    Error Csa add_entry failed: X-DT BACKING STORE PROBLEM ... while adding ...
    Unable to create &#x27;...&#x27; in Desktop calendar

  9. What if I see the message:
    Error Undefined subroutine &amp;SyncCM::cm::</pre>

右文（仅阅读辅助）：

<pre>setup called at 
    .../SyncCM.pm line 864

  10. My calendar server has just been upgraded and SyncCM no longer works.. what do I do now?

  11. Duplicates are being created for some of my repeating appointments.. what is going on?

SourceForge.net Logo&lt;|im_end|&gt;The Post Your Thoughts of the Moment Thread

Discussion in &#x27;</pre>

## Feature 15596，h_V=2

### 位置320728｜high_activation｜z=0.1103424

上下文313，目标offset=423，目标token="\n\n"；原文档未知。

包含目标的模型可见前文：

<pre> drop in diastolic pressure less than 10 mmHg when patient changes position from lying to sitting
D. A drop in diastolic pressure greater than 10 mmHg when patient changes position from lying to sitting

67. Which of the following measures will not help correct the patient’s condition [1]

A. Offer large amount of oral fluid intake to replace fluid lost
B. Give enteral or parenteral fluid
C. Frequent oral care
D. Give small volumes of fluid at frequent interval

68. After nursing intervention, you will expect the patient to have [1]

1. Maintain body temperature at 36.5 C
2. Exhibit return of BP and Pulse to normal
3. Manifest normal skin turgor of skin and tongue
4. Drinks fluids as prescribed

A. 1,3
B. 2,4
C. 1,3,4
D. 2,3,4

SITUATION: [ From JUN 2005 NLE ] A 65 year old woman was admitted for Parkinson’s Disease. The charge nurse is going to make an initial assessment.

69. Which of the following is a characteristic of a patient with advanced Parkinson’s disease? [1]

A. Disturbed vision
B. Forgetfulness
C. Mask like facial expression
D. Muscle atrophy

70. The onset of Parkinson’s disease is between 50-60 years old. This disorder is caused by [1]

A. Injurious chemical substances
B. Hereditary factors
C. Death of brain cells due to old age
D. Impairment of dopamine producing cells in the brain

71. The patient was prescribed with levodopa. What is the action of this drug? [1]

A. Increase dopamine availability
B. Activates dopaminergic receptors in the basal ganglia
C. Decrease acetylcholine availability
D. Release dopamine and other catecholamine from neurological storage sites

</pre>

右文（仅阅读辅助）：

<pre>72. You are discussing with the dietician what food to avoid with patients taking levodopa? [3]

A. Vitamin C rich food
B. Vitamin E rich food
C. Thiamine rich food
D. Vitamin B6 rich food

73. One day, the patient complained of difficulty in walking. Your response would be [2]

A. You will</pre>

### 位置434549｜random｜z=0.04344782

上下文424，目标offset=657，目标token=".\n\n\n"；原文档未知。

包含目标的模型可见前文：

<pre>0mm f/4 L)

Fisher Price Kid-Tough, Shutter: 1/10, Aperture: f/2.8, ISO: 60

Even after all of that, I’m really the most proud of this image. When my five year old son heard I was going to take pictures of the moon, he wanted to grab his camera and come with me. Shooting the moon with my son will go down as one of those classic moments. Plus I think I can use special times like that to justify the cost of a 400mm f/2.8 to the wife. $12,000. Shoot for the moon.

This entry was posted in Photo, Writing and tagged , , , , . Bookmark the permalink.

2 Responses to 300mm vs 200mm (L): The Harvest Moon

  1. Aaron says:

    That’s an amazing difference! I love the sharpness using the L lens.

    FYI… the image comparison doesn’t work in Chrome either. Had to pop open Firefox.

  2. Hey there just wanted to give you a brief heads up&lt;|im_end|&gt;Dec 18, 2013
Home| Tools| Events| Blogs| Discussions| Sign UpLogin

The Truth about Trade

RSS By: Dean Kleckner, AgWeb.com


Vermont’s REAL Food Safety Issue

Apr 19, 2012

By Terry Wanzek: Jamestown, North Dakota

The &quot;heads&quot; side of every quarter pictures a famous farmer: George Washington. Among the 50 states represented on the &quot;tails&quot; side, however, only Vermont shows a farmer: He’s tapping maple trees for syrup. 


So it would be a special shame if Vermont’s legislators were to pass a bill that would hurt farmers not just in the Green Mountain State, but across America. 


The bill would require all food that possibly contains genetically modified (GM) ingredients to say so on a special label. 


If this sounds reasonable on the surface, consider a few details: Just about everything we eat derives in some way from biotechnology (which is a good thing), the public isn’t exactly clamoring for this bill, and supporters of the proposal are driven primarily by greed and cynicism. 


Thankfully, the bill is now stuck in a committee and many observers think it will stay there, failing to become a law before the state’s general assembly finishes its work this year. But I’ve spent a fair bit of time around state capitols (I’m both a family farmer and a State Senator in North Dakota), and I’ve seen a lot happen in the last days of a session. 


So farmers need to keep an eye on what happens in Montpelier. 

The fundamental flaw in Vermont’s bill is that nobody needs it. It’s a solution in search of a problem. 


Biotechnology is an accepted tool of conventional agriculture. Around the world, farmers have grown more than 3 billion acres of GM crops--that is, plants bred to have a natural resistance to insects and weeds, resulting in a bountiful and sustainable food ingredient.


</pre>

右文（仅阅读辅助）：

<pre>In the United States, the vast majority of corn and soybeans are genetically enhanced. Farmers are able to grow more food on less land, boosting our national food security and helping us conserve wilderness at the same time. Most Americans eat food derived from biotechnology every day. 


Biotechnology is a process. The food it produces is no different nutritionally from other kinds of food. Demanding special</pre>

### 位置5514321｜random｜z=0.03905329

上下文5389，目标offset=709，目标token=".\n"；原文档未知。

包含目标的模型可见前文：

<pre> next in line to be a big-time player. He was voted &quot;Best Fit in any System&quot; which speaks to his versatility.
Bad: At times, Ely didn&#x27;t have the most pop on his ball. There were opportunities for him to fire it to a receiver and he floated it a little too much sometimes.
Kiehl Frazier6-3/212Springdale (Ark.) Shiloh Christian
Good: Frazier is big and strong and was one of the best-looking quarterbacks at the event. He got better as the week went on and has pop on his passes.
Bad: Frazier does have a wind-up motion on his delivery which could be a concern playing against SEC defenses.
Everett Golson6-0/170Myrtle Beach (S.C.)
Good: Golson has a lot of strength for his size and his delivery is fine but at only 6 feet tall seeing over big offensive lines in the ACC could be a concern. He&#x27;s best when making something happen in the backfield.
Bad: His size is an issue. Golson will be one of the smaller quarterbacks in the ACC but if the UNC coaching staff can be creative then he could be a special prospect.
Cody Kessler6-1/208Bakersfield (Calif.) Centennial
Good: Kessler has a good release point, can get out of the pocket and throw consistently and is physical - probably the strongest-looking quarterback at the Elite 11. He could easily be confused for a fullback or a linebacker.
Bad: There isn&#x27;t much to criticize with Kessler but one concern could be that he winds the ball up high and takes an extra second to throw a pass. It doesn&#x27;t seem like a big issue but it could be something to watch.
Adam Pittser6-1/200Richmond (Ill.) Burton
Good: Pittser might not become a five-star recruit but he has helped himself immeasurably at the Elite 11. Not only did Pittser belong here but he was one of the better quarterbacks. He is strong, tough and has a lot of zip on his passes.
Bad: Can Pittser do this consistently? He runs the wing-T in high school so it&#x27;s tough to know whether Pittser can deliver these performances over and over again.
DaMarcus Smith6-1/180Louisville (Ky.) Seneca
Good: Smith, who missed last season with a knee injury, looks healthy and his arm is stronger than ever. The Louisville commit can fire the ball past defenders and to his receivers and can also move around the pocket well.
Bad: There were times when Smith lacked consistency. Some throws were wild but when Smith composed himself he was one of the better throwers in attendance.
Kendal Thompson6-2/180Moore (Okla.) Southmoore
Good: Thompson is a dual-threat quarterback but didn&#x27;t get to show his running skills much in this competition. Still, he delivered on-point passes and showed a good release point.
Bad: One concern with Thompson is that he throws a lot with only his arm and doesn&#x27;t use the rest of his body to deliver more power behind the ball.
J.W. Walsh6-2/190Denton (Texas) Guyer
Good: Walsh is an outstanding competitor who totaled 49 touchdowns last season. He has good footwork and had probably the quickest release of any quarterback.
</pre>

右文（仅阅读辅助）：

<pre>Bad: There were numerous times when Walsh didn&#x27;t throw good spirals. Whether it was a grip problem or something else we&#x27;re not sure but he didn&#x27;t have the same issue at the recent NIKE 7on Tournament.
After watching Driskel, from Oviedo (Fla.) Hagerty, for four straight days working out in drills and 7-on-7 competition the comparison</pre>

### 位置5619532｜random｜z=0.04881892

上下文5492，目标offset=514，目标token="]\n\n"；原文档未知。

包含目标的模型可见前文：

<pre> deprecated setRouting() function, however this may have unexpected side effects and/or not even work depending upon what the hardware is capable of and what cases are correctly managed in the underlying subsystems/drivers.

share|improve this answer
The routing function picks one audio device, not multiple. That&#x27;s why I was wondering if I could directly write bytedata onto the audio jack. Thanks, anyway. –  Torcellite Sep 5 at 18:16
add comment

Your Answer


&lt;|im_end|&gt;Take the tour ×

I want to create dynamic menus according to user permissions. As was already discussed here and by the the documentation itself, I know that I can achieve this in the templates using the following snippet:

{% if perms.polls.can_vote %}
        &lt;a href=&quot;/polls/vote&quot;&gt;Vote&lt;/a&gt;
{% endif %}

But the problem is that for security reasons I want to limit the access to the views too. The snippet that I found in the documentation is the following:

from django.contrib.auth.decorators import permission_required

def my_view(request):
    # ...
my_view = permission_required(&#x27;polls.can_vote&#x27;, login_url=&#x27;/loginpage/&#x27;)(my_view)

Isn&#x27;t this against DRY principle? Isn&#x27;t there a way to define only in one place what is the permission needed for each url? Perhaps in urls.py?

share|improve this question
add comment

2 Answers

up vote 2 down vote accepted

EDIT: (See end of post for the original text of the answer with the initial, simple idea.)

After being kindly stricken with a cluebat (see the OP&#x27;s comment below), I find I can see more to the problem than before. Sorry it took so long. Anyway:

Would this kind of template be alright for you?

{% for mi in dyn_menu_items %}
  {% if mi.authorised %}
     &lt;a href={{ mi.url }}&gt;{{ mi.title }}&lt;/a&gt;
  {% endif %}
{% endfor %}

To make this work on the Python side, you could use RequestContext in your views with a custom context processor setting the dyn_menu_items variable appropriately. In case some background information is required, the Advanced Templates chapter of the Django Book introduces RequestContext, shows how to use it with render_to_response (kinda important :-)) etc.

Also, I guess at this point it could be useful to put the view functions responsible for the locked-up sections of your site in a list somewhere:

_dyn_menu_items = [(url1, view1, title1, perm1), ...]

</pre>

右文（仅阅读辅助）：

<pre>Then you could map a couple of functions, say prepare_pattern and prepare_menu_item across that list, having it work roughly like so:

def prepare_pattern(menu_item):
    url1, view, title, perm = menu_item
    pattern = PREPARE_URLCONF_ENTRY_SOMEHOW(...) # fill in as appropriate
    return pattern

def prepare_menu_item(menu_item):
    url, view</pre>

### 位置9142092｜high_activation｜z=0.1103424

上下文8935，目标offset=533，目标token="\n\n"；原文档未知。

包含目标的模型可见前文：

<pre> dans l&#x27;impressionnant et rare entreprise et les concepts de marketing pour les entreprises utilisant une mini-encyclopédie incroyable trouvent au Check-out now et enfin comprennent comment la vente,Louboutin Strident Daffodile - Christian louboutin pas cher, ainsi que de leurs clients et donc on.00. alors que Google paye les factures webmasters créer plusieurs sites Web avec contenu gratuit et utilitaires pour tout le monde,, 000-10, imaginez que vous puissiez utiliser personnellement le pouvoir d&#x27;internet pour produire pour vous un revenu réel, vous voulez vous assurer qu&#x27;ils sont une entreprise solide, une fois que vous avez passé par le processus de la première fois,Nouveau-Christian Louboutin - Christian louboutin pas cher, donc, pour ceux d&#x27;entre vous qui ne connaissent pas,? À l&#x27;aide de fichiers audio mp3 pour diffuser un message s&#x27;appelait auparavant «

yaerirl fdglfvk

dtkdscjcjopfm, Gail wix 49 okbridge, IsFqAbn, Pamelor, BYaLTOV, Cialis Daily, hsMJqQQ, Nick diaz 32red poker, BqHSFvl, Raspberry Ketones, tgZIIEr, Facebook marketing success, bgXwjWV.

pmumxmh xgngnuq

jnwxlcjcjopfm, Generic Levitra, YQgGcFt.

beownlw vkbmthq

ljjuucjcjopfm, Gay male edging, hRSbabw.

ovrmavi lzjwbhr

reiidcjcjopfm, Buy xanax bars medicaments, OGoulUQ, Cialis professional, VEkPLMp, Online fioricet, dPFFvdF, Sign up bonus online casino, TGQNmtq, Buy levitra online, zWAHtvO, Pokies, AJyAGWt.

oreqsek euscatf

kkzwycjcjopfm, Vigrx plus directions, xuJuXYF, Cialis uk suppliers, tqSIAEY, Fioricet, sOfUOnt, Vigrx rip off, WUZiBbB, Ambien cr without a prescription, VmaGfLK, Priligy t, CCOYzWM.

sbgzdfo rjhyugo

</pre>

右文（仅阅读辅助）：

<pre>omrwicjcjopfm, Xanax drug, fkTcwAF.

gohrptb ctkzksz

tuqcscjcjopfm, Which is better the levitra are the cialis, LxqCsgZ, Cialis, wapCwKw, Buy viagra uk, kagLnci, Ambien without prescription, IDPeuoW,</pre>

### 位置9224478｜random｜z=0.01122126

上下文9016，目标offset=23，目标token=".\n\n"；原文档未知。

包含目标的模型可见前文：

<pre> the aging process can last from 3 months to one year or longer, depending on the final product that is desired.

</pre>

右文（仅阅读辅助）：

<pre>You are on Page 1



&lt;|im_end|&gt;IRS targeting violated employee contract against political coercion

June 4, 2013, Fairfax, VA—Americans for Limited Government President Nathan Mehrens today issued the following statement calling attention to a 2009 National Treasury Employees Union contract agreement that forbade political coercion at the Internal Revenue Service (IRS) and stated “Employees should be protected against</pre>

### 位置9404677｜high_activation｜z=0.1152252

上下文9192，目标offset=154，目标token="..\n\n"；原文档未知。

包含目标的模型可见前文：

<pre> application.
Raja Sagar Panamgipalli
Ranch Hand

Joined: Aug 13, 2003
Posts: 109
Thanx Dima..

I some what get it but don&#x27;t get it..
can u do a favor by expalianing the following piece of code..

PreparedStatement pstmt=con.prepareStatement(&quot;INSERT INTO EMP(NAME,PHONE)VALUES(? ,?)&quot;);
then i give
pstmt.setString(2,&quot;274 7071&quot;);

what exactly happens here...
In a preparedstatment we are specifying the arguments while creating an object of PreparedStatement from Connection Obj.when unlike in a createStatement method of the Connection we don&#x27;t do that.
Have i messed up...sorry...plz elaborate..

</pre>

右文（仅阅读辅助）：

<pre>God bless mankind..
Wayne L Johnson
Ranch Hand

Joined: Sep 03, 2003
Posts: 399
You are on the right track, Raja. The basic &quot;createStatement()&quot; method returns a &quot;Statement&quot; instance that can be used to send SQL to the database for execution. Every SQL you send will get validated, compiled, and</pre>

### 位置10251837｜random｜z=0.0908111

上下文10020，目标offset=187，目标token=" ,\n\n"；原文档未知。

包含目标的模型可见前文：

<pre> giant ape, but the daredevil stunts just pushed things too far. Everyone has their limits, I guess.&lt;|im_end|&gt;Iscriviti Feedback Italian
cerca qualsiasi parola, ad esempio cenosillicaphobia:
1. Hajmadilla
1. Flaccid penis
2. Not being able to sexually perform due to either performance anxiety, or too much alcohol or drugs.
3. Reaction to something unattractive or uncool
Ex 1.
Guy 1: Did you fuck that girl last night?
Guy 2: I took her home, but I got hajmadilla
Guy 1: I hate when that happens

Ex 2.
That 300 pound girl who won&#x27;t shut up in my econ class is giving me a hajmadilla
rss and gcal&lt;|im_end|&gt;Questions on Sampling 11-20

Labels: , , ,

</pre>

右文（仅阅读辅助）：

<pre>1. Define Non probability Sampling
The difference between non probability and probability sampling is that non probability sampling does not involve random selection and probability sampling does. It can be divided into two broad types: accidental or purpose. In purposive sampling, we sample with a purpose in mind

2. Define various non probability sampling methods
Modal Instance Sampling
Expert Sampling
Quota Sampling
Non proportional Quota</pre>

## Feature 15730，h_V=1

### 位置1785326｜random｜z=0.01373525

上下文1744，目标offset=817，目标token="\n"；原文档未知。

包含目标的模型可见前文：

<pre> thanksgiving, forgiveness, nonviolence, rational and scientific thinking, awe and wonder at the universe, and the recognition that our well-being depends on the well-being of everyone on the planet and the well-being of the Earth itself. It further mandates the teaching of all knowledge and skills required to assure that all students can contribute to the implementation of policies that enhance the long-term sustainability of Earth.

It will take just as long to pass the shorter more narrowly framed attempts to overthrow Citizens United as it will to pass this broader ESRA version. Yet in the actual struggle for change, the ESRA goes far deeper and is far more likely to stir the enthusiasm of the American people and the activists necessary to carry a campaign for constitutional reform to every corner of the country. What Obama should have learned during the fight for health care reform is that the full weight of corporate power gets mobilized just as heavily for moderate reform as it would for a more appealing, broader, and deeper reform. And the broader reform, precisely because it spells out what we are seeking, is much more likely to generate popular support and to educate people along the way to a vision of a more democratic and more environmentally responsible society.

The fourth opportunity: Israel’s May 31 attack on the Gaza aid flotilla.

Israel’s attack on the Gaza aid flotilla has provoked worldwide attention to the unjust blockade of some food, clothing, building materials, and other essentials for the people of Gaza, who are living under extremely oppressive conditions, as well as attention to the more general issue of the Occupation of the West Bank by Israel. This is a perfect moment for progressive forces to push for an international conference of all the relevant stakeholders and countries of the world that helped create Israel in the UN vote of November 1947 to now develop a peace plan that provides security for Israel and full national self-determination for the Palestinian people. It’s the moment for a peace plan that involves a Palestinian state on all of the West Bank and Gaza, that enables the sharing of Jerusalem, and that secures justice for the Palestinian people in the form of massive reparations to Palestinian refugees all around the world. This is the moment for the peoples of the world -- together with the economic, political, and military power of the U.S. -- to impose a solution, and that is what we must publicly call on Obama and the Democratic Party to pursue.

We at the Strategy Conference of Liberals and Progressives next weekend in Washington, D.C., will be holding a memorial service for those killed by the Israeli assault, as well as a prayer service for those hurt or wounded (including Israeli soldiers who were sent by an idiotic and self-destructive Israeli military/political elite to commit this unjustified assault). We will be praying not only for their speedy recovery, but also for the freeing of Israeli soldier Gilad Shalit by Hamas and the freeing of thousands of Palestinian prisoners by Israel. This will take place at a rally across from the White House on Sunday, June 13, from 11 a.m. to 2 p.m. in Lafayette Park. 

The suffering of both Palestinian and Israeli peoples will not be brought about by the lame process of negotiations with the United States unwilling to use its power to push Israel. Given the realities of the current Congress, there is no hope that President Obama will exercise the needed leadership by himself, but we could push him into an international framework that gives him the legitimacy to use American power in defense of a rational solution that is fair to both sides. 

This is not the moment for progressives to waste our energies denouncing Israel, though we certainly have reason to be angry at what Israel has been doing for these past 43 years since the 1967 conquest of Palestine—it is the moment for us to put forward a rational plan to once and for all end this conflict. Will we waste this opportunity as well?

  • submit to reddit

Enviro Newswire

Enviro Newswire
presented by&lt;|im_end|&gt;News &amp; Politics  
</pre>

右文（仅阅读辅助）：

<pre>comments_image Comments


Student loans have been going up since the recession began--and now defaults are up too. Something has to be done, but what?
  • submit to reddit
  • submit to reddit

“If you want to take a relation of violent extortion, sheer power, and turn it into something moral, and most of all, make it seem like the victims are to blame, you</pre>

### 位置5056354｜random｜z=0.01446767

上下文4942，目标offset=70，目标token="\n\n\n"；原文档未知。

包含目标的模型可见前文：

<pre> changes, that is, when an ADAM instance is added or removed.

You can modify the values in the following table on the msDS-Other-Settings attribute of the directory service object, or on a crossRef object, to configure the referral behavior of an ADAM instance.


Value name Default Meaning



Maximum number of referrals returned by ADAM


</pre>

右文（仅阅读辅助）：

<pre>5 minutes

Time interval at which referral information is updated



Setting the value to 1 prevents ADAM from providing referral information

Values that you set on a crossRef object take precedence over any values that you set on the directory service object.

Generating referrals without crossRef objects

If a crossRef does not exist for the search base, ADAM determines the DNS name if the distinguished name that is</pre>

### 位置6249798｜random｜z=0.105288

上下文6108，目标offset=549，目标token="."；原文档未知。

包含目标的模型可见前文：

<pre> $G : \mathsf{Qcoh}(Y) \to \mathcal{C}$ are cocontinuous $k$-linear tensor functors, then for every epimorphism $A \boxtimes_k B \to A&#x27; \boxtimes_k B&#x27;$ also the induced morphism $F(A) \otimes G(B) \to F(A&#x27;) \otimes G(B&#x27;)$ is an epimorphism. I know this (quite indirectly) when $X$ is quasiprojective. For the general case I need a &quot;separated&quot; characterization of epimorphisms.

share|improve this question
What happens for vector spaces, i.e. the case $R=k=S$? –  HenrikRüping Oct 2 at 19:03
Well in this case epis = split epis are easy to characterize (because we have fully-faithfulness). –  Martin Brandenburg Oct 2 at 22:48
add comment


Your Answer



Browse other questions tagged or ask your own question.&lt;|im_end|&gt;Take the tour ×

Historically, the lattices with high density were studied intensively, e.g. E_8 lattice or Leech Lattice. However, there are situations that lattices with low kissing number are required. Specifically, I am wondering if there is any infinite family of n-dimension lattices which the kissing number is bounded by poly(n), and still relatively dense?

share|improve this question
add comment

3 Answers

If the question is about the asymptotic behavior in high dimensions then I do not think it is known or even conjectured that the kissing number for the densest packing is not polynomial in n. To the best of my memory (but check the book by Conway and Sloane) there are no known examples of lattices where the kissing number is exponential, and the best known bound are only quasi-polynomial ($n^{\log n}$).

So &quot;dense lattice packing&quot; and &quot;huge kissing numbers&quot; are not the same in very high dimensions. (There are the same in dimension 24!). If you are interested in interesting notions of low density packings you can think about packings which are locally densest but globally very undense. It does make sense to consider, even in low dimensions, what is the smallest &quot;local maximum&quot; for density of lattices.

Update: Let me add some more details on the connection between kissing number and more generally &quot;the low end of the distance distribution&quot; of a packing and the density. It is convenient to talk, more genarally, about spherical codes, and also to draw the analogy with binary codes.</pre>

右文（仅阅读辅助）：

<pre> The densest examples of spherical codes and binary error correcting codes are obtained by randomized constructions. For those the kissing number is expected to be subexponential. It is known that if these randomized bounds can be improved to get higher density than some relaxed notion of a kissing number will be exponential. (This is a result of Nati Linial and me for the binary case and I think that it was</pre>

### 位置7641736｜high_activation｜z=0.1804833

上下文7469，目标offset=73，目标token=">"；原文档未知。

包含目标的模型可见前文：

<pre>htubs. Poisons have been popular.&lt;/p&gt; &lt;p&gt; But water is not poisonous if drunk in moderate quantities, and none of those other weapons is harmful in normal use, any more than guns are. It is perfectly obvious to all but government junkies that people are killed not by weapons, but by their wielders. People.&lt;/p&gt; &lt;p&gt;</pre>

右文（仅阅读辅助）：

<pre> That gives quite a problem to said junkies. The only way they know, to fix any anomaly, is to write a law. Writing and enforcing laws are their sole occupational skills.&lt;/p&gt; &lt;p&gt; So which is it to be: to ban weapons, to ban people, or to ban both?&lt;/p&gt; &lt;p&gt; Consider the weapons-ban first. Outlaw all knives, all</pre>

### 位置7641778｜high_activation｜z=0.1814599

上下文7469，目标offset=115，目标token=">"；原文档未知。

包含目标的模型可见前文：

<pre>htubs. Poisons have been popular.&lt;/p&gt; &lt;p&gt; But water is not poisonous if drunk in moderate quantities, and none of those other weapons is harmful in normal use, any more than guns are. It is perfectly obvious to all but government junkies that people are killed not by weapons, but by their wielders. People.&lt;/p&gt; &lt;p&gt; That gives quite a problem to said junkies. The only way they know, to fix any anomaly, is to write a law. Writing and enforcing laws are their sole occupational skills.&lt;/p&gt; &lt;p&gt;</pre>

右文（仅阅读辅助）：

<pre> So which is it to be: to ban weapons, to ban people, or to ban both?&lt;/p&gt; &lt;p&gt; Consider the weapons-ban first. Outlaw all knives, all piano wires (and so, all pianos), all guns, all subway platforms and so on. Anything that can be used to kill, make it illegal. Easy; then there&amp;#39;ll be</pre>

### 位置8211676｜random｜z=0.1043114

上下文8026，目标offset=150，目标token="."；原文档未知。

包含目标的模型可见前文：

<pre>&quot; URL, that way when the users tries to go &quot;Setting&quot;-&gt;&quot;Change Password&quot; they will be redirected to your custom URL and make the password change in your backend.

share|improve this answer
I discovered the same a couple of days back while fiddling with the GA control panel. What I couldn&#x27;t figure out is, in all the docs, it says that this enables the password changing for GA WebApps. But does that include the mail service too? Coz that is my primary concern. Thanks for your reply :) –  miCRoSCoPiC_eaRthLinG Jul 10 &#x27;09 at 11:52
You are right, it&#x27;s only for webapps.</pre>

右文（仅阅读辅助）：

<pre> For IMAP/POP/API access then you&#x27;ll need to provide the password stored in Google Apps. You can include, in your change password application, the logic for synchronizing the password with Google Apps through the Provisioning API. –  dcifuen Jul 21 &#x27;09 at 13:01
Thanks. That helped clear a lot of doubts. –  miCR</pre>

### 位置9216216｜random｜z=0.0501122

上下文9007，目标offset=972，目标token="\""；原文档未知。

包含目标的模型可见前文：

<pre> the viewing screen, heaving a deep sigh. she had almost told him about her heritage, her guilty secret.
she could never tell anyone, she would be branded as xenos and executed for being the very thing she was sworn to hunt.


Captain Stern dropped to the floor as the halo of blinding blue light around him dissapeared, blood oozed from a gash in his leg before being clotted by his enhanced internal systems a second later.
Stern climbed to his feet and examined his surroundings. the grey rockcrete walls, exposed circuitry and flashing machinery of the control tower of Camp Bastion was a welcoming sight after the hell Stern had just fought off. he turned and reset the teleporter so that any other Grey Knights could teleport back to the camp.
Stern&#x27;s name described his features. he was an old Grey Knight, having served for nigh on four hundred years, his grey hair was close cropped and at the moment was plastered to his head with sweat and blood. his silver terminator armour was adorned with gold lettering and symbols of the chapter. a silvery halo surrounded the armour, designed specifically for the purpose of weakening daemons when they drew close. in his right hand, Stern carried a nemesis force sword that stood as tall as he did, whilst upon his left arm a wrist mounted storm bolter sat, the two barrels smoking after being fired so much.
Stern rose to his feet as he saw a blue halo of light flash in front of the teleporter, and he saw Castellan Crowe spat out by the blue light, followed by five white helmeted Purifiers.
Stern offered out a hand and hauled the Castellan to his feet.
&quot;only five survivors, Garran?&quot; he asked.
&quot;i count it as four more than you, Brother-Captain.&quot; retorted the Castellan.
&quot;aye.&quot; replied Stern sadly, &quot;we lost squad Verac to a group of Juggernauts in the southern pass, all twenty of them.&quot;
&quot;emperor preserve them.&quot; replied Crowe, a moment of silence fell over the group.
the silence was briefly cut short by a figure striding into the control room.
the group turned to see a man in shining gold armour and red underlay walked confidently across the floor of the control room. his ancient face was lined with the long years of constant battle. his bald head gleamed in the mechanical glow of the humming machinery. Inquisitor Benjamin Mordecai of the ordo hereticus stood with his arms folded, a look of grim determination on his face.
&quot;alright.&quot; he said in a deep voice, &quot;lets get back to work.&quot;
&quot;what is our next move?&quot; asked Crowe as the Grey Knights gathered around the Inquisitor.
&quot;we&#x27;re bailing out.&quot; said Mordecai simply.
&quot;but our strike cruiser was downed by the blasted warp storm!&quot; put in Stern, losing patience.
&quot;indeed.&quot; said Mordecai formally, &quot;but help has arrived. a fellow Inquisitor by the name of Lorelei Grey has made contact, and her warriors are coming to pick us up.&quot;
&quot;good, then we can barrage this place from orbit!&quot; roared Crowe. his statement was greeted by roars of agreement from the five Purifiers.
Stern grimaced at this. he did not like to kill an entire planet if he could help it. there were still citizens on this planet. those too poor or too foolish to leave were just left behind by sector command.
&quot;is there not something else we can try?&quot; asked Stern.
&quot;for now, we will defend the bastion.&quot; replied Mordecai calmly, &quot;we have Daemons approaching from the north and south, and we must prepare. how many Grey Knights do we have left at our disposal?&quot;
&quot;thirty.&quot; growled Stern. he hated people who merely saw soldiers as numbers, to be subtracted and divided by the whims of a superior who enjoyed playing god. these were his men, courageous and honourable. Stern felt this more so amongst soldiers such as imperial guardsmen, who had families and homes to protect.
&quot;then we divide them between the north and the south. Castellan Crowe, you and your Purifiers, along with ten others will defend the north. Stern, you and a retinue of Terminators, along with ten others will defend the south.&quot;
&quot;i don&#x27;t think...&quot; began Stern.
&quot;it was not a question, Brother-Captain.&quot; snarled the Inquisitor.
the Grey Knights filed out of the room, followed by the Inquisitor, so that only Crowe and Stern were left.
&quot;i wish it wouldn&#x27;t come to exterminatus.&quot; sighed Stern, &quot;this planet dosen&#x27;t deserve death.&quot;
&quot;</pre>

右文（仅阅读辅助）：

<pre>it has ever been thus, Brother Stern.&quot; said Crowe beside him, &quot;it would be folley to try and change the will of an Inquisitor.&quot;
&quot;i wish we didn&#x27;t have to answer to such heartless bastards.&quot; spat Stern</pre>

### 位置9363476｜high_activation｜z=0.1804833

上下文9151，目标offset=899，目标token=">"；原文档未知。

包含目标的模型可见前文：

<pre> warning Saudis fighting in Syria will be arrested when they return home.

Iran argues Syria&#x27;s neighbors cannot afford to watch the conflict spread in the region. In recent months Iranian Foreign Minister Ali Akbar Salehi has traveled to Jordan, Turkey and Saudi Arabia to bridge the gap in their understanding of Syria&#x27;s future.

Abdulahian claims the three states are drawing closer to it in seeking a regional political solution to the crisis in Syria, which in Iran&#x27;s view should encourage talks between the Syrian government and opposition forces.

Jordan is concerned by the overflow of Syrian refugees, Turkey faces internal unrest partly for mismanaging the Syrian crisis, and Saudi Arabia is wavering over its Syria policy given Washington&#x27;s reluctance to heavily arm rebels even with emerging evidence that the Syrian army used chemical gas to contain the rebels.

The head of Iran&#x27;s National Security and Foreign Policy Parliamentary Commission, Alaadin Boroujerdi, says Washington&#x27;s reluctance is because the heavy arms could be used against Israel.

Israel should take this as a warning from Iran. In May, Israel said it attacked an Iranian missile shipment to Hezbollah in Syria, and the Syrian army said it exchanged fire with Israeli forces in Golan, which the Iranian-backed Press TV reported. The Iran-based journal, Iranian Diplomacy, termed the attacks a &quot;game changer.&quot;

An alarmed Iran signaled a shift in battle front tactics in Syria. Abdulahian warned that he doubted Israel could defend itself if Arab rebels were to attack the Golan Heights, a segment of Syrian territory which Israel took over in the 1967 Arab-Israeli War.

Iran does not want a takeover of Golan. Its occupation by Israel lets Iran shame Arab leaders for their inability to reclaim it. But an upheaval in Golan might suit Iran if Israel does not stop attacking its allies.

On May 30, Assad warned Israel he was under pressure by the Syrian people to retake Golan. A conflict between Israel and Syria is bound to spread to Gaza, the West Bank and the Sinai where Arabs dispute the 1967 occupation by Israel of those lands.

It is uncertain if that is a fight Assad wants. On June 6, the Syrian army retook a crossing in Golan from Arab rebels, signaling to Israel that it had a better chance of protecting itself having Assad in power.

That might just be the right reason to talk to Iran when it comes to Syria.&lt;|im_end|&gt;Advogato blog for johnm Advogato blog for johnm en-us mod_virgule Thu, 12 Dec 2013 07:23:57 GMT Thu, 4 Mar 2004 17:34:14 GMT 4 Mar 2004 Ob-it&#x27;s been a really really &lt;b&gt;really&lt;/b&gt; long time... &lt;p&gt; For today, this is just a wee note about my &lt;a href=&quot;&quot; title=&quot;Diary entry for 28 October 2002&quot; &gt;previous entry&lt;/a&gt;, in which I had found an inadequacy in &lt;a href=&quot;&quot; &gt;ccache&lt;/a&gt;&#x27;s hash. It had returned a cached object with incorrect file paths in its debug information, which the linker was then printing out in warnings and error messages. &lt;p&gt; Other people must have been noticing that too, because soon thereafter ccache acquired a &lt;tt&gt;CCACHE_HASHDIR&lt;/tt&gt; option to put the whole path into the hash calculation. &lt;p&gt; That wouldn&#x27;t help me much, of course, because with my build directory varying daily it would be the same thing as just disabling the cache entirely! Instead, I wound up using a small sed script to canonicalise the logs before I looked at them. &lt;p&gt; Pretty stone age, but effective. Tue, 29 Oct 2002 02:24:56 GMT 29 Oct 2002 &lt;b&gt;Extreme panic!&lt;/b&gt; &lt;p&gt; Each time I do a full &lt;a href=&quot;&quot; &gt;prc-tools&lt;/a&gt; build, I get a 1.3 Mb build log and sometimes I even look at it. (Building prc-tools means building two binutilses, two GCCs, a GDB, and a few other bits and pieces. Along the way you build four BFDs and six libiberties. So that log builds up pretty quickly!) &lt;p&gt;</pre>

右文（仅阅读辅助）：

<pre> At the moment, due to popular demand (three FreeBSD whiners :-)), I&#x27;m working on making --enable-nls work properly. To be sure, there&#x27;s a bug here in the current top-level prc-tools, and I&#x27;m glad to be finally looking into it. &lt;p&gt; So I&#x27;m comparing the logs from builds with and without --with-included-gettext. I look at</pre>

## Feature 16323，h_V=1

### 位置111813｜random｜z=0.01624904

上下文109，目标offset=260，目标token="):"；原文档未知。

包含目标的模型可见前文：

<pre>4486. 
  36. ^ Sugranyes G, Kyriakopoulos M, Corrigall R, Taylor E, Frangou S (2011). &quot;Autism spectrum disorders and schizophrenia: meta-analysis of the neural correlates of social cognition&quot;. PLoS ONE 6 (10): e25322. doi:10.1371/journal.pone.0025322. PMC 3187762. PMID 21998649. 
  37. ^ Fadiga, L.; Craighero, L. &amp; Olivier, E. (2005). &quot;Human motor cortex excitability during the perception of others&#x27; action&quot;. Current Opinion in Neurobiology 15 (2): 213–218. doi:10.1016/j.conb.2005.03.013. PMID 15831405. 
  38. ^ Shamay-Tsoory, S.G. (2011). &quot;The Neural Bases for Empathy&quot;. The Neuroscientist 17 (1):</pre>

右文（仅阅读辅助）：

<pre> 18–24. doi:10.1177/1073858410379268. PMID 21071616. 
  39. ^ Nishitani, N.; Avikainen S. &amp; Hari R. (2004). &quot;Abnormal imitation-related cortical</pre>

### 位置1419481｜random｜z=0.02467189

上下文1387，目标offset=316，目标token=" scene"；原文档未知。

包含目标的模型可见前文：

<pre>.

Just this week, my high-school senior watched former President Bill Clinton&#x27;s uncensored impeachment hearings in an advanced-placement U.S. government class. Fittingly, the teacher labeled that day&#x27;s lesson on the whiteboard as “Watching Disturbing Videos.”  (I appreciate that the American classroom is showing the future of our country how not to behave when you are in the White House! But I digress.)

As the film industry has realized, rendering historical accounts of our country&#x27;s past on the big and small screen has broad and significant audience appeal.

Whether it&#x27;s Steven Spielberg&#x27;s depiction of a single man&#x27;s attempt to save as many Jews as he could from the Nazi genocide in &quot;Shindler&#x27;s List&quot; (also shown in classrooms), to bringing to life a crucial moment in our country&#x27;s politics in &quot;Lincoln,&quot; to Katherine Bigelow&#x27;s portrayal of American bravery while battling in foreign territories for the sake of our homeland&#x27;s freedom in &quot;The Hurt Locker&quot; and &quot;Zero Dark Thirty,&quot; to Quentin Tarantino&#x27;s sadistic blend of film noire (&quot;Inglorious Bastards,&quot; &quot;Djandgo Unchained&quot;), these stories grip us because they tell us about the heart or hatred that humankind has and is capable of directing at other humans. 

More importantly, these films show us in vivid and living color what we as a civilization must not forgets.  

However, criticism about the lack of truthfulness or historical fact in movies continues.

 &quot;Zero Dark Thirty&#x27;s&quot; torture scenes and &quot;Argo&#x27;s&quot; tarmac chase scene</pre>

右文（仅阅读辅助）：

<pre> are examples of the ongoing debate over accuracy versus artistic freedom in films.

Hollywood&#x27;s version of these events is now being closely scrutinized as a failure to stick to the facts and historical evidence in the making of these epic reels in favor of drama.

Such is the case with the recent controversy Spielberg&#x27;s &quot;Lincoln&quot; created when the format of the crucial vote to pass the 13th Amendment</pre>

### 位置1651680｜random｜z=0.012709

上下文1614，目标offset=211，目标token=" Latin"；原文档未知。

包含目标的模型可见前文：

<pre> Song and Dance Ensemble. Four years later, he received the same job at the Pyatigorsk Musical Comedy Theatre. By the age of twenty, he had reached perfection in folk and character dancing, and had studied the fundamentals of classic ballet.

After Chechens were deported, Esambayev was employed with the Kyrgyz Opera and Ballet Theatre, where he danced principal parts in Swan Lake, The Fountain of Bakhchisarai and The Sleeping Beauty, as well as in the first Kyrgyz ethnic ballets.

After return to Chechnya, he became solo performer of the Chechen-Ingush State Philharmonic Society to quit ballet and turn to ethnic dancing of the whole world.

He staged dances for himself. The Indian ritual dance The Golden God, the Spanish La Corrida, and the Tajik Knife Dance were his first endeavours.

Esambayev performed to full houses in Chechnya-Ingushetia, Moscow and in every part of Russia.

He made a triumphal tour of France and Latin</pre>

右文（仅阅读辅助）：

<pre> America with the Soviet Ballet Stars company in 1959. He immediately started to perform any local dance he saw. The Brazilian Macumba dance became legendary in his rendition.

The tour brought him global renown. Immediately after it, he established his own company to travel all over Russia and the world with his programme Dances of the World’s Nations. His triumphs were unprecedented. Experts and the</pre>

### 位置2093459｜high_activation｜z=1.142836

上下文2046，目标offset=0，目标token=" different"；原文档未知。

包含目标的模型可见前文：

<pre> different</pre>

右文（仅阅读辅助）：

<pre> as night and day when comparing the game against OSU to the game against USC.

Against Oklahoma State, the Bulldog offense only generated 257 yards, only had 58 penalty yards and Joe Cox only completed 50 percent of his passes. The defense held the explosive Cowboy offense to 307 total yards.

Against South Carolina, the Bulldog offense had </pre>

### 位置2185547｜high_activation｜z=1.142836

上下文2136，目标offset=0，目标token=" different"；原文档未知。

包含目标的模型可见前文：

<pre> different</pre>

右文（仅阅读辅助）：

<pre> predicament.

To the casual listener compression can sound &quot;good,&quot; mostly because it makes the music seem louder and punchier, and once music&#x27;s natural soft-loud dynamic shifts are squashed flat music is easier to hear in noisy environments like cars or over iPods. Compression reduces the need to adjust playback volume--because it&#x27;s always nearly the same volume--loud.

Engineers worry that if they</pre>

### 位置2497582｜high_activation｜z=1.142836

上下文2441，目标offset=0，目标token=" different"；原文档未知。

包含目标的模型可见前文：

<pre> different</pre>

右文（仅阅读辅助）：

<pre> view, saying, &quot;It&#x27;s not really fair to say he&#x27;s bad at endings. He&#x27;s not prescriptive as a writer, so therefore the end will sometimes be inconclusive. Everybody expects a resolution, just like everybody expects to be happy. He&#x27;s pointing up the chimeras that contemporarysociety has highlighted. The penultimate sentence in the last book is, &#x27;this is not the</pre>

### 位置4178799｜random｜z=0.008497573

上下文4084，目标offset=289，目标token=" for"；原文档未知。

包含目标的模型可见前文：

<pre> to push pop&#x27;s musical conventions forward. And even if his new album is his most off-kilter, it doesn&#x27;t mean he&#x27;s missed the mark.

BLOCK: Oliver Wang writes about music for The L.A. Weekly, Vibe, and The new album by Kanye West is called &quot;808s and Heartbreak.&quot;


WEST: (Singing) Goodbye, my friend. Will I ever love again? Goodbye, my friend. Will I ever...

BLOCK: You&#x27;re listening to All Things Considered from NPR News.






Support comes from:&lt;|im_end|&gt;




And I&#x27;m Melissa Block. More than a year ago, Pakistan&#x27;s army went into the Swat Valley in the northwest of that country. The army promised to get rid of Taliban militants there. Many Pakistanis thought the military would win in a few weeks, but the war is still going on and the Taliban is stronger than ever. As NPR&#x27;s Philip Reeves reports, the conflict is taking a nasty turn. In the last two weeks, there has been a spike in the number of corpses dumped in the streets - victims of tit-for-tat assassinations.

PHILIP REEVES: Sometimes it&#x27;s just one body found lying in the open as the sun rises over the valley. Sometimes it&#x27;s more. Sometimes the bodies are beheaded. Sometimes they come with a note, threatening death to anyone who moves the corpses before a stated hour. It&#x27;s not easy for</pre>

右文（仅阅读辅助）：

<pre> Western journalists to visit Swat. The militants have a strong presence, but you can call people there albeit on a crackling phone line.

Mr. SIUDIN YUSATSA(ph) (Peace Activist, Mingira, Swat Valley): Yeah, yeah, yeah, (unintelligible) please.

REEVES: Siudin Yusatsa is a peace activist in Sw</pre>

### 位置4588616｜random｜z=0.03639064

上下文4484，目标offset=882，目标token=" web"；原文档未知。

包含目标的模型可见前文：

<pre>uence and errors in the information management process while maintaining good flexibility in experiment production pipeline.

thumbnailFigure 2. Experimental workflow, shared information and actors of microarray experiment production formalized in MicroGen system. BIO.: Biologist; S.O.: Spotting Operator ; H.O.: Hybridisation Operator; P.O.: Processing Operator.

Finally, use of server-side web technologies, which allow centralization of data archiving and processing operations and easy deployment of suitable graphic user interfaces (GUI), enables MicroGen to easily provide collaborative work support also among different actors located in a distance. This choice makes faster and easier both managing and maintaining the system, and deploying the developed functionalities and GUIs to all its remote clients, besides lowering system maintenance costs. In fact, the employed web technologies allow using MicroGen everywhere an Internet/intranet access is available, requiring only a common web browser without any additional plug-in. The system is also simple to run. It only requires to be installed on a server computer with an Internet Information Server as web server.

MicroGen system is freely available for academic and non-profit use at: webcite.


MicroGen facilitates workflow management of spotted microarray experiment production, provides an efficient way to gather complete experimental information, and supports collaborative work. In fact, thanks to its well-defined core database architecture, MicroGen facilitates collection and storage of all experimental information according to the MIAME standard. Ordered availability of such information allows subsequent efficient and effective analyses of experimental results.

In addition to orderly store all information produced, by easing the process of information sharing, MicroGen represents a valid support for collaborative work even among research centres geographically distant from each other.

MicroGen also facilitates experimental data comparison. In fact, it allows saving quantitative results also in a standard text format. This increases portability and compatibility of results. Identification of results from experiment with similar characteristic is also facilitated thanks to the complete experimental information orderly stored within the system.

MicroGen graphic user interface is very simple and intuitive, providing an easy method for a biologist or a biotechnology technician to read or collect information about performed microarray experiments. The whole procedure of collecting experimental information is driven by the system, and all the steps to follow are simple and immediate. Forms with multiple choices or dynamic links are presented within web pages in order to quickly access a great number of different data. User&#x27;s information, present progress status of an experiment, its MIAME data, and experimental results currently uploaded are all viewable at any time to all actors involved in the experiment.


Using a relational database developed in MS-Access, we implemented a core data repository specifically structured to collect the whole information about all the actors involved in the production of spotted microarray experiments. The tables of this central database are grouped in three sections: a section containing information about the experiment itself and the additional files (such as quantification results) associated with the experiment; a section with the data about each user who worked on the experiment; and a MIAME section, which contains the whole information, according to the MIAME standard, about the experiment production (Figure 1). MicroGen core engine was developed using Microsoft Active Server Page technology, with Javascript language for scripting, and connections to the core repository were implemented by using Microsoft ActiveX Data Object technology. Hyper Text Markup Language 4.01 was used for formatting the graphic user interface implemented as web pages.

Authors&#x27; contributions

SB and DC developed the whole MicroGen program and its core database engine, and wrote this paper. MM was responsible for project conception and coordination, developed clone&#x27;s additional databases, and contributed to write this paper. FP provided supervision and funding of the project.


  1. Brazma A, Hingamp P, Quackenbush J, Sherlock G, Spellman P, Stoeckert C, Aach J, Ansorge W, Ball CA, Causton HC, Gaasterland T, Glenisson P, Holstege FC, Kim IF, Markowitz V, Matese JC, Parkinson H, Robinson A, Sarkans U, Schulze-Kremer S, Stewart J, Taylor R, Vilo J, Vingron M: Minimum Information About a Microarray Experiment (MIAME) – toward standards for microarray data.


  2. The Microarray Gene Expression Data (MGED) society. The MIAME checklist [] web</pre>

右文（仅阅读辅助）：

<pre>cite

  3. EMBL-EBI European Bioinformatics Institute. The ArrayExpress Database [] webcite

  4. Barrett T, Suzek T, Troup D, Wilhite S, Ngau W, Ledoux P, Rudnev D, Lash A, Fujibuchi W, Edgar R: NCBI GEO: mining millions of expression profiles-database</pre>


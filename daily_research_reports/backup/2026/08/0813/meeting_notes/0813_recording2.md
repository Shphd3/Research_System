0813_ 分析混杂_原文
2026年08月14日 17:24
发言人1   00:00
是哪个男的？男的是19是吧？

发言人2   00:03
对，浅蓝的就是有纯蓝的是20，然后这个棕色的是20. 

发言人1   00:08
棕色是25。比如说他们之间的区别，比如我把他们的difference画一下，能看出啥来着？

发言人2   00:18
如果把方差直接剪的话，这个图我没画，然后我。对，然后下面这个图可能会明显一点，就是这个是第零层和第一层。或者是他们在某些方案上确实有差别。

发言人1   00:44
因为我们认为模型每层肯定学了新的东西，对吧？这个肯定的对不对？

发言人2   00:49
对的。

发言人1   00:50
就是他每层肯定学了新的东西，然后那他每层之间肯定有不同，对不对？对，肯定有不同。我如果我把很多层，就是我把很多个token，把它信息混在一起来看，它应该具有一个统计的特征，对不对？是的，我们认为它应该有统计特征。然后我们现在这个问题怎么找到这个统计特征，对不对？

发言人2   01:13
是的。我我我我现在觉得这个就是我觉得是我们目前的分析方法可能有有局限性。就是我觉得有我们现在的分析方法，一个是我们假设了必须通过比较不同层的标准才能找到。但是我觉得就是你因为你的深层表上是包含了浅层表中的信息的，所以我觉得其实我记得。

发言人1   01:39
我记得是不是应该这么做，就是说不应该拿个1000，应该是这样。就是说就是我每个token实际上我从第一层到最后一层，对不对？是然后我是不是应该把每一层，就是咱们刚才是说1000乘100万个向量，对不对？如果是一天成本100万，如果我算difference的时候，我实际上是把这一层的信息混在了一起，对不对？

发言人2   02:06
是对。

发言人1   02:07
然后我们实际上就是要处理的那个，你们是不是等一下，另外一个也不是给我发的消息。

发言人1   02:25
等一下，不好意思，我。

发言人1   02:41
就是。就是我觉得是不是应该每个token从第一层到最后一层对应的先咱们先做减法。

发言人2   02:55
就是只看一个token的时候，不看不同层面。

发言人1   02:58
但是这个剪什么是这样，比如我先做一组升降机对不对？我先做一个正交机，我做完正交机之后，我把每层BO这层100万的token对不对？然后我把这一层第一层和第二层对应100万的token推荐的那个500维先做一个减法，然后算这个减完之后的这个500乘100万，看它的分布。

发言人2   03:30
点完之后的500场. 

发言人1   03:32
但是实际上你们摆是不就是这么做的。我意思就是说我因为这事我也没想好。就是我也没想好，就是我就是在想，第一反正咱们这个咱们不多说别的，咱们就说只有一个token好吧，咱们就说一个token对吧，就是我这个玩意就一个token对吧？然后我第一个进来之后，他他他有一个然后到第二层到第三层，对不对？我们只想看他每层这一个token长，就是多学了点啥东西。

发言人2   04:06
吧啊是对吧。

发言人1   04:07
就是那我怎么比较对不对？我一个token我还是可以一组一组中交？我认为这个token在这组正交机上都有投影，对吧？对对对，反正我就讲哪个通用，然后就比较这个token在每个层上，就是这个500维上面的做个投影的差别，我肯定是可以做的，对不对？但是实际上你们原来你做的是不是也是这样？

发言人2   04:42
原来做的应该还是有区别的，因为是每个方向上算出来是很多个token的统计。是什么？

发言人1   04:49
不是你反正是有一组正有一个500个1000维的正交机了，对不对？咱们有主机了对吧？咱们第一讲，假设这个就叫张馨子，张坚，我们定一个张馨子空间对吧？然后呢我就想在这个张馨子空间来度量，这是这些数据的difference生成的difference？然后我现在有100万个token对不对？对，然后我有这个100万的通用，在张鑫的这个叫叫咱们这个叫叫张子，就叫新子的空间，对吧？

发言人1   05:16
薪资空间我想看。我原来的做法是我把每一个现在某一位生成的每一个某一层生成的向量。比如说我们可以先看看它的CODCOI的这个或者body head那个那个tension输出那些东西。我在这个500个向量身上，在此空间都做过投影，得出了一个500维的一个向量对吧？对，然后我得出这个500位的向量，然后我这个500维的向量，然后我是100万个token都坐着，所以我是个500乘100万对不对？

发言人1   05:51
对，原来咱们做法是想看500乘100万的万2万次，对不对？然后算出virus，然后再比再和这个virus和前一层的比对，这个确实是有问题的对吧？我应该是把这个500乘100万和前面那一层的500乘100万先减。明白了吧？对吧？就先减减就是说我对应的token和token减。那第一个token的500，每一个和第一个token在第一层的500人和第一个token在第二层的那个500维先剪剪出一个difference出来对不对？我就有100万个定粉丝对吧？

发言人1   06:36
然后100万个difference实际上这时候我不用算variance了，就是在100万的difference上边。实验过100万个difference，就算100万个就是500乘100万个difference。实际上我就可以算，其实我就可以算这个500个均值和500个方差了，对对对吧？是实际我应该做这个事儿，对吧？

发言人1   07:11
比如江西你是一个token，安瑞是个token，王瑞金是个token，对吧？就是说你们经过每一层，你想看你一层和下一层你学了一些什么新的知识，对不对？那你的心态知识哪来的呢？实际上张欣你看你的知识哪来的，你就是比如假设你就三个头围，你和黄老金和和4个，然后还有星宇，你们四个偷的影响你的信息是哪儿来的？你的信息实际上就是从星宇瑞军和是星宇瑞军和安瑞的抄的，对不对？

发言人1   07:44
因为你就是一个团队，意思是一个上下文决定，你sell attention直播就把大家旁边信息整合了一下，对不对？对，所以就是说在每一层做的话没意义，对吧？学习单元还是把信息混一会儿了，对不对？

发言人1   07:58
对我应该去看你在一层里边是不是就是一个token在不同层之间。比如说你第一层你没有混淆，就是你对不对？那第二层你在做到第二层的时候，你把比如安瑞的信息拷过来了，对吧？第三层你把黄尔君的信息拷过来了，那你想你在那个就500位的投影，你在不同层之间difference，那你第一次的difference就应该是安瑞这边。第二就是安瑞，就是黄瑞军，对不对？

发言人1   08:25
所以但是如果你在某一层先做一下，这个就是一个整合。你还是华润金安瑞，反正你这层信息就是这么多人。是的，是不是？我认为因为这个问题是没招，这个问题我也想不出来，因为我我只有一个information，对吧？

发言人1   08:42
我也自己做实验，做完实验之后我就说说这个不对，没有问题对吧？那不不对，不是个坏事。当然这来递送文章那是个坏事对吧？不对，他不是个坏事。我就琢磨，因为这个因为我们的直接上，他他他不应该没有，不应该有问题，对不对？肯定是有区别的，我只要找个区别在哪儿，对不对？

发言人1   08:58
但是核心就是说什么叫区别？因为他上半天是本质上的事情，就是把这层的信息和前层的之前整合在一起，对吧？是的，对，就是不是不是我说我会说什么，就是我这一层就是我每一层就是把这一层的就是我这个头子和旁边这些头发混在一起了，对不对啊啊啊对，那我的比较肯定是得跟你token比，对不对？是的，比如星宇离你很远，对吧？你一层绝对没有心仪的信息。

发言人1   09:26
到第二层的时候，你做了一个长城的attention之后，你把信息给信息加回来了对不对？信誉对不对？对对，就是这样的。这个时候你你你算的区别就是说你和实际上就把给剪出来了，对不对？是的，对，这是一种道理对吧？

发言人1   09:43
但是咱们再看原来的，我们现在做法有什么问题，吧？比如说我在一层，我一层就是你你有一个500V然后瑞金有个安安瑞有个500倍，然后心里有个500倍，这是个信息对吧？那然后我们在这个里边算virus对不对？

发言人1   09:58
对，这个partners实际上就是比如说你和星宇到底有多少区别，你和瑞金有多少区别，对不对？对，变成这个东西，这个东西实际上我觉得到深层时候可能确实会变一点，但是我觉得变化不大，因为毕竟你还是这么多token，对不对？对，所以这里边的意思实际上是没有变化的，对不对，是的，对，你们这是你的做法。那个瑞军，安睿和那个星期有没有人说该做过这种做法，或者有不同的做法？

发言人3   10:29
有的，就是我已经说过的，就是我的做法就是说就是最底层的一些东西，我们总是认为深层和浅层总之有相同的东西，那么我们我就去找他们相同的东西到底在哪个子空间里面，那去掉了这个子空间外的才有可能是深层新的东西。我是有这个有点。

发言人1   10:50
对，那你先找他们的相同点，那你怎么找相同的？

发言人3   10:53
对，三方点就是这个地方，就是我的这个。例如这里就是说我我我的千万点。就是如果浅层的某一个方向上，数据的token在这个方向机构很大，那么我理应在深层的某一个方向上也找到一个方向，这个方向上对于那些数据的token都接吻很大。所以就是我就是我希望找到那些方向，使得token在这几个方向上的激活，在申请层是一样的，用这种方式来找那个。

发言人1   11:19
相同的对对对对，但是我们在大，那我们实际上就是说白了就是说这实际上我们认为他他他没有一个只有浅层。我们不认为他的某些四层颜值，包括common信息某些是不一样的，对吧？我们不认为它是个零和一的游戏，对不对？是的，这个你没法说我钱，三百维就是全是com信息，后边两百维这个东西就不存在了，对不对？那你咋办？就是你怎么找common，common我可以阿里就是说每一位都是common，对不对？每一位都有common信息，每一位都有special的信息，只是他不太一样而已，对不对？

发言人3   12:01
那我这里的话，我只能就是那他应该回答不了这么细的问题。他只能说比如说我们社保。

发言人1   12:09
因为我们认为他已经都映射到一个低位子宫间上去了，对不对，是的，对，我们已经认为他都已经接到一个DDV子空间上去了，对吧？

发言人1   12:27
所以因为它都是用稻子地位子空间的时候，所以说白了就是说就是黄瑞军你的你你第一层，你第二层加了点儿锐，加了点儿睿的信息。然后我就想看你第二次问题，他们之间有什么区别，对不对？是的，所以实际上假设如果我们认为整个就是个低质子空间的话，那也就是说我无法从过从那个维度上来区分对吧？大概就是在500维箱混在一起，对不对？是啊，那我只能在500维里边找到的这个粉丝。

发言人3   12:55
对不对？对。

发言人1   12:57
对吧？就是说比如说你第一层数学用了千500位，第二层离散数学也用了这500位。线性就是比如说抽象代数也用了这五百维那，我就想看这500维之间的difference，对不对？

发言人3   13:09
是的。

发言人1   13:10
对，那那这个difference原来我们的想法是说我第二个维度，第一个token是比如说这个线性代数对吧？后面第二个token是离就是这个离散数学吧，就十万代数学。第二离散数学，我们想看他们俩之间的这个区别，这个玩意儿的区别对吧？但是因为它里边都带着数学，所以它的learns实践可能不一定好，对吧？是的，对，然后如果我把比如说你第一层和第二层减，第一层你是你第二层是你关瑞，你剪完之后应该好像应该是带着一堆，就是简单的一个顺序，安瑞对不对？

发言人3   13:43
至少安瑞会剩更多的信息。相比于这个我自己就intuition上好像是对，是的。

发言人1   13:49
好像应该是这么底，对不对？也就是说我就相信说白了就是说我把这个问题简化到一个极简的层面，因为一个token是没法用的。这个就比如说你和张欣就那两对，第一层你是你张欣张欣对吧？比如张欣是一，你是零，对不对？那第二层就得变成了你就是第二层你就是你们俩混在一起的时候，你变成了一个。比如张熙变成0.5，你也变成0.5，对吧？但是你可能两个还是不太一样的，你是0.6，然后是张鑫是0.4对吧？假设是这样，那这样结果的话，我要算difference的时候，我其实我也不能说我不能那么算，对不对？实际上那样的话就是我们俩的difference就是你和张鑫的difference between小了对不对？

发言人3   14:35
对。

发言人1   14:35
应该是变小了，然后在浅层会变态。但是我另外一种做法是这样，我把第一层张鑫减掉，他剩个零点，就是剩一个负的0.6。你和你你简单说你是个正的0.4，对不对？然后这是这个difference，这个difference里的时候就会比较大对吧？

发言人3   14:51
我我们对对对我们对研究院应该是是我们都是认为是对的。那那我感觉我这一方面就是最多只能解释到我尝试找一个所有token在某些方向下基本不变的方向。

发言人1   15:07
这就只能认为我觉得实际上这个问题可以这么做，就是实际上这个问题不难解决，就是不难分析是这么做。你不要拿个100万，他ok，你就是拿十个token，就是十个token云眼是可以分析的，对不对？我训练完了之后，我就是个头盔，就是什么今天下雨了，我不想被淋湿，所以我在想对不对？对，就这么一句话。然后我就让他走一遍这个模型，然后我就看这个token哪层的一个个来分析。肉眼来看我我理解。

发言人3   15:34
对我理解刚才你跟丹妮说的那个英雄园，这个对我是高丽人。

发言人1   15:39
那行，那那明白那行，那个安瑞，你。

发言人4   15:42
我问一下。

发言人1   15:43
我这边等等一下。

发言人4   15:49
我这边就是跟瑞军那个思路有点像，但是我是说想找到一个低质的空间，然后是一个新的地址空间，然后就是可以把浅层和深层的表征都映射到这个相同的空间里面去做分析。对，然后这边这个公式就是说这个X是浅层的表征，然后我还是深层的表征，然后我在这个浅层和在浅层的表征空间里，找到一个从地位映射到一个比较低低质的R这呃这个比比如说这个低质的支持R的这个映射关系，然后就是把这个浅层和深层的表格放到同一个空间里去比较。然后我我是认为在这个空间里面，就是我的这个浅层的信息和深层的信息的它的相关性是比较强的，然后会得到这么一个低质的贡献。然后在这个身份的表格里面，没有办法被这个低质空间所表示的部分，我我我认为是到那个在深层新产生的信息。

发言人1   16:55
我觉得实际上我觉得不应该这么做。其实就是说我们最后想构建一个子空间，你想你本正想问你是怎么回事，你即使想构建一个子空间，我明面上是说我想这个构建的子空间能够三号有效的度量每一层新产生的features的对应的子空间。对不对？对，就是说就相当于我这边为啥？因为我是吧？我getting能够分了，能够区分这个能够区分离散和这个组合，对不对？离散数学、组合数学离散和组合，我想分析这个区分这个东西对不对？对，就是我想做这个东西。

发言人1   17:32
那你想我为了达到这一点，我需要做哪几件事情？首先我希望找到一个子空间，这个实际上就是刚才黄晓军说的，就是我想找一个总监能够分开，就是和数学把它拆出去，对不对，对，是的，对，但是实际上我是不可能完全把数学拆掉的。但是我不管数学，我先不管数学，是我就想找到一个子空间。那个那个什么特别敏感，对那个就是组合和离散这个的特征的violence特别敏感，对不对？

发言人4   18:05
对，是啊。

发言人1   18:05
两个对象对这个特别敏感，对吧？那这个敏感实际上是黄荣军你前面说的那个想法，实际上没有第一步是没有错的。你实际上并不是说我就给一个二千做500个月，把前300个剩下剩。明白了，不是这个意思，而是说你想看我们每层产生的新的feature，在一个子空间中的sensitivity在哪些sensitivity最大，我就用它，对不对？

发言人3   18:29
这是我对我只是对你一直。

发言人1   18:31
想做这件事儿，对吧？这么做本身这个动机是没错的。但是你想你为了达到这一点，咱把这话再说一遍，我希望找到一个低质的子空间，这个空间具有什么特征呢？针对我们每层产生的新的feature，它的virus在这个子空间是最大是吧？

发言人3   18:54
对，这就反正可能不是弯的，但是肯定是某种指标，他肯定是星星星。

发言人1   18:58
星星星就是能够因为我virus 1，事实上我是想度量他们的区别对对对，因为我的目的是为了做给你挺对吧？嗯对我就相当于能够把线就是组合和离散这两词分开，对不对？那肯定是得能够有效度量他们俩之间的virus，对不对？是吧？

发言人1   19:15
是的，对，比如说假设简单的例子，我X轴是离散和组合，然后比如离散是一，组合是负？Y轴是数学？那我肯定是把X轴拿出来，对不对？所以从这个咱们先讲，就是咱先用这个东西，就是说我其实里面有三个文件夹，我希望找到一个低质的子空间，这是第一个关键字才能干嘛呢？能对每层产生的新的feature，明白吧？这是个新的feature，它的里边的violence能够做一个很好的度量。对，这基本上有三个东西对吧，这三个这件事情，那一个低质子空间，找到一个低质子空间，我们知道反正肯定就是前500维里头的，对不对？是啊，好像反正我们知道the candidate顶的是前500的，后边先不管了。

发言人1   20:02
然后第二我是希望找到新产生的feature，对吧？第二新产生的feature。什么叫新产生的feature？就是一共我们模型两层，第二层和第不不仅不同于第一层的东西，对不对？对，那怎么最简单呢？我把第二层的对应的哪个东西和第一层点掉了，就是这个是difference对不对？这个difference里边就相当于我有100万个token？

发言人1   20:28
这个defense或者两个东西，一个是离散数学，一个组合数学。我理想情况下就是一讲完之后就剩理想和组合了，对不对？然后我再看这就是这个东西在前100 5500位里找到对他的口味是最敏感的那些。

发言人3   20:42
对吧？

发言人1   20:44
那那我意思说白了就是我剪完之后，我就用那个剪这个东西也去做个SVD呗。

发言人3   20:50
然后去匹配前面的发展。

发言人1   20:51
或者不是不是以前不是用不是做SVD，应该是做一个口味儿。行，要算一个口味儿的那些得算个hisense。对不对？就是这两个矩阵相乘，相当于是500，就是一个是机器人。我现在是500乘100万，对不对？500万，然后我现在500万已经算100万，这算NTK还是算还是一份那个还是算那个那个feature information matrix。反正就是说我得是五百乘上100万，再乘上100万乘上500，最后得出一个500乘500的矩阵，对不对？这就是这个口味的存在问题，对不对？

发言人1   21:26
然后我再对他做SVD对不对？是这样，你数学比我好多了。我就是我现在是想干这件事情，就是我现在就这么说，这么说就是我现在咱们就假设就两个特惠，一个是组合数据，一个是listen to，对吧？然后我捡我钱能捡回来就剩我认为就是一个是离散，一个是组合的对吧？我是伊斯兰和组合合在一起形成一个矩阵，这个矩阵是什么呢？500乘2对不对？

发言人3   21:53
对的。

发言人1   21:54
我500乘2，我现在想算500乘2，我希望找到一个一一就是两个向量的，实际上就是两个向量对吧？2个500位向量，然后在这个能够最好的表达它的这个万儿子，对不对？但是我就是实际上这个时候我做做出来的，其实我这当然500乘2，最后你比如说他举行就是2乘2，对不对？

发言人1   22:14
不是，或者就是说我现在给你那个500乘100万的矩阵对吧？然后这里面就包括两个信息，离散数学和组合数学好不好？离散和组合对吧？然后我现在给你就是这个500乘以100万这样一个离散和组合的信息代表在一起了。假设离散占了一半，组合占了一半，对吧？Whatever我现在想想算他的conversation，这个时候我就应该是用这个500乘100万乘上它的转值100万乘500对不对？得出一个500乘500乘500的地震，对不对？

发言人3   22:42
对，然后在里面找方向。

发言人1   22:44
然后再找方向对不对？

发言人3   22:46
是的。

发言人1   22:46
是应该这么做，对不对？

发言人3   22:51
这个逻辑是就是找我们认为剪掉的那个表针的方式。

发言人1   22:57
是对的对。对，就是这个方法其实是这样的，我们认为还是这样的，就是我有一个假设对吧？因为我不知道答案，是一点点来降低这个就是我认为他都是在临时空间里，也是第一位空间里，对吧？然后他不可能在一个包围里头，然后是然后我认为每层一定是学点新的东西对，刚才咱们说就是我们把这个话在假设这个成立的时候，我们再往前推一步说，我们认为要希望找到一个第一就是子空间。然后这个子空间能够对每层新产生的信息，就是在他的他的这个变化能够找到一个最敏感的一个子空间，能够去度量这个的变化。

发言人1   23:42
好的，然后因为为什么呢你要做这件事呢？因为我就想在这层做getting，对对对吧，这几个向量其实最后就用于做getting，对不对？然后这个getting就是来决定现在就是我基于这个东西，我来决定到底该往哪折发，对不对？因为我假设我的下游任务就是为了这个代理人，对不对？行好，那行，那这样，你是怎么做的。

发言人5   24:09
我就可以上去了。好，我的方法是我的好方法和张鑫方法分析的一种有点像。就是我是把所有层的这个参数矩阵给它拼起来，就是MLP层的那个参数计算拼起来，然后去找其中的这个共同的方向，然后在这个共同的方向上面来进行分析这个attention的每每一层attention的方差。然后麻烦往下麻烦往下。再往下就看的那个图。

发言人1   24:50
好，但是实际上这个作品不应该是错的。因为你想的是我希望产生新的体育产业对吧？新的特征对吧？新的特征就是说我如果算进去covariance的时候，baLance的时候，我其实已经是在度量上的区别了对吧？比如说我不减第二层就是离散数理学和组合数学好吧？我就是然后我每个是一个伍佰维的向量，然后我有100万个token，然后我实际上就想看这个500乘100万在上面？但是只不过这时候我还是要做500乘以100万，在城市上100万乘500我还得做成一个500乘以500的然后这个就是要看他的covariance. 

发言人5   25:29
然后再看区别对不对？

发言人1   25:31
对的，你是看的conversation的。

发言人5   25:33
对，我我我看了copy的意思。

发言人1   25:35
然后我是绑了张鑫没看到张鑫。

发言人5   25:38
我们这个都是朴朴朴的，那个曲线都可以。

发言人1   25:41
但是最后张鑫你那块在看了吗？这个就是相当于是这样，就是说你没解没关系，你反正就是我找了一组正交机对吧，反正就是一个500个正500正相机。是的，然后我每个都是500乘100万，对不对？然后我们这个500乘100万，在这个某一层的500乘100万，我想度量他的virus，实际上我还是得500乘100万，再承认这个100万成本，把它变成一个500乘100，500乘500的时候，然后看住了他的威尔斯，对不对？

发言人5   26:07
对。

发言人1   26:09
不是我问张鑫的。

发言人2   26:10
张鑫你是我我之我之前也不是这样做的。

发言人1   26:14
你没就没就没做这个口碑上的矩阵，对吧？

发言人2   26:17
我没做口袋的举的，因为我是哪个方向独立。

发言人3   26:19
所有的方向我们没有把那个500个方案一起拿出来。我们这是单个方向的100万个值断的一个方向，是就每套跟他花了最大的风险。

发言人1   26:31
我想起来了。对，可能其实应该是在500维这上来做，不能在单位来了里做，对不对？因为我实际上是在比一个方向，就是我实际上是一个伍佰维的向量的difference，不是500个独立的向量的difference是500个独立的是标量的difference对不对？

发言人3   26:54
是的，所以就是说。

发言人1   26:55
我应该是一个500乘以100万乘上一个100乘500，这个口味是没错，是在这样做对吧？那个就是NDK对吧？你要填你的kernel对不对？反过来做的话，就是说如果我是100万乘500，再乘上500乘以100万，那就是feature information matrix。他们两个度量东西是不一样的，四个。

发言人1   27:27
我问一下GBT，然后问一下GBT。

发言人1   27:37
就是。

发言人1   27:45
等一下。

发言人1   27:54
Hello, I got to help . 

发言人6   27:56
with today. Yeah so I have . 

发言人1   27:58
a question here. So let's say, uh, we have a representation space which is five hundred, five hundred domain. Uh, sorry, sir, I have a representation space which is, uh, let's say, uh, the is the space is about, I say, uh, uh, is about five hundred factors. 

发言人1   28:21
Each vector is a thousand dimensions. Okay, so so then I have one meeting tokens. Okay, so each token is a one thousand dimension. 

发言人1   28:33
Okay, so, uh, what I want to do is I want to use this five hundred of a thousand dimensions. Uh, legislature is called the, I want to use subspace to somehow to find the differences of this one million tokens. Again, each token is a one, uh, one thousand dimensions. 

发言人1   28:56
So what I can do is for each token first, I do like mapping. So basically calculate the the projection of each token, this one thousand dimension vector until this five hundred, one thousand uh, subjects. So I get after this mapping, uh, uh, uh, we essentially start, I gave this a five hundred, uh, like projection, right, right. 

发言人6   29:24
Get the yeah yeah yeah yeah yeah yeah yeah yeah yeah the coke and is just a five hundred quoted vector of, yeah. You can compare tokens in the corner of its face and also look at what's left over outside of this place. 

发言人1   29:43
好的，谢谢。For each token. So overall, I have wandering poems. So then what I get essentially is a five hundred times one minute, right? 

发言人1   29:55
So in so now, I want to basically to do, to evaluate their differences. I think what I should do is I should do, what I should do is, let's say, this matrix, we call AA is one hundred times. I see. 

发言人1   30:08
What I should do is I should do a times a transform. So transformation, then I get five hundred by five hundred. Uh, matrix. This matrix is capture the covariance of this one meeting token. And in terms of projection on this subspace doesn't correct. 

发言人6   30:28
I'll make you check that just as egg the shape is right a times a transpose, give you a five hundred, five hundred matrix by itself. That's the uncensured second moment matrix of the personal fortune horrible variance. Subtract a meme projected cornet from every oem, then form the product and scale by one over n minus one. 

发言人1   30:49
Yeah. 

发言人6   30:50
yeah, yeah. 

发言人1   30:50
yeah. Go ahead. Yeah, go ahead. 

发言人6   30:52
Then the diagonal interest, then the diagonal entries, are variances along each protracted direction and the off diagonals shut, which protected directions varied. 

发言人1   31:03
Better yet, that makes sense. So in that case, uh, if I want to use this one to help me to essentially separate, classify separately a petition, this one million tokens into some groups, how should I do that? 

发言人6   31:20
Let me think about that. Forsake the covariance matrix helps file directions that matter, but it doesn't by itself. Group tokens. 

发言人6   31:28
A common move is to censure a duke. E, C, A. Keep the top components, then cluster the tokens in the reduced space with a million points. Mini batch came maize as lasalle devolved a gaussian nature. If you want soft memberships, choose the number of clusters by stability or silhouette style tracks, plus INTER. 

发言人1   31:49
Okay, okay, I think that makes sense. In this case, can you help me to write a marketing document to expect story and, uh uh, give me the U. L. For downloading the nature of the equations in the tech phone. 

发言人6   32:04
Can you do that? sure. I put together, mister. 

发言人1   32:07
Carrying a short note with . 

发言人6   32:09
the projections, covariance and clustering workflow. 

发言人1   32:13
And also in the document, can you help me not only say how should do it step by step, and also explain the rationale behind the wide, the basic? Doing this way is correct. 

发言人6   32:27
I wonder that. 

发言人1   32:28
Okay, thank you. 

发言人6   32:31
I'm adding the wretched now too. Projection preserves the same moon of hereabout covariance finds dominant variation and P, C, A, D noises before clustering. 

发言人1   32:41
Yes, yes, totally. Thank you. 

发言人6   33:34
I put the fool right up in the share timeline with the equations . 

发言人1   33:40
and latex um yeah, okay, got it. Thank you. Oh, so, uh, I think I don't think the equations are written. India, the tech phone, can you double check? Let me tell you what you are seeing. 

发言人6   33:56
The mark gallery source, mark galaxy source is using a standard latex delimiters. So the equations are in latex form in the file. If for saying plain text, that's likely to pretty word. 

发言人1   34:09
No, no, no, no, I need a telephone. This is not a telephone, and the, uh, you can see that if you do a screen shot of my screen, you will see this visualization is completely wrong. 

发言人6   34:21
Let me check what's happening in your preview noise. 

发言人1   34:48
So do you see the problem? 

发言人6   34:51
Yes, I see the issue of you are opening the raw mart dow foul in a chrome. So the lake pep's cousin being rendered. 

发言人1   35:00
So then where is the correct file button . 

发言人6   35:03
brought you the rendered version? The rendered document is that top now and the markdown was forced as there too. 

发言人1   35:19
Okay, okay. Now I think this is all right now. Okay, thank you so much. I have talked to you later today. Okay, thank you . 

发言人6   35:25
anytime I have. No. 

发言人1   35:27
yeah, but yeah. 行，那咱们看一下，看一下那个，你们在吧？

发言人5   35:37
在的在的在的在的在的。

发言人1   35:39
等一下，我看一下，调一下screen。对，你看GP多好用，你看他是这么做的，就是说只有100万个头壳能看到屏幕，然后这每一个是1000人为的。我要找一个reference subspace，然后能够使用这个东西，怎么做呢？就是说这self swift splash right signal to compare if you have also on the current prevention coordinate，然后就是说这个等于the projection subspace就等于这个。然后这是一个fine honey project，every token, 然后center的data，因为你要求一下center data，这样才是covers，然后这样算一个东西，再做一下PC，把PC最大的那几个东西来做。明白了吧？明白，我把那个我一会儿把那个，我现在给我看看，我那个文章转转，我可以直接给你发群里面看一下，对吧？这个当然就reason一下。

发言人1   36:53
我想问一下。

发言人1   37:24
那个叫什么通用，这个就是你们跟这个问题，你们跟GPT聊，对吧？我就跟GPT聊了两句，对吧？对，这车有啥跟你男的跟他聊的。

发言人2   37:36
好的。

发言人1   37:38
对我看见文章在那儿了。

发言人1   37:54
对我我查了一下，能看见了吗？能看见你没有分享。但是实际上就是说这个制度还是一点假设，我们认为什么就是你要如果结果不对的话没什么大不了。你结果不对的时候，咱们再看这里边到底假设哪错了呢？好的，行，那还有啥？

发言人2   38:14
就是宋老师我们现在还有一种可能新的找法，就是因为你新的你生成的表中包含了浅层的信息，那我们是不是可以在每一层构建它的层级结构。然后我们认为就是那种底层的叶子节点，就是之前的旧信息。

发言人3   38:30
我觉得这个东西，我觉得这一层新信息可以这个不是我没听懂。

发言人1   38:34
不是没听懂，你说什么意思？你准备怎么做？

发言人2   38:36
就是我因为我的每一层的表征都包含了前一之前层的信息。我对每一层的表征，如果我能够把它构建成一个层级结构，那我就知道越上层的表越越层层层级越深的那那些非叶子节点，它就更可能是这一层学道德心的组合信息。

发言人1   38:59
不是我怎么做呢？

发言人2   39:01
关键是我们具体的做法我们还在看，但是我觉得我们可以试着去这样做一下。

发言人1   39:07
不是怎么不是我就是完全没听懂。你说的只是个概念，不是一个号了。

发言人2   39:13
对。

发言人1   39:14
就是因为我不可能给世界上所有的语音这个语料去做这个东西，对不对？是啊，对我我要做的就是说我模型最后能够有的，实际上就是我我我一定只能在普攻间做这件事儿，对不对？我只能再补一年做，对不对？

发言人2   39:35
这个我不确定。

发言人1   39:37
你不在普通间做，你在别的空间做了，你普通间给你的是一个低质表征，这个是计算效率是很高的。你不在这做你怎么做呢？

发言人1   39:49
而且你最后做一个getting的话，你的getting得是得适用于这个模型所训练的所有的数据才可以，对吧？是的，你是说白了就是你就想找个分类器。

发言人2   39:58
对你就想。

发言人1   39:59
找到一个子空间，然后这个子空间在这个上面。就是比如说钉钉这东方其实最早做的工作不就是做了个大概一百压到100多个，我觉得挺，然后就在这个维里边去做这个去做分发的，去做kimi cluster。然后对，本质上他是就原理上这么做，他原理上没错，就应该这么做吧，对吧？那然后你要求就说你得是个低质子空间，且这个低质子空间咱每层都自己又可以有个低质子空间，所以就是每层都得自己搞定这么一个地址总空间。且这个地址总空间还得适用于你的所有token走一遍的东西，对不对？

发言人2   40:34
answer. 

发言人2   40:46
很好的，我们之后都会去尝试一下。我们我们现在没有什么。

发言人1   40:51
说到的对吧？就是这个anyway了。行，那个那个你明白了吧？

发言人5   40:59
我明白了上市。

发言人1   41:01
你你你也明白了，对不对？

发言人5   41:02
对对对。

发言人1   41:04
行好，OK就是核心，就是说你在里面你做一个假设，你每一步的话基于这个假设，然后如何来来计算？对我来做一个执行，就是你你就是anyway，就是你这他其实就是一个思辨的过程，不断越来越细，对吧？好的，行行，那好，下面那个谁？一鸣，你和董芳。就先说华为的那个项目，第一个是你，你稍微等你。

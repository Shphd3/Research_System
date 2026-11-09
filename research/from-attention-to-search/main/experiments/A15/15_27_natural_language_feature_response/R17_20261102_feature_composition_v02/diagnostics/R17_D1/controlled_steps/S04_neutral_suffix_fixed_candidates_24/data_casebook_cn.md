# S04：24条完整前文、token与原模型分数

所有正文沿用S03，唯一后缀精确为换行+`Description:`。两完整候选` cat.`→[8251,13]、` dog.`→[5562,13]，均2个token，含前导空格与句号。总分含全部token，不校正先验或长度。P/N无正确答案；不能把偏好当作正确分类。

## S04_F01_P · exploration · ['animal']

```text
This object is an animal.
Description:
```

完整token IDs：`[1986, 1633, 374, 458, 9864, 624, 5009, 25]`；token pieces：`['This', 'Ġobject', 'Ġis', 'Ġan', 'Ġanimal', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置7／1起8。旧目标` a`，ID264，0起位置9。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-9.82304573059082, -3.16817569732666] | -12.991221428 |
| " dog." | [5562, 13] | 2 | [-9.77775764465332, -3.0843749046325684] | -12.862132549 |

差S_cat−S_dog=-0.129088879；首选dog；正确标签=不定义；正确性=不评分。P的cat/dog标签为未知，非否定。

## S04_F01_cat · exploration · ['animal', 'cat']

```text
This animal is a cat.
Description:
```

完整token IDs：`[1986, 9864, 374, 264, 8251, 624, 5009, 25]`；token pieces：`['This', 'Ġanimal', 'Ġis', 'Ġa', 'Ġcat', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置7／1起8。旧目标` a`，ID264，0起位置9。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-7.086837291717529, -3.3330130577087402] | -10.419850349 |
| " dog." | [5562, 13] | 2 | [-9.99154281616211, -3.551046371459961] | -13.542589188 |

差S_cat−S_dog=3.122738838；首选cat；正确标签=cat；正确性=True。P的cat/dog标签为未知，非否定。

## S04_F01_dog · exploration · ['animal', 'dog']

```text
This animal is a dog.
Description:
```

完整token IDs：`[1986, 9864, 374, 264, 5562, 624, 5009, 25]`；token pieces：`['This', 'Ġanimal', 'Ġis', 'Ġa', 'Ġdog', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置7／1起8。旧目标` a`，ID264，0起位置9。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-9.85776138305664, -3.635854482650757] | -13.493615866 |
| " dog." | [5562, 13] | 2 | [-6.559361457824707, -3.5458641052246094] | -10.105225563 |

差S_cat−S_dog=-3.388390303；首选dog；正确标签=dog；正确性=True。P的cat/dog标签为未知，非否定。

## S04_F01_N · exploration · ['non_animal', 'chair']

```text
This object is a chair.
Description:
```

完整token IDs：`[1986, 1633, 374, 264, 10496, 624, 5009, 25]`；token pieces：`['This', 'Ġobject', 'Ġis', 'Ġa', 'Ġchair', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置7／1起8。旧目标` a`，ID264，0起位置9。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-12.764867782592773, -4.039678573608398] | -16.804546356 |
| " dog." | [5562, 13] | 2 | [-14.050835609436035, -4.8018269538879395] | -18.852662563 |

差S_cat−S_dog=2.048116207；首选cat；正确标签=不定义；正确性=不评分。P的cat/dog标签为未知，非否定。

## S04_F02_P · exploration · ['animal']

```text
In this story, the object is an animal.
Description:
```

完整token IDs：`[641, 419, 3364, 11, 279, 1633, 374, 458, 9864, 624, 5009, 25]`；token pieces：`['In', 'Ġthis', 'Ġstory', ',', 'Ġthe', 'Ġobject', 'Ġis', 'Ġan', 'Ġanimal', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置11／1起12。旧目标` a`，ID264，0起位置13。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-9.704242706298828, -4.343315124511719] | -14.047557831 |
| " dog." | [5562, 13] | 2 | [-9.400522232055664, -4.406085968017578] | -13.806608200 |

差S_cat−S_dog=-0.240949631；首选dog；正确标签=不定义；正确性=不评分。P的cat/dog标签为未知，非否定。

## S04_F02_cat · exploration · ['animal', 'cat']

```text
In this story, the animal is a cat.
Description:
```

完整token IDs：`[641, 419, 3364, 11, 279, 9864, 374, 264, 8251, 624, 5009, 25]`；token pieces：`['In', 'Ġthis', 'Ġstory', ',', 'Ġthe', 'Ġanimal', 'Ġis', 'Ġa', 'Ġcat', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置11／1起12。旧目标` a`，ID264，0起位置13。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-8.044876098632812, -4.2789177894592285] | -12.323793888 |
| " dog." | [5562, 13] | 2 | [-10.608049392700195, -4.64453125] | -15.252580643 |

差S_cat−S_dog=2.928786755；首选cat；正确标签=cat；正确性=True。P的cat/dog标签为未知，非否定。

## S04_F02_dog · exploration · ['animal', 'dog']

```text
In this story, the animal is a dog.
Description:
```

完整token IDs：`[641, 419, 3364, 11, 279, 9864, 374, 264, 5562, 624, 5009, 25]`；token pieces：`['In', 'Ġthis', 'Ġstory', ',', 'Ġthe', 'Ġanimal', 'Ġis', 'Ġa', 'Ġdog', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置11／1起12。旧目标` a`，ID264，0起位置13。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-10.537370681762695, -4.359692573547363] | -14.897063255 |
| " dog." | [5562, 13] | 2 | [-7.878993034362793, -4.686586856842041] | -12.565579891 |

差S_cat−S_dog=-2.331483364；首选dog；正确标签=dog；正确性=True。P的cat/dog标签为未知，非否定。

## S04_F02_N · exploration · ['non_animal', 'chair']

```text
In this story, the object is a chair.
Description:
```

完整token IDs：`[641, 419, 3364, 11, 279, 1633, 374, 264, 10496, 624, 5009, 25]`；token pieces：`['In', 'Ġthis', 'Ġstory', ',', 'Ġthe', 'Ġobject', 'Ġis', 'Ġa', 'Ġchair', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置11／1起12。旧目标` a`，ID264，0起位置13。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-11.13659381866455, -5.502554893493652] | -16.639148712 |
| " dog." | [5562, 13] | 2 | [-11.638270378112793, -6.104922294616699] | -17.743192673 |

差S_cat−S_dog=1.104043961；首选cat；正确标签=不定义；正确性=不评分。P的cat/dog标签为未知，非否定。

## S04_F03_P · exploration · ['animal']

```text
We are describing an object. It is an animal.
Description:
```

完整token IDs：`[1654, 525, 22692, 458, 1633, 13, 1084, 374, 458, 9864, 624, 5009, 25]`；token pieces：`['We', 'Ġare', 'Ġdescribing', 'Ġan', 'Ġobject', '.', 'ĠIt', 'Ġis', 'Ġan', 'Ġanimal', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置12／1起13。旧目标` a`，ID264，0起位置14。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-7.792952537536621, -3.0425915718078613] | -10.835544109 |
| " dog." | [5562, 13] | 2 | [-7.609947204589844, -3.0208637714385986] | -10.630810976 |

差S_cat−S_dog=-0.204733133；首选dog；正确标签=不定义；正确性=不评分。P的cat/dog标签为未知，非否定。

## S04_F03_cat · exploration · ['animal', 'cat']

```text
We are describing an animal. It is a cat.
Description:
```

完整token IDs：`[1654, 525, 22692, 458, 9864, 13, 1084, 374, 264, 8251, 624, 5009, 25]`；token pieces：`['We', 'Ġare', 'Ġdescribing', 'Ġan', 'Ġanimal', '.', 'ĠIt', 'Ġis', 'Ġa', 'Ġcat', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置12／1起13。旧目标` a`，ID264，0起位置14。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-5.256192684173584, -3.0896987915039062] | -8.345891476 |
| " dog." | [5562, 13] | 2 | [-8.57415771484375, -3.4547791481018066] | -12.028936863 |

差S_cat−S_dog=3.683045387；首选cat；正确标签=cat；正确性=True。P的cat/dog标签为未知，非否定。

## S04_F03_dog · exploration · ['animal', 'dog']

```text
We are describing an animal. It is a dog.
Description:
```

完整token IDs：`[1654, 525, 22692, 458, 9864, 13, 1084, 374, 264, 5562, 624, 5009, 25]`；token pieces：`['We', 'Ġare', 'Ġdescribing', 'Ġan', 'Ġanimal', '.', 'ĠIt', 'Ġis', 'Ġa', 'Ġdog', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置12／1起13。旧目标` a`，ID264，0起位置14。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-8.344568252563477, -3.532650947570801] | -11.877219200 |
| " dog." | [5562, 13] | 2 | [-4.903797149658203, -3.3373043537139893] | -8.241101503 |

差S_cat−S_dog=-3.636117697；首选dog；正确标签=dog；正确性=True。P的cat/dog标签为未知，非否定。

## S04_F03_N · exploration · ['non_animal', 'chair']

```text
We are describing an object. It is a chair.
Description:
```

完整token IDs：`[1654, 525, 22692, 458, 1633, 13, 1084, 374, 264, 10496, 624, 5009, 25]`；token pieces：`['We', 'Ġare', 'Ġdescribing', 'Ġan', 'Ġobject', '.', 'ĠIt', 'Ġis', 'Ġa', 'Ġchair', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置12／1起13。旧目标` a`，ID264，0起位置14。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-9.68211555480957, -3.610293388366699] | -13.292408943 |
| " dog." | [5562, 13] | 2 | [-10.747819900512695, -4.031032562255859] | -14.778852463 |

差S_cat−S_dog=1.486443520；首选cat；正确标签=不定义；正确性=不评分。P的cat/dog标签为未知，非否定。

## S04_F04_P · heldout_check · ['animal']

```text
The note identifies this object as an animal.
Description:
```

完整token IDs：`[785, 5185, 35511, 419, 1633, 438, 458, 9864, 624, 5009, 25]`；token pieces：`['The', 'Ġnote', 'Ġidentifies', 'Ġthis', 'Ġobject', 'Ġas', 'Ġan', 'Ġanimal', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置10／1起11。旧目标` a`，ID264，0起位置12。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-10.421489715576172, -3.294320583343506] | -13.715810299 |
| " dog." | [5562, 13] | 2 | [-10.524730682373047, -3.351283550262451] | -13.876014233 |

差S_cat−S_dog=0.160203934；首选cat；正确标签=不定义；正确性=不评分。P的cat/dog标签为未知，非否定。

## S04_F04_cat · heldout_check · ['animal', 'cat']

```text
The note identifies this animal as a cat.
Description:
```

完整token IDs：`[785, 5185, 35511, 419, 9864, 438, 264, 8251, 624, 5009, 25]`；token pieces：`['The', 'Ġnote', 'Ġidentifies', 'Ġthis', 'Ġanimal', 'Ġas', 'Ġa', 'Ġcat', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置10／1起11。旧目标` a`，ID264，0起位置12。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-7.505302429199219, -3.2185730934143066] | -10.723875523 |
| " dog." | [5562, 13] | 2 | [-10.29324722290039, -3.829832077026367] | -14.123079300 |

差S_cat−S_dog=3.399203777；首选cat；正确标签=cat；正确性=True。P的cat/dog标签为未知，非否定。

## S04_F04_dog · heldout_check · ['animal', 'dog']

```text
The note identifies this animal as a dog.
Description:
```

完整token IDs：`[785, 5185, 35511, 419, 9864, 438, 264, 5562, 624, 5009, 25]`；token pieces：`['The', 'Ġnote', 'Ġidentifies', 'Ġthis', 'Ġanimal', 'Ġas', 'Ġa', 'Ġdog', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置10／1起11。旧目标` a`，ID264，0起位置12。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-10.172515869140625, -3.74224853515625] | -13.914764404 |
| " dog." | [5562, 13] | 2 | [-7.2976274490356445, -3.470536708831787] | -10.768164158 |

差S_cat−S_dog=-3.146600246；首选dog；正确标签=dog；正确性=True。P的cat/dog标签为未知，非否定。

## S04_F04_N · heldout_check · ['non_animal', 'chair']

```text
The note identifies this object as a chair.
Description:
```

完整token IDs：`[785, 5185, 35511, 419, 1633, 438, 264, 10496, 624, 5009, 25]`；token pieces：`['The', 'Ġnote', 'Ġidentifies', 'Ġthis', 'Ġobject', 'Ġas', 'Ġa', 'Ġchair', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置10／1起11。旧目标` a`，ID264，0起位置12。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-11.939921379089355, -4.036646366119385] | -15.976567745 |
| " dog." | [5562, 13] | 2 | [-13.526376724243164, -5.198619842529297] | -18.724996567 |

差S_cat−S_dog=2.748428822；首选cat；正确标签=不定义；正确性=不评分。P的cat/dog标签为未知，非否定。

## S04_F05_P · heldout_check · ['animal']

```text
An animal is the object described in this example.
Description:
```

完整token IDs：`[2082, 9864, 374, 279, 1633, 7481, 304, 419, 3110, 624, 5009, 25]`；token pieces：`['An', 'Ġanimal', 'Ġis', 'Ġthe', 'Ġobject', 'Ġdescribed', 'Ġin', 'Ġthis', 'Ġexample', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置11／1起12。旧目标` a`，ID264，0起位置13。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-7.738954067230225, -3.964874744415283] | -11.703828812 |
| " dog." | [5562, 13] | 2 | [-7.156790256500244, -3.873138189315796] | -11.029928446 |

差S_cat−S_dog=-0.673900366；首选dog；正确标签=不定义；正确性=不评分。P的cat/dog标签为未知，非否定。

## S04_F05_cat · heldout_check · ['animal', 'cat']

```text
A cat is the animal described in this example.
Description:
```

完整token IDs：`[32, 8251, 374, 279, 9864, 7481, 304, 419, 3110, 624, 5009, 25]`；token pieces：`['A', 'Ġcat', 'Ġis', 'Ġthe', 'Ġanimal', 'Ġdescribed', 'Ġin', 'Ġthis', 'Ġexample', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置11／1起12。旧目标` a`，ID264，0起位置13。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-6.097275733947754, -3.964884042739868] | -10.062159777 |
| " dog." | [5562, 13] | 2 | [-8.786816596984863, -4.067941665649414] | -12.854758263 |

差S_cat−S_dog=2.792598486；首选cat；正确标签=cat；正确性=True。P的cat/dog标签为未知，非否定。

## S04_F05_dog · heldout_check · ['animal', 'dog']

```text
A dog is the animal described in this example.
Description:
```

完整token IDs：`[32, 5562, 374, 279, 9864, 7481, 304, 419, 3110, 624, 5009, 25]`；token pieces：`['A', 'Ġdog', 'Ġis', 'Ġthe', 'Ġanimal', 'Ġdescribed', 'Ġin', 'Ġthis', 'Ġexample', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置11／1起12。旧目标` a`，ID264，0起位置13。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-8.914697647094727, -4.114521503448486] | -13.029219151 |
| " dog." | [5562, 13] | 2 | [-5.152340412139893, -3.9853403568267822] | -9.137680769 |

差S_cat−S_dog=-3.891538382；首选dog；正确标签=dog；正确性=True。P的cat/dog标签为未知，非否定。

## S04_F05_N · heldout_check · ['non_animal', 'chair']

```text
A chair is the object described in this example.
Description:
```

完整token IDs：`[32, 10496, 374, 279, 1633, 7481, 304, 419, 3110, 624, 5009, 25]`；token pieces：`['A', 'Ġchair', 'Ġis', 'Ġthe', 'Ġobject', 'Ġdescribed', 'Ġin', 'Ġthis', 'Ġexample', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置11／1起12。旧目标` a`，ID264，0起位置13。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-10.435174942016602, -4.262690544128418] | -14.697865486 |
| " dog." | [5562, 13] | 2 | [-10.956944465637207, -4.579965591430664] | -15.536910057 |

差S_cat−S_dog=0.839044571；首选cat；正确标签=不定义；正确性=不评分。P的cat/dog标签为未知，非否定。

## S04_F06_P · heldout_check · ['animal']

```text
The report calls the object an animal.
Description:
```

完整token IDs：`[785, 1895, 6738, 279, 1633, 458, 9864, 624, 5009, 25]`；token pieces：`['The', 'Ġreport', 'Ġcalls', 'Ġthe', 'Ġobject', 'Ġan', 'Ġanimal', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置9／1起10。旧目标` a`，ID264，0起位置11。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-10.203892707824707, -3.73140549659729] | -13.935298204 |
| " dog." | [5562, 13] | 2 | [-9.339468955993652, -3.616037607192993] | -12.955506563 |

差S_cat−S_dog=-0.979791641；首选dog；正确标签=不定义；正确性=不评分。P的cat/dog标签为未知，非否定。

## S04_F06_cat · heldout_check · ['animal', 'cat']

```text
The report calls the animal a cat.
Description:
```

完整token IDs：`[785, 1895, 6738, 279, 9864, 264, 8251, 624, 5009, 25]`；token pieces：`['The', 'Ġreport', 'Ġcalls', 'Ġthe', 'Ġanimal', 'Ġa', 'Ġcat', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置9／1起10。旧目标` a`，ID264，0起位置11。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-6.737390518188477, -3.6283392906188965] | -10.365729809 |
| " dog." | [5562, 13] | 2 | [-8.75796890258789, -3.7303342819213867] | -12.488303185 |

差S_cat−S_dog=2.122573376；首选cat；正确标签=cat；正确性=True。P的cat/dog标签为未知，非否定。

## S04_F06_dog · heldout_check · ['animal', 'dog']

```text
The report calls the animal a dog.
Description:
```

完整token IDs：`[785, 1895, 6738, 279, 9864, 264, 5562, 624, 5009, 25]`；token pieces：`['The', 'Ġreport', 'Ġcalls', 'Ġthe', 'Ġanimal', 'Ġa', 'Ġdog', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置9／1起10。旧目标` a`，ID264，0起位置11。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-9.853570938110352, -3.6794281005859375] | -13.532999039 |
| " dog." | [5562, 13] | 2 | [-6.678717136383057, -3.696146011352539] | -10.374863148 |

差S_cat−S_dog=-3.158135891；首选dog；正确标签=dog；正确性=True。P的cat/dog标签为未知，非否定。

## S04_F06_N · heldout_check · ['non_animal', 'chair']

```text
The report calls the object a chair.
Description:
```

完整token IDs：`[785, 1895, 6738, 279, 1633, 264, 10496, 624, 5009, 25]`；token pieces：`['The', 'Ġreport', 'Ġcalls', 'Ġthe', 'Ġobject', 'Ġa', 'Ġchair', '.Ċ', 'Description', ':']`。目标`:`，ID25，0起位置9／1起10。旧目标` a`，ID264，0起位置11。

| 精确候选（JSON保留空格） | token IDs | 长度 | 逐token logP | 总logP |
| --- | --- | --- | --- | --- |
| " cat." | [8251, 13] | 2 | [-11.521050453186035, -4.271947860717773] | -15.792998314 |
| " dog." | [5562, 13] | 2 | [-11.945069313049316, -4.890810966491699] | -16.835880280 |

差S_cat−S_dog=1.042881966；首选cat；正确标签=不定义；正确性=不评分。P的cat/dog标签为未知，非否定。

# 实际专家→feature→文本卡

本附录是固定规则抽样，不是全部输入。按每策略每专家抽非T10最高频2项、n≥5最低频2项、负责低频目标中支持最高2项，去重不补位；每项从实际接收且命中位置用固定种子20261019随机取1例，优先未展示上下文。图中raw token片段保留边界与转义，后2token仅事后辅助，不用于路由。原文档边界未知，只截同一连续缓存上下文，不拼接文件／窗口。JSON保存完整可见前缀。

共184张卡。空专家没有收到的文本；对应图保留空栏。

## 1. O／专家3／feature 13662

- TRAIN激活频率p=0.47755371；EVAL专家内q=1；支持64/64；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117679，文件token偏移8410112，块内0。
- 前2：`[]`｜当前：`["Ġgroup"]`｜后2：`["ĊĊ", "A"]`。
- 阅读文本：""｜**" group"**｜"\n\nA"。
- 下一token标签（不参与路由）："\n\n"。选择原因：highest_nonTop10_frequency.

## 2. O／专家3／feature 16323

- TRAIN激活频率p=0.44309627；EVAL专家内q=1；支持64/64；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117673，文件token偏移8403968，块内0。
- 前2：`[]`｜当前：`["Ġdefinitely"]`｜后2：`["Ġhandle", "Ġthe"]`。
- 阅读文本：""｜**" definitely"**｜" handle the"。
- 下一token标签（不参与路由）：" handle"。选择原因：highest_nonTop10_frequency.

## 3. O／专家3／feature 5285

- TRAIN激活频率p=0.019133668；EVAL专家内q=1；支持64/64；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117698，文件token偏移8429568，块内0。
- 前2：`[]`｜当前：`["Ġand"]`｜后2：`["Ġ$", "1"]`。
- 阅读文本：""｜**" and"**｜" $1"。
- 下一token标签（不参与路由）：" $"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 4. O／专家3／feature 9996

- TRAIN激活频率p=0.0054164882；EVAL专家内q=1；支持64/64；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117706，文件token偏移8437760，块内0。
- 前2：`[]`｜当前：`["Ġall"]`｜后2：`["Ġthe", "Ġway"]`。
- 阅读文本：""｜**" all"**｜" the way"。
- 下一token标签（不参与路由）：" the"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 5. O／专家4／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.74226804；支持72/97；名单负责专家=6（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117706，文件token偏移8438251，块内491。
- 前2：`["Ġon", "Ġhis"]`｜当前：`["Ġlips"]`｜后2：`[".", "ĠHe"]`。
- 阅读文本：" on his"｜**" lips"**｜". He"。
- 下一token标签（不参与路由）："."。选择原因：highest_nonTop10_frequency.

## 6. O／专家4／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.79381443；支持77/97；名单负责专家=5（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117673，文件token偏移8404861，块内893。
- 前2：`["Ġcontrad", "icts"]`｜当前：`["Ġitself"]`｜后2：`[".", "ĠAnd"]`。
- 阅读文本：" contradicts"｜**" itself"**｜". And"。
- 下一token标签（不参与路由）："."。选择原因：highest_nonTop10_frequency.

## 7. O／专家4／feature 13090

- TRAIN激活频率p=0.0016218863；EVAL专家内q=0.051546392；支持5/97；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117709，文件token偏移8441714，块内882。
- 前2：`["Ġbe", "Ġutterly"]`｜当前：`["Ġmeaningless"]`｜后2：`[":", "ĠI"]`。
- 阅读文本：" be utterly"｜**" meaningless"**｜": I"。
- 下一token标签（不参与路由）：":"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 8. O／专家4／feature 12666

- TRAIN激活频率p=0.0015683334；EVAL专家内q=0.06185567；支持6/97；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117717，文件token偏移8449348，块内324。
- 前2：`["Ġoutcomes", "Ġof"]`｜当前：`["Ġcommunism"]`｜后2：`["Ġor", "Ġcapitalism"]`。
- 阅读文本：" outcomes of"｜**" communism"**｜" or capitalism"。
- 下一token标签（不参与路由）：" or"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 9. O／专家5／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.3423913；支持63/184；名单负责专家=6（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117689，文件token偏移8420943，块内591。
- 前2：`["ĠMur", "ator"]`｜当前：`["ian"]`｜后2：`["ĠFragment", "Ġ("]`。
- 阅读文本：" Murator"｜**"ian"**｜" Fragment ("。
- 下一token标签（不参与路由）：" Fragment"。选择原因：highest_nonTop10_frequency.

## 10. O／专家5／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.42391304；支持78/184；名单负责专家=5（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117699，文件token偏移8431089，块内497。
- 前2：`[":", "Ġdry"]`｜当前：`["Ġp"]`｜后2：`["atty", "."]`。
- 阅读文本：": dry"｜**" p"**｜"atty."。
- 下一token标签（不参与路由）："atty"。选择原因：highest_nonTop10_frequency.

## 11. O／专家5／feature 5443

- TRAIN激活频率p=0.0015759838；EVAL专家内q=0.027173913；支持5/184；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117671，文件token偏移8402867，块内947。
- 前2：`["Jonathan", "H"]`｜当前：`["ob"]`｜后2：`["bs", "ĠNot"]`。
- 阅读文本："JonathanH"｜**"ob"**｜"bs Not"。
- 下一token标签（不参与路由）："bs"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 12. O／专家5／feature 2537

- TRAIN激活频率p=0.0015683334；EVAL专家内q=0.081521739；支持15/184；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117720，文件token偏移8453000，块内904。
- 前2：`["Ġchampion", "ĠJim"]`｜当前：`["mie"]`｜后2：`["ĠJohnson", "."]`。
- 阅读文本：" champion Jim"｜**"mie"**｜" Johnson."。
- 下一token标签（不参与路由）：" Johnson"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 13. O／专家6／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.91909432；支持6373/6934；名单负责专家=6（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117707，文件token偏移8439715，块内931。
- 前2：`["Ġmade", "Ġphoto"]`｜当前：`["-taking"]`｜后2：`["Ġon", "Ġa"]`。
- 阅读文本：" made photo"｜**"-taking"**｜" on a"。
- 下一token标签（不参与路由）：" on"。选择原因：highest_nonTop10_frequency.

## 14. O／专家6／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.67594462；支持4687/6934；名单负责专家=5（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117719，文件token偏移8451168，块内96。
- 前2：`["Ġsensational", "Ġas"]`｜当前：`["Ġher"]`｜后2：`["Ġinvolvement", "Ġin"]`。
- 阅读文本：" sensational as"｜**" her"**｜" involvement in"。
- 下一token标签（不参与路由）：" involvement"。选择原因：highest_nonTop10_frequency.

## 15. O／专家6／feature 3794

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0021632535；支持15/6934；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117664，文件token偏移8395232，块内480。
- 前2：`["ĠShe", "Ġunknow"]`｜当前：`["ingly"]`｜后2：`["Ġhas", "Ġbecome"]`。
- 阅读文本：" She unknow"｜**"ingly"**｜" has become"。
- 下一token标签（不参与路由）：" has"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 16. O／专家6／feature 9137

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0021632535；支持15/6934；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117705，文件token偏移8436800，块内64。
- 前2：`["Ġhas", "Ġcaught"]`｜当前：`["Ġup"]`｜后2：`["Ġin", "Ġstadium"]`。
- 阅读文本：" has caught"｜**" up"**｜" in stadium"。
- 下一token标签（不参与路由）：" in"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 17. O／专家7／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.65968722；支持38343/58123；名单负责专家=6（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117671，文件token偏移8402797，块内877。
- 前2：`["Ġabout", "Ġa"]`｜当前：`["Ġtrillion"]`｜后2：`["Ġof", "Ġthese"]`。
- 阅读文本：" about a"｜**" trillion"**｜" of these"。
- 下一token标签（不参与路由）：" of"。选择原因：highest_nonTop10_frequency.

## 18. O／专家7／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.57896186；支持33651/58123；名单负责专家=5（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117708，文件token偏移8439828，块内20。
- 前2：`["Ġphoto", "-cap"]`｜当前：`["able"]`｜后2：`["Ġdevices", "Ġthat"]`。
- 阅读文本：" photo-cap"｜**"able"**｜" devices that"。
- 下一token标签（不参与路由）：" devices"。选择原因：highest_nonTop10_frequency.

## 19. O／专家7／feature 2157

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0013419817；支持78/58123；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117700，文件token偏移8432345，块内729。
- 前2：`["Ġmy", "Ġgreat"]`｜当前：`["-"]`｜后2：`["unc", "les"]`。
- 阅读文本：" my great"｜**"-"**｜"uncles"。
- 下一token标签（不参与路由）："unc"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 20. O／专家7／feature 3794

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0015312355；支持89/58123；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117678，文件token偏移8410089，块内1001。
- 前2：`["Ġon", "Ġthe"]`｜当前：`["Ġincidental"]`｜后2：`["Ġmemory", "Ġrecognition"]`。
- 阅读文本：" on the"｜**" incidental"**｜" memory recognition"。
- 下一token标签（不参与路由）：" memory"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 21. F／专家7／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.68577414；支持44851/65402；名单负责专家=7（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117717，文件token偏移8449864，块内840。
- 前2：`["Ġthe", "Ġgreater"]`｜当前：`["Ġtruths"]`｜后2：`["Ġof", "Ġinstitutional"]`。
- 阅读文本：" the greater"｜**" truths"**｜" of institutional"。
- 下一token标签（不参与路由）：" of"。选择原因：highest_nonTop10_frequency.

## 22. F／专家7／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.58855998；支持38493/65402；名单负责专家=7（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117688，文件token偏移8420115，块内787。
- 前2：`["ical", "Ġparticipant"]`｜当前：`["Ġ("]`｜后2：`["A", "1"]`。
- 阅读文本："ical participant"｜**" ("**｜"A1"。
- 下一token标签（不参与路由）："A"。选择原因：highest_nonTop10_frequency.

## 23. F／专家7／feature 2157

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0011926241；支持78/65402；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117665，文件token偏移8396633，块内857。
- 前2：`["-less", "-than"]`｜当前：`["-"]`｜后2：`["what", "-it"]`。
- 阅读文本："-less-than"｜**"-"**｜"what-it"。
- 下一token标签（不参与路由）："what"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 24. F／专家7／feature 3794

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0016054555；支持105/65402；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117664，文件token偏移8394816，块内64。
- 前2：`["Ġin", "Ġa"]`｜当前：`["Ġsystematic"]`｜后2：`["Ġsociety", "Ġthat"]`。
- 阅读文本：" in a"｜**" systematic"**｜" society that"。
- 下一token标签（不参与路由）：" society"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 25. T／专家0／feature 14

- TRAIN激活频率p=0.66684008；EVAL专家内q=1；支持1/1；名单负责专家=7（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117667，文件token偏移8398334，块内510。
- 前2：`["?ĊĊ", "Ġ"]`｜当前：`["Ġ"]`｜后2：`["2", "8"]`。
- 阅读文本："?\n\n "｜**" "**｜"28"。
- 下一token标签（不参与路由）："2"。选择原因：highest_nonTop10_frequency.

## 26. T／专家0／feature 13276

- TRAIN激活频率p=0.44618704；EVAL专家内q=1；支持1/1；名单负责专家=7（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117667，文件token偏移8398334，块内510。
- 前2：`["?ĊĊ", "Ġ"]`｜当前：`["Ġ"]`｜后2：`["2", "8"]`。
- 阅读文本："?\n\n "｜**" "**｜"28"。
- 下一token标签（不参与路由）："2"。选择原因：highest_nonTop10_frequency.

## 27. T／专家0／feature 5412

- TRAIN激活频率p=0.0018896505；EVAL专家内q=1；支持1/1；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117667，文件token偏移8398334，块内510。
- 前2：`["?ĊĊ", "Ġ"]`｜当前：`["Ġ"]`｜后2：`["2", "8"]`。
- 阅读文本："?\n\n "｜**" "**｜"28"。
- 下一token标签（不参与路由）："2"。选择原因：assigned_low_target_largest_support.

## 28. T／专家0／feature 601

- TRAIN激活频率p=0.0018360977；EVAL专家内q=1；支持1/1；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117667，文件token偏移8398334，块内510。
- 前2：`["?ĊĊ", "Ġ"]`｜当前：`["Ġ"]`｜后2：`["2", "8"]`。
- 阅读文本："?\n\n "｜**" "**｜"28"。
- 下一token标签（不参与路由）："2"。选择原因：assigned_low_target_largest_support.

## 29. T／专家7／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.68578462；支持44851/65401；名单负责专家=7（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117714，文件token偏移8446349，块内397。
- 前2：`["if", "Ġpossible"]`｜当前：`[")ĊĊ"]`｜后2：`["share", "|"]`。
- 阅读文本："if possible"｜**")\n\n"**｜"share|"。
- 下一token标签（不参与路由）："share"。选择原因：highest_nonTop10_frequency.

## 30. T／专家7／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.58856898；支持38493/65401；名单负责专家=7（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117681，文件token偏移8413182，块内1022。
- 前2：`["Ġpredict", "Ġthat"]`｜当前：`["Ġam"]`｜后2：`["us"]`。
- 阅读文本：" predict that"｜**" am"**｜"us"。
- 下一token标签（不参与路由）："us"。选择原因：highest_nonTop10_frequency.

## 31. T／专家7／feature 2157

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0011926423；支持78/65401；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117706，文件token偏移8437897，块内137。
- 前2：`["0", "0"]`｜当前：`["-"]`｜后2：`["2", "0"]`。
- 阅读文本："00"｜**"-"**｜"20"。
- 下一token标签（不参与路由）："2"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 32. T／专家7／feature 3794

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.00160548；支持105/65401；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117676，文件token偏移8407872，块内832。
- 前2：`[",", "Ġwithout"]`｜当前：`["Ġconscious"]`｜后2：`["Ġeffort", "Ġor"]`。
- 阅读文本：", without"｜**" conscious"**｜" effort or"。
- 下一token标签（不参与路由）：" effort"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 33. Tphi／专家0／feature 14

- TRAIN激活频率p=0.66684008；EVAL专家内q=1；支持1/1；名单负责专家=7（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117667，文件token偏移8398334，块内510。
- 前2：`["?ĊĊ", "Ġ"]`｜当前：`["Ġ"]`｜后2：`["2", "8"]`。
- 阅读文本："?\n\n "｜**" "**｜"28"。
- 下一token标签（不参与路由）："2"。选择原因：highest_nonTop10_frequency.

## 34. Tphi／专家0／feature 13276

- TRAIN激活频率p=0.44618704；EVAL专家内q=1；支持1/1；名单负责专家=7（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117667，文件token偏移8398334，块内510。
- 前2：`["?ĊĊ", "Ġ"]`｜当前：`["Ġ"]`｜后2：`["2", "8"]`。
- 阅读文本："?\n\n "｜**" "**｜"28"。
- 下一token标签（不参与路由）："2"。选择原因：highest_nonTop10_frequency.

## 35. Tphi／专家0／feature 5412

- TRAIN激活频率p=0.0018896505；EVAL专家内q=1；支持1/1；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117667，文件token偏移8398334，块内510。
- 前2：`["?ĊĊ", "Ġ"]`｜当前：`["Ġ"]`｜后2：`["2", "8"]`。
- 阅读文本："?\n\n "｜**" "**｜"28"。
- 下一token标签（不参与路由）："2"。选择原因：assigned_low_target_largest_support.

## 36. Tphi／专家0／feature 601

- TRAIN激活频率p=0.0018360977；EVAL专家内q=1；支持1/1；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117667，文件token偏移8398334，块内510。
- 前2：`["?ĊĊ", "Ġ"]`｜当前：`["Ġ"]`｜后2：`["2", "8"]`。
- 阅读文本："?\n\n "｜**" "**｜"28"。
- 下一token标签（不参与路由）："2"。选择原因：assigned_low_target_largest_support.

## 37. Tphi／专家7／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.68578462；支持44851/65401；名单负责专家=7（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117701，文件token偏移8432845，块内205。
- 前2：`["Ġtime", "ĠI"]`｜当前：`["Ġtried"]`｜后2：`["Ġit", "Ġ-"]`。
- 阅读文本：" time I"｜**" tried"**｜" it -"。
- 下一token标签（不参与路由）：" it"。选择原因：highest_nonTop10_frequency.

## 38. Tphi／专家7／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.58856898；支持38493/65401；名单负责专家=7（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117690，文件token偏移8422232，块内856。
- 前2：`["Ġknow", "Ġwhat"]`｜当前：`["Ġis"]`｜后2：`["Ġand", "Ġis"]`。
- 阅读文本：" know what"｜**" is"**｜" and is"。
- 下一token标签（不参与路由）：" and"。选择原因：highest_nonTop10_frequency.

## 39. Tphi／专家7／feature 2157

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0011926423；支持78/65401；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117667，文件token偏移8398426，块内602。
- 前2：`["Ġwith", "ĠChrist"]`｜当前：`["("]`｜后2：`["Yes", ","]`。
- 阅读文本：" with Christ"｜**"("**｜"Yes,"。
- 下一token标签（不参与路由）："Yes"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 40. Tphi／专家7／feature 3794

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.00160548；支持105/65401；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117693，文件token偏移8425449，块内1001。
- 前2：`["mouth", "ĠInv"]`｜当前：`["itational"]`｜后2：`[".", "ĠThe"]`。
- 阅读文本："mouth Inv"｜**"itational"**｜". The"。
- 下一token标签（不参与路由）："."。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 41. R11／专家0／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.644511；支持5595/8681；名单负责专家=2（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117692，文件token偏移8424179，块内755。
- 前2：`["ĠChrist", ",ĊĊĊ"]`｜当前：`["2"]`｜后2：`["7", "-"]`。
- 阅读文本：" Christ,\n\n\n"｜**"2"**｜"7-"。
- 下一token标签（不参与路由）："7"。选择原因：highest_nonTop10_frequency.

## 42. R11／专家0／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.52493952；支持4557/8681；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117718，文件token偏移8450137，块内89。
- 前2：`["Ġsociety", ","]`｜当前：`["Ġthey"]`｜后2：`["Ġwould", "Ġeither"]`。
- 阅读文本：" society,"｜**" they"**｜" would either"。
- 下一token标签（不参与路由）：" would"。选择原因：highest_nonTop10_frequency.

## 43. R11／专家0／feature 14834

- TRAIN激活频率p=0.002180366；EVAL专家内q=0.012671351；支持110/8681；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117697，文件token偏移8429243，块内699。
- 前2：`["Ġ:", "-("]`｜当前：`["."]`｜后2：`["ĠAnyone", "Ġbeen"]`。
- 阅读文本：" :-("｜**"."**｜" Anyone been"。
- 下一token标签（不参与路由）：" Anyone"。选择原因：assigned_low_target_largest_support.

## 44. R11／专家0／feature 4020

- TRAIN激活频率p=0.001560683；EVAL专家内q=0.012901739；支持112/8681；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117672，文件token偏移8403799，块内855。
- 前2：`["Ġgag", "ĊĊ"]`｜当前：`["Ġ"]`｜后2：`["Ġ", "4"]`。
- 阅读文本：" gag\n\n"｜**" "**｜" 4"。
- 下一token标签（不参与路由）：" "。选择原因：assigned_low_target_largest_support.

## 45. R11／专家0／feature 3794

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.00069116461；支持6/8681；名单负责专家=1（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117709，文件token偏移8441691，块内859。
- 前2：`["Ġa", "Ġperson"]`｜当前：`["Ġaesthetic"]`｜后2：`["Ġpleasure", ","]`。
- 阅读文本：" a person"｜**" aesthetic"**｜" pleasure,"。
- 下一token标签（不参与路由）：" pleasure"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 46. R11／专家0／feature 7272

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.00069116461；支持6/8681；名单负责专家=4（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117658，文件token偏移8389245，块内637。
- 前2：`["1", "0"]`｜当前：`[")-"]`｜后2：`["ĠIt", "Ġtakes"]`。
- 阅读文本："10"｜**")-"**｜" It takes"。
- 下一token标签（不参与路由）：" It"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 47. R11／专家1／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.73194368；支持8006/10938；名单负责专家=2（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117675，文件token偏移8406291，块内275。
- 前2：`["Ġcorner", "."]`｜当前：`["ĠAnd"]`｜后2：`["ĠI", "Ġcaught"]`。
- 阅读文本：" corner."｜**" And"**｜" I caught"。
- 下一token标签（不参与路由）：" I"。选择原因：highest_nonTop10_frequency.

## 48. R11／专家1／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.62845127；支持6874/10938；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117669，文件token偏移8400134，块内262。
- 前2：`["-b", "ashing"]`｜当前：`["Ġmovement"]`｜后2：`["Ġcalled", "ĠF"]`。
- 阅读文本："-bashing"｜**" movement"**｜" called F"。
- 下一token标签（不参与路由）：" called"。选择原因：highest_nonTop10_frequency.

## 49. R11／专家1／feature 4717

- TRAIN激活频率p=0.0022109676；EVAL专家内q=0.0081367709；支持89/10938；名单负责专家=1（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117692，文件token偏移8424336，块内912。
- 前2：`["Ġto", "Ġthe"]`｜当前：`["Ġother"]`｜后2：`["'s", "Ġtradition"]`。
- 阅读文本：" to the"｜**" other"**｜"'s tradition"。
- 下一token标签（不参与路由）："'s"。选择原因：assigned_low_target_largest_support.

## 50. R11／专家1／feature 5329

- TRAIN激活频率p=0.0020962115；EVAL专家内q=0.010970927；支持120/10938；名单负责专家=1（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117714，文件token偏移8446906，块内954。
- 前2：`["Ġin", "Ġthe"]`｜当前：`["Ġrevenue"]`｜后2：`["-based", "Ġinsurance"]`。
- 阅读文本：" in the"｜**" revenue"**｜"-based insurance"。
- 下一token标签（不参与路由）："-based"。选择原因：assigned_low_target_largest_support.

## 51. R11／专家1／feature 2157

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0013713659；支持15/10938；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117686，文件token偏移8417409，块内129。
- 前2：`["Ġ[", "t"]`｜当前：`["("]`｜后2：`["2", "9"]`。
- 阅读文本：" [t"｜**"("**｜"29"。
- 下一token标签（不参与路由）："2"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 52. R11／专家1／feature 7272

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0010056683；支持11/10938；名单负责专家=4（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117684，文件token偏移8416251，块内1019。
- 前2：`[".;", "Ġt"]`｜当前：`["("]`｜后2：`["2", "4"]`。
- 阅读文本：".; t"｜**"("**｜"24"。
- 下一token标签（不参与路由）："2"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 53. R11／专家2／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.7503609；支持7277/9698；名单负责专家=2（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117707，文件token偏移8438823，块内39。
- 前2：`["ĠSummer", "ĠEP"]`｜当前：`["Ġessentially"]`｜后2：`["Ġamounts", "Ġto"]`。
- 阅读文本：" Summer EP"｜**" essentially"**｜" amounts to"。
- 下一token标签（不参与路由）：" amounts"。选择原因：highest_nonTop10_frequency.

## 54. R11／专家2／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.61827181；支持5996/9698；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117693，文件token偏移8424633，块内185。
- 前2：`["Ġreally", "Ġsure"]`｜当前：`["Ġwhat"]`｜后2：`["Ġthe", "Ġreal"]`。
- 阅读文本：" really sure"｜**" what"**｜" the real"。
- 下一token标签（不参与路由）：" the"。选择原因：highest_nonTop10_frequency.

## 55. R11／专家2／feature 14932

- TRAIN激活频率p=0.0021038619；EVAL专家内q=0.018560528；支持180/9698；名单负责专家=2（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117667，文件token偏移8398052，块内228。
- 前2：`[",", "Ġand"]`｜当前：`["Ġdoesn"]`｜后2：`["'t", "Ġcare"]`。
- 阅读文本：", and"｜**" doesn"**｜"'t care"。
- 下一token标签（不参与路由）："'t"。选择原因：assigned_low_target_largest_support.

## 56. R11／专家2／feature 7462

- TRAIN激活频率p=0.0018973009；EVAL专家内q=0.028459476；支持276/9698；名单负责专家=2（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117694，文件token偏移8425581，块内109。
- 前2：`[")", "Ġled"]`｜当前：`["Ġthe"]`｜后2：`["Ġcharge", "Ġfor"]`。
- 阅读文本：") led"｜**" the"**｜" charge for"。
- 下一token标签（不参与路由）：" charge"。选择原因：assigned_low_target_largest_support.

## 57. R11／专家2／feature 3794

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.002371623；支持23/9698；名单负责专家=1（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117687，文件token偏移8419134，块内830。
- 前2：`[".", "ĠThe"]`｜当前：`["Ġsystematic"]`｜后2：`["Ġevaluation", "Ġof"]`。
- 阅读文本：". The"｜**" systematic"**｜" evaluation of"。
- 下一token标签（不参与路由）：" evaluation"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 58. R11／专家2／feature 9137

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0017529388；支持17/9698；名单负责专家=1（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117709，文件token偏移8440937，块内105。
- 前2：`["Ġon", "Ġpar"]`｜当前：`["Ġwith"]`｜后2：`["Ġthe", "Ġsome"]`。
- 阅读文本：" on par"｜**" with"**｜" the some"。
- 下一token标签（不参与路由）：" the"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 59. R11／专家3／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.70445344；支持2610/3705；名单负责专家=2（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117673，文件token偏移8404135，块内167。
- 前2：`["Ġit", "Ġworks"]`｜当前：`["Ġbut"]`｜后2：`["Ġit", "Ġmakes"]`。
- 阅读文本：" it works"｜**" but"**｜" it makes"。
- 下一token标签（不参与路由）：" it"。选择原因：highest_nonTop10_frequency.

## 60. R11／专家3／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.62051282；支持2299/3705；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117721，文件token偏移8453802，块内682。
- 前2：`["Ġenter", "Ġinto"]`｜当前：`["Ġforce"]`｜后2：`[".", "ĠThe"]`。
- 阅读文本：" enter into"｜**" force"**｜". The"。
- 下一token标签（不参与路由）："."。选择原因：highest_nonTop10_frequency.

## 61. R11／专家3／feature 2987

- TRAIN激活频率p=0.0024557806；EVAL专家内q=0.024561404；支持91/3705；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117667，文件token偏移8398325，块内501。
- 前2：`[",", "Ġand"]`｜当前：`["Ġwhat"]`｜后2：`["Ġdoes", "Ġa"]`。
- 阅读文本：", and"｜**" what"**｜" does a"。
- 下一token标签（不参与路由）：" does"。选择原因：assigned_low_target_largest_support.

## 62. R11／专家3／feature 1115

- TRAIN激活频率p=0.0015453822；EVAL专家内q=0.025641026；支持95/3705；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117682，文件token偏移8413233，块内49。
- 前2：`["Ġ", "2"]`｜当前：`["4"]`｜后2：`["Ġmusical", "Ġexcerpts"]`。
- 阅读文本：" 2"｜**"4"**｜" musical excerpts"。
- 下一token标签（不参与路由）：" musical"。选择原因：assigned_low_target_largest_support.

## 63. R11／专家3／feature 2157

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0021592443；支持8/3705；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117665，文件token偏移8396633，块内857。
- 前2：`["-less", "-than"]`｜当前：`["-"]`｜后2：`["what", "-it"]`。
- 阅读文本："-less-than"｜**"-"**｜"what-it"。
- 下一token标签（不参与路由）："what"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 64. R11／专家3／feature 12397

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0021592443；支持8/3705；名单负责专家=4（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117699，文件token偏移8431185，块内593。
- 前2：`["Ġa", "Ġnice"]`｜当前：`["Ġthick"]`｜后2：`["Ġp", "atty"]`。
- 阅读文本：" a nice"｜**" thick"**｜" patty"。
- 下一token标签（不参与路由）：" p"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 65. R11／专家4／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.63329634；支持2853/4505；名单负责专家=2（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117697，文件token偏移8429474，块内930。
- 前2：`["ĠSuff", "ice"]`｜当前：`["Ġto"]`｜后2：`["Ġsay", "Ġfor"]`。
- 阅读文本：" Suffice"｜**" to"**｜" say for"。
- 下一token标签（不参与路由）：" say"。选择原因：highest_nonTop10_frequency.

## 66. R11／专家4／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.51564928；支持2323/4505；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117682，文件token偏移8414092，块内908。
- 前2：`["Ġin", "Ġa"]`｜当前：`["Ġrather"]`｜后2：`["Ġconsistent", "Ġmanner"]`。
- 阅读文本：" in a"｜**" rather"**｜" consistent manner"。
- 下一token标签（不参与路由）：" consistent"。选择原因：highest_nonTop10_frequency.

## 67. R11／专家4／feature 7810

- TRAIN激活频率p=0.0018437481；EVAL专家内q=0.014428413；支持65/4505；名单负责专家=4（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117663，文件token偏移8394156，块内428。
- 前2：`["\",", "Ġand"]`｜当前：`["Ġhow"]`｜后2：`["Ġhe", "Ġapproaches"]`。
- 阅读文本："\", and"｜**" how"**｜" he approaches"。
- 下一token标签（不参与路由）：" he"。选择原因：assigned_low_target_largest_support.

## 68. R11／专家4／feature 15067

- TRAIN激活频率p=0.0016295367；EVAL专家内q=0.022641509；支持102/4505；名单负责专家=4（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117703，文件token偏移8434693，块内5。
- 前2：`["Ċ", "ĠĠĠĠĠĠĠĠĠĠĠ"]`｜当前：`["Ġ"]`｜后2：`["1", "."]`。
- 阅读文本："\n           "｜**" "**｜"1."。
- 下一token标签（不参与路由）："1"。选择原因：assigned_low_target_largest_support.

## 69. R11／专家4／feature 3794

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0017758047；支持8/4505；名单负责专家=1（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117664，文件token偏移8394816，块内64。
- 前2：`["Ġin", "Ġa"]`｜当前：`["Ġsystematic"]`｜后2：`["Ġsociety", "Ġthat"]`。
- 阅读文本：" in a"｜**" systematic"**｜" society that"。
- 下一token标签（不参与路由）：" society"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 70. R11／专家4／feature 9137

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.002663707；支持12/4505；名单负责专家=1（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117705，文件token偏移8436799，块内63。
- 前2：`["ĠLeague", "Ġhas"]`｜当前：`["Ġcaught"]`｜后2：`["Ġup", "Ġin"]`。
- 阅读文本：" League has"｜**" caught"**｜" up in"。
- 下一token标签（不参与路由）：" up"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 71. R11／专家5／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.64266245；支持7309/11373；名单负责专家=2（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117706，文件token偏移8438129，块内369。
- 前2：`["-of", "-f"]`｜当前：`["actly"]`｜后2：`[",", "Ġand"]`。
- 阅读文本："-of-f"｜**"actly"**｜", and"。
- 下一token标签（不参与路由）：","。选择原因：highest_nonTop10_frequency.

## 72. R11／专家5／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.55939506；支持6362/11373；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117665，文件token偏移8396764，块内988。
- 前2：`["Ġwe", "Ġset"]`｜当前：`["Ġout"]`｜后2：`["Ġin", "Ġlife"]`。
- 阅读文本：" we set"｜**" out"**｜" in life"。
- 下一token标签（不参与路由）：" in"。选择原因：highest_nonTop10_frequency.

## 73. R11／专家5／feature 6682

- TRAIN激活频率p=0.0023333741；EVAL专家内q=0.018728568；支持213/11373；名单负责专家=5（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117704，文件token偏移8435844，块内132。
- 前2：`["Ġtab", "Ċ"]`｜当前：`["Toggle"]`｜后2：`["Ġthe", "Ġdisplay"]`。
- 阅读文本：" tab\n"｜**"Toggle"**｜" the display"。
- 下一token标签（不参与路由）：" the"。选择原因：assigned_low_target_largest_support.

## 74. R11／专家5／feature 11329

- TRAIN激活频率p=0.0017136912；EVAL专家内q=0.025059351；支持285/11373；名单负责专家=5（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117705，文件token偏移8437202，块内466。
- 前2：`["Ġbest", "Ġor"]`｜当前：`["Ġworst"]`｜后2：`["Ġteam", "Ġmoney"]`。
- 阅读文本：" best or"｜**" worst"**｜" team money"。
- 下一token标签（不参与路由）：" team"。选择原因：assigned_low_target_largest_support.

## 75. R11／专家5／feature 2157

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0014947683；支持17/11373；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117693，文件token偏移8424828，块内380。
- 前2：`["2", "7"]`｜当前：`["-"]`｜后2：`["0", "8"]`。
- 阅读文本："27"｜**"-"**｜"08"。
- 下一token标签（不参与路由）："0"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 76. R11／专家5／feature 3794

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0040446672；支持46/11373；名单负责专家=1（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117676，文件token偏移8407132，块内92。
- 前2：`["Ġundermine", "Ġthe"]`｜当前：`["Ġaesthetic"]`｜后2：`["Ġdialect", "ic"]`。
- 阅读文本：" undermine the"｜**" aesthetic"**｜" dialectic"。
- 下一token标签（不参与路由）：" dialect"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 77. R11／专家6／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.72023096；支持6611/9179；名单负责专家=2（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117681，文件token偏移8412284，块内124。
- 前2：`["Ġand", "Ġto"]`｜当前：`["Ġtest"]`｜后2：`["Ġfurther", "Ġthe"]`。
- 阅读文本：" and to"｜**" test"**｜" further the"。
- 下一token标签（不参与路由）：" further"。选择原因：highest_nonTop10_frequency.

## 78. R11／专家6／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.63198606；支持5801/9179；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117662，文件token偏移8392996，块内292。
- 前2：`["Ġhome", ","]`｜当前：`["Ġcars"]`｜后2：`[",", "Ġand"]`。
- 阅读文本：" home,"｜**" cars"**｜", and"。
- 下一token标签（不参与路由）：","。选择原因：highest_nonTop10_frequency.

## 79. R11／专家6／feature 899

- TRAIN激活频率p=0.002386927；EVAL专家内q=0.0087155464；支持80/9179；名单负责专家=6（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117665，文件token偏移8396147，块内371。
- 前2：`["Ġblack", "Ġfemales"]`｜当前：`["Ġso"]`｜后2：`["Ġladies", "Ġi"]`。
- 阅读文本：" black females"｜**" so"**｜" ladies i"。
- 下一token标签（不参与路由）：" ladies"。选择原因：assigned_low_target_largest_support.

## 80. R11／专家6／feature 4873

- TRAIN激活频率p=0.0020579595；EVAL专家内q=0.011874932；支持109/9179；名单负责专家=6（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117674，文件token偏移8405878，块内886。
- 前2：`["Ġbetween", "Ġreality"]`｜当前：`["Ġand"]`｜后2：`["Ġabstraction", "."]`。
- 阅读文本：" between reality"｜**" and"**｜" abstraction."。
- 下一token标签（不参与路由）：" abstraction"。选择原因：assigned_low_target_largest_support.

## 81. R11／专家6／feature 2157

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0015252206；支持14/9179；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117682，文件token偏移8413994，块内810。
- 前2：`["Ġwith", "ĠF"]`｜当前：`["("]`｜后2：`["1", ","]`。
- 阅读文本：" with F"｜**"("**｜"1,"。
- 下一token标签（不参与路由）："1"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 82. R11／专家6／feature 3794

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.00098049897；支持9/9179；名单负责专家=1（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117658，文件token偏移8389474，块内866。
- 前2：`["Âł", "adam"]`｜当前：`["antly"]`｜后2：`["Âł", "declare"]`。
- 阅读文本：" adam"｜**"antly"**｜" declare"。
- 下一token标签（不参与路由）：" "。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 83. R11／专家7／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.6267923；支持4590/7323；名单负责专家=2（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117718，文件token偏移8450443，块内395。
- 前2：`["ĠSome", "Ġrange"]`｜当前：`["Ġexpansion"]`｜后2：`[".", "ĠStretch"]`。
- 阅读文本：" Some range"｜**" expansion"**｜". Stretch"。
- 下一token标签（不参与路由）："."。选择原因：highest_nonTop10_frequency.

## 84. R11／专家7／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.58459648；支持4281/7323；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117662，文件token偏移8393366，块内662。
- 前2：`["Ġyears", "Ġnow"]`｜当前：`["Ġsince"]`｜后2：`["ĠI", "Ġhave"]`。
- 阅读文本：" years now"｜**" since"**｜" I have"。
- 下一token标签（不参与路由）：" I"。选择原因：highest_nonTop10_frequency.

## 85. R11／专家7／feature 15412

- TRAIN激活频率p=0.0022874717；EVAL专家内q=0.030452001；支持223/7323；名单负责专家=7（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117689，文件token偏移8421156，块内804。
- 前2：`["Ġto", "Ġmake"]`｜当前：`["Ġno"]`｜后2：`["Ġfalse", "Ġstatements"]`。
- 阅读文本：" to make"｜**" no"**｜" false statements"。
- 下一token标签（不参与路由）：" false"。选择原因：assigned_low_target_largest_support.

## 86. R11／专家7／feature 2492

- TRAIN激活频率p=0.0017442928；EVAL专家内q=0.042468933；支持311/7323；名单负责专家=7（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117690，文件token偏移8421528，块内152。
- 前2：`["ĠMarc", "ion"]`｜当前：`[","]`｜后2：`["Ġfor", "Ġexample"]`。
- 阅读文本：" Marcion"｜**","**｜" for example"。
- 下一token标签（不参与路由）：" for"。选择原因：assigned_low_target_largest_support.

## 87. R11／专家7／feature 2157

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0027311211；支持20/7323；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117670，文件token偏移8401790，块内894。
- 前2：`["8", "2"]`｜当前：`["-"]`｜后2：`["9", "1"]`。
- 阅读文本："82"｜**"-"**｜"91"。
- 下一token标签（不参与路由）："9"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 88. R11／专家7／feature 3794

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0012290045；支持9/7323；名单负责专家=1（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117716，文件token偏移8448907，块内907。
- 前2：`[",", "Ġfor"]`｜当前：`["-profit"]`｜后2：`["Ġcapital", "âĢĻs"]`。
- 阅读文本：", for"｜**"-profit"**｜" capital’s"。
- 下一token标签（不参与路由）：" capital"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 89. R22／专家0／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.82388326；支持7396/8977；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117675，文件token偏移8406024，块内8。
- 前2：`["Ġas", "ĠI"]`｜当前：`["Ġproceeded"]`｜后2：`[",", "ĠI"]`。
- 阅读文本：" as I"｜**" proceeded"**｜", I"。
- 下一token标签（不参与路由）：","。选择原因：highest_nonTop10_frequency.

## 90. R22／专家0／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.65489584；支持5879/8977；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117676，文件token偏移8407355，块内315。
- 前2：`["Ġpaper", "Ġissue"]`｜当前：`["Ġeventually"]`｜后2：`["Ġseemed", "Ġirrelevant"]`。
- 阅读文本：" paper issue"｜**" eventually"**｜" seemed irrelevant"。
- 下一token标签（不参与路由）：" seemed"。选择原因：highest_nonTop10_frequency.

## 91. R22／专家0／feature 7462

- TRAIN激活频率p=0.0018973009；EVAL专家内q=0.019494263；支持175/8977；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117712，文件token偏移8444156，块内252。
- 前2：`["Ġthought", ","]`｜当前：`["Ġthis"]`｜后2：`["Ġwas", "Ġa"]`。
- 阅读文本：" thought,"｜**" this"**｜" was a"。
- 下一token标签（不参与路由）：" was"。选择原因：assigned_low_target_largest_support.

## 92. R22／专家0／feature 10292

- TRAIN激活频率p=0.0017442928；EVAL专家内q=0.013256099；支持119/8977；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117719，文件token偏移8451663，块内591。
- 前2：`["Ġsexually", "Ġexcited"]`｜当前：`["."]`｜后2：`["ĠWrestling", "Ġis"]`。
- 阅读文本：" sexually excited"｜**"."**｜" Wrestling is"。
- 下一token标签（不参与路由）：" Wrestling"。选择原因：assigned_low_target_largest_support.

## 93. R22／专家0／feature 3794

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0026734989；支持24/8977；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117661，文件token偏移8392253，块内573。
- 前2：`["ĠYou", "Ġare"]`｜当前：`["Ġmistakenly"]`｜后2：`["Ġmaking", "Ġreference"]`。
- 阅读文本：" You are"｜**" mistakenly"**｜" making reference"。
- 下一token标签（不参与路由）：" making"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 94. R22／专家0／feature 7272

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.00055697895；支持5/8977；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117660，文件token偏移8390751，块内95。
- 前2：`["Ġyour", "Ġis"]`｜当前：`["h"]`｜后2：`["Ġtogether", ".Ċ"]`。
- 阅读文本：" your is"｜**"h"**｜" together.\n"。
- 下一token标签（不参与路由）：" together"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 95. R22／专家1／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.68295956；支持3563/5217；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117667，文件token偏移8398377，块内553。
- 前2：`["Ġto", "Ġtruly"]`｜当前：`["Ġlisten"]`｜后2：`["Ġto", "Ġthe"]`。
- 阅读文本：" to truly"｜**" listen"**｜" to the"。
- 下一token标签（不参与路由）：" to"。选择原因：highest_nonTop10_frequency.

## 96. R22／专家1／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.5652674；支持2949/5217；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117710，文件token偏移8442822，块内966。
- 前2：`["ĠThanks", "Ġfor"]`｜当前：`["Ġsharing"]`｜后2：`["Ġit", ".ĊĊ"]`。
- 阅读文本：" Thanks for"｜**" sharing"**｜" it.\n\n"。
- 下一token标签（不参与路由）：" it"。选择原因：highest_nonTop10_frequency.

## 97. R22／专家1／feature 13924

- TRAIN激活频率p=0.0016830895；EVAL专家内q=0.018976423；支持99/5217；名单负责专家=1（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117669，文件token偏移8400635，块内763。
- 前2：`["Ġwhile", "Ġchasing"]`｜当前：`["Ġor"]`｜后2：`["Ġat", "Ġleast"]`。
- 阅读文本：" while chasing"｜**" or"**｜" at least"。
- 下一token标签（不参与路由）：" at"。选择原因：assigned_low_target_largest_support.

## 98. R22／专家1／feature 9313

- TRAIN激活频率p=0.0015912847；EVAL专家内q=0.017059613；支持89/5217；名单负责专家=1（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117720，文件token偏移8452218，块内122。
- 前2：`["Ġtest", "ĊĊ"]`｜当前：`["MARK"]`｜后2：`["ĠLONG", "ĠAP"]`。
- 阅读文本：" test\n\n"｜**"MARK"**｜" LONG AP"。
- 下一token标签（不参与路由）：" LONG"。选择原因：assigned_low_target_largest_support.

## 99. R22／专家1／feature 3794

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0040253019；支持21/5217；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117717，文件token偏移8449703，块内679。
- 前2：`[",", "Ġfor"]`｜当前：`["-profit"]`｜后2：`["Ġcapital", "Ġworks"]`。
- 阅读文本：", for"｜**"-profit"**｜" capital works"。
- 下一token标签（不参与路由）：" capital"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 100. R22／专家1／feature 9137

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.00095840521；支持5/5217；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117701，文件token偏移8433225，块内585。
- 前2：`["Ġand", "Ġcan"]`｜当前：`["Ġenlight"]`｜后2：`["en", "Ġme"]`。
- 阅读文本：" and can"｜**" enlight"**｜"en me"。
- 下一token标签（不参与路由）："en"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 101. R22／专家2／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.67611005；支持4964/7342；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117672，文件token偏移8403699，块内755。
- 前2：`["Ġthen", "Ġsometimes"]`｜当前：`["Ġshe"]`｜后2：`["âĢĻs", "Ġon"]`。
- 阅读文本：" then sometimes"｜**" she"**｜"’s on"。
- 下一token标签（不参与路由）："’s"。选择原因：highest_nonTop10_frequency.

## 102. R22／专家2／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.57532008；支持4224/7342；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117674，文件token偏移8405376，块内384。
- 前2：`[".", "ĠThey"]`｜当前：`["Ġwere"]`｜后2：`["Ġa", "Ġsad"]`。
- 阅读文本：". They"｜**" were"**｜" a sad"。
- 下一token标签（不参与路由）：" a"。选择原因：highest_nonTop10_frequency.

## 103. R22／专家2／feature 11329

- TRAIN激活频率p=0.0017136912；EVAL专家内q=0.019068374；支持140/7342；名单负责专家=2（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117694，文件token偏移8425493，块内21。
- 前2：`["Ġsix", "Ġguests"]`｜当前：`["Ġfrom"]`｜后2：`["ĠJapan", ";"]`。
- 阅读文本：" six guests"｜**" from"**｜" Japan;"。
- 下一token标签（不参与路由）：" Japan"。选择原因：assigned_low_target_largest_support.

## 104. R22／专家2／feature 10498

- TRAIN激活频率p=0.0016983904；EVAL专家内q=0.01634432；支持120/7342；名单负责专家=2（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117692，文件token偏移8424244，块内820。
- 前2：`["Ġthe", "Ġmore"]`｜当前：`["ĠProtestant"]`｜后2：`["Ġview", "Ġof"]`。
- 阅读文本：" the more"｜**" Protestant"**｜" view of"。
- 下一token标签（不参与路由）：" view"。选择原因：assigned_low_target_largest_support.

## 105. R22／专家2／feature 3794

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0021792427；支持16/7342；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117683，文件token偏移8414212，块内4。
- 前2：`["Ġleave", "Ġspeech"]`｜当前：`["Ġpros"]`｜后2：`["ody", "Ġunaffected"]`。
- 阅读文本：" leave speech"｜**" pros"**｜"ody unaffected"。
- 下一token标签（不参与路由）："ody"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 106. R22／专家2／feature 7272

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0028602561；支持21/7342；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117719，文件token偏移8451421，块内349。
- 前2：`["1", "0"]`｜当前：`["/"]`｜后2：`["2", "0"]`。
- 阅读文本："10"｜**"/"**｜"20"。
- 下一token标签（不参与路由）："2"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 107. R22／专家3／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.68346667；支持5126/7500；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117696，文件token偏移8428297，块内777。
- 前2：`["they", "Ġare"]`｜当前：`["Ġbetter"]`｜后2：`["Ġfor", "Ġmost"]`。
- 阅读文本："they are"｜**" better"**｜" for most"。
- 下一token标签（不参与路由）：" for"。选择原因：highest_nonTop10_frequency.

## 108. R22／专家3／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.61453333；支持4609/7500；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117682，文件token偏移8413534，块内350。
- 前2：`["Ġuse", "Ġto"]`｜当前：`["Ġrecognize"]`｜后2：`["Ġthe", "Ġemotion"]`。
- 阅读文本：" use to"｜**" recognize"**｜" the emotion"。
- 下一token标签（不参与路由）：" the"。选择原因：highest_nonTop10_frequency.

## 109. R22／专家3／feature 5374

- TRAIN激活频率p=0.0023027725；EVAL专家内q=0.015866667；支持119/7500；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117665，文件token偏移8396656，块内880。
- 前2：`["Ġhormones", "Ġthey"]`｜当前：`["Ġget"]`｜后2：`["Ġwhen", "Ġthey"]`。
- 阅读文本：" hormones they"｜**" get"**｜" when they"。
- 下一token标签（不参与路由）：" when"。选择原因：assigned_low_target_largest_support.

## 110. R22／专家3／feature 5329

- TRAIN激活频率p=0.0020962115；EVAL专家内q=0.017333333；支持130/7500；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117715，文件token偏移8447320，块内344。
- 前2：`["Ġbe", "Ġsignificantly"]`｜当前：`["Ġless"]`｜后2：`["Ġthan", "Ġwhat"]`。
- 阅读文本：" be significantly"｜**" less"**｜" than what"。
- 下一token标签（不参与路由）：" than"。选择原因：assigned_low_target_largest_support.

## 111. R22／专家3／feature 2157

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0018666667；支持14/7500；名单负责专家=4（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117686，文件token偏移8417430，块内150。
- 前2：`["Ġ[", "t"]`｜当前：`["("]`｜后2：`["2", "9"]`。
- 阅读文本：" [t"｜**"("**｜"29"。
- 下一token标签（不参与路由）："2"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 112. R22／专家3／feature 3794

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0021333333；支持16/7500；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117666，文件token偏移8397743，块内943。
- 前2：`["Ġto", "Ġ*"]`｜当前：`["actively"]`｜后2：`["*", "Ġdisplay"]`。
- 阅读文本：" to *"｜**"actively"**｜"* display"。
- 下一token标签（不参与路由）："*"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 113. R22／专家4／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.63350077；支持3279/5176；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117665，文件token偏移8396574，块内798。
- 前2：`["Ġshould", "Ġnot"]`｜当前：`["Ġhave"]`｜后2：`["Ġmarried", "Ġanyway"]`。
- 阅读文本：" should not"｜**" have"**｜" married anyway"。
- 下一token标签（不参与路由）：" married"。选择原因：highest_nonTop10_frequency.

## 114. R22／专家4／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.55370943；支持2866/5176；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117721，文件token偏移8453514，块内394。
- 前2：`["Ġwindow", "Ġwhen"]`｜当前：`["Ġrad"]`｜后2：`["ion", "u"]`。
- 阅读文本：" window when"｜**" rad"**｜"ionu"。
- 下一token标签（不参与路由）："ion"。选择原因：highest_nonTop10_frequency.

## 115. R22／专家4／feature 14834

- TRAIN激活频率p=0.002180366；EVAL专家内q=0.017774343；支持92/5176；名单负责专家=4（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117705，文件token偏移8436855，块内119。
- 前2：`["Ġ$", "5"]`｜当前：`["."]`｜后2：`["6", "Ġmillion"]`。
- 阅读文本：" $5"｜**"."**｜"6 million"。
- 下一token标签（不参与路由）："6"。选择原因：assigned_low_target_largest_support.

## 116. R22／专家4／feature 5578

- TRAIN激活频率p=0.0018666993；EVAL专家内q=0.017387944；支持90/5176；名单负责专家=4（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117690，文件token偏移8421957，块内581。
- 前2：`["ian", ","]`｜当前：`["Ġlike"]`｜后2：`["Ġthe", "Ġrest"]`。
- 阅读文本："ian,"｜**" like"**｜" the rest"。
- 下一token标签（不参与路由）：" the"。选择原因：assigned_low_target_largest_support.

## 117. R22／专家4／feature 2157

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0056027821；支持29/5176；名单负责专家=4（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117695，文件token偏移8427366，块内870。
- 前2：`["ĠChe", "ez"]`｜当前：`["-"]`｜后2：`["its", "Ġare"]`。
- 阅读文本：" Cheez"｜**"-"**｜"its are"。
- 下一token标签（不参与路由）："its"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 118. R22／专家4／feature 7272

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0038639876；支持20/5176；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117681，文件token偏移8412796，块内636。
- 前2：`["(", "1"]`｜当前：`[","]`｜后2：`["2", "8"]`。
- 阅读文本："(1"｜**","**｜"28"。
- 下一token标签（不参与路由）："2"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 119. R22／专家5／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.66189687；支持7586/11461；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117660，文件token偏移8391470，块内814。
- 前2：`["ĠAnonymous", ","]`｜当前：`["Ġthank"]`｜后2：`["Ġyou", "Ġfor"]`。
- 阅读文本：" Anonymous,"｜**" thank"**｜" you for"。
- 下一token标签（不参与路由）：" you"。选择原因：highest_nonTop10_frequency.

## 120. R22／专家5／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.50571503；支持5796/11461；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117683，文件token偏移8414507，块内299。
- 前2：`["Ġdiffering", "Ġby"]`｜当前：`["Ġtheir"]`｜后2：`["Ġfinal", "Ġpitch"]`。
- 阅读文本：" differing by"｜**" their"**｜" final pitch"。
- 下一token标签（不参与路由）：" final"。选择原因：highest_nonTop10_frequency.

## 121. R22／专家5／feature 9107

- TRAIN激活频率p=0.0024098782；EVAL专家内q=0.010993805；支持126/11461；名单负责专家=5（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117691，文件token偏移8423110，块内710。
- 前2：`["Ġfather", "ĠGregory"]`｜当前：`[",Ċ"]`｜后2：`["A", "Ġsuccinct"]`。
- 阅读文本：" father Gregory"｜**",\n"**｜"A succinct"。
- 下一token标签（不参与路由）："A"。选择原因：assigned_low_target_largest_support.

## 122. R22／专家5／feature 7381

- TRAIN激活频率p=0.0015912847；EVAL专家内q=0.020068057；支持230/11461；名单负责专家=5（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117705，文件token偏移8436960，块内224。
- 前2：`["Ġin", "Ġthe"]`｜当前：`["Ġ"]`｜后2：`["1", "9"]`。
- 阅读文本：" in the"｜**" "**｜"19"。
- 下一token标签（不参与路由）："1"。选择原因：assigned_low_target_largest_support.

## 123. R22／专家5／feature 2157

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0020068057；支持23/11461；名单负责专家=4（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117682，文件token偏移8413735，块内551。
- 前2：`["Ġwith", "ĠF"]`｜当前：`["("]`｜后2：`["1", ","]`。
- 阅读文本：" with F"｜**"("**｜"1,"。
- 下一token标签（不参与路由）："1"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 124. R22／专家5／feature 3794

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.00043626211；支持5/11461；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117664，文件token偏移8394816，块内64。
- 前2：`["Ġin", "Ġa"]`｜当前：`["Ġsystematic"]`｜后2：`["Ġsociety", "Ġthat"]`。
- 阅读文本：" in a"｜**" systematic"**｜" society that"。
- 下一token标签（不参与路由）：" society"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 125. R22／专家6／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.65557382；支持9574/14604；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117687，文件token偏移8418564，块内260。
- 前2：`["Ġtheir", "Ġclassification"]`｜当前：`["Ġof"]`｜后2：`["Ġeach", "Ġproduction"]`。
- 阅读文本：" their classification"｜**" of"**｜" each production"。
- 下一token标签（不参与路由）：" each"。选择原因：highest_nonTop10_frequency.

## 126. R22／专家6／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.6291427；支持9188/14604；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117701，文件token偏移8433595，块内955。
- 前2：`["Ġbatter", "),"]`｜当前：`["Ġwith"]`｜后2：`["Ġbacon", "Ġand"]`。
- 阅读文本：" batter),"｜**" with"**｜" bacon and"。
- 下一token标签（不参与路由）：" bacon"。选择原因：highest_nonTop10_frequency.

## 127. R22／专家6／feature 12862

- TRAIN激活频率p=0.0023486749；EVAL专家内q=0.026225692；支持383/14604；名单负责专家=6（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117681，文件token偏移8413031，块内871。
- 前2：`["Ġas", "Ġbetween"]`｜当前：`["Ġtwo"]`｜后2：`["Ġtones", "Ġlying"]`。
- 阅读文本：" as between"｜**" two"**｜" tones lying"。
- 下一token标签（不参与路由）：" tones"。选择原因：assigned_low_target_largest_support.

## 128. R22／专家6／feature 10013

- TRAIN激活频率p=0.0022645205；EVAL专家内q=0.022665023；支持331/14604；名单负责专家=6（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117689，文件token偏移8420375，块内23。
- 前2：`["Ġexplor", "ations"]`｜当前：`["Ġinto"]`｜后2：`["Ġdevelopmental", "Ġmusical"]`。
- 阅读文本：" explorations"｜**" into"**｜" developmental musical"。
- 下一token标签（不参与路由）：" developmental"。选择原因：assigned_low_target_largest_support.

## 129. R22／专家6／feature 2157

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.00047932073；支持7/14604；名单负责专家=4（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117669，文件token偏移8400298，块内426。
- 前2：`["Ġand", "Ġself"]`｜当前：`["-"]`｜后2：`["ent", "ilt"]`。
- 阅读文本：" and self"｜**"-"**｜"entilt"。
- 下一token标签（不参与路由）："ent"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 130. R22／专家6／feature 3794

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0015064366；支持22/14604；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117664，文件token偏移8395232，块内480。
- 前2：`["ĠShe", "Ġunknow"]`｜当前：`["ingly"]`｜后2：`["Ġhas", "Ġbecome"]`。
- 阅读文本：" She unknow"｜**"ingly"**｜" has become"。
- 下一token标签（不参与路由）：" has"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 131. R22／专家7／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.65619512；支持3363/5125；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117683，文件token偏移8414219，块内11。
- 前2：`["Ġassess", "Ġthis"]`｜当前：`["Ġhypothesis"]`｜后2：`["Ġregarding", "Ġthe"]`。
- 阅读文本：" assess this"｜**" hypothesis"**｜" regarding the"。
- 下一token标签（不参与路由）：" regarding"。选择原因：highest_nonTop10_frequency.

## 132. R22／专家7／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.58185366；支持2982/5125；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117701，文件token偏移8432837，块内197。
- 前2：`["ĠYork", "Ġwas"]`｜当前：`["Ġa"]`｜后2：`["Ġrevelation", "Ġto"]`。
- 阅读文本：" York was"｜**" a"**｜" revelation to"。
- 下一token标签（不参与路由）：" revelation"。选择原因：highest_nonTop10_frequency.

## 133. R22／专家7／feature 15412

- TRAIN激活频率p=0.0022874717；EVAL专家内q=0.017365854；支持89/5125；名单负责专家=7（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117689，文件token偏移8421261，块内909。
- 前2：`["ĠI", "Ġquestioned"]`｜当前：`["Ġhim"]`｜后2：`["Ġin", "Ġregard"]`。
- 阅读文本：" I questioned"｜**" him"**｜" in regard"。
- 下一token标签（不参与路由）：" in"。选择原因：assigned_low_target_largest_support.

## 134. R22／专家7／feature 10992

- TRAIN激活频率p=0.001935553；EVAL专家内q=0.02204878；支持113/5125；名单负责专家=7（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117662，文件token偏移8393569，块内865。
- 前2：`["Ġwoman", "Ġare"]`｜当前：`["Ġno"]`｜后2：`["Ġlonger", "Ġwoman"]`。
- 阅读文本：" woman are"｜**" no"**｜" longer woman"。
- 下一token标签（不参与路由）：" longer"。选择原因：assigned_low_target_largest_support.

## 135. R22／专家7／feature 7272

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0013658537；支持7/5125；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117709，文件token偏移8440906，块内74。
- 前2：`["0", "9"]`｜当前：`["Ġ--"]`｜后2：`["Ġproved", "Ġthat"]`。
- 阅读文本："09"｜**" --"**｜" proved that"。
- 下一token标签（不参与路由）：" proved"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 136. R22／专家7／feature 9137

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0052682927；支持27/5125；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117673，文件token偏移8404978，块内1010。
- 前2：`["Ġup", "Ġto"]`｜当前：`["Ġmy"]`｜后2：`["Ġwaist", ","]`。
- 阅读文本：" up to"｜**" my"**｜" waist,"。
- 下一token标签（不参与路由）：" waist"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 137. R33／专家0／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.72458287；支持9771/13485；名单负责专家=5（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117691，文件token偏移8423409，块内1009。
- 前2：`["Ġreceive", "Ġa"]`｜当前：`["Ġbook"]`｜后2：`[",", "Ġit"]`。
- 阅读文本：" receive a"｜**" book"**｜", it"。
- 下一token标签（不参与路由）：","。选择原因：highest_nonTop10_frequency.

## 138. R33／专家0／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.65880608；支持8884/13485；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117700，文件token偏移8431878，块内262。
- 前2：`["Ġ(", "meaning"]`｜当前：`["Ġnot"]`｜后2：`["Ġfatty", "Ġenough"]`。
- 阅读文本：" (meaning"｜**" not"**｜" fatty enough"。
- 下一token标签（不参与路由）：" fatty"。选择原因：highest_nonTop10_frequency.

## 139. R33／专家0／feature 9292

- TRAIN激活频率p=0.0024175286；EVAL专家内q=0.011568409；支持156/13485；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117694，文件token偏移8426009，块内537。
- 前2：`["5", "Ċ"]`｜当前：`["9"]`｜后2：`[".", "ĠMatt"]`。
- 阅读文本："5\n"｜**"9"**｜". Matt"。
- 下一token标签（不参与路由）："."。选择原因：assigned_low_target_largest_support.

## 140. R33／专家0／feature 11329

- TRAIN激活频率p=0.0017136912；EVAL专家内q=0.032035595；支持432/13485；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117713，文件token偏移8445511，块内583。
- 前2：`["Ġknowing", "ĠBl"]`｜当前：`["azer"]`｜后2：`["Ġfans", ","]`。
- 阅读文本：" knowing Bl"｜**"azer"**｜" fans,"。
- 下一token标签（不参与路由）：" fans"。选择原因：assigned_low_target_largest_support.

## 141. R33／专家0／feature 3794

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.002373007；支持32/13485；名单负责专家=2（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117661，文件token偏移8392568，块内888。
- 前2：`["Ġinto", "Ġsense"]`｜当前：`["less"]`｜后2：`["Ġpower", "Ġstruggles"]`。
- 阅读文本：" into sense"｜**"less"**｜" power struggles"。
- 下一token标签（不参与路由）：" power"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 142. R33／专家0／feature 7272

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.00037078235；支持5/13485；名单负责专家=5（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117720，文件token偏移8452311，块内215。
- 前2：`["Ġa", "Ġfor"]`｜当前：`["kl"]`｜后2：`["ift", "\""]`。
- 阅读文本：" a for"｜**"kl"**｜"ift\""。
- 下一token标签（不参与路由）："ift"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 143. R33／专家1／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.61831789；支持1735/2806；名单负责专家=5（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117664，文件token偏移8395056，块内304。
- 前2：`["Ġwouldn", "'t"]`｜当前：`["Ġbe"]`｜后2：`["Ġraising", "Ġchildren"]`。
- 阅读文本：" wouldn't"｜**" be"**｜" raising children"。
- 下一token标签（不参与路由）：" raising"。选择原因：highest_nonTop10_frequency.

## 144. R33／专家1／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.58125445；支持1631/2806；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117667，文件token偏移8398717，块内893。
- 前2：`["Ġand", "ĊĊ"]`｜当前：`["ĠĠĠ"]`｜后2：`["Ġ", "2"]`。
- 阅读文本：" and\n\n"｜**"   "**｜" 2"。
- 下一token标签（不参与路由）：" "。选择原因：highest_nonTop10_frequency.

## 145. R33／专家1／feature 2987

- TRAIN激活频率p=0.0024557806；EVAL专家内q=0.032430506；支持91/2806；名单负责专家=1（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117710，文件token偏移8442507，块内651。
- 前2：`["Ġconcerned", "Ġwith"]`｜当前：`["Ġwhat"]`｜后2：`["Ġbrand", "Ġand"]`。
- 阅读文本：" concerned with"｜**" what"**｜" brand and"。
- 下一token标签（不参与路由）：" brand"。选择原因：assigned_low_target_largest_support.

## 146. R33／专家1／feature 7948

- TRAIN激活频率p=0.0024481302；EVAL专家内q=0.026728439；支持75/2806；名单负责专家=1（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117659，文件token偏移8390502，块内870。
- 前2：`["Ġbecause", "Ġwe"]`｜当前：`["Ġtake"]`｜后2：`["Ġcare", "Ġof"]`。
- 阅读文本：" because we"｜**" take"**｜" care of"。
- 下一token标签（不参与路由）：" care"。选择原因：assigned_low_target_largest_support.

## 147. R33／专家1／feature 2113

- TRAIN激活频率p=0.0015377318；EVAL专家内q=0.0017818959；支持5/2806；名单负责专家=2（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117713，文件token偏移8445373，块内445。
- 前2：`["7", "th"]`｜当前：`["Ġto"]`｜后2：`["Ġ", "2"]`。
- 阅读文本："7th"｜**" to"**｜" 2"。
- 下一token标签（不参与路由）：" "。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 148. R33／专家1／feature 2157

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0064148254；支持18/2806；名单负责专家=1（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117682，文件token偏移8413735，块内551。
- 前2：`["Ġwith", "ĠF"]`｜当前：`["("]`｜后2：`["1", ","]`。
- 阅读文本：" with F"｜**"("**｜"1,"。
- 下一token标签（不参与路由）："1"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 149. R33／专家2／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.74776975；支持7041/9416；名单负责专家=5（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117667，文件token偏移8397941，块内117。
- 前2：`[",", "ĠTV"]`｜当前：`[","]`｜后2：`["Ġmovies", ","]`。
- 阅读文本：", TV"｜**","**｜" movies,"。
- 下一token标签（不参与路由）：" movies"。选择原因：highest_nonTop10_frequency.

## 150. R33／专家2／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.57890824；支持5451/9416；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117659，文件token偏移8390555，块内923。
- 前2：`["ated", ","]`｜当前：`["Ġused"]`｜后2：`[",", "Ġabused"]`。
- 阅读文本："ated,"｜**" used"**｜", abused"。
- 下一token标签（不参与路由）：","。选择原因：highest_nonTop10_frequency.

## 151. R33／专家2／feature 6145

- TRAIN激活频率p=0.0021497644；EVAL专家内q=0.010407816；支持98/9416；名单负责专家=2（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117686，文件token偏移8418065，块内785。
- 前2：`["Ġsinging", "Ġproduction"]`｜当前：`["Ġof"]`｜后2：`["Ġonly", "Ġseven"]`。
- 阅读文本：" singing production"｜**" of"**｜" only seven"。
- 下一token标签（不参与路由）：" only"。选择原因：assigned_low_target_largest_support.

## 152. R33／专家2／feature 7462

- TRAIN激活频率p=0.0018973009；EVAL专家内q=0.011363636；支持107/9416；名单负责专家=2（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117720，文件token偏移8452553，块内457。
- 前2：`["Ġto", "Ġdrive"]`｜当前：`["Ġthese"]`｜后2：`["Ġcars", "."]`。
- 阅读文本：" to drive"｜**" these"**｜" cars."。
- 下一token标签（不参与路由）：" cars"。选择原因：assigned_low_target_largest_support.

## 153. R33／专家2／feature 9137

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0018054376；支持17/9416；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117671，文件token偏移8402452，块内532。
- 前2：`[",", "Ġback"]`｜当前：`["Ġup"]`｜后2：`["Ġto", "Ġthe"]`。
- 阅读文本：", back"｜**" up"**｜" to the"。
- 下一token标签（不参与路由）：" to"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 154. R33／专家2／feature 15492

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0013806287；支持13/9416；名单负责专家=4（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117677，文件token偏移8408238，块内174。
- 前2：`["ĠA", "Ġcentury"]`｜当前：`["Ġlater"]`｜后2：`[",", "ĠG"]`。
- 阅读文本：" A century"｜**" later"**｜", G"。
- 下一token标签（不参与路由）：","。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 155. R33／专家3／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.65514348；支持3904/5959；名单负责专家=5（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117680，文件token偏移8411530，块内394。
- 前2：`["Ġin", "Ġeach"]`｜当前：`["Ġfamily"]`｜后2：`["Ġwho", "Ġwere"]`。
- 阅读文本：" in each"｜**" family"**｜" who were"。
- 下一token标签（不参与路由）：" who"。选择原因：highest_nonTop10_frequency.

## 156. R33／专家3／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.54455446；支持3245/5959；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117701，文件token偏移8433042，块内402。
- 前2：`["Ġthe", "Ġlast"]`｜当前：`["Ġtime"]`｜后2：`["ĠI", "Ġhad"]`。
- 阅读文本：" the last"｜**" time"**｜" I had"。
- 下一token标签（不参与路由）：" I"。选择原因：highest_nonTop10_frequency.

## 157. R33／专家3／feature 14375

- TRAIN激活频率p=0.0021191627；EVAL专家内q=0.021480114；支持128/5959；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117679，文件token偏移8410581，块内469。
- 前2：`[".", "7"]`｜当前：`["*"]`｜后2：`["8", "0"]`。
- 阅读文本：".7"｜**"*"**｜"80"。
- 下一token标签（不参与路由）："8"。选择原因：assigned_low_target_largest_support.

## 158. R33／专家3／feature 1186

- TRAIN激活频率p=0.0020350083；EVAL专家内q=0.019466353；支持116/5959；名单负责专家=3（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117699，文件token偏移8431266，块内674。
- 前2：`["Ġdry", ","]`｜当前：`["Ġit"]`｜后2：`["Ġwas", "Ġreally"]`。
- 阅读文本：" dry,"｜**" it"**｜" was really"。
- 下一token标签（不参与路由）：" was"。选择原因：assigned_low_target_largest_support.

## 159. R33／专家3／feature 7272

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0025172009；支持15/5959；名单负责专家=5（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117719，文件token偏移8451421，块内349。
- 前2：`["1", "0"]`｜当前：`["/"]`｜后2：`["2", "0"]`。
- 阅读文本："10"｜**"/"**｜"20"。
- 下一token标签（不参与路由）："2"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 160. R33／专家3／feature 9137

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0010068803；支持6/5959；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117697，文件token偏移8428933，块内389。
- 前2：`["Ġand", "Ġwith"]`｜当前：`["Ġgood"]`｜后2：`[",", "Ġgood"]`。
- 阅读文本：" and with"｜**" good"**｜", good"。
- 下一token标签（不参与路由）：","。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 161. R33／专家4／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.6694626；支持6864/10253；名单负责专家=5（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117686，文件token偏移8417541，块内261。
- 前2：`["us", "ia"]`｜当前：`["Ġperform"]`｜后2：`["Ġpoorly", "Ġin"]`。
- 阅读文本："usia"｜**" perform"**｜" poorly in"。
- 下一token标签（不参与路由）：" poorly"。选择原因：highest_nonTop10_frequency.

## 162. R33／专家4／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.60928509；支持6247/10253；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117682，文件token偏移8413641，块内457。
- 前2：`["ĠThis", "Ġdistinction"]`｜当前：`["Ġdoes"]`｜后2：`["Ġnot", "Ġemerge"]`。
- 阅读文本：" This distinction"｜**" does"**｜" not emerge"。
- 下一token标签（不参与路由）：" not"。选择原因：highest_nonTop10_frequency.

## 163. R33／专家4／feature 8214

- TRAIN激活频率p=0.0022262684；EVAL专家内q=0.020189213；支持207/10253；名单负责专家=4（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117720，文件token偏移8452441，块内345。
- 前2：`["Ġheaded", "Ġback"]`｜当前：`["Ġto"]`｜后2：`["ĠNorth", "ĠCarolina"]`。
- 阅读文本：" headed back"｜**" to"**｜" North Carolina"。
- 下一token标签（不参与路由）：" North"。选择原因：assigned_low_target_largest_support.

## 164. R33／专家4／feature 9313

- TRAIN激活频率p=0.0015912847；EVAL专家内q=0.015605189；支持160/10253；名单负责专家=4（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117712，文件token偏移8444101，块内197。
- 前2：`["iving", "Ġup"]`｜当前：`["ĠO"]`｜后2：`["Ġboards", ","]`。
- 阅读文本："iving up"｜**" O"**｜" boards,"。
- 下一token标签（不参与路由）：" boards"。选择原因：assigned_low_target_largest_support.

## 165. R33／专家4／feature 2157

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.001365454；支持14/10253；名单负责专家=1（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117687，文件token偏移8418886，块内582。
- 前2：`[";", "Ġt"]`｜当前：`["("]`｜后2：`["8", ")"]`。
- 阅读文本："; t"｜**"("**｜"8)"。
- 下一token标签（不参与路由）："8"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 166. R33／专家4／feature 3794

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.001365454；支持14/10253；名单负责专家=2（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117717，文件token偏移8449703，块内679。
- 前2：`[",", "Ġfor"]`｜当前：`["-profit"]`｜后2：`["Ġcapital", "Ġworks"]`。
- 阅读文本：", for"｜**"-profit"**｜" capital works"。
- 下一token标签（不参与路由）：" capital"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 167. R33／专家5／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.66422618；支持5897/8878；名单负责专家=5（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117699，文件token偏移8431030，块内438。
- 前2：`["ĠSunday", "Ġafternoon"]`｜当前：`["Ġwhen"]`｜后2：`["Ġwe", "Ġwere"]`。
- 阅读文本：" Sunday afternoon"｜**" when"**｜" we were"。
- 下一token标签（不参与路由）：" we"。选择原因：highest_nonTop10_frequency.

## 168. R33／专家5／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.54584366；支持4846/8878；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117683，文件token偏移8414340，块内132。
- 前2：`["Ġstatement", "."]`｜当前：`["ĠThe"]`｜后2：`["Ġpitch", "Ġchange"]`。
- 阅读文本：" statement."｜**" The"**｜" pitch change"。
- 下一token标签（不参与路由）：" pitch"。选择原因：highest_nonTop10_frequency.

## 169. R33／专家5／feature 12587

- TRAIN激活频率p=0.0024481302；EVAL专家内q=0.023879252；支持212/8878；名单负责专家=5（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117682，文件token偏移8414091，块内907。
- 前2：`["Ġmusic", "Ġin"]`｜当前：`["Ġa"]`｜后2：`["Ġrather", "Ġconsistent"]`。
- 阅读文本：" music in"｜**" a"**｜" rather consistent"。
- 下一token标签（不参与路由）：" rather"。选择原因：assigned_low_target_largest_support.

## 170. R33／专家5／feature 10498

- TRAIN激活频率p=0.0016983904；EVAL专家内q=0.021175941；支持188/8878；名单负责专家=5（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117677，文件token偏移8408959，块内895。
- 前2：`["Ġspecificity", "Ġof"]`｜当前：`["Ġthe"]`｜后2：`["Ġauditory", "Ġdisorder"]`。
- 阅读文本：" specificity of"｜**" the"**｜" auditory disorder"。
- 下一token标签（不参与路由）：" auditory"。选择原因：assigned_low_target_largest_support.

## 171. R33／专家5／feature 2157

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.00078846587；支持7/8878；名单负责专家=1（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117716，文件token偏移8449020，块内1020。
- 前2：`["-l", "ord"]`｜当前：`["-"]`｜后2：`["king", "-controlled"]`。
- 阅读文本："-lord"｜**"-"**｜"king-controlled"。
- 下一token标签（不参与路由）："king"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 172. R33／专家5／feature 3794

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0013516558；支持12/8878；名单负责专家=2（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117686，文件token偏移8418051，块内771。
- 前2：`["Ġafter", "Ġthe"]`｜当前：`["Ġexper"]`｜后2：`["im", "enter"]`。
- 阅读文本：" after the"｜**" exper"**｜"imenter"。
- 下一token标签（不参与路由）："im"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 173. R33／专家6／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.68082735；支持5497/8074；名单负责专家=5（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117711，文件token偏移8443128，块内248。
- 前2：`["Ġcomment", "Ġabout"]`｜当前：`["Ġphotography"]`｜后2：`["Ġnot", "Ġbeing"]`。
- 阅读文本：" comment about"｜**" photography"**｜" not being"。
- 下一token标签（不参与路由）：" not"。选择原因：highest_nonTop10_frequency.

## 174. R33／专家6／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.56229874；支持4540/8074；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117668，文件token偏移8398863，块内15。
- 前2：`["Ġour", "Ġcollege"]`｜当前：`["Ġyears"]`｜后2：`["Ġthat", "Ġblack"]`。
- 阅读文本：" our college"｜**" years"**｜" that black"。
- 下一token标签（不参与路由）：" that"。选择原因：highest_nonTop10_frequency.

## 175. R33／专家6／feature 1924

- TRAIN激活频率p=0.0023180733；EVAL专家内q=0.010403765；支持84/8074；名单负责专家=6（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117667，文件token偏移8398014，块内190。
- 前2：`["ĠSo", "Ġhe"]`｜当前：`["Ġwill"]`｜后2：`["Ġnot", "Ġhave"]`。
- 阅读文本：" So he"｜**" will"**｜" not have"。
- 下一token标签（不参与路由）：" not"。选择原因：assigned_low_target_largest_support.

## 176. R33／专家6／feature 10992

- TRAIN激活频率p=0.001935553；EVAL专家内q=0.014614813；支持118/8074；名单负责专家=6（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117713，文件token偏移8445846，块内918。
- 前2：`["Ġthere", "'s"]`｜当前：`["Ġno"]`｜后2：`["Ġneed", "Ġto"]`。
- 阅读文本：" there's"｜**" no"**｜" need to"。
- 下一token标签（不参与路由）：" need"。选择原因：assigned_low_target_largest_support.

## 177. R33／专家6／feature 2157

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.00074312608；支持6/8074；名单负责专家=1（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117692，文件token偏移8424033，块内609。
- 前2：`["1", "1"]`｜当前：`["-"]`｜后2：`["0", "8"]`。
- 阅读文本："11"｜**"-"**｜"08"。
- 下一token标签（不参与路由）："0"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 178. R33／专家6／feature 3794

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0042110478；支持34/8074；名单负责专家=2（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117685，文件token偏移8416938，块内682。
- 前2：`[".", "ĠInc"]`｜当前：`["idental"]`｜后2：`["Ġencoding", "Ġof"]`。
- 阅读文本：". Inc"｜**"idental"**｜" encoding of"。
- 下一token标签（不参与路由）：" encoding"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 179. R33／专家7／feature 10778

- TRAIN激活频率p=0.74703164；EVAL专家内q=0.63420609；支持4142/6531；名单负责专家=5（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117696，文件token偏移8428278，块内758。
- 前2：`["Ġitself", ".ĊĊ"]`｜当前：`["ĠĠĠ"]`｜后2：`["Ġ", "2"]`。
- 阅读文本：" itself.\n\n"｜**"   "**｜" 2"。
- 下一token标签（不参与路由）：" "。选择原因：highest_nonTop10_frequency.

## 180. R33／专家7／feature 1053

- TRAIN激活频率p=0.67175929；EVAL专家内q=0.55871995；支持3649/6531；名单负责专家=0（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117681，文件token偏移8412961，块内801。
- 前2：`["Ġthe", "Ġmost"]`｜当前：`["Ġlikely"]`｜后2：`["Ġorigin", "Ġof"]`。
- 阅读文本：" the most"｜**" likely"**｜" origin of"。
- 下一token标签（不参与路由）：" origin"。选择原因：highest_nonTop10_frequency.

## 181. R33／专家7／feature 9658

- TRAIN激活频率p=0.0023563254；EVAL专家内q=0.027560864；支持180/6531；名单负责专家=7（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117693，文件token偏移8424899，块内451。
- 前2：`["Ġby", "Ġit"]`｜当前：`[".'"]`｜后2：`["ĠBut", ","]`。
- 阅读文本：" by it"｜**".'"**｜" But,"。
- 下一token标签（不参与路由）：" But"。选择原因：assigned_low_target_largest_support.

## 182. R33／专家7／feature 601

- TRAIN激活频率p=0.0018360977；EVAL专家内q=0.026335936；支持172/6531；名单负责专家=7（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117663，文件token偏移8393824，块内96。
- 前2：`[".ĊĊ", "Ġ"]`｜当前：`["Ġ"]`｜后2：`["1", "2"]`。
- 阅读文本：".\n\n "｜**" "**｜"12"。
- 下一token标签（不参与路由）："1"。选择原因：assigned_low_target_largest_support.

## 183. R33／专家7／feature 2157

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.0045934773；支持30/6531；名单负责专家=1（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117695，文件token偏移8427339，块内843。
- 前2：`["ĠChe", "ez"]`｜当前：`["-"]`｜后2：`["its", "Ġare"]`。
- 阅读文本：" Cheez"｜**"-"**｜"its are"。
- 下一token标签（不参与路由）："its"。选择原因：lowest_nonTop10_frequency_with_n>=5.

## 184. R33／专家7／feature 3794

- TRAIN激活频率p=0.0015300814；EVAL专家内q=0.00076557954；支持5/6531；名单负责专家=2（−1为未指定）。
- 文件 `/data/share/109_cache_dir/hf_data/dclm_bin/global-shard_01_of_10/local-shard_2_of_10_shard_00000247_processed.bin`；上下文117661，文件token偏移8391746，块内66。
- 前2：`["Ġon", "Ġto"]`｜当前：`["Ġmistakenly"]`｜后2：`["Ġfail", "Ġan"]`。
- 阅读文本：" on to"｜**" mistakenly"**｜" fail an"。
- 下一token标签（不参与路由）：" fail"。选择原因：lowest_nonTop10_frequency_with_n>=5.


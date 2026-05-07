# round_continual_3 micro_semantic_token_audit

## Reliability Audit

- 成功模型数: 3
- 汇总来源: `/data/250010109/spectral_router/exp_TRACE/output/round_continual_3/per_model_metrics.json`
- 评测层: [2, 6, 10]
- Top-50 在内部按 token 最大 logit 去重排序，表格展示 Top-30。

## 实验做法细节

- 数据与抽样：WOS `validate` 固定抽样 5000 条，text=`abstract`，label=`domain`。
- 模型口径：`linear_running_center`、`acp_lite`、`quadratic_nosvd_debias`，统一 `checkpoint-40000`。
- 前向与截取：评测层 [2, 6, 10]，在对应 `mlp` 前向前钩子抓取 routing 输入。
- logits 定义：统一使用 pre-softmax router logits；linear 用 `gate(x)`，acp_lite 用 `acp_gate_center+acp_gate_residual`，quadratic 用 `linear_router+quadratic_router`。
- token 对齐：按 `attention_mask` 过滤有效 token，logits 与 `input_ids` 一一对齐。
- 排序规则：对每个 expert、每个 token id 保留全数据最大 logit，再做全局降序，内部保留 Top-50。
- 解码清洗：用 tokenizer 单 token 解码；去掉空白项与特殊 token。
- 表格展示：每个 expert 展示 Top-30，确保可读性与信息量平衡。

## 为什么每个 expert 看起来 token 数一样

- 表格里的 token 数是展示配额，不是路由负载：每个 expert 固定展示 Top-30（内部保留 Top-50），所以看起来数量一致。
- 真正“路由到该 expert 的 token 数”在 `Top1 Routed Tokens` 列，会明显不一样。
- 若某个 expert 的 `Top1 Routed Tokens` 很小但仍有 Top-30，这是因为它仍可从全量样本里选出最高分 token，只是覆盖面较窄。

## 最终分析

- 你看到“规律不明显”是正常现象：BPE 子词会把语义拆成词片，单 token 粒度天然更碎。
- 规律主要体现在“类别倾向”而不是完整单词：例如数字/符号、功能词、学科术语、词缀片段。
- `quadratic_nosvd_debias` 的多个 expert 在概念类词片上更集中，`acp_lite` 与 linear 模型中数字/符号专家更显著。
- 当前证据支持“微语义分工存在”，并且可在三层同时观察到。
- 层间差异以 Top-30 token 集合 Jaccard 衡量（同 expert id 对齐）：
  - acp_lite 2->6 平均 Jaccard=0.0223
  - acp_lite 6->10 平均 Jaccard=0.0108
  - acp_lite 2->10 平均 Jaccard=0.0043
  - linear_running_center 2->6 平均 Jaccard=0.0130
  - linear_running_center 6->10 平均 Jaccard=0.0087
  - linear_running_center 2->10 平均 Jaccard=0.0043
  - quadratic_nosvd_debias 2->6 平均 Jaccard=0.0150
  - quadratic_nosvd_debias 6->10 平均 Jaccard=0.0043
  - quadratic_nosvd_debias 2->10 平均 Jaccard=0.0044
- 解释：Jaccard 越低说明层间词片漂移越明显；越高说明该模型在相邻层的专家语义更稳定。

## 跨层总览

| Model Alias | Layer | Token Count | Experts | Max Top1 Routed | Min Top1 Routed |
| --- | ---: | ---: | ---: | ---: | ---: |
| acp_lite | 2 | 632846 | 8 | 139797 | 7772 |
| acp_lite | 6 | 632846 | 8 | 210838 | 14010 |
| acp_lite | 10 | 632846 | 8 | 193016 | 4623 |
| linear_running_center | 2 | 632846 | 8 | 146293 | 15665 |
| linear_running_center | 6 | 632846 | 8 | 269354 | 2003 |
| linear_running_center | 10 | 632846 | 8 | 217860 | 531 |
| quadratic_nosvd_debias | 2 | 632846 | 8 | 242261 | 31199 |
| quadratic_nosvd_debias | 6 | 632846 | 8 | 347120 | 1440 |
| quadratic_nosvd_debias | 10 | 632846 | 8 | 262656 | 260 |

## Experiment -> Theory Result Card

### Model: qwen3-moe-H768-linear_running_center_acp_lite_on_8gpu-center_running-gate_off-acp_on-lb_0-linear (Layer 2)

| Expert ID | Top1 Routed Tokens | Top Tokens (by max logit) | Extracted Feature Guess |
| --- | ---: | --- | --- |
| Expert 0 | 20890 | "There", "Let", "here", "It", "od", "il", "ath", "-", "UG", "ur", "in", "isen", "or", "b", "are", "CH", "g", "we", "Here", "CP", "av", "after", "It", "x", "by", "arth", "is", "it", "c", "qu" | Domain/content terms |
| Expert 1 | 121477 | "about", "of", "male", "men", "ically", "care", "'s", "opinion", "izing", "evidence", "ing", "writers", "female", "adults", "theories", "ized", "ly", "knowledge", "youth", "bearing", "elder", "Youth", "beliefs", "personality", "persons", "ial", "child", "care", "adult", "intellectual" | Domain/content terms |
| Expert 2 | 7772 | """, "dr", "'", "p", "`", "d", "h", "c", "fr", "in", "Mr", "sm", "ex", "://", "rep", "end", "ended", "r", "pro", "amb", "ab", "n", "do", "ch", "g", "b", "adm", "Home", "3", "Dr" | Domain/content terms |
| Expert 3 | 91843 | "D", "li", "eb", "G", "ann", "n", "r", "ol", "M", "ieg", "B", "V", "enz", "IN", "A", "S", "he", "FP", "EB", "pan", "op", "eh", "ale", "IS", "om", "upp", "oon", "R", "Y", "C" | Domain/content terms |
| Expert 4 | 52529 | "-eight", "-nine", "four", "-four", "eight", "%", "-two", "%", "-six", "-five", "-", "%-", "November", "7", "-seven", "nine", "four", "1", "5", "2", "March", "July", "6", "+", "percent", "9", "August", "0", "3", "8" | Domain/content terms |
| Expert 5 | 139797 | "to", "into", "on", "down", "restrict", "for", "-off", "up", "by", "toward", "divert", "adapt", "susceptible", "ed", "convert", "with", "fit", "ing", "-of", "in", "-in", "towards", "from", "iate", "ening", "out", "poses", "ease", "-f", "-to" | Domain/content terms |
| Expert 6 | 119811 | "-east", "air", "waves", "tunnel", "belt", "of", "-based", "junction", "tidal", "front", "water", "mass", "Sea", "plane", "foot", "wave", "cover", "of", "-end", "al", "control", "-time", "turbine", "nuclear", "War", "field", "line", "gate", "energy", "clearance" | Domain/content terms |
| Expert 7 | 78727 | "such", "cert", "to", "part", "follows", "ym", "p", "with", "well", "for", "n", "per", "As", "expected", "pir", "many", "compared", "suggested", "opposed", "usual", "done", "far", "cor", "What", "is", "part", "in", "But", "shown", "of" | Domain/content terms |

### Model: qwen3-moe-H768-linear_running_center_acp_lite_on_8gpu-center_running-gate_off-acp_on-lb_0-linear (Layer 6)

| Expert ID | Top1 Routed Tokens | Top Tokens (by max logit) | Extracted Feature Guess |
| --- | ---: | --- | --- |
| Expert 0 | 52593 | "3", "7", "6", "1", "8", "0", "4", "5", "2", "-", ".", "9", ",", ":", "IEEE", "-five", "m", "degrees", "to", "km", "m", "%", "/", "(", "Rev", "-", "x", "kW", "-four", "-year" | Domain/content terms |
| Expert 1 | 201136 | "a", "wide", "striking", "marked", "their", "serious", "growing", "increasing", "finer", "stress", "greatly", "dramatic", "-sh", "burdens", "sustained", "an", "alarming", "changes", "disrupt", "quality", "on", "results", "value", "key", "far", "different", "demand", "widespread", "heightened", "savings" | Domain/content terms |
| Expert 2 | 14507 | ":", ".", ")", "reserved", """, "'", "creativecommons", ").", "clusions", ".Method", "in", "by", ".h", "Results", "IVE", "an", "):", "s", "(", "Conclusion", "Published", "see", "http", ".org", "The", "doi", ".-", "summar", "://", "ER" | Domain/content terms |
| Expert 3 | 53245 | ",", "specifically", "especially", "such", "particularly", "and", "to", "or", "-,", "a", "most", "ie", "in", "including", "),", "avoids", "-", "prevent", "even", ";", "(", "are", "for", "studying", "has", "mostly", "many", "how", "namely", "mainly" | Domain/content terms |
| Expert 4 | 210838 | "-key", "key", "encryption", "crypt", "domain", "amer", "IP", "matching", "interface", "PCR", "ase", "multiplication", "on", "ifier", "representation", "addresses", "abeled", "tests", "capacitor", "element", "programming", "expression", "factor", "containers", "switched", "ode", "-vector", "polymer", "ran", "electron" | Domain/content terms |
| Expert 5 | 24959 | "know", "followed", "seek", "had", "might", "understand", "have", "you", "consider", "expect", "thesized", "spent", "involved", "recognize", "believe", "would", "to", "intrigued", "take", "wished", "encounter", "perceive", "we", "viewed", "do", "reasoned", "reluctant", "developed", "note", "they" | Domain/content terms |
| Expert 6 | 14010 | "ch", "ob", "arr", "and", "uf", "son", "Crist", "aram", "uss", "sch", "st", "esh", "up", "h", "ae", "cz", "for", "sw", "ar", "-B", "ass", "Red", "ius", "oz", "ou", "ad", "rens", "z", ".", "Kol" | Domain/content terms |
| Expert 7 | 61558 | "yet", "case", "as", "though", "which", "much", "however", "such", ",", "until", "times", "well", "if", "therefore", "so", "end", "result", "now", "example", "addition", "consequence", "respect", "hand", "importantly", "than", "),", "context", "reason", "far", "recently" | Domain/content terms |

### Model: qwen3-moe-H768-linear_running_center_acp_lite_on_8gpu-center_running-gate_off-acp_on-lb_0-linear (Layer 10)

| Expert ID | Top1 Routed Tokens | Top Tokens (by max logit) | Extracted Feature Guess |
| --- | ---: | --- | --- |
| Expert 0 | 106235 | "ultr", "sy", "Tr", "cyc", "Coch", "Qu", "Es", "Ph", "qu", "Emb", "emb", "extr", "-qu", "tro", "Fr", "hy", "phy", "amph", "fr", "nec", "ep", "rem", "Hy", "ph", "-ph", "Hyp", "hydro", "marg", "br", "ne" | Domain/content terms |
| Expert 1 | 18072 | "uck", "Andre", "Dan", "Castle", "Fay", "Fried", "Gates", "Jane", "Caleb", "Glenn", "Patrick", "Tall", "Jacob", "Russell", "John", "Bad", "Marsh", "Global", "Stan", "Bell", "Gilbert", "Sara", "Boss", "Beck", "Golden", "Lyn", "Vladimir", "Eduardo", "Gale", "Christ" | Domain/content terms |
| Expert 2 | 4623 | "larg", "binary", "conting", "purpos", "applic", "consequ", "remed", "estim", "steroids", "recept", "Binary", "inclus", "caus", "ampl", "regist", "necess", "effic", "adequ", "dut", "compar", "inher", "conserv", "allow", "definit", "incid", "innoc", "repar", "toler", "continu", "perman" | Domain/content terms |
| Expert 3 | 67741 | "towards", "toward", "to", "from", "mimic", "with", "than", "below", "supporting", "over", "oppose", "support", "for", "upon", "appreciate", "on", "makes", "about", "solve", "of", "surrounding", "promote", "around", "against", "remembering", "without", "protect", "above", "preventing", "beyond" | Domain/content terms |
| Expert 4 | 193016 | "structural", "clinical", "medical", "Clinical", "our", "empirical", "biological", "laboratory", "multiple", "various", "infectious", "pathological", "new", "the", "demographic", "two", "practical", "general", "key", "intellectual", "several", "broad", "molecular", "occupational", "three", "reproductive", "ological", "etic", "this", "physiological" | Domain/content terms |
| Expert 5 | 56883 | "is", "well", "routinely", "therefore", "rapidly", "generally", "also", "often", "increasingly", "practically", "broadly", "highly", "ally", "may", "has", "not", "extremely", "must", "newly", "can", "certainly", "mechanically", "widely", "usually", "economically", "be", "ationally", "thus", "sometimes", "especially" | Domain/content terms |
| Expert 6 | 140781 | "carried", "taken", "take", "brings", "brought", "moves", "go", "carrying", "goes", "vivo", "driven", "put", "progressed", "site", "atively", "progress", "come", "coming", "benefits", "laid", "attention", "moving", "voters", "adopted", "stage", "lies", "comes", "falls", "criticism", "set" | Domain/content terms |
| Expert 7 | 45495 | "We", "We", "we", "to", "would", "have", "recently", "So", "you", "been", "I", "should", "they", "Who", "now", "Why", "To", "When", "are", "either", "who", "can", "How", "he", "will", "and", "easily", "must", "ically", "particularly" | Domain/content terms |

### Model: qwen3-moe-H768--linear_running_center_8gpu_gbs768-center_running-gate_off-acp_off-lb_0-linear (Layer 2)

| Expert ID | Top1 Routed Tokens | Top Tokens (by max logit) | Extracted Feature Guess |
| --- | ---: | --- | --- |
| Expert 0 | 65521 | "R", "F", "M", "G", "P", "A", "CA", "B", "V", "H", "IS", "PR", "N", "1", "DF", "IT", "PS", "T", "Z", "K", "E", "CH", "MA", "p", "CR", "MO", "O", "D", "US", "SS" | Domain/content terms |
| Expert 1 | 97931 | "most", "half", "of", "year", "-order", "-line", "highest", "steps", "-leading", "erg", "six", "-generation", "choice", "step", "important", "Year", "two", "decade", "week", "different", "years", "attempts", "decades", "part", "-person", "few", "Next", "-year", "generation", "hundred" | Domain/content terms |
| Expert 2 | 129581 | "-st", "p", "-in", "di", "pin", "-through", "-w", "risk", "used", "uneven", "-re", "-d", "tract", "represented", "ex", "time", "est", "-the", "-", "active", "-f", "-s", "part", "extended", "extr", "-en", "weight", "extent", "-speed", "develop" | Domain/content terms |
| Expert 3 | 15665 | "qu", "c", "UG", "g", "hh", "I", "w", "UD", "What", "b", "ig", "CH", "rr", "There", "AD", "You", "PT", "CS", "IS", "ur", "ber", "been", "OP", "is", "now", "are", "Else", "RR", "x", "Z" | Domain/content terms |
| Expert 4 | 61763 | "al", "man", "ica", "ke", "ak", "stein", "ol", "ian", "as", "Bay", "chi", "z", "u", "ov", "itz", "at", "hoff", "ich", "ob", "ie", "ella", "ic", "an", "oder", "i", "el", "anmar", "oram", "antan", "in" | Domain/content terms |
| Expert 5 | 68454 | "iv", "mit", "ep", "ag", "ir", "But", "allo", "ind", "ur", "op", ".", "enz", "But", "".", "em", "ob", "for", "ie", "ter", "ox", "age", "if", "(", ").", "rob", "Finally", "however", "eg", "'.", "ree" | Domain/content terms |
| Expert 6 | 47638 | "ar", "al", "ol", "irc", "ert", "yc", "rit", "as", "ob", "ac", "av", "antic", "ost", "em", "ag", "isc", "ab", "an", "olar", "se", "vers", "in", "erring", "oll", "gr", "ect", "amb", "par", "l", "aint" | Domain/content terms |
| Expert 7 | 146293 | "valve", "ports", "valves", "controller", "partition", "-pass", "wheels", "processing", "coverage", "performance", "signal", "locks", "transfer", "detection", "flow", "systems", "interface", "circuit", "execution", "structure", "table", "bandwidth", "transmission", "frequencies", "driver", "signals", "pump", "communication", "vibration", "converter" | Domain/content terms |

### Model: qwen3-moe-H768--linear_running_center_8gpu_gbs768-center_running-gate_off-acp_off-lb_0-linear (Layer 6)

| Expert ID | Top1 Routed Tokens | Top Tokens (by max logit) | Extracted Feature Guess |
| --- | ---: | --- | --- |
| Expert 0 | 30657 | "of", "urg", "for", "an", "F", "Pen", "and", "National", "Technology", "on", "had", "Institute", "United", "Development", "una", "aba", "Affairs", "presidential", "in", ",", "Fe", "in", ".K", "International", "University", "South", "asa", "Health", "Sudan", "Academy" | Domain/content terms |
| Expert 1 | 176489 | "Reduce", "Language", "al", "key", "search", "matrices", "algebra", "distributed", "etric", "language", "ex", "ology", "ically", "image", "measure", "-point", "atical", "Neural", "Learning", "the", "vector", "parallel", "words", "and", "prime", "ational", "uzzy", "in", "ynomial", "of" | Domain/content terms |
| Expert 2 | 5054 | "re", "(", "The", "5", "musical", "and", "hym", "dramas", "the", "music", "film", "in", "ns", "8", "ues", "or", ",", "television", "onte", ")", "),", "to", "cine", "ass", "WATCH", "F", "1", "Fear", "pos", "line" | Domain/content terms |
| Expert 3 | 49553 | "and", "1", "to", "ty", "5", "3", "0", "%", "9", "4", "Twenty", "years", "-", "7", "hundred", "twenty", "th", "8", "2", "in", "billion", "6", "million", "of", "-of", ".", "week", "-six", "forty", "per" | Domain/content terms |
| Expert 4 | 2003 | "agus", "ah", "ia", "Din", "to", "ly", "footsteps", "x", "of", ",", "hy", "don", "column", "us", "figure", "husband", "ince", "from", "Other", "re", "skeletal", "ghost", "life", "fire", "Qu", "a", "it", "City", "ore", "remains" | Domain/content terms |
| Expert 5 | 84043 | "to", "also", "longer", "only", "been", ";", "recognize", "believe", "have", "unknown", "short", "but", "even", "play", "is", "do", "remained", "and", "problem", "if", "facing", "lessons", ",", "can", "just", "be", "explored", "no", "they", "though" | Domain/content terms |
| Expert 6 | 269354 | "elial", "omer", "ort", "lastic", "y", "oc", "-cell", "melan", "el", "in", "al", "opathy", "yl", "endoth", "acet", "-car", "ular", "uc", "age", "ate", "rotein", "om", "ph", "ab", "on", "ator", "phosph", "at", "D", "op" | Domain/content terms |
| Expert 7 | 15693 | "1", "0", "-", "6", "3", "/", ".", "5", ".org", "2", "/by", "OL", ".html", "nd", "creativecommons", "M", "(", "/C", "http", "/licenses", "b", "9", "4", "VI", "S", "iley", "F", "7", "://", "OA" | Domain/content terms |

### Model: qwen3-moe-H768--linear_running_center_8gpu_gbs768-center_running-gate_off-acp_off-lb_0-linear (Layer 10)

| Expert ID | Top1 Routed Tokens | Top Tokens (by max logit) | Extracted Feature Guess |
| --- | ---: | --- | --- |
| Expert 0 | 30796 | ".", ").", ":", "):", ".)", "-", "Here", "?", ")].", "to", "IVE", "IVES", ")", "First", ":", "METHODS", "Methods", "When", "Moreover", "Next", "."", "here", "Firstly", "Well", "Next", "%).", "Secondly", "Here", ",", "Please" | Punctuation / symbols |
| Expert 1 | 799 | "anny", "Caleb", "John", "Jane", "Mr", "Lady", "Dick", "Simon", "Witch", "ory", "Ferdinand", "Vladimir", "Santa", "Sergei", "Russell", "Benjamin", "Angel", "iff", "Cynthia", "God", "Amit", "olf", "Eduardo", "Richard", "Harry", "Ludwig", "Bob", "N", "Sara", "Kate" | Domain/content terms |
| Expert 2 | 43669 | "initially", "they", "may", "would", "are", "been", "never", "becomes", "has", "can", "to", "was", "ancestors", "became", "we", "soon", "not", "be", "cannot", "is", "have", "increasingly", "being", "might", "quite", "easily", "protagonists", "students", "insiders", "yet" | Domain/content terms |
| Expert 3 | 531 | "binary", "is", "pills", "focus", "azole", "steroids", ")", "ality", "are", "aimed", "tim", "concern", "relevant", "pty", "leth", "conce", "pid", "can", "scrutin", "know", "Tem", "comp", "Gre", "Cou", "mix", "paper", "Pl", "rost", "stre", "Spr" | Domain/content terms |
| Expert 4 | 217860 | "the", "itable", "a", "'s", "of", "Western", "psychological", "your", "social", "general", "diverse", "verbal", "many", "ative", "reproductive", "Early", "Social", "central", "national", "ical", "their", "different", "multiple", "important", "our", "its", "numerous", "political", "In", "real" | Domain/content terms |
| Expert 5 | 105088 | "dil", "-r", "phy", "-dis", "anth", "L", "ab", "prec", "Spir", "suppl", "displ", "-enh", "H", "Emb", "pro", "recom", "poly", "fr", "dys", "cad", "collo", "Ev", "te", "eup", "C", "Dys", "tre", "-de", "agr", "Tra" | Domain/content terms |
| Expert 6 | 214505 | "factors", "leaks", "model", "behaviors", "ites", "death", "pression", "assessments", "water", "fuel", "investment", "treatment", "Activity", "Theory", "characterization", "simulations", "data", "topic", "schizophrenia", "therapy", "Security", "ified", "changes", "measurements", "Food", "obesity", "land", "impairment", "ols", "electricity" | Domain/content terms |
| Expert 7 | 19598 | "to", "and", "At", "than", "<=", "at", "=", "is", "at", "below", "around", "if", "of", "as", "equals", "where", "with", "let", "about", "from", "->", "between", "size", "return", "If", "by", "using", "very", "when", "," | Function words |

### Model: qwen3-moe-H768-quadratic_nosvd_running_center_8gpu_debias-center_running-gate_off-acp_off-lb_0-quadratic_nosvd (Layer 2)

| Expert ID | Top1 Routed Tokens | Top Tokens (by max logit) | Extracted Feature Guess |
| --- | ---: | --- | --- |
| Expert 0 | 242261 | "motor", "power", "vehicles", "thermal", "vehicle", "hybrid", "electric", "Energy", "energy", "hydrogen", "ed", "Light", "Thermal", "-wave", "harmonic", "ity", "shock", "isation", "speed", "phot", "distortion", "ic", "transportation", "field", "Power", "emission", "idal", "water", "Level", "storage" | Domain/content terms |
| Expert 1 | 99594 | "'.", "(", "4", "8", "].", "6", "0", ";", "and", "-", "5", "2", "7", "".", ").", "').", "3", "9", ".", "1", "or", "ado", ")."", "ie", ".,", ");", ",.", "i", ".]", "*)" | Punctuation / symbols |
| Expert 2 | 38420 | "erg", "y", "-generation", "United", "Mexico", "een", "year", "most", "second", "Three", "ty", "New", "-", "principal", "-in", "-order", "first", "the", "Kingdom", "all", "decade", "hundred", "majority", "-party", "my", "art", "of", "teen", "Philadelphia", "number" | Domain/content terms |
| Expert 3 | 36373 | "steadily", "Can", "Does", "av", "drastically", "consistently", "gradually", "recently", "readily", "ine", "relatively", "greatly", "progressively", "increasingly", "sufficiently", "up", "vastly", "or", "to", "slightly", "hardly", "significantly", "way", "rarely", "opy", "themselves", "repeatedly", "help", "E", "narrowly" | Domain/content terms |
| Expert 4 | 77481 | "During", "p", "by", "In", "z", "late", "March", "fl", "After", "-c", "Between", "By", "tra", "cent", "At", "-in", "the", "st", "-st", "situ", "con", "ade", "fin", "Within", "in", "flamm", "-re", "lie", "ert", "el" | Domain/content terms |
| Expert 5 | 31199 | "ch", "ik", "ia", "ater", "ure", "if", "il", "-up", "it", "smiles", "av", "chat", "ing", "-to", "on", "ath", "talk", "-ahead", "looking", "-made", "believe", "man", "iac", "lessness", "pat", "h", "worry", "inas", "ayed", "isen" | Domain/content terms |
| Expert 6 | 62185 | "ra", "ou", "M", "H", "ol", "C", "D", "rit", "T", "ur", "un", "PT", "ase", "U", "F", "r", "RE", "ont", "R", "Ps", "omb", "al", "IS", "S", "c", "oli", "ad", "in", "ret", "IM" | Domain/content terms |
| Expert 7 | 45333 | "such", "As", "per", "defined", "an", "a", "described", "distinct", "compared", "p", "cribed", "many", "ym", "As", "-s", "part", "n", "cert", "opposed", "an", "eline", "the", "cor", "-built", "part", "our", "done", "most", "soon", "phy" | Domain/content terms |

### Model: qwen3-moe-H768-quadratic_nosvd_running_center_8gpu_debias-center_running-gate_off-acp_off-lb_0-quadratic_nosvd (Layer 6)

| Expert ID | Top1 Routed Tokens | Top Tokens (by max logit) | Extracted Feature Guess |
| --- | ---: | --- | --- |
| Expert 0 | 35268 | "and", "undergraduate", "co", "graduate", "Science", "studies", "ing", "graduate", "undergrad", "Master", "career", "in", "working", "-level", "Department", "Sc", "courses", "apprentice", "business", "students", "college", "level", "university", "iting", "parents", "Teaching", "specialist", "Graduate", "married", "residency" | Domain/content terms |
| Expert 1 | 3115 | "have", "is", "remain", "exist", "remains", "be", "has", "no", "been", "are", "little", "limited", "a", ",", "to", "seems", "known", "appears", "exists", "happens", "were", "like", "currently", "still", "in", "reason", "many", "several", "meant", "evidence" | Domain/content terms |
| Expert 2 | 15473 | "Action", "Act", "political", "Convention", "passed", "presidential", "on", "of", "Executive", "public", "Rights", "Nations", "reform", "nationally", "Congress", "for", "government", "ed", "Federal", "the", ",", "protecting", "defined", "authorization", "strengthening", "parliamentary", "mandated", "igration", "fiscal", "elections" | Domain/content terms |
| Expert 3 | 5948 | "ch", "ikh", "z", "ibe", "irl", "ass", "ett", "a", "-Bar", "Red", "ob", "k", "ork", "es", "Crist", "ig", "Dar", "Rom", "g", "Sou", "b", "chen", "ri", "ugar", "West", "ew", "ak", "qu", "rez", "up" | Domain/content terms |
| Expert 4 | 1440 | "footsteps", "waiting", "to", "at", "heads", "outside", "cross", "wind", "ground", "smiling", "the", "a", "couch", "by", "from", "confronted", "crossings", ",", "ly", "rain", "ghost", "coming", "wrestling", "neck", "itated", "see", "stop", "door", "torch", "soon" | Domain/content terms |
| Expert 5 | 188296 | "logical", "meaning", "method", "itional", "reasoning", "conceptual", "fundamental", ",", "concept", "semantic", "but", "and", "nature", "assumption", "possibilities", "assumptions", "logic", "notion", "concepts", "reality", "role", "mathematical", "accuracy", "pragmatic", "Problem", "sense", "ving", "thinking", "ological", "principles" | Domain/content terms |
| Expert 6 | 347120 | "al", "meth", "osphate", "ine", "ative", "xygen", "yl", "ph", "ans", "5", "col", "id", "phen", "ellular", "ortic", "onic", "is", "xy", "occus", "ase", "oxy", "lateral", "oste", "atic", "hydro", "loid", "th", "transfer", "act", "plant" | Domain/content terms |
| Expert 7 | 36186 | "2", "BL", "1", "3", "5", "-", "7", "BY", "PH", "0", "FT", "UL", "/", "SE", "SP", "MED", "QU", "6", "AD", "4", "SER", "&", "8", "SH", "LL", "X", "9", "SL", "AM", "AB" | Domain/content terms |

### Model: qwen3-moe-H768-quadratic_nosvd_running_center_8gpu_debias-center_running-gate_off-acp_off-lb_0-quadratic_nosvd (Layer 10)

| Expert ID | Top1 Routed Tokens | Top Tokens (by max logit) | Extracted Feature Guess |
| --- | ---: | --- | --- |
| Expert 0 | 262656 | "the", "educational", "implementation", "our", "socioeconomic", "personal", "computational", "lifetime", "physical", "daily", ")", "of", "occupational", "psychological", "ocial", "wide", "health", "functional", "financial", "and", "clean", "social", "economic", "mental", "a", "their", "plays", "gaining", "great", "processing" | Domain/content terms |
| Expert 1 | 5360 | "incompetent", "partners", "parents", "leaders", "moral", "carriers", "figure", "recurring", "ghost", "The", "sex", "of", "language", "tales", "human", "ancy", "autonomy", "hope", "men", "profession", "women", "roles", "patriarch", "Church", "violent", "character", "opponents", "assumption", "the", "ators" | Domain/content terms |
| Expert 2 | 107337 | "g", "capac", "dis", "multip", "unic", "int", "exper", "-str", "d", "Ign", "g", "enef", "opro", "turb", "Dop", "op", "-ref", "-w", "subst", "param", "-br", "adv", "yst", "-com", "prest", "tro", "oc", "int", "-f", "rif" | Domain/content terms |
| Expert 3 | 38618 | "currently", "appropriately", "ably", "not", "widely", "ographically", "ally", "privately", "frequently", "heavily", "readily", "economically", "commercially", "and", "sometimes", "clinically", "really", "already", "cannot", "adequately", "should", "is", "ially", "ively", "commonly", "accurately", "ly", "fully", "ply", "strategically" | Domain/content terms |
| Expert 4 | 124016 | "Southern", "West", "Castle", "Swedish", "Pacific", "Northern", "Marine", "Gene", "International", "United", "North", "Royal", "East", "Lake", "Costa", "Central", "4", "Society", "South", "otechnology", "Miami", "Japan", "American", "Eastern", "Nova", "of", "European", "Policy", "Emerald", "Health" | Domain/content terms |
| Expert 5 | 92129 | "inear", "quadratic", "density", "its", "multiple", "olic", "determinant", "ous", "function", "convex", "ometric", "ian", "iton", "symmetric", "tensor", "by", "imensional", "matrices", "offsets", "tangent", "dispersion", "Tits", "essian", "surfaces", "field", "ric", "pair", "vin", "path", "conservation" | Domain/content terms |
| Expert 6 | 260 | "binary", "amid", "paper", "algebra", "mix", "sche", "Binary", "las", "arg", "i", "ind", "est", "ax", "psychology", "lith", "iph", "produced", "prospect", "clin", "amo", "vo", "sol", "ox", "ceph", "hydro", "rene", "mo", "syst", ".", "depot" | Domain/content terms |
| Expert 7 | 2470 | "years", "right", "come", "goes", "go", "coming", "back", "Out", "came", "out", "long", "day", "all", "gone", "days", "month", "up", "comes", "this", "decade", "a", "going", """, "Up", "footsteps", "Looking", ":", "kind", "Going", "instead" | Domain/content terms |


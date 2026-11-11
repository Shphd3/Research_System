# input_gate_trace

AI分析；研究者判断Unknown。

源：原训练4rank评估JSONL与MIG复算的FP32完整状态缓存；A5为训练同次捕获。用户明确接受微小偏差后继续，未改R04。

| arm   |   original_training_eval |   cache_unquantized |   fp16_position_mean |   cache_minus_original |   fp16_minus_cache | file                                                                                                                | sha256                                                           |
|:------|-------------------------:|--------------------:|---------------------:|-----------------------:|-------------------:|:--------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------|
| A5    |               4.039119   |          4.039119   |           4.0391189  |         0              |    -1.0318927e-07  | /data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/positions/A5/step002000.npz | 44476f99a66f39f65f0dd5ef563562fbc7de9a9cb3d73a0af45dcdb7f443e3d7 |
| A0    |               4.08314162 |          4.08314167 |           4.08314255 |         4.94274186e-08 |     8.7894833e-07  | /data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/positions/A0/step002000.npz | 62e51f099ab9303855c3faae85b560f8753f09538fdccd9ab7f2f7672a8a1ea8 |
| A1    |               4.15760435 |          4.15761426 |           4.15761372 |         9.90982602e-06 |    -5.35646008e-07 | /data/250010109/MoE_Router/experiments/20261109_atom_concentration_regularizer/analysis/positions/A1/step002000.npz | 5c69116db6af8595b513fed294834b589ce704b9bec779c7fb3830c3bcaf365e |

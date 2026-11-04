# Qwen3 加法P01配对监督终点

三个续训顺序种子、六个固定200步实际LoRA终点，共用同一B01起点 `e0b5321c343d88aac3c8118fb400086ee853f2157c58a12d53a3ad77ea1aecbb`。每步N/R输入64A＋64基础，先每序列CE均值再固定除128；只有基础系数N0/R1改变。旧I01尺度不同，不是本轮因果对照。[English](qwen_addition_p01_20261026.md)。

当前操作性条件满足：True；平均基础改善99.4444个百分点，平均A变化-2.0000个百分点。结果限于已暴露DEV行为，不证明内部模块、容量或MoE无用；未做TEST或B新推理。

- `adapter_qwen_addition_p01_20261026_s11_N_endpoint`：[文件](/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/paired_replay/p01_A_base_seqmean_s11_22_33/seed_11/N/checkpoints/endpoint.pt)，SHA-256 `550c03279497f2ba0374a5351a81e095b3eb4181e7e962fe87abfaf00b73933f`。
- `adapter_qwen_addition_p01_20261026_s11_R_endpoint`：[文件](/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/paired_replay/p01_A_base_seqmean_s11_22_33/seed_11/R/checkpoints/endpoint.pt)，SHA-256 `d2630d54094201f979001f9274c6832f99119d1249ba09c2932712fffbc9b2b7`。
- `adapter_qwen_addition_p01_20261026_s22_N_endpoint`：[文件](/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/paired_replay/p01_A_base_seqmean_s11_22_33/seed_22/N/checkpoints/endpoint.pt)，SHA-256 `d09b3c80f2713bf44dea569b32802a05e8adab0f1bedc072e16b790e0f58e802`。
- `adapter_qwen_addition_p01_20261026_s22_R_endpoint`：[文件](/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/paired_replay/p01_A_base_seqmean_s11_22_33/seed_22/R/checkpoints/endpoint.pt)，SHA-256 `d34dd93031aec90ede6ebc19678c78f379f624f442b8d577bcd645b6ca3711a6`。
- `adapter_qwen_addition_p01_20261026_s33_N_endpoint`：[文件](/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/paired_replay/p01_A_base_seqmean_s11_22_33/seed_33/N/checkpoints/endpoint.pt)，SHA-256 `c5a53b4c358545faa05184b10cb172ec92a817a3e3f9b7884a41bcca8a126b18`。
- `adapter_qwen_addition_p01_20261026_s33_R_endpoint`：[文件](/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/paired_replay/p01_A_base_seqmean_s11_22_33/seed_33/R/checkpoints/endpoint.pt)，SHA-256 `9cff8c7076b55aa46f43fff6193ee95d497fb4b558e30ed51330de78ba67185a`。

[六产物strict收据](checks/20261025T172510Z_qwen_addition_p01_endpoints.json)、[一页结果](/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/paired_replay/p01_A_base_seqmean_s11_22_33/summary_cn.md)与[配置](/data/250010109/MoE_Router/experiments/20261025_qwen_addition_qualification/paired_replay/p01_A_base_seqmean_s11_22_33/config.json)保留来源。父模型/tokenizer/数据/共同adapter ID在catalog身份中完整列出。每文件仅含81,920 FP32 block14 Q/K/V/O rank8 alpha16 dropout0 LoRA及optimizer/RNG/order/进度，不含完整BF16父模型。N的基础输入暴露不等于正权重监督。加载为source/engine.py::load_reusable；同进程恢复通过、外部exact resume未验证。登记不授予后续训练或发布权限。

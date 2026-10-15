# Interactive text continuation: Dense, S7 and SALL

[中文使用说明](README_cn.md)

`run_comparison.sh` invokes `compare_models.py` for local read-only inference.
No training, cloud submission, installation or download occurs.

```bash
cd /data/250010109/Research_System/daily_research_reports/1010/docs/model_evaluation
bash run_comparison.sh --check-only
bash run_comparison.sh                 # interactive, default Dense / S7 / SALL
bash run_comparison.sh --models base --base-source qwen
bash run_comparison.sh --decode sample --temperature 0.8 --top-p 0.95 --seed 42
bash run_comparison.sh "Introduce yourself:"   # one-shot
```

Type a single line at `输入>` and press Enter. The same raw text/token IDs go to
all selected models. Turns are independent; no history or chat template is added.
`/quit`, `/exit` or EOF exits; Ctrl-C interrupts and releases workers. Output is
printed after each model finishes its continuation, not streamed token by token.

**Every model defaults to 500 new tokens**, excluding the prompt. Emitted EOS
stops immediately. `--max-new-tokens N` changes the uniform cap. Stop reasons are
`eos`, `max_new_tokens` and `context_limit`. Native context is2048; long inputs may
leave fewer than500 available positions. Inputs are never silently cropped.

Default base is the eight-layer Dense exact-33B checkpoint; S7 is fresh lambda0.1
and SALL unit-weight, also exact33B. `--base-source qwen` selects original
28-layer Qwen3-0.6B-Base. This changes architecture and training lineage, so it is
not a matched quality comparison. Identities, paths and qualified native sources
come from the [asset registry](../../../../assets/README.md), checked each run.
Local Qwen generation/tokenizer configuration agrees on EOS151643,
`<|endoftext|>`. Declaration does not establish EOS frequency in training targets;
no such count was performed. The inspected native reader consumes existing token
bins without adding EOS. Failure to emit EOS within500 tokens cannot show it was
absent from training. Document completion and assistant-turn completion differ.

Default greedy decoding takes the highest-probability token at each step.
Optional sample decoding applies temperature and nucleus/top-p filtering, then
samples with the seed reset for every model/prompt. No repetition penalty is
applied. Less repetition under sampling would establish sensitivity to decoding,
not rule out training problems. All three models repeat in the supplied screenshot;
numbered lists may reflect continuation of an introduction guide/question list.
That interpretation remains a hypothesis; the screenshot cannot establish an SAE
cause. A larger cap observes longer behavior rather than fixing repetition.

Interactive workers each load once and **remain resident simultaneously**.
Use `--models s7` to reduce memory use. One-shot workers load and exit sequentially.
Native imports are isolated per process. Loading reuses native config/weights with
mmap/meta/strict assign; optimizer state is not restored. LM readout bypasses
auxiliary SAE loss computation. Prefixes are recomputed with no KV cache, including
original Qwen in this inspection script;500-token generation can therefore be slow.

CUDA is selected locally when available, otherwise CPU. `--device cpu`,
`--dtype bfloat16`, `MODEL_EVAL_PYTHON` and `MODEL_EVAL_DEPS_DIR` select existing
resources/environments. Float32 is the default. Optional `--output PATH` writes
completed results on normal interactive exit/handled interruption or batch success;
it refuses overwrite. Keep outputs execution-side. A failed run need not save.

Validation covers current selected asset access, dependency/tokenizer preflight,
tiny CPU native loading, EOS/cap/sampling controls, repeated interactive inputs and
worker cleanup. No new real-model500-token inference was performed for this change.

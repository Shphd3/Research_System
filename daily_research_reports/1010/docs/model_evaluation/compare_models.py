#!/usr/bin/env python3
"""Read-only text continuation for the registered exact-33B Dense/S7/SALL trio.

Reuse: each model's qualified native config/model and checkpoint schema.
Adaptation: mmap + meta/strict assign avoids loading optimizer tensors into RAM;
last-position LM logits and a simple uncached generation loop replace training/probing.
Each native implementation runs in a separate process to isolate dense_sae imports.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time

SYSTEM_ROOT = Path(__file__).resolve().parents[4]
ASSET_IDS = {
    "base": "model_dense_33b",
    "s7": "model_s7_fresh_lambda0p1_33b",
    "sall": "model_sall_unit_weight_33b",
    "qwen": "model_qwen3_0p6b_base",
}
TOKENIZER_ID = "tokenizer_qwen3_0p6b_base"


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def parser():
    p = argparse.ArgumentParser(description="相同原文输入，对比 base / S7 / SALL 的续写；不训练、不提交作业。")
    p.add_argument("--prompt", action="append", help="输入原文；可重复指定多个。不会加聊天模板。")
    p.add_argument("--models", nargs="+", choices=["base", "s7", "sall"], default=["base", "s7", "sall"])
    p.add_argument("--base-source", choices=["dense", "qwen"], default="dense", help="base默认8层Dense 33B；qwen为原始28层Qwen3-0.6B-Base。")
    p.add_argument("--max-new-tokens", type=int, default=500, help="所有所选模型统一的新增token上限，默认500；遇EOS提前停止。")
    p.add_argument("--interactive", action="store_true", help="加载后反复输入；没有--prompt时默认启用。/quit退出。")
    p.add_argument("--decode", choices=["greedy", "sample"], default="greedy")
    p.add_argument("--temperature", type=float, default=0.8, help="采样温度；greedy模式不使用。")
    p.add_argument("--top-p", type=float, default=0.95, help="采样保留累计概率达到此值的最小token集合。")
    p.add_argument("--seed", type=int, default=42, help="采样时每个模型、每段输入重设的随机种子。")
    p.add_argument("--serve", action="store_true", help=argparse.SUPPRESS)
    p.add_argument("--device", default="auto", help="auto / cpu / cuda / cuda:0；只使用本地设备。")
    p.add_argument("--dtype", choices=["float32", "bfloat16", "float16"], default="float32")
    p.add_argument("--output", type=Path, help="可选JSON结果地址；拒绝覆盖已有文件，建议放执行目录。")
    p.add_argument("--check-only", action="store_true", help="只检查资产、依赖及输入，不加载模型，不生成。")
    p.add_argument("--worker", choices=["base", "s7", "sall"], help=argparse.SUPPRESS)
    return p


def selected_specs(args):
    catalog = read_json(SYSTEM_ROOT / "assets/catalog.json")
    assets = {a["id"]: a for a in catalog["assets"]}
    specs = []
    for name in args.models:
        key = "qwen" if name == "base" and args.base_source == "qwen" else name
        asset = assets[ASSET_IDS[key]]
        location = Path(asset["locations"][0]["path"])
        native = key != "qwen"
        identity = asset["identity"]
        spec = {
            "name": name, "asset_id": asset["id"], "native": native,
            "checkpoint": str(location), "identity": identity,
            "max_new_tokens": args.max_new_tokens,
        }
        if native:
            spec["source_root"] = identity["qualified_vendor_code_root"]
        specs.append(spec)
    tokenizer_path = Path(assets[TOKENIZER_ID]["locations"][0]["path"])
    return specs, tokenizer_path


def check_inputs(specs):
    command = [sys.executable, str(SYSTEM_ROOT / "tools/check_assets.py"), "--strict", "--asset", TOKENIZER_ID]
    for spec in specs:
        command.extend(["--asset", spec["asset_id"]])
    subprocess.run(command, check=True)
    for spec in specs:
        if not spec["native"]:
            continue
        checkpoint = Path(spec["checkpoint"])
        manifest = read_json(checkpoint / "manifest.json")
        if manifest.get("complete") is not True or manifest.get("tokens_seen") != 33_000_000_000:
            raise ValueError(f"不是完整的精确33B检查点：{checkpoint}")
        state = next(f for f in manifest["files"] if f["path"] == "state.pt")
        if (checkpoint / "state.pt").stat().st_size != state["size_bytes"]:
            raise ValueError(f"state.pt大小与原manifest不符：{checkpoint}")
        source = Path(spec["source_root"]) / "dense_sae/model/modeling_qwen3_sae.py"
        if not source.is_file():
            raise FileNotFoundError(f"找不到此模型的原生实现：{source}")


def tokenizer_and_prompts(path, prompts):
    from tokenizers import Tokenizer

    tokenizer = Tokenizer.from_file(str(path / "tokenizer.json"))
    token = read_json(path / "tokenizer_config.json")["eos_token"]
    if isinstance(token, dict):
        token = token["content"]
    eos_id = tokenizer.token_to_id(token)
    if eos_id is None:
        raise ValueError(f"tokenizer内没有声明的停止符：{token}")
    encoded = [tokenizer.encode(text, add_special_tokens=False).ids for text in prompts]
    if any(not ids for ids in encoded):
        raise ValueError("输入必须至少编码出一个token。")
    return tokenizer, encoded, eos_id, token


def load_native(spec, device, dtype):
    """Read known local training-state weights; do not execute optimizer/resume."""
    import torch

    if any(name == "dense_sae" or name.startswith("dense_sae.") for name in sys.modules):
        raise RuntimeError("原生模块已导入；必须为每个模型使用独立worker。")
    sys.path.insert(0, spec["source_root"])
    from dense_sae.model import Qwen3SAEConfig, Qwen3SAEForCausalLM

    state_path = Path(spec["checkpoint"]) / "state.pt"
    payload = torch.load(state_path, map_location="cpu", weights_only=False, mmap=True)
    config = Qwen3SAEConfig.from_dict(payload["extra_training_state"]["model_config"])
    expected = spec["identity"]
    if config.num_hidden_layers != expected["layers"] or config.hidden_size != expected["hidden_size"]:
        raise ValueError("检查点模型配置与登记身份不符。")
    with torch.device("meta"):
        model = Qwen3SAEForCausalLM(config)
    # Strict loading covers all native backbone AND embedded SAE keys/shapes.
    model.load_state_dict(payload["model"], strict=True, assign=True)
    model = model.to(device=device, dtype=dtype).eval().requires_grad_(False)
    del payload
    return model, config.max_position_embeddings


def load_model(spec, device, dtype):
    if spec["native"]:
        return load_native(spec, device, dtype)
    from transformers import AutoModelForCausalLM

    model = AutoModelForCausalLM.from_pretrained(
        spec["checkpoint"], local_files_only=True, trust_remote_code=False,
        torch_dtype=dtype,
    ).to(device).eval().requires_grad_(False)
    return model, model.config.max_position_embeddings


def greedy_generate(next_logits, prompt_ids, *, eos_id, max_new_tokens, context_limit, device,
                    decode="greedy", temperature=0.8, top_p=0.95, seed=42):
    """Count only new tokens; an emitted EOS is counted, but an input EOS is not."""
    import torch

    if max_new_tokens <= 0:
        raise ValueError("生成上限必须为正整数。")
    if not prompt_ids or len(prompt_ids) >= context_limit:
        raise ValueError(f"输入需非空且短于上下文上限{context_limit}；不静默截断输入。")
    if decode not in {"greedy", "sample"} or not (0 < temperature < float("inf")) or not 0 < top_p <= 1:
        raise ValueError("解码参数无效：温度必须为正有限数，top-p需在(0,1]。")
    generator = torch.Generator(device=device).manual_seed(seed) if decode == "sample" else None
    sequence = torch.tensor([prompt_ids], dtype=torch.long, device=device)
    generated = []
    reason = "max_new_tokens"
    with torch.inference_mode():
        for _ in range(max_new_tokens):
            if sequence.shape[1] >= context_limit:
                reason = "context_limit"
                break
            logits = next_logits(sequence).float().reshape(-1)
            if not bool(torch.isfinite(logits).all()):
                raise FloatingPointError("下一token的logits出现NaN/Inf。")
            if decode == "greedy":
                next_id = int(logits.argmax().item())
            else:
                # Keep the token that crosses the threshold, including at least one.
                sorted_logits, order = torch.sort(logits / temperature, descending=True)
                probabilities = torch.softmax(sorted_logits, dim=-1)
                remove = probabilities.cumsum(dim=-1) - probabilities >= top_p
                sorted_logits[remove] = -float("inf")
                choice = torch.multinomial(torch.softmax(sorted_logits, dim=-1), 1, generator=generator)
                next_id = int(order[choice].item())
            generated.append(next_id)
            if next_id == eos_id:
                reason = "eos"
                break
            sequence = torch.cat([sequence, sequence.new_tensor([[next_id]])], dim=1)
    return generated, reason


def worker(args, specs, tokenizer_path, prompts):
    import torch
    from torch.nn import functional as F

    spec = next(s for s in specs if s["name"] == args.worker)
    tokenizer, encoded, eos_id, eos_token = tokenizer_and_prompts(tokenizer_path, prompts)
    if args.device == "auto":
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device(args.device)
    if device.type not in {"cpu", "cuda"}:
        raise ValueError("只支持cpu或本地cuda设备。")
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("当前Python没有可用CUDA；可显式指定--device cpu。")
    dtype = getattr(torch, args.dtype)
    started = time.monotonic()
    model, context_limit = load_model(spec, device, dtype)
    load_seconds = time.monotonic() - started

    def next_logits(ids):
        if spec["native"]:
            hidden = model.forward_intermediates(ids)["final_h"][:, -1, :]
            return F.linear(hidden, model.output_weight)
        hidden = model.model(input_ids=ids, use_cache=False).last_hidden_state[:, -1, :]
        return model.lm_head(hidden)

    metadata = {
        **spec, "device": str(device), "dtype": args.dtype, "context_limit": context_limit,
        "eos_token_id": eos_id, "eos_token": eos_token, "decoding": args.decode,
        "temperature": args.temperature if args.decode == "sample" else None,
        "top_p": args.top_p if args.decode == "sample" else None,
        "seed": args.seed if args.decode == "sample" else None,
        "kv_cache": False, "tokenizer": str(tokenizer_path), "loading_seconds": load_seconds,
    }

    def generate(text):
        ids = tokenizer.encode(text, add_special_tokens=False).ids
        started = time.monotonic()
        generated, reason = greedy_generate(
            next_logits, ids, eos_id=eos_id, max_new_tokens=spec["max_new_tokens"],
            context_limit=context_limit, device=device, decode=args.decode,
            temperature=args.temperature, top_p=args.top_p, seed=args.seed,
        )
        return {
            "prompt": text, "prompt_token_ids": ids, "generated_token_ids": generated,
            "continuation": tokenizer.decode(generated, skip_special_tokens=True),
            "continuation_with_special_tokens": tokenizer.decode(generated, skip_special_tokens=False),
            "generated_tokens": len(generated), "stop_reason": reason,
            "generation_seconds": time.monotonic() - started,
        }

    if args.serve:
        print(json.dumps({"ready": metadata}, ensure_ascii=False), flush=True)
        for line in sys.stdin:
            try:
                request = json.loads(line)
                if request.get("quit"):
                    break
                reply = {"result": generate(request["prompt"])}
            except (ValueError, KeyError, RuntimeError, FloatingPointError) as error:
                reply = {"error": str(error)}
            print(json.dumps(reply, ensure_ascii=False), flush=True)
    else:
        print(json.dumps({**metadata, "results": [generate(text) for text in prompts]},
                         ensure_ascii=False), flush=True)


def worker_command(args, name):
    return [sys.executable, str(Path(__file__).resolve()), "--worker", name,
            "--models", *args.models, "--base-source", args.base_source,
            "--max-new-tokens", str(args.max_new_tokens), "--device", args.device,
            "--dtype", args.dtype, "--decode", args.decode,
            "--temperature", str(args.temperature), "--top-p", str(args.top_p), "--seed", str(args.seed)]


def receive(process):
    line = process.stdout.readline()
    if not line:
        raise RuntimeError("模型worker提前退出；请查看上方错误，不会替换模型。")
    reply = json.loads(line)
    if "error" in reply:
        raise RuntimeError(reply["error"])
    return reply


def display(name, result):
    print(f"\n[{name}] 续写：{result['continuation'] or '（没有可显示文本）'}", flush=True)
    print(f"新token数：{result['generated_tokens']}；停止原因：{result['stop_reason']}；"
          f"生成耗时：{result['generation_seconds']:.1f}s", flush=True)


def close_workers(processes):
    for process in processes:
        if process.poll() is None:
            process.terminate()
    for process in processes:
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        process.stdin.close()
        process.stdout.close()


def interact(args, specs, tokenizer_path, reports):
    processes = []
    tokenizer, _, _, _ = tokenizer_and_prompts(tokenizer_path, [])
    try:
        for spec in specs:
            print(f"正在加载 {spec['name']}（交互期间常驻；每轮独立续写）……", flush=True)
            process = subprocess.Popen(worker_command(args, spec["name"]) + ["--serve"],
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       text=True, encoding="utf-8", bufsize=1)
            processes.append(process)
            metadata = receive(process)["ready"]
            reports.append({**metadata, "results": []})
            print(f"[{spec['name']}] 已加载，EOS={metadata['eos_token_id']}，"
                  f"加载{metadata['loading_seconds']:.1f}s", flush=True)
        print("输入文本后按回车；/quit或/exit退出。输入不会自动累积成聊天历史。", flush=True)
        while True:
            try:
                text = input("\n输入> ")
            except EOFError:
                break
            if text.strip() in {"/quit", "/exit"}:
                break
            if not text.strip():
                continue
            ids = tokenizer.encode(text, add_special_tokens=False).ids
            if not ids or any(len(ids) >= report["context_limit"] for report in reports):
                print("输入为空或超过所选模型的上下文边界；请缩短输入。", flush=True)
                continue
            print(f"输入{len(ids)}个token；每个模型最多新增{args.max_new_tokens}个token。", flush=True)
            for process, report in zip(processes, reports):
                print(f"[{report['name']}] 正在生成……", flush=True)
                process.stdin.write(json.dumps({"prompt": text}, ensure_ascii=False) + "\n")
                process.stdin.flush()
                result = receive(process)["result"]
                if result["prompt_token_ids"] != ids:
                    raise RuntimeError("worker输入token IDs与公共输入不一致。")
                report["results"].append(result)
                display(report["name"], result)
    except KeyboardInterrupt:
        print("\n已中断，释放模型进程。", flush=True)
    finally:
        close_workers(processes)


def main(argv=None):
    args = parser().parse_args(argv)
    if args.max_new_tokens <= 0:
        raise ValueError("--max-new-tokens必须为正整数。")
    if len(set(args.models)) != len(args.models):
        raise ValueError("--models不能重复。")
    if not (0 < args.temperature < float("inf")) or not 0 < args.top_p <= 1:
        raise ValueError("温度必须为正有限数，top-p需在(0,1]。")
    args.interactive = args.interactive or args.prompt is None
    prompts = args.prompt if args.prompt is not None else ["The capital of France is"]
    specs, tokenizer_path = selected_specs(args)
    if args.worker:
        worker(args, specs, tokenizer_path, prompts)
        return 0
    if args.output and args.output.exists():
        raise FileExistsError(f"拒绝覆盖已有结果：{args.output}")
    check_inputs(specs)
    if importlib.util.find_spec("torch") is None or importlib.util.find_spec("tokenizers") is None:
        raise RuntimeError("缺少torch/tokenizers。请用run_comparison.sh，或指定MODEL_EVAL_PYTHON及MODEL_EVAL_DEPS_DIR。")
    if any(not s["native"] for s in specs) and importlib.util.find_spec("transformers") is None:
        raise RuntimeError("Qwen原始模型还需要transformers；请用包含此依赖的Python环境。")
    _, encoded, eos_id, eos_token = tokenizer_and_prompts(tokenizer_path, prompts)
    for spec in specs:
        if spec["native"] and any(len(ids) >= 2048 for ids in encoded):
            raise ValueError("8层模型上下文为2048；输入太长，需留生成空间。")
    print(f"base={args.base_source}；相同原文/相同token IDs；{args.decode}；停止符={eos_token}({eos_id})", flush=True)
    for spec in specs:
        print(f"{spec['name']}: {spec['asset_id']}，最多{spec['max_new_tokens']}个新token", flush=True)
    if args.check_only:
        print("检查通过：未加载模型、未生成、未使用GPU计算。", flush=True)
        return 0
    reports = []
    if args.interactive:
        if args.prompt:
            raise ValueError("交互模式请直接在提示后输入文本；--prompt用于一次性批量模式。")
        interact(args, specs, tokenizer_path, reports)
    else:
        for spec in specs:
            print(f"\n正在加载 {spec['name']}（各模型顺序运行）……", flush=True)
            command = worker_command(args, spec["name"])
            for prompt in prompts:
                command.extend(["--prompt", prompt])
            completed = subprocess.run(command, text=True, encoding="utf-8", capture_output=True)
            if completed.stderr:
                print(completed.stderr, file=sys.stderr, end="", flush=True)
            if completed.returncode:
                raise RuntimeError(f"{spec['name']}加载或生成失败（退出码{completed.returncode}）；未尝试替换模型。")
            report = json.loads(completed.stdout)
            if [r["prompt_token_ids"] for r in report["results"]] != encoded:
                raise RuntimeError("worker输入token IDs与公共输入不一致。")
            reports.append(report)
            print(f"[{spec['name']}] {report['device']} / {report['dtype']}，加载{report['loading_seconds']:.1f}s", flush=True)
            for index, result in enumerate(report["results"], 1):
                print(f"\n输入{index}：{result['prompt']}\n续写：{result['continuation'] or '（没有可显示文本）'}", flush=True)
                print(f"新token数：{result['generated_tokens']}；停止原因：{result['stop_reason']}", flush=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as stream:
            json.dump({"created_at_utc": datetime.now(timezone.utc).isoformat(), "models": reports},
                      stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        print(f"\n结果已保存：{args.output.resolve()}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, KeyError, ImportError, FloatingPointError, subprocess.CalledProcessError) as error:
        print(f"错误：{error}", file=sys.stderr)
        raise SystemExit(1)

"""CPU-only generation controls and tiny native-model loading; no real weights."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
import io

import torch

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "daily_research_reports/1010/docs/model_evaluation/compare_models.py"
SPEC = importlib.util.spec_from_file_location("text_comparison", SCRIPT)
comparison = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(comparison)


class GenerationControlTest(unittest.TestCase):
    def generate(self, callback, prompt=None, cap=30, context=128):
        return comparison.greedy_generate(
            callback, [1, 2] if prompt is None else prompt, eos_id=7,
            max_new_tokens=cap, context_limit=context, device="cpu",
        )

    def test_emitted_eos_stops_and_counts_only_new_tokens(self):
        seen = []

        def callback(ids):
            seen.append(ids.tolist()[0])
            logits = torch.zeros(8)
            logits[3 if len(seen) == 1 else 7] = 1
            return logits

        generated, reason = self.generate(callback, prompt=[7, 1, 2])
        self.assertEqual(generated, [3, 7])
        self.assertEqual(reason, "eos")
        self.assertEqual(seen, [[7, 1, 2], [7, 1, 2, 3]])

    def test_no_eos_hits_500_new_tokens_excluding_prompt(self):
        calls = []

        def callback(ids):
            calls.append(ids.shape[1])
            return torch.tensor([0., 0., 1., 0., 0., 0., 0., 0.])

        generated, reason = self.generate(callback, prompt=list(range(20)), cap=500, context=600)
        self.assertEqual(len(generated), 500)
        self.assertEqual(reason, "max_new_tokens")
        self.assertEqual(calls, list(range(20, 520)))

    def test_context_boundary_stops_without_cropping_prompt(self):
        generated, reason = self.generate(lambda ids: torch.arange(7.), context=4)
        self.assertEqual(generated, [6, 6])
        self.assertEqual(reason, "context_limit")
        with self.assertRaises(ValueError):
            self.generate(lambda ids: torch.arange(7.), prompt=[1, 2, 3, 4], context=4)

    def test_nonfinite_logits_and_empty_inputs_fail(self):
        with self.assertRaises(FloatingPointError):
            self.generate(lambda ids: torch.tensor([float("nan"), 1.]))
        with self.assertRaises(ValueError):
            self.generate(lambda ids: torch.arange(7.), prompt=[])

    def test_all_models_share_default_500_and_requested_cap(self):
        defaults, _ = comparison.selected_specs(comparison.parser().parse_args([]))
        self.assertEqual([s["max_new_tokens"] for s in defaults], [500, 500, 500])
        args = comparison.parser().parse_args(["--max-new-tokens", "300"])
        specs, _ = comparison.selected_specs(args)
        self.assertEqual([(s["name"], s["max_new_tokens"]) for s in specs],
                         [("base", 300), ("s7", 300), ("sall", 300)])
        args = comparison.parser().parse_args(["--base-source", "qwen", "--max-new-tokens", "5"])
        specs, _ = comparison.selected_specs(args)
        self.assertEqual(specs[0]["asset_id"], "model_qwen3_0p6b_base")
        self.assertEqual(specs[0]["max_new_tokens"], 5)

    def test_sampling_keeps_threshold_token_and_stops_on_eos(self):
        kwargs = dict(eos_id=7, max_new_tokens=500, context_limit=600,
                      device="cpu", decode="sample", temperature=1., seed=9)
        # Tiny top-p retains the largest-probability token, never an empty set.
        generated, reason = comparison.greedy_generate(
            lambda ids: torch.arange(8.), [1], top_p=0.001, **kwargs)
        self.assertEqual((generated, reason), ([7], "eos"))
        kwargs.update(eos_id=99, max_new_tokens=20)
        callback = lambda ids: torch.arange(8.)
        first = comparison.greedy_generate(callback, [1], top_p=1., **kwargs)
        second = comparison.greedy_generate(callback, [1], top_p=1., **kwargs)
        self.assertEqual(first, second)
        self.assertEqual(first[1], "max_new_tokens")

    def test_interactive_reuses_workers_and_sends_identical_inputs(self):
        args = comparison.parser().parse_args([])
        specs, path = comparison.selected_specs(args)
        children = []

        def launch(*unused, **options):
            child = type("Child", (), {})()
            child.stdin = io.StringIO()
            child.stdout = io.StringIO()
            child.poll = lambda: None
            children.append(child)
            return child

        def receive(child):
            if not child.stdin.getvalue():
                return {"ready": {"name": specs[children.index(child)]["name"],
                                  "context_limit": 2048, "eos_token_id": 7,
                                  "loading_seconds": 0}}
            text = json.loads(child.stdin.getvalue().splitlines()[-1])["prompt"]
            return {"result": {"prompt": text, "prompt_token_ids": [len(text)],
                               "continuation": text, "generated_tokens": 1,
                               "stop_reason": "eos", "generation_seconds": 0}}

        tokenizer = type("Tokenizer", (), {"encode": lambda self, text, **kw:
                         type("Encoded", (), {"ids": [len(text)]})()})()
        reports = []
        with patch.object(comparison, "tokenizer_and_prompts", return_value=(tokenizer, [], 7, "EOS")), \
             patch.object(comparison.subprocess, "Popen", side_effect=launch), \
             patch.object(comparison, "receive", side_effect=receive), \
             patch.object(comparison, "close_workers") as close, \
             patch("builtins.input", side_effect=["hello", "second", "/quit"]), \
             patch("sys.stdout", new_callable=io.StringIO):
            comparison.interact(args, specs, path, reports)
        self.assertEqual(len(children), 3)
        sent = [child.stdin.getvalue() for child in children]
        self.assertEqual(sent, [sent[0]] * 3)
        self.assertEqual([r["prompt"] for r in reports[0]["results"]], ["hello", "second"])
        close.assert_called_once_with(children)

    def test_worker_cleanup_terminates_and_reaps_real_child(self):
        child = subprocess.Popen([sys.executable, "-c", "import sys; sys.stdin.read()"],
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        comparison.close_workers([child])
        self.assertIsNotNone(child.poll())
        self.assertTrue(child.stdin.closed and child.stdout.closed)

    def test_serving_worker_loads_once_and_stops_each_request_on_eos(self):
        args = comparison.parser().parse_args(["--worker", "s7", "--serve", "--device", "cpu"])
        specs, path = comparison.selected_specs(args)
        tokenizer = type("Tokenizer", (), {
            "encode": lambda self, text, **kw: type("Encoded", (), {"ids": [len(text)]})(),
            "decode": lambda self, ids, **kw: "EOS"})()
        model = type("Model", (), {
            "output_weight": torch.arange(8.).reshape(8, 1),
            "forward_intermediates": lambda self, ids: {"final_h": torch.ones(1, ids.shape[1], 1)}})()
        requests = '\n'.join(json.dumps(x) for x in [{"prompt": "one"}, {"prompt": "two"}, {"quit": True}])
        with patch.object(comparison, "tokenizer_and_prompts", return_value=(tokenizer, [], 7, "EOS")), \
             patch.object(comparison, "load_model", return_value=(model, 2048)) as load, \
             patch("sys.stdin", io.StringIO(requests)), patch("sys.stdout", new_callable=io.StringIO) as output:
            comparison.worker(args, specs, path, [])
        load.assert_called_once()
        replies = [json.loads(line) for line in output.getvalue().splitlines()]
        self.assertIn("ready", replies[0])
        self.assertEqual([reply["result"]["generated_token_ids"] for reply in replies[1:]], [[7], [7]])
        self.assertTrue(all(reply["result"]["stop_reason"] == "eos" for reply in replies[1:]))

    def test_all_three_native_sources_load_strictly_and_preserve_lm_path(self):
        args = comparison.parser().parse_args([])
        specs, _ = comparison.selected_specs(args)
        # Native packages share a name: use a fresh process for each version,
        # exactly as production does. Fixture modules are cleared only to test
        # reloading the SAME tiny fixture, never to switch production versions.
        child = r'''
import dataclasses, importlib.util, json, sys, tempfile
from pathlib import Path
import torch
spec = json.loads(sys.argv[2])
sys.path.insert(0, spec['source_root'])
from dense_sae.model import Qwen3SAEConfig, Qwen3SAEForCausalLM
options = dict(vocab_size=13, hidden_size=8, intermediate_size=16,
 num_hidden_layers=2, num_attention_heads=2, num_key_value_heads=1,
 head_dim=4, max_position_embeddings=16, sae_width=12, sae_k=2,
 sae_mode='none' if spec['name']=='base' else 'sidecar', bottleneck_alpha=0.,
 sae_auxk=0, sae_auxk_coef=0., sae_hook_layer=1, sae_hook_layers=(1,0))
fields = {f.name for f in dataclasses.fields(Qwen3SAEConfig)}
config = Qwen3SAEConfig.from_dict({k:v for k,v in options.items() if k in fields})
original = Qwen3SAEForCausalLM(config).eval()
ids = torch.tensor([[1,2,3]], dtype=torch.long)
with torch.inference_mode(): expected = original.forward_intermediates(ids)['final_h']
with tempfile.TemporaryDirectory() as directory:
 spec['checkpoint'] = directory
 spec['identity'] = {'layers':2,'hidden_size':8}
 payload = {'model': original.state_dict(), 'optimizer': {'fixture_only':torch.ones(3)},
            'extra_training_state': {'model_config':config.to_dict()}}
 torch.save(payload, Path(directory)/'state.pt')
 for name in list(sys.modules):
  if name=='dense_sae' or name.startswith('dense_sae.'): del sys.modules[name]
 module_spec = importlib.util.spec_from_file_location('comparison_fixture', sys.argv[1])
 app = importlib.util.module_from_spec(module_spec); module_spec.loader.exec_module(app)
 model, context = app.load_native(spec, torch.device('cpu'), torch.float32)
 assert context==16 and not any(p.requires_grad for p in model.parameters())
 def no_auxiliary(*args): raise AssertionError('generation executed a sidecar SAE')
 for layer in model.modules():
  if type(layer).__name__=='TopKSAE': layer.register_forward_pre_hook(no_auxiliary)
 with torch.inference_mode(): actual=model.forward_intermediates(ids)['final_h']
 torch.testing.assert_close(actual, expected, rtol=0, atol=0)
 # Missing weights may not be silently initialized.
 del payload['model'][next(iter(payload['model']))]
 torch.save(payload, Path(directory)/'state.pt')
 for name in list(sys.modules):
  if name=='dense_sae' or name.startswith('dense_sae.'): del sys.modules[name]
 try: app.load_native(spec, torch.device('cpu'), torch.float32)
 except RuntimeError: pass
 else: raise AssertionError('missing key was accepted')
print('tiny native fixture PASS:', spec['name'])
'''
        for spec in specs:
            with self.subTest(model=spec["name"]):
                result = subprocess.run([sys.executable, "-c", child, str(SCRIPT), json.dumps(spec)],
                                        capture_output=True, text=True, timeout=40)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()

"""Deterministic source-checker regressions, not a renderer test."""
from pathlib import Path
import importlib.util
import subprocess
import sys
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'check_markdown_math.py'
spec = importlib.util.spec_from_file_location('markdown_math', SCRIPT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class MathSourceTests(unittest.TestCase):
    def good(self, text, **kwargs):
        self.assertEqual(module.check_text(text, **kwargs), [])

    def bad(self, text, fragment):
        self.assertTrue(any(fragment in e for e in module.check_text(text)))

    def test_inline(self):
        self.good(r'The value is \(x^{2}+y\).')

    def test_display(self):
        self.good('Explanation.\n\n\\[\nx^{2}+y\n\\]\n\nBoundary.')

    def test_multiline_literal(self):
        self.good('```python\nx = r"\\[raw"\n```\n`\\alpha` and $HOME; $5 or $10.')

    def test_long_literal_fence(self):
        self.good('````text\n```\n\\(not math\n````')

    def test_comments_urls(self):
        self.good('<!-- \\(broken\n\\alpha -->\nhttps://example.org/$x$/\\alpha')

    def test_empty_inline(self):
        self.bad(r'\( \)', 'empty inline')

    def test_empty_display(self):
        self.bad('\\[\n\n\\]', 'empty display')

    def test_missing_close(self):
        self.bad(r'\(x', 'unbalanced')

    def test_unclosed_display(self):
        self.bad('\\[\nx', 'unclosed display')

    def test_nonstandalone_display(self):
        self.bad(r'Here \[x\] is inline.', 'non-standalone')

    def test_unbalanced_braces(self):
        self.bad(r'\(x^{2\)', 'unbalanced braces')

    def test_double_escape(self):
        self.bad(r'\\(x\\)', 'doubled')

    def test_nested(self):
        self.bad('\\[\n\\(x\\)\n\\]', 'nested')

    def test_raw_tex(self):
        self.bad(r'Uncontained \alpha', 'raw TeX')

    def test_blank_lines(self):
        self.bad('Text\n\\[\nx\n\\]\nText', 'blank line')

    def test_unclosed_fence(self):
        self.bad('```\ntext', 'unclosed literal')

    def test_dollar_copy(self):
        self.bad('$x+y$', 'not the canonical')
        self.good('$x+y$', allow_dollar=True)
        self.good('$$\nx+y\n$$', allow_dollar=True)

    def test_missing_cli_file(self):
        result = subprocess.run([sys.executable, str(SCRIPT), '/nonexistent/math.md'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('SOURCE FAIL', result.stdout)
        self.assertIn('NOT checked', result.stdout)


if __name__ == '__main__':
    unittest.main()

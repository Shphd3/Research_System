# Mathematics in Markdown

The default reading surface for this project is Codex chat and file preview.
On 2026-09-26 the researcher checked both surfaces and confirmed that the
following LaTeX delimiters render correctly there.

- Inline mathematics: `\(...\)`, for example `\(x^2+y^2=z^2\)`.
- Display mathematics: `\[...\]`, in a standalone block with blank lines
  before and after. Prefer separate delimiter lines for multiline equations.
- Use a single literal backslash in Markdown source. Do not turn the source
  into `\\(...\\)`; string literals in programs may need their own escaping.
- Explain essential symbols in ordinary prose. Keep equations out of code
  spans/fences unless explicitly showing literal source.
- Preserve code, shell variables, currency, URLs and quoted syntax examples.
  A dollar sign in those contexts is not a mathematical delimiter.
- Formatting changes must preserve formula bodies, values, scientific meaning,
  approval/state fields and evidence identity. Keep archived snapshots and
  append-only conversation logs intact. A source-file hash changes after a
  formatting edit; retain historical hashes as historical identities.

This convention applies to maintained Markdown, templates, applicable Skills,
and research replies. The from-attention-to-search project inherits this rule
through the root AGENTS. Do not maintain duplicate scientific sources just to
support another renderer.

MathJax supports these delimiters by default, but Markdown rendering depends on
the host. GitHub documents dollar-delimited math and fenced `math` blocks; do
not assume this Codex convention will render unchanged there. When a different
reading surface is requested, adapt its exported reading copy to the supported
syntax and check that surface. Formatting alone cannot add math support to a
renderer that lacks it.

Sources: [MathJax delimiters](https://docs.mathjax.org/en/latest/input/tex/delimiters.html),
[GitHub mathematical expressions](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions).

Rendered examples for the chosen reading surface:

The parameter gradient is \(G=e\,u^\top\), where \(u\) is the layer input and
\(e\) is the gradient with respect to its output.

\[
\langle e_1u_1^\top,e_2u_2^\top\rangle_F
=(e_1^\top e_2)(u_1^\top u_2).
\]

"""Navigation and portable-reading regressions; no scientific verdict is tested here."""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from research_paths import local_links, rebase_links, link_path, relocated
from build_reading_bundle import build, reading_copy, select_documents
from check_current_entrypoints import inspect, current_entrypoints


class PathTests(unittest.TestCase):
    def test_rebase_preserves_equations_code_external_and_fragment(self):
        root = Path('/workspace')
        text = r'''[claim](target.md#answer)
\(f[x](y)\) and \[h[z](w)\]
`[example](literal.md)`
~~~text
[example](fenced.md)
~~~
[worker](/worker/evidence.json)
[web](https://example.org)
'''
        result = rebase_links(text, root/'old/page.md', root/'new/deep/page.md', {'old/target.md':'new/target.md'}, root)
        self.assertEqual(result, text.replace('target.md#answer', '../target.md#answer'))

    def test_spaces_encoding_and_line_numbers(self):
        path, tail = link_path('<../a%20b.md:12#section>', Path('/workspace/new/a.md'), Path('/workspace'))
        self.assertEqual(path, Path('/workspace/a b.md'))
        self.assertEqual(tail, ':12#section')
        self.assertEqual(relocated(path, {'a b.md':'new/b.md'}, Path('/workspace')), Path('/workspace/new/b.md'))

    def test_math_is_not_a_dependency(self):
        text = r'\(\mathbb{E}[G](x)\) and `[literal](x)` plus [real](x.md)'
        self.assertEqual(len(list(local_links(text, Path('/work/a.md'), Path('/work')))), 1)

    def test_archiving_a_previously_relocated_record(self):
        root = Path('/workspace')
        mapping = {'old/meeting.md': 'daily/0930/meeting.md',
                   'daily/0930/meeting.md': 'daily/backup/09/0930/meeting.md'}
        self.assertEqual(relocated(root/'old/meeting.md', mapping, root),
                         root/'daily/backup/09/0930/meeting.md')

    def test_relocation_cycle_reports_an_error(self):
        with self.assertRaisesRegex(ValueError, 'Cyclic research relocation'):
            relocated(Path('/workspace/a.md'),
                      {'a.md': 'b.md', 'b.md': 'a.md'}, Path('/workspace'))

    def test_relative_worker_link_keeps_same_identity_after_move(self):
        root = Path('/workspace')
        result = rebase_links('[data](../../worker/result.csv)', root/'old/page.md', root/'new/deep/page.md', {}, root)
        self.assertEqual(result, '[data](/worker/result.csv)')

    def test_balanced_path_and_title_survive_rebase(self):
        root = Path('/workspace')
        text = '[A](<q/file (v1).md#section> "reader title") and [B](q/file(v1).md)'
        links = list(local_links(text, root/'old/page.md', root))
        self.assertEqual(links[0][1], root/'old/q/file (v1).md')
        self.assertEqual(links[1][1], root/'old/q/file(v1).md')
        self.assertEqual(rebase_links(text, root/'old/page.md', root/'new/page.md', {}, root),
                         '[A](<../old/q/file (v1).md#section> "reader title") and [B](<../old/q/file(v1).md>)')

    def test_entrypoint_helper_ignores_code_and_keeps_title_separate(self):
        self.assertEqual(current_entrypoints('`[fake](x.md)`\n[real](<a b.md> "title")'), ['a b.md'])


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.root = self.base/'system'
        self.project = self.root/'Projects/p'
        self.main = self.project/'main'
        self.main.mkdir(parents=True)
        (self.main/'roadmap.md').write_text('# Route\n[Current Focus](focus.md)\n[Unselected](history.md)\n')
        (self.main/'focus.md').write_text('# Focus\nproblem_key: q\n[Summary](q/summary.md)\n')
        (self.main/'history.md').write_text('old')
        (self.main/'q').mkdir()
        self.summary = self.main/'q/summary.md'
        self.summary.write_text('# Summary\nUnknown\n![figure](plot.svg)\n[worker](/worker/data.json)\n[missing](absent.json)\n')
        (self.main/'q/summary_cn.md').write_text('# 结果\nUnknown\n')
        (self.main/'q/plot.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
        self.output = self.base/'bundle'

    def tearDown(self):
        self.temp.cleanup()

    def test_scope_exact_copies_and_zip(self):
        manifest = build(self.root, 'p', self.output, [], True)
        paths = {row['path'] for row in manifest['files']}
        self.assertIn('Projects/p/main/q/summary_cn.md', paths)
        self.assertNotIn('Projects/p/main/history.md', paths)
        for row in manifest['files']:
            data = (self.output/row['copy']).read_bytes()
            self.assertEqual(data, (self.root/row['path']).read_bytes())
            self.assertEqual(hashlib.sha256(data).hexdigest(), row['sha256'])
        reasons = {r['reason'] for r in manifest['omitted_links']}
        self.assertIn('source unavailable', reasons)
        self.assertIn('outside allowed source workspace', reasons)
        self.assertIn('outside selected documents or asset/size limit', reasons)
        with zipfile.ZipFile(str(self.output)+'.zip') as archive:
            self.assertIn('bundle/README.md', archive.namelist())
        self.assertIn('Unknown', (self.output/'documents/Projects/p/main/q/summary.md').read_text())
        self.assertFalse(list(self.output.rglob('*.html')))

    def test_symlink_does_not_copy_outside_data(self):
        secret = self.base/'outside.json'; secret.write_text('NOT FOR BUNDLE')
        (self.main/'q/link.json').symlink_to(secret)
        self.summary.write_text('[link](link.json)')
        manifest = build(self.root, 'p', self.output, [], False)
        self.assertTrue(any(r['reason']=='outside allowed source workspace' for r in manifest['omitted_links']))
        self.assertFalse(any(row['path'].endswith('link.json') for row in manifest['files']))

    def test_no_overwrite_or_project_traversal(self):
        self.output.mkdir(); (self.output/'keep').write_text('existing')
        with self.assertRaises(ValueError): build(self.root, 'p', self.output, [])
        self.assertEqual((self.output/'keep').read_text(), 'existing')
        with self.assertRaises(ValueError): build(self.root, '../p', self.base/'out', [])

    def test_missing_project_and_source_are_clear(self):
        with self.assertRaisesRegex(ValueError, 'roadmap unavailable'):
            build(self.root, 'absent', self.output, [])
        with self.assertRaisesRegex(ValueError, 'Unavailable or unsupported'):
            build(self.root, 'p', self.output, ['missing.md'])
        self.assertFalse(self.output.exists())

    def test_reading_copy_preserves_prose_math_and_code(self):
        text = '# Explanation\nUnknown\n' + r'\(x^2\) and `\(y\)` and `[code](unchanged.md)`'
        self.assertEqual(reading_copy(text, lambda url: 'REPLACED'), text)
        text += '\n~~~text\n[fenced](also-unchanged.md)\n~~~\n[real](source.md)\n'
        self.assertEqual(reading_copy(text, lambda url: 'new.md'), text.replace('[real](source.md)', '[real](new.md)'))

    def test_remote_inline_image_becomes_source_link(self):
        text = '![remote](https://example.org/figure.png)'
        self.assertEqual(reading_copy(text, lambda url: url), '[remote](https://example.org/figure.png)')

    def test_incomplete_checkout_is_diagnostic(self):
        (self.root/'PROJECTS.md').write_text('[Missing project](Projects/absent/main/roadmap.md)')
        with patch('check_current_entrypoints.tracked_paths', return_value=set()):
            failures, _, _ = inspect(self.root, True)
        self.assertTrue(any('MISSING Projects/absent' in row for row in failures))
        self.assertTrue(any('NO_PROJECT_ROUTE' in row for row in failures))

    def test_explicit_source_does_not_expand_other_records(self):
        (self.main/'q/protocol.md').write_text('# Contract')
        (self.main/'q/anchor.md').write_text('# Design')
        self.summary.write_text('# Summary\n[contract](protocol.md)\n[design](anchor.md)')
        manifest = build(self.root, 'p', self.output, [str(self.summary)])
        paths = {row['path'] for row in manifest['files']}
        self.assertIn('Projects/p/main/q/summary_cn.md', paths)
        self.assertNotIn('Projects/p/main/q/protocol.md', paths)
        self.assertNotIn('Projects/p/main/q/anchor.md', paths)
        self.assertNotIn('Projects/p/main/focus.md', paths)
        self.assertTrue(any(row['target'].endswith('protocol.md') for row in manifest['omitted_links']))
        self.assertIn('指定来源', (self.output/'README.md').read_text())

    def test_cross_project_source_version_is_in_manifest(self):
        other = self.root/'Projects/other'
        other.mkdir()
        source = other/'report.md'
        source.write_text('# Historical report\nSource remains historical.')
        manifest = build(self.root, 'p', self.output, [str(source)])
        self.assertIn(str(other), {row['path'] for row in manifest['source_versions']})
        page = (self.output/'README.md').read_text()
        self.assertIn('Historical report', page)
        self.assertTrue((self.output/'documents/Projects/other/report.md').is_file())
        self.assertIn('指定来源', page)

    def test_metadata_owners_are_reported_when_missing_or_unselected(self):
        (self.main/'focus.md').write_text('# Focus\n~~~text\nanchor: Projects/p/main/missing_anchor.md\n~~~\n')
        manifest = build(self.root, 'p', self.output, [])
        self.assertTrue(any(row['kind'] == 'owner field' and row['reason'] == 'source unavailable'
                            for row in manifest['omitted_links']))
        self.assertIn('Projects/p/main/focus.md', (self.output/'README.md').read_text())

    def test_default_uses_explicit_protocols_not_problem_key_directory(self):
        (self.main/'r').mkdir()
        (self.main/'q/protocol.md').write_text('# Protocol')
        (self.main/'r/protocol.md').write_text('# Protocol R')
        (self.main/'r/summary.md').write_text('# Summary R')
        (self.main/'old').mkdir()
        (self.main/'old/summary.md').write_text('# Prior result')
        (self.main/'focus.md').write_text('# Focus\nproblem_key: A15.unrelated_identity\n'
            'protocol: ../../Projects/p/main/q/protocol.md; Projects/p/main/r/protocol.md\n'
            '[Prior](old/summary.md)\n[Current](q/summary.md)')
        paths = set(select_documents(self.root, self.project, []))
        self.assertIn(self.summary, paths)
        self.assertIn(self.main/'r/summary.md', paths)
        self.assertNotIn(self.main/'old/summary.md', paths)

    def test_default_without_protocol_uses_direct_result_links(self):
        (self.main/'focus.md').write_text('# Focus\nproblem_key: A15.unrelated_identity\n[Summary](q/summary.md)')
        self.assertIn(self.summary, select_documents(self.root, self.project, []))

    def test_portable_inline_reference_and_asset_links(self):
        (self.main/'focus.md').write_text('# Focus\n[Local](#answer)\n[Other](q/summary.md#answer)\n\n## Answer\nFocus answer\n')
        self.summary.write_text('# Summary\n## Answer\nEvidence\n\n[Reference image][plot]\n\n'
            '[Missing reference][missing]\n\n![SVG](plot.svg#part)\n\n'
            '[plot]: plot.svg#part "title"\n[missing]: absent-reference.json\n')
        manifest = build(self.root, 'p', self.output, [])
        doc = self.output/'documents/Projects/p/main/q/summary.md'
        text = doc.read_text()
        self.assertIn('plot.svg#part "title"', text)
        self.assertIn('[Reference image][plot]', text)
        self.assertIn('UNAVAILABLE.md', text)
        self.assertNotIn('absent-reference.json', text)
        self.assertTrue(any(row['target'].endswith('absent-reference.json') for row in manifest['omitted_links']))
        focus = self.output/'documents/Projects/p/main/focus.md'
        self.assertIn('[Local](#answer)', focus.read_text())
        self.assertIn('[Other](q/summary.md#answer)', focus.read_text())
        # Both inline and reference destinations resolve within the portable copy.
        from research_paths import link_matches, reference_matches
        from urllib.parse import unquote
        for path in self.output.rglob('*.md'):
            if path.is_relative_to(self.output/'sources'):
                continue  # Exact originals deliberately keep original destinations.
            for match in [*link_matches(path.read_text()), *reference_matches(path.read_text())]:
                target = match['target'].strip('<>')
                if target.startswith('#'):
                    continue
                self.assertTrue((path.parent/unquote(target.split('#')[0])).is_file(), (path, target))
        row = next(r for r in manifest['files'] if r['path'].endswith('/q/summary.md'))
        self.assertEqual(row['reading_sha256'], hashlib.sha256(doc.read_bytes()).hexdigest())

    def test_reference_definitions_in_code_and_math_are_not_rebased(self):
        text = '~~~md\n[inside]: untouched.md\n~~~\n[outside]: <a b.md> "title"\n'
        result = reading_copy(text, lambda url: 'new.md')
        self.assertEqual(result, text.replace('<a b.md>', 'new.md'))

    def test_existing_zip_with_dotted_output_name_is_untouched(self):
        output = self.base/'reading.v1'
        archive = self.base/'reading.v1.zip'
        archive.write_bytes(b'keep existing archive')
        with self.assertRaisesRegex(ValueError, 'Output already exists'):
            build(self.root, 'p', output, [], True)
        self.assertEqual(archive.read_bytes(), b'keep existing archive')
        self.assertFalse(output.exists())

    def test_source_bytes_are_shared_by_page_copy_and_hash(self):
        original = self.summary.read_bytes()
        real_read = Path.read_bytes
        reads = []
        def changing_source(path):
            data = real_read(path)
            if path == self.summary:
                reads.append(path)
                path.write_text('# Changed after read\nNEW SOURCE VERSION')
            return data
        with patch.object(Path, 'read_bytes', changing_source):
            manifest = build(self.root, 'p', self.output, [])
        row = next(row for row in manifest['files'] if row['path'].endswith('/q/summary.md'))
        self.assertEqual(len(reads), 1)
        self.assertEqual((self.output/row['copy']).read_bytes(), original)
        self.assertEqual(row['sha256'], hashlib.sha256(original).hexdigest())
        self.assertNotIn('NEW SOURCE VERSION', (self.output/row['reading_copy']).read_text())

    def test_bundle_works_without_site_packages(self):
        script = ('import sys; from pathlib import Path; '
                  'sys.path.insert(0, sys.argv[1]); from build_reading_bundle import build; '
                  'build(Path(sys.argv[2]), "p", Path(sys.argv[3]), [])')
        result = subprocess.run([sys.executable, '-S', '-c', script, str(Path(__file__).resolve().parents[1]),
                                 str(self.root), str(self.output)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.output/'README.md').is_file())
        self.assertFalse((self.output/'index.html').exists())
        self.assertIn('# Summary', (self.output/'documents/Projects/p/main/q/summary.md').read_text())

    def test_chinese_roadmap_and_git_failure_are_diagnostic(self):
        (self.root/'PROJECTS.md').write_text('[Route](Projects/p/main/roadmap.md)')
        (self.main/'roadmap_cn.md').write_text('[失效入口](missing-cn.md)')
        with patch('check_current_entrypoints.tracked_paths', return_value=set()):
            failures, _, _ = inspect(self.root, True)
        self.assertTrue(any('missing-cn.md' in row for row in failures))
        with patch('check_current_entrypoints.tracked_paths', side_effect=subprocess.CalledProcessError(128, 'git')):
            failures, _, _ = inspect(self.root, True)
        self.assertTrue(any('TRACKING_UNAVAILABLE' in row for row in failures))


if __name__ == '__main__':
    unittest.main()

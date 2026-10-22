"""Guard refresh ownership and stable checks using the real reading-bundle builder."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sync_anchor_reading import STATE, sync


class AnchorSyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.main = self.root / 'Projects/demo/main'
        self.main.mkdir(parents=True)
        (self.main / 'roadmap.md').write_text('# Project route\n')
        self.source = 'Projects/demo/main/17_04_anchor.md'
        self.body = '# Mapping\n\nDRAFT; judgment: Unknown.\n\n[Metadata](inventory.json)\n[Missing](unselected.md)\n'
        (self.root / self.source).write_text(self.body)
        (self.main / '17_04_anchor_cn.md').write_text('# 映射\n\n判断：Unknown。\n')
        (self.main / 'inventory.json').write_text('{"data_id":"tiny"}\n')
        self.config = self.root / 'sync/anchors/profiles.json'
        self.config.parent.mkdir(parents=True)
        self.sources = [self.source]
        self.write_profile()
        self.target = self.root / 'sync/anchors/demo/17_04'

    def write_profile(self):
        self.config.write_text(json.dumps({'schema_version': 1, 'entries': [
            {'project': 'demo', 'anchor_id': '17_04', 'sources': self.sources}]}))

    def run_sync(self, check=False):
        return sync(self.root, 'demo', '17_04', check)

    def test_real_bundle_and_check_ignore_timestamp_and_repository_head(self):
        with patch('build_reading_bundle.repo_version', return_value={'head': 'first'}):
            self.run_sync()
        self.assertEqual((self.target / 'sources' / self.source).read_text(), self.body)
        self.assertIn('DRAFT; judgment: Unknown.', (self.target / 'documents' / self.source).read_text())
        self.assertTrue((self.target / 'documents/Projects/demo/main/17_04_anchor_cn.md').is_file())
        self.assertTrue((self.target / 'sources/Projects/demo/main/inventory.json').is_file())
        self.assertIn('unselected.md', (self.target / 'UNAVAILABLE.md').read_text())
        before = (self.target / 'manifest.json').read_bytes()
        with patch('build_reading_bundle.repo_version', return_value={'head': 'unrelated-new-head'}):
            self.assertEqual(self.run_sync(check=True), self.target)
        self.assertEqual((self.target / 'manifest.json').read_bytes(), before)

    def test_source_and_selection_changes_are_stale_then_refresh(self):
        self.run_sync()
        original = self.body + '\nA new factual source line.\n'
        (self.root / self.source).write_text(original)
        with self.assertRaisesRegex(ValueError, 'stale'):
            self.run_sync(check=True)
        self.run_sync()
        self.run_sync(check=True)
        self.assertEqual((self.root / self.source).read_text(), original)
        # Even the same copied set has a different explicitly selected scope.
        self.sources.append('Projects/demo/main/17_04_anchor_cn.md')
        self.write_profile()
        with self.assertRaisesRegex(ValueError, 'stale'):
            self.run_sync(check=True)
        self.run_sync()
        self.run_sync(check=True)

    def test_manual_edit_or_deletion_refuses_check_and_refresh(self):
        self.run_sync()
        generated = self.target / 'documents' / self.source
        generated.write_text('Human edit; do not overwrite.\n')
        for check in (True, False):
            with self.subTest(check=check), self.assertRaisesRegex(ValueError, 'edited or removed'):
                self.run_sync(check)
        self.assertEqual(generated.read_text(), 'Human edit; do not overwrite.\n')
        generated.unlink()
        with self.assertRaisesRegex(ValueError, 'edited or removed'):
            self.run_sync()

    def test_unowned_or_different_owner_target_is_never_overwritten(self):
        self.target.mkdir(parents=True)
        note = self.target / 'personal.md'
        note.write_text('Keep this.')
        with self.assertRaisesRegex(ValueError, 'no sync ownership manifest'):
            self.run_sync()
        self.assertEqual(note.read_text(), 'Keep this.')
        (self.target / STATE).write_text(json.dumps({'schema_version': 1, 'owner': {'anchor_id': 'other'}}))
        with self.assertRaisesRegex(ValueError, 'different or unknown'):
            self.run_sync()

    def test_preserve_unrelated_file_but_reject_new_generated_conflict(self):
        self.run_sync()
        note = self.target / 'personal/notes.md'
        note.parent.mkdir()
        note.write_text('Keep my notes.')
        (self.root / self.source).write_text(self.body + '\nUpdated source.\n')
        self.run_sync()
        self.assertEqual(note.read_text(), 'Keep my notes.')
        self.run_sync(check=True)
        new_source = 'Projects/demo/main/extra.md'
        (self.root / new_source).write_text('# Newly selected\n')
        conflict = self.target / 'documents' / new_source
        conflict.write_text('An unrelated existing file.')
        self.sources.append(new_source)
        self.write_profile()
        with self.assertRaisesRegex(ValueError, 'overwrite an unrelated file'):
            self.run_sync()
        self.assertEqual(conflict.read_text(), 'An unrelated existing file.')
        self.assertEqual(note.read_text(), 'Keep my notes.')

    def test_reject_path_escape_payload_sources_and_symlink_targets(self):
        for project, anchor in (('../demo', '17_04'), ('demo', '../escaped')):
            with self.subTest(project=project, anchor=anchor), self.assertRaisesRegex(ValueError, 'Unsafe'):
                sync(self.root, project, anchor)
        for source in ('../outside.md', '/outside.md', 'Projects/demo/main/inventory.json',
                       'Projects/demo/main/raw_data/private.md'):
            self.sources = [source]
            self.write_profile()
            with self.subTest(source=source), self.assertRaises(ValueError):
                self.run_sync()
        self.sources = [self.source]
        self.write_profile()
        elsewhere = self.root / 'untouched'
        elsewhere.mkdir()
        self.target.parent.mkdir(parents=True)
        self.target.symlink_to(elsewhere, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'real directories'):
            self.run_sync()
        self.assertEqual(list(elsewhere.iterdir()), [])

    def test_linked_raw_payload_is_not_published(self):
        raw = self.main / 'raw_data'
        raw.mkdir()
        (raw / 'samples.csv').write_text('private,row\n')
        (self.root / self.source).write_text(self.body + '\n[Raw](raw_data/samples.csv)\n')
        with self.assertRaisesRegex(ValueError, 'Payload directories'):
            self.run_sync()
        self.assertFalse(self.target.exists())


if __name__ == '__main__':
    unittest.main()

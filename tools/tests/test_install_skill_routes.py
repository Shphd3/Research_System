"""Verify replacement preservation, link resolution and repeat installation."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from install_skill_routes import install


class SkillRouteTests(unittest.TestCase):
    def test_preserve_then_route_and_repeat(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            source, dest, backup = base/'repo/.agents/skills', base/'user/skills', base/'backup'
            skill = source/'example/SKILL.md'
            skill.parent.mkdir(parents=True)
            skill.write_text('---\nname: example\ndescription: Explain examples.\n---\nCanonical\n')
            old = dest/'example'; old.mkdir(parents=True)
            (old/'SKILL.md').write_text('old workflow')
            (old/'private.txt').write_text('preserve bytes')
            other = dest/'unrelated'; other.mkdir()
            (other/'SKILL.md').write_text('unrelated')
            install(source, dest, backup)
            self.assertEqual((old/'SKILL.md').read_text(), 'old workflow')
            self.assertFalse(backup.exists())
            install(source, dest, backup, True)
            self.assertEqual((backup/'example/private.txt').read_text(), 'preserve bytes')
            self.assertIn(skill.resolve().as_posix(), (old/'SKILL.md').read_text())
            self.assertFalse((old/'private.txt').exists())
            self.assertEqual((other/'SKILL.md').read_text(), 'unrelated')
            self.assertEqual(install(source, dest, backup, True), [('example', 'unchanged')])

    def test_refuse_unsafe_backup_before_writing(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            source = base/'canonical/example'; source.mkdir(parents=True)
            (source/'SKILL.md').write_text('---\nname: example\ndescription: Examples.\n---\n')
            with self.assertRaises(ValueError):
                install(source.parent, base/'user', base/'user/backup', True)
            self.assertFalse((base/'user').exists())


if __name__ == '__main__':
    unittest.main()

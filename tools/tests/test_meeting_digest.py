import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from meeting_digest import build  # noqa: E402

LOG = """# 1109_demo：示例

## 1109 10:00　第一步

- 假设：噪声主导
- 先验→模型→计算：梯度=信号+零均值噪声 → E[ΔL]二阶项 tr(HΣ)/n → 一步 SGD 扫 η、n
- 跑前预测：A → 做 H2；B → 停
- 结果：斜率 2.0
- 研究者决定：Unknown
- 链条位置：机制

今日认识更新：噪声项主导一步更新

## 1201 10:00　范围外

- 假设：不应出现
- 链条位置：纯理解
"""


class DigestTests(unittest.TestCase):
    def test_window_and_fields(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / '1109_demo').mkdir()
            (Path(d) / '1109_demo' / 'log.md').write_text(LOG, encoding='utf-8')
            text = build(Path(d), '1109', '1110')
            self.assertIn('待研究者确认', text)
            self.assertIn('噪声项主导一步更新', text)
            self.assertIn('斜率 2.0', text)
            self.assertIn('tr(HΣ)/n', text)
            self.assertNotIn('不应出现', text)
            self.assertIn('1 条记录', text)


if __name__ == '__main__':
    unittest.main()

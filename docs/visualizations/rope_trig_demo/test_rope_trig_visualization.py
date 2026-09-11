import math
import tempfile
import unittest
from pathlib import Path

import matplotlib.image as mpimg
import numpy as np

from rope_trig_visualization import generate_figures, rotate_2d, rope_frequencies


class RopeTrigVisualizationTests(unittest.TestCase):
    def test_rope_frequencies_use_standard_formula(self):
        frequencies = rope_frequencies(8)
        expected = np.array([10000.0 ** (-2 * i / 8) for i in range(4)])
        np.testing.assert_allclose(frequencies, expected)

    def test_rotate_2d_matches_hand_calculated_points(self):
        np.testing.assert_allclose(rotate_2d((1.0, 0.0), math.pi / 2), (0.0, 1.0), atol=1e-12)
        np.testing.assert_allclose(rotate_2d((1.0, 2.0), math.pi), (-1.0, -2.0), atol=1e-12)
        np.testing.assert_allclose(rotate_2d((3.0, 4.0), 0.0), (3.0, 4.0), atol=1e-12)

    def test_generate_figures_writes_nonempty_pngs(self):
        with tempfile.TemporaryDirectory() as directory:
            outputs = generate_figures(Path(directory))
            self.assertEqual({path.name for path in outputs}, {"trig_functions.png", "rope_positions.png"})
            for path in outputs:
                self.assertTrue(path.is_file())
                self.assertGreater(path.stat().st_size, 10_000)
                image = mpimg.imread(path)
                self.assertGreaterEqual(image.shape[1], 1600)
                self.assertGreaterEqual(image.shape[0], 1000)


if __name__ == "__main__":
    unittest.main()

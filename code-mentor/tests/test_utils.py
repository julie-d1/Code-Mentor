import unittest
from codementor.analysis.utils import estimate_code_complexity, normalize_text

class TestUtils(unittest.TestCase):
    def test_normalize_text(self):
        self.assertEqual(normalize_text("  hi  "), "hi")
        self.assertEqual(normalize_text(None), "")

    def test_estimate_complexity_counts_keywords_and_depth(self):
        code = """def f(x):
    if x:
        for i in range(3):
            pass
"""
        c = estimate_code_complexity(code)
        self.assertTrue(c >= 3)  # def + if + for (+ depth)

if __name__ == "__main__":
    unittest.main()

import unittest
from codementor.analysis.ast_metrics import compute_ast_metrics

class TestAstMetrics(unittest.TestCase):
    def test_metrics_basic(self):
        code = """class A:
    def m(self):
        for i in range(3):
            if i % 2 == 0:
                pass
"""
        m = compute_ast_metrics(code)
        self.assertEqual(m.classes, 1)
        self.assertEqual(m.functions, 1)
        self.assertEqual(m.loops, 1)
        self.assertEqual(m.ifs, 1)
        self.assertTrue(m.max_depth > 0)

if __name__ == "__main__":
    unittest.main()

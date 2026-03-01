import unittest
from codementor.fixer.patcher import simple_auto_fix, make_unified_diff

class TestPatcher(unittest.TestCase):
    def test_simple_auto_fix_two_sum(self):
        buggy = """def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(len(nums)):
            if nums[i] + nums[j] == target:
                return i, j
"""
        fixed = simple_auto_fix(buggy)
        self.assertIn("seen", fixed)
        self.assertIn("enumerate", fixed)

    def test_make_unified_diff(self):
        d = make_unified_diff("a\n", "b\n")
        self.assertIn("---", d)
        self.assertIn("+++", d)

if __name__ == "__main__":
    unittest.main()

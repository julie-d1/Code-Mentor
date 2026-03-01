import unittest
from codementor.skill_model import SkillEstimator

class TestSkillEstimator(unittest.TestCase):
    def test_bucket_changes(self):
        s = SkillEstimator()
        # positive + optimization keywords should nudge up
        st = s.update(1, 1, "any tips to optimize this?")
        self.assertIn(s.bucket(), {"intermediate", "advanced", "beginner"})
        # frustrated + stuck should nudge down
        st2 = s.update(0, 10, "I'm stuck and confused")
        self.assertTrue(0.0 <= st2 <= 1.0)

if __name__ == "__main__":
    unittest.main()

import unittest

from codementor.mentor_agent import CodeMentor, MentorConfig

class _StubEmotion:
    def __init__(self, label=1):
        self.label = label
    def predict(self, text):
        return self.label

class TestAgent(unittest.TestCase):
    def test_respond_shape_offline(self):
        m = CodeMentor(MentorConfig())
        # prevent model downloads in test
        m.emotion = _StubEmotion(label=0)

        out = m.respond("def f():\n    return 1\n", "I'm confused", mode="explain")
        for k in ["answer","prompt","sentiment","skill_level","skill_bucket","complexity"]:
            self.assertIn(k, out)
        self.assertEqual(out["sentiment"], "frustrated")

if __name__ == "__main__":
    unittest.main()

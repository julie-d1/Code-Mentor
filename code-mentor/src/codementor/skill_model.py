from dataclasses import dataclass
@dataclass
class SkillState:
    level: float = 0.5
    seen: int = 0
class SkillEstimator:
    def __init__(self):
        self.state = SkillState()
    def update(self, sentiment_label: int, complexity: int, user_msg: str):
        delta = 0.0
        if sentiment_label == 1: delta += 0.05
        else: delta -= 0.07
        lm = (user_msg or "").lower()
        if "optimiz" in lm or "tip" in lm: delta += 0.05
        if "stuck" in lm or "confus" in lm: delta -= 0.05
        if complexity >= 6: delta += 0.02
        self.state.level = float(min(1.0, max(0.0, self.state.level + delta)))
        self.state.seen += 1
        return self.state.level
    def bucket(self) -> str:
        x = self.state.level
        if x < 0.35: return "beginner"
        if x < 0.7:  return "intermediate"
        return "advanced"

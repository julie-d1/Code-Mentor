import re
from dataclasses import dataclass
from codementor.analysis.ast_metrics import compute_ast_metrics
from codementor.models.emotion import EmotionModel
from codementor.skill_model import SkillEstimator
from codementor.analysis.utils import estimate_code_complexity, normalize_text
from codementor.session_store import Memory
from codementor.fixer.patcher import simple_auto_fix


@dataclass
class MentorConfig:
    model="gpt-4o-mini"
    temperature=0.3

class CodeMentor:
    def __init__(self, config: MentorConfig):
        self.cfg = config
        self.emotion = None  # lazy init to avoid model downloads on import/tests

    # ===== Prompt Builder =====
    def build_prompt(self, code, msg, mode, skill, emotion):
        skill_text = {
            "beginner": "Explain using very simple language, no jargon.",
            "intermediate": "Explain with medium detail and examples.",
            "advanced": "Provide deep technical explanation and optimization notes."
        }[skill]

        emotion_text = {
            1: "User feels confident or neutral. Maintain an informative tone.",
            0: "User is confused or frustrated. Use a friendly, supportive tone."
        }[emotion]

        mode_instruction = {
            "explain": "EXPLAIN the code as if teaching a student. No fixes. Be clear and structured.",
            "hint": "Provide HINTS ONLY. Do NOT give the answer directly. Use questions + clues.",
            "fix": "Return ONLY FIXED CODE inside a python code block. Do not add explanations."
        }[mode]

        return f"""
    You are CodeMentor, an emotion-aware AI code mentor.

    USER EMOTION: {emotion_text}
    USER SKILL LEVEL INFERENCE: {skill_text}

    TASK MODE: {mode_instruction}

    USER MESSAGE:
    {msg}

    USER CODE:
    {code}""" 


    # ===== Core API =====
    def respond(self, code: str, msg: str, mode: str = "explain") -> dict:
        """Main entrypoint used by the UI.

        Returns a dict with:
          - answer: model response (may include code block for fix mode)
          - prompt: the prompt that would be sent to an LLM
          - sentiment: 'positive' or 'frustrated'
          - skill_level: float in [0, 1]
          - skill_bucket: beginner/intermediate/advanced
          - complexity: int heuristic complexity score
        """
        code = code or ""
        msg = normalize_text(msg)
        mode = (mode or "explain").lower().strip()
        if mode not in {"explain", "hint", "fix"}:
            mode = "explain"

        # 1) Infer emotion from the user message
        if self.emotion is None:
            self.emotion = EmotionModel()
        emotion_label = int(self.emotion.predict(msg))  # 1=positive/neutral, 0=frustrated
        sentiment = "positive" if emotion_label == 1 else "frustrated"

        # 2) Estimate code complexity (simple heuristic)
        complexity = int(estimate_code_complexity(code))

        # 3) Update skill estimate and bucket
        if not hasattr(self, "skill"):
            self.skill = SkillEstimator()
        skill_level = float(self.skill.update(emotion_label, complexity, msg))
        skill_bucket = self.skill.bucket()

        # 4) Build prompt (kept for transparency / debugging)
        prompt = self.build_prompt(code, msg, mode, skill_bucket, emotion_label)

        # 5) Generate an answer (rule-based fallback; replace with LLM call if desired)
        answer = self._rule_based_answer(code, msg, mode, skill_bucket, emotion_label)

        # 6) Store a tiny breadcrumb of the interaction
        if not hasattr(self, "memory"):
            self.memory = Memory()
        self.memory.add(code, sentiment, skill_bucket)

        return {
            "answer": answer,
            "prompt": prompt,
            "sentiment": sentiment,
            "skill_level": skill_level,
            "skill_bucket": skill_bucket,
            "complexity": complexity,
        }

    def _rule_based_answer(self, code: str, msg: str, mode: str, skill: str, emotion_label: int) -> str:
        """Offline fallback so the app runs without external API keys.

        If you want to use a real LLM, swap this with an API call and keep the same return shape.
        """
        supportive = (emotion_label == 0)

        if mode == "hint":
            tone = "You’ve got this. " if supportive else ""
            hints = [
                "What is the input and expected output for a simple test case?",
                "Try printing intermediate values (or using a debugger) to see where the logic diverges.",
                "Identify the core loop/branch and check edge cases (empty input, off-by-one, None).", 
            ]
            if "two_sum" in (code or ""):
                hints.insert(0, "For two_sum: consider using a hash map to avoid nested loops.")
            return tone + "\n".join(f"- {h}" for h in hints)

        if mode == "fix":
            fixed = simple_auto_fix(code)
            # Always return code inside a python code block for the UI extractor
            return f"```python\n{fixed.rstrip()}\n```\n"

        # explain
        tone = "No worries — here’s a clear breakdown:\n\n" if supportive else "Here’s a breakdown:\n\n"
        # keep the explanation lightweight and structured
        bullets = [
            "**Goal:** Describe what the code is trying to do.",
            "**How it works:** Walk through the main steps (functions, loops, conditionals).", 
            "**Complexity:** Note any nested loops or expensive operations.",
            "**Next improvement:** Suggest one concrete improvement or test to run.",
        ]
        if skill == "beginner":
            bullets[1] = "**How it works:** Explain each line/section in plain language."
        elif skill == "advanced":
            bullets.append("**Optimization:** Mention alternatives or performance tradeoffs.")
        return tone + "\n".join(f"- {b}" for b in bullets)
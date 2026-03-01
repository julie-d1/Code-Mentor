# CodeMentor — Adaptive Code Mentor (Emotion + Skill Aware)

A Gradio app that **explains**, **hints**, and **(optionally) fixes** code while adapting tone based on the user's message (emotion) and an inferred skill level.

This repo is organized as an installable Python package (src layout), so you can run:

```bash
python -m codementor.app
```

---

## What it does

- **Emotion-aware tone** (positive/neutral vs frustrated) using a Transformers classifier (`EmotionModel`)
- **Skill-adaptive prompting** (beginner/intermediate/advanced) using a lightweight `SkillEstimator`
- **Code diagnostics**
  - AST-based structural metrics (`compute_ast_metrics`)
  - Optional Ruff static analysis (`run_ruff`)
- **Fix mode**
  - Offline fallback patching for a small set of patterns (`simple_auto_fix`)
  - Displays unified diff for transparency

> Note: The app includes an **offline rule-based responder** so it runs without API keys.
> If you want real LLM responses, swap in your preferred provider inside `codementor/mentor_agent.py`.

---

## Architecture (high level)

```mermaid
flowchart LR
  UI[Gradio UI\n(codementor.app)] -->|code + message + mode| AGENT[CodeMentor\n(mentor_agent.respond)]
  AGENT --> EMO[EmotionModel\n(models/emotion.py)]
  AGENT --> SKILL[SkillEstimator\n(skill_model.py)]
  AGENT --> CMPX[Complexity\n(analysis/utils.py)]
  AGENT --> PROMPT[Prompt Builder\n(mentor_agent.build_prompt)]
  AGENT -->|answer| UI

  UI --> AST[AST Metrics\n(analysis/ast_metrics.py)]
  UI --> RUFF[Ruff Check\n(analysis/static_tools.py)]
  UI --> FIX[Auto Fix + Diff\n(fixer/patcher.py)]
```

---

## Project layout

```
code-mentor/
  src/codementor/
    app.py                 # Gradio UI entrypoint
    mentor_agent.py        # CodeMentor agent (emotion + skill + prompt)
    skill_model.py         # Simple skill estimator
    session_store.py       # Lightweight in-memory history
    analysis/
      ast_metrics.py
      static_tools.py
      utils.py
    models/
      emotion.py           # Emotion classifier (local fine-tuned OR HF fallback)
    fixer/
      patcher.py           # Simple auto-fix + unified diff
  scripts/
    quick_eval.py
    train_emotion_quick.py
  data/
    emotion.jsonl
    examples_code.md
  tests/
    ...
```

---

## Setup

### 1) Create a virtual environment + install

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

### 2) Run the app

```bash
python -m codementor.app
```

---

## (Optional) Train the emotion model locally

By default the app will try to load a local model from:

- `models/emotion-small/`

If it doesn't exist, it automatically falls back to a Hugging Face sentiment model.

To train the small local model:

```bash
python scripts/train_emotion_quick.py
```

This writes a fine-tuned model to `models/emotion-small/`.

---

## Quick evaluation script

```bash
python scripts/quick_eval.py
```

---

## Tests

Runs with the standard library `unittest` (no extra deps):

```bash
python -m unittest discover -s tests -v
```

---

## Swapping in a real LLM

`codementor/mentor_agent.py` contains `_rule_based_answer(...)` as an offline fallback.

To use a real model:
- replace `_rule_based_answer` with an API call (OpenAI, Anthropic, etc.)
- keep `respond(...)` return keys the same so the UI continues to work:
  - `answer`, `prompt`, `sentiment`, `skill_level`, `skill_bucket`, `complexity`

---

## License

Add a license of your choice (MIT is common for portfolio projects).

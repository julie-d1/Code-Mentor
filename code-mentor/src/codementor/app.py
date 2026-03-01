import re
import gradio as gr
from codementor.mentor_agent import CodeMentor, MentorConfig
from codementor.analysis.ast_metrics import compute_ast_metrics
from codementor.analysis.static_tools import run_ruff
from codementor.fixer.patcher import simple_auto_fix, make_unified_diff

CODE_RE = re.compile(r"```(?:\w+)?\n(.*?)```", re.DOTALL)

cfg = MentorConfig()
mentor = CodeMentor(cfg)

def extract_code_block(text: str):
    m = CODE_RE.search(text or "")
    return m.group(1) if m else None

def explain_tab(code, message):
    try:
        out = mentor.respond(code or "", message or "", mode="explain")
        astm = compute_ast_metrics(code or "")
        diag = (
            f"Sentiment: {out['sentiment']} | "
            f"Skill: {out['skill_bucket']} ({out['skill_level']:.2f}) | "
            f"Complexity: {out['complexity']} | "
            f"AST depth: {astm.max_depth}"
        )
        ruff = run_ruff(code or "")
        rsum = f"Ruff: {'available' if ruff['available'] else 'not installed'}, issues: {len(ruff['issues'])}"
        return out["answer"], diag + " | " + rsum, out["prompt"]
    except Exception as e:
        return f"⚠️ Error: {e}", "Diagnostics unavailable", ""

def hint_tab(code, message):
    try:
        out = mentor.respond(code or "", message or "", mode="hint")
        return (
            out["answer"],
            f"Sentiment: {out['sentiment']} | "
            f"Skill: {out['skill_bucket']} ({out['skill_level']:.2f})",
            out["prompt"],
        )
    except Exception as e:
        return f"⚠️ Error: {e}", "Diagnostics unavailable", ""

def fix_tab(code, message):
    try:
        out = mentor.respond(code or "", message or "", mode="fix")
        llm_code = extract_code_block(out["answer"]) or ""
        auto = simple_auto_fix(code or "")
        fixed = llm_code.strip() if llm_code.strip() else auto
        diff = make_unified_diff(code or "", fixed)
        return fixed, diff, out["answer"]
    except Exception as e:
        return "", f"⚠️ Error: {e}", ""

with gr.Blocks(title="CodeSensei Pro — Adaptive Code Mentor") as demo:
    gr.Markdown("# CodeSensei Pro — Adaptive Code Mentor")

    with gr.Accordion("Quick Examples", open=False):
        gr.Examples(
            examples=[
                [
                    "def factorial(n):\n    return 1 if n == 0 else n * factorial(n - 1)",
                    "I don’t understand how recursion works 😫",
                    "Explain",
                ],
                [
                    "def is_prime(n):\n    for i in range(2, n):\n        if n % i == 0:\n            return False\n    return True",
                    "Got it working! Any optimization tips?",
                    "Hint",
                ],
                [
                    "def two_sum(nums, target):\n    for i in range(len(nums)):\n        for j in range(len(nums)):\n            if nums[i] + nums[j] == target:\n                return i, j",
                    "It sometimes returns same index twice",
                    "Fix",
                ],
            ],
            inputs=[
                gr.Code(lines=6, language="python", label="Code"),
                gr.Textbox(label="Message"),
                gr.Dropdown(choices=["Explain", "Hint", "Fix"], value="Explain", label="Mode"),
            ],
            outputs=[],
            examples_per_page=3,
        )

    with gr.Tab("Explain"):
        code1 = gr.Code(label="Paste your code", language="python", lines=18)
        msg1 = gr.Textbox(label="Your message")
        btn1 = gr.Button("Explain")
        ans1 = gr.Markdown(label="Mentor Answer")
        diag1 = gr.Textbox(label="Diagnostics", interactive=False)
        prm1 = gr.Textbox(label="(Debug) Prompt", visible=False)
        btn1.click(explain_tab, [code1, msg1], [ans1, diag1, prm1])

    with gr.Tab("Hint"):
        code2 = gr.Code(label="Paste your code", language="python", lines=18)
        msg2 = gr.Textbox(label="Your message")
        btn2 = gr.Button("Get Hints")
        ans2 = gr.Markdown(label="Mentor Hints")
        diag2 = gr.Textbox(label="Diagnostics", interactive=False)
        prm2 = gr.Textbox(label="(Debug) Prompt", visible=False)
        btn2.click(hint_tab, [code2, msg2], [ans2, diag2, prm2])

    with gr.Tab("Fix"):
        code3 = gr.Code(label="Paste your buggy code", language="python", lines=18)
        msg3 = gr.Textbox(label="Describe the bug (optional)")
        btn3 = gr.Button("Fix Code")
        fixed = gr.Code(label="Fixed code", language="python", lines=18)
        diff = gr.Textbox(label="Unified diff", lines=18, show_copy_button=True)
        raw = gr.Markdown(label="Model Rationale")
        btn3.click(fix_tab, [code3, msg3], [fixed, diff, raw])

demo = demo
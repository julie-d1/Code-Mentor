import json, subprocess, tempfile, os, shutil
def run_ruff(code: str):
    if shutil.which("ruff") is None:
        return {"available": False, "issues": []}
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "tmp.py"); open(p,"w").write(code or "")
        out = subprocess.run(["ruff","check",p,"--output-format","json"], capture_output=True, text=True)
        try: issues = json.loads(out.stdout or "[]")
        except Exception: issues = []
        return {"available": True, "issues": issues}

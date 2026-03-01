import difflib
def simple_auto_fix(code: str) -> str:
    if "two_sum" in (code or "") and "for i in range" in code and "for j in range" in code:
        return """def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return seen[need], i
        seen[x] = i
    return None
"""
    return code or ""
def make_unified_diff(old: str, new: str, a="original.py", b="fixed.py") -> str:
    old_lines = (old or "").splitlines(keepends=True)
    new_lines = (new or "").splitlines(keepends=True)
    return "".join(difflib.unified_diff(old_lines, new_lines, fromfile=a, tofile=b, lineterm=""))

import re
def estimate_code_complexity(code: str) -> int:
    code = code or ""
    keywords = ["for", "while", "if", "elif", "else", "try", "except", "with", "def", "class"]
    cnt = sum(len(re.findall(r"\b"+kw+r"\b", code)) for kw in keywords)
    depths = [len(re.match(r"\s*", ln).group(0))//4 for ln in code.splitlines()]
    return cnt + (max(depths) if depths else 0)
def normalize_text(s: str) -> str:
    return (s or "").strip()

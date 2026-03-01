import time, hashlib
class Memory:
    def __init__(self): self.rows = []
    def add(self, code_text: str, sentiment: str, bucket: str):
        h = hashlib.sha1((code_text or "").encode()).hexdigest()[:8]
        self.rows.append((time.time(), h, sentiment, bucket))
    def last(self, n=5): return self.rows[-n:]

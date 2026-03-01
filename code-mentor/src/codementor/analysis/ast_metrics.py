import ast
from dataclasses import dataclass
@dataclass
class Metrics:
    functions: int
    classes: int
    ifs: int
    loops: int
    max_depth: int
class DepthVisitor(ast.NodeVisitor):
    def __init__(self):
        self.depth = 0; self.max_depth = 0
        self.functions = 0; self.classes = 0; self.ifs = 0; self.loops = 0
    def generic_visit(self, node):
        self.depth += 1; self.max_depth = max(self.max_depth, self.depth)
        super().generic_visit(node); self.depth -= 1
    def visit_FunctionDef(self, node): self.functions += 1; self.generic_visit(node)
    def visit_AsyncFunctionDef(self, node): self.functions += 1; self.generic_visit(node)
    def visit_ClassDef(self, node): self.classes += 1; self.generic_visit(node)
    def visit_If(self, node): self.ifs += 1; self.generic_visit(node)
    def visit_For(self, node): self.loops += 1; self.generic_visit(node)
    def visit_While(self, node): self.loops += 1; self.generic_visit(node)
def compute_ast_metrics(code: str) -> Metrics:
    try: tree = ast.parse(code or "")
    except SyntaxError: return Metrics(0,0,0,0,0)
    v = DepthVisitor(); v.visit(tree)
    return Metrics(v.functions, v.classes, v.ifs, v.loops, v.max_depth)

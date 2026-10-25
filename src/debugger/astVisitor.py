import ast

# Sources: https://deepsource.com/blog/python-asts-by-building-your-own-linter, https://docs.python.org/3/library/ast.html#ast.NodeVisitor.visit
class MyVisitor(ast.NodeVisitor):
    def __init__(self):
        self.target_array = ""
        self.shadow_idx = ""

    # Traverses for-loops
    def visit_For(self, node): # Visit a node. The default implementation calls the method called self.visit_classname where classname is the name of the node class

        if isinstance(node.target, ast.Tuple): # Only try to access .id if the target is an ast.Name node, if not skip it
            self.target_array = node.iter.args[0].id # Array being iterated on
            self.shadow_idx = node.target.elts[0].id # Iterator node object

        # Continue visiting child nodes
        # self.generic_visit(node)
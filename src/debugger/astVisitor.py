import ast

# Sources: https://deepsource.com/blog/python-asts-by-building-your-own-linter, https://docs.python.org/3/library/ast.html#ast.NodeVisitor.visit
class MyVisitor(ast.NodeVisitor):
    def __init__(self):
        self.iter_id = "" # Array being iterated on
        self.target_id = "" # Iterator node object

    # Traverses for-loops
    def visit_For(self, node): # Visit a node. The default implementation calls the method called self.visit_classname where classname is the name of the node class

        if isinstance(node.target, ast.Name): # Only try to access .id if the target is an ast.Name node, if not skip it
            self.iter_id = node.iter.id
            self.target_id = node.target.id

        # Continue visiting child nodes
        # self.generic_visit(node)
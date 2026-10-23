import ast

# Sources: https://deepsource.com/blog/python-asts-by-building-your-own-linter, https://docs.python.org/3/library/ast.html#ast.NodeVisitor.visit
class MyVisitor(ast.NodeVisitor):
    def __init__(self):
        self.iter_vars = []

    # Traverses all children
    def generic_visit(self, node):
        # print(f'Printing node class name: {node.__class__.__name__}')
        super().generic_visit(node)

    # Traverse only specific node objects
    def visit_For(self, node): # Visit a node. The default implementation calls the method called self.visit_classname where classname is the name of the node class

        if isinstance(node.target, ast.Name): # Only try to access .id if the target is an ast.Name node, if not skip it
            # print(node.target.id)
            self.iter_vars.append(node.target.id)

        # Continue visiting child nodes
        # self.generic_visit(node)
    
    def visit_While(self, node):
        # print(node)
        return

visitor = MyVisitor()

code = '''
lst = [1, 2, 3, 4, 5, 6]

def linear_search(lst, target):
    for e in lst:
        if e == target:
            return True
    return False

linear_search(lst, 6)
'''

tree = ast.parse(code) # Parse code with ast

print(ast.dump(tree, indent=2)) # Print all objects in the tree

visitor.visit(tree)

print(visitor.iter_vars)

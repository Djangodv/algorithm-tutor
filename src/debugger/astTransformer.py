import ast

class MyTransformer(ast.NodeTransformer):
    # Redundant?
    def __init__(self):
        return
    
    def visit_For(self, node):

        # Source: https://www.stanza.dev/courses/python-metaprogramming/ast/python-metaprogramming-ast-transformers#best-practices
        # Ensures child nodes are also transformed, usually done first so parent nodes can be influenced by child nodes
        self.generic_visit(node)

        # Checking instance makes sure only simple for-loops (e.g. for var in list) are rewritten
        if isinstance(node.target, ast.Name):

            target_override = ast.Tuple(
                elts=[
                    ast.Name(id=f'_shadow_idx_{node.lineno}', ctx=ast.Store()),
                    node.target],
                ctx=ast.Store())

            iter_override = ast.Call(
                func=ast.Name(id='enumerate', ctx=ast.Load()),
                args=[node.iter]
            )

            ast.copy_location(target_override, node.target)
            ast.copy_location(iter_override, node.iter)

            node.target = target_override
            node.iter = iter_override

        # Leave non matching for-loops unchanged
        return node
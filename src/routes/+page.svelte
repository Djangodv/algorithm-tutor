<script lang='ts'>

    import { loadPyodide } from 'pyodide';
	import { onMount } from 'svelte';
    import { type PyodideInterface } from 'pyodide';

    // Import seperate Python debugger components
    import ast_visitor_code from '../debugger/astVisitor.py?raw';
    import ast_transformer_code from '../debugger/astTransformer.py?raw';
    import tracer_code from '../debugger/tracer.py?raw';
    // console.log(tracer_code); // TEST

    let pyodide: PyodideInterface;

    // Source: https://svelte.dev/docs/svelte/lifecycle-hooks
    // The 'onMount' function schedules a callback to run as soon as the component has been mounted to the DOM.
    // The DOM is the browser's representation of an HTML page as a tree of objects/nodes.

    onMount(async () => {
        // Source: https://www.reddit.com/r/sveltejs/comments/ya24m6/python_pyodide_module_works_with_sveltekit/
        pyodide = await loadPyodide({
            indexURL: "https://cdn.jsdelivr.net/pyodide/v314.0.7/full/",
        });
        console.log(pyodide.runPython(`
            import sys
            sys.version
        `));
        // Source: https://pyodide.org/en/stable/usage/streams.html
        pyodide.setStdout({
            batched: (str: string) => {
                // console.log(str);
                output += str + "\n";
            }
        });
        await loadPythonComponents();
    })

    async function loadPythonComponents() {
        pyodide.FS.writeFile('/home/pyodide/astVisitor.py', ast_visitor_code);
        pyodide.FS.writeFile('/home/pyodide/astTransformer.py', ast_transformer_code);
        pyodide.FS.writeFile('/home/pyodide/tracer.py', tracer_code);
    }

    async function runPythonAnalysis(code: string) {

        const injectedCode: string = `
import ast
import sys

from astTransformer import MyTransformer
from astVisitor import MyVisitor
from tracer import DebugTracer

code = """${code}"""

tree = ast.parse(code)

transformer = MyTransformer()
modified_tree = ast.fix_missing_locations(transformer.visit(tree))

visitor = MyVisitor()
visitor.visit(modified_tree)

# Initialization of DebugTracer class can only be done when visitor.visit has been ran
tracer = DebugTracer(visitor.target_array, visitor.shadow_idx)

code_obj = compile(modified_tree, filename='<transformed>', mode='exec')

# Only run the tracer on the user code (nothing else)
sys.settrace(tracer.myTracer)

# Pass a sandbox environment to the exec() function with access to only the builtin methods (w. __builtins__), i.e. print(), len(), etc.
sandbox_env = {"__builtins__": __builtins__}
exec(code_obj, sandbox_env) 

sys.settrace(None)

for i in tracer.execution_history:
    print(i)
        `

        return await pyodide.runPythonAsync(injectedCode)

    }

    let input_code = $state('');
    let output = $state('');

    async function runCode() {
        // await pyodide.runPythonAsync(input_code);
        await runPythonAnalysis(input_code);
        console.log(output)
    };

</script>

<h1>Welcome to Algorithm Tutor</h1>
<p>Visit <a href="https://github.com/Djangodv/algorithm-tutor">github.com/Djangodv/algorithm-tutor</a> for more information about the project.</p>

<!-- Source: https://svelte.dev/tutorial/svelte/text-inputs -->
<!-- <input bind:value={input_code} placeholder="Input code..."> -->
<textarea bind:value={input_code} style="height: 100px; width: 500px" placeholder="Input code..."></textarea>
<button onclick={runCode}>Run</button>
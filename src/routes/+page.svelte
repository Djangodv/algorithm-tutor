<script lang='ts'>

    import { loadPyodide } from 'pyodide';
	import { onMount } from 'svelte';
    import { type PyodideInterface } from 'pyodide';

    // Import seperate Python debugger components
    import ast_visitor_code from '../debugger/astVisitor.py?raw';
    // console.log(ast_visitor_code); // TEST

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
    }

    async function runPythonAnalysis(code: string) {

        const injectedCode: string = `
import ast

from astVisitor import MyVisitor

visitor = MyVisitor()

code = """
${code}
"""

tree = ast.parse(code)

# print(ast.dump(tree, indent=2))

visitor.visit(tree)

print(visitor.target_array, visitor.index_variable)
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
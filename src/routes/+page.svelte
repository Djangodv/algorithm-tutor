<script lang='ts'>

    import { loadPyodide } from 'pyodide';
	import { onMount } from 'svelte';
    import { type PyodideInterface } from 'pyodide';

    let pyodide: PyodideInterface;

    // Source: https://svelte.dev/docs/svelte/lifecycle-hooks
    // The 'onMount' function schedules a callback to run as soon as the component has been mounted to the DOM.
    // The DOM is the browser's representation of an HTML page as a tree of objects/nodes.

    onMount(async () => {
        // Source: https://www.reddit.com/r/sveltejs/comments/ya24m6/python_pyodide_module_works_with_sveltekit/
        pyodide = await loadPyodide();
        console.log(pyodide.runPython(`
            import sys
            sys.version
        `));
        // Source: https://pyodide.org/en/stable/usage/streams.html
        pyodide.setStdout({
            batched: (str: string) => {
                output = str + "\n";
            }
        });
    })

    let input_code = $state('');
    let output = $state('');

    async function runCode() {
        await pyodide.runPythonAsync(input_code);
        console.log(output)
    };

</script>

<h1>Welcome to Algorithm Tutor</h1>
<p>Visit <a href="https://github.com/Djangodv/algorithm-tutor">github.com/Djangodv/algorithm-tutor</a> for more information about the project.</p>

<!-- Source: https://svelte.dev/tutorial/svelte/text-inputs -->
<input bind:value={input_code} placeholder="Input code...">
<button onclick={runCode}>Run</button>
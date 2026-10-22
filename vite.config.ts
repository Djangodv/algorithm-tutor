// import adapter from '@sveltejs/adapter-auto';
import adapter from '@sveltejs/adapter-static';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { viteStaticCopy } from "vite-plugin-static-copy";
import { dirname, join } from "path";
import { fileURLToPath } from "url";

const PYODIDE_EXCLUDE = [
  "!**/*.{md,html}",
  "!**/*.d.ts",
  "!**/*.whl",
  "!**/pyodide/node_modules",
];

export function viteStaticCopyPyodide() {
  const pyodideDir = dirname(fileURLToPath(import.meta.resolve("pyodide")));
  return viteStaticCopy({
    targets: [
      {
        src: [join(pyodideDir, "*").replace(/\\/g, "/")].concat(
          PYODIDE_EXCLUDE
        ),
        dest: "assets",
      },
    ],
  });
}

export default defineConfig({

	// Fix: "The dependency might be incompatible with the dep optimizer. Try adding it to `optimizeDeps.exclude`"
	optimizeDeps: {
		exclude: ['pyodide']
	},
	plugins: [
		// viteStaticCopyPyodide(),
		sveltekit({
			compilerOptions: {
				// Enable use of 'await' keyword inside top level of your component's <script>
				experimental: {
					async: true
				},

				// Force runes mode for the project, except for libraries. Can be removed in svelte 6.
				runes: ({ filename }) =>
					filename.split(/[/\\]/).includes('node_modules') ? undefined : true
			},

			// adapter-auto only supports some environments, see https://svelte.dev/docs/kit/adapter-auto for a list.
			// If your environment is not supported, or you settled on a specific environment, switch out the adapter.
			// See https://svelte.dev/docs/kit/adapters for more information about adapters.
			adapter: adapter({
				// default options are shown. On some platforms
				// these options are set automatically — see below
				pages: 'build',
				assets: 'build',
				fallback: undefined, // 'index.html'
				precompress: false,
				strict: true
			}),
			// Source: https://99helpers.com/hosting-guides/deploy/sveltekit/github-pages
			// A GitHub Pages project site lives in a subfolder, USERNAME.github.io/REPO, so the build has to know that folder's name.
			paths: {
				base: process.env.BASE_PATH || ""
			}
		})
	]
});

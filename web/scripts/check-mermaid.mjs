// Parse every Mermaid block in tracked Markdown with Mermaid's own parser, without a browser.
// Part of `make lint`, so a diagram that does not parse fails locally and in the agent sandbox;
// `make diagrams` still renders them with Chromium in CI (labels, <foreignObject> check).
// Uses the mermaid version that @mermaid-js/mermaid-cli pins, so it parses like the CI renderer.
import { execFileSync } from 'node:child_process'
import { readFileSync } from 'node:fs'
import { pathToFileURL } from 'node:url'

import DOMPurify from 'dompurify'

// Mermaid wires DOMPurify at import time; in Node there is no DOM, and parsing never sanitises.
DOMPurify.addHook ??= () => {}
DOMPurify.sanitize ??= (text) => text
const { default: mermaid } = await import('mermaid')
mermaid.initialize({ startOnLoad: false })

const BLOCK = /^```mermaid\n([\s\S]*?)^```/gm

/** Return one message per Mermaid block in `markdown` that does not parse. */
export async function checkMarkdown(markdown) {
  const errors = []
  let index = 0
  for (const match of markdown.matchAll(BLOCK)) {
    index += 1
    const line = markdown.slice(0, match.index).split('\n').length
    try {
      await mermaid.parse(match[1])
    } catch (error) {
      const first = String(error?.message ?? error).split('\n').slice(0, 3).join(' | ')
      errors.push(`block ${index} (line ${line}): ${first}`)
    }
  }
  return errors
}

async function main(root) {
  const files = execFileSync('git', ['grep', '-l', '```mermaid', '--', '*.md'], { cwd: root })
    .toString()
    .trim()
    .split('\n')
    .filter(Boolean)
  let failed = 0
  for (const file of files) {
    for (const error of await checkMarkdown(readFileSync(`${root}/${file}`, 'utf8'))) {
      failed += 1
      console.error(`${file}: ${error}`)
    }
  }
  console.log(`mermaid: ${files.length} files checked, ${failed} block(s) failed`)
  return failed ? 1 : 0
}

if (import.meta.url === pathToFileURL(process.argv[1] ?? '').href) {
  const root = execFileSync('git', ['rev-parse', '--show-toplevel']).toString().trim()
  process.exit(await main(root))
}

import { describe, expect, it } from 'vitest'

import { checkMarkdown } from './check-mermaid.mjs'

const fence = (body) => '```mermaid\n' + body + '\n```\n'

describe('checkMarkdown', () => {
  it('passes valid diagrams of several kinds', async () => {
    const md =
      fence('flowchart LR\n    T1 --> T2') +
      fence('sequenceDiagram\n    Lead->>CLI: compute, nothing recorded') +
      fence('erDiagram\n    A ||--o{ B : "holds"')
    expect(await checkMarkdown(md)).toEqual([])
  })

  it('reports a semicolon that ends a sequence message (the CI failure of 2026-11-24)', async () => {
    const md = 'text\n' + fence('sequenceDiagram\n    CLI-->>Lead: non-zero exit; nothing recorded')
    const errors = await checkMarkdown(md)
    expect(errors).toHaveLength(1)
    expect(errors[0]).toMatch(/^block 1 \(line 2\): Parse error/)
  })

  it('ignores Markdown without Mermaid blocks', async () => {
    expect(await checkMarkdown('# Title\n\n```python\nx = 1; y = 2\n```\n')).toEqual([])
  })
})

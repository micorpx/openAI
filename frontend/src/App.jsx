import React, { useState } from 'react'

const sample = `# Release v1.2.0 — 2025-10-27

## Highlights
- New analytics dashboard improves insights for managers.
- Memory leak fix reduces server restarts.

## New Features
- Analytics dashboard with export to CSV. (PR #410)

## Bug Fixes
- Fixed memory leak in cache service (#245)
- Fixed API auth timeout (#262)
`;

export default function App(){
  const [markdown, setMarkdown] = useState(sample);
  return (
    <div style={{padding:20,fontFamily:'Arial, sans-serif',maxWidth:900,margin:'auto'}}>
      <h1>Release Notes Preview</h1>
      <div style={{display:'flex',gap:20}}>
        <textarea value={markdown} onChange={(e)=>setMarkdown(e.target.value)} style={{flex:1,height:500}} />
        <div style={{flex:1,borderLeft:'1px solid #ddd',paddingLeft:20}}>
          <div dangerouslySetInnerHTML={{__html:markdown.replace(/\n/g,'<br/>')}} />
        </div>
      </div>
    </div>
  )
}

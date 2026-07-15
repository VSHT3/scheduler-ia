// CS IA: Computational Solution — documentation PDF (Criteria A–E)
// Word cap: 2000 words total, excluding code, code comments, and diagrams.
// Only FINISHED sections are included here; drafts live outside this project
// (see ../../REAL IA.md for the working outline).
//
// Build: typst compile main.typ

#import "@preview/wordometer:0.1.4": word-count, total-words

#set document(title: "Task Scheduler: a Computational Solution")
#set page(paper: "a4", margin: 2.5cm, numbering: "1")
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true)
#set heading(numbering: none)

#show heading.where(level: 1): it => {
  v(1em)
  text(size: 16pt, weight: "bold", it)
  v(0.5em)
}
#show heading.where(level: 2): it => {
  v(0.8em)
  text(size: 13pt, weight: "bold", it)
  v(0.3em)
}

// ---------------------------------------------------------------------------
// Cover page
// ---------------------------------------------------------------------------
#page(numbering: none)[
  #v(4cm)
  #align(center)[
    #text(size: 22pt, weight: "bold")[Task Scheduler]
    #v(0.5em)
    #text(size: 14pt)[A Computational Solution]
    #v(2em)
    #text(size: 12pt)[IB Computer Science HL --- Internal Assessment]
    #v(4em)
    // Everything inside word-count blocks below is counted; cover page is not.
    #text(size: 12pt)[Word count: *#context total-words*]
    #v(1em)
    #text(size: 10pt, fill: gray)[
      Excludes code, code comments, diagrams, tables, and this cover page.
    ]
  ]
]

// ---------------------------------------------------------------------------
// Criteria. Only finished sections are included; the rest are added as they
// are completed (B after the Gantt is rendered, C after design, D after the
// build, E after testing).
// ---------------------------------------------------------------------------
#[
  #show: word-count.with(exclude: (raw, table, figure))
  #include "criteria/a.typ"
]

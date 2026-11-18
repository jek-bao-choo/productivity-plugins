# sales-process

Sales process tools for Claude Code.

## Skills

### qualifying-lead

Turn raw sales notes into a structured lead qualification document using BANT, MEDDICC and 3 WHYs, with mermaid org charts, timeline diagrams and discovery questions.

**Usage:** `/sales-process:qualifying-lead`

### answering-rfp

Turn an RFP, RFI or vendor questionnaire into a structured response built with Claude Artifact Sheets (top preference; `.csv` or Excel `.xlsx` only when Artifact Sheets isn't available) with Datadog supportability assessments, web-search-grounded answers, documentation URLs and demo links. Anything a source does not confirm is marked Skipped, never guessed.

**Usage:** `/sales-process:answering-rfp`

## Moved skills

`creating-eval-plan`, `converting-evalplan-to-tmap` and `formulate-success-criteria` now live in the [`poc-process`](../poc-process) plugin (as of sales-process 0.2.0).

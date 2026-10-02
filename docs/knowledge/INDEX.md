# Knowledge cards — the retrievable layer

A lesson recorded only as a dated note is findable by the person who wrote it and by nobody
else. A **knowledge card** is the same lesson turned into a *question someone would actually
ask*, with the answer and the evidence underneath it. The `LESSON-PROMOTION` doctrine requires
every new dated lesson in `DEV_NOTES.md` to reach this layer or be explicitly declined.

One card per file. Name the file after the subject, put the question in the H1.

| Card | Answers |
| --- | --- |
| [`a-byte-ceiling-applies-to-authored-content.md`](a-byte-ceiling-applies-to-authored-content.md) | when does a byte ceiling apply to a generated file — and how is the exemption checked rather than declared? |
| [`a-dead-justification-camouflages-a-silent-path.md`](a-dead-justification-camouflages-a-silent-path.md) | a comment explains why a silent skip is safe — can I trust it? |
| [`the-chipdoc-request-channel.md`](the-chipdoc-request-channel.md) | how do I ask chipdoc to acquire a document — and how do I read the answer? |
| [`the-corpus-writes-shapes-my-grammar-cannot-state.md`](the-corpus-writes-shapes-my-grammar-cannot-state.md) | my schema validates the files it was designed from — why does it refuse the real corpus? |
| [`portable-shell-fixtures-keep-mutations-whole-line.md`](portable-shell-fixtures-keep-mutations-whole-line.md) | my self-test arm fails "for the wrong reason" — is the gate broken, or is my fixture's shape feeding the mutation through a different path? |
| [`director-named-actions-run-first.md`](director-named-actions-run-first.md) | the director named an action mid-startup — where does it go in the queue? |
| [`duplicate-document-ownership.md`](duplicate-document-ownership.md) | two tracked files are byte-identical — which one is canonical, and what proves it? |
| [`re-derivable-vs-cited-evidence.md`](re-derivable-vs-cited-evidence.md) | a document reports a check that passed elsewhere — may this project rely on it? |
| [`census-instrument-signature-gap.md`](census-instrument-signature-gap.md) | my census evidence was rejected by the acceptance gate — is my evidence weak, or the gate? |
| [`self-test-arms-that-never-ran.md`](self-test-arms-that-never-ran.md) | my gate's self-test says `N pass / 0 fail` — how do I know N is all the arms I wrote? |
| [`a-pdf-text-layer-is-not-the-page.md`](a-pdf-text-layer-is-not-the-page.md) | a PDF's text layer disagrees with its own page (or another extraction mode) — which do I trust? |
| [`reduced-width-verification-of-signed-ops.md`](reduced-width-verification-of-signed-ops.md) | my exhaustive reduced-width test fails on signed operations — is the primitive wrong? |
| [`availability-is-not-identity.md`](availability-is-not-identity.md) | the package manager has a formula with the right name — is it the right software? |
| [`a-shorter-trace-is-not-agreement.md`](a-shorter-trace-is-not-agreement.md) | my differential comparison says the two models agree — over how many steps? |
| [`zero-hits-absence-or-blindness.md`](zero-hits-absence-or-blindness.md) | my search returned zero hits — is that absence, or is my instrument blind? |
| [`device-unit-applicability-by-declaration.md`](device-unit-applicability-by-declaration.md) | my new unit isn't a processor — how do the gates know what applies to it? |
| [`a-duplicate-id-is-a-contradiction-not-a-shadowing.md`](a-duplicate-id-is-a-contradiction-not-a-shadowing.md) | my id-keyed map handles duplicate records fine — why did the gate stay green on a catalogue arguing with itself? |
| [`a-parse-without-error-is-not-a-faithful-read.md`](a-parse-without-error-is-not-a-faithful-read.md) | my reader parsed the file without error — can I trust the strings it handed back? |
| [`a-version-string-is-not-an-identity.md`](a-version-string-is-not-an-identity.md) | someone says my pinned source does not exist — is my pin wrong, or are we reading different publications? |
| [`a-survey-that-found-things-can-still-have-missed-things.md`](a-survey-that-found-things-can-still-have-missed-things.md) | my survey found plenty — how do I know it found everything? |
| [`all-green-but-the-product-has-not-moved.md`](all-green-but-the-product-has-not-moved.md) | every check is green and the infrastructure is beautiful — why hasn't the product moved? |
| [`pin-the-mechanism-slope-before-the-number.md`](pin-the-mechanism-slope-before-the-number.md) | my measurement says "1.4 allocations per step" — is that signoff-grade? |
| [`an-inherited-label-is-a-claim-to-re-derive.md`](an-inherited-label-is-a-claim-to-re-derive.md) | a design brief names a device — can I trust the label, or must I measure it? |
| [`the-chipdoc-channel.md`](the-chipdoc-channel.md) | how does semulith ask chipdoc for a document, and know it was heard? (`materials/requests.sexp` with `(status open)` — preferred; catalog gaps the fallback; exactly-once ids; the 2026-09-30 incident's lesson) |

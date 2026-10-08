# Toolbox — governance

Repository discipline — the doctrine enforcer, mirrors, routing, history, push, provenance.
Part of the partitioned toolbox: the doctrine and the bounded index are `TOOLBOX.md`; every
diagnostic is tracked so a number it produced can be re-derived (`LIVE-CONTAINMENT.3`).

| Tool | Answers | How to invoke |
| --- | --- | --- |
| `scripts/check_doctrines.sh` | which doctrine is breached, and where? (the whole registry, one verdict per rule) | `make gate` |
| `scripts/check_delivery_provenance.sh` | has a delivered file drifted from the bytes we were given, and is every manifest row's treatment declared? | `scripts/check_delivery_provenance.sh` |
| `scripts/check_fixture_fingerprints.sh` | does every pinned `sha256` still describe the file it names? | `scripts/check_fixture_fingerprints.sh` |
| `scripts/check_readme_routes.sh` | is every destination the landing page routes to governed, and is any live surface near its ceiling? | `scripts/check_readme_routes.sh` |
| `scripts/check_frontier_sync.sh` | does the task-tree index still name the leaf the tree itself calls next? | `scripts/check_frontier_sync.sh` |
| `scripts/check_registry_mirror.sh` | do the doctrine documents still list exactly the doctrines that are registered? | `scripts/check_registry_mirror.sh` |
| `scripts/check_tree_claims.sh` | does a live document state a leaf count, an active tree or a frontier leaf the trees contradict? | `scripts/check_tree_claims.sh` |
| `scripts/check_derived_counts.sh --list` | which counts in the live docs are re-derived, by what command, and what do they currently come to? | `scripts/check_derived_counts.sh [--list]` |
| `scripts/check_fact_ownership.sh` | does the fact-ownership registry hold — one owner per kind, every mirror governed, every restatement registered? | `scripts/check_fact_ownership.sh [--self-test]` (FACT-OWNERSHIP doctrine; registry: `doctrine/fact_ownership.tsv`) |
| `scripts/check_push_cadence.sh` | may this push happen now, or is it exceptional and awaiting the director? | `scripts/check_push_cadence.sh [--status \| --gate \| --self-test]` |
| `scripts/pre_push.sh` | the push boundary's full behavior: cadence first, then the named suite, then the green record | `scripts/pre_push.sh [--self-test]` (the pre-push hook execs it; the cadence number stays in check_push_cadence.sh alone) |
| `scripts/approved_push.sh` | the ACT of an exceptional push — suite green, then the ledger entry committed, then the push | `scripts/approved_push.sh '<the director's reason>' [push args]` (`--self-test` drives the whole act against a local bare upstream) |
| `scripts/check_push_record.sh` | is the approval ledger append-only, and is every entry well-formed? | `scripts/check_push_record.sh [--self-test]` (PUSH-RECORD; fired RED against the real corpus before registration, `PUSH-DISCIPLINE.3`) |
| `make ci` | the NAMED full local suite — what does the push boundary verify before bytes leave? | `make ci` (check + gate + bench + smoke-bench + book; the membership is named in the Makefile comment) |
| `scripts/shard_history.py` | is an append-history head nearing its ceiling, and which oldest entries would move into the next frozen shard? | `scripts/shard_history.py [--max-bytes N] [--dry-run] [--self-test]` |
| `scripts/history_archive.py` | can a former history shard be retrieved byte-exact from the tracked terminal without Git history? | `python3 scripts/history_archive.py`; `--read docs/changelog/shard-0001.md` emits authenticated original bytes; descriptors, objects, source manifest and every member checked; `probe_history_archive.py` runs the positive and sixteen negative controls under SHARD-FREEZE |
| `scripts/check_changelog_shards.sh` | is the sharded changelog history still frozen, append-only, and exactly partitioned — every live/archived shard authenticated, predecessor rows unchanged, no entry duplicated? | `scripts/check_changelog_shards.sh [--self-test]` |
| `scripts/gen_model_book.py` | what do the pinned dossiers lower to as the model books' materials tables — and is a document the generator cannot read refused by name rather than guessed? | `python3 scripts/gen_model_book.py [--check]` |
| `scripts/check_materials_bill.sh` | does every unit's materials bill still equal the pinned dossier, and does every material state what it does NOT supply? | `scripts/check_materials_bill.sh [--self-test]` (MATERIALS-BILL; fired RED against the real corpus before registration, `MODEL-BOOKS.1`) |
| `scripts/check_unit_books.sh` | does every registered unit have its own mdBook, and does every book build? | `scripts/check_unit_books.sh [--self-test]` (UNIT-BOOKS; fired RED against the real corpus before registration, `MODEL-BOOKS.6`) |
| `scripts/gen_book_index.py` | what does the project book's own text lower to as its index — and is a book shape the generator cannot emit (a missing chapter, an undeclared chapter set) refused by name rather than guessed? | `python3 scripts/gen_book_index.py [--check]` |
| `scripts/check_book_index.sh` | is the book's index still the byte-exact function of the book's text? | `scripts/check_book_index.sh [--self-test]` (BOOK-INDEX doctrine; fired RED against the real book before registration, `BOOK-APPARATUS.1`) |
| `scripts/upstream_exposure.py` | how long has each open upstream issue been reported, and which of our leaves does it block? | `python3 scripts/upstream_exposure.py [--open-count] [--self-test]` (derived from the dated records, never typed; the open count is re-derived by DERIVED-COUNTS, `UPSTREAM-TRACK.3`) |
| `scripts/check_seam_integrity.sh` | have this repo's repairs to the neutral checks quietly stopped working? | `scripts/check_seam_integrity.sh` |
| `scripts/check_task_acceptance.sh --print-sig` | what does the acceptance gate actually accept as evidence right now? | `scripts/check_task_acceptance.sh --print-sig \| --print-code-re` |
| any project check's `--self-test` | does this gate still discriminate — do its RED arms fail for the right reason? | `scripts/check_<name>.sh --self-test` |
| `git log -S'<token>'` | when did this string enter or leave the tree, and in which work unit? | `git log -S'<token>' --oneline` |

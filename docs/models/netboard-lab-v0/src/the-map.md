# The generated map

The map below is **generated, never handwritten** — the leaf's acceptance is that no
handwritten duplicate map exists anywhere. `scripts/gen_board.py` derives it from the
canonical board definition (`board.sexp`), and the BOARD-GEN doctrine re-derives it on
every commit and refuses drift, naming the artifact. What you see here is the same file
the dossier links to (`profiles/netboard-lab-v0/map.md`), included — one owner, two
readers. Its machine-readable half is `hardware.sexp` (schema `schema/hardware.sexp`),
carrying the same content resolved: computed region ends, the wiring, the absences.

{{#include ../../../../profiles/netboard-lab-v0/map.md}}

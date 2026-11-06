;; sources.sexp — the pinned specification source for `sifive-uart-lab-v0` (P5-BOARD.2,
;; 2026-10-02). One document form; validate with
;;   python3 scripts/check_sexp_schema.py profiles/sifive-uart-lab-v0/sources.sexp schema/sources.sexp

(comment "profiles/sifive-uart-lab-v0/sources.sexp — the pinned specification source for the SiFive"
         "UART device dossier. One source, one chapter: the UART is documented in §13 of the"
         "FU540-C000 manual, and this dossier cites nothing else from the manual — the SoC's"
         "memory map, other peripherals and boot flow are the board's and other devices'"
         "business, not this unit's."
         ""
         "⛔ THE ACQUISITION ROUTE IS THE MATERIALS CORPUS, NOT HTTP. The artifact was adopted"
         "into materials/catalog.sexp through the chipdoc channel (corpus-path"
         "sifive/fu540/current/FU540-C000_v1p5_manual.pdf) and is fetched into the untracked,"
         "repo-volume cache .materials/ by scripts/materials.py. `base_url` below records the"
         "corpus locator — the identity we actually acquired against — and `http_status` is 0"
         "by declaration: 0 means 'no HTTP fetch was performed by this project', never a server"
         "response. The pin was re-verified from the cache on `retrieved`: sha256"
         "5fa68a677ca4bc9fc81456840834eb4fa72874a2bd72a76c33f6709f3ecab79c, 2,361,460 bytes"
         "(scripts/materials.py --verify). A fresh-fetch route from the publisher (the"
         "dsp56300-lab-v0 dual-route pattern) is not established: v1p5's publisher URL is not"
         "recorded in the channel's answer, and guessing a CDN locator is not an acquisition."
         ""
         "⛔ NAME THE ISSUE, NOT JUST THE PART. The same manual circulates as v1p0 (retained at"
         "sifive/fu540/legacy/ in the corpus, and mirrored on third-party sites) and as v1p3/"
         "v1p4 on SiFive's CDN. This pin is v1p5, the current issue; every locator in this"
         "dossier was read against it (a 2026-10-02 pdftotext census of this artifact found"
         "zero occurrences of '16550' — P5-BOARD.1's measured correction, D-BOARD-UART-KIND)."
         ""
         "Terms: unrecorded in the materials catalog (`licence-evidence` there says why). The"
         "artifact is READ, not redistributed — the cache is untracked and no copy is"
         "committed. SRC-01 requires the actual terms before the artifact is relied on for"
         "anything shipped; that obligation stands.")

(sources (publication "SiFive FU540-C000 Manual — SiFive, Inc. (chipdoc materials corpus)")
  (not_this_publication "third-party mirrors and the legacy v1p0/v1p3/v1p4 issues — the pin is v1p5 via the corpus")
  (revision "v1p5")
  (base_url "chipdoc corpus: sifive/fu540/current/FU540-C000_v1p5_manual.pdf")
  (retrieved "2026-10-02")
  (work_dir ".materials/sifive")
  (comment "repo-volume, untracked; scripts/materials.py owns the cache")
  (source (id "SIFIVE-FU540-C000") (file "fu540-c000-v1p5.pdf")
    (title "SiFive FU540-C000 Manual v1p5") (chapter_version "v1p5")
    (sha256 "5fa68a677ca4bc9fc81456840834eb4fa72874a2bd72a76c33f6709f3ecab79c")
    (bytes 2361460) (http_status 0)
    (supplies "the SiFive UART contract — §13 only: the instance parameters (Table 58), the register map and the aligned-32-bit access rule (§13.3, Table 59), the per-register semantics of txdata/rxdata/txctrl/rxctrl/ie/ip/div (§13.4–§13.9, Tables 60–66), the FIFO depths and the watermark conditions. It does NOT supply: Reserved-bit behaviour, the effect of accesses outside Table 59's offsets, the effect of accesses that are not naturally aligned 32-bit, or the reset values the tables mark X.")))

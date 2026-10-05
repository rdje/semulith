# CHANGELOG shard — SEMULITH-P5-0017 … SEMULITH-P5-0017

> Sharded from `CHANGELOG.md` when it crossed its 64 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## SEMULITH-P5-0017 (leaf P5-BOARD.4) — the composition verdict: ACCEPTED, decided on every commit by BOARD-VERDICT; four dispositions as data; the 16-bit declaration measured false and narrowed

- The gate's core obligation landed: for every CPU environment assumption, the named
  board or device guarantee that satisfies it — or a rejection. The verdict is
  **ACCEPTED** and re-decided on every commit by the 33rd project doctrine,
  **BOARD-VERDICT** (`scripts/board_verdict.py` + `scripts/check_board_verdict.sh`):
  the discharge over the composed catalogues (8/8), every `satisfies` edge resolved to
  a discharged assumption (3/3), and every board-deferred device obligation bound to
  exactly one decision `answers` edge (4/4) — an unmatched assumption or a dangling
  edge is a REJECTION by name, never a note.
- The machinery: four deferred obligations (`OB-NIC-STRAP-RESETS` joined the three
  `.10` pre-wired records) carry the marker param `composition_disposition "required"`;
  `schema/board.sexp`'s `decision` gained the optional `answers` edge; the
  dispositions mirror into `hardware.sexp` (schema + `gen_board.py`) for the model
  route. The dispositions, decided: D32 tied high + SPEED_SEL at its pull-up
  (`D-BOARD-NIC-STRAPS`); the NIC's guest-readable time sources frozen
  (`D-BOARD-NIC-TIME-FROZEN`); the replay link scene static-complete at 100BASE-TX FD
  from before the guest's first access (`D-BOARD-NIC-LINK-SCENE`, BSR `0x782D`); pin
  reads tied off at 0 (`D-BOARD-NIC-PIN-TIEOFFS`).
- Measured in execution, fixed at root: the board's eth0 declared 16-bit accesses from
  the datasheet's summary sentence (§1.10), but §3.6 makes the bus widths
  mode-exclusive — with D32 strapped the declaration narrowed to 32; the NIC dossier's
  pairing-latch census entry flipped to absent with the new reason. The expectations
  re-pinned what the verdict determines (`hw_cfg` `0x00050004`, `free_run` `0` frozen,
  `phy_basic_status` `0x782D`).
- The authored verdict: `profiles/netboard-lab-v0/COMPOSITION-VERDICT.md` — the
  per-assumption table (every §5 aspect enumerated; the not-arising ones recorded with
  reasons), the `OB-PLATFORM` note (the discharge edges alone would be materially
  misleading), the interface-test leg (`make check` + smoke green — the RAM half; the
  MMIO halves attach with the device models, named), and MODEL-COMPOSE's open question
  answered for this board shape: no operator beyond union + discharge is needed.
  Included as the board book's verdict chapter.
- Validation: BOARD-VERDICT self-test 6/6 (every RED asserting its reason on copies of
  the real board) + real run green; `make gate` → all doctrines green (DERIVED-COUNTS
  re-derived 32 → 33 doctrines, 359 → 365 arms); `make check` + `run_smoke` green;
  `mdbook build` rc 0; `gen_book_index.py --check` rc 0. No Rust surface touched.


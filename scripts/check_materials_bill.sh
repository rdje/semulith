#!/usr/bin/env bash
# scripts/check_materials_bill.sh — MATERIALS-BILL (project doctrine).
#
# MODEL-BOOKS.1's acceptance, mechanized: every modelled unit's book carries a materials bill
# whose identity tables are GENERATED from the pinned dossier (a digest cannot rot — drift is
# refused, never patched) and whose prose states, for EVERY material, what it does NOT supply
# (a bill that lists only what things provide is how a project comes to believe it has
# information it never acquired).
#
# Two halves per registered unit (materials/units.sexp — the one registration place):
#
#   DRIFT        `scripts/gen_model_book.py --check` regenerates the four fragments
#                (pinned specifications, encoding tables, reference models, internal
#                contracts) in memory and byte-compares them against the committed ones —
#                a hand-edited table is how the bill quietly stops describing the dossier.
#   COMPLETENESS every material the pinned data enumerates — each specification artifact,
#                the encoding source, every reference candidate — and each internal
#                contract has its own `###` section in `src/materials.md`, and each section
#                carries its "does not supply" statement. A material without a section is
#                an omission; a section without the negative statement is the lie of
#                omission this leaf exists to prevent. `P5-BOARD.11` (2026-10-02): the
#                enumeration is keyed on the unit's DECLARED shape
#                (`gen_model_book.unit_shape`) — a device pins no references.sexp (no
#                encoding source, no candidates, by declaration) and a board's materials
#                are its composition pins in board.sexp; an undeclared absence stays
#                CANNOT JUDGE.
#
# CONTRACT: exit code is the verdict; explains on stderr; deterministic; read-only; no network.
#   --self-test   run the RED/GREEN controls against synthetic fixtures and exit.
set -uo pipefail
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT"

command -v python3 >/dev/null 2>&1 || {
  echo "MATERIALS-BILL: REFUSED — python3 is not on PATH; this check cannot judge." >&2; exit 2; }

check_bills() { # $1 = root (the corpus root; units registry + profiles + books under it)
python3 - "$1" <<'PY'
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, "scripts")
import sexp as S
import dossier_sexp as D
import gen_model_book as G

units_path = root / "materials" / "units.sexp"
if not units_path.is_file():
    print("MATERIALS-BILL: REFUSED — materials/units.sexp is absent; the unit registry "
          "this check enumerates is gone")
    print("__CHECKED__ 0"); sys.exit(2)
units = S.read_file(units_path)
unit_forms = [u for u in units if isinstance(u, list) and u and str(u[0]) == "unit"]
if not unit_forms:
    print("MATERIALS-BILL: REFUSED — the unit registry is empty; a census over no units "
          "is a claim about nothing")
    print("__CHECKED__ 0"); sys.exit(2)

findings, checked = [], 0
for u in unit_forms:
    uid = str(S.field(u, "id", "units.sexp"))
    book_rel = str(S.field(u, "book", "units.sexp")).rstrip("/")
    profile_dir = root / "profiles" / uid
    book_dir = root / book_rel
    bill = book_dir / "src" / "materials.md"
    checked += 1
    before = len(findings)

    # ---- structure: the book exists and carries the bill -----------------------------
    if not (book_dir / "book.toml").is_file() or not (book_dir / "src" / "SUMMARY.md").is_file():
        findings.append(f"NO BOOK {uid}: {book_rel} lacks book.toml/src/SUMMARY.md — a "
                        f"unit whose materials are unreviewable is a unit unreviewed")
        continue
    if not bill.is_file():
        findings.append(f"NO BILL {uid}: {book_rel}/src/materials.md is absent — the "
                        f"materials bill is the deliverable, not an option")
        continue

    # ---- DRIFT: the fragments still equal the pinned data ------------------------------
    r = subprocess.run([sys.executable, "scripts/gen_model_book.py", "--check",
                        "--profile-dir", str(profile_dir), "--book-dir", str(book_dir)],
                       capture_output=True, text=True)
    if r.returncode == 2:
        findings.append(f"CANNOT JUDGE {uid}: {r.stderr.strip()}")
        continue
    if r.returncode != 0:
        findings.append(f"DRIFT {uid}: {r.stderr.strip()} — regenerate with "
                        f"`python3 scripts/gen_model_book.py`; never edit the fragments")

    # ---- COMPLETENESS: every material has its section AND its negative statement -------
    # P5-BOARD.11: the enumeration is keyed on the unit's DECLARED shape
    # (gen_model_book.unit_shape) — a device dossier has no references.sexp (no encoding
    # source, no reference candidates, by declaration) and a board dossier pins its
    # materials in board.sexp (the processor unit + the device material ids). An
    # undeclared absence stays CANNOT JUDGE.
    shape = G.unit_shape(profile_dir)
    required: list[str] = []
    if shape == "board":
        try:
            bdoc = S.read_file(profile_dir / "board.sexp")[0]
        except (S.SexpError, IndexError) as exc:
            findings.append(f"CANNOT JUDGE {uid}: the pinned dossier does not map — {exc}")
            continue
        bproc = S.children(bdoc, "processor")[0]
        required = [str(S.field(bproc, "unit", "board.sexp"))]
        required += [str(S.field(d, "material", "board.sexp"))
                     for d in S.children(bdoc, "device")]
    else:
        try:
            src = D.load_sources(profile_dir / "sources.sexp")
            required = [s["id"] for s in src.get("source", [])]
            if shape != "device-model":
                refs = D.load_references(profile_dir / "references.sexp")
                required += ([e["id"] for e in refs.get("encoding_source", [])]
                             + [c["id"] for c in refs.get("candidate", [])])
        except D.DossierError as exc:
            findings.append(f"CANNOT JUDGE {uid}: the pinned dossier does not map — {exc}")
            continue
    required += list(G.shape_contracts(shape))
    text = bill.read_text()
    # one section per `###` heading; a section runs to the next heading of any level
    heads = [(m.start(), m.group(1)) for m in re.finditer(r"(?m)^###\s+(.*)$", text)]
    bounds = [m.start() for m in re.finditer(r"(?m)^#{1,3}\s", text)]
    for mid in required:
        hit = None
        for pos, heading in heads:
            if mid in heading:
                hit = pos
                break
        if hit is None:
            findings.append(f"MISSING SECTION {uid}: the bill has no `###` section naming "
                            f"'{mid}' — a material the pinned data carries is omitted, "
                            f"and an omission reads as if the material does not exist")
            continue
        end = min((b for b in bounds if b > hit), default=len(text))
        section = text[hit:end]
        if not re.search(r"does not supply", section, re.I):
            findings.append(f"NO DOES-NOT-SUPPLY {uid}: the '{mid}' section never states "
                            f"what the material does NOT supply — a bill that lists only "
                            f"what things provide is the lie of omission this gate exists "
                            f"to refuse")
    if len(findings) == before:
        print(f"  {uid}: {len(required)} materials, every fragment matches the pinned "
              f"data, every section carries its does-not-supply")

for f in findings:
    print(f)
print(f"__CHECKED__ {checked}")
sys.exit(1 if findings else 0)
PY
}

self_test() {
  SELFTEST_TMP() { local d="$ROOT/target/doctrine-selftest"; mkdir -p "$d"; mktemp -d "$d/XXXXXX"; }
  local t pass=0 fail=0 out rc
  t="$(SELFTEST_TMP)"

  argc() {
    [ "$2" -eq "$1" ] && return 0
    fail=$((fail+1))
    printf 'MATERIALS-BILL self-test HARNESS: %s() got %s argument(s), expected %s — a missing `;` before `arm` swallows it\n' "$3" "$2" "$1" >&2
    return 1
  }
  arm() {
    argc 3 "$#" arm || return
    out="$(check_bills "$t" 2>&1)"; rc=$?
    if [ "$rc" != "$2" ]; then
      fail=$((fail+1)); printf 'MATERIALS-BILL self-test MISS: %s expected rc=%s got rc=%s\n%s\n' "$1" "$2" "$rc" "$out" >&2
    elif ! printf '%s' "$out" | grep -qF "$3"; then
      fail=$((fail+1)); printf 'MATERIALS-BILL self-test MISS: %s right verdict, wrong reason (no %s)\n%s\n' "$1" "$3" "$out" >&2
    else pass=$((pass+1)); fi
  }

  # A scratch corpus: the REAL profile dossier and book, re-rooted as unit "p" — the
  # fragments are regenerated into the fixture by the real generator.
  fixture() {
    rm -rf "$t/profiles/p" "$t/books/p"
    mkdir -p "$t/profiles" "$t/books" "$t/materials"
    cp -R "$ROOT/profiles/rv64i-lab-v0" "$t/profiles/p"
    cp -R "$ROOT/docs/models/rv64i-lab-v0" "$t/books/p"
    printf '(unit (id "p") (kind processor) (layer processor) (book "books/p"))\n' \
      > "$t/materials/units.sexp"
    python3 scripts/gen_model_book.py --profile-dir "$t/profiles/p" \
      --book-dir "$t/books/p" >/dev/null
  }

  arm "REFUSE no units registry at all" 2 "REFUSED"

  fixture
  arm "GREEN the real bill over the real dossier" 0 "every section carries its does-not-supply"

  printf '\n| `X` | hand-edited |\n' >> "$t/books/p/src/materials/pinned-specifications.md"
  arm "RED   a hand-edited generated table" 1 "DRIFT"
  python3 scripts/gen_model_book.py --profile-dir "$t/profiles/p" \
    --book-dir "$t/books/p" >/dev/null

  python3 - "$t/books/p/src/materials.md" <<'PYEOF'
import re, sys
p = sys.argv[1]
text = open(p).read()
i = text.index("### `spike`")
j = text.index("###", i + 5)
open(p, "w").write(text[:i] + text[j:])
PYEOF
  arm "RED   a material with no section" 1 "MISSING SECTION p: the bill has no \`###\` section naming 'spike'"

  fixture
  python3 - "$t/books/p/src/materials.md" <<'PYEOF'
import sys
p = sys.argv[1]
text = open(p).read()
i = text.index("### `spike`")
j = text.index("###", i + 5)
section = text[i:j].replace("**Does not supply:**", "**Supplies, furthermore:**")
open(p, "w").write(text[:i] + section + text[j:])
PYEOF
  arm "RED   a section that never says what the material does NOT supply" 1 "NO DOES-NOT-SUPPLY"

  fixture
  rm "$t/books/p/src/materials.md"
  arm "RED   a book with no bill chapter" 1 "NO BILL"

  rm "$t/books/p/book.toml"
  arm "RED   a book with no skeleton" 1 "NO BOOK"

  # ── P5-BOARD.11: the device and board shapes — the census follows the declaration.
  # The fixtures re-root the REAL dossiers (the UART's, the board's) exactly as the
  # processor fixture does, and the bills name every material the shape enumerates.
  devfixture() {
    rm -rf "$t/profiles/d" "$t/books/d"
    mkdir -p "$t/books/d/src/materials"
    cp -R "$ROOT/profiles/sifive-uart-lab-v0" "$t/profiles/d"
    cat > "$t/materials/units.sexp" <<'EOF'
(unit (id "d") (kind device) (layer device) (book "books/d"))
EOF
    cat > "$t/books/d/book.toml" <<'EOF'
[book]
title = "d"
EOF
    printf '# Summary\n\n[materials](materials.md)\n' > "$t/books/d/src/SUMMARY.md"
    python3 scripts/gen_model_book.py --profile-dir "$t/profiles/d" \
      --book-dir "$t/books/d" >/dev/null
    {
      printf '# Materials bill\n\n'
      for m in SIFIVE-FU540-C000 profile.sexp state.sexp requirements.sexp \
               contract-obligations.sexp expectations/; do
        printf '### `%s`\n\nWhat it is for.\n\n**Does not supply:** something.\n\n' "$m"
      done
    } > "$t/books/d/src/materials.md"
  }

  devfixture
  arm "GREEN a device-shaped bill — no references.sexp, expectations/ is the corpus" 0 \
      "every section carries its does-not-supply"

  devfixture
  python3 - "$t/books/d/src/materials.md" <<'PYEOF'
import sys
p = sys.argv[1]
text = open(p).read()
i = text.index("### `expectations/`")
j = text.index("###", i + 5) if "###" in text[i + 5:] else len(text)
open(p, "w").write(text[:i] + text[j:])
PYEOF
  arm "RED   a device bill omitting the expectations/ section" 1 "MISSING SECTION d"

  boardfixture() {
    rm -rf "$t/profiles/b" "$t/books/b"
    mkdir -p "$t/books/b/src/materials"
    cp -R "$ROOT/profiles/netboard-lab-v0" "$t/profiles/b"
    cat > "$t/materials/units.sexp" <<'EOF'
(unit (id "b") (kind board) (layer board) (book "books/b"))
EOF
    cat > "$t/books/b/book.toml" <<'EOF'
[book]
title = "b"
EOF
    printf '# Summary\n\n[materials](materials.md)\n' > "$t/books/b/src/SUMMARY.md"
    python3 scripts/gen_model_book.py --profile-dir "$t/profiles/b" \
      --book-dir "$t/books/b" >/dev/null
    {
      printf '# Materials bill\n\n'
      for m in rv64i-lab-v0 SIFIVE-FU540-C000 MICROCHIP-LAN9118 board.sexp DOSSIER.md; do
        printf '### `%s`\n\nWhat it is for.\n\n**Does not supply:** something.\n\n' "$m"
      done
    } > "$t/books/b/src/materials.md"
  }

  boardfixture
  arm "GREEN a board-shaped bill — the composition pins are the materials" 0 \
      "every section carries its does-not-supply"

  boardfixture
  python3 - "$t/books/b/src/materials.md" <<'PYEOF'
import sys
p = sys.argv[1]
text = open(p).read()
i = text.index("### `MICROCHIP-LAN9118`")
j = text.index("###", i + 5)
open(p, "w").write(text[:i] + text[j:])
PYEOF
  arm "RED   a board bill omitting a device material pin" 1 "MISSING SECTION b"

  rm -rf "$t"
  printf 'MATERIALS-BILL --self-test: %d pass / %d fail\n' "$pass" "$fail"
  [ "$fail" -eq 0 ]
}

[ "${1:-}" = "--self-test" ] && { self_test; exit $?; }

self_test >/dev/null 2>&1 || {
  echo "MATERIALS-BILL: REFUSED — the check does not discriminate (self-test failed)." >&2; exit 2; }

out="$(check_bills "$ROOT")"; rc=$?
count="$(printf '%s' "$out" | sed -n 's/^__CHECKED__ //p')"
body="$(printf '%s' "$out" | grep -v '^__CHECKED__ ' || true)"
if [ "$rc" -eq 2 ]; then
  { echo "MATERIALS-BILL: REFUSED — the unit corpus could not be read."
    printf '%s\n' "$body" | sed 's/^/  /'; } >&2
  exit 2
fi
if [ "$rc" -ne 0 ]; then
  { echo "MATERIALS-BILL: a unit's materials bill does not hold."
    printf '%s\n' "$body" | sed 's/^/  /'
    echo "  Regenerate the fragments (never edit them), and give every material its section"
    echo "  with its does-not-supply statement."; } >&2
  exit 1
fi
printf '%s\n' "$body"
printf 'MATERIALS-BILL: ok (%s unit(s) — generated tables match the pinned data; every material states what it does not supply)\n' "${count:-0}"
exit 0

# The published selected Sail identity

`profiles/rv64gc-lab-v0/retained/sail-identity.sexp` is the selected reference
descriptor for the proposed first canonical division capture. Its711 bytes have
SHA256 `b0d88c7ae4b3cbb6b856af338811947dd58c6d8e754043d901f2952aeaecea77`.
It contains one candidate and no experiments. The existing bounded
[identity emitter and reader](retained-method.md#emitting-a-selected-execution-descriptor)
produce and verify it; there is no second artifact format or parser.

The descriptor projects these execution fields from the separately validated
current parent dossier, `profiles/rv64gc-lab-v0/references.sexp`:

| Field | Selected value |
| --- | --- |
| `id` | `sail-riscv` |
| `origin` | `https://github.com/riscv/sail-riscv` |
| `kind` | `prebuilt release binary` |
| `release` | `0.14` |
| `binary` | `target/refs/sail-riscv-Mac-arm64/bin/sail_riscv_sim` |
| `binary_sha256` | `16de42a86e4ea7a300385092632cd95d153cb3f6c119d31eaa9384953990b7bf` |

Other optional execution fields are absent. Empty presence would be a different
identity. The selected candidate has fixed descriptive labels: role `selected
execution identity`, status `retained descriptor`, and lineage `unexamined; no
ancestry or independence credit`. Parent assessments, historical matching prose,
other candidates, encoding-source records and experiment records are excluded.
Changing that prose cannot change this projection. Relevant execution-field
changes must make the old descriptor stale even if its file pin still matches.

The date `2026-10-19` records descriptor publication. Host fields record the
publication host: Darwin, kernel27.0.0, arm64, and the observed Apple clang21
version string. The host note explicitly says that this is publication rather
than binary acquisition and attests no execution. Checking elsewhere preserves
that historical metadata; it does not rediscover or compare the checking host.
The repository-relative `work_dir` remains `target/refs`.

## Verify without the acquired binary or source cache

From the trusted repository root, this complete example validates the parent
schema before mapping, selects exactly one current candidate and authenticates
the retained descriptor through its existing reader. The input ID below is a
local diagnostic name; the final manifest must declare its exact principal.

```bash
PYTHONPATH=scripts python3 - <<'PY_SELECTED_IDENTITY'
from pathlib import Path
import check_sexp_schema as K
import dossier_sexp as D
import matched_gpr_identity as I
import sexp as S

root = Path.cwd()
parent = "profiles/rv64gc-lab-v0/references.sexp"
with (root / parent).open("rb") as stream:
    payload = stream.read(65537)
if not 1 <= len(payload) <= 65536:
    raise ValueError("parent exceeds diagnostic bound")
text = payload.decode("utf-8")
constructs, operators = K.load_schema(root / "schema/references.sexp")
issues = K.validate_text(text, constructs, operators, parent)
if issues:
    raise ValueError(issues[0])
forms = [form for form in S.parse(text, parent) if form[0] != "comment"]
if len(forms) != 1 or forms[0][0] != "references":
    raise ValueError("expected one parent references document")
document = D.references_to_doc(forms[0])
selected = [candidate for candidate in document["candidate"]
            if candidate["id"] == "sail-riscv"]
if document["profile"] != "rv64gc-lab-v0" or len(selected) != 1:
    raise ValueError("expected this profile's one selected candidate")
record = dict(id="SAIL-IDENTITY", role="reference-identity",
              path="profiles/rv64gc-lab-v0/retained/sail-identity.sexp",
              sha256="b0d88c7ae4b3cbb6b856af338811947dd58c6d8e754043d901f2952aeaecea77")
checked = I.read_reference_identity(root, record, selected[0])
print(checked.disposition, checked.pin.disposition, len(checked.execution_identity))
changed = dict(selected[0], binary_sha256="0" * 64)
stale = I.read_reference_identity(root, record, changed)
print(stale.disposition, stale.pin.disposition)
PY_SELECTED_IDENTITY
python3 scripts/probe_retained_sail_identity.py
python3 -O scripts/probe_retained_sail_identity.py
```

It prints `matched matched 6`, then `stale matched`. The11 controls also rebuild
the exact published bytes through the emitter using fixed publication metadata,
check optional presence and excluded prose, reject malformed or oversized
descriptors, and distinguish a changed pin from changed execution identity.
A three-file copy containing only the parent dossier, retained descriptor and
references schema verifies with no binary or `.materials` directory present.
Those are the diagnostic's retained data requirements; Python and the existing
project reader/schema modules remain runtime dependencies. It runs no reference
process and supplies no canonical execution evidence.

The current CPU-SYSTEM report includes every tracked profile source in its dossier
digest. Stage a new retained source before regenerating through
`python3 scripts/gate_report.py rv64gc-lab-v0 --gate GS`; the report check must run
against that final tracked population. This publication changes only the report's
dossier digest, with every capability verdict unchanged.

The descriptor belongs to the existing bounded `profiles/` family. It is a
selected `reference-identity` principal, separate from dependency children and the
original publication authority for the retained DIV statement. Publishing it
does not finish the capture declaration. The [prepared retention family](prepared-inputs.md)
is declared; the [composed entrypoint and exact native declarations](capture-plan.md#retained-native-predeclarations)
are retained. Commit them before a canonical run. Fresh replay separately needs the
actual pinned executable. Full method/policy adequacy and qualification remain
pending.

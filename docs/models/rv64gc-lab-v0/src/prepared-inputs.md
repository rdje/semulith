# Prepared inputs for the finite division capture

The first proposed canonical case now has four retained inputs under
`evidence/rv64gc-signed-div-truncation-v2/`. They were curated without launching a
reference process. Preparation checks source/image correspondence and all27
source-derived GPR-change boundaries; it grants no execution or qualification
credit. The [reviewed finite property](source-property.md) remains the signed
quotient change at boundary2, rather than complete M-extension coverage.

| File under the case directory | Bytes | SHA256 |
| --- | --- | --- |
| `guest.elf` | 4416 | `38a327660cb1c699e15694fe98d0467e909726555688074d558768300138e153` |
| `reference-config.json` | 7609 | `666d937305f503aa2754784186945f033ade43601f9c9d0073a9ffeefeb43ed2` |
| `baseline.expected.sexp` | 5847 | `87a5b54c50e147017a2dc60d69869d36679067026d7f449d75db6a344199907e` |
| `control.expected.sexp` | 5443 | `3f8d591db326a6a83a47921b7743297edc758eb602fa70660b770d37a07c758e` |

The four files total23,315 bytes. The selected [Sail identity](selected-identity.md)
and retained DIV statement remain separate existing inputs in the profile.
An acquired executable is a separately pinned replay dependency.

## Canonical sources and construction

The guest source is `profiles/rv64gc-lab-v0/guests/m-div.s`,2512 bytes with SHA256
`a7cbbe8c3005a7c0da68bf356a0fb6b072dbe0cdcc659eff523e465c60ae907f`.
`matched_gpr_image.build_guest_image` constructs the complete ELF at the fixed
cold entry `0x80000000` through the canonical GC assembler. The public
`check_source_image` verifies every supplied ELF byte against that construction.
Header, padding and instruction bytes are all included.

The baseline is a byte-exact copy of the existing canonical `m-div.expected.sexp`
beside that source. It declares27 boundaries and54 fetches. The public
`compare_source_expectation` rederives every declared GPR change through the
existing snapshot author and binds the reviewed x7 witness. This finite check
does not observe every architectural state dimension.

The control maps that baseline through the existing expectations schema and
dossier owner, changes only boundary2's x7 value from `0xfffffffffffffffd` (`-3`)
to `0xfffffffffffffffc` (`-4`), and renders through the existing serializer.
A structured comment labels the deliberately wrong value. Every mapped field
outside that one value, including the correct baseline derivation text, remains
equal. The source author reports a difference at boundary2. That is a prepared
negative expectation; the fresh reference control run still has to occur.

The configuration's canonical source remains
`profiles/rv64gc-lab-v0/reference/sail-rv64gc-lab-v0.override.sexp`,6993 bytes with
SHA256 `9d27a970c42bdcccfdf948c39868a788d0dd3ecb7eb961767a143af1d3545935`.
Raw override-schema validation precedes its sole dossier mapping. The retained
JSON is exactly `json.dumps(mapped_override, indent=2) + "\n"`, the representation
used by the existing public `materialize_sail_override` route. It is an
interoperability artifact for Sail's published interface. S-expression remains
the source of truth. A byte/dictionary equality check supplies no new observed
configuration-effect or platform-equivalence credit.

## Verify the retained inputs

Run from the trusted repository root:

```bash
python3 scripts/probe_div_capture_inputs.py
python3 -O scripts/probe_div_capture_inputs.py
```

Both modes report `DIV-CAPTURE-INPUTS: 16 tests / 0 failures / 0 errors`. The
controls authenticate actual pins through the anchored snapshot reader, check
complete image/value/config correspondence, distinguish unavailable files from
changed bytes, and refuse an oversized artifact even with a matching pin.
The loader checks the declared member list and per-role bounds, refuses links
and foreign-volume members, and never descends into unknown directories. Omitting
that actual loader check loses five assertions in both modes, with zero harness
errors. Repinning a changed image does not restore source correspondence. A second
wrong control value is detected at its actual earlier source boundary.

The supplied-byte checks start no process and perform no artifact reopen;
canonical schema/assembler data remain explicit tool dependencies. A separate
75-file copied runtime/data set passes with neither the binary nor `.materials`.
Ten damaged or missing input/authority/layout cases refuse in normal and optimized
Python. The current [producer review](capture-plan.md#reviewing-the-authority-loader-within-the-producer-route)
covers37 modules,27 execution-data files,13 current views and64 proposed children.
Preparation's canonical override/schema and baseline remain curation inputs,
separate from that declared execution-loader trace.
The final manifest must still be constructed from the complete reviewed route.

## Reproduce the four files in a disposable directory

This complete example uses existing public producers and mappers. It writes
only inside a temporary directory under `target/`, compares every reproduced
byte with the retained inputs and removes the temporary files. It launches no
reference process and changes no retained artifact.

```bash
PYTHONPATH=scripts python3 - <<'PY_PREPARED_DIV'
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import check_sexp_schema as K
import dossier_sexp as D
import matched_gpr_comparison as C
import matched_gpr_image as G
import matched_gpr_property as P
import records_sexp as R
import sexp as S

root = Path.cwd()
profile = root / "profiles/rv64gc-lab-v0"
retained = root / "evidence/rv64gc-signed-div-truncation-v2"
case = P.signed_division_case()
def read(path):
    with path.open("rb") as stream:
        data = stream.read(65537)
    if not 1 <= len(data) <= 65536:
        raise ValueError("curation input exceeds bound")
    return data
def map_document(data, kind, mapper):
    text = data.decode("utf-8")
    constructs, operators = K.load_schema(root / "schema" / (kind + ".sexp"))
    issues = K.validate_text(text, constructs, operators, kind)
    if issues:
        raise ValueError(issues[0])
    forms = [form for form in S.parse(text, kind) if form[0] != "comment"]
    if len(forms) != 1 or forms[0][0] != kind:
        raise ValueError("expected one canonical document")
    return mapper(forms[0])
source = read(profile / "guests/m-div.s")
baseline = read(profile / "guests/m-div.expected.sexp")
expected = map_document(baseline, "expectations", D.expectations_to_doc)
override = map_document(read(profile / "reference/sail-rv64gc-lab-v0.override.sexp"),
                        "override", D.override_to_doc)
values = C.compare_source_expectation(source=source, baseline_expectation=baseline,
    instructions=case.instructions, program=case.program, witness=case.witness)
if values.disposition != "matched" or values.facts.witness_value != case.expected_value:
    raise ValueError(values.reason)
changed = deepcopy(expected)
changed["step"][2]["writes"]["x7"] = f"0x{case.control_value:016x}"
note = ("Deliberately incorrect negative control: only boundary 2 x7 changes from -3 to -4. "
        "Baseline derivation text is retained to show why the value is wrong; no execution evidence.")
control = R.render_forms([[S.Symbol("comment"), note], D.expectations_to_form(changed)]).encode()
image = G.build_guest_image(source, program=case.program, entry=0x80000000)
outputs = {"guest.elf": image.image,
           "reference-config.json": (json.dumps(override, indent=2) + "\n").encode(),
           "baseline.expected.sexp": baseline, "control.expected.sexp": control}
base = root / "target/prepared-div-inputs-example"
base.mkdir(parents=True, exist_ok=True)
with TemporaryDirectory(dir=base) as directory:
    for name, payload in outputs.items():
        with (Path(directory) / name).open("xb") as stream:
            stream.write(payload)
        print(name, len(payload), payload == read(retained / name))
PY_PREPARED_DIV
```

The four lines report `guest.elf 4416 True`, `reference-config.json 7609 True`,
`baseline.expected.sexp 5847 True` and `control.expected.sexp 5443 True`.
Curating the baseline, deriving source values and observing Sail remain separate
activities. The existing source author is named once; preparation adds no
independent expected-result producer.

## Declared output namespace and retention

The bounded `evidence/README.md` index declares one finite case with22 total
slots: this family index, four prepared inputs, twelve future observations and
five declaration/result slots. Future runs use `baseline`, `repeat`
and `control`, each with `.trace`, `.stdout`, `.stderr` and `.receipt.sexp`.
The metadata names are `planned-experiment.sexp`, `dependencies.sexp`,
`authorities.sexp`, `measured-experiment.sexp` and `verification.json`.
The three native declarations are now [retained](capture-plan.md#retained-native-predeclarations);
the twelve observations and two result files are now [retained](canonical-division.md).

The registry caps the family at22 files,16 MiB aggregate and4 MiB per member.
Three traces at the collector's4 MiB bound, six streams and three receipts at
64 KiB each, nine prepared/metadata slots at64 KiB, and the4 KiB index total at
most13,766,656 bytes. The index also has an80-line ceiling. Existing family caps,
the128 MiB combined artifact-read allowance and16 MiB snapshot ceiling stay
unchanged. These payload/retention ceilings do not bound total process RAM.

The [capture declaration](capture-plan.md#complete-the-capture-declaration) and
composed entrypoint are now retained; commit the exact native files before
reference execution. Collection must use the combined allowance API,
refuse existing output names and preserve real failed/partial observations.
Offline retained evaluation must work without an acquired reference cache;
fresh replay separately needs the actual pinned binary. Full method/policy
adequacy and qualification remain pending; canonical observations are retained.

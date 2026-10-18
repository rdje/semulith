# DEV_NOTES shard — _(2026-10-18)_ … _(2026-10-18)_

> Sharded from `DEV_NOTES.md` under its 48 KiB ceiling (`doctrine/readme_routes.tsv`).
> Entries in a shard are **never edited after the shard** — git history is canonical.

## _(2026-10-18)_ — full-profile detector controls before GC reduction (P4-SYSTEM.16)

P4-0251 begins after5c42e3a/brief0/host0, with only the explicitly queued task
note dirty. Native demo --profile=rv64gc-lab-v0 --guest=guest-control with
--mutate=zext-addi refuses2 before; --json instead returns0/plain text. The
latter is a real machine-readable-success defect: the common parser consumes
the flag but the GC route ignores its boolean. Own and fix it in this slice.

Add model_rv64gc::Model with Production, ZextAddi and JalNoLink. Rebuild only
the selected canonical GC effect spine, retaining the entire generated table
and all row metadata, including compressed expansion effects. This never uses
scalar-only tables or a second evaluator. OnceLock caches each control table;
only three small static Sem nodes for the ADDI spine are allocated once, while
JAL reuses its existing transfer effect. Unexpected source shapes refuse by
name. They are deliberately wrong controls, not accepted ISA implementations.
The full P4.15 mutation campaign is still pending; do not credit its gate kind.

The common runner accepts an explicit full-GC table. Production still passes
INSNS; the existing loop changes only step to step_over with that parameter.
New named APIs preserve the same typed fault regions. Every167 guest compares
production trace/fetch/complete final CPU state/memory through both API paths.
Selected controls fail at guest-control boundaries1/x1 and7/x5, anchored in the
spec-derived expected writes. Metadata/pointer checks preserve all untouched
rows and repeat-call cache identity; malformed effect shapes and unknown names
refuse. C-links remains identical under these 32-bit-form controls.

The text demo names each selected model and displays both observations at the
first differing paired boundary. Unknown controls refuse2; detectable wrong
results exit1. A GC --json request now refuses2 with an explicit unsupported
structured-report message and no stdout; scalar JSON remains valid. Default
production output is compared byte-exact to the pre-change native output.
GC bundles still record production only; model-aware records and reduction
follow in .16. Book examples state that intentionally wrong demos exit1 and
unaffected guests may agree. No CPU acceptance or regression-campaign claim.

Strict lint first rejects three nested pattern matches; flatten them into
explicit match patterns/guards, retaining the same shape refusals. No allow
attribute or lint policy changes. Own necessary whole-history rollover before
new prose: CH78=72+6/5453B into0337; DEV17=14+3/7207B into0338, with exact order
and bytes and old manifest prefix. Sharder self-test12/0. Evidence and final
scope/old-loop/default-output proofs: target/p4-system-16/controls. Rust/wasm,
focused publication and book checks precede normal COMMIT. LIVE_STATUS stays
P4 In Progress13/18, replay3/4, CPU-SYSTEM incomplete; board10/12 unchanged.
The history gate correctly refuses intent-added shards with the old staged
manifest. Stage the complete verified partition before judging that view.
New shard terminal blank lines are exact old payload bytes; preserve them.
The whitespace probe reports only those two shard endings; source/docs checks
exclude these two verbatim artifacts explicitly. No frozen payload is trimmed. Focused13, Rust/wasm, seven books and normal/O
scope checks pass:1487 protected files/95 old head entries, exact legacy loop
with explicit table, byte-exact default demo and four rendered guide views.

The first full hook exposes the isolated C-image crate's explicit dependency
closure: it copies run_rv64gc but omits its new Model module. The positive
case cannot compile, and the wrong-offset arm fails for that unrelated reason;
GUEST-GEN correctly refuses326pass/2fail. Add the unchanged production Model
module to that fixture and its root declarations. Its test module is an explicit
empty fixture because this crate runs only its own image tests; the complete
control-model suite remains compiled/executed in the workspace. Preserve both
original C-image tests, expected data and the exact wrong-offset mutation.
This is dependency-closure repair, not acceptance of a compile error as evidence.
Reading the affected C chapter also finds its current-scope sentence still
calling v2 open after .13 froze it and still referring to remaining contract
work after G-CONTRACT passed. Correct both current-status phrases against the
contract/gate; historical receipts and all contract members remain exact.
Direct image positive normal/O exits0, wrong-offset normal/O exits1 with the
same mixed-step0-write reason, and padding exits1 at exact-image verification.
The complete GUEST-GEN self-test returns328/0 after repair. Scope normal/O now
protects1485 files/95 old entries; final book and publication checks follow.

## _(2026-10-18)_ — complete RV64GC replay records (P4-SYSTEM.16)

P4-0250 starts from clean1cf0673, brief0/untracked and a green host census.
The actual GC bundle CLI refuses2 before. Add the fs-free BundleRv64gc API
and explicit-profile bundle/replay routes. Input is a complete snapshot; its
CPU, memory, typed fault regions and runtime/definition/lock identity travel
with an explicit flat-memory/no-external-events policy. CLI recording selects
tracked production guests from reset; API recording also supports checkpoints.
Producer-source pins bind the replay machinery and string encoder. These are
reproducibility identities, not an external author's authenticity signature.

Compare incoming PC, resulting mode and ordered GPR changes at their first
absolute boundary, then independently compare boundary count, model-error and
fetch receipts and SHA256 of the complete canonical final checkpoint. Aggregate
receipts do not pretend to locate the first instruction responsible. Identical
model-error reproduction is successful replay, not a correct CPU verdict.
Keep reduction/nonproduction GC mutation models out of this slice. Bounds:
10000 continuation boundaries, existing64MiB memory, 145MiB JSON, depth12,
2000000 structural punctuation and4096B model-error text; fail before parsing
or execution at the applicable boundary. Artifact limits are not exact RAM caps.

Review also finds both snapshot writers interpolate digest text unescaped.
Permanent Cargo tests reproduce runtime and memory quote/control-character
serialization failures independently (1pass/2fail before), then pass3/0 after
using the existing JSON string encoder. Restore continues refusing both foreign
identities. The earlier manual rlib probe could not link; its output is not a
behavior witness. Include the encoder source in the conservative runtime pins.
No valid digest bytes or scalar replay behavior change. CLI tests retain the
actual scalar catalogue/default route as well as four GC system cases.

Own necessary bounded retention in the product slice: all four complete a21
reader-unit spans (3766B) move into the existing mutable reader record. Preserve
its121386B old prefix and every published archive. Source offsets/digests plus
unique root stubs yield the exact131036B owner inverse; four independently
damaged payloads refuse. Root127897B/retention128023B before new growth stay
under the existing131072B ceilings. Preserve the original root heading and
link the full retained decision/acceptance/verification/commit bytes. No capacity
raise, new task file, canonical record or qualification change.

Evidence: target/p4-system-16/replay. All167 corpus bundles round-trip/replay;
mid-execution/empty continuations and changed PC/mode/GPR/length/fetch/error/final
receipts discriminate, as do missing/foreign/invalid inputs and step bounds.
Four real CLI cases cover atomics, wait/timer, translation and floating point;
usage/malformed2, changed/refused1, identical0. G-REPLAY gains only the bundle
kind (3/4); CPU-SYSTEM remains incomplete, P4 remains13/18 and .14 stays open.
The first manifest used kind bundle; the gate refused it by name. Correct to
the existing required kind replay-bundle without changing the gate. Focused
publication, Rust/wasm and book checks precede the normal COMMIT. The route
gate catches the new LIVE row6B over its fixed cap; concise current wording
fits. Correct the print probe to require the gate table in its actual GC book
owner; both main-book guide views remain explicitly checked. Focused13, make check,
wasm, seven books and source/inverse checks pass normal/O:1479 protected
files,93 whole old head entries,4 retained spans/4 damaged refusals. The first
commit hook rejects the abbreviated ADDRESSED bullet. Cancel that owned Git
parent/eight descendants, verify process residue0, add the actual Cargo command
and rc=0 to the bullet, then rerun acceptance and normal hooks.


# The four `state` requirements are credited through matched cases in the GPR vocabulary; the CSR-write format waits for a property GPRs cannot witness

- **Type:** `decision`
- **Date:** `2026-10-27`
- **Status:** `active`
- **Owner / source:** `P4-SYSTEM.14` a43, `SEMULITH-P4-0305` (feature 9 under
  [`decision_alternate-port-and-features.md`](decision_alternate-port-and-features.md)); the workflow's decision under
  [`decision_four-rulings-delegated.md`](decision_four-rulings-delegated.md); continues
  [`decision_req-gc-m-credited-implemented.md`](decision_req-gc-m-credited-implemented.md) and
  [`decision_qualified-matched-experiment-contract.md`](decision_qualified-matched-experiment-contract.md).
answers: How do the four `kind state` requirements of rv64gc-lab-v0 leave `planned`, in what order, with what vocabulary, and what does each case not claim?

## The fact / decision

1. **The route is the M case's.** G-STATE's open part is `0 of 4 state requirements implemented`; the derivation
   (`scripts/requirement_status.py`) credits a requirement only through a CURRENT credit record naming a case whose
   measured record and receipt authenticate. Each of REQ-D-XLEN, REQ-D-CSR-SET, REQ-D-ZICNTR and REQ-D-SSTC therefore
   gets one finite matched case under `evidence/<case>/`, declared, captured (baseline, byte-identical repeat, a
   diverging control) through the fixed Sail invocation, reviewed, credited (`authority review` under the 2026-10-26
   delegation) and recorded in the dossier — three units per case: (i) program + EVD-05 expectations derived from the
   pinned chapters before any run + curated inputs + declaration; (ii) capture + retained reviews; (iii) credit record +
   dossier record + the derived `implementation_status`.
2. **The vocabulary stays `matched-gpr-v1`.** Every required check of the four obligations can be witnessed as a GPR
   change at a step boundary, with the policy's feature rules met inside the program:
   - XLEN (`defined`, low): 64-bit values and 2^64 wrap (shifts by 63, sign/zero extension, `*W` results); the 64-bit
     address space through a faulting access whose `mtval`, read into a GPR by the handler, carries the full address.
     Control: a 32-bit-truncated expected value.
   - CSR-SET (`implementation-defined`, high): the 33 CSRs each read into a sentinel-loaded GPR at their privilege (a
     zero reset value is then an observed change); alias pairs written through one name and read through the other
     (`sstatus`/`mstatus`, `sie`/`mie`, `sip`/`mip`, `fflags`/`frm`/`fcsr`); a refused write (read-only address,
     lower-privilege access) that must not commit, read back; a non-member address trapping illegal-instruction
     (`mcause` 2 and `mepc` into GPRs) — the policy's "legal/refused modes, aliases and preserved state".
   - ZICNTR (`implementation-defined`, high): readable in M; gated in S/U by `mcounteren`/`scounteren` (trap or marker
     write after the read); `instret` counts retired instructions in both models. The `cycle` and `time` VALUES are
     the laboratory's declared profile difference (fixed-zero cycle, one tick per step boundary — `mm-counters.expected.sexp`;
     Sail: `mcycle` per instruction, `mtime` per `instructions_per_tick` 2 at `clock_frequency` 1e9) and stay
     corpus-judged; the case names them in `limitations` as the policy's "explicitly observed and justified profile
     difference". "Host timing is not guest time."
   - SSTC (`implementation-defined`, high): `stimecmp` accessible in M, in S iff `menvcfg.STCE` (trap otherwise);
     delivery (`scause` 0x8000000000000005 into a GPR) with boundary-robust schedules both models deliver at the same
     step — `stimecmp` 0 once `sie.STIE`/`sstatus.SIE` are set — and suppression with `stimecmp` max, `STIE` clear,
     `STCE` clear; rate-dependent schedules stay in `mm-stimecmp.expected.sexp`.
   The high-risk three carry the policy's second method as the m-forms case did: the EVD-05 expectation author and the
   Sail reference are the two producers; the adversarial case is the refused write / suppressed delivery.
3. **The CSR-write format is deferred.** The pinned Sail sim's `--trace-csr` prints `CSR mstatus (0x300) <- 0x…` (44
   such lines over the retained M guest, all at its traps: target/p4-system-14/a43/sail-trace-csr-sample.txt). It is
   not in the fixed 11-argv invocation `matched_gpr_execution.py` pins; adopting it is a new format (`matched-state-v1`:
   collector parse, comparison rule, `schema/references.sexp` pattern, argv, probes, gate arms) of the a12–a42 scale.
   It is built only when a required check cannot be witnessed through GPRs — none of the four needs it.
4. **Order.** a43a XLEN (feature 10; the smallest, `defined`, and the first exercise of the route on a second
   requirement), a43b CSR-SET, a43c ZICNTR, a43d SSTC. The status act of a43d regenerates GS with G-STATE green (the
   census is already 12 of 12 answered).

## Why

- A requirement leaves `planned` only through a case (EVIDENCE_POLICY.md "Status and supersession": "No typed success
  word substitutes for executed evidence"); the a42 series built the whole route and credited one requirement with it;
  re-using it is the honest minimum and the fastest path to the axis.
- Every GPR witness above is an observation both models already emit under the fixed invocation; a new trace vocabulary
  would add months of mechanism for properties the GPR trace already reaches through the handler-reads-CSR idiom the
  corpus uses everywhere (`mm-csr-*`, `mm-counters`, `mm-stimecmp`).
- The counter values cannot agree and must not be made to: the laboratory's counter policy is a declared choice of
  this profile (P4-SYSTEM.5/.9 own the rate semantics); the policy's implementation-defined row allows a justified
  observed difference, not a silent exclusion — so the case records it.

## How to apply

- Before a43a's capture, review the case manifest's dependency closure: the M case's manifest pins `scripts/gate_report.py`
  (60 inputs), and the pending ruling on report generators as measurement inputs decides whether four more credits
  may inherit that coupling (`a-report-generator-pinned-as-a-measurement-input.md`).
- Each case's `limitations` state what the status does not claim: a finite program, one witness per check, counter
  values and rate-dependent schedules out of scope, no claim about acceptance.
- A property that cannot be phrased as a GPR change at a step boundary reopens item 3; nothing else does.

## Addendum — measured 2026-10-27 (a43b-1, `SEMULITH-P4-0307`)

- **The reference has no Zicntr under the pinned override.** `csrrs` of mcycle, minstret, cycle, time and instret each trap
  illegal-instruction in the pinned Sail sim (33-CSR probe; `profiles/rv64gc-lab-v0/reference/sail-rv64gc-lab-v0.override.sexp`
  declares `Zicntr` unsupported; the dossier records "disabled reference Zicntr … leave those observations unmatched"). So
  item 2's CSR-SET case matches 28 of the 33 and names the five counters as corpus-judged (`mm-counters`,
  `mm-csr-ro-counters`). **Corrected by a43d-1 (`SEMULITH-P4-0308`):** item 2's ZICNTR case cannot be matched against this
  reference at all — a counter read that succeeds in the laboratory traps in Sail, and the S/U gating trap paths would
  agree for different reasons (the gate there, the absent extension here), which the policy forbids to count. ZICNTR's
  credit waits for a reference with Zicntr (a per-case reference configuration or a second reference), i.e. on the
  pinned-tooling ruling; its program is not authored until then. The policy's "genuine reference limitation leaves the
  affected comparison uncredited" applies.
- **The reference has no timer source under the pinned override** (`platform/clint` unsupported): with STCE set and
  `stimecmp` = 0 the laboratory reads `mip.STIP` (0x20) and Sail reads 0, and the supervisor timer interrupt the
  laboratory delivers at the next step head never arrives in Sail (probes target/p4-system-14/a43d/draft/mip-probe.s,
  sstc-probe.s; the dossier's "unmatched timer source"). So item 2's SSTC case witnesses M access without gating, a
  64-bit compare value written and read back, the two S gates (`mcounteren.TM`, `menvcfg.STCE`) as separate trap paths,
  and the S-mode kernel programming its own timer; delivery and suppression stay corpus-judged (`mm-stimecmp`,
  `w-timer`) and are named in the case's limitations.
- **The spec-side deriver's CSR vocabulary is the 33.** `derive_rv64gc_expectations.py` refuses any other CSR number
  (`csr 0x… outside the corpus's vocabulary`) and is a pinned input of the retained DIV case, so the "non-member address
  traps" witness is not derivable today; the negative side of CSR-SET is the refused write and the privilege-refused access.
- **A same-value write is not a change.** The GPR vocabulary records changes; a handler reading the same cause twice needs a
  sentinel between (the M program's own idiom). A trap before `mtvec` is set cascades into a fetch fault at address 0.

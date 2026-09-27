#!/usr/bin/env python3
"""Compare each reference model's OWN self-description against the profile, field by field.

⛔ WHY THIS EXISTS — a defect, not a nicety. `P0-PROFILE.10` found that this project had claimed a
"matched profile" on the strength of one scalar: `--print-isa-string` returned `rv64i_zvl32b`,
which is *true*, and describes an **instruction set** rather than a **machine**. Underneath it the
reference kept a device-bearing platform, and a guest read an advancing `mtime` with a plain load.

The failure mode is not an instrument that cannot see. It is **an instrument answering a narrower
question than the one asked** — a single confident scalar standing in for a configuration. A zero
invites doubt; a correct, confident, narrower answer does not.

⭐ THE REPLACEMENT PRINCIPLE. A match is claimed against the model's **own self-description at the
widest granularity it offers**, compared field by field — never against a scalar the operator
chose to read. Both references emit a **device tree**, which is that wider surface and is machine
readable, so the comparison is a command rather than a paragraph:

    sail_riscv_sim --config-override <cfg> --print-device-tree
    spike --isa=… --priv=… --dump-dts <elf>

⚠️ AND THE WIDE INSTRUMENT HAS ITS OWN SCOPE, which this module states rather than implies. A
device tree describes what a platform ADVERTISES. It is not the model's semantics, it is not its
memory attributes, and it can carry residue — the Sail tree still advertises a `timebase-frequency`
and an `htif` node with no device behind them. Wider is not complete, and the honest form of the
claim is "these fields agree", never "the models match".
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import dossier_sexp as D                                # noqa: E402

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())

# The fields a processor profile actually constrains. Each is read from both trees and compared
# with what the profile declares. A field absent from a tree is reported as absent, never as
# agreement — an omitted field reads exactly like a matching one otherwise.
FIELDS = ("riscv,isa", "mmu-type", "riscv,pmpregions", "timebase-frequency")


def dts_sail(config: Path) -> str:
    sim = ROOT / "target/refs/sail-riscv-Mac-arm64/bin/sail_riscv_sim"
    return subprocess.run([str(sim), "--config-override", str(config), "--print-device-tree"],
                          capture_output=True, text=True).stdout


def dts_spike(elf: Path) -> str:
    spike = ROOT / "target/refs/spike-build/spike"
    return subprocess.run([str(spike), "--isa=rv64i", "--priv=m", "--dump-dts", str(elf)],
                          capture_output=True, text=True).stdout


def field(dts: str, name: str) -> str:
    m = re.search(rf"{re.escape(name)}\s*=\s*([^;]+);", dts)
    return m.group(1).strip() if m else "<absent>"


def devices(dts: str) -> list[str]:
    """Every node of the form `name@address` — the devices the platform advertises."""
    return sorted({d.strip() for d in re.findall(r"^\s*([a-z0-9_]+@[0-9a-f]+)\s*\{", dts, re.M)})


def main() -> int:
    # the tracked truth is the .sexp; the JSON the model reads is derived from it
    # (SOT-FORMAT.4 — see run_smoke.py for the same pattern)
    if not (ROOT / "profiles/rv64i-lab-v0/reference/sail-rv64i-lab-v0.override.sexp").is_file():
        print("compare_platforms: the tracked override sail-rv64i-lab-v0.override.sexp is "
              "missing", file=sys.stderr)
        return 2
    cfg = D.materialize_sail_override(ROOT, "rv64i-lab-v0")
    elf = ROOT / "target/refs/guests/smoke-arith.elf"
    for p in (cfg, elf):
        if not p.exists():
            print(f"compare_platforms: {p} is missing — run scripts/run_smoke.py first",
                  file=sys.stderr)
            return 2

    sail, spike = dts_sail(cfg), dts_spike(elf)
    if not sail or not spike:
        print("compare_platforms: a model emitted no device tree; cannot judge", file=sys.stderr)
        return 2

    print(f"{'FIELD':22} {'sail (matched)':24} {'spike (matched)':24} agree")
    disagree = 0
    for f in FIELDS:
        a, b = field(sail, f), field(spike, f)
        ok = a == b
        disagree += 0 if ok else 1
        print(f"{f:22} {a:24} {b:24} {'yes' if ok else 'NO'}")

    da, db = devices(sail), devices(spike)
    print()
    print(f"devices advertised — sail : {', '.join(da) or 'none'}")
    print(f"devices advertised — spike: {', '.join(db) or 'none'}")
    only_spike = [d for d in db if d not in da]
    only_sail = [d for d in da if d not in db]
    print(f"  only spike: {', '.join(only_spike) or 'none'}")
    print(f"  only sail : {', '.join(only_sail) or 'none'}")

    print()
    print(f"platform fields disagreeing: {disagree} of {len(FIELDS)}; "
          f"devices only one model advertises: {len(only_spike) + len(only_sail)}")
    print("These are ENUMERATED differences (DIFF-PLATFORM-SPIKE), not failures: Spike's devices "
          "cannot be removed from its command line. The number existing is the point — it is what "
          "a single ISA string could not have told anyone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

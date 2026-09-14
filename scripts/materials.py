#!/usr/bin/env python3
"""Resolve a primary-source material to a path inside this repository — and never store one.

A MATERIAL is a document a model is derived from. `materials/catalog.sexp` records what each one
is; this tool answers *where is it right now*, which is a different question and a machine-shaped
one.

⛔ THE WHOLE DESIGN IS ONE RULE (Policy 12): a tracked file may not contain an absolute path,
because the repository can be moved to another directory, machine or filesystem and nothing about
it may break. A hard-coded `/Volumes/…` does not fail loudly when that happens — it fails as
"file not found" about a document that is sitting right there, which sends the reader looking for
the wrong problem. So paths compose from two roots and the catalogue knows only one of them:

    cache      <repo root>/<cache-root>/<cache-path>     both halves tracked and relative
    corpus     $<env-var>/<corpus-path>                  the left half NEVER tracked

The environment variable is the seam. An operator sets it once; git never sees it.

⛔ AND THE CACHE IS NOT A SOURCE OF TRUTH. `.materials/` is gitignored, so a fresh clone has an
empty one. That is the normal state, not an error state, and the difference matters: every path
this tool cannot produce becomes a REFUSAL NAMING THE COMMAND THAT FIXES IT, never a silent
fallback to a copy found somewhere else. A tool that quietly reads a different file than the one
the digest describes is worse than a tool that stops.
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sexp as _sexp                                                   # noqa: E402

REPO = Path(__file__).resolve().parent.parent
CATALOG = "materials/catalog.sexp"

REQUIRED = ("title", "revision", "licence", "corpus", "corpus-path", "cache-path", "sha256", "bytes")

# ⛔ A MATERIAL IS NOT ALWAYS ONE FILE. The RISC-V pin is a 72-page HTML snapshot, and a snapshot
# whose identity is "the digest of one of its pages" is not identified at all. A `snapshot` names a
# MANIFEST inside itself; the manifest's digest is the material's identity, and the manifest's
# entries verify every page. One extra field and one extra branch buys a whole shape of material.
KINDS = ("document", "snapshot")


class MaterialError(Exception):
    """A refusal. A material that cannot be resolved is never approximated."""


def _relative(kind: str, value: str, where: str) -> str:
    """A path in the catalogue is relative, and stays inside the root it is relative to."""
    if not value:
        raise MaterialError(f"{where}: {kind} is empty")
    if value.startswith("/") or (len(value) > 1 and value[1] == ":"):
        raise MaterialError(
            f"{where}: {kind} {value!r} is ABSOLUTE. Every path in the catalogue is relative to a "
            f"root named in the file, because this repository must survive being moved to another "
            f"filesystem (Policy 12). Record the path relative to its root instead.")
    parts = value.split("/")
    if ".." in parts:
        raise MaterialError(
            f"{where}: {kind} {value!r} escapes its root with '..'. A path that climbs out of the "
            f"root it is declared against is an absolute path wearing a disguise.")
    return value


def load(path: Path | None = None) -> dict:
    path = path or (REPO / CATALOG)
    forms = _sexp.read_file(path)
    if len(forms) != 1 or _sexp.head(forms[0], str(path)) != "materials":
        raise MaterialError(f"{path}: expected exactly one (materials …) form")
    root = forms[0]
    cache_root = _relative("cache-root", str(_sexp.field(root, "cache-root", str(path))), str(path))

    corpora: dict[str, dict] = {}
    for c in _sexp.children(root, "corpus"):
        cid = str(_sexp.field(c, "id", str(path)))
        if cid in corpora:
            raise MaterialError(f"{path}: corpus id {cid!r} declared twice")
        corpora[cid] = {"env_var": str(_sexp.field(c, "env-var", str(path))),
                        "revision": str(_sexp.field(c, "revision", str(path)))}

    materials: dict[str, dict] = {}
    for m in _sexp.children(root, "material"):
        mid = str(_sexp.field(m, "id", str(path)))
        where = f"{path}: material {mid!r}"
        if mid in materials:
            raise MaterialError(f"{path}: material id {mid!r} declared twice. An id is how a "
                                f"requirement names its evidence; two of them is no id at all.")
        rec = {"id": mid}
        for f in REQUIRED:
            try:
                rec[f.replace("-", "_")] = _sexp.field(m, f, where)
            except _sexp.SexpError as exc:
                raise MaterialError(f"{where}: missing required field ({f} …) — {exc}") from None
        rec["corpus"] = str(rec["corpus"])
        rec["sha256"] = str(rec["sha256"])
        rec["cache_path"] = _relative("cache-path", str(rec["cache_path"]), where)
        rec["corpus_path"] = _relative("corpus-path", str(rec["corpus_path"]), where)
        if rec["corpus"] not in corpora:
            raise MaterialError(f"{where}: names corpus {rec['corpus']!r}, which is not declared")
        if len(rec["sha256"]) != 64 or any(c not in "0123456789abcdef" for c in rec["sha256"]):
            raise MaterialError(f"{where}: sha256 is not 64 lowercase hex characters")
        kinds = _sexp.children(m, "kind")
        rec["kind"] = str(kinds[0][1]) if kinds else "document"
        if rec["kind"] not in KINDS:
            raise MaterialError(f"{where}: kind {rec['kind']!r} is not one of {', '.join(KINDS)}")
        if rec["kind"] == "snapshot":
            man = _sexp.children(m, "manifest")
            if not man:
                raise MaterialError(
                    f"{where}: a snapshot must name its (manifest …). Without one its sha256 "
                    f"would identify a single page and say nothing about the other 71.")
            rec["manifest"] = _relative("manifest", str(man[0][1]), where)
        materials[mid] = rec
    if not materials:
        raise MaterialError(f"{path}: declares no material")
    return {"cache_root": cache_root, "corpora": corpora, "materials": materials, "path": path}


def _digest(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve(cat: dict, mid: str, repo: Path | None = None) -> str:
    """The repo-root-relative path of a cached material, or a refusal that says what to run."""
    repo = repo or REPO
    if mid not in cat["materials"]:
        raise MaterialError(f"unknown material {mid!r}. Declared: "
                            f"{', '.join(sorted(cat['materials']))}")
    rec = cat["materials"][mid]
    rel = f"{cat['cache_root']}/{rec['cache_path']}"
    full = repo / rel
    probe = full / rec["manifest"] if rec["kind"] == "snapshot" else full
    if not probe.exists():
        env = cat["corpora"][rec["corpus"]]["env_var"]
        raise MaterialError(
            f"{mid}: not in the local cache at {rel}. The cache is gitignored, so an empty one is "
            f"the normal state of a fresh clone, not a fault. Populate it:\n"
            f"    export {env}=<path to the {rec['corpus']} checkout>\n"
            f"    scripts/materials.py --fetch {mid}")
    got = _digest(probe)
    if got != rec["sha256"]:
        raise MaterialError(
            f"{mid}: the cached copy at {rel} is NOT the catalogued "
            f"{'snapshot (its manifest differs)' if rec['kind'] == 'snapshot' else 'document'}.\n"
            f"    catalogued sha256 {rec['sha256']}\n"
            f"    cached     sha256 {got}\n"
            f"A material is identified by its digest, not by its filename. Re-fetch it, or if the "
            f"document genuinely changed, update the catalogue in a leaf that says why.")
    return rel


def _verify_manifest(root: Path, manifest: str) -> tuple[int, int]:
    """Check every entry of a `shasum`-style manifest. Returns (checked, failed)."""
    n = bad = 0
    for line in (root / manifest).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        digest, _, name = line.partition("  ")
        if not name:
            continue
        n += 1
        f = root / name.lstrip("*").strip()
        if not f.exists() or _digest(f) != digest.strip():
            bad += 1
    return n, bad


def corpus_drift(cat: dict) -> list[str]:
    """⛔ The corpus is a MOVING repository, and the catalogue pins one revision of it. A path that
    moved upstream is the failure this reports: the digests still protect the BYTES, but nothing
    else notices that the record now describes a layout that is gone."""
    import subprocess
    out = []
    for cid, c in sorted(cat["corpora"].items()):
        root = os.environ.get(c["env_var"])
        if not root:
            continue
        try:
            at = subprocess.run(["git", "-C", root, "rev-parse", "--short", "HEAD"],
                                capture_output=True, text=True, timeout=15)
        except OSError:
            continue
        head = at.stdout.strip()
        if head and head != c["revision"]:
            out.append(f"corpus {cid!r}: catalogued at {c['revision']}, checkout is at {head}. "
                       f"Digests still protect the bytes, but a path that MOVED upstream will "
                       f"only show up as a failed --fetch. Re-derive the catalogue.")
    return out


def fetch(cat: dict, ids: list[str], repo: Path | None = None) -> int:
    import shutil
    repo = repo or REPO
    rc = 0
    for mid in ids or sorted(cat["materials"]):
        rec = cat["materials"][mid]
        corpus = cat["corpora"][rec["corpus"]]
        root = os.environ.get(corpus["env_var"])
        if not root:
            print(f"  REFUSED {mid}: ${corpus['env_var']} is not set. This repository does not "
                  f"store the corpus location, by design (Policy 12); the operator supplies it.",
                  file=sys.stderr)
            rc = 1; continue
        src = Path(root) / rec["corpus_path"]
        if not src.exists():
            print(f"  REFUSED {mid}: not at ${corpus['env_var']}/{rec['corpus_path']}", file=sys.stderr)
            rc = 1; continue
        dst = repo / cat["cache_root"] / rec["cache_path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        if rec["kind"] == "snapshot":
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            probe = dst / rec["manifest"]
        else:
            shutil.copy2(src, dst)
            probe = dst
        got = _digest(probe)
        if got != rec["sha256"]:
            shutil.rmtree(dst) if rec["kind"] == "snapshot" else dst.unlink()
            print(f"  REFUSED {mid}: copied, digest {got[:16]}… != catalogued "
                  f"{rec['sha256'][:16]}…; the copy was removed rather than kept", file=sys.stderr)
            rc = 1; continue
        extra = ""
        if rec["kind"] == "snapshot":
            n, bad = _verify_manifest(dst, rec["manifest"])
            if bad:
                shutil.rmtree(dst)
                print(f"  REFUSED {mid}: {bad} of {n} manifest entries do not verify; the copy "
                      f"was removed rather than kept", file=sys.stderr)
                rc = 1; continue
            extra = f", {n} manifest entries verified"
        print(f"  ok      {mid}  -> {cat['cache_root']}/{rec['cache_path']}  "
              f"({int(rec['bytes']):,} B, sha256 verified{extra})")
    return rc


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[1] == "--self-test":
        return _selftest()
    try:
        cat = load()
        if len(argv) == 1 or argv[1] == "--list":
            print(f"{CATALOG}: {len(cat['materials'])} material(s), cache root "
                  f"{cat['cache_root']}/ (gitignored)")
            for d in corpus_drift(cat):
                print(f"  \u26a0\ufe0f  {d}")
            for mid, rec in sorted(cat["materials"].items()):
                try:
                    where = resolve(cat, mid)
                    state = f"cached  {where}"
                except MaterialError:
                    state = "absent  (scripts/materials.py --fetch)"
                print(f"  {mid:24} {str(rec['licence']):12} {state}")
            return 0
        if argv[1] == "--resolve" and len(argv) == 3:
            print(resolve(cat, argv[2])); return 0
        if argv[1] == "--fetch":
            return fetch(cat, argv[2:])
        if argv[1] == "--verify":
            bad = 0
            for mid in sorted(cat["materials"]):
                try:
                    resolve(cat, mid); print(f"  ok      {mid}")
                except MaterialError as exc:
                    print(f"  {exc}", file=sys.stderr); bad += 1
            drift = corpus_drift(cat)
            for d in drift:
                print(f"  \u26a0\ufe0f  {d}", file=sys.stderr)
            print(f"materials --verify: {len(cat['materials']) - bad} verified / {bad} unresolved"
                  f"{f' / {len(drift)} corpus revision drift' if drift else ''}")
            return 1 if bad else 0
    except (MaterialError, _sexp.SexpError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr); return 1
    print("usage: materials.py [--list | --resolve <id> | --fetch [<id>…] | --verify | --self-test]",
          file=sys.stderr)
    return 2


# ---------------------------------------------------------------------------------------
# Self-test. Every arm below is about the SAME property: a path this project records must stay
# meaningful after the repository is moved. The arms that matter are the RED ones.
# ---------------------------------------------------------------------------------------
def _selftest() -> int:
    import tempfile, textwrap
    passed = failed = 0

    def arm(label: str, fn) -> None:
        nonlocal passed, failed
        try:
            fn()
        except AssertionError as exc:
            print(f"  FAIL  {label}: {exc}"); failed += 1
        except Exception as exc:                        # noqa: BLE001
            print(f"  FAIL  {label}: unexpected {type(exc).__name__}: {exc}"); failed += 1
        else:
            print(f"  ok    {label}"); passed += 1

    GOOD = textwrap.dedent('''\
        (materials
          (schema-version 1) (cache-root ".materials")
          (corpus (id "c") (title "t") (kind git-repository) (revision "r") (env-var "X_ROOT"))
          (material (id "M1") (title "t") (revision "1") (licence "CC-BY-4.0") (corpus "c")
                    (corpus-path "a/b.pdf") (cache-path "a/b.pdf")
                    (sha256 "%s") (bytes 3)))
        ''')
    D3 = hashlib.sha256(b"abc").hexdigest()

    def written(text: str) -> Path:
        d = Path(tempfile.mkdtemp()); (d / "materials").mkdir()
        (d / "materials" / "catalog.sexp").write_text(text)
        return d

    def refuses(text: str, needle: str) -> None:
        try:
            load(written(text) / "materials" / "catalog.sexp")
        except MaterialError as exc:
            assert needle in str(exc), f"refused for the wrong reason: {exc}"
        else:
            raise AssertionError(f"accepted a catalogue it must refuse ({needle})")

    arm("GREEN a well-formed catalogue loads", lambda: (
        lambda c: None if len(c["materials"]) == 1 else (_ for _ in ()).throw(
            AssertionError("expected 1 material")))(load(written(GOOD % D3) / "materials" / "catalog.sexp")))

    arm("RED   an ABSOLUTE cache-path is refused",
        lambda: refuses(GOOD.replace('(cache-path "a/b.pdf")', '(cache-path "/Volumes/SSD/b.pdf")') % D3,
                        "is ABSOLUTE"))
    arm("RED   an ABSOLUTE corpus-path is refused",
        lambda: refuses(GOOD.replace('(corpus-path "a/b.pdf")', '(corpus-path "/opt/x/b.pdf")') % D3,
                        "is ABSOLUTE"))
    arm("RED   an ABSOLUTE cache-root is refused",
        lambda: refuses(GOOD.replace('(cache-root ".materials")', '(cache-root "/var/cache")') % D3,
                        "is ABSOLUTE"))
    arm("RED   a cache-path climbing out with '..' is refused",
        lambda: refuses(GOOD.replace('(cache-path "a/b.pdf")', '(cache-path "../../b.pdf")') % D3,
                        "escapes its root"))
    DUP = (GOOD % D3).rstrip()[:-1] + (
        f'  (material (id "M1") (title "other") (revision "2") (licence "l") (corpus "c")\n'
        f'            (corpus-path "c/d.pdf") (cache-path "c/d.pdf")\n'
        f'            (sha256 "{D3}") (bytes 9)))\n')
    arm("RED   a duplicated material id is refused", lambda: refuses(DUP, "declared twice"))
    arm("RED   a missing required field is refused",
        lambda: refuses(GOOD.replace('(licence "CC-BY-4.0") ', "") % D3, "missing required field"))
    arm("RED   a corpus that is not declared is refused",
        lambda: refuses(GOOD.replace('(corpus "c")', '(corpus "nope")') % D3, "not declared"))
    arm("RED   a sha256 that is not 64 hex is refused",
        lambda: refuses(GOOD % "abc", "not 64 lowercase hex"))
    arm("RED   a catalogue with no material is refused", lambda: refuses(
        '(materials (schema-version 1) (cache-root ".materials") '
        '(corpus (id "c") (title "t") (kind git-repository) (revision "r") (env-var "X")))',
        "declares no material"))

    # --- snapshots: a material that is a directory is identified by its manifest, not a page
    SNAP = textwrap.dedent('''\
        (materials
          (schema-version 1) (cache-root ".materials")
          (corpus (id "c") (title "t") (kind git-repository) (revision "r") (env-var "X_ROOT"))
          (material (id "S1") (title "t") (revision "1") (licence "l") (corpus "c") (kind snapshot)
                    %s (corpus-path "snap") (cache-path "snap")
                    (sha256 "%s") (bytes 3)))
        ''')
    arm("RED   a snapshot with no (manifest …) is refused",
        lambda: refuses(SNAP % ("", D3), "must name its (manifest"))
    arm("RED   an unknown material kind is refused",
        lambda: refuses(SNAP.replace("(kind snapshot)", "(kind tarball)") % ('(manifest "M")', D3),
                        "is not one of"))
    arm("RED   a snapshot manifest path that is absolute is refused",
        lambda: refuses(SNAP % ('(manifest "/etc/M")', D3), "is ABSOLUTE"))

    def snapshot_ok() -> None:
        d = written(SNAP % ('(manifest "SHA256SUMS")', hashlib.sha256(
            b"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad  a.txt\n").hexdigest()))
        s = d / ".materials" / "snap"; s.mkdir(parents=True)
        (s / "a.txt").write_bytes(b"abc")
        (s / "SHA256SUMS").write_bytes(
            b"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad  a.txt\n")
        cat = load(d / "materials" / "catalog.sexp")
        assert resolve(cat, "S1", repo=d) == ".materials/snap", "snapshot did not resolve"
        n, bad = _verify_manifest(s, "SHA256SUMS")
        assert (n, bad) == (1, 0), f"manifest check gave {(n, bad)}"
    arm("GREEN a snapshot resolves through its manifest, and the manifest verifies", snapshot_ok)

    def snapshot_tampered() -> None:
        d = written(SNAP % ('(manifest "SHA256SUMS")', hashlib.sha256(
            b"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad  a.txt\n").hexdigest()))
        s = d / ".materials" / "snap"; s.mkdir(parents=True)
        (s / "a.txt").write_bytes(b"TAMPERED")
        (s / "SHA256SUMS").write_bytes(
            b"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad  a.txt\n")
        n, bad = _verify_manifest(s, "SHA256SUMS")
        assert (n, bad) == (1, 1), f"a tampered page passed the manifest check: {(n, bad)}"
    arm("RED   a tampered page inside a verifying snapshot is caught", snapshot_tampered)

    # --- resolution: absence and mismatch are different refusals, and both name the fix
    def absent() -> None:
        d = written(GOOD % D3)
        try:
            resolve(load(d / "materials" / "catalog.sexp"), "M1", repo=d)
        except MaterialError as exc:
            assert "--fetch" in str(exc), f"refusal does not name the populate command: {exc}"
            assert "X_ROOT" in str(exc), f"refusal does not name the environment variable: {exc}"
        else:
            raise AssertionError("resolved a material that is not cached")
    arm("RED   an absent material refuses WITH the command that fixes it", absent)

    def mismatch() -> None:
        d = written(GOOD % D3)
        f = d / ".materials" / "a"; f.mkdir(parents=True)
        (f / "b.pdf").write_bytes(b"not abc")
        try:
            resolve(load(d / "materials" / "catalog.sexp"), "M1", repo=d)
        except MaterialError as exc:
            assert "NOT the catalogued document" in str(exc), f"wrong reason: {exc}"
        else:
            raise AssertionError("accepted a cached file whose digest disagrees")
    arm("RED   a cached file with the wrong digest is refused", mismatch)

    def good_resolve() -> None:
        d = written(GOOD % D3)
        f = d / ".materials" / "a"; f.mkdir(parents=True)
        (f / "b.pdf").write_bytes(b"abc")
        got = resolve(load(d / "materials" / "catalog.sexp"), "M1", repo=d)
        assert got == ".materials/a/b.pdf", f"got {got!r}"
        assert not got.startswith("/"), "resolve returned an absolute path"
    arm("GREEN resolve returns a REPO-ROOT-RELATIVE path", good_resolve)

    arm("RED   an unknown material id is refused", lambda: (
        lambda c: (_ for _ in ()).throw(AssertionError("resolved an id that does not exist"))
        if _try_resolve(c, "NOPE") else None)(load(written(GOOD % D3) / "materials" / "catalog.sexp")))

    # --- the real catalogue must itself obey every rule above
    arm("GREEN the tracked catalogue loads and declares materials", lambda: (
        lambda c: None if c["materials"] else (_ for _ in ()).throw(AssertionError("empty")))(load()))

    print(f"materials --self-test: {passed} pass / {failed} fail")
    return 1 if failed else 0


def _try_resolve(cat: dict, mid: str) -> bool:
    try:
        resolve(cat, mid); return True
    except MaterialError:
        return False


if __name__ == "__main__":
    sys.exit(main(sys.argv))

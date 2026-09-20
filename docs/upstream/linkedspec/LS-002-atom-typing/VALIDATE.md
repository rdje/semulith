# LS-002 — how to reproduce

| Path | What it is |
| --- | --- |
| `REPORT.md` | the finding and why a consumer may care |
| `repro.sh` | prints the four values side by side |
| `cases/*.sexp` | bare and quoted forms of a numeric and a version |
| `evidence/shipped.txt` | our captured run at pin `ad290bdb4` |

```sh
bash repro.sh "$CARGO_TARGET_DIR/debug/lispish_file" specs/Lispish.spec
```

Expected: the bare and quoted forms print the **same** value, and the script says so.

⚠️ There is nothing to validate here, because there is no fix proposed. This issue exists to put
the consequence of a documented behaviour on the record, and to ask whether a token-kind channel
belongs beside the strict-document work you already track. Both possible answers — "yes, tracked"
and "no, use a schema" — close it.

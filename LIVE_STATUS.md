# LIVE_STATUS.md — authoritative live progress tracker

Rows use ONLY these four states: **Done · Mostly Done · In Progress · Not Started**.
Review and update before every commit whenever actual closure or remaining scope changes;
summarize the snapshot in every commit-workflow completion message.

## Foundation

| Area | Status | Notes |
| --- | --- | --- |
| Discipline spine (`bedrock` 0.6.1) | Done | memory architecture · task-trees · commit workflow · doctrine enforcement · mdBook skeleton |
| Planning package v0.2 ingested | In Progress | `SEMULITH-PKG` — docs landed; live-fingerprint gates and book sync pending |
| Roadmap converted to task-trees | Not Started | `SEMULITH-TREES` — P0–P7 plus the cross-cutting lanes |

## Roadmap milestones (`ROADMAP.md` §6)

| Milestone | Gate | Status | Notes |
| --- | --- | --- | --- |
| P0 — profile and evidence access | G0 | Not Started | select `rv64i-lab-v0`; prove a real reference path |
| P1 — processor laboratory | G1 | Not Started | `semulith-core` / `-verify` / `-cli`; graph + evidence checker |
| P2 — validated RV64I profile | CPU-LAB | Not Started | — |
| DSP specification and stress review | — | Not Started | — |
| P3 — shared interfaces + real DSP slice | BREADTH | Not Started | — |
| P4 — Linux CPU profile | CPU-SYSTEM | Not Started | — |
| P5 — board model | BOARD | Not Started | — |
| archogen OS integration | ARCHOGEN-OS | Not Started | — |
| P6 — Linux userspace | LINUX | Not Started | — |
| P7 — useful headless computer | SYSTEM | Not Started | — |
| Separate multicore CPU work | multicore gate | Not Started | — |

No gate has been run. Every row above is project state, not a conformance claim.

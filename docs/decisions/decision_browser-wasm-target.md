# The browser is a first-class target: JS + Wasm, not a late port

- **Type:** `decision`
- **Date:** `2026-09-27`
- **Status:** `active`
- **Owner / source:** director vision, stated in conversation `2026-09-27`: *"one of my
  vision with SEMULITH will also be able to run everything in the browser (JS + Wasm)"*

## The fact / decision

Every Semulith model must be able to run in the browser. JS + Wasm is a first-class
delivery target from the start, not a port attempted after the fact. The engine remains
Rust compiled to `wasm32`; nothing is rewritten in JavaScript.

## Why

The dual mandate ([[decision_dual-mandate-production-and-teaching]]) wants a student to run
models anywhere; a browser target removes every install barrier and turns the per-model
mdBook into a live demo. The architecture already points the same way: the execution
authority is the data-driven interpreter ([[decision_interpreter-before-compiler]]), and a
definitional interpreter over declared data is the construct that ports to Wasm cleanly —
no JIT, no host code generation, no FFI. Host-native stays a build mode; the Wasm target
keeps the engine honest about dependencies (no hidden host OS calls, no off-volume paths).

## How to apply

- The constraint lands earliest at P1: `P1-LAB`'s crate skeleton builds for
  `wasm32-unknown-unknown` from its first slice (owned by the `PORT-WEB` tree's leaf `.1`,
  [`docs/tasks/PORT-WEB.md`](../tasks/PORT-WEB.md), consumed by `P1-LAB` per
  [[decision_lane-consumption]]).
- Engine code avoids std-only APIs that have no Wasm path (filesystem, processes, threads
  as host assumptions); where a capability genuinely needs the host, it goes behind an
  explicit feature gate with the Wasm build proving the seam.
- The Python doctrine/tooling layer stays host-side: it is build-time and review-time
  machinery, never part of what ships to the browser.
- Later leaves own the browser harness (a JS/Wasm runner the mdBook can embed) and, much
  later, archogen-in-browser demos. Do not pull those forward; the build target comes
  first.

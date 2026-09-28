#!/usr/bin/env node
// scripts/smoke_bench.js — headless verification of the browser bench's engine (LAB-BENCH.1,
// acceptance 3). The page cannot be clicked in a commit gate, so this script instantiates the
// same wasm module the page imports and asserts, over the wire-exact exports, what the page
// would show:
//   - every guest under 'none' meets the pinned expectations AND the crossing census;
//   - each exposed mutant is detected exactly where the P1-LAB.9 suite pins it
//     (zext-addi @ 1, jal-no-link @ 7, jalr-odd-bit @ 10; phantom-load agrees at the trace
//     level and is caught by the census instead: 7 crossings where 0 are pinned).
// Run after scripts/build_bench.sh. Exit 0 — all arms pass; 1 — a discrepancy, named.

"use strict";

const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const wasmPath = path.join(root, "bench", "semulith_verify.wasm");

function fail(why) {
  console.error(`smoke_bench: FAIL — ${why}`);
  process.exit(1);
}

async function main() {
  if (!fs.existsSync(wasmPath)) {
    fail("bench/semulith_verify.wasm is absent — run scripts/build_bench.sh first");
  }
  const { instance } = await WebAssembly.instantiate(fs.readFileSync(wasmPath), {});
  const ex = instance.exports;
  const read = (ptr) => {
    if (ptr === 0) return null;
    const bytes = new Uint8Array(ex.memory.buffer, ptr);
    let end = 0;
    while (bytes[end] !== 0) end += 1;
    return new TextDecoder().decode(bytes.subarray(0, end));
  };
  const run = (guest, mutation) => {
    const text = read(ex.bench_run_guest(guest, mutation));
    const data = JSON.parse(text);
    if (data.error) fail(`bench_run_guest(${guest}, ${mutation}): ${data.error}`);
    return data;
  };

  const guests = [];
  for (let i = 0; i < ex.bench_guest_count(); i += 1) {
    guests.push(read(ex.bench_guest_name(i)));
  }
  const mutations = [];
  for (let i = 0; i < ex.bench_mutation_count(); i += 1) {
    mutations.push(read(ex.bench_mutation_name(i)));
  }
  const none = mutations.indexOf("none");
  if (none < 0) fail("the 'none' model is not exposed");

  let arms = 0;
  for (const name of guests) {
    const g = guests.indexOf(name);
    const clean = run(g, none);
    if (!clean.expectations_met) fail(`${name}: clean run must meet the pinned expectations`);
    if (!clean.census_met) {
      fail(`${name}: clean run must meet the census (${clean.data_crossings} vs pinned ${clean.data_crossings_pinned})`);
    }
    if (clean.divergence !== null) fail(`${name}: clean run must not diverge from itself`);
    arms += 1;
  }

  const divergences = [
    ["guest-control", "zext-addi", 1],
    ["guest-control", "jal-no-link", 7],
    ["guest-control", "jalr-odd-bit", 10],
  ];
  for (const [guest, mutation, at] of divergences) {
    const data = run(guests.indexOf(guest), mutations.indexOf(mutation));
    if (data.expectations_met) fail(`${mutation}: the anchor must break`);
    if (!data.census_met) fail(`${mutation}: the census must stay intact`);
    if (!data.divergence || data.divergence.at !== at) {
      fail(`${mutation}: divergence at ${data.divergence ? data.divergence.at : "none"}, the .9 suite pins ${at}`);
    }
    arms += 1;
  }

  const phantom = run(guests.indexOf("guest-control"), mutations.indexOf("phantom-load"));
  if (!phantom.expectations_met) fail("phantom-load: the architectural trace must still agree");
  if (phantom.divergence !== null) fail("phantom-load: no trace-level divergence is the point");
  if (phantom.census_met || phantom.data_crossings !== 7 || phantom.data_crossings_pinned !== 0) {
    fail(`phantom-load: caught by the census — 7 crossings vs pinned 0, got ${phantom.data_crossings} vs ${phantom.data_crossings_pinned}`);
  }
  arms += 1;

  console.log(`smoke_bench: ok (${arms} arms — clean ${guests.length}, ${divergences.length} trace-level mutants, the census arm)`);
}

main().catch((error) => fail(error));

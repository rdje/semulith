// bench/main.js — the laboratory bench page (LAB-BENCH.1). Imports the std-only wasm module
// (scripts/build_bench.sh copies it here), runs the chosen guest under the clean and the
// mutated model, and renders both traces with the first divergence highlighted. No framework,
// no build step: this file is the whole client.

"use strict";

const state = { exports: null, stories: {} };

async function load() {
  const response = await fetch("semulith_verify.wasm");
  if (!response.ok) {
    throw new Error(`semulith_verify.wasm: ${response.status} — run scripts/build_bench.sh first`);
  }
  const { instance } = await WebAssembly.instantiate(await response.arrayBuffer(), {});
  state.exports = instance.exports;
  const read = (ptr) => {
    const bytes = new Uint8Array(instance.exports.memory.buffer, ptr);
    let end = 0;
    while (bytes[end] !== 0) end += 1;
    return new TextDecoder().decode(bytes.subarray(0, end));
  };
  state.read = read;

  const guest = document.getElementById("guest");
  for (let i = 0; i < state.exports.bench_guest_count(); i += 1) {
    const name = read(state.exports.bench_guest_name(i));
    guest.append(new Option(name, i));
  }
  const mutation = document.getElementById("mutation");
  for (let i = 0; i < state.exports.bench_mutation_count(); i += 1) {
    const name = read(state.exports.bench_mutation_name(i));
    mutation.append(new Option(name, i));
    state.stories[name] = read(state.exports.bench_mutation_story(i));
  }
  document.getElementById("run").addEventListener("click", run);
  guest.addEventListener("change", run);
  mutation.addEventListener("change", () => {
    document.getElementById("mutation-story").textContent =
      state.stories[mutation.selectedOptions[0].textContent] || "";
    run();
  });
  document.getElementById("mutation-story").textContent =
    state.stories[mutation.selectedOptions[0].textContent] || "";
  run();
}

function runGuest(index, mutation) {
  const json = state.read(state.exports.bench_run_guest(index, mutation));
  return JSON.parse(json);
}

function render(table, data, divergedAt) {
  table.replaceChildren();
  for (const step of data.trace) {
    const row = table.appendChild(document.createElement("tr"));
    if (step.n === divergedAt) row.classList.add("diverged");
    const notes = [];
    for (const [reg, value] of step.writes) notes.push(`x${reg} &larr; ${value}`);
    if (step.trap) notes.push(`trap cause=${step.trap.cause} tval=${step.trap.tval}`);
    row.innerHTML =
      `<td>${step.n}</td><td>${step.pc}</td><td>(${step.word})</td>` +
      `<td>${step.insn}</td><td class="notes">${notes.join("; ")}</td>`;
  }
}

function run() {
  const guest = Number(document.getElementById("guest").value);
  const mutationIndex = Number(document.getElementById("mutation").value);
  const mutationName = document.getElementById("mutation").selectedOptions[0].textContent;
  const clean = runGuest(guest, 0);
  const mutated = mutationName === "none" ? clean : runGuest(guest, mutationIndex);

  render(document.getElementById("clean"), clean, null);
  render(document.getElementById("mut"), mutated, mutated.divergence ? mutated.divergence.at : null);
  document.getElementById("mut-title").textContent =
    mutationName === "none" ? "same trace (no mutation selected)" : `trace under '${mutationName}'`;

  const verdict = document.getElementById("verdict");
  const messages = [];
  if (!mutated.expectations_met) messages.push("pinned expectations BROKEN");
  if (!mutated.census_met) {
    messages.push(
      `crossing census DISAGREES — ${mutated.data_crossings} data crossing(s) where the source pins ${mutated.data_crossings_pinned} (the trace never betrayed it)`,
    );
  }
  if (mutated.divergence) {
    messages.push(`first divergence at aligned step ${mutated.divergence.at}: ${mutated.divergence.what}`);
  }
  if (messages.length === 0) {
    verdict.className = "ok";
    verdict.textContent =
      `${clean.guest}: the pinned specification-derived expectations hold; the crossing census agrees.`;
  } else {
    verdict.className = "bad";
    verdict.textContent = messages.join("  —  ");
  }
}

load().catch((error) => {
  const verdict = document.getElementById("verdict");
  verdict.className = "bad";
  verdict.textContent = String(error);
});

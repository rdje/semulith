//! The browser bench's wasm exports — `LAB-BENCH.1`. Std-only `extern "C"` surface: the page
//! (`bench/index.html`) imports the module this file compiles into and calls these five
//! functions; there is no wasm-bindgen and no foreign dependency (RUST-01). The engine behind
//! every export is the same `run`/`mutate` code the commit gate tests — the bench re-implements
//! nothing.
//!
//! String results are NUL-terminated and leaked: the bench page lives for one browser session
//! and calls each function a handful of times, so a free protocol would be ceremony without a
//! beneficiary.
//!
//! - `bench_guest_count() -> usize` — how many tracked guests exist.
//! - `bench_guest_name(i) -> *const c_char` — the guest's name (NUL-terminated).
//! - `bench_mutation_count() -> usize` — how many named models exist (see `mutate::MUTATIONS`).
//! - `bench_mutation_name(i) -> *const c_char` — the mutation's name.
//! - `bench_mutation_story(i) -> *const c_char` — the mutation's one-line story for the page.
//! - `bench_run_guest(guest, mutation) -> *mut c_char` — `report::to_json` of the run, or a
//!   JSON `{"error": …}` object naming the reason a run could not be judged.

use std::os::raw::c_char;

use crate::guests::GUESTS;
use crate::mutate::MUTATIONS;
use crate::report;

/// Leak a NUL-terminated copy of `s` — see the module docs for why leaking is right here.
fn leaked_cstr(s: &str) -> *mut c_char {
    let mut bytes = s.as_bytes().to_vec();
    bytes.push(0);
    let leaked: &'static mut [u8] = Box::leak(bytes.into_boxed_slice());
    leaked.as_mut_ptr().cast::<c_char>()
}

#[no_mangle]
pub extern "C" fn bench_guest_count() -> usize {
    GUESTS.len()
}

#[no_mangle]
pub extern "C" fn bench_guest_name(index: usize) -> *const c_char {
    match GUESTS.get(index) {
        Some(guest) => leaked_cstr(guest.name),
        None => std::ptr::null(),
    }
}

#[no_mangle]
pub extern "C" fn bench_mutation_count() -> usize {
    MUTATIONS.len()
}

#[no_mangle]
pub extern "C" fn bench_mutation_name(index: usize) -> *const c_char {
    match MUTATIONS.get(index) {
        Some((name, _)) => leaked_cstr(name),
        None => std::ptr::null(),
    }
}

#[no_mangle]
pub extern "C" fn bench_mutation_story(index: usize) -> *const c_char {
    match MUTATIONS.get(index) {
        Some((_, story)) => leaked_cstr(story),
        None => std::ptr::null(),
    }
}

#[no_mangle]
pub extern "C" fn bench_run_guest(guest: usize, mutation: usize) -> *mut c_char {
    let json = match (GUESTS.get(guest), MUTATIONS.get(mutation)) {
        (Some(g), Some((m, _))) => match report::run_guest(g.name, m) {
            Ok(run) => report::to_json(&run),
            Err(why) => format!("{{\"error\":\"{why}\"}}"),
        },
        _ => "{\"error\":\"unknown guest or mutation index\"}".to_string(),
    };
    leaked_cstr(&json)
}

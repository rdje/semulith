//! The M extension's instruction vectors (`P4-SYSTEM.11` slice c1): the generated table
//! (`m_vectors/vectors.txt`, emitted by `scripts/gen_m_vectors.py` and gated by M-VECTORS) run
//! through the ENGINE — each vector's word decoded by the generated rv64gc table, its
//! `m.sem.sexp` rule evaluated with its zero-divisor guard, its operators at their width. The
//! expected values are the generator's exact-integer reference (RVI-M §11.1, Table 1 tested by
//! name), never the engine's arithmetic; the instruction words are built here from the
//! chapter's R-type layout, independently of the generated decode table.

#[cfg(test)]
mod tests;

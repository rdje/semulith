//! Every generated M vector, one instruction at a time, through `exec_rv64gc::step`.

use crate::fixtures::FlatMemory;
use semulith_core::exec_rv64gc::{step, StepRv64gc};
use semulith_core::state_rv64gc::ArchitecturalState;

const VECTORS: &str = include_str!("vectors.txt");
const ENTRY: u64 = 0x8000_0000;

/// `mn x3, x1, x2` — the R-type layout with funct7 = 1, OP (0x33) or OP-32 (0x3b) for the
/// word forms (RVI-M §11.1; the rv_m/rv64_m rows), built here rather than read from the
/// generated table, so a decode defect cannot hide behind its own encoding.
fn word(mn: &str) -> u32 {
    let (funct3, opcode) = match mn {
        "mul" => (0, 0x33),
        "mulh" => (1, 0x33),
        "mulhsu" => (2, 0x33),
        "mulhu" => (3, 0x33),
        "div" => (4, 0x33),
        "divu" => (5, 0x33),
        "rem" => (6, 0x33),
        "remu" => (7, 0x33),
        "mulw" => (0, 0x3b),
        "divw" => (4, 0x3b),
        "divuw" => (5, 0x3b),
        "remw" => (6, 0x3b),
        "remuw" => (7, 0x3b),
        other => panic!("no M instruction named {other}"),
    };
    (1 << 25) | (2 << 20) | (1 << 15) | (funct3 << 12) | (3 << 7) | opcode
}

fn hex(field: &str) -> u64 {
    u64::from_str_radix(field, 16).unwrap_or_else(|e| panic!("{field}: {e}"))
}

#[test]
fn every_generated_vector_holds_through_the_engine() {
    // the table states its own size; a run that read fewer lines judged less than it claims
    let declared: usize = VECTORS
        .lines()
        .find_map(|l| {
            l.strip_prefix("# ")?
                .split_once(" vectors over ")?
                .0
                .parse()
                .ok()
        })
        .expect("the table's header states its vector count");
    let mut judged = 0;
    for line in VECTORS
        .lines()
        .filter(|l| !l.is_empty() && !l.starts_with('#'))
    {
        let f: Vec<&str> = line.split(' ').collect();
        assert_eq!(f.len(), 4, "a vector is `mnemonic rs1 rs2 rd`: {line}");
        let (a, b, want) = (hex(f[1]), hex(f[2]), hex(f[3]));
        let mut memory = FlatMemory::new(ENTRY, 4096);
        memory.load_image(0, &word(f[0]).to_le_bytes());
        let mut state = ArchitecturalState::zeroed_at(ENTRY);
        state.write_x(1, a);
        state.write_x(2, b);
        let outcome = step(&mut state, &mut memory);
        assert_eq!(outcome, StepRv64gc::Executed, "{line}");
        assert_eq!(
            state.read_x(3),
            want,
            "{line}: rd {:#x}, the reference {want:#x}",
            state.read_x(3)
        );
        assert_eq!(
            state.pc(),
            ENTRY + 4,
            "{line}: no M instruction traps — the next pc"
        );
        judged += 1;
    }
    assert_eq!(judged, declared, "the table's vectors, every one judged");
}

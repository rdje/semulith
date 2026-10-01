//! The canonical end-state dump — byte-compatible vocabulary with the reference harness's
//! `difftest corpus` output (`tools/difftest/README.md` at the pinned commit), so the
//! comparator can treat both engines identically. Register lines in the harness's order,
//! then optional deviation-encoded memory and stack dumps. This model emits NO `cyc`
//! line: cycle counts are informational upstream (LIMITATIONS §4) and no timing is
//! modelled here — the comparator skips `cyc` by recorded rule.

use crate::machine::{
    Machine, ResetImage, P_DUMP_FROM, P_WORDS, STACK_LEVELS, X_HARNESS_FROM, X_HARNESS_TO, X_WORDS,
    Y_WORDS,
};

fn reg_line(out: &mut String, name: &str, value: u32) {
    out.push_str(&format!("{name} {value:06x}\n"));
}

/// The register block, in the reference harness's field order.
pub fn dump_registers(out: &mut String, m: &Machine) {
    out.push_str(&format!("steps {}\n", m.steps));
    reg_line(out, "pc", m.pc);
    reg_line(out, "sr", m.sr);
    reg_line(out, "omr", m.omr);
    reg_line(out, "la", m.la);
    reg_line(out, "lc", m.lc);
    reg_line(out, "sp", m.sp);
    reg_line(out, "ssh", m.ssh());
    reg_line(out, "ssl", m.ssl());
    reg_line(out, "ep", m.ep);
    reg_line(out, "sz", m.sz);
    reg_line(out, "sc", m.sc);
    reg_line(out, "vba", m.vba);
    reg_line(out, "x0", m.x0);
    reg_line(out, "x1", m.x1);
    reg_line(out, "y0", m.y0);
    reg_line(out, "y1", m.y1);
    reg_line(out, "a0", (m.a & 0xFF_FFFF) as u32);
    reg_line(out, "a1", ((m.a >> 24) & 0xFF_FFFF) as u32);
    reg_line(out, "a2", ((m.a >> 48) & 0xFF) as u32);
    reg_line(out, "b0", (m.b & 0xFF_FFFF) as u32);
    reg_line(out, "b1", ((m.b >> 24) & 0xFF_FFFF) as u32);
    reg_line(out, "b2", ((m.b >> 48) & 0xFF) as u32);
    for i in 0..8 {
        reg_line(out, &format!("r{i}"), m.r[i]);
    }
    for i in 0..8 {
        reg_line(out, &format!("n{i}"), m.n[i]);
    }
    for i in 0..8 {
        reg_line(out, &format!("m{i}"), m.m[i]);
    }
}

/// The `--dump-mem` deviation lines: the words inside the sanctioned windows that differ
/// from the init image, as `xm<addr4hex>` / `ym<addr4hex>` / `pm<addr4hex>` (the harness's
/// X window excludes its private $0400-$04FF span; P compares $07C0-$07FF against the
/// loaded image).
pub fn dump_memory_deviations(out: &mut String, m: &Machine, init: &ResetImage) {
    for addr in 0..X_WORDS {
        if (X_HARNESS_FROM..=X_HARNESS_TO).contains(&addr) {
            continue;
        }
        if m.x[addr] != init.x[addr] {
            out.push_str(&format!("xm{addr:04x} {:06x}\n", m.x[addr]));
        }
    }
    for addr in 0..Y_WORDS {
        if m.y[addr] != init.y[addr] {
            out.push_str(&format!("ym{addr:04x} {:06x}\n", m.y[addr]));
        }
    }
    for addr in P_DUMP_FROM..P_WORDS {
        if m.p[addr] != init.p[addr] {
            out.push_str(&format!("pm{addr:04x} {:06x}\n", m.p[addr]));
        }
    }
}

/// The `--dump-stack` deviation lines: stack slots 1-15 against their zero seed, as
/// `sh<slot2>` / `sl<slot2>`.
pub fn dump_stack_deviations(out: &mut String, m: &Machine) {
    for slot in 1..STACK_LEVELS {
        let [hi, lo] = m.stack_slots()[slot];
        if hi != 0 {
            out.push_str(&format!("sh{slot:02} {hi:06x}\n"));
        }
        if lo != 0 {
            out.push_str(&format!("sl{slot:02} {lo:06x}\n"));
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /// The dump vocabulary, pinned against the reference's observed output for the demo
    /// guest (the `.3` evidence-path record's dump): register order, 6-hex values, and the
    /// deviation encoding's omission of zero-delta cells.
    #[test]
    fn register_block_matches_the_reference_vocabulary() {
        let m = Machine::new();
        let mut out = String::new();
        dump_registers(&mut out, &m);
        let lines: Vec<&str> = out.lines().collect();
        assert_eq!(lines[0], "steps 0");
        assert_eq!(lines[1], "pc 000000");
        assert_eq!(lines[2], "sr c00300");
        assert_eq!(lines[3], "omr 000300");
        assert_eq!(lines[4], "la ffffff");
        assert_eq!(lines[7], "ssh 000000");
        assert_eq!(lines[19], "a2 000000");
        assert_eq!(lines[23], "r0 000000");
        assert_eq!(lines[39], "m0 ffffff");
        assert_eq!(
            lines.len(),
            47,
            "steps + 46 register lines, never a cyc line"
        );
        assert!(!out.contains("cyc"));
    }

    #[test]
    fn deviations_omit_zero_deltas_and_the_harness_window() {
        let mut m = Machine::new();
        let init = m.reset_image();
        m.x[0x200] = 0x01F253;
        m.x[0x201] = 0; // written to its init value: no line, like xm0201 in the demo
        m.x[0x450] = 0xABCDEF; // inside the harness window $0400-$04FF: never dumped
        m.y[0x300] = 0x01F253;
        let mut out = String::new();
        dump_memory_deviations(&mut out, &m, &init);
        assert_eq!(out, "xm0200 01f253\nym0300 01f253\n");
    }

    #[test]
    fn stack_deviations_follow_the_seed_encoding() {
        let mut m = Machine::new();
        m.push(0xFF_FFFF, 0).unwrap();
        m.push(0x00010F, 0xC0_0310).unwrap();
        let mut out = String::new();
        dump_stack_deviations(&mut out, &m);
        assert_eq!(out, "sh01 ffffff\nsh02 00010f\nsl02 c00310\n");
    }
}

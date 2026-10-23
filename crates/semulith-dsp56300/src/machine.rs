//! Architectural state for the bounded DSP56300 model — every field the reference
//! harness's canonical dump names, nothing more.
//!
//! Representation: 24-bit registers are `u32` masked to `MASK24`, the 56-bit accumulators
//! are `u64` masked to `MASK56` — the masked fixed-width storage `docs/ARCHITECTURE.md` §4
//! sanctions for nonstandard widths. Reset values are the FM's (Table 5-1 for SR; the
//! register-file reset states of FM §3/§5) cross-checked against the reference's observed
//! end-state (`la`/`m` reset to `$FFFFFF`, `omr` to `$000300`).

/// 24-bit P/X/Y word mask (FM §3.1).
pub const MASK24: u32 = 0x00FF_FFFF;
/// 56-bit accumulator mask (A2:A1:A0 = 8+24+24 bits, FM §3.1).
pub const MASK56: u64 = 0x00FF_FFFF_FFFF_FFFF;

/// Sign-extend a 24-bit word to `i32`.
pub fn s24(v: u32) -> i32 {
    (((v & MASK24) << 8) as i32) >> 8
}

/// Sign-extend a 56-bit accumulator value to `i64`.
pub fn s56(v: u64) -> i64 {
    (((v & MASK56) << 8) as i64) >> 8
}

/// Memory-space sizes, bounded to the reference harness's sanctioned windows
/// (`tools/difftest/README.md`): X $0000-$0BFF, Y $0000-$07FF, P $0000-$07FF (the loaded
/// image lives low; the harness's P deviation window $07C0-$07FF is inside this). An
/// access outside is a typed `ModelStop::OutOfWindow`, never a wrap.
pub const X_WORDS: usize = 0x0C00;
/// Y data space size in words (`$0000`–`$07FF`).
pub const Y_WORDS: usize = 0x0800;
/// P program space size in words (`$0000`–`$07FF`).
pub const P_WORDS: usize = 0x0800;

/// The P deviation window the harness compares (its X window is $0000-$0BFF minus the
/// harness-private $0400-$04FF, which this model also excludes from its dump).
pub const P_DUMP_FROM: usize = 0x07C0;
/// First word of the harness-private X range the dump excludes.
pub const X_HARNESS_FROM: usize = 0x0400;
/// Last word of the harness-private X range the dump excludes.
pub const X_HARNESS_TO: usize = 0x04FF;

/// Hardware stack depth (FM §5.4.3: "16-level by 48-bit"); slots are addressed by the
/// pre-incremented SP, so slot 0 is never written and slots 1-15 are the dumped ones.
pub const STACK_LEVELS: usize = 16;

/// A typed stop — the subset's honest boundary. Anything the subset does not cover is one
/// of these, never a guessed behaviour (`docs/ARCHITECTURE.md` §2).
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ModelStop {
    /// A fetched word outside subset v0's decode — named, with its address and word.
    UnsupportedInsn {
        /// The P address the word was fetched from.
        addr: u32,
        /// The 24-bit instruction word.
        word: u32,
    },
    /// A memory access outside the modelled windows.
    OutOfWindow {
        /// The memory space accessed: `X`, `Y` or `P`.
        space: char,
        /// The address outside the window.
        addr: u32,
    },
    /// The 16-level hardware stack overflowed (stack extension is excluded upstream too).
    StackOverflow,
    /// The case's step budget was exhausted before the stop pc was reached.
    BudgetExhausted {
        /// The case's step budget.
        budget: u64,
    },
    /// A `.lod`/`.meta` construct the runner does not support (e.g. fill headers).
    Input(String),
}

impl std::fmt::Display for ModelStop {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ModelStop::UnsupportedInsn { addr, word } => write!(
                f,
                "unsupported instruction word {word:06X} at P:{addr:06X} — outside dsp56300-lab-v0 subset v0"
            ),
            ModelStop::OutOfWindow { space, addr } => {
                write!(f, "{space}-space address {addr:06X} is outside the modelled window")
            }
            ModelStop::StackOverflow => write!(
                f,
                "hardware stack overflow beyond 16 levels (stack extension is not in subset v0)"
            ),
            ModelStop::BudgetExhausted { budget } => {
                write!(f, "step budget {budget} exhausted before the stop pc was reached")
            }
            ModelStop::Input(what) => write!(f, "unsupported input: {what}"),
        }
    }
}

impl std::error::Error for ModelStop {}

/// The machine: the full canonical-dump register set, the hardware stack, and the three
/// memory spaces. Field order and names follow the dump's vocabulary.
pub struct Machine {
    /// Program counter.
    pub pc: u32,
    /// Status register; the Loop Flag is bit 15 (FM Table 5-1).
    pub sr: u32,
    /// Operating mode register.
    pub omr: u32,
    /// Loop address register: the last instruction of the current DO loop.
    pub la: u32,
    /// Loop counter register.
    pub lc: u32,
    /// Stack pointer.
    pub sp: u32,
    /// Stack extension pointer.
    pub ep: u32,
    /// Stack size register.
    pub sz: u32,
    /// Stack counter register.
    pub sc: u32,
    /// Vector base address register.
    pub vba: u32,
    /// Data ALU input register X0.
    pub x0: u32,
    /// Data ALU input register X1.
    pub x1: u32,
    /// Data ALU input register Y0.
    pub y0: u32,
    /// Data ALU input register Y1.
    pub y1: u32,
    /// Accumulator A as A2:A1:A0 in the low 56 bits.
    pub a: u64,
    /// Accumulator B as B2:B1:B0 in the low 56 bits.
    pub b: u64,
    /// AGU address registers R0–R7.
    pub r: [u32; 8],
    /// AGU offset registers N0–N7.
    pub n: [u32; 8],
    /// AGU modifier registers M0–M7 (`$FFFFFF` selects linear addressing).
    pub m: [u32; 8],
    /// The hardware stack: `[ssh, ssl]` per level, indexed by SP (slot 0 unused).
    stack: [[u32; 2]; STACK_LEVELS],
    /// X data memory, `X_WORDS` words.
    pub x: Vec<u32>,
    /// Y data memory, `Y_WORDS` words.
    pub y: Vec<u32>,
    /// P program memory, `P_WORDS` words.
    pub p: Vec<u32>,
    /// Instructions executed so far.
    pub steps: u64,
}

/// The initial memory image the deviation dump compares against: X/Y zero-filled (no
/// `fill` header is supported in subset v0 — a meta carrying one is a `ModelStop::Input`),
/// P holding the loaded program.
pub struct ResetImage {
    /// X data memory at reset.
    pub x: Vec<u32>,
    /// Y data memory at reset.
    pub y: Vec<u32>,
    /// P program memory holding the loaded program.
    pub p: Vec<u32>,
}

impl Machine {
    /// Power-on reset state: SR `$C00300` (CP=11, I1=I0=1, CCR clear — FM Table 5-1),
    /// OMR `$000300`, LA and all M registers `$FFFFFF`, everything else zero. The PC is
    /// set by the runner from the case's load base (the harness starts execution there).
    pub fn new() -> Self {
        Machine {
            pc: 0,
            sr: 0xC0_0300,
            omr: 0x0000_0300,
            la: MASK24,
            lc: 0,
            sp: 0,
            ep: 0,
            sz: 0,
            sc: 0,
            vba: 0,
            x0: 0,
            x1: 0,
            y0: 0,
            y1: 0,
            a: 0,
            b: 0,
            r: [0; 8],
            n: [0; 8],
            m: [MASK24; 8],
            stack: [[0; 2]; STACK_LEVELS],
            x: vec![0; X_WORDS],
            y: vec![0; Y_WORDS],
            p: vec![0; P_WORDS],
            steps: 0,
        }
    }

    /// The SSH register view: the high half of the top stack level (zero at SP=0 — the
    /// reference's dump shows `ssh 000000` at case end, matching an untouched slot 0).
    pub fn ssh(&self) -> u32 {
        self.stack[self.sp as usize][0]
    }

    /// The SSL register view: the low half of the top stack level.
    pub fn ssl(&self) -> u32 {
        self.stack[self.sp as usize][1]
    }

    /// The deviation-encoded stack slots 1-15 against their zero seed (dump order).
    pub fn stack_slots(&self) -> &[[u32; 2]; STACK_LEVELS] {
        &self.stack
    }

    /// Push one 48-bit level (FM §5.4.3: SP+1 → SP, then the write).
    pub fn push(&mut self, hi: u32, lo: u32) -> Result<(), ModelStop> {
        if self.sp as usize >= STACK_LEVELS - 1 {
            return Err(ModelStop::StackOverflow);
        }
        self.sp += 1;
        self.stack[self.sp as usize] = [hi & MASK24, lo & MASK24];
        Ok(())
    }

    /// Pop one 48-bit level.
    pub fn pop(&mut self) -> (u32, u32) {
        let v = self.stack[self.sp as usize];
        self.sp = self.sp.saturating_sub(1);
        (v[0], v[1])
    }

    /// The Loop Flag — SR bit 15 (FM Table 5-1).
    pub fn lf(&self) -> bool {
        self.sr & (1 << 15) != 0
    }

    /// Set or clear the Loop Flag, SR bit 15.
    pub fn set_lf(&mut self, on: bool) {
        if on {
            self.sr |= 1 << 15;
        } else {
            self.sr &= !(1 << 15);
        }
    }

    /// A copy of the X, Y and P spaces as they are now: taken after the program is loaded
    /// and before it runs, it is the base the deviation dump compares against.
    pub fn reset_image(&self) -> ResetImage {
        ResetImage {
            x: self.x.clone(),
            y: self.y.clone(),
            p: self.p.clone(),
        }
    }
}

impl Default for Machine {
    fn default() -> Self {
        Self::new()
    }
}

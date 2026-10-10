//! Qualified one-hart reservation histories; expectations precede execution.
use super::*;

#[derive(Debug, Default, PartialEq, Eq)]
struct Counts {
    boundaries: usize,
    data: usize,
    walks: usize,
    permissions: usize,
}
impl Counts {
    fn add(&mut self, other: Self) {
        self.boundaries += other.boundaries;
        self.data += other.data;
        self.walks += other.walks;
        self.permissions += other.permissions;
    }
    fn require(
        self,
        boundaries: usize,
        data: usize,
        walks: usize,
        permissions: usize,
    ) -> Result<(), String> {
        let expected = Self {
            boundaries,
            data,
            walks,
            permissions,
        };
        if self != expected {
            return Err(format!(
                "reservation matrix extent {self:?}, expected {expected:?}"
            ));
        }
        Ok(())
    }
}

// The program and every boundary expectation are complete before the first step.
struct Plan {
    fixture: Fixture,
    words: Vec<u32>,
    expected: Vec<Observation>,
}
impl Plan {
    fn new(mode: PrivilegeMode, vector: usize) -> Self {
        let mut fixture = Fixture::new(0, mode, &VECTORS[vector], DATA);
        fixture
            .observer
            .memory
            .load_image(0x90, &VECTORS[vector].old.to_le_bytes());
        fixture.hart.write_x(14, DATA);
        fixture.hart.write_x(15, 0x0102_0304_0506_0708);
        fixture.hart.write_f(15, VECTORS[vector].source);
        fixture.expected = Observation::capture(&mut fixture.hart, &fixture.observer, true);
        Self {
            fixture,
            words: Vec::new(),
            expected: Vec::new(),
        }
    }
    fn registers(&mut self, values: &[(u8, u64)]) {
        for &(index, value) in values {
            self.fixture.hart.write_x(index, value);
            self.fixture.expected.x[usize::from(index)] = value;
        }
    }
    fn prior(&mut self, kind: usize, n: u32) {
        let reservation = self.fixture.hart.reservation();
        *reservation = Reservation::new();
        match kind {
            0 => reservation.establish(DATA + 0x20, 8),
            1 => reservation.establish(DATA, if n == 4 { 8 } else { 4 }),
            2 => {
                reservation.establish(DATA + 0x10, 4);
                reservation.clear();
            }
            _ => {}
        }
        self.fixture.expected.reservation = *reservation;
    }
    fn translated(&mut self, second_pa: u64, flags: u64) {
        self.fixture.hart.write_csr(CSR_MSTATUS, 0xa_0002_6808);
        self.fixture.hart.write_csr(CSR_SATP, 0x8000_0000_0000_0002);
        let old = memory_value(&self.fixture.expected, DATA, 8);
        // Preserve the initial nonzero FIFO cursor and unrelated cached entries.
        for (address, value) in [
            (0x2000_u64, 0xc01_u64),
            (0x3000, 0x1001),
            (0x4080, 0x1400 | flags),
            (0x4088, ((second_pa >> 12) << 10) | 0xc7),
            (PA, old),
        ] {
            self.fixture
                .observer
                .memory
                .load_image((address - ENTRY) as usize, &value.to_le_bytes());
        }
        self.fixture.expected =
            Observation::capture(&mut self.fixture.hart, &self.fixture.observer, true);
    }
    fn push(&mut self, word: u32, retired: bool, update: impl FnOnce(&mut Observation, u64)) {
        let pc = ENTRY + 4 * self.words.len() as u64;
        self.words.push(word);
        let expected = &mut self.fixture.expected;
        expected.requests.extend([
            Request::FetchParcel { addr: pc },
            Request::FetchParcel { addr: pc + 2 },
        ]);
        expected.parcels += 2;
        expected.csrs[CSR_MCYCLE] += 1;
        if retired {
            expected.csrs[CSR_MINSTRET] += 1;
        }
        expected.pc = pc + 4;
        update(expected, pc);
        self.expected.push(expected.clone());
    }
    fn lr(&mut self, n: u32, order: u32, rd: u32, base: u32, pa: u64, walk: Option<u64>) {
        self.push(
            atomic_word(2, n, order, rd, base, 0),
            true,
            |expected, _| {
                if let Some(va) = walk {
                    mapped(expected, va, pa);
                }
                expected.requests.push(Request::Load {
                    width: width(n),
                    addr: pa,
                });
                let value = memory_value(expected, pa, n);
                if rd != 0 {
                    expected.x[rd as usize] = if n == 4 {
                        value as u32 as i32 as i64 as u64
                    } else {
                        value
                    };
                }
                expected.reservation.establish(pa, n as u8);
            },
        );
    }
    // Keep encoded fields, physical outcome and expected success explicit and separate.
    #[allow(clippy::too_many_arguments)]
    fn sc(
        &mut self,
        n: u32,
        order: u32,
        rd: u32,
        base: u32,
        source: u32,
        pa: u64,
        succeeds: bool,
        walk: Option<u64>,
    ) {
        self.push(
            atomic_word(3, n, order, rd, base, source),
            true,
            |expected, _| {
                if let Some(va) = walk {
                    mapped(expected, va, pa);
                }
                // Scenario-literal success; the production match predicate is never consulted.
                if succeeds {
                    store(expected, pa, n, expected.x[source as usize]);
                } else {
                    expected.requests.push(Request::StorePermission {
                        width: width(n),
                        addr: pa,
                    });
                }
                if rd != 0 {
                    expected.x[rd as usize] = u64::from(!succeeds);
                }
                expected.reservation.clear();
            },
        );
    }
    fn ordinary(&mut self, kind: usize, n: u32, order: u32) {
        let word = match kind {
            0 | 1 => (15 << 20) | (14 << 15) | ((if kind == 0 { 2 } else { 3 }) << 12) | 0x23,
            2 => (15 << 20) | (14 << 15) | (3 << 12) | 0x27,
            3 => atomic_word(0, n, order, 16, 14, 15),
            4 => (1 << 20) | (16 << 7) | 0x13,
            _ => 0x0ff0_000f,
        };
        self.push(word, true, |expected, _| match kind {
            0 | 1 => store(
                expected,
                DATA,
                if kind == 0 { 4 } else { 8 },
                expected.x[15],
            ),
            2 => store(expected, DATA, 8, expected.f[15]),
            3 => {
                let old = memory_value(expected, DATA, n);
                expected.requests.push(Request::Load {
                    width: width(n),
                    addr: DATA,
                });
                store(expected, DATA, n, old.wrapping_add(expected.x[15]));
                expected.x[16] = if n == 4 {
                    old as u32 as i32 as i64 as u64
                } else {
                    old
                };
            }
            4 => expected.x[16] = 1,
            _ => {}
        });
    }
    fn prepare(&mut self) {
        for (i, word) in self.words.iter().enumerate() {
            let bytes = word.to_le_bytes();
            self.fixture.observer.memory.load_image(i * 4, &bytes);
            for expected in &mut self.expected {
                expected.memory[i * 4..i * 4 + 4].copy_from_slice(&bytes);
            }
        }
    }
    fn check(mut self, table: &[InsnDef]) -> Result<Counts, String> {
        self.prepare();
        for (index, expected) in self.expected.iter().enumerate() {
            judge(&self.fixture.observe(table), expected)
                .map_err(|error| format!("reservation boundary {index}: {error}"))?;
        }
        let last = self
            .expected
            .last()
            .expect("a reservation program has a boundary");
        Ok(Counts {
            boundaries: self.expected.len(),
            data: last
                .requests
                .iter()
                .filter(|r| matches!(r, Request::Load { .. } | Request::Store { .. }))
                .count(),
            permissions: last
                .requests
                .iter()
                .filter(|r| matches!(r, Request::StorePermission { .. }))
                .count(),
            walks: last
                .requests
                .iter()
                .filter(|r| matches!(r, Request::WalkAccess { .. }))
                .count(),
        })
    }
}
fn atomic_word(function: u32, n: u32, order: u32, rd: u32, base: u32, source: u32) -> u32 {
    (word(function, n, order, rd, source) & !(31 << 15)) | (base << 15)
}
fn memory_value(expected: &Observation, address: u64, n: u32) -> u64 {
    let mut bytes = [0; 8];
    let start = (address - ENTRY) as usize;
    bytes[..n as usize].copy_from_slice(&expected.memory[start..start + n as usize]);
    u64::from_le_bytes(bytes)
}
fn store(expected: &mut Observation, address: u64, n: u32, value: u64) {
    let value = if n == 4 { value & 0xffff_ffff } else { value };
    expected.requests.push(Request::Store {
        width: width(n),
        addr: address,
        data: value,
    });
    let start = (address - ENTRY) as usize;
    expected.memory[start..start + n as usize].copy_from_slice(&value.to_le_bytes()[..n as usize]);
}
fn walk(expected: &mut Observation, va: u64) {
    for addr in [0x2000, 0x3000, 0x4000 + ((va >> 12) & 511) * 8] {
        expected.requests.push(Request::WalkAccess { addr });
    }
}
fn mapped(expected: &mut Observation, va: u64, pa: u64) {
    walk(expected, va);
    expected.tlb.install(TlbEntry {
        valid: true,
        global: false,
        asid: 0,
        vpn: va >> 12,
        pa_base: pa,
        r: true,
        w: true,
        x: false,
        u: false,
        a: true,
        d: true,
        level: 0,
    });
}
fn trap(expected: &mut Observation, pc: u64, cause: u64, address: u64) {
    let mode = match expected.mode {
        PrivilegeMode::U => 0,
        PrivilegeMode::S => 1,
        PrivilegeMode::M => 3,
    };
    let old = expected.csrs[CSR_MSTATUS];
    expected.csrs[CSR_MSTATUS] =
        (old & !((3 << 11) | (1 << 7) | (1 << 3))) | (mode << 11) | ((old & (1 << 3)) << 4);
    expected.mode = PrivilegeMode::M;
    expected.pc = 0x1100;
    expected.csrs[CSR_MCAUSE] = cause;
    expected.csrs[CSR_MEPC] = pc;
    expected.csrs[CSR_MTVAL] = address;
}

fn histories_over(table: &[InsnDef]) -> Result<(), String> {
    let mut counts = Counts::default();
    for history in 0..13 {
        for n in [4, 8] {
            for order in 0..4 {
                for mode in MODES {
                    for (lr_rd, sc_rd) in [(0, 0), (6, 10), (7, 7), (9, 9)] {
                        for vector in [0, 1, 2, 7] {
                            for source in [9, 10, 0] {
                                let other = if n == 4 { 8 } else { 4 };
                                let (target, last) = match history {
                                    0 => (DATA, DATA + 16),
                                    1 => (DATA + 16, DATA + 16),
                                    2 => (DATA + 16, DATA),
                                    5 => (DATA + 32, DATA + 32),
                                    _ => (DATA, DATA),
                                };
                                let mut plan = Plan::new(mode, vector);
                                plan.registers(&[
                                    (10, target),
                                    (11, last),
                                    (13, if history == 6 { DATA } else { DATA + 16 }),
                                ]);
                                if history == 5 {
                                    plan.prior(2, n);
                                }
                                if history != 5 {
                                    plan.lr(n, order, lr_rd, 6, DATA, None);
                                }
                                match history {
                                    0 | 1 => plan.lr(n, order, 7, 13, DATA + 16, None),
                                    6 => plan.lr(other, order, 7, 13, DATA, None),
                                    7.. => plan.ordinary(history - 7, n, order),
                                    _ => {}
                                }
                                let sc_width = if history == 4 || history == 6 {
                                    other
                                } else {
                                    n
                                };
                                plan.sc(
                                    sc_width,
                                    order,
                                    sc_rd,
                                    10,
                                    source,
                                    target,
                                    matches!(history, 1 | 3 | 6..=12),
                                    None,
                                );
                                plan.sc(
                                    if history == 6 { other } else { n },
                                    order,
                                    5,
                                    11,
                                    source,
                                    last,
                                    false,
                                    None,
                                );
                                counts.add(plan.check(table).map_err(|e| format!("history={history} n={n} order={order} {mode:?} rd={lr_rd}/{sc_rd} vector={vector} source={source}: {e}"))?);
                            }
                        }
                    }
                }
            }
        }
    }
    counts.require(54144, 33408, 0, 19584)
}
fn aliases_over(table: &[InsnDef]) -> Result<(), String> {
    let mut counts = Counts::default();
    for same in [false, true] {
        for n in [4, 8] {
            for order in 0..4 {
                for (lr_rd, sc_rd) in [(0, 0), (6, 10), (7, 7), (9, 9)] {
                    for vector in [0, 1, 2, 7] {
                        for source in [9, 10, 0] {
                            let second_pa = if same { PA } else { 0x3000 };
                            let mut plan = Plan::new(PrivilegeMode::M, vector);
                            plan.translated(second_pa, 0xc7);
                            plan.registers(&[(6, VA), (10, VA + 0x1000), (11, VA + 0x1000)]);
                            plan.lr(n, order, lr_rd, 6, PA, Some(VA));
                            plan.sc(
                                n,
                                order,
                                sc_rd,
                                10,
                                source,
                                second_pa,
                                same,
                                Some(VA + 0x1000),
                            );
                            plan.sc(n, order, 5, 11, source, second_pa, false, None);
                            counts.add(plan.check(table).map_err(|e| format!("physical alias same={same} n={n} order={order} rd={lr_rd}/{sc_rd} vector={vector} source={source}: {e}"))?);
                        }
                    }
                }
            }
        }
    }
    counts.require(2304, 1152, 4608, 1152)
}
fn bare_faults_over(table: &[InsnDef]) -> Result<(), String> {
    let mut counts = Counts::default();
    for function in [2, 3] {
        for n in [4, 8] {
            for order in 0..4 {
                for mode in MODES {
                    for rd in [0, 6, 7, 9] {
                        for fault in 0..3 {
                            for prior in 0..if function == 2 || fault == 0 { 4 } else { 1 } {
                                let address = match fault {
                                    0 => DATA + 1,
                                    1 => 0,
                                    _ => DATA,
                                };
                                let mut plan = Plan::new(mode, 7);
                                plan.prior(prior, n);
                                plan.registers(&[(6, address)]);
                                if function == 3 && fault != 0 {
                                    plan.fixture.hart.reservation().establish(address, n as u8);
                                    plan.fixture
                                        .expected
                                        .reservation
                                        .establish(address, n as u8);
                                }
                                let request = if function == 2 {
                                    Request::Load {
                                        width: width(n),
                                        addr: address,
                                    }
                                } else {
                                    Request::Store {
                                        width: width(n),
                                        addr: address,
                                        data: if n == 4 {
                                            plan.fixture.expected.x[9] & 0xffff_ffff
                                        } else {
                                            plan.fixture.expected.x[9]
                                        },
                                    }
                                };
                                if fault == 2 {
                                    plan.fixture.observer.fail = Some(request);
                                }
                                plan.push(
                                    atomic_word(
                                        function,
                                        n,
                                        order,
                                        rd,
                                        6,
                                        if function == 2 { 0 } else { 9 },
                                    ),
                                    false,
                                    |expected, pc| {
                                        if fault != 0 {
                                            expected.requests.push(request);
                                        }
                                        trap(
                                            expected,
                                            pc,
                                            if function == 2 { 5 } else { 7 },
                                            address,
                                        );
                                    },
                                );
                                counts.add(plan.check(table)?);
                            }
                        }
                    }
                }
            }
        }
    }
    counts.require(1728, 960, 0, 0)
}
fn translated_faults_over(table: &[InsnDef]) -> Result<(), String> {
    let mut counts = Counts::default();
    for function in [2, 3] {
        for n in [4, 8] {
            for order in 0..4 {
                for rd in [0, 6, 7, 9] {
                    let bad: &[u64] = if function == 2 {
                        &[0xc6, 0xc5, 0xc9, 0x87, 0xd7]
                    } else {
                        &[0xc6, 0xc5, 0xc9, 0x87, 0xd7, 0xc3, 0x47]
                    };
                    for (&flags, fail_walk) in bad.iter().map(|f| (f, None)).chain(
                        [0x2000, 0x3000, 0x4080]
                            .into_iter()
                            .map(|a| (&0xc7, Some(a))),
                    ) {
                        for prior in 0..4 {
                            let mut plan = Plan::new(PrivilegeMode::M, 7);
                            plan.prior(prior, n);
                            plan.translated(PA, flags);
                            plan.registers(&[(6, VA)]);
                            plan.fixture.observer.fail =
                                fail_walk.map(|addr| Request::WalkAccess { addr });
                            plan.push(
                                atomic_word(
                                    function,
                                    n,
                                    order,
                                    rd,
                                    6,
                                    if function == 2 { 0 } else { 9 },
                                ),
                                false,
                                |expected, pc| {
                                    for address in [0x2000, 0x3000, 0x4080] {
                                        expected
                                            .requests
                                            .push(Request::WalkAccess { addr: address });
                                        if fail_walk == Some(address) {
                                            break;
                                        }
                                    }
                                    let cause = if fail_walk.is_some() {
                                        if function == 2 {
                                            5
                                        } else {
                                            7
                                        }
                                    } else if function == 2 {
                                        13
                                    } else {
                                        15
                                    };
                                    trap(expected, pc, cause, VA);
                                },
                            );
                            counts.add(plan.check(table).map_err(|e| format!("translated fault function={function} n={n} flags={flags:x} walk={fail_walk:?} prior={prior} rd={rd}: {e}"))?);
                        }
                    }
                    for prior in 0..if function == 2 { 4 } else { 1 } {
                        let mut plan = Plan::new(PrivilegeMode::M, 7);
                        plan.prior(prior, n);
                        plan.translated(PA, 0xc7);
                        plan.registers(&[(6, VA)]);
                        if function == 3 {
                            plan.fixture.hart.reservation().establish(PA, n as u8);
                            plan.fixture.expected.reservation.establish(PA, n as u8);
                        }
                        let request = if function == 2 {
                            Request::Load {
                                width: width(n),
                                addr: PA,
                            }
                        } else {
                            Request::Store {
                                width: width(n),
                                addr: PA,
                                data: if n == 4 {
                                    plan.fixture.expected.x[9] & 0xffff_ffff
                                } else {
                                    plan.fixture.expected.x[9]
                                },
                            }
                        };
                        plan.fixture.observer.fail = Some(request);
                        plan.push(
                            atomic_word(
                                function,
                                n,
                                order,
                                rd,
                                6,
                                if function == 2 { 0 } else { 9 },
                            ),
                            false,
                            |expected, pc| {
                                mapped(expected, VA, PA);
                                expected.requests.push(request);
                                trap(expected, pc, if function == 2 { 5 } else { 7 }, VA);
                            },
                        );
                        counts.add(plan.check(table)?);
                    }
                }
            }
        }
    }
    counts.require(2464, 160, 6624, 0)
}
pub(super) fn positive_over(table: &[InsnDef]) -> Result<(), String> {
    histories_over(table)?;
    aliases_over(table)
}
pub(super) fn negative_over(table: &[InsnDef]) -> Result<(), String> {
    bare_faults_over(table)?;
    translated_faults_over(table)
}
#[cfg(test)]
mod tests {
    use super::*;
    use semulith_core::definition_rv64gc::Sem;
    #[test]
    fn reservation_histories_and_physical_aliases() {
        assert_eq!(positive_over(INSNS), Ok(()));
    }
    #[test]
    fn reservation_faults_preserve_prior_state() {
        assert_eq!(negative_over(INSNS), Ok(()));
    }
    fn changed(name: &str, effect: &'static Sem) -> Vec<InsnDef> {
        INSNS
            .iter()
            .map(|row| InsnDef {
                from: row.from,
                name: row.name,
                mask: row.mask,
                value: row.value,
                operands: row.operands,
                source: row.source,
                effect: if row.name == name { effect } else { row.effect },
                length: row.length,
                expansion: row.expansion,
            })
            .collect()
    }
    const SC_W: &Sem = &Sem::Set(
        &Sem::Reg("rd"),
        &Sem::StoreConditional(
            &Sem::Lit(32),
            &Sem::Reg("rs1"),
            &Sem::Trunc(32, &Sem::Reg("rs2")),
        ),
    );
    const SC_D: &Sem = &Sem::Set(
        &Sem::Reg("rd"),
        &Sem::StoreConditional(&Sem::Lit(64), &Sem::Reg("rs1"), &Sem::Reg("rs2")),
    );
    #[test]
    fn wrong_reservation_instruction_effects_are_rejected() {
        for (name, replacement) in [
            ("lr.w", "lr.d"),
            ("lr.d", "lr.w"),
            ("sc.w", "sc.d"),
            ("sc.d", "sc.w"),
        ] {
            let effect = INSNS.iter().find(|r| r.name == replacement).unwrap().effect;
            assert!(
                positive_over(&changed(name, effect)).is_err(),
                "wrong width {name}"
            );
        }
        for name in ["lr.w", "lr.d"] {
            assert!(positive_over(&changed(name, &Sem::Nop)).is_err());
        }
        for (name, effect) in [
            (
                "lr.w",
                &Sem::Set(
                    &Sem::Reg("rd"),
                    &Sem::Sext(
                        64,
                        &Sem::Load(&Sem::Lit(32), &Sem::Lit(1), &Sem::Reg("rs1")),
                    ),
                ),
            ),
            (
                "lr.d",
                &Sem::Set(
                    &Sem::Reg("rd"),
                    &Sem::Load(&Sem::Lit(64), &Sem::Lit(0), &Sem::Reg("rs1")),
                ),
            ),
        ] {
            assert!(positive_over(&changed(name, effect)).is_err());
        }
        for name in ["sc.w", "sc.d"] {
            assert!(
                positive_over(&changed(name, &Sem::Set(&Sem::Reg("rd"), &Sem::Lit(1)))).is_err()
            );
        }
        for (name, effect) in [
            (
                "sc.w",
                &Sem::Seq(&[
                    &Sem::Store(
                        &Sem::Lit(32),
                        &Sem::Reg("rs1"),
                        &Sem::Trunc(32, &Sem::Reg("rs2")),
                    ),
                    &Sem::Set(&Sem::Reg("rd"), &Sem::Lit(0)),
                ]),
            ),
            (
                "sc.d",
                &Sem::Seq(&[
                    &Sem::Store(&Sem::Lit(64), &Sem::Reg("rs1"), &Sem::Reg("rs2")),
                    &Sem::Set(&Sem::Reg("rd"), &Sem::Lit(0)),
                ]),
            ),
            (
                "sc.w",
                &Sem::Seq(&[
                    SC_W,
                    &Sem::Load(&Sem::Lit(64), &Sem::Lit(0), &Sem::Lit(DATA)),
                ]),
            ),
            (
                "sc.d",
                &Sem::Seq(&[
                    SC_D,
                    &Sem::Load(&Sem::Lit(64), &Sem::Lit(0), &Sem::Lit(DATA)),
                ]),
            ),
        ] {
            assert!(positive_over(&changed(name, effect)).is_err());
        }
        for (name, effect) in [
            (
                "sc.w",
                &Sem::Seq(&[&Sem::Set(&Sem::Reg("rd"), &Sem::Lit(42)), SC_W]),
            ),
            (
                "sc.d",
                &Sem::Seq(&[&Sem::Set(&Sem::Reg("rd"), &Sem::Lit(42)), SC_D]),
            ),
        ] {
            assert!(negative_over(&changed(name, effect)).is_err());
        }
    }
    #[test]
    fn corrupted_reservation_captures_fail_each_component() {
        let mut plan = Plan::new(PrivilegeMode::M, 7);
        plan.fixture.hart.reservation().establish(DATA, 8);
        plan.fixture.expected.reservation.establish(DATA, 8);
        plan.sc(8, 0, 7, 6, 9, DATA, true, None);
        plan.prepare();
        let actual = plan.fixture.observe(INSNS);
        assert_eq!(judge(&actual, &plan.expected[0]), Ok(()));
        for kind in 0..16 {
            let mut bad = actual.clone();
            match kind {
                0 => bad.reservation = Reservation::new(),
                1 => {
                    bad.reservation.establish(DATA, 4);
                    bad.reservation.clear();
                }
                2 => {
                    bad.reservation.establish(DATA + 8, 8);
                    bad.reservation.clear();
                }
                3 => bad.reservation.establish(DATA, 8),
                4 => bad.x[0] = 1,
                5 => bad.f[0] ^= 1,
                6 => bad.csrs[CSR_MCYCLE] += 1,
                7 => bad.wait.enter(),
                8 => bad.pc += 4,
                9 => bad.mode = PrivilegeMode::U,
                10 => bad.memory[0x101] ^= 1,
                11 => {
                    bad.requests.pop().expect("completed SC emitted a Store");
                }
                12 => bad.requests.swap(0, 1),
                13 => bad.parcels += 1,
                14 => bad.executed = false,
                _ => bad.tlb.install(TlbEntry {
                    valid: true,
                    global: false,
                    asid: 0x12,
                    vpn: 0x41,
                    pa_base: 0xa000,
                    r: true,
                    w: true,
                    x: true,
                    u: false,
                    a: true,
                    d: true,
                    level: 0,
                }),
            }
            assert!(
                judge(&bad, &plan.expected[0]).is_err(),
                "capture component {kind}"
            );
        }
    }
}

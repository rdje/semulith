//! GENERATED — do not edit (OWN-03). Regenerate with `python3 scripts/gen_guests.py`; drift between this fixture and the tracked guest sources is refused by the GUEST-GEN doctrine (`scripts/check_guest_gen.sh`). This module lowers the tracked assembly guests and their specification-derived expectations into data for the verify-side execution tests (`P1-LAB.8`): every expectation value was derived from the pinned specification prose before any model ran (EVD-05), so the commit gate re-runs the first-execution-slice differential offline.
//!
//! Canonical inputs (sha256):
//!   `profiles/rv64i-lab-v0/encoding.sexp`  `93a2d4718a50b60c23c3b5e64afa64499b09fcf41a906d46d83e63eebab2e5e9`
//!   `profiles/rv64i-lab-v0/guests/bound-alias.expected.sexp`  `6302190f10800d758c27323eb7b7b29d97f99069cf28ad624889e802b03e74ad`
//!   `profiles/rv64i-lab-v0/guests/bound-alias.s`  `e180f4df21803411a70c7b652425d780c51dd880c59ee7e80c70b8fad58fd65f`
//!   `profiles/rv64i-lab-v0/guests/bound-arith.expected.sexp`  `855e2994b8b5ff7aaa6014002a23cfe09c7631a19faeb68a077a793033f357c0`
//!   `profiles/rv64i-lab-v0/guests/bound-arith.s`  `13b3be6d77489ae88564a00c0b8d57800e488a1104ad5df04bbaad15618a4e3b`
//!   `profiles/rv64i-lab-v0/guests/bound-ext.expected.sexp`  `fdd9b96a4ce10b3207e6f4f5fd413553023c4d6d1c4f9509fec40a136daf6a98`
//!   `profiles/rv64i-lab-v0/guests/bound-ext.s`  `7b33b6b517f5fb25e7c2aec9caa6899c3e7a4aef4cba28660c0fffa99e48dec6`
//!   `profiles/rv64i-lab-v0/guests/bound-shift.expected.sexp`  `3009550a91ff679e40603764396ca9c96c55af2843911d68ba6df523dbc0d838`
//!   `profiles/rv64i-lab-v0/guests/bound-shift.s`  `d0502bfd2fb3fc2cffc62a357514de1bf2e1db1bd0bd83808348bcc7b73c13f6`
//!   `profiles/rv64i-lab-v0/guests/bound-shiftw.expected.sexp`  `46b6c8513ae5f01f3adebe29dc0f18d41aa7111557cb897117d3c1cba52e6aa5`
//!   `profiles/rv64i-lab-v0/guests/bound-shiftw.s`  `0d06652ccfd1b5c78a7fc845b9c9d25acdea96ce379e1744bcf0de92cf7f36f2`
//!   `profiles/rv64i-lab-v0/guests/dir-chain.expected.sexp`  `8a788e5f401295627a922acd987912e305bf71fc61dca39af251a274c2c59e8e`
//!   `profiles/rv64i-lab-v0/guests/dir-chain.s`  `39eca25dc00031aaa41295ef74fb17878ad40f45c33de29b5d141b5867396164`
//!   `profiles/rv64i-lab-v0/guests/dir-chase.expected.sexp`  `300545aff8d0c6fe0e4f7adfae677207ed3fe4dcec65cb49a39255551968fa00`
//!   `profiles/rv64i-lab-v0/guests/dir-chase.s`  `048298bc99c08d7564001f9d9513c78c72c33752a419ed609a38583519473997`
//!   `profiles/rv64i-lab-v0/guests/dir-cmp-branch.expected.sexp`  `edecc2ad9fb4821fe7fedaf59a5339e4fdedf6c2245c3b13173a318cc25e754b`
//!   `profiles/rv64i-lab-v0/guests/dir-cmp-branch.s`  `0f3b157395468c4edbb6ddb6dcad4cf4fff89380636f0f521302ea69dc437d3b`
//!   `profiles/rv64i-lab-v0/guests/dir-ext-matrix.expected.sexp`  `1b8148edc09a26017cfc358d522f8cbb57813914e695e7449a07dd6c4ce19388`
//!   `profiles/rv64i-lab-v0/guests/dir-ext-matrix.s`  `020cd75e06a44d3c2e533bc5d6b086432b13f29b5b03345c7e44d0e9f4beed5c`
//!   `profiles/rv64i-lab-v0/guests/dir-memwalk.expected.sexp`  `457fd7089d62bc51aa5eae83b759fd69c86f724d98b03ebbc94eb97ce8c527f8`
//!   `profiles/rv64i-lab-v0/guests/dir-memwalk.s`  `2d939ac2d8a2a4780032d631b3e0c68739ae7b2328a4988c03067329aedb3036`
//!   `profiles/rv64i-lab-v0/guests/dir-runoff.expected.sexp`  `16cba7629001418e756c0963022fb0430f97e45f3881b39eac2d8d8fb62f2e7a`
//!   `profiles/rv64i-lab-v0/guests/dir-runoff.s`  `384fe5d7f276e5b2ded2173cec8e880577128d161cdbda046f0c304a104dc8e4`
//!   `profiles/rv64i-lab-v0/guests/dir-selfmod-fence.expected.sexp`  `1f495af021278ce85cd3c8c1f195fe67d11907dd2515e7238b5015e13513cd77`
//!   `profiles/rv64i-lab-v0/guests/dir-selfmod-fence.s`  `15f6684165d656d8af857cfcdece9a873c919f165ef979ee2c1909863df49a3e`
//!   `profiles/rv64i-lab-v0/guests/dir-x0-writes.expected.sexp`  `99ef2f9d93df14929678aa8b82f9c728158c82a59f14bee3bc7a3ad281624c5f`
//!   `profiles/rv64i-lab-v0/guests/dir-x0-writes.s`  `2daf04a0f2f0f3b7141b42e228d673c6594fe32817a94069b846054ae78c308c`
//!   `profiles/rv64i-lab-v0/guests/fault-access-ld.expected.sexp`  `ddaf0b9f1f05dcd7a62fd1977a8a42edfc484e26f4dc7aeaa688c6fe55cba2f4`
//!   `profiles/rv64i-lab-v0/guests/fault-access-ld.s`  `f0bafd194b4b0db3474d854c2d8dcc5591db3a4b0601566fd5dcefcd4d1a426b`
//!   `profiles/rv64i-lab-v0/guests/fault-access-sd.expected.sexp`  `c286c38bd6a5763cd66a078c267d73acf2550eae05922a620b6528780d5042d2`
//!   `profiles/rv64i-lab-v0/guests/fault-access-sd.s`  `aa94443da02904dc45b2dfc270a681972b35d3abefe56bb37a09555eda5a87fb`
//!   `profiles/rv64i-lab-v0/guests/fault-branch-nt.expected.sexp`  `2eb0f00a2d6796153ed85c7ed63d4f5dd4326154adb49a3a96a8551f6596f3d3`
//!   `profiles/rv64i-lab-v0/guests/fault-branch-nt.s`  `070d919040740bdafe9143fb160c1d475c6a950aa065c27384d65bdafc75466e`
//!   `profiles/rv64i-lab-v0/guests/fault-fence.expected.sexp`  `9e6969f2a86a12b3278eb88172539270ca0df4a2c007f59e747d82b1996a8388`
//!   `profiles/rv64i-lab-v0/guests/fault-fence.s`  `2d7bc1d6395ef2087807f62581ec446cce45efed4525626b2e8df7b059c360d0`
//!   `profiles/rv64i-lab-v0/guests/fault-fetch.expected.sexp`  `7cd18309ee051e35485fb038e32fc3d03a139c934c84487874f4b72e8cd929ec`
//!   `profiles/rv64i-lab-v0/guests/fault-fetch.s`  `2f8a8057a999629fd6a411d65e5a3ed4c8bd65e36508bc9904b60d9099477bf1`
//!   `profiles/rv64i-lab-v0/guests/fault-hints.expected.sexp`  `20d791e08d29e5fd71a51e2d8582b86acc45115e4d93eee72949f7676407b098`
//!   `profiles/rv64i-lab-v0/guests/fault-hints.s`  `ee84d9e8eb066e36153ef677fd41c3f3a8e641ec606310d5340f039c53a36821`
//!   `profiles/rv64i-lab-v0/guests/fault-jal-mis.expected.sexp`  `4cadbc0a7702c49ca8d3aaeaa93e194b50dc281d54a440248ace9e59f5fe370f`
//!   `profiles/rv64i-lab-v0/guests/fault-jal-mis.s`  `cd96d5b0fb65172725a1d4eba62d01c5efa303b8a71e574d77449b470dfde38a`
//!   `profiles/rv64i-lab-v0/guests/fault-jalr-mis.expected.sexp`  `85d4b689518069949b92910ce3fdcab7de2bfe3f6d60f58107437765b6e4598e`
//!   `profiles/rv64i-lab-v0/guests/fault-jalr-mis.s`  `ae910bf22b13c543a6888b27d875aa72b4fea5659c2511ae5cbe1dd68e41ee28`
//!   `profiles/rv64i-lab-v0/guests/fault-ld-mis-d.expected.sexp`  `758a553468bf6b10dd3e56789d63fbcebd8da1a9e0efb12f526ef9f5eb234196`
//!   `profiles/rv64i-lab-v0/guests/fault-ld-mis-d.s`  `3d21d3718ccdada0fe113d67d495717feacbd074d3712a6c0ec2204e339a0efd`
//!   `profiles/rv64i-lab-v0/guests/fault-ld-mis-h.expected.sexp`  `ab25c1ac1e100393afd90d92bbbaf8709d7b85f57255d83d62671672968d7ecd`
//!   `profiles/rv64i-lab-v0/guests/fault-ld-mis-h.s`  `49a2c3b3ddaa559f029728ea947c17704a15e0ab84544337911064a0f0943d77`
//!   `profiles/rv64i-lab-v0/guests/fault-ld-x0-fault.expected.sexp`  `9cd5dd8d9ba4ac0dcc8b8eeb007670433b702895f87a273ab6d1bada8be3bedb`
//!   `profiles/rv64i-lab-v0/guests/fault-ld-x0-fault.s`  `fcd5934ed90390c0886e750c3f383483c3268d7688030b6a2d0d55520bd73f04`
//!   `profiles/rv64i-lab-v0/guests/fault-ld-x0-mis.expected.sexp`  `9a6e37907cd8e50ed4cbbe30406da543681ddd71aec5795e47b36ac001d08ed7`
//!   `profiles/rv64i-lab-v0/guests/fault-ld-x0-mis.s`  `b144786699c73dd2360ea28f5eafdc10678b9ebb012c579bc6ad0111548d4d2c`
//!   `profiles/rv64i-lab-v0/guests/fault-reserved.expected.sexp`  `47caf3d332c4668e80949523e52ec98e687c79bfc3ac7900c4c9d8d2b2d18ebc`
//!   `profiles/rv64i-lab-v0/guests/fault-reserved.s`  `65bf2c9805b77047f0c599a9d48af11d1c7e33ef061a0aea028df4684d67f01e`
//!   `profiles/rv64i-lab-v0/guests/fault-selfmod.expected.sexp`  `1c68412cb5eea6d1e48edfd187a3d51043b04e8bcf1470e09753ac57917a1108`
//!   `profiles/rv64i-lab-v0/guests/fault-selfmod.s`  `9cbd4bffa445e2adc3975ffd8fe6880c98156be3013e6b665ca0876c08163d04`
//!   `profiles/rv64i-lab-v0/guests/fault-shiftw-res.expected.sexp`  `9659ef1277e9bb0a64b19a7f31f0927749f71fd7a1800d9a8c2583ea1eab1f36`
//!   `profiles/rv64i-lab-v0/guests/fault-shiftw-res.s`  `9129c4d9559648ea63e6aa21da18b3cb98514ced7f789c50896da54e6f1f9855`
//!   `profiles/rv64i-lab-v0/guests/fault-st-mis-d.expected.sexp`  `e465b3fbbf3d56f86e7b66543adc9ade16a1083a696b11467529073f126ed08c`
//!   `profiles/rv64i-lab-v0/guests/fault-st-mis-d.s`  `df3acd877518bde4055c19d517af14f462ab1201fc5ff3eeebc2025b8eada956`
//!   `profiles/rv64i-lab-v0/guests/fault-st-mis-h.expected.sexp`  `270d776325cd16a87caafb6847a17df67541db55fde5f3dd1666af6ff0ae58e5`
//!   `profiles/rv64i-lab-v0/guests/fault-st-mis-h.s`  `5ade62462a835877d09c9541f94069f47444ac65734f153d3d15b4d5a982e003`
//!   `profiles/rv64i-lab-v0/guests/fault-st-mis-w.expected.sexp`  `4a438ca7ea4a4e5151bd4b03cd426051c7d732889eda849d568794f88c7e019f`
//!   `profiles/rv64i-lab-v0/guests/fault-st-mis-w.s`  `a8e4b686e75bb63e187852063bf609bd7922dcca6f4bb15c3d99201cbda7dabe`
//!   `profiles/rv64i-lab-v0/guests/guest-control.expected.sexp`  `4caae2a18515bc4b479ca810df3edd2d23c534f19b8cb9afc081a97cb48485ac`
//!   `profiles/rv64i-lab-v0/guests/guest-control.s`  `497f63c79cd8e25918d845d5cc7d3430566b2f504a31cd33b2deb572f94694e6`
//!   `profiles/rv64i-lab-v0/guests/guest-no-device.expected.sexp`  `2be4382d503c302ed52b68335f6b52a4b8848aa80bfca4b96f503666305336b7`
//!   `profiles/rv64i-lab-v0/guests/guest-no-device.s`  `4f6d655d95eaf9e132a3c66ff71d65def1642ade2997f96f663829ce65db50a3`
//!   `profiles/rv64i-lab-v0/guests/it-alias-bound.expected.sexp`  `5d602f4e52567cca76696bbe1039da02a9f9b7539c4265c404f62f9e1445dcfe`
//!   `profiles/rv64i-lab-v0/guests/it-alias-bound.s`  `2f09ca9262b6bc236660c461b68be3a6d3c2a13f020751c7bfc18f54e0e7b39c`
//!   `profiles/rv64i-lab-v0/guests/it-fault-alias.expected.sexp`  `6ac459aa3f8c25b2be0287b3843ae465851364b994823c6fc9a0311aebef5b5d`
//!   `profiles/rv64i-lab-v0/guests/it-fault-alias.s`  `5ca3546f8346feb1bd4e75589a0276c5f25e280f51355618e399a5dab8f5e9cb`
//!   `profiles/rv64i-lab-v0/guests/it-fault-wrap-ld.expected.sexp`  `692412eae28fd42d2a5b2ed0da2019adc31e957bd6af201aa23ffd3ef8f82f48`
//!   `profiles/rv64i-lab-v0/guests/it-fault-wrap-ld.s`  `8a33575014793c4f23d8ce6e6e48f3eb3f2e833a2f5026d4d426627d33ece0e5`
//!   `profiles/rv64i-lab-v0/guests/it-fault-wrap-sd.expected.sexp`  `c129b45cc8aa897533dcd2921bf92617f8acccce92a55001181a53c2051da5d4`
//!   `profiles/rv64i-lab-v0/guests/it-fault-wrap-sd.s`  `b84984b4f170336c92639fe40336141a6fff6951024dad8df94c460b670aff9f`
//!   `profiles/rv64i-lab-v0/guests/it-fencei.expected.sexp`  `7bebe44f33685b9341e9a8e3496a8c33ce33f6c1114c4e09c2174bb3b6373ee0`
//!   `profiles/rv64i-lab-v0/guests/it-fencei.s`  `44471db1f1454d90484e182fe083101c9e9357e829e1c39a37c8536d496cbda5`
//!   `profiles/rv64i-lab-v0/guests/it-prio-jump.expected.sexp`  `4a1756d854e3fc2f6e7c7adcd675874327d5b837286f790d048e5dc301676ab9`
//!   `profiles/rv64i-lab-v0/guests/it-prio-jump.s`  `5c4c0442f763a484321617598885dc49c534505b60eada2a0499c930414a2206`
//!   `profiles/rv64i-lab-v0/guests/it-prio-load.expected.sexp`  `1bb9f68b7c3e8814afb3cbd5c49c936df2f324cb7a2601a58da2f74e5a7dc118`
//!   `profiles/rv64i-lab-v0/guests/it-prio-load.s`  `ad39fe5f0a602818f486e66ea50ac30be9fc8975da300250b10d050eebd7a05a`
//!   `profiles/rv64i-lab-v0/guests/it-progress-loop.expected.sexp`  `8318bacf7fb31c2c5f9df96b80c5d93cd19a7fd9af8244d3b9d50cf5f2c9b955`
//!   `profiles/rv64i-lab-v0/guests/it-progress-loop.s`  `98f034a39a435a823b639d7655b7213f591e30e6c166310626988973883a0f3f`
//!   `profiles/rv64i-lab-v0/guests/scope-alu.expected.sexp`  `51db1890cb3acf60b7215d48b816bc07159a4ebbea074c3614b927d885bec2da`
//!   `profiles/rv64i-lab-v0/guests/scope-alu.s`  `927382ca130c89032d35619086339e7afa7316ec7202ce947cc575e9717c3517`
//!   `profiles/rv64i-lab-v0/guests/scope-branch.expected.sexp`  `b43b2690339c94e03cd0114e6f7e09602d4da30c520a4350505fab1588697fb6`
//!   `profiles/rv64i-lab-v0/guests/scope-branch.s`  `856333d6109e300b0c68f050b183bd95fa1aff342fd8c76c9cfccf9c883eb7ab`
//!   `profiles/rv64i-lab-v0/guests/scope-ebreak.expected.sexp`  `b4b52ac8b1ee44af16bae685ac51ce6d8ba4df5c455ff886593a6c90ca976ab7`
//!   `profiles/rv64i-lab-v0/guests/scope-ebreak.s`  `0d2d4b6ee08a5120348887306c09029d20a35240cee44e42e2d2ac6fe06e6f10`
//!   `profiles/rv64i-lab-v0/guests/scope-ecall.expected.sexp`  `506b4697c318a5f13f94d60b55a62053399f3797e0f22deef38c2bafe743faa3`
//!   `profiles/rv64i-lab-v0/guests/scope-ecall.s`  `e35b711474b88ca35d593ff4227ed2129c22e8df7f2d5e75773bf2911272b23f`
//!   `profiles/rv64i-lab-v0/guests/scope-mem.expected.sexp`  `f2ea5a85940c9b779a15dd755136af75a4f5e8c4a34ae786a962a85bc28689de`
//!   `profiles/rv64i-lab-v0/guests/scope-mem.s`  `e30e3b0f9464a75e79fba148d6185acab64613b0a7ceffa3d7aa7fa4b56a6321`
//!   `profiles/rv64i-lab-v0/guests/smoke-arith.expected.sexp`  `d0c5b96125992bc58fb403173f8ff9839d827264a2cc39c70b87ac05b3f43f72`
//!   `profiles/rv64i-lab-v0/guests/smoke-arith.s`  `5bd4d210483ed8c7815e40acb1c113fadf815359a73dae5c3e944d34208760f9`
//!   `profiles/rv64i-lab-v0/guests/smoke-trap.expected.sexp`  `081ed9427c790df38822107188dd91b03847e92bcb0a722f420eb7e89a289e35`
//!   `profiles/rv64i-lab-v0/guests/smoke-trap.s`  `c9533287494eecf17ecd965070232331cfdefc2eb9af1fb36de644c9c819d216`
//! Generator: `scripts/gen_guests.py` (sha256 `890e429c7df36ab7ad781fce5579d1db6f877e4ab7a258417ec621802dddefa3`)
//!
//! Every data array below carries `#[rustfmt::skip]`: the emission is
//! byte-stable by construction (one entry per line), so regeneration and the
//! GUEST-GEN drift check compare bytes rustfmt never reorders.

/// The expected observations for one executed step of a guest: which register
/// writes the pinned specification-derived expectations declare, as
/// `(register index, value)` pairs ascending by index. An empty slice declares
/// the step writes nothing.
pub struct Expectation {
    /// The step's index in the executed trace.
    pub step: usize,
    /// The register writes the expectations declare for this step.
    pub writes: &'static [(u8, u64)],
}

#[rustfmt::skip]
static WORDS_SMOKE_ARITH: &[u32] = &[
    0x800000B7,
    0x0010811B,
    0xFFF00193,
    0x03F19213,
    0x03F25293,
    0x43F25313,
    0x0001839B,
    0x01F1941B,
    0x002084B3,
    0x00100513,
    0x01F51513,
    0x40953023,
];
#[rustfmt::skip]
static EXPECTED_SMOKE_ARITH: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0xFFFFFFFF80000000)] },
    Expectation { step: 1, writes: &[(2, 0xFFFFFFFF80000001)] },
    Expectation { step: 2, writes: &[(3, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 3, writes: &[(4, 0x8000000000000000)] },
    Expectation { step: 4, writes: &[(5, 0x0000000000000001)] },
    Expectation { step: 5, writes: &[(6, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 6, writes: &[(7, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 7, writes: &[(8, 0xFFFFFFFF80000000)] },
    Expectation { step: 8, writes: &[(9, 0xFFFFFFFF00000001)] },
    Expectation { step: 9, writes: &[(10, 0x0000000000000001)] },
    Expectation { step: 10, writes: &[(10, 0x0000000080000000)] },
    Expectation { step: 11, writes: &[] },
];

#[rustfmt::skip]
static WORDS_GUEST_CONTROL: &[u32] = &[
    0x00300093,
    0xFFF08093,
    0xFE009EE3,
    0x00C002EF,
    0x55500313,
    0x00130313,
    0x00700393,
    0x00000497,
    0x00D48567,
    0x3E700693,
    0x02A00593,
    0x00100613,
];
#[rustfmt::skip]
static EXPECTED_GUEST_CONTROL: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000000000003)] },
    Expectation { step: 1, writes: &[(1, 0x0000000000000002)] },
    Expectation { step: 2, writes: &[] },
    Expectation { step: 3, writes: &[(1, 0x0000000000000001)] },
    Expectation { step: 4, writes: &[] },
    Expectation { step: 5, writes: &[(1, 0x0000000000000000)] },
    Expectation { step: 6, writes: &[] },
    Expectation { step: 7, writes: &[(5, 0x0000000080000010)] },
    Expectation { step: 8, writes: &[(7, 0x0000000000000007)] },
    Expectation { step: 9, writes: &[(9, 0x000000008000001C)] },
    Expectation { step: 10, writes: &[(10, 0x0000000080000024)] },
    Expectation { step: 11, writes: &[(11, 0x000000000000002A)] },
    Expectation { step: 12, writes: &[(12, 0x0000000000000001)] },
];
#[rustfmt::skip]
static NEVER_WRITTEN_GUEST_CONTROL: &[u8] = &[6, 13];

#[rustfmt::skip]
static WORDS_SMOKE_TRAP: &[u32] = &[
    0x00100513,
    0x01F51513,
    0x40152083,
];
#[rustfmt::skip]
static EXPECTED_SMOKE_TRAP: &[Expectation] = &[
    Expectation { step: 0, writes: &[(10, 0x0000000000000001)] },
    Expectation { step: 1, writes: &[(10, 0x0000000080000000)] },
    Expectation { step: 2, writes: &[] },
];
#[rustfmt::skip]
static NEVER_WRITTEN_SMOKE_TRAP: &[u8] = &[1];

#[rustfmt::skip]
static WORDS_GUEST_NO_DEVICE: &[u32] = &[
    0x00100513,
    0x01951513,
    0x0000C5B7,
    0xFF858593,
    0x00B50533,
    0x00053083,
];
#[rustfmt::skip]
static EXPECTED_GUEST_NO_DEVICE: &[Expectation] = &[
    Expectation { step: 0, writes: &[(10, 0x0000000000000001)] },
    Expectation { step: 1, writes: &[(10, 0x0000000002000000)] },
    Expectation { step: 2, writes: &[(11, 0x000000000000C000)] },
    Expectation { step: 3, writes: &[(11, 0x000000000000BFF8)] },
    Expectation { step: 4, writes: &[(10, 0x000000000200BFF8)] },
    Expectation { step: 5, writes: &[] },
];
#[rustfmt::skip]
static NEVER_WRITTEN_GUEST_NO_DEVICE: &[u8] = &[1];

#[rustfmt::skip]
static WORDS_SCOPE_ALU: &[u32] = &[
    0xFFF00093,
    0x65400113,
    0x47000193,
    0x80000237,
    0x02000293,
    0x00317333,
    0x003163B3,
    0x00314433,
    0xFFF27493,
    0x7FF26513,
    0xFFF24593,
    0x0020A633,
    0x00100693,
    0x0020B6B3,
    0x00122713,
    0x00100793,
    0x00123793,
    0xFFF23813,
    0x403108B3,
    0x40218933,
    0x002199B3,
    0x00225A33,
    0x40225AB3,
    0x00220B3B,
    0x40220BBB,
    0x00511C3B,
    0x00225CBB,
    0x40225D3B,
    0x01F25D9B,
    0x41F25E1B,
    0x0FF0000F,
];
#[rustfmt::skip]
static EXPECTED_SCOPE_ALU: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 1, writes: &[(2, 0x0000000000000654)] },
    Expectation { step: 2, writes: &[(3, 0x0000000000000470)] },
    Expectation { step: 3, writes: &[(4, 0xFFFFFFFF80000000)] },
    Expectation { step: 4, writes: &[(5, 0x0000000000000020)] },
    Expectation { step: 5, writes: &[(6, 0x0000000000000450)] },
    Expectation { step: 6, writes: &[(7, 0x0000000000000674)] },
    Expectation { step: 7, writes: &[(8, 0x0000000000000224)] },
    Expectation { step: 8, writes: &[(9, 0xFFFFFFFF80000000)] },
    Expectation { step: 9, writes: &[(10, 0xFFFFFFFF800007FF)] },
    Expectation { step: 10, writes: &[(11, 0x000000007FFFFFFF)] },
    Expectation { step: 11, writes: &[(12, 0x0000000000000001)] },
    Expectation { step: 12, writes: &[(13, 0x0000000000000001)] },
    Expectation { step: 13, writes: &[(13, 0x0000000000000000)] },
    Expectation { step: 14, writes: &[(14, 0x0000000000000001)] },
    Expectation { step: 15, writes: &[(15, 0x0000000000000001)] },
    Expectation { step: 16, writes: &[(15, 0x0000000000000000)] },
    Expectation { step: 17, writes: &[(16, 0x0000000000000001)] },
    Expectation { step: 18, writes: &[(17, 0x00000000000001E4)] },
    Expectation { step: 19, writes: &[(18, 0xFFFFFFFFFFFFFE1C)] },
    Expectation { step: 20, writes: &[(19, 0x0000000047000000)] },
    Expectation { step: 21, writes: &[(20, 0x00000FFFFFFFF800)] },
    Expectation { step: 22, writes: &[(21, 0xFFFFFFFFFFFFF800)] },
    Expectation { step: 23, writes: &[(22, 0xFFFFFFFF80000654)] },
    Expectation { step: 24, writes: &[(23, 0x000000007FFFF9AC)] },
    Expectation { step: 25, writes: &[(24, 0x0000000000000654)] },
    Expectation { step: 26, writes: &[(25, 0x0000000000000800)] },
    Expectation { step: 27, writes: &[(26, 0xFFFFFFFFFFFFF800)] },
    Expectation { step: 28, writes: &[(27, 0x0000000000000001)] },
    Expectation { step: 29, writes: &[(28, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 30, writes: &[] },
];

#[rustfmt::skip]
static WORDS_SCOPE_MEM: &[u32] = &[
    0x00100513,
    0x01F51513,
    0x80FFF0B7,
    0x7F000113,
    0x0020E0B3,
    0x02009093,
    0x80FFF1B7,
    0x0021E1B3,
    0x02019193,
    0x0201D193,
    0x0030E3B3,
    0x40753023,
    0x40050583,
    0x40154603,
    0x40251683,
    0x40255703,
    0x40052783,
    0x40456803,
    0x40053883,
    0x40052003,
    0xFFF00213,
    0x40450823,
    0x41053903,
    0x40451C23,
    0x41853983,
    0x42452023,
    0x42053A03,
    0x42752423,
    0x42853A83,
];
#[rustfmt::skip]
static EXPECTED_SCOPE_MEM: &[Expectation] = &[
    Expectation { step: 0, writes: &[(10, 0x0000000000000001)] },
    Expectation { step: 1, writes: &[(10, 0x0000000080000000)] },
    Expectation { step: 2, writes: &[(1, 0xFFFFFFFF80FFF000)] },
    Expectation { step: 3, writes: &[(2, 0x00000000000007F0)] },
    Expectation { step: 4, writes: &[(1, 0xFFFFFFFF80FFF7F0)] },
    Expectation { step: 5, writes: &[(1, 0x80FFF7F000000000)] },
    Expectation { step: 6, writes: &[(3, 0xFFFFFFFF80FFF000)] },
    Expectation { step: 7, writes: &[(3, 0xFFFFFFFF80FFF7F0)] },
    Expectation { step: 8, writes: &[(3, 0x80FFF7F000000000)] },
    Expectation { step: 9, writes: &[(3, 0x0000000080FFF7F0)] },
    Expectation { step: 10, writes: &[(7, 0x80FFF7F080FFF7F0)] },
    Expectation { step: 11, writes: &[] },
    Expectation { step: 12, writes: &[(11, 0xFFFFFFFFFFFFFFF0)] },
    Expectation { step: 13, writes: &[(12, 0x00000000000000F7)] },
    Expectation { step: 14, writes: &[(13, 0xFFFFFFFFFFFF80FF)] },
    Expectation { step: 15, writes: &[(14, 0x00000000000080FF)] },
    Expectation { step: 16, writes: &[(15, 0xFFFFFFFF80FFF7F0)] },
    Expectation { step: 17, writes: &[(16, 0x0000000080FFF7F0)] },
    Expectation { step: 18, writes: &[(17, 0x80FFF7F080FFF7F0)] },
    Expectation { step: 19, writes: &[] },
    Expectation { step: 20, writes: &[(4, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 21, writes: &[] },
    Expectation { step: 22, writes: &[(18, 0x00000000000000FF)] },
    Expectation { step: 23, writes: &[] },
    Expectation { step: 24, writes: &[(19, 0x000000000000FFFF)] },
    Expectation { step: 25, writes: &[] },
    Expectation { step: 26, writes: &[(20, 0x00000000FFFFFFFF)] },
    Expectation { step: 27, writes: &[] },
    Expectation { step: 28, writes: &[(21, 0x0000000080FFF7F0)] },
];

#[rustfmt::skip]
static WORDS_SCOPE_BRANCH: &[u32] = &[
    0x00500093,
    0x00500113,
    0xFFF00193,
    0x00208463,
    0x00100A13,
    0x00308463,
    0x00100213,
    0x0011C463,
    0x00100A93,
    0x0030C463,
    0x00100293,
    0x0030D463,
    0x00100B13,
    0x0011D463,
    0x00100313,
    0x0030E463,
    0x00100B93,
    0x0011E463,
    0x00100393,
    0x0011F463,
    0x00100C13,
    0x0030F463,
    0x00100413,
    0x00100493,
];
#[rustfmt::skip]
static EXPECTED_SCOPE_BRANCH: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000000000005)] },
    Expectation { step: 1, writes: &[(2, 0x0000000000000005)] },
    Expectation { step: 2, writes: &[(3, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 3, writes: &[] },
    Expectation { step: 4, writes: &[] },
    Expectation { step: 5, writes: &[(4, 0x0000000000000001)] },
    Expectation { step: 6, writes: &[] },
    Expectation { step: 7, writes: &[] },
    Expectation { step: 8, writes: &[(5, 0x0000000000000001)] },
    Expectation { step: 9, writes: &[] },
    Expectation { step: 10, writes: &[] },
    Expectation { step: 11, writes: &[(6, 0x0000000000000001)] },
    Expectation { step: 12, writes: &[] },
    Expectation { step: 13, writes: &[] },
    Expectation { step: 14, writes: &[(7, 0x0000000000000001)] },
    Expectation { step: 15, writes: &[] },
    Expectation { step: 16, writes: &[] },
    Expectation { step: 17, writes: &[(8, 0x0000000000000001)] },
    Expectation { step: 18, writes: &[(9, 0x0000000000000001)] },
];
#[rustfmt::skip]
static NEVER_WRITTEN_SCOPE_BRANCH: &[u8] = &[20, 21, 22, 23, 24];

#[rustfmt::skip]
static WORDS_SCOPE_ECALL: &[u32] = &[
    0x00700093,
    0x00000073,
];
#[rustfmt::skip]
static EXPECTED_SCOPE_ECALL: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000000000007)] },
    Expectation { step: 1, writes: &[] },
];

#[rustfmt::skip]
static WORDS_SCOPE_EBREAK: &[u32] = &[
    0x00900093,
    0x00100073,
];
#[rustfmt::skip]
static EXPECTED_SCOPE_EBREAK: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000000000009)] },
    Expectation { step: 1, writes: &[] },
];

#[rustfmt::skip]
static WORDS_BOUND_SHIFT: &[u32] = &[
    0x80000437,
    0x02041413,
    0x00140413,
    0x00045493,
    0x00145493,
    0x00245493,
    0x00345493,
    0x00445493,
    0x00545493,
    0x00645493,
    0x00745493,
    0x00845493,
    0x00945493,
    0x00A45493,
    0x00B45493,
    0x00C45493,
    0x00D45493,
    0x00E45493,
    0x00F45493,
    0x01045493,
    0x01145493,
    0x01245493,
    0x01345493,
    0x01445493,
    0x01545493,
    0x01645493,
    0x01745493,
    0x01845493,
    0x01945493,
    0x01A45493,
    0x01B45493,
    0x01C45493,
    0x01D45493,
    0x01E45493,
    0x01F45493,
    0x02045493,
    0x02145493,
    0x02245493,
    0x02345493,
    0x02445493,
    0x02545493,
    0x02645493,
    0x02745493,
    0x02845493,
    0x02945493,
    0x02A45493,
    0x02B45493,
    0x02C45493,
    0x02D45493,
    0x02E45493,
    0x02F45493,
    0x03045493,
    0x03145493,
    0x03245493,
    0x03345493,
    0x03445493,
    0x03545493,
    0x03645493,
    0x03745493,
    0x03845493,
    0x03945493,
    0x03A45493,
    0x03B45493,
    0x03C45493,
    0x03D45493,
    0x03E45493,
    0x03F45493,
    0x40045A13,
    0x40145A13,
    0x40245A13,
    0x40445A13,
    0x40845A13,
    0x41045A13,
    0x42045A13,
    0x43F45A13,
    0x00041A93,
    0x00141A93,
    0x00241A93,
    0x00441A93,
    0x00841A93,
    0x01041A93,
    0x02041A93,
    0x03F41A93,
    0x04000513,
    0xFFF00593,
    0x00A455B3,
    0xFFF00613,
    0x00C416B3,
    0x40C45733,
];
#[rustfmt::skip]
static EXPECTED_BOUND_SHIFT: &[Expectation] = &[
    Expectation { step: 0, writes: &[(8, 0xFFFFFFFF80000000)] },
    Expectation { step: 1, writes: &[(8, 0x8000000000000000)] },
    Expectation { step: 2, writes: &[(8, 0x8000000000000001)] },
    Expectation { step: 3, writes: &[(9, 0x8000000000000001)] },
    Expectation { step: 4, writes: &[(9, 0x4000000000000000)] },
    Expectation { step: 5, writes: &[(9, 0x2000000000000000)] },
    Expectation { step: 6, writes: &[(9, 0x1000000000000000)] },
    Expectation { step: 7, writes: &[(9, 0x0800000000000000)] },
    Expectation { step: 8, writes: &[(9, 0x0400000000000000)] },
    Expectation { step: 9, writes: &[(9, 0x0200000000000000)] },
    Expectation { step: 10, writes: &[(9, 0x0100000000000000)] },
    Expectation { step: 11, writes: &[(9, 0x0080000000000000)] },
    Expectation { step: 12, writes: &[(9, 0x0040000000000000)] },
    Expectation { step: 13, writes: &[(9, 0x0020000000000000)] },
    Expectation { step: 14, writes: &[(9, 0x0010000000000000)] },
    Expectation { step: 15, writes: &[(9, 0x0008000000000000)] },
    Expectation { step: 16, writes: &[(9, 0x0004000000000000)] },
    Expectation { step: 17, writes: &[(9, 0x0002000000000000)] },
    Expectation { step: 18, writes: &[(9, 0x0001000000000000)] },
    Expectation { step: 19, writes: &[(9, 0x0000800000000000)] },
    Expectation { step: 20, writes: &[(9, 0x0000400000000000)] },
    Expectation { step: 21, writes: &[(9, 0x0000200000000000)] },
    Expectation { step: 22, writes: &[(9, 0x0000100000000000)] },
    Expectation { step: 23, writes: &[(9, 0x0000080000000000)] },
    Expectation { step: 24, writes: &[(9, 0x0000040000000000)] },
    Expectation { step: 25, writes: &[(9, 0x0000020000000000)] },
    Expectation { step: 26, writes: &[(9, 0x0000010000000000)] },
    Expectation { step: 27, writes: &[(9, 0x0000008000000000)] },
    Expectation { step: 28, writes: &[(9, 0x0000004000000000)] },
    Expectation { step: 29, writes: &[(9, 0x0000002000000000)] },
    Expectation { step: 30, writes: &[(9, 0x0000001000000000)] },
    Expectation { step: 31, writes: &[(9, 0x0000000800000000)] },
    Expectation { step: 32, writes: &[(9, 0x0000000400000000)] },
    Expectation { step: 33, writes: &[(9, 0x0000000200000000)] },
    Expectation { step: 34, writes: &[(9, 0x0000000100000000)] },
    Expectation { step: 35, writes: &[(9, 0x0000000080000000)] },
    Expectation { step: 36, writes: &[(9, 0x0000000040000000)] },
    Expectation { step: 37, writes: &[(9, 0x0000000020000000)] },
    Expectation { step: 38, writes: &[(9, 0x0000000010000000)] },
    Expectation { step: 39, writes: &[(9, 0x0000000008000000)] },
    Expectation { step: 40, writes: &[(9, 0x0000000004000000)] },
    Expectation { step: 41, writes: &[(9, 0x0000000002000000)] },
    Expectation { step: 42, writes: &[(9, 0x0000000001000000)] },
    Expectation { step: 43, writes: &[(9, 0x0000000000800000)] },
    Expectation { step: 44, writes: &[(9, 0x0000000000400000)] },
    Expectation { step: 45, writes: &[(9, 0x0000000000200000)] },
    Expectation { step: 46, writes: &[(9, 0x0000000000100000)] },
    Expectation { step: 47, writes: &[(9, 0x0000000000080000)] },
    Expectation { step: 48, writes: &[(9, 0x0000000000040000)] },
    Expectation { step: 49, writes: &[(9, 0x0000000000020000)] },
    Expectation { step: 50, writes: &[(9, 0x0000000000010000)] },
    Expectation { step: 51, writes: &[(9, 0x0000000000008000)] },
    Expectation { step: 52, writes: &[(9, 0x0000000000004000)] },
    Expectation { step: 53, writes: &[(9, 0x0000000000002000)] },
    Expectation { step: 54, writes: &[(9, 0x0000000000001000)] },
    Expectation { step: 55, writes: &[(9, 0x0000000000000800)] },
    Expectation { step: 56, writes: &[(9, 0x0000000000000400)] },
    Expectation { step: 57, writes: &[(9, 0x0000000000000200)] },
    Expectation { step: 58, writes: &[(9, 0x0000000000000100)] },
    Expectation { step: 59, writes: &[(9, 0x0000000000000080)] },
    Expectation { step: 60, writes: &[(9, 0x0000000000000040)] },
    Expectation { step: 61, writes: &[(9, 0x0000000000000020)] },
    Expectation { step: 62, writes: &[(9, 0x0000000000000010)] },
    Expectation { step: 63, writes: &[(9, 0x0000000000000008)] },
    Expectation { step: 64, writes: &[(9, 0x0000000000000004)] },
    Expectation { step: 65, writes: &[(9, 0x0000000000000002)] },
    Expectation { step: 66, writes: &[(9, 0x0000000000000001)] },
    Expectation { step: 67, writes: &[(20, 0x8000000000000001)] },
    Expectation { step: 68, writes: &[(20, 0xC000000000000000)] },
    Expectation { step: 69, writes: &[(20, 0xE000000000000000)] },
    Expectation { step: 70, writes: &[(20, 0xF800000000000000)] },
    Expectation { step: 71, writes: &[(20, 0xFF80000000000000)] },
    Expectation { step: 72, writes: &[(20, 0xFFFF800000000000)] },
    Expectation { step: 73, writes: &[(20, 0xFFFFFFFF80000000)] },
    Expectation { step: 74, writes: &[(20, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 75, writes: &[(21, 0x8000000000000001)] },
    Expectation { step: 76, writes: &[(21, 0x0000000000000002)] },
    Expectation { step: 77, writes: &[(21, 0x0000000000000004)] },
    Expectation { step: 78, writes: &[(21, 0x0000000000000010)] },
    Expectation { step: 79, writes: &[(21, 0x0000000000000100)] },
    Expectation { step: 80, writes: &[(21, 0x0000000000010000)] },
    Expectation { step: 81, writes: &[(21, 0x0000000100000000)] },
    Expectation { step: 82, writes: &[(21, 0x8000000000000000)] },
    Expectation { step: 83, writes: &[(10, 0x0000000000000040)] },
    Expectation { step: 84, writes: &[(11, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 85, writes: &[(11, 0x8000000000000001)] },
    Expectation { step: 86, writes: &[(12, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 87, writes: &[(13, 0x8000000000000000)] },
    Expectation { step: 88, writes: &[(14, 0xFFFFFFFFFFFFFFFF)] },
];

#[rustfmt::skip]
static WORDS_BOUND_SHIFTW: &[u32] = &[
    0x80000437,
    0x00140413,
    0x4004549B,
    0x4014549B,
    0x4024549B,
    0x4034549B,
    0x4044549B,
    0x4054549B,
    0x4064549B,
    0x4074549B,
    0x4084549B,
    0x4094549B,
    0x40A4549B,
    0x40B4549B,
    0x40C4549B,
    0x40D4549B,
    0x40E4549B,
    0x40F4549B,
    0x4104549B,
    0x4114549B,
    0x4124549B,
    0x4134549B,
    0x4144549B,
    0x4154549B,
    0x4164549B,
    0x4174549B,
    0x4184549B,
    0x4194549B,
    0x41A4549B,
    0x41B4549B,
    0x41C4549B,
    0x41D4549B,
    0x41E4549B,
    0x41F4549B,
    0x00045A1B,
    0x00145A1B,
    0x00245A1B,
    0x00445A1B,
    0x00845A1B,
    0x01045A1B,
    0x01F45A1B,
    0x00041A9B,
    0x00141A9B,
    0x00241A9B,
    0x00441A9B,
    0x00841A9B,
    0x01041A9B,
    0x01F41A9B,
    0x06000513,
    0x00A45633,
    0x00100593,
    0x00A455BB,
    0xFFF00693,
    0x00D4173B,
    0x40D457BB,
];
#[rustfmt::skip]
static EXPECTED_BOUND_SHIFTW: &[Expectation] = &[
    Expectation { step: 0, writes: &[(8, 0xFFFFFFFF80000000)] },
    Expectation { step: 1, writes: &[(8, 0xFFFFFFFF80000001)] },
    Expectation { step: 2, writes: &[(9, 0xFFFFFFFF80000001)] },
    Expectation { step: 3, writes: &[(9, 0xFFFFFFFFC0000000)] },
    Expectation { step: 4, writes: &[(9, 0xFFFFFFFFE0000000)] },
    Expectation { step: 5, writes: &[(9, 0xFFFFFFFFF0000000)] },
    Expectation { step: 6, writes: &[(9, 0xFFFFFFFFF8000000)] },
    Expectation { step: 7, writes: &[(9, 0xFFFFFFFFFC000000)] },
    Expectation { step: 8, writes: &[(9, 0xFFFFFFFFFE000000)] },
    Expectation { step: 9, writes: &[(9, 0xFFFFFFFFFF000000)] },
    Expectation { step: 10, writes: &[(9, 0xFFFFFFFFFF800000)] },
    Expectation { step: 11, writes: &[(9, 0xFFFFFFFFFFC00000)] },
    Expectation { step: 12, writes: &[(9, 0xFFFFFFFFFFE00000)] },
    Expectation { step: 13, writes: &[(9, 0xFFFFFFFFFFF00000)] },
    Expectation { step: 14, writes: &[(9, 0xFFFFFFFFFFF80000)] },
    Expectation { step: 15, writes: &[(9, 0xFFFFFFFFFFFC0000)] },
    Expectation { step: 16, writes: &[(9, 0xFFFFFFFFFFFE0000)] },
    Expectation { step: 17, writes: &[(9, 0xFFFFFFFFFFFF0000)] },
    Expectation { step: 18, writes: &[(9, 0xFFFFFFFFFFFF8000)] },
    Expectation { step: 19, writes: &[(9, 0xFFFFFFFFFFFFC000)] },
    Expectation { step: 20, writes: &[(9, 0xFFFFFFFFFFFFE000)] },
    Expectation { step: 21, writes: &[(9, 0xFFFFFFFFFFFFF000)] },
    Expectation { step: 22, writes: &[(9, 0xFFFFFFFFFFFFF800)] },
    Expectation { step: 23, writes: &[(9, 0xFFFFFFFFFFFFFC00)] },
    Expectation { step: 24, writes: &[(9, 0xFFFFFFFFFFFFFE00)] },
    Expectation { step: 25, writes: &[(9, 0xFFFFFFFFFFFFFF00)] },
    Expectation { step: 26, writes: &[(9, 0xFFFFFFFFFFFFFF80)] },
    Expectation { step: 27, writes: &[(9, 0xFFFFFFFFFFFFFFC0)] },
    Expectation { step: 28, writes: &[(9, 0xFFFFFFFFFFFFFFE0)] },
    Expectation { step: 29, writes: &[(9, 0xFFFFFFFFFFFFFFF0)] },
    Expectation { step: 30, writes: &[(9, 0xFFFFFFFFFFFFFFF8)] },
    Expectation { step: 31, writes: &[(9, 0xFFFFFFFFFFFFFFFC)] },
    Expectation { step: 32, writes: &[(9, 0xFFFFFFFFFFFFFFFE)] },
    Expectation { step: 33, writes: &[(9, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 34, writes: &[(20, 0xFFFFFFFF80000001)] },
    Expectation { step: 35, writes: &[(20, 0x0000000040000000)] },
    Expectation { step: 36, writes: &[(20, 0x0000000020000000)] },
    Expectation { step: 37, writes: &[(20, 0x0000000008000000)] },
    Expectation { step: 38, writes: &[(20, 0x0000000000800000)] },
    Expectation { step: 39, writes: &[(20, 0x0000000000008000)] },
    Expectation { step: 40, writes: &[(20, 0x0000000000000001)] },
    Expectation { step: 41, writes: &[(21, 0xFFFFFFFF80000001)] },
    Expectation { step: 42, writes: &[(21, 0x0000000000000002)] },
    Expectation { step: 43, writes: &[(21, 0x0000000000000004)] },
    Expectation { step: 44, writes: &[(21, 0x0000000000000010)] },
    Expectation { step: 45, writes: &[(21, 0x0000000000000100)] },
    Expectation { step: 46, writes: &[(21, 0x0000000000010000)] },
    Expectation { step: 47, writes: &[(21, 0xFFFFFFFF80000000)] },
    Expectation { step: 48, writes: &[(10, 0x0000000000000060)] },
    Expectation { step: 49, writes: &[(12, 0x00000000FFFFFFFF)] },
    Expectation { step: 50, writes: &[(11, 0x0000000000000001)] },
    Expectation { step: 51, writes: &[(11, 0xFFFFFFFF80000001)] },
    Expectation { step: 52, writes: &[(13, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 53, writes: &[(14, 0xFFFFFFFF80000000)] },
    Expectation { step: 54, writes: &[(15, 0xFFFFFFFFFFFFFFFF)] },
];

#[rustfmt::skip]
static WORDS_BOUND_ARITH: &[u32] = &[
    0xFFF00093,
    0x0010D093,
    0x00100113,
    0x03F11113,
    0x00100213,
    0x004081B3,
    0x404102B3,
    0x00108333,
    0xFFF10393,
    0x80000413,
    0x7FF00493,
    0xDEADB537,
    0x7EF50513,
    0x02051513,
    0xFFF00593,
    0x0215D593,
    0x00B56533,
    0x0015061B,
    0xFFF1069B,
    0x0045073B,
    0x404107BB,
    0x40A2083B,
    0x001128B3,
    0x00100913,
    0x00113933,
    0x002039B3,
    0x80012A13,
    0xFFF03A93,
    0x7FFFFB37,
    0x80000B97,
    0x7FFFFC17,
];
#[rustfmt::skip]
static EXPECTED_BOUND_ARITH: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 1, writes: &[(1, 0x7FFFFFFFFFFFFFFF)] },
    Expectation { step: 2, writes: &[(2, 0x0000000000000001)] },
    Expectation { step: 3, writes: &[(2, 0x8000000000000000)] },
    Expectation { step: 4, writes: &[(4, 0x0000000000000001)] },
    Expectation { step: 5, writes: &[(3, 0x8000000000000000)] },
    Expectation { step: 6, writes: &[(5, 0x7FFFFFFFFFFFFFFF)] },
    Expectation { step: 7, writes: &[(6, 0xFFFFFFFFFFFFFFFE)] },
    Expectation { step: 8, writes: &[(7, 0x7FFFFFFFFFFFFFFF)] },
    Expectation { step: 9, writes: &[(8, 0xFFFFFFFFFFFFF800)] },
    Expectation { step: 10, writes: &[(9, 0x00000000000007FF)] },
    Expectation { step: 11, writes: &[(10, 0xFFFFFFFFDEADB000)] },
    Expectation { step: 12, writes: &[(10, 0xFFFFFFFFDEADB7EF)] },
    Expectation { step: 13, writes: &[(10, 0xDEADB7EF00000000)] },
    Expectation { step: 14, writes: &[(11, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 15, writes: &[(11, 0x000000007FFFFFFF)] },
    Expectation { step: 16, writes: &[(10, 0xDEADB7EF7FFFFFFF)] },
    Expectation { step: 17, writes: &[(12, 0xFFFFFFFF80000000)] },
    Expectation { step: 18, writes: &[(13, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 19, writes: &[(14, 0xFFFFFFFF80000000)] },
    Expectation { step: 20, writes: &[(15, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 21, writes: &[(16, 0xFFFFFFFF80000002)] },
    Expectation { step: 22, writes: &[(17, 0x0000000000000001)] },
    Expectation { step: 23, writes: &[(18, 0x0000000000000001)] },
    Expectation { step: 24, writes: &[(18, 0x0000000000000000)] },
    Expectation { step: 25, writes: &[(19, 0x0000000000000001)] },
    Expectation { step: 26, writes: &[(20, 0x0000000000000001)] },
    Expectation { step: 27, writes: &[(21, 0x0000000000000001)] },
    Expectation { step: 28, writes: &[(22, 0x000000007FFFF000)] },
    Expectation { step: 29, writes: &[(23, 0x0000000000000074)] },
    Expectation { step: 30, writes: &[(24, 0x00000000FFFFF078)] },
];

#[rustfmt::skip]
static WORDS_BOUND_EXT: &[u32] = &[
    0x00100513,
    0x01F51513,
    0x07F00093,
    0x08000113,
    0xFFF00193,
    0x00008237,
    0xFFF20213,
    0x000082B7,
    0xFFF00313,
    0x02135313,
    0x00100393,
    0x01F39393,
    0x18000413,
    0xFFFF84B7,
    0x40150023,
    0x402500A3,
    0x40350123,
    0x40451423,
    0x40551523,
    0x40351623,
    0x40652823,
    0x40752A23,
    0x40352C23,
    0x40050583,
    0x40150603,
    0x40154683,
    0x40250703,
    0x40254783,
    0x40851803,
    0x40A51883,
    0x40A55903,
    0x40C51983,
    0x40C55A03,
    0x41052A83,
    0x41452B03,
    0x41456B83,
    0x41852C03,
    0x41856C83,
    0x400501A3,
    0xFFF00D13,
    0x40350D03,
    0x42850023,
    0x42054D83,
    0x42951423,
    0x42855E03,
    0x42952823,
    0x43056E83,
];
#[rustfmt::skip]
static EXPECTED_BOUND_EXT: &[Expectation] = &[
    Expectation { step: 0, writes: &[(10, 0x0000000000000001)] },
    Expectation { step: 1, writes: &[(10, 0x0000000080000000)] },
    Expectation { step: 2, writes: &[(1, 0x000000000000007F)] },
    Expectation { step: 3, writes: &[(2, 0x0000000000000080)] },
    Expectation { step: 4, writes: &[(3, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 5, writes: &[(4, 0x0000000000008000)] },
    Expectation { step: 6, writes: &[(4, 0x0000000000007FFF)] },
    Expectation { step: 7, writes: &[(5, 0x0000000000008000)] },
    Expectation { step: 8, writes: &[(6, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 9, writes: &[(6, 0x000000007FFFFFFF)] },
    Expectation { step: 10, writes: &[(7, 0x0000000000000001)] },
    Expectation { step: 11, writes: &[(7, 0x0000000080000000)] },
    Expectation { step: 12, writes: &[(8, 0x0000000000000180)] },
    Expectation { step: 13, writes: &[(9, 0xFFFFFFFFFFFF8000)] },
    Expectation { step: 14, writes: &[] },
    Expectation { step: 15, writes: &[] },
    Expectation { step: 16, writes: &[] },
    Expectation { step: 17, writes: &[] },
    Expectation { step: 18, writes: &[] },
    Expectation { step: 19, writes: &[] },
    Expectation { step: 20, writes: &[] },
    Expectation { step: 21, writes: &[] },
    Expectation { step: 22, writes: &[] },
    Expectation { step: 23, writes: &[(11, 0x000000000000007F)] },
    Expectation { step: 24, writes: &[(12, 0xFFFFFFFFFFFFFF80)] },
    Expectation { step: 25, writes: &[(13, 0x0000000000000080)] },
    Expectation { step: 26, writes: &[(14, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 27, writes: &[(15, 0x00000000000000FF)] },
    Expectation { step: 28, writes: &[(16, 0x0000000000007FFF)] },
    Expectation { step: 29, writes: &[(17, 0xFFFFFFFFFFFF8000)] },
    Expectation { step: 30, writes: &[(18, 0x0000000000008000)] },
    Expectation { step: 31, writes: &[(19, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 32, writes: &[(20, 0x000000000000FFFF)] },
    Expectation { step: 33, writes: &[(21, 0x000000007FFFFFFF)] },
    Expectation { step: 34, writes: &[(22, 0xFFFFFFFF80000000)] },
    Expectation { step: 35, writes: &[(23, 0x0000000080000000)] },
    Expectation { step: 36, writes: &[(24, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 37, writes: &[(25, 0x00000000FFFFFFFF)] },
    Expectation { step: 38, writes: &[] },
    Expectation { step: 39, writes: &[(26, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 40, writes: &[(26, 0x0000000000000000)] },
    Expectation { step: 41, writes: &[] },
    Expectation { step: 42, writes: &[(27, 0x0000000000000080)] },
    Expectation { step: 43, writes: &[] },
    Expectation { step: 44, writes: &[(28, 0x0000000000008000)] },
    Expectation { step: 45, writes: &[] },
    Expectation { step: 46, writes: &[(29, 0x00000000FFFF8000)] },
];

#[rustfmt::skip]
static WORDS_BOUND_ALIAS: &[u32] = &[
    0x00100513,
    0x01F51513,
    0x040300B7,
    0x20108093,
    0x08070137,
    0x60510113,
    0x02011113,
    0x001160B3,
    0x40153023,
    0x40054583,
    0x40154603,
    0x40254683,
    0x40354703,
    0x40454783,
    0x40554803,
    0x40654883,
    0x40754903,
    0x40153423,
    0x0AA00193,
    0x403505A3,
    0x4CD00213,
    0x40451723,
    0x40853983,
    0x00500A13,
    0x014A0A33,
    0x00700A93,
    0x415A8AB3,
    0x00100B13,
    0x016B2B33,
    0x02100B93,
    0x017B9BB3,
    0x40050C13,
    0x000C0C03,
    0xFFF00013,
    0x40153823,
    0x40052823,
    0x41053C83,
];
#[rustfmt::skip]
static EXPECTED_BOUND_ALIAS: &[Expectation] = &[
    Expectation { step: 0, writes: &[(10, 0x0000000000000001)] },
    Expectation { step: 1, writes: &[(10, 0x0000000080000000)] },
    Expectation { step: 2, writes: &[(1, 0x0000000004030000)] },
    Expectation { step: 3, writes: &[(1, 0x0000000004030201)] },
    Expectation { step: 4, writes: &[(2, 0x0000000008070000)] },
    Expectation { step: 5, writes: &[(2, 0x0000000008070605)] },
    Expectation { step: 6, writes: &[(2, 0x0807060500000000)] },
    Expectation { step: 7, writes: &[(1, 0x0807060504030201)] },
    Expectation { step: 8, writes: &[] },
    Expectation { step: 9, writes: &[(11, 0x0000000000000001)] },
    Expectation { step: 10, writes: &[(12, 0x0000000000000002)] },
    Expectation { step: 11, writes: &[(13, 0x0000000000000003)] },
    Expectation { step: 12, writes: &[(14, 0x0000000000000004)] },
    Expectation { step: 13, writes: &[(15, 0x0000000000000005)] },
    Expectation { step: 14, writes: &[(16, 0x0000000000000006)] },
    Expectation { step: 15, writes: &[(17, 0x0000000000000007)] },
    Expectation { step: 16, writes: &[(18, 0x0000000000000008)] },
    Expectation { step: 17, writes: &[] },
    Expectation { step: 18, writes: &[(3, 0x00000000000000AA)] },
    Expectation { step: 19, writes: &[] },
    Expectation { step: 20, writes: &[(4, 0x00000000000004CD)] },
    Expectation { step: 21, writes: &[] },
    Expectation { step: 22, writes: &[(19, 0x04CD0605AA030201)] },
    Expectation { step: 23, writes: &[(20, 0x0000000000000005)] },
    Expectation { step: 24, writes: &[(20, 0x000000000000000A)] },
    Expectation { step: 25, writes: &[(21, 0x0000000000000007)] },
    Expectation { step: 26, writes: &[(21, 0x0000000000000000)] },
    Expectation { step: 27, writes: &[(22, 0x0000000000000001)] },
    Expectation { step: 28, writes: &[(22, 0x0000000000000000)] },
    Expectation { step: 29, writes: &[(23, 0x0000000000000021)] },
    Expectation { step: 30, writes: &[(23, 0x0000004200000000)] },
    Expectation { step: 31, writes: &[(24, 0x0000000080000400)] },
    Expectation { step: 32, writes: &[(24, 0x0000000000000001)] },
    Expectation { step: 33, writes: &[] },
    Expectation { step: 34, writes: &[] },
    Expectation { step: 35, writes: &[] },
    Expectation { step: 36, writes: &[(25, 0x0807060500000000)] },
];

#[rustfmt::skip]
static WORDS_FAULT_JAL_MIS: &[u32] = &[
    0x00100093,
    0x002002EF,
];
#[rustfmt::skip]
static EXPECTED_FAULT_JAL_MIS: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000000000001)] },
    Expectation { step: 1, writes: &[] },
];
#[rustfmt::skip]
static NEVER_WRITTEN_FAULT_JAL_MIS: &[u8] = &[5];

#[rustfmt::skip]
static WORDS_FAULT_JALR_MIS: &[u32] = &[
    0x00300093,
    0x000082E7,
];
#[rustfmt::skip]
static EXPECTED_FAULT_JALR_MIS: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000000000003)] },
    Expectation { step: 1, writes: &[] },
];
#[rustfmt::skip]
static NEVER_WRITTEN_FAULT_JALR_MIS: &[u8] = &[5];

#[rustfmt::skip]
static WORDS_FAULT_BRANCH_NT: &[u32] = &[
    0x00100093,
    0x00100363,
    0x00200113,
    0x00001363,
    0x00300193,
    0x0000C363,
    0x00400213,
    0x00105363,
    0x00500293,
    0x0000E563,
    0x00600313,
    0x00107563,
    0x00700393,
    0x00000463,
    0x00800413,
    0x00900493,
];
#[rustfmt::skip]
static EXPECTED_FAULT_BRANCH_NT: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000000000001)] },
    Expectation { step: 1, writes: &[] },
    Expectation { step: 2, writes: &[(2, 0x0000000000000002)] },
    Expectation { step: 3, writes: &[] },
    Expectation { step: 4, writes: &[(3, 0x0000000000000003)] },
    Expectation { step: 5, writes: &[] },
    Expectation { step: 6, writes: &[(4, 0x0000000000000004)] },
    Expectation { step: 7, writes: &[] },
    Expectation { step: 8, writes: &[(5, 0x0000000000000005)] },
    Expectation { step: 9, writes: &[] },
    Expectation { step: 10, writes: &[(6, 0x0000000000000006)] },
    Expectation { step: 11, writes: &[] },
    Expectation { step: 12, writes: &[(7, 0x0000000000000007)] },
    Expectation { step: 13, writes: &[] },
];
#[rustfmt::skip]
static NEVER_WRITTEN_FAULT_BRANCH_NT: &[u8] = &[8];

#[rustfmt::skip]
static WORDS_FAULT_FETCH: &[u32] = &[
    0x400000B7,
    0x00008067,
];
#[rustfmt::skip]
static EXPECTED_FAULT_FETCH: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000040000000)] },
    Expectation { step: 1, writes: &[] },
    Expectation { step: 2, writes: &[] },
];

#[rustfmt::skip]
static WORDS_FAULT_LD_MIS_H: &[u32] = &[
    0x00100513,
    0x01F51513,
    0x40151083,
];
#[rustfmt::skip]
static EXPECTED_FAULT_LD_MIS_H: &[Expectation] = &[
    Expectation { step: 0, writes: &[(10, 0x0000000000000001)] },
    Expectation { step: 1, writes: &[(10, 0x0000000080000000)] },
    Expectation { step: 2, writes: &[] },
];
#[rustfmt::skip]
static NEVER_WRITTEN_FAULT_LD_MIS_H: &[u8] = &[1];

#[rustfmt::skip]
static WORDS_FAULT_LD_MIS_D: &[u32] = &[
    0x00100513,
    0x01F51513,
    0x40453083,
];
#[rustfmt::skip]
static EXPECTED_FAULT_LD_MIS_D: &[Expectation] = &[
    Expectation { step: 0, writes: &[(10, 0x0000000000000001)] },
    Expectation { step: 1, writes: &[(10, 0x0000000080000000)] },
    Expectation { step: 2, writes: &[] },
];
#[rustfmt::skip]
static NEVER_WRITTEN_FAULT_LD_MIS_D: &[u8] = &[1];

#[rustfmt::skip]
static WORDS_FAULT_ST_MIS_H: &[u32] = &[
    0x00100513,
    0x01F51513,
    0x00700093,
    0x401510A3,
];
#[rustfmt::skip]
static EXPECTED_FAULT_ST_MIS_H: &[Expectation] = &[
    Expectation { step: 0, writes: &[(10, 0x0000000000000001)] },
    Expectation { step: 1, writes: &[(10, 0x0000000080000000)] },
    Expectation { step: 2, writes: &[(1, 0x0000000000000007)] },
    Expectation { step: 3, writes: &[] },
];

#[rustfmt::skip]
static WORDS_FAULT_ST_MIS_W: &[u32] = &[
    0x00100513,
    0x01F51513,
    0x00700093,
    0x40152123,
];
#[rustfmt::skip]
static EXPECTED_FAULT_ST_MIS_W: &[Expectation] = &[
    Expectation { step: 0, writes: &[(10, 0x0000000000000001)] },
    Expectation { step: 1, writes: &[(10, 0x0000000080000000)] },
    Expectation { step: 2, writes: &[(1, 0x0000000000000007)] },
    Expectation { step: 3, writes: &[] },
];

#[rustfmt::skip]
static WORDS_FAULT_ST_MIS_D: &[u32] = &[
    0x00100513,
    0x01F51513,
    0x00700093,
    0x40153223,
];
#[rustfmt::skip]
static EXPECTED_FAULT_ST_MIS_D: &[Expectation] = &[
    Expectation { step: 0, writes: &[(10, 0x0000000000000001)] },
    Expectation { step: 1, writes: &[(10, 0x0000000080000000)] },
    Expectation { step: 2, writes: &[(1, 0x0000000000000007)] },
    Expectation { step: 3, writes: &[] },
];

#[rustfmt::skip]
static WORDS_FAULT_LD_X0_MIS: &[u32] = &[
    0x00100513,
    0x01F51513,
    0x40252003,
];
#[rustfmt::skip]
static EXPECTED_FAULT_LD_X0_MIS: &[Expectation] = &[
    Expectation { step: 0, writes: &[(10, 0x0000000000000001)] },
    Expectation { step: 1, writes: &[(10, 0x0000000080000000)] },
    Expectation { step: 2, writes: &[] },
];

#[rustfmt::skip]
static WORDS_FAULT_LD_X0_FAULT: &[u32] = &[
    0x400005B7,
    0x0005B003,
];
#[rustfmt::skip]
static EXPECTED_FAULT_LD_X0_FAULT: &[Expectation] = &[
    Expectation { step: 0, writes: &[(11, 0x0000000040000000)] },
    Expectation { step: 1, writes: &[] },
];

#[rustfmt::skip]
static WORDS_FAULT_ACCESS_LD: &[u32] = &[
    0x400005B7,
    0x0005B083,
];
#[rustfmt::skip]
static EXPECTED_FAULT_ACCESS_LD: &[Expectation] = &[
    Expectation { step: 0, writes: &[(11, 0x0000000040000000)] },
    Expectation { step: 1, writes: &[] },
];
#[rustfmt::skip]
static NEVER_WRITTEN_FAULT_ACCESS_LD: &[u8] = &[1];

#[rustfmt::skip]
static WORDS_FAULT_ACCESS_SD: &[u32] = &[
    0x400005B7,
    0x00900093,
    0x0015B023,
];
#[rustfmt::skip]
static EXPECTED_FAULT_ACCESS_SD: &[Expectation] = &[
    Expectation { step: 0, writes: &[(11, 0x0000000040000000)] },
    Expectation { step: 1, writes: &[(1, 0x0000000000000009)] },
    Expectation { step: 2, writes: &[] },
];

#[rustfmt::skip]
static WORDS_FAULT_RESERVED: &[u32] = &[
    0x00100093,
    0xFFFFFFFF,
];
#[rustfmt::skip]
static EXPECTED_FAULT_RESERVED: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000000000001)] },
    Expectation { step: 1, writes: &[] },
];

#[rustfmt::skip]
static WORDS_FAULT_SHIFTW_RES: &[u32] = &[
    0x00700093,
    0x0210911B,
];
#[rustfmt::skip]
static EXPECTED_FAULT_SHIFTW_RES: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000000000007)] },
    Expectation { step: 1, writes: &[] },
];
#[rustfmt::skip]
static NEVER_WRITTEN_FAULT_SHIFTW_RES: &[u8] = &[2];

#[rustfmt::skip]
static WORDS_FAULT_FENCE: &[u32] = &[
    0x00100093,
    0x1FF0000F,
    0x8330000F,
    0x0FF0008F,
    0x0FF0800F,
    0x00F0000F,
    0x0F00000F,
    0x00200113,
];
#[rustfmt::skip]
static EXPECTED_FAULT_FENCE: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000000000001)] },
    Expectation { step: 1, writes: &[] },
    Expectation { step: 2, writes: &[] },
    Expectation { step: 3, writes: &[] },
    Expectation { step: 4, writes: &[] },
    Expectation { step: 5, writes: &[] },
    Expectation { step: 6, writes: &[] },
    Expectation { step: 7, writes: &[(2, 0x0000000000000002)] },
];

#[rustfmt::skip]
static WORDS_FAULT_HINTS: &[u32] = &[
    0x00500093,
    0x7FFFF037,
    0x12345017,
    0x00108013,
    0x0020801B,
    0x0010803B,
    0x0010903B,
    0x40108033,
    0x00200033,
    0x00300193,
];
#[rustfmt::skip]
static EXPECTED_FAULT_HINTS: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000000000005)] },
    Expectation { step: 1, writes: &[] },
    Expectation { step: 2, writes: &[] },
    Expectation { step: 3, writes: &[] },
    Expectation { step: 4, writes: &[] },
    Expectation { step: 5, writes: &[] },
    Expectation { step: 6, writes: &[] },
    Expectation { step: 7, writes: &[] },
    Expectation { step: 8, writes: &[] },
    Expectation { step: 9, writes: &[(3, 0x0000000000000003)] },
];

#[rustfmt::skip]
static WORDS_FAULT_SELFMOD: &[u32] = &[
    0x007000B7,
    0x11308093,
    0x00000197,
    0x0011A623,
    0x00400213,
    0x00200113,
    0x00500293,
];
#[rustfmt::skip]
static EXPECTED_FAULT_SELFMOD: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000000700000)] },
    Expectation { step: 1, writes: &[(1, 0x0000000000700113)] },
    Expectation { step: 2, writes: &[(3, 0x0000000080000008)] },
    Expectation { step: 3, writes: &[] },
    Expectation { step: 4, writes: &[(4, 0x0000000000000004)] },
    Expectation { step: 5, writes: &[(2, 0x0000000000000007)] },
    Expectation { step: 6, writes: &[(5, 0x0000000000000005)] },
];

#[rustfmt::skip]
static WORDS_IT_PRIO_JUMP: &[u32] = &[
    0x400000B7,
    0x00308093,
    0x000082E7,
];
#[rustfmt::skip]
static EXPECTED_IT_PRIO_JUMP: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000040000000)] },
    Expectation { step: 1, writes: &[(1, 0x0000000040000003)] },
    Expectation { step: 2, writes: &[] },
];
#[rustfmt::skip]
static NEVER_WRITTEN_IT_PRIO_JUMP: &[u8] = &[5];

#[rustfmt::skip]
static WORDS_IT_PRIO_LOAD: &[u32] = &[
    0x400000B7,
    0x00108093,
    0x0000A103,
];
#[rustfmt::skip]
static EXPECTED_IT_PRIO_LOAD: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000040000000)] },
    Expectation { step: 1, writes: &[(1, 0x0000000040000001)] },
    Expectation { step: 2, writes: &[] },
];
#[rustfmt::skip]
static NEVER_WRITTEN_IT_PRIO_LOAD: &[u8] = &[2];

#[rustfmt::skip]
static WORDS_IT_FAULT_ALIAS: &[u32] = &[
    0x800002B7,
    0x0012A283,
];
#[rustfmt::skip]
static EXPECTED_IT_FAULT_ALIAS: &[Expectation] = &[
    Expectation { step: 0, writes: &[(5, 0xFFFFFFFF80000000)] },
    Expectation { step: 1, writes: &[] },
];

#[rustfmt::skip]
static WORDS_IT_FAULT_WRAP_LD: &[u32] = &[
    0xFFC00093,
    0x0040B103,
];
#[rustfmt::skip]
static EXPECTED_IT_FAULT_WRAP_LD: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0xFFFFFFFFFFFFFFFC)] },
    Expectation { step: 1, writes: &[] },
];
#[rustfmt::skip]
static NEVER_WRITTEN_IT_FAULT_WRAP_LD: &[u8] = &[2];

#[rustfmt::skip]
static WORDS_IT_FAULT_WRAP_SD: &[u32] = &[
    0xFF800093,
    0x00700113,
    0x0020B423,
];
#[rustfmt::skip]
static EXPECTED_IT_FAULT_WRAP_SD: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0xFFFFFFFFFFFFFFF8)] },
    Expectation { step: 1, writes: &[(2, 0x0000000000000007)] },
    Expectation { step: 2, writes: &[] },
];

#[rustfmt::skip]
static WORDS_IT_ALIAS_BOUND: &[u32] = &[
    0xFFF00293,
    0x005282BB,
    0x04100313,
    0x00635333,
    0x03F00393,
    0x007393B3,
    0xFFF00413,
    0x00100493,
    0x008424B3,
    0x40840433,
];
#[rustfmt::skip]
static EXPECTED_IT_ALIAS_BOUND: &[Expectation] = &[
    Expectation { step: 0, writes: &[(5, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 1, writes: &[(5, 0xFFFFFFFFFFFFFFFE)] },
    Expectation { step: 2, writes: &[(6, 0x0000000000000041)] },
    Expectation { step: 3, writes: &[(6, 0x0000000000000020)] },
    Expectation { step: 4, writes: &[(7, 0x000000000000003F)] },
    Expectation { step: 5, writes: &[(7, 0x8000000000000000)] },
    Expectation { step: 6, writes: &[(8, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 7, writes: &[(9, 0x0000000000000001)] },
    Expectation { step: 8, writes: &[(9, 0x0000000000000000)] },
    Expectation { step: 9, writes: &[(8, 0x0000000000000000)] },
];

#[rustfmt::skip]
static WORDS_IT_PROGRESS_LOOP: &[u32] = &[
    0x00100093,
    0x00108093,
    0xFFDFF06F,
];
#[rustfmt::skip]
static EXPECTED_IT_PROGRESS_LOOP: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000000000001)] },
    Expectation { step: 1, writes: &[(1, 0x0000000000000002)] },
    Expectation { step: 2, writes: &[] },
    Expectation { step: 3, writes: &[(1, 0x0000000000000003)] },
    Expectation { step: 4, writes: &[] },
    Expectation { step: 5, writes: &[(1, 0x0000000000000004)] },
    Expectation { step: 6, writes: &[] },
    Expectation { step: 7, writes: &[(1, 0x0000000000000005)] },
    Expectation { step: 8, writes: &[] },
    Expectation { step: 9, writes: &[(1, 0x0000000000000006)] },
    Expectation { step: 10, writes: &[] },
    Expectation { step: 11, writes: &[(1, 0x0000000000000007)] },
    Expectation { step: 12, writes: &[] },
];

#[rustfmt::skip]
static WORDS_IT_FENCEI: &[u32] = &[
    0x00100093,
    0x0000100F,
    0x00700113,
];
#[rustfmt::skip]
static EXPECTED_IT_FENCEI: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000000000001)] },
    Expectation { step: 1, writes: &[] },
];
#[rustfmt::skip]
static NEVER_WRITTEN_IT_FENCEI: &[u8] = &[2];

#[rustfmt::skip]
static WORDS_DIR_RUNOFF: &[u32] = &[
    0x00100093,
    0x00200113,
];
#[rustfmt::skip]
static EXPECTED_DIR_RUNOFF: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000000000001)] },
    Expectation { step: 1, writes: &[(2, 0x0000000000000002)] },
    Expectation { step: 2, writes: &[] },
];

#[rustfmt::skip]
static WORDS_DIR_CHASE: &[u32] = &[
    0x00000097,
    0x06008093,
    0x02A00393,
    0x0070B823,
    0x00000117,
    0x06010113,
    0x0020B023,
    0x00000197,
    0x01C18193,
    0x0030B423,
    0x0000B203,
    0x00023283,
    0x0080B303,
    0x00030067,
    0x00700413,
    0x00900493,
    0x00100073,
];
#[rustfmt::skip]
static EXPECTED_DIR_CHASE: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000080000000)] },
    Expectation { step: 1, writes: &[(1, 0x0000000080000060)] },
    Expectation { step: 2, writes: &[(7, 0x000000000000002A)] },
    Expectation { step: 3, writes: &[] },
    Expectation { step: 4, writes: &[(2, 0x0000000080000010)] },
    Expectation { step: 5, writes: &[(2, 0x0000000080000070)] },
    Expectation { step: 6, writes: &[] },
    Expectation { step: 7, writes: &[(3, 0x000000008000001C)] },
    Expectation { step: 8, writes: &[(3, 0x0000000080000038)] },
    Expectation { step: 9, writes: &[] },
    Expectation { step: 10, writes: &[(4, 0x0000000080000070)] },
    Expectation { step: 11, writes: &[(5, 0x000000000000002A)] },
    Expectation { step: 12, writes: &[(6, 0x0000000080000038)] },
    Expectation { step: 13, writes: &[] },
    Expectation { step: 14, writes: &[(8, 0x0000000000000007)] },
    Expectation { step: 15, writes: &[(9, 0x0000000000000009)] },
    Expectation { step: 16, writes: &[] },
];

#[rustfmt::skip]
static WORDS_DIR_EXT_MATRIX: &[u32] = &[
    0x00000097,
    0x0A008093,
    0x0000B023,
    0x08000113,
    0x00208023,
    0x00008283,
    0x0000C303,
    0x00009383,
    0x0000A403,
    0x0000B483,
    0x0000B023,
    0x00008137,
    0x00209023,
    0x00008283,
    0x00108303,
    0x0000D383,
    0x00009403,
    0x0000A483,
    0x0000B503,
    0x0000B023,
    0x80000137,
    0x0020A023,
    0x00308283,
    0x00209303,
    0x0000E383,
    0x0000A403,
    0x0000B483,
    0x80000137,
    0x02011113,
    0x0020B023,
    0x00708283,
    0x00609303,
    0x0040A383,
    0x0000B403,
    0x00100593,
];
#[rustfmt::skip]
static EXPECTED_DIR_EXT_MATRIX: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000080000000)] },
    Expectation { step: 1, writes: &[(1, 0x00000000800000A0)] },
    Expectation { step: 2, writes: &[] },
    Expectation { step: 3, writes: &[(2, 0x0000000000000080)] },
    Expectation { step: 4, writes: &[] },
    Expectation { step: 5, writes: &[(5, 0xFFFFFFFFFFFFFF80)] },
    Expectation { step: 6, writes: &[(6, 0x0000000000000080)] },
    Expectation { step: 7, writes: &[(7, 0x0000000000000080)] },
    Expectation { step: 8, writes: &[(8, 0x0000000000000080)] },
    Expectation { step: 9, writes: &[(9, 0x0000000000000080)] },
    Expectation { step: 10, writes: &[] },
    Expectation { step: 11, writes: &[(2, 0x0000000000008000)] },
    Expectation { step: 12, writes: &[] },
    Expectation { step: 13, writes: &[(5, 0x0000000000000000)] },
    Expectation { step: 14, writes: &[(6, 0xFFFFFFFFFFFFFF80)] },
    Expectation { step: 15, writes: &[(7, 0x0000000000008000)] },
    Expectation { step: 16, writes: &[(8, 0xFFFFFFFFFFFF8000)] },
    Expectation { step: 17, writes: &[(9, 0x0000000000008000)] },
    Expectation { step: 18, writes: &[(10, 0x0000000000008000)] },
    Expectation { step: 19, writes: &[] },
    Expectation { step: 20, writes: &[(2, 0xFFFFFFFF80000000)] },
    Expectation { step: 21, writes: &[] },
    Expectation { step: 22, writes: &[(5, 0xFFFFFFFFFFFFFF80)] },
    Expectation { step: 23, writes: &[(6, 0xFFFFFFFFFFFF8000)] },
    Expectation { step: 24, writes: &[(7, 0x0000000080000000)] },
    Expectation { step: 25, writes: &[(8, 0xFFFFFFFF80000000)] },
    Expectation { step: 26, writes: &[(9, 0x0000000080000000)] },
    Expectation { step: 27, writes: &[] },
    Expectation { step: 28, writes: &[(2, 0x8000000000000000)] },
    Expectation { step: 29, writes: &[] },
    Expectation { step: 30, writes: &[] },
    Expectation { step: 31, writes: &[] },
    Expectation { step: 32, writes: &[(7, 0xFFFFFFFF80000000)] },
    Expectation { step: 33, writes: &[(8, 0x8000000000000000)] },
    Expectation { step: 34, writes: &[(11, 0x0000000000000001)] },
];

#[rustfmt::skip]
static WORDS_DIR_SELFMOD_FENCE: &[u32] = &[
    0x007000B7,
    0x11308093,
    0x00000197,
    0x0011A823,
    0x0330000F,
    0x00400213,
    0x00200113,
    0x00500293,
];
#[rustfmt::skip]
static EXPECTED_DIR_SELFMOD_FENCE: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000000700000)] },
    Expectation { step: 1, writes: &[(1, 0x0000000000700113)] },
    Expectation { step: 2, writes: &[(3, 0x0000000080000008)] },
    Expectation { step: 3, writes: &[] },
    Expectation { step: 4, writes: &[] },
    Expectation { step: 5, writes: &[(4, 0x0000000000000004)] },
    Expectation { step: 6, writes: &[(2, 0x0000000000000007)] },
    Expectation { step: 7, writes: &[(5, 0x0000000000000005)] },
];

#[rustfmt::skip]
static WORDS_DIR_CMP_BRANCH: &[u32] = &[
    0x00500293,
    0x00700313,
    0x0062A3B3,
    0x00039463,
    0x01100413,
    0x00032393,
    0x00038463,
    0x02200413,
    0x406303B3,
    0x00039463,
    0x00300493,
    0x0062A3B3,
    0x00038463,
    0x00400513,
    0x00B00593,
];
#[rustfmt::skip]
static EXPECTED_DIR_CMP_BRANCH: &[Expectation] = &[
    Expectation { step: 0, writes: &[(5, 0x0000000000000005)] },
    Expectation { step: 1, writes: &[(6, 0x0000000000000007)] },
    Expectation { step: 2, writes: &[(7, 0x0000000000000001)] },
    Expectation { step: 3, writes: &[] },
    Expectation { step: 4, writes: &[(7, 0x0000000000000000)] },
    Expectation { step: 5, writes: &[] },
    Expectation { step: 6, writes: &[] },
    Expectation { step: 7, writes: &[] },
    Expectation { step: 8, writes: &[(9, 0x0000000000000003)] },
    Expectation { step: 9, writes: &[(7, 0x0000000000000001)] },
    Expectation { step: 10, writes: &[] },
    Expectation { step: 11, writes: &[(10, 0x0000000000000004)] },
    Expectation { step: 12, writes: &[(11, 0x000000000000000B)] },
];
#[rustfmt::skip]
static NEVER_WRITTEN_DIR_CMP_BRANCH: &[u8] = &[8];

#[rustfmt::skip]
static WORDS_DIR_MEMWALK: &[u32] = &[
    0x00000097,
    0x06008093,
    0x00A00113,
    0x0020B023,
    0x01400113,
    0x0020B423,
    0x01E00113,
    0x0020B823,
    0x02800113,
    0x0020BC23,
    0x00400193,
    0x04008213,
    0x0000B283,
    0x00523023,
    0x00808093,
    0x00820213,
    0xFFF18193,
    0xFE0196E3,
    0x00100073,
];
#[rustfmt::skip]
static EXPECTED_DIR_MEMWALK: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000080000000)] },
    Expectation { step: 1, writes: &[(1, 0x0000000080000060)] },
    Expectation { step: 2, writes: &[(2, 0x000000000000000A)] },
    Expectation { step: 3, writes: &[] },
    Expectation { step: 4, writes: &[(2, 0x0000000000000014)] },
    Expectation { step: 5, writes: &[] },
    Expectation { step: 6, writes: &[(2, 0x000000000000001E)] },
    Expectation { step: 7, writes: &[] },
    Expectation { step: 8, writes: &[(2, 0x0000000000000028)] },
    Expectation { step: 9, writes: &[] },
    Expectation { step: 10, writes: &[(3, 0x0000000000000004)] },
    Expectation { step: 11, writes: &[(4, 0x00000000800000A0)] },
    Expectation { step: 12, writes: &[(5, 0x000000000000000A)] },
    Expectation { step: 13, writes: &[] },
    Expectation { step: 14, writes: &[(1, 0x0000000080000068)] },
    Expectation { step: 15, writes: &[(4, 0x00000000800000A8)] },
    Expectation { step: 16, writes: &[(3, 0x0000000000000003)] },
    Expectation { step: 17, writes: &[] },
    Expectation { step: 18, writes: &[(5, 0x0000000000000014)] },
    Expectation { step: 19, writes: &[] },
    Expectation { step: 20, writes: &[(1, 0x0000000080000070)] },
    Expectation { step: 21, writes: &[(4, 0x00000000800000B0)] },
    Expectation { step: 22, writes: &[(3, 0x0000000000000002)] },
    Expectation { step: 23, writes: &[] },
    Expectation { step: 24, writes: &[(5, 0x000000000000001E)] },
    Expectation { step: 25, writes: &[] },
    Expectation { step: 26, writes: &[(1, 0x0000000080000078)] },
    Expectation { step: 27, writes: &[(4, 0x00000000800000B8)] },
    Expectation { step: 28, writes: &[(3, 0x0000000000000001)] },
    Expectation { step: 29, writes: &[] },
    Expectation { step: 30, writes: &[(5, 0x0000000000000028)] },
    Expectation { step: 31, writes: &[] },
    Expectation { step: 32, writes: &[(1, 0x0000000080000080)] },
    Expectation { step: 33, writes: &[(4, 0x00000000800000C0)] },
    Expectation { step: 34, writes: &[(3, 0x0000000000000000)] },
    Expectation { step: 35, writes: &[] },
    Expectation { step: 36, writes: &[] },
];

#[rustfmt::skip]
static WORDS_DIR_CHAIN: &[u32] = &[
    0x00000097,
    0x06008093,
    0x00200313,
    0x06400393,
    0x00100293,
    0x00429293,
    0x00328293,
    0x006292B3,
    0x0050B023,
    0x0000B283,
    0x4012D293,
    0x006282BB,
    0x0FF2C293,
    0x0022D293,
    0x0072829B,
    0x03E2F293,
    0x406282BB,
    0x0072B2B3,
    0x00800413,
];
#[rustfmt::skip]
static EXPECTED_DIR_CHAIN: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000080000000)] },
    Expectation { step: 1, writes: &[(1, 0x0000000080000060)] },
    Expectation { step: 2, writes: &[(6, 0x0000000000000002)] },
    Expectation { step: 3, writes: &[(7, 0x0000000000000064)] },
    Expectation { step: 4, writes: &[(5, 0x0000000000000001)] },
    Expectation { step: 5, writes: &[(5, 0x0000000000000010)] },
    Expectation { step: 6, writes: &[(5, 0x0000000000000013)] },
    Expectation { step: 7, writes: &[(5, 0x000000000000004C)] },
    Expectation { step: 8, writes: &[] },
    Expectation { step: 9, writes: &[] },
    Expectation { step: 10, writes: &[(5, 0x0000000000000026)] },
    Expectation { step: 11, writes: &[(5, 0x0000000000000028)] },
    Expectation { step: 12, writes: &[(5, 0x00000000000000D7)] },
    Expectation { step: 13, writes: &[(5, 0x0000000000000035)] },
    Expectation { step: 14, writes: &[(5, 0x000000000000003C)] },
    Expectation { step: 15, writes: &[] },
    Expectation { step: 16, writes: &[(5, 0x000000000000003A)] },
    Expectation { step: 17, writes: &[(5, 0x0000000000000001)] },
    Expectation { step: 18, writes: &[(8, 0x0000000000000008)] },
];

#[rustfmt::skip]
static WORDS_DIR_X0_WRITES: &[u32] = &[
    0x00000097,
    0x06008093,
    0xFFF00113,
    0x0020B023,
    0x00008003,
    0x0000C003,
    0x00009003,
    0x0000D003,
    0x0000E003,
    0x0000B003,
    0x00500193,
    0x4031803B,
    0x0031D03B,
    0x4031D03B,
    0x0011901B,
    0x0011D01B,
    0x4011D01B,
    0x00400213,
];
#[rustfmt::skip]
static EXPECTED_DIR_X0_WRITES: &[Expectation] = &[
    Expectation { step: 0, writes: &[(1, 0x0000000080000000)] },
    Expectation { step: 1, writes: &[(1, 0x0000000080000060)] },
    Expectation { step: 2, writes: &[(2, 0xFFFFFFFFFFFFFFFF)] },
    Expectation { step: 3, writes: &[] },
    Expectation { step: 4, writes: &[] },
    Expectation { step: 5, writes: &[] },
    Expectation { step: 6, writes: &[] },
    Expectation { step: 7, writes: &[] },
    Expectation { step: 8, writes: &[] },
    Expectation { step: 9, writes: &[] },
    Expectation { step: 10, writes: &[(3, 0x0000000000000005)] },
    Expectation { step: 11, writes: &[] },
    Expectation { step: 12, writes: &[] },
    Expectation { step: 13, writes: &[] },
    Expectation { step: 14, writes: &[] },
    Expectation { step: 15, writes: &[] },
    Expectation { step: 16, writes: &[] },
    Expectation { step: 17, writes: &[(4, 0x0000000000000004)] },
];
#[rustfmt::skip]
static NEVER_WRITTEN_DIR_X0_WRITES: &[u8] = &[0];

/// A tracked guest program (assembled bytes) and the specification-derived
/// observations it must produce under the definitional interpreter.
pub struct Guest {
    /// The guest's name — the basename of its tracked sources.
    pub name: &'static str,
    /// The declared entry address (the reset vector of the laboratory).
    pub entry: u64,
    /// The guest's instruction words, little-endian sequence.
    pub words: &'static [u32],
    /// How many steps the program executes (the expectations declare it).
    pub executed_steps: usize,
    /// The expected register writes, one entry per executed step.
    pub expected: &'static [Expectation],
    /// Registers a correct execution must never write (the negative
    /// observations; a control transfer that failed to skip is invisible to
    /// positive checks alone).
    pub never_written: &'static [u8],
    /// Whether the cross-model comparison is enabled for this guest (a
    /// recorded platform difference may disable it; the skip is printed,
    /// never silent).
    pub cross_model: bool,
}

/// The tracked guests, in the experiment's run order.
pub static GUESTS: &[Guest] = &[
    Guest {
        name: "smoke-arith",
        entry: 0x0000000080000000,
        words: WORDS_SMOKE_ARITH,
        executed_steps: 12,
        expected: EXPECTED_SMOKE_ARITH,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "guest-control",
        entry: 0x0000000080000000,
        words: WORDS_GUEST_CONTROL,
        executed_steps: 13,
        expected: EXPECTED_GUEST_CONTROL,
        never_written: NEVER_WRITTEN_GUEST_CONTROL,
        cross_model: true,
    },
    Guest {
        name: "smoke-trap",
        entry: 0x0000000080000000,
        words: WORDS_SMOKE_TRAP,
        executed_steps: 3,
        expected: EXPECTED_SMOKE_TRAP,
        never_written: NEVER_WRITTEN_SMOKE_TRAP,
        cross_model: true,
    },
    Guest {
        name: "guest-no-device",
        entry: 0x0000000080000000,
        words: WORDS_GUEST_NO_DEVICE,
        executed_steps: 6,
        expected: EXPECTED_GUEST_NO_DEVICE,
        never_written: NEVER_WRITTEN_GUEST_NO_DEVICE,
        cross_model: false,
    },
    Guest {
        name: "scope-alu",
        entry: 0x0000000080000000,
        words: WORDS_SCOPE_ALU,
        executed_steps: 31,
        expected: EXPECTED_SCOPE_ALU,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "scope-mem",
        entry: 0x0000000080000000,
        words: WORDS_SCOPE_MEM,
        executed_steps: 29,
        expected: EXPECTED_SCOPE_MEM,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "scope-branch",
        entry: 0x0000000080000000,
        words: WORDS_SCOPE_BRANCH,
        executed_steps: 19,
        expected: EXPECTED_SCOPE_BRANCH,
        never_written: NEVER_WRITTEN_SCOPE_BRANCH,
        cross_model: true,
    },
    Guest {
        name: "scope-ecall",
        entry: 0x0000000080000000,
        words: WORDS_SCOPE_ECALL,
        executed_steps: 2,
        expected: EXPECTED_SCOPE_ECALL,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "scope-ebreak",
        entry: 0x0000000080000000,
        words: WORDS_SCOPE_EBREAK,
        executed_steps: 2,
        expected: EXPECTED_SCOPE_EBREAK,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "bound-shift",
        entry: 0x0000000080000000,
        words: WORDS_BOUND_SHIFT,
        executed_steps: 89,
        expected: EXPECTED_BOUND_SHIFT,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "bound-shiftw",
        entry: 0x0000000080000000,
        words: WORDS_BOUND_SHIFTW,
        executed_steps: 55,
        expected: EXPECTED_BOUND_SHIFTW,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "bound-arith",
        entry: 0x0000000080000000,
        words: WORDS_BOUND_ARITH,
        executed_steps: 31,
        expected: EXPECTED_BOUND_ARITH,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "bound-ext",
        entry: 0x0000000080000000,
        words: WORDS_BOUND_EXT,
        executed_steps: 47,
        expected: EXPECTED_BOUND_EXT,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "bound-alias",
        entry: 0x0000000080000000,
        words: WORDS_BOUND_ALIAS,
        executed_steps: 37,
        expected: EXPECTED_BOUND_ALIAS,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "fault-jal-mis",
        entry: 0x0000000080000000,
        words: WORDS_FAULT_JAL_MIS,
        executed_steps: 2,
        expected: EXPECTED_FAULT_JAL_MIS,
        never_written: NEVER_WRITTEN_FAULT_JAL_MIS,
        cross_model: true,
    },
    Guest {
        name: "fault-jalr-mis",
        entry: 0x0000000080000000,
        words: WORDS_FAULT_JALR_MIS,
        executed_steps: 2,
        expected: EXPECTED_FAULT_JALR_MIS,
        never_written: NEVER_WRITTEN_FAULT_JALR_MIS,
        cross_model: true,
    },
    Guest {
        name: "fault-branch-nt",
        entry: 0x0000000080000000,
        words: WORDS_FAULT_BRANCH_NT,
        executed_steps: 14,
        expected: EXPECTED_FAULT_BRANCH_NT,
        never_written: NEVER_WRITTEN_FAULT_BRANCH_NT,
        cross_model: true,
    },
    Guest {
        name: "fault-fetch",
        entry: 0x0000000080000000,
        words: WORDS_FAULT_FETCH,
        executed_steps: 3,
        expected: EXPECTED_FAULT_FETCH,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "fault-ld-mis-h",
        entry: 0x0000000080000000,
        words: WORDS_FAULT_LD_MIS_H,
        executed_steps: 3,
        expected: EXPECTED_FAULT_LD_MIS_H,
        never_written: NEVER_WRITTEN_FAULT_LD_MIS_H,
        cross_model: true,
    },
    Guest {
        name: "fault-ld-mis-d",
        entry: 0x0000000080000000,
        words: WORDS_FAULT_LD_MIS_D,
        executed_steps: 3,
        expected: EXPECTED_FAULT_LD_MIS_D,
        never_written: NEVER_WRITTEN_FAULT_LD_MIS_D,
        cross_model: true,
    },
    Guest {
        name: "fault-st-mis-h",
        entry: 0x0000000080000000,
        words: WORDS_FAULT_ST_MIS_H,
        executed_steps: 4,
        expected: EXPECTED_FAULT_ST_MIS_H,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "fault-st-mis-w",
        entry: 0x0000000080000000,
        words: WORDS_FAULT_ST_MIS_W,
        executed_steps: 4,
        expected: EXPECTED_FAULT_ST_MIS_W,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "fault-st-mis-d",
        entry: 0x0000000080000000,
        words: WORDS_FAULT_ST_MIS_D,
        executed_steps: 4,
        expected: EXPECTED_FAULT_ST_MIS_D,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "fault-ld-x0-mis",
        entry: 0x0000000080000000,
        words: WORDS_FAULT_LD_X0_MIS,
        executed_steps: 3,
        expected: EXPECTED_FAULT_LD_X0_MIS,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "fault-ld-x0-fault",
        entry: 0x0000000080000000,
        words: WORDS_FAULT_LD_X0_FAULT,
        executed_steps: 2,
        expected: EXPECTED_FAULT_LD_X0_FAULT,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "fault-access-ld",
        entry: 0x0000000080000000,
        words: WORDS_FAULT_ACCESS_LD,
        executed_steps: 2,
        expected: EXPECTED_FAULT_ACCESS_LD,
        never_written: NEVER_WRITTEN_FAULT_ACCESS_LD,
        cross_model: true,
    },
    Guest {
        name: "fault-access-sd",
        entry: 0x0000000080000000,
        words: WORDS_FAULT_ACCESS_SD,
        executed_steps: 3,
        expected: EXPECTED_FAULT_ACCESS_SD,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "fault-reserved",
        entry: 0x0000000080000000,
        words: WORDS_FAULT_RESERVED,
        executed_steps: 2,
        expected: EXPECTED_FAULT_RESERVED,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "fault-shiftw-res",
        entry: 0x0000000080000000,
        words: WORDS_FAULT_SHIFTW_RES,
        executed_steps: 2,
        expected: EXPECTED_FAULT_SHIFTW_RES,
        never_written: NEVER_WRITTEN_FAULT_SHIFTW_RES,
        cross_model: true,
    },
    Guest {
        name: "fault-fence",
        entry: 0x0000000080000000,
        words: WORDS_FAULT_FENCE,
        executed_steps: 8,
        expected: EXPECTED_FAULT_FENCE,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "fault-hints",
        entry: 0x0000000080000000,
        words: WORDS_FAULT_HINTS,
        executed_steps: 10,
        expected: EXPECTED_FAULT_HINTS,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "fault-selfmod",
        entry: 0x0000000080000000,
        words: WORDS_FAULT_SELFMOD,
        executed_steps: 7,
        expected: EXPECTED_FAULT_SELFMOD,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "it-prio-jump",
        entry: 0x0000000080000000,
        words: WORDS_IT_PRIO_JUMP,
        executed_steps: 3,
        expected: EXPECTED_IT_PRIO_JUMP,
        never_written: NEVER_WRITTEN_IT_PRIO_JUMP,
        cross_model: true,
    },
    Guest {
        name: "it-prio-load",
        entry: 0x0000000080000000,
        words: WORDS_IT_PRIO_LOAD,
        executed_steps: 3,
        expected: EXPECTED_IT_PRIO_LOAD,
        never_written: NEVER_WRITTEN_IT_PRIO_LOAD,
        cross_model: true,
    },
    Guest {
        name: "it-fault-alias",
        entry: 0x0000000080000000,
        words: WORDS_IT_FAULT_ALIAS,
        executed_steps: 2,
        expected: EXPECTED_IT_FAULT_ALIAS,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "it-fault-wrap-ld",
        entry: 0x0000000080000000,
        words: WORDS_IT_FAULT_WRAP_LD,
        executed_steps: 2,
        expected: EXPECTED_IT_FAULT_WRAP_LD,
        never_written: NEVER_WRITTEN_IT_FAULT_WRAP_LD,
        cross_model: true,
    },
    Guest {
        name: "it-fault-wrap-sd",
        entry: 0x0000000080000000,
        words: WORDS_IT_FAULT_WRAP_SD,
        executed_steps: 3,
        expected: EXPECTED_IT_FAULT_WRAP_SD,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "it-alias-bound",
        entry: 0x0000000080000000,
        words: WORDS_IT_ALIAS_BOUND,
        executed_steps: 10,
        expected: EXPECTED_IT_ALIAS_BOUND,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "it-progress-loop",
        entry: 0x0000000080000000,
        words: WORDS_IT_PROGRESS_LOOP,
        executed_steps: 13,
        expected: EXPECTED_IT_PROGRESS_LOOP,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "it-fencei",
        entry: 0x0000000080000000,
        words: WORDS_IT_FENCEI,
        executed_steps: 2,
        expected: EXPECTED_IT_FENCEI,
        never_written: NEVER_WRITTEN_IT_FENCEI,
        cross_model: true,
    },
    Guest {
        name: "dir-runoff",
        entry: 0x0000000080000000,
        words: WORDS_DIR_RUNOFF,
        executed_steps: 3,
        expected: EXPECTED_DIR_RUNOFF,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "dir-chase",
        entry: 0x0000000080000000,
        words: WORDS_DIR_CHASE,
        executed_steps: 17,
        expected: EXPECTED_DIR_CHASE,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "dir-ext-matrix",
        entry: 0x0000000080000000,
        words: WORDS_DIR_EXT_MATRIX,
        executed_steps: 35,
        expected: EXPECTED_DIR_EXT_MATRIX,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "dir-selfmod-fence",
        entry: 0x0000000080000000,
        words: WORDS_DIR_SELFMOD_FENCE,
        executed_steps: 8,
        expected: EXPECTED_DIR_SELFMOD_FENCE,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "dir-cmp-branch",
        entry: 0x0000000080000000,
        words: WORDS_DIR_CMP_BRANCH,
        executed_steps: 13,
        expected: EXPECTED_DIR_CMP_BRANCH,
        never_written: NEVER_WRITTEN_DIR_CMP_BRANCH,
        cross_model: true,
    },
    Guest {
        name: "dir-memwalk",
        entry: 0x0000000080000000,
        words: WORDS_DIR_MEMWALK,
        executed_steps: 37,
        expected: EXPECTED_DIR_MEMWALK,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "dir-chain",
        entry: 0x0000000080000000,
        words: WORDS_DIR_CHAIN,
        executed_steps: 19,
        expected: EXPECTED_DIR_CHAIN,
        never_written: &[],
        cross_model: true,
    },
    Guest {
        name: "dir-x0-writes",
        entry: 0x0000000080000000,
        words: WORDS_DIR_X0_WRITES,
        executed_steps: 18,
        expected: EXPECTED_DIR_X0_WRITES,
        never_written: NEVER_WRITTEN_DIR_X0_WRITES,
        cross_model: true,
    },
];

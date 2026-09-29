//! The recorded input bundle and its replay — `P1-LAB.10`, task card T008 (G-REPLAY:
//! "reports and relevant successes/failures reproduce from recorded definitions, tools,
//! inputs, and event choices"). `docs/ARCHITECTURE.md` §7: identity includes code and
//! generator versions, initial state, guest image, environment policy, and the relevant
//! event choices — *a seed without the generator version and event stream is insufficient*.
//!
//! A [`Bundle`] is everything one run consumed, plus the result it produced:
//!
//! - [`Algorithm`] — the tool: the harness version and the model under test
//!   (`"production"` or `"mutant:<name>"`, the `.9` suite's published vocabulary), and the
//!   definition identity flattened from `semulith-core::definition::MANIFEST` (profile,
//!   ilen, generator name+sha256, every input pin). At replay every pin is re-compared
//!   against the live manifest and a mismatch is **refused by name** — replaying against a
//!   different definition is a different experiment, not a replay.
//! - [`Platform`] — the environment policy: the FlatMemory region declaration. Together
//!   with [`Bundle::entry`] it is the laboratory reset (the profile declares x1..x31 = 0,
//!   REQ-D-ENTRY-STATE, so the zero registers ride as documentation rather than data).
//! - [`Image`] — the guest words plus the sha256 of the little-endian image bytes; the
//!   digest is recomputed at replay, so an image tampered after recording is refused by
//!   name.
//! - [`Events`] — the actual relevant event choices, recorded as data. This platform's
//!   choice is `DeclaredNone`: OB-ENV-EVENT-DELIVERY declares no asynchronous event, and
//!   the bundle says so explicitly rather than leaving the choice unrecorded. Any other
//!   claim is refused by name as not-this-platform (scripted-environment replay joins
//!   when a tracked consumer needs it — the tree's Open Questions).
//! - `budget` — the step bound, and [`Recorded`] — the result: the observation steps in
//!   the normalized vocabulary plus the stop's canonical render. Rendering is
//!   deterministic, and a `Failed`/`Undefined` stop carries data no JSON round-trip could
//!   rebuild typed, so the stop is compared rendered — nothing is lost by not re-typing.
//!
//! Serialization is JSON, both directions — the crate carries no dependencies, the writer
//! is hand-rolled like [`crate::report`]'s, and the parser is the crate's own [`json`]
//! reader. A document missing any accompaniment fails parse **naming the field**: the
//! bare-seed refusal is structural, not a policy a reader could waive. The library stays
//! `std::fs`-free (bytes in, verdict out) so the workspace keeps building for
//! `wasm32-unknown-unknown`; file IO lives in the CLI command.

use semulith_core::definition::{InsnDef, MANIFEST};

use crate::fixtures::FlatMemory;
use crate::json::{self, Json};
use crate::mutate;
use crate::report::push_escaped;
use crate::run::{self, Divergence, Step};
use crate::sha256::sha256_hex;

/// The platform's declared event-delivery policy this bundle records (OB-ENV-EVENT-DELIVERY).
pub const EVENT_OBLIGATION: &str = "OB-ENV-EVENT-DELIVERY";

/// Everything one run consumed and the result it produced — see the module documentation.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Bundle {
    pub algorithm: Algorithm,
    pub platform: Platform,
    pub entry: u64,
    pub image: Image,
    pub events: Events,
    pub budget: usize,
    pub recorded: Recorded,
}

/// The tool that produced the result: harness version, model under test, and the
/// definition identity (OWN-03's manifest, flattened — the algorithm/version accompaniment
/// a seed must carry).
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Algorithm {
    /// The recording harness, `"semulith-verify <version>"`.
    pub harness: String,
    /// `"production"` or `"mutant:<name>"` — resolved through [`table_for_model`].
    pub model: String,
    /// The unit definition the run executed against (from `definition::MANIFEST`).
    pub profile: String,
    /// The instruction length in bits (ILEN = 32 for this profile).
    pub ilen: u32,
    /// The generator that produced the definition, `(name, sha256)`.
    pub generator: (String, String),
    /// Every canonical input pin the definition carries, `(path, sha256)`.
    pub inputs: Vec<(String, String)>,
}

/// The environment policy: one little-endian main-memory region `[base, base + size)`.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Platform {
    pub base: u64,
    pub size: u64,
}

/// The guest image and the digest that guards it.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Image {
    pub words: Vec<u32>,
    pub sha256: String,
}

/// The actual relevant event choices. This platform declares no asynchronous event; the
/// choice itself is recorded, not left implicit.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Events {
    /// OB-ENV-EVENT-DELIVERY: the platform declares no asynchronous event — the recorded
    /// event stream is empty, as a fact, not an omission.
    DeclaredNone,
}

/// The recorded result: the observation steps plus the stop's canonical render.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Recorded {
    pub steps: Vec<Step>,
    /// `format!("{:?}", stop)` — deterministic, and comparable without re-typing data a
    /// round-trip cannot rebuild.
    pub stop: String,
}

/// The inputs to record over: the model name (the bundle vocabulary), the platform facts,
/// and the step bound.
pub struct CaseSpec {
    /// `"production"` or `"mutant:<name>"`.
    pub model: String,
    pub entry: u64,
    pub base: u64,
    pub size: u64,
    pub budget: usize,
}

impl Bundle {
    /// Run the named model over the given words under the platform and capture the result.
    /// `Err` names an unknown model or an image that does not fit the declared region.
    pub fn record(spec: &CaseSpec, words: &[u32]) -> Result<Self, String> {
        let table = table_for_model(&spec.model)?;
        let bytes = image_bytes(words);
        check_layout(spec.base, spec.size, spec.entry, bytes.len())?;
        let image = Image {
            words: words.to_vec(),
            sha256: sha256_hex(&bytes),
        };
        let mut env = FlatMemory::new(spec.base, spec.size as usize);
        env.load_image((spec.entry - spec.base) as usize, &bytes);
        let (trace, _crossings) = run::run_over(&mut env, spec.entry, spec.budget, &table);
        Ok(Self {
            algorithm: algorithm_for(&spec.model),
            platform: Platform {
                base: spec.base,
                size: spec.size,
            },
            entry: spec.entry,
            image,
            events: Events::DeclaredNone,
            budget: spec.budget,
            recorded: Recorded {
                steps: trace.steps,
                stop: format!("{:?}", trace.stop),
            },
        })
    }

    /// Re-derive the recorded result from the recorded inputs. Identity is checked first
    /// (definition pins, then the image digest); a mismatch refuses by name. The recorded
    /// and re-derived streams are then walked by the first-divergence comparator, so a
    /// drifted result is reported at its first differing observation, never as a summary.
    pub fn replay(&self) -> Result<Replay, String> {
        self.check_identity()?;
        let table = table_for_model(&self.algorithm.model)?;
        let mut env = FlatMemory::new(self.platform.base, self.platform.size as usize);
        env.load_image(
            (self.entry - self.platform.base) as usize,
            &image_bytes(&self.image.words),
        );
        let (trace, _crossings) = run::run_over(&mut env, self.entry, self.budget, &table);
        if format!("{:?}", trace.stop) != self.recorded.stop {
            return Err(format!(
                "stop mismatch: the bundle records '{}', the replay produced '{:?}' — the recorded result does not reproduce",
                self.recorded.stop, trace.stop
            ));
        }
        if self.recorded.steps.is_empty() && trace.steps.is_empty() {
            return Ok(Replay::Identical);
        }
        if self.recorded.steps.is_empty() || trace.steps.is_empty() {
            let longer = if trace.steps.is_empty() {
                "recorded"
            } else {
                "replay"
            };
            return Ok(Replay::LengthMismatch {
                agreed: 0,
                longer: longer.to_string(),
            });
        }
        match run::compare(&self.recorded.steps, &trace.steps, ("recorded", "replay")) {
            Ok(run::Verdict::Agree { .. }) => Ok(Replay::Identical),
            Ok(run::Verdict::Divergence(d)) => Ok(Replay::Mismatch(d)),
            Ok(run::Verdict::LengthMismatch { agreed, longer }) => {
                Ok(Replay::LengthMismatch { agreed, longer })
            }
            Err(why) => Err(format!("replay comparison refused: {why:?}")),
        }
    }

    /// Identity before execution: definition pins against the live manifest, then the
    /// image digest against the bundle's own words.
    fn check_identity(&self) -> Result<(), String> {
        let alg = &self.algorithm;
        if alg.profile != MANIFEST.profile {
            return Err(format!(
                "definition pin mismatch: the bundle records profile '{}', this build's definition is '{}'",
                alg.profile, MANIFEST.profile
            ));
        }
        if alg.ilen != MANIFEST.ilen {
            return Err(format!(
                "definition pin mismatch: the bundle records ilen {}, this build's definition carries {}",
                alg.ilen, MANIFEST.ilen
            ));
        }
        if alg.generator.0 != MANIFEST.generator.name
            || alg.generator.1 != MANIFEST.generator.sha256
        {
            return Err(format!(
                "definition pin mismatch: the bundle records generator '{}' (sha256 {}), this build's definition carries '{}' (sha256 {})",
                alg.generator.0, alg.generator.1, MANIFEST.generator.name, MANIFEST.generator.sha256
            ));
        }
        for (path, sha) in &alg.inputs {
            match MANIFEST.inputs.iter().find(|pin| pin.path == path) {
                Some(pin) if pin.sha256 == *sha => {}
                Some(pin) => {
                    return Err(format!(
                        "definition pin mismatch: input '{path}' is pinned to sha256 {sha} in the bundle but {sha_pin} in this build's definition",
                        sha_pin = pin.sha256
                    ));
                }
                None => {
                    return Err(format!(
                        "definition pin mismatch: the bundle pins input '{path}', which this build's definition does not carry"
                    ));
                }
            }
        }
        for pin in MANIFEST.inputs {
            if !alg.inputs.iter().any(|(path, _)| path == pin.path) {
                return Err(format!(
                    "definition pin mismatch: this build's definition pins input '{}', which the bundle does not carry",
                    pin.path
                ));
            }
        }
        let digest = sha256_hex(&image_bytes(&self.image.words));
        if digest != self.image.sha256 {
            return Err(format!(
                "image digest mismatch: the bundle records sha256 {want}, but its own words hash to {got} — the image was altered after recording",
                want = self.image.sha256,
                got = digest
            ));
        }
        check_layout(
            self.platform.base,
            self.platform.size,
            self.entry,
            image_bytes(&self.image.words).len(),
        )?;
        Ok(())
    }

    /// Serialize as JSON — the on-disk seed. Hand-rolled, like
    /// [`crate::report::to_json`]: the crate carries no dependencies and the shape is
    /// small and fixed.
    #[must_use]
    pub fn to_json(&self) -> String {
        let mut out = String::with_capacity(1024);
        out.push_str("{\"algorithm\":");
        push_algorithm(&mut out, &self.algorithm);
        out.push_str(",\"platform\":");
        push_platform(&mut out, &self.platform);
        out.push_str(",\"entry\":\"");
        push_hex64(&mut out, self.entry);
        out.push_str("\",\"image\":");
        push_image(&mut out, &self.image);
        out.push_str(",\"events\":{\"kind\":\"declared_none\",\"obligation\":\"");
        out.push_str(EVENT_OBLIGATION);
        out.push_str("\"},\"budget\":");
        out.push_str(&self.budget.to_string());
        out.push_str(",\"recorded\":");
        push_recorded(&mut out, &self.recorded);
        out.push('}');
        out
    }

    /// Parse a recorded bundle. Every missing or malformed accompaniment is an error
    /// **naming the field** — a bare seed is not a bundle, structurally.
    pub fn parse(text: &str) -> Result<Self, String> {
        let doc = json::parse(text).map_err(|e| format!("not JSON: {e}"))?;
        let root = doc
            .as_obj()
            .ok_or("bundle: the document is not an object")?;
        let algorithm = parse_algorithm(need(root, "algorithm", "bundle")?)?;
        let platform = parse_platform(need(root, "platform", "bundle")?)?;
        let entry = hex_u64(need(root, "entry", "bundle")?, "entry")?;
        let image = parse_image(need(root, "image", "bundle")?)?;
        let events = parse_events(need(root, "events", "bundle")?)?;
        let budget = int_usize(need(root, "budget", "bundle")?, "budget")?;
        let recorded = parse_recorded(need(root, "recorded", "bundle")?)?;
        Ok(Self {
            algorithm,
            platform,
            entry,
            image,
            events,
            budget,
            recorded,
        })
    }
}

/// The outcome of re-deriving a recorded result.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Replay {
    /// The recorded steps and stop reproduce exactly.
    Identical,
    /// The recorded and replayed streams first diverge here — step and field named.
    Mismatch(Divergence),
    /// One stream ended before the other; the agreeing prefix is not a pass.
    LengthMismatch { agreed: usize, longer: String },
}

/// Resolve a bundle model name to the instruction table it names. `"production"` is the
/// generated definition; `"mutant:<name>"` resolves through [`mutate::table_for`]. An
/// unknown name is an error naming it.
pub fn table_for_model(model: &str) -> Result<Vec<InsnDef>, String> {
    match model.strip_prefix("mutant:") {
        Some(name) => mutate::table_for(name).ok_or_else(|| {
            format!("unknown mutation '{name}' — not in the published suite vocabulary")
        }),
        None if model == "production" => Ok(semulith_core::definition::INSNS
            .iter()
            .map(|insn| InsnDef { ..*insn })
            .collect()),
        None => Err(format!(
            "unknown model '{model}' — wants 'production' or 'mutant:<name>'"
        )),
    }
}

/// The little-endian image bytes of one word sequence — the guest image, the thing the
/// digest guards.
pub(crate) fn image_bytes(words: &[u32]) -> Vec<u8> {
    let mut bytes = Vec::with_capacity(words.len() * 4);
    for word in words {
        bytes.extend_from_slice(&word.to_le_bytes());
    }
    bytes
}

fn algorithm_for(model: &str) -> Algorithm {
    Algorithm {
        harness: concat!("semulith-verify ", env!("CARGO_PKG_VERSION")).to_string(),
        model: model.to_string(),
        profile: MANIFEST.profile.to_string(),
        ilen: MANIFEST.ilen,
        generator: (
            MANIFEST.generator.name.to_string(),
            MANIFEST.generator.sha256.to_string(),
        ),
        inputs: MANIFEST
            .inputs
            .iter()
            .map(|pin| (pin.path.to_string(), pin.sha256.to_string()))
            .collect(),
    }
}

/// The image must lie inside the declared region: a replay that fetches outside the
/// recorded platform is a different experiment.
fn check_layout(base: u64, size: u64, entry: u64, image_len: usize) -> Result<(), String> {
    let top = base
        .checked_add(size)
        .ok_or("the declared region wraps the address space")?;
    if entry < base || entry >= top {
        return Err(format!(
            "entry {entry:#018x} lies outside the declared region [{base:#018x}, {top:#018x})"
        ));
    }
    let end = entry
        .checked_add(image_len as u64)
        .ok_or("the image end wraps the address space")?;
    if end > top {
        return Err(format!(
            "the image [{entry:#018x}, {end:#018x}) overruns the declared region [{base:#018x}, {top:#018x})"
        ));
    }
    Ok(())
}

fn push_hex64(out: &mut String, value: u64) {
    out.push_str(&format!("0x{value:016x}"));
}

fn push_algorithm(out: &mut String, alg: &Algorithm) {
    out.push_str("{\"harness\":\"");
    push_escaped(out, &alg.harness);
    out.push_str("\",\"model\":\"");
    push_escaped(out, &alg.model);
    out.push_str("\",\"definition\":{\"profile\":\"");
    push_escaped(out, &alg.profile);
    out.push_str("\",\"ilen\":");
    out.push_str(&alg.ilen.to_string());
    out.push_str(",\"generator\":{\"name\":\"");
    push_escaped(out, &alg.generator.0);
    out.push_str("\",\"sha256\":\"");
    push_escaped(out, &alg.generator.1);
    out.push_str("\"},\"inputs\":[");
    for (i, (path, sha)) in alg.inputs.iter().enumerate() {
        if i > 0 {
            out.push(',');
        }
        out.push_str("{\"path\":\"");
        push_escaped(out, path);
        out.push_str("\",\"sha256\":\"");
        push_escaped(out, sha);
        out.push_str("\"}");
    }
    out.push_str("]}}");
}

fn push_platform(out: &mut String, platform: &Platform) {
    out.push_str("{\"base\":\"");
    push_hex64(out, platform.base);
    out.push_str("\",\"size\":\"");
    push_hex64(out, platform.size);
    out.push_str("\"}");
}

fn push_image(out: &mut String, image: &Image) {
    out.push_str("{\"sha256\":\"");
    push_escaped(out, &image.sha256);
    out.push_str("\",\"words\":[");
    for (i, word) in image.words.iter().enumerate() {
        if i > 0 {
            out.push(',');
        }
        out.push_str(&format!("\"0x{word:08x}\""));
    }
    out.push_str("]}");
}

fn push_recorded(out: &mut String, recorded: &Recorded) {
    out.push_str("{\"stop\":\"");
    push_escaped(out, &recorded.stop);
    out.push_str("\",\"steps\":[");
    for (n, step) in recorded.steps.iter().enumerate() {
        if n > 0 {
            out.push(',');
        }
        out.push_str("{\"pc\":\"");
        push_hex64(out, step.pc);
        out.push_str("\",\"word\":");
        match step.word {
            Some(word) => out.push_str(&format!("\"0x{word:08x}\"")),
            // The fetch-fault step carries no word (run::Step); null is its honest form.
            None => out.push_str("null"),
        }
        out.push_str(",\"writes\":[");
        for (i, (reg, value)) in step.writes.iter().enumerate() {
            if i > 0 {
                out.push(',');
            }
            out.push_str(&format!("[{reg},\"0x{value:016x}\"]"));
        }
        out.push_str("],\"trap\":");
        match step.trap {
            Some((cause, tval)) => {
                out.push_str(&format!(
                    "{{\"cause\":\"0x{cause:02x}\",\"tval\":\"0x{tval:016x}\"}}"
                ));
            }
            None => out.push_str("null"),
        }
        out.push('}');
    }
    out.push_str("]}");
}

fn need<'a>(obj: &'a [(String, Json)], key: &str, what: &str) -> Result<&'a Json, String> {
    obj.iter()
        .rev()
        .find(|(k, _)| k == key)
        .map(|(_, v)| v)
        .ok_or_else(|| format!("{what}: missing '{key}' — a bare seed is not a bundle"))
}

fn hex_u64(node: &Json, what: &str) -> Result<u64, String> {
    let text = node
        .as_str()
        .ok_or_else(|| format!("{what}: wants a 0x-prefixed hex string"))?;
    let digits = text
        .strip_prefix("0x")
        .ok_or_else(|| format!("{what}: '{text}' wants a 0x prefix"))?;
    u64::from_str_radix(digits, 16).map_err(|_| format!("{what}: '{text}' is not hex"))
}

fn hex_u32(node: &Json, what: &str) -> Result<u32, String> {
    let value = hex_u64(node, what)?;
    u32::try_from(value).map_err(|_| format!("{what}: '{value:#x} does not fit 32 bits"))
}

fn hex_u8(node: &Json, what: &str) -> Result<u8, String> {
    let value = hex_u64(node, what)?;
    u8::try_from(value).map_err(|_| format!("{what}: '{value:#x} does not fit 8 bits"))
}

fn int_usize(node: &Json, what: &str) -> Result<usize, String> {
    match node {
        Json::Int(value) if *value >= 0 => usize::try_from(*value)
            .map_err(|_| format!("{what}: {value} does not fit this host's usize")),
        _ => Err(format!("{what}: wants a non-negative integer")),
    }
}

fn parse_algorithm(node: &Json) -> Result<Algorithm, String> {
    let obj = node.as_obj().ok_or("algorithm: wants an object")?;
    let harness = need(obj, "harness", "algorithm")?
        .as_str()
        .ok_or("algorithm.harness: wants a string")?
        .to_string();
    let model = need(obj, "model", "algorithm")?
        .as_str()
        .ok_or("algorithm.model: wants a string — 'production' or 'mutant:<name>'")?
        .to_string();
    if model != "production" && !model.starts_with("mutant:") {
        return Err(format!(
            "algorithm.model: '{model}' wants 'production' or 'mutant:<name>'"
        ));
    }
    let definition = need(obj, "definition", "algorithm")?
        .as_obj()
        .ok_or("algorithm.definition: wants an object")?;
    let profile = need(definition, "profile", "algorithm.definition")?
        .as_str()
        .ok_or("algorithm.definition.profile: wants a string")?
        .to_string();
    let ilen = match need(definition, "ilen", "algorithm.definition")? {
        Json::Int(value) if *value >= 0 => u32::try_from(*value)
            .map_err(|_| "algorithm.definition.ilen: does not fit u32".to_string())?,
        _ => return Err("algorithm.definition.ilen: wants a non-negative integer".to_string()),
    };
    let generator_obj = need(definition, "generator", "algorithm.definition")?
        .as_obj()
        .ok_or("algorithm.definition.generator: wants an object")?;
    let generator = (
        need(generator_obj, "name", "algorithm.definition.generator")?
            .as_str()
            .ok_or("algorithm.definition.generator.name: wants a string")?
            .to_string(),
        need(generator_obj, "sha256", "algorithm.definition.generator")?
            .as_str()
            .ok_or("algorithm.definition.generator.sha256: wants a string")?
            .to_string(),
    );
    let inputs_node = need(definition, "inputs", "algorithm.definition")?
        .as_arr()
        .ok_or("algorithm.definition.inputs: wants an array")?;
    let mut inputs = Vec::with_capacity(inputs_node.len());
    for (i, pin) in inputs_node.iter().enumerate() {
        let pin_obj = pin
            .as_obj()
            .ok_or_else(|| format!("algorithm.definition.inputs[{i}]: wants an object"))?;
        inputs.push((
            need(pin_obj, "path", "algorithm.definition.inputs")?
                .as_str()
                .ok_or("algorithm.definition.inputs.path: wants a string")?
                .to_string(),
            need(pin_obj, "sha256", "algorithm.definition.inputs")?
                .as_str()
                .ok_or("algorithm.definition.inputs.sha256: wants a string")?
                .to_string(),
        ));
    }
    Ok(Algorithm {
        harness,
        model,
        profile,
        ilen,
        generator,
        inputs,
    })
}

fn parse_platform(node: &Json) -> Result<Platform, String> {
    let obj = node.as_obj().ok_or("platform: wants an object")?;
    Ok(Platform {
        base: hex_u64(need(obj, "base", "platform")?, "platform.base")?,
        size: hex_u64(need(obj, "size", "platform")?, "platform.size")?,
    })
}

fn parse_image(node: &Json) -> Result<Image, String> {
    let obj = node.as_obj().ok_or("image: wants an object")?;
    let sha256 = need(obj, "sha256", "image")?
        .as_str()
        .ok_or("image.sha256: wants a string")?
        .to_string();
    let words_node = need(obj, "words", "image")?
        .as_arr()
        .ok_or("image.words: wants an array")?;
    let mut words = Vec::with_capacity(words_node.len());
    for (i, word) in words_node.iter().enumerate() {
        words.push(hex_u32(word, &format!("image.words[{i}]"))?);
    }
    Ok(Image { words, sha256 })
}

fn parse_events(node: &Json) -> Result<Events, String> {
    let obj = node.as_obj().ok_or("events: wants an object")?;
    match need(obj, "kind", "events")?
        .as_str()
        .ok_or("events.kind: wants a string")?
    {
        "declared_none" => Ok(Events::DeclaredNone),
        other => Err(format!(
            "events.kind: '{other}' is not this platform's recorded event policy — {EVENT_OBLIGATION} declares no asynchronous event; a scripted stream is not a recorded choice of rv64i-lab-v0"
        )),
    }
}

fn parse_recorded(node: &Json) -> Result<Recorded, String> {
    let obj = node.as_obj().ok_or("recorded: wants an object")?;
    let stop = need(obj, "stop", "recorded")?
        .as_str()
        .ok_or("recorded.stop: wants a string")?
        .to_string();
    let steps_node = need(obj, "steps", "recorded")?
        .as_arr()
        .ok_or("recorded.steps: wants an array")?;
    let mut steps = Vec::with_capacity(steps_node.len());
    for (n, step) in steps_node.iter().enumerate() {
        let step_obj = step
            .as_obj()
            .ok_or_else(|| format!("recorded.steps[{n}]: wants an object"))?;
        let mut writes = Vec::new();
        let writes_node = need(step_obj, "writes", "recorded.steps")?
            .as_arr()
            .ok_or("recorded.steps.writes: wants an array")?;
        for (i, write) in writes_node.iter().enumerate() {
            let pair = write
                .as_arr()
                .ok_or_else(|| format!("recorded.steps.writes[{i}]: wants [reg, \"hexvalue\"]"))?;
            if pair.len() != 2 {
                return Err(format!(
                    "recorded.steps.writes[{i}]: wants exactly [reg, \"hexvalue\"]"
                ));
            }
            let reg = match pair[0] {
                Json::Int(value) if (0..=31).contains(&value) => value as u8,
                _ => {
                    return Err(format!(
                        "recorded.steps.writes[{i}][0]: wants a register index 0..=31"
                    ))
                }
            };
            let value = hex_u64(&pair[1], &format!("recorded.steps.writes[{i}][1]"))?;
            writes.push((reg, value));
        }
        let trap = match need(step_obj, "trap", "recorded.steps")? {
            Json::Null => None,
            trap_obj => {
                let trap_obj = trap_obj
                    .as_obj()
                    .ok_or("recorded.steps.trap: wants an object or null")?;
                Some((
                    hex_u8(
                        need(trap_obj, "cause", "recorded.steps.trap")?,
                        "recorded.steps.trap.cause",
                    )?,
                    hex_u64(
                        need(trap_obj, "tval", "recorded.steps.trap")?,
                        "recorded.steps.trap.tval",
                    )?,
                ))
            }
        };
        steps.push(Step {
            pc: hex_u64(need(step_obj, "pc", "recorded.steps")?, "recorded.steps.pc")?,
            word: match need(step_obj, "word", "recorded.steps")? {
                // The fetch-fault step is recorded with a null word.
                Json::Null => None,
                word_node => Some(hex_u32(word_node, "recorded.steps.word")?),
            },
            writes,
            trap,
        });
    }
    Ok(Recorded { steps, stop })
}

#[cfg(test)]
mod tests;

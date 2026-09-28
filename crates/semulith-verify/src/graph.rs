//! The requirement/evidence/obligation graph checker — task card T004, the executable form
//! of `docs/EVIDENCE_AND_GATES.md` §3 over the frozen JSONL records.
//!
//! What it checks, each rule a named arm so a finding names its contract:
//!
//! - [`Rule::UniqueId`] — a catalogue may not carry two records with the same id (the
//!   id→record map collapses duplicates silently; a catalogue lying about its own identity
//!   would have every other rule check only the survivor);
//! - [`Rule::OrphanEvidence`] — every `evidence_ids` entry on a requirement names an evidence
//!   record that exists;
//! - [`Rule::OrphanLink`] — `requirement_ids`, `obligation_ids`, and `dependencies` edges
//!   resolve across the union, so a deleted node or edge cannot silently orphan a record
//!   (the §3 invariant "removed nodes/edges cannot silently make affected requirements or
//!   tests disappear from the report");
//! - [`Rule::OrphanSource`] — every `source_refs.source_id` names a source the ledger pins
//!   (SRC-03 one layer up: a locator into a document nobody acquired is not a citation);
//! - [`Rule::Scope`] — every record's `profile_ids` names a profile the fixture context
//!   declares (profile-scope consistency);
//! - [`Rule::ArtifactHash`] — every artifact/input carrying `path` + `sha256` resolves
//!   through the injected resolver and hashes to its recorded value — artifact existence
//!   and freshness, "stale hash" named as such;
//! - [`Rule::MissingEvidence`] — every obligation the context declares has at least one
//!   evidence record citing it;
//! - [`Rule::ContextCheck`] — a contract obligation's `required_checks` name check ids the
//!   fixture context declares;
//! - [`Rule::DepCycle`] — requirement dependencies are acyclic.
//!
//! ⛔ The gate policy is honest by construction: a [`GateStatus::Passed`] verdict requires
//! zero findings AND every declared obligation pointed at by **successful, current** evidence
//! (schema-level completion data plus hashes that verify here); anything less is
//! [`GateStatus::Incomplete`], never a silent pass — "missing required checks produce
//! `incomplete`, not `passed`" (`docs/EVIDENCE_AND_GATES.md` §4). The frozen examples are
//! deliberately `planned`, so the expected verdict on them is `incomplete`.
//!
//! The library never touches the filesystem: evidence bytes arrive through a resolver
//! closure, keeping the crate buildable for `wasm32-unknown-unknown` (PORT-WEB) and the
//! checker's verdicts a pure function of its inputs.

use crate::json::Json;
use crate::sha256::sha256_hex;

/// One rule of the graph contract — a finding carries it so the failure names what broke.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Rule {
    /// two records share an id inside one catalogue
    UniqueId,
    /// a requirement cites an evidence id that does not exist
    OrphanEvidence,
    /// an edge (requirement/obligation/dependency/check) names a node that does not exist
    OrphanLink,
    /// a `source_refs.source_id` names nothing the source ledger pins
    OrphanSource,
    /// a record applies to a profile the fixture context does not declare
    Scope,
    /// an artifact is missing, or its bytes do not hash to the recorded value
    ArtifactHash,
    /// a declared obligation has no evidence record citing it
    MissingEvidence,
    /// a contract `required_checks` id is not declared in the fixture context
    ContextCheck,
    /// requirement `dependencies` contain a cycle
    DepCycle,
}

impl Rule {
    /// the stable tag a finding line carries
    #[must_use]
    pub const fn tag(self) -> &'static str {
        match self {
            Self::UniqueId => "UNIQUE-ID",
            Self::OrphanEvidence => "ORPHAN-EVIDENCE",
            Self::OrphanLink => "ORPHAN-LINK",
            Self::OrphanSource => "ORPHAN-SOURCE",
            Self::Scope => "SCOPE",
            Self::ArtifactHash => "ARTIFACT-HASH",
            Self::MissingEvidence => "MISSING-EVIDENCE",
            Self::ContextCheck => "CONTEXT-CHECK",
            Self::DepCycle => "DEP-CYCLE",
        }
    }
}

/// A bundle of parsed record catalogues plus the fixture context and the source ledger.
#[derive(Clone, Debug)]
pub struct Bundle {
    /// requirement records, one JSON value per JSONL line
    pub requirements: Vec<Json>,
    /// evidence records
    pub evidence: Vec<Json>,
    /// contract-obligation records
    pub obligations: Vec<Json>,
    /// the fixture context (`fixture-context.json`)
    pub context: Json,
    /// the source ledger (`sources.json`)
    pub sources: Json,
}

impl Bundle {
    /// requirement ids in catalogue order
    fn requirement_ids(&self) -> Vec<&str> {
        ids(&self.requirements)
    }

    /// evidence ids in catalogue order
    fn evidence_ids(&self) -> Vec<&str> {
        ids(&self.evidence)
    }

    /// obligation ids the fixture context declares
    fn context_obligation_ids(&self) -> Vec<&str> {
        string_ids(&self.context, "obligations")
    }

    /// check ids the fixture context declares (on its obligations)
    fn context_check_ids(&self) -> Vec<&str> {
        let mut out = Vec::new();
        if let Some(obs) = self.context.get("obligations").and_then(Json::as_arr) {
            for ob in obs {
                if let Some(checks) = ob.get("check_ids").and_then(Json::as_arr) {
                    for c in checks {
                        if let Some(s) = c.as_str() {
                            out.push(s);
                        }
                    }
                }
            }
        }
        out
    }

    /// profile ids the fixture context declares
    fn context_profile_ids(&self) -> Vec<&str> {
        string_ids(&self.context, "profiles")
    }

    /// source ids the ledger pins
    fn ledger_source_ids(&self) -> Vec<&str> {
        string_ids(&self.sources, "sources")
    }
}

fn ids(records: &[Json]) -> Vec<&str> {
    records
        .iter()
        .filter_map(|r| r.get("id").and_then(Json::as_str))
        .collect()
}

fn string_ids<'a>(doc: &'a Json, key: &str) -> Vec<&'a str> {
    doc.get(key)
        .and_then(Json::as_arr)
        .map(|items| {
            items
                .iter()
                .filter_map(|i| i.get("id").and_then(Json::as_str))
                .collect()
        })
        .unwrap_or_default()
}

fn str_list<'a>(record: &'a Json, key: &str) -> Vec<&'a str> {
    record
        .get(key)
        .and_then(Json::as_arr)
        .map(|items| items.iter().filter_map(Json::as_str).collect())
        .unwrap_or_default()
}

/// A single defect: the rule, the record (or edge) it attaches to, and what was measured.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Finding {
    /// which graph rule failed
    pub rule: Rule,
    /// the subject — a catalogue record id, or an edge description
    pub subject: String,
    /// the measured reason
    pub detail: String,
}

impl Finding {
    fn new(rule: Rule, subject: impl Into<String>, detail: impl Into<String>) -> Self {
        Self {
            rule,
            subject: subject.into(),
            detail: detail.into(),
        }
    }
}

/// The gate verdict — `docs/EVIDENCE_AND_GATES.md` §7's three states.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum GateStatus {
    /// no findings and every declared obligation is met by successful, current evidence
    Passed,
    /// no findings, but at least one obligation lacks successful current evidence
    Incomplete,
    /// at least one finding — the bundle is rejected
    Failed,
}

impl GateStatus {
    /// the stable word the report line carries
    #[must_use]
    pub const fn word(self) -> &'static str {
        match self {
            Self::Passed => "passed",
            Self::Incomplete => "incomplete",
            Self::Failed => "failed",
        }
    }
}

/// The checker's verdict over a bundle.
#[derive(Clone, Debug)]
pub struct Report {
    /// every measured defect, in rule order
    pub findings: Vec<Finding>,
    /// the gate verdict
    pub gate: GateStatus,
    /// per declared obligation: met by passed, current evidence?
    pub obligations: Vec<(String, bool)>,
}

impl Report {
    /// The verdict as the report presentation renders it (used by the CLI and the tests).
    #[must_use]
    pub fn render(&self, bundle: &Bundle) -> String {
        let mut out = String::new();
        out.push_str(&format!(
            "graph check: {} requirement(s), {} evidence record(s), {} obligation(s)\n",
            bundle.requirements.len(),
            bundle.evidence.len(),
            bundle.obligations.len()
        ));
        for f in &self.findings {
            out.push_str(&format!("  {} {}: {}\n", f.rule.tag(), f.subject, f.detail));
        }
        match self.gate {
            GateStatus::Passed => out
                .push_str("gate: passed — every declared obligation is met by current evidence\n"),
            GateStatus::Incomplete => {
                let unmet: Vec<&str> = self
                    .obligations
                    .iter()
                    .filter(|(_, met)| !met)
                    .map(|(id, _)| id.as_str())
                    .collect();
                out.push_str(&format!(
                    "gate: incomplete — no graph defects, but {} declared obligation(s) lack successful current evidence: {}\n",
                    unmet.len(),
                    unmet.join(", ")
                ));
            }
            GateStatus::Failed => out.push_str(&format!(
                "gate: failed — {} finding(s) reject the bundle\n",
                self.findings.len()
            )),
        }
        out
    }
}

/// Check a bundle. `artifacts` resolves a recorded `path` to its bytes; `None` means the
/// artifact does not exist — a finding, never a skipped row. Schema validity is the
/// caller's first phase; this phase assumes the catalogues parsed and validates the graph.
pub fn check_bundle(bundle: &Bundle, artifacts: &dyn Fn(&str) -> Option<Vec<u8>>) -> Report {
    let mut findings = Vec::new();

    unique_ids(&bundle.requirements, "requirements", &mut findings);
    unique_ids(&bundle.evidence, "evidence", &mut findings);
    unique_ids(&bundle.obligations, "obligations", &mut findings);

    let req_ids = bundle.requirement_ids();
    let ev_ids = bundle.evidence_ids();
    let ctx_ob_ids = bundle.context_obligation_ids();
    let ctx_profiles = bundle.context_profile_ids();
    let ctx_checks = bundle.context_check_ids();
    let ledger = bundle.ledger_source_ids();

    check_scopes(bundle, &ctx_profiles, &mut findings);
    check_sources(bundle, &ledger, &mut findings);
    check_requirement_links(bundle, &ev_ids, &ctx_ob_ids, &req_ids, &mut findings);
    check_evidence_links(bundle, &req_ids, &ctx_ob_ids, &mut findings);
    check_obligation_links(bundle, &req_ids, &ctx_checks, &mut findings);
    check_artifact_hashes(bundle, artifacts, &mut findings);
    let evidence_with_hash_findings = subjects_with_hash_findings(&findings);
    check_missing_evidence(bundle, &ctx_ob_ids, &mut findings);
    check_dep_cycles(bundle, &req_ids, &mut findings);

    let obligations: Vec<(String, bool)> = ctx_ob_ids
        .iter()
        .map(|oid| {
            let met = bundle.evidence.iter().any(|ev| {
                str_list(ev, "obligation_ids").contains(oid)
                    && ev.get("status").and_then(Json::as_str) == Some("passed")
                    && !evidence_with_hash_findings.contains(&record_key("evidence", ev))
            });
            ((*oid).to_string(), met)
        })
        .collect();

    let gate = if !findings.is_empty() {
        GateStatus::Failed
    } else if obligations.iter().all(|(_, met)| *met) {
        GateStatus::Passed
    } else {
        GateStatus::Incomplete
    };

    Report {
        findings,
        gate,
        obligations,
    }
}

fn record_key(catalogue: &str, record: &Json) -> String {
    format!(
        "{catalogue}:{}",
        record.get("id").and_then(Json::as_str).unwrap_or("<no id>")
    )
}

fn subjects_with_hash_findings(findings: &[Finding]) -> std::collections::BTreeSet<String> {
    findings
        .iter()
        .filter(|f| f.rule == Rule::ArtifactHash)
        .map(|f| f.subject.clone())
        .collect()
}

fn unique_ids(records: &[Json], catalogue: &str, findings: &mut Vec<Finding>) {
    let mut seen = std::collections::BTreeSet::new();
    for r in records {
        let Some(id) = r.get("id").and_then(Json::as_str) else {
            continue;
        };
        if !seen.insert(id.to_string()) {
            findings.push(Finding::new(
                Rule::UniqueId,
                format!("{catalogue}:{id}"),
                "the id appears twice — the id→record map collapses duplicates, so every rule below would have checked only the survivor",
            ));
        }
    }
}

fn check_scopes(bundle: &Bundle, ctx_profiles: &[&str], findings: &mut Vec<Finding>) {
    for (catalogue, records) in [
        ("requirements", &bundle.requirements),
        ("evidence", &bundle.evidence),
        ("obligations", &bundle.obligations),
    ] {
        for r in records {
            for pid in str_list(r, "profile_ids") {
                if !ctx_profiles.contains(&pid) {
                    findings.push(Finding::new(
                        Rule::Scope,
                        record_key(catalogue, r),
                        format!("applies to profile '{pid}', which the fixture context does not declare"),
                    ));
                }
            }
        }
    }
}

fn check_sources(bundle: &Bundle, ledger: &[&str], findings: &mut Vec<Finding>) {
    for (catalogue, records) in [
        ("requirements", &bundle.requirements),
        ("evidence", &bundle.evidence),
        ("obligations", &bundle.obligations),
    ] {
        for r in records {
            for sref in r
                .get("source_refs")
                .and_then(Json::as_arr)
                .unwrap_or(&[])
                .iter()
            {
                if let Some(sid) = sref.get("source_id").and_then(Json::as_str) {
                    if !ledger.contains(&sid) {
                        findings.push(Finding::new(
                            Rule::OrphanSource,
                            record_key(catalogue, r),
                            format!("cites source '{sid}', which the source ledger does not pin"),
                        ));
                    }
                }
            }
        }
    }
}

fn check_requirement_links(
    bundle: &Bundle,
    ev_ids: &[&str],
    ctx_ob_ids: &[&str],
    req_ids: &[&str],
    findings: &mut Vec<Finding>,
) {
    for r in &bundle.requirements {
        let key = record_key("requirements", r);
        for eid in str_list(r, "evidence_ids") {
            if !ev_ids.contains(&eid) {
                findings.push(Finding::new(
                    Rule::OrphanEvidence,
                    key.clone(),
                    format!("cites evidence '{eid}', which no evidence record provides — the link is stale or was deleted"),
                ));
            }
        }
        for oid in str_list(r, "obligation_ids") {
            if !ctx_ob_ids.contains(&oid) {
                findings.push(Finding::new(
                    Rule::OrphanLink,
                    key.clone(),
                    format!("cites obligation '{oid}', which the fixture context does not declare"),
                ));
            }
        }
        for dep in str_list(r, "dependencies") {
            if !req_ids.contains(&dep) {
                findings.push(Finding::new(
                    Rule::OrphanLink,
                    key.clone(),
                    format!("depends on requirement '{dep}', which does not exist — a deleted dependency link"),
                ));
            }
        }
    }
}

fn check_evidence_links(
    bundle: &Bundle,
    req_ids: &[&str],
    ctx_ob_ids: &[&str],
    findings: &mut Vec<Finding>,
) {
    for ev in &bundle.evidence {
        let key = record_key("evidence", ev);
        for rid in str_list(ev, "requirement_ids") {
            if !req_ids.contains(&rid) {
                findings.push(Finding::new(
                    Rule::OrphanLink,
                    key.clone(),
                    format!("cites requirement '{rid}', which does not exist"),
                ));
            }
        }
        for oid in str_list(ev, "obligation_ids") {
            if !ctx_ob_ids.contains(&oid) {
                findings.push(Finding::new(
                    Rule::OrphanLink,
                    key.clone(),
                    format!("cites obligation '{oid}', which the fixture context does not declare"),
                ));
            }
        }
    }
}

fn check_obligation_links(
    bundle: &Bundle,
    req_ids: &[&str],
    ctx_checks: &[&str],
    findings: &mut Vec<Finding>,
) {
    for ob in &bundle.obligations {
        let key = record_key("obligations", ob);
        for dep in str_list(ob, "dependencies") {
            if !req_ids.contains(&dep) {
                findings.push(Finding::new(
                    Rule::OrphanLink,
                    key.clone(),
                    format!("depends on requirement '{dep}', which does not exist — a deleted dependency link"),
                ));
            }
        }
        for chk in str_list(ob, "required_checks") {
            if !ctx_checks.contains(&chk) {
                findings.push(Finding::new(
                    Rule::ContextCheck,
                    key.clone(),
                    format!("requires check '{chk}', which the fixture context does not declare"),
                ));
            }
        }
    }
}

fn check_artifact_hashes(
    bundle: &Bundle,
    artifacts: &dyn Fn(&str) -> Option<Vec<u8>>,
    findings: &mut Vec<Finding>,
) {
    for ev in &bundle.evidence {
        let key = record_key("evidence", ev);
        for list_key in ["inputs", "artifacts"] {
            let entries = ev.get(list_key).and_then(Json::as_arr).unwrap_or(&[]);
            for entry in entries.iter() {
                let (Some(path), Some(want)) = (
                    entry.get("path").and_then(Json::as_str),
                    entry.get("sha256").and_then(Json::as_str),
                ) else {
                    continue; // shape is the schema phase's job
                };
                match artifacts(path) {
                    None => findings.push(Finding::new(
                        Rule::ArtifactHash,
                        key.clone(),
                        format!("{list_key} names '{path}', which does not exist"),
                    )),
                    Some(bytes) => {
                        let got = sha256_hex(&bytes);
                        if got != want {
                            findings.push(Finding::new(
                                Rule::ArtifactHash,
                                key.clone(),
                                format!("{list_key} '{path}' hashes to {got}, the record pins {want} — a stale hash"),
                            ));
                        }
                    }
                }
            }
        }
    }
}

fn check_missing_evidence(bundle: &Bundle, ctx_ob_ids: &[&str], findings: &mut Vec<Finding>) {
    for oid in ctx_ob_ids {
        let cited = bundle
            .evidence
            .iter()
            .any(|ev| str_list(ev, "obligation_ids").contains(oid));
        if !cited {
            findings.push(Finding::new(
                Rule::MissingEvidence,
                format!("context:{oid}"),
                "the declared obligation has no evidence record citing it — the requirement it owns would silently drop out of any report",
            ));
        }
    }
}

fn check_dep_cycles(bundle: &Bundle, req_ids: &[&str], findings: &mut Vec<Finding>) {
    // iterative DFS over requirements' dependencies; only edges that resolve are walked
    #[derive(Clone, Copy, PartialEq, Eq)]
    enum Mark {
        InStack,
        Done,
    }
    let mut marks: std::collections::BTreeMap<&str, Mark> = std::collections::BTreeMap::new();
    for start in req_ids {
        if marks.contains_key(start) {
            continue;
        }
        let mut stack: Vec<(&str, Vec<&str>)> = vec![(start, str_list_by_id(bundle, start))];
        marks.insert(start, Mark::InStack);
        while let Some((node, mut deps)) = stack.pop() {
            if let Some(dep) = deps.pop() {
                stack.push((node, deps));
                if !req_ids.contains(&dep) {
                    continue; // unresolved edges are ORPHAN-LINK's finding
                }
                match marks.get(dep) {
                    Some(Mark::InStack) => {
                        findings.push(Finding::new(
                            Rule::DepCycle,
                            format!("requirements:{node}"),
                            format!("dependency on '{dep}' closes a cycle — requirement dependencies must be acyclic"),
                        ));
                    }
                    Some(Mark::Done) => {}
                    None => {
                        marks.insert(dep, Mark::InStack);
                        stack.push((dep, str_list_by_id(bundle, dep)));
                    }
                }
            } else {
                marks.insert(node, Mark::Done);
            }
        }
    }
}

fn str_list_by_id<'a>(bundle: &'a Bundle, id: &str) -> Vec<&'a str> {
    bundle
        .requirements
        .iter()
        .find(|r| r.get("id").and_then(Json::as_str) == Some(id))
        .map(|r| str_list(r, "dependencies"))
        .unwrap_or_default()
}

#[cfg(test)]
mod tests;

# Glossary — v0.2

| Term | Meaning in this project |
|---|---|
| Architecture / ISA | Rules presented to software by a processor family, including applicable instruction and system behavior |
| Profile | Versioned selection of architecture revisions, features, parameters, environment and support scope |
| Canonical definition | The single owned executable interpretation used to derive a production processor/device model |
| External authority | Applicable manufacturer or standards specification; our interpretation remains subject to it |
| Dossier | Profile, sources, requirements, questions, state/semantics and evidence for one target |
| Requirement | Identified source-linked obligation; not merely an implementation task |
| Verification disposition | How an obligation is to be checked and the recorded evidence/limitations supporting its status |
| Oracle / reference | A source of expected behavior with explicit scope, provenance, configuration and possible correlated errors |
| Observation contract | Which state, effects, ordering and progress are compared and under what equivalences |
| Environment contract | CPU assumptions and provider guarantees defining legal memory, event, time and other interactions |
| Laboratory | Controlled processor testing environment; not a physical or virtual board model |
| Model limitation | Supported target behavior that this implementation cannot currently model; not a target illegal-instruction trap |
| Validated | Met a named engineering evidence policy for an explicit scope and artifact version |
| Proved | Established a stated proposition through a checked argument with recorded assumptions and bounds |
| Locked | Versioned accepted profile with attached evidence; corrections reopen affected obligations |
| Gate | Reproducible acceptance predicate over configuration, requirements, artifacts and current evidence |
| Conformance | Produced behavior satisfies the relevant specification contract; exact scope and evidence must be stated |
| Exploration coverage | Which allowed choices/interleavings/outcomes were considered; distinct from producing only legal behavior |
| Canonical input fingerprint | Hash/version identity of definition and configuration used by a generated or checked artifact |
| Independent evidence | Evidence whose relevant expected behavior does not merely originate from the same implementation or mistaken derivation |
| Diagnostic tracing | Optional recording of execution; distinct from semantic effects needed for correct behavior |
| Software computer | CPU(s), memory, devices, board wiring, boot environment and guest payloads composed in software |
| eADL | archogen's functional HW/OS description system; no implementation bodies or implementation-provider selection |
| archogen | OS-generation engine and catalogs that realize eADL requirements and compose simulator models |
| Platform contract | Assembled-machine capabilities plus boot/test interface exposed to an OS producer; distinct from the CPU/environment contract |

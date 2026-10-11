#!/usr/bin/env python3
"""Offline artifact grammar controls. Dummy pins are never execution evidence."""
from __future__ import annotations

import argparse
import copy
from pathlib import Path
import sys
import types
import unittest
from unittest import mock

import dossier_sexp as D
import matched_gpr_artifacts as A
import records_sexp as R
import sexp as S

DEPENDENCIES_PATH = "target/illustrative/dependencies.sexp"
CAPTURE_PATH = "target/illustrative/capture.sexp"


def dependencies():
    return {"format_version": "matched-gpr-dependencies-v1", "input": [
        {"id": "policy", "role": "evidence-policy", "path": "profiles/rv64gc-lab-v0/EVIDENCE_POLICY.md", "sha256": "a" * 64},
        {"id": "mapper", "role": "mapping", "path": "scripts/dossier_sexp.py", "sha256": "b" * 64}]}


def capture():
    return {"format_version": "sail-gpr-capture-v1", "run_id": "base", "run_kind": "baseline",
            "argv": ["reference/bin/sail", "--example", "", "--example", "λ"],
            "process_exit": 0, "reference_candidate_id": "sail-riscv",
            "reference_binary_sha256": "c" * 64, "collector_input_id": "collector",
            "input": [{"id": "collector", "sha256": "d" * 64}, {"id": "guest", "sha256": "e" * 64}],
            "observation": [
                {"id": "trace", "role": "raw-gpr", "path": "target/illustrative/base.trace", "byte_size": 1, "sha256": "f" * 64},
                {"id": "stdout", "role": "process-stdout", "path": "target/illustrative/base.stdout", "byte_size": 0, "sha256": "0" * 64},
                {"id": "stderr", "role": "process-stderr", "path": "target/illustrative/base.stderr", "byte_size": 0, "sha256": "1" * 64}],
            "host": {"os": "illustrative", "kernel": "unknown", "arch": "example"},
            "tool": [{"id": "python", "version": "illustrative"}, {"id": "collector", "version": "sha256:dummy"}]}


def raw(doc, family):
    mapper = D.dependencies_to_form if family == "dependencies" else D.capture_to_form
    return R.render_forms([mapper(doc)]).encode()


def parser(family):
    return A.parse_dependencies if family == "dependencies" else A.parse_capture


def location(family):
    return DEPENDENCIES_PATH if family == "dependencies" else CAPTURE_PATH


class ArtifactTests(unittest.TestCase):
    def refuse(self, payload, family, reason):
        with self.assertRaisesRegex(A.ArtifactError, reason):
            parser(family)(payload, path=location(family))

    def documents(self):
        return (("dependencies", dependencies()), ("capture", capture()))

    def test_lossless_complete_documents(self):
        for family, doc in self.documents():
            with self.subTest(family=family):
                self.assertEqual(parser(family)(raw(doc, family), path=location(family)), doc)
                encoder = A.encode_dependencies if family == "dependencies" else A.encode_capture
                self.assertEqual(encoder(doc, path=location(family)), raw(doc, family))

    def test_order_repeated_empty_and_unicode_argv(self):
        doc = capture()
        result = A.parse_capture(raw(doc, "capture"), path=CAPTURE_PATH)
        self.assertEqual(result["argv"], doc["argv"])
        self.assertEqual(result["tool"], doc["tool"])
        self.assertEqual(result["observation"], doc["observation"])

    def test_coherent_failed_process_is_data(self):
        for status in (-9, 1, 127):
            for kind in ("baseline", "repeat", "control"):
                with self.subTest(status=status, kind=kind):
                    doc = capture(); doc.update(process_exit=status, run_kind=kind)
                    doc["observation"][0]["byte_size"] = 0
                    self.assertEqual(A.parse_capture(raw(doc, "capture"), path=CAPTURE_PATH), doc)

    def test_parser_does_not_authenticate_or_execute(self):
        # No actual fixture files exist; only the two project-tool schemas are read.
        A._schema("dependencies"); A._schema("capture")
        with mock.patch.object(Path, "open", side_effect=AssertionError("artifact reopened")):
            for family, doc in self.documents():
                self.assertEqual(parser(family)(raw(doc, family), path=location(family)), doc)

    def test_exact_byte_limit(self):
        for family, doc in self.documents():
            payload = raw(doc, family)
            payload += b" " * (A.DOCUMENT_BYTES - len(payload))
            self.assertEqual(parser(family)(payload, path=location(family)), doc)
            self.refuse(payload + b" ", family, "payload")

    def test_limit_refuses_before_parser(self):
        for family, _ in self.documents():
            with mock.patch.object(S, "parse", side_effect=AssertionError("parsed oversize")):
                self.refuse(b" " * (A.DOCUMENT_BYTES + 1), family, "payload")

    def test_utf8_byte_limit_is_not_character_count(self):
        for family, doc in self.documents():
            payload = raw(doc, family) + ('\n;' + 'λ' * (A.DOCUMENT_BYTES // 2)).encode()
            self.assertGreater(len(payload), A.DOCUMENT_BYTES)
            self.refuse(payload, family, "payload")

    def test_immutable_bytes_required(self):
        for family, doc in self.documents():
            for value in (raw(doc, family).decode(), bytearray(raw(doc, family)), memoryview(raw(doc, family)), None):
                with self.subTest(family=family, value=type(value)):
                    self.refuse(value, family, "snapshot bytes")

    def test_empty_malformed_and_non_utf8(self):
        for family, _ in self.documents():
            for payload in (b"", b"\xff", b"(", b")", b"()", b"42", b'("capture")', b"(comment)", b"(comment 1)"):
                with self.subTest(family=family, payload=payload):
                    self.refuse(payload, family, ".")

    def test_extreme_nesting_and_integer_refuse(self):
        for family, _ in self.documents():
            for payload in (b"(" * 2000 + b")" * 2000, b"9" * 5000):
                self.refuse(payload, family, ".")

    def test_exactly_one_root(self):
        for family, doc in self.documents():
            payload = raw(doc, family)
            for value in (b" ", b'(comment "only annotation")', payload + payload):
                self.refuse(value, family, "exactly one")

    def test_wrong_declared_root_refuses(self):
        for family, doc in self.documents():
            # A construct declared by this schema still cannot become its document.
            mapper = D.dependencies_to_form if family == "dependencies" else D.capture_to_form
            form = S.children(mapper(doc), "input")[0]
            self.refuse(R.render_forms([form]).encode(), family, "exactly one")

    def test_annotations_preserve_data(self):
        for family, doc in self.documents():
            mapper = D.dependencies_to_form if family == "dependencies" else D.capture_to_form
            form = mapper(doc)
            for node in self.nodes(form):
                node.append([S.Symbol("comment"), "λ; annotation\nline"])
            payload = R.render_forms([[S.Symbol("comment"), "top"], form]).encode()
            self.assertEqual(parser(family)(payload, path=location(family)), doc)

    @staticmethod
    def nodes(form):
        # Only record nodes; scalar fields have no nested data children.
        return [form] + [child for child in form[1:] if isinstance(child, list)
                         and any(isinstance(value, list) for value in child[1:])]

    def test_unknown_field_at_every_depth(self):
        for family, doc in self.documents():
            mapper = D.dependencies_to_form if family == "dependencies" else D.capture_to_form
            original = mapper(doc)
            for index in range(len(self.nodes(original))):
                form = copy.deepcopy(original)
                self.nodes(form)[index].append([S.Symbol("unexpected"), "value"])
                self.refuse(R.render_forms([form]).encode(), family, "undeclared")

    def test_duplicate_singular_at_every_depth(self):
        for family, doc in self.documents():
            mapper = D.dependencies_to_form if family == "dependencies" else D.capture_to_form
            original = mapper(doc)
            for index, node in enumerate(self.nodes(original)):
                scalar = next(child for child in node[1:] if len(child) == 2 and not isinstance(child[1], list))
                if scalar[0] == "argv":
                    self.fail("fixture singular field no longer first")
                form = copy.deepcopy(original)
                self.nodes(form)[index].append(copy.deepcopy(scalar))
                self.refuse(R.render_forms([form]).encode(), family, "duplicated")

    def test_missing_required_at_every_depth(self):
        for family, doc in self.documents():
            mapper = D.dependencies_to_form if family == "dependencies" else D.capture_to_form
            original = mapper(doc)
            for index in range(len(self.nodes(original))):
                form = copy.deepcopy(original); self.nodes(form)[index].pop(1)
                self.refuse(R.render_forms([form]).encode(), family, "missing required")

    def test_wrong_types_and_arity_at_every_depth(self):
        for family, doc in self.documents():
            mapper = D.dependencies_to_form if family == "dependencies" else D.capture_to_form
            original = mapper(doc)
            for index in range(len(self.nodes(original))):
                for suffix in ([], [7], ["one", "two"]):
                    form = copy.deepcopy(original); node = self.nodes(form)[index]
                    node[1] = [node[1][0], *suffix]
                    self.refuse(R.render_forms([form]).encode(), family, "(arity|type)")

    def test_empty_required_collections(self):
        for family, doc in self.documents():
            for key in (("input",) if family == "dependencies" else ("argv", "input", "observation", "tool")):
                changed = copy.deepcopy(doc); changed[key] = []
                self.refuse(raw(changed, family), family, "min is")

    def test_exact_versions_and_run_kinds(self):
        for family, doc in self.documents():
            for value in ("unknown", doc["format_version"] + "\n", ""):
                changed = copy.deepcopy(doc); changed["format_version"] = value
                self.refuse(raw(changed, family), family, "does not match")
        for value in ("unknown", "baseline\n"):
            doc = capture(); doc["run_kind"] = value
            self.refuse(raw(doc, "capture"), "capture", "does not match")

    def test_exact_digest_tokens(self):
        for family, doc in self.documents():
            locations = [("input", i) for i in range(len(doc["input"]))]
            if family == "capture":
                locations += [("observation", i) for i in range(3)] + [(None, None)]
            for key, index in locations:
                for value in ("a" * 63, "A" * 64, "g" * 64, "a" * 64 + "\n", ""):
                    changed = copy.deepcopy(doc)
                    target = changed if key is None else changed[key][index]
                    target["reference_binary_sha256" if key is None else "sha256"] = value
                    self.refuse(raw(changed, family), family, "does not match")

    def test_nonempty_required_strings(self):
        for family, doc in self.documents():
            mapper = D.dependencies_to_form if family == "dependencies" else D.capture_to_form
            original = mapper(doc)
            for index, node in enumerate(self.nodes(original)):
                for field in node[1:]:
                    if len(field) == 2 and type(field[1]) is str and field[0] not in ("argv", "format_version", "sha256", "reference_binary_sha256", "run_kind", "role"):
                        form = copy.deepcopy(original); target = self.nodes(form)[index]
                        next(item for item in target[1:] if item[0] == field[0])[1] = ""
                        self.refuse(R.render_forms([form]).encode(), family, "min-length")

    def test_path_context_is_required_and_canonical(self):
        for family, doc in self.documents():
            for path in ("", "/outside", "./capture", "a/../b", "a//b", "a\\b", "a:b", "a\x00b", 1):
                with self.assertRaisesRegex(A.ArtifactError, "noncanonical"):
                    parser(family)(raw(doc, family), path=path)

    def test_paths_refuse_noncanonical_forms(self):
        for family, doc in self.documents():
            key = "input" if family == "dependencies" else "observation"
            for path in ("/absolute", "./a", "a/../b", "a//b", "a/", "a\\b", "a:b", "a\n", ".", "a\x7fb"):
                changed = copy.deepcopy(doc); changed[key][0]["path"] = path
                self.refuse(raw(changed, family), family, "noncanonical")

    def test_duplicate_input_ids(self):
        for family, doc in self.documents():
            doc["input"][1]["id"] = doc["input"][0]["id"]
            self.refuse(raw(doc, family), family, "duplicate id")

    def test_duplicate_manifest_paths(self):
        doc = dependencies(); doc["input"][1]["path"] = doc["input"][0]["path"]
        self.refuse(raw(doc, "dependencies"), "dependencies", "duplicate path")

    def test_manifest_64_accepts_65_refuses(self):
        doc = dependencies()
        doc["input"] = [{**doc["input"][0], "id": f"leaf-{i}", "path": f"target/leaf-{i}"} for i in range(64)]
        self.assertEqual(A.parse_dependencies(raw(doc, "dependencies"), path=DEPENDENCIES_PATH), doc)
        doc["input"].append({**doc["input"][0], "id": "leaf-64", "path": "target/leaf-64"})
        self.refuse(raw(doc, "dependencies"), "dependencies", "more than 64")

    def test_manifest_self_and_nested_role_refuse(self):
        doc = dependencies(); doc["input"][0]["path"] = DEPENDENCIES_PATH
        self.refuse(raw(doc, "dependencies"), "dependencies", "self reference")
        doc = dependencies(); doc["input"][0]["role"] = "dependency-manifest"
        self.refuse(raw(doc, "dependencies"), "dependencies", "nested manifest")

    def test_collector_inventory_edge(self):
        doc = capture(); doc["collector_input_id"] = "missing"
        self.refuse(raw(doc, "capture"), "capture", "collector input")

    def test_duplicate_output_and_tool_ids(self):
        for key in ("observation", "tool"):
            doc = capture(); doc[key][1]["id"] = doc[key][0]["id"]
            self.refuse(raw(doc, "capture"), "capture", "duplicate id")

    def test_duplicate_output_paths(self):
        doc = capture(); doc["observation"][1]["path"] = doc["observation"][0]["path"]
        self.refuse(raw(doc, "capture"), "capture", "duplicate path")

    def test_output_roles_are_exactly_three(self):
        doc = capture(); doc["observation"][1]["role"] = "raw-gpr"
        self.refuse(raw(doc, "capture"), "capture", "exactly one")
        doc = capture(); doc["observation"].append({**doc["observation"][0], "id": "extra", "path": "target/extra"})
        self.refuse(raw(doc, "capture"), "capture", "exactly one")
        for role in ("process-receipt", "unknown", "raw-gpr\n"):
            doc = capture(); doc["observation"][0]["role"] = role
            self.refuse(raw(doc, "capture"), "capture", "does not match")

    def test_receipt_cannot_be_its_own_output(self):
        doc = capture(); doc["observation"][0]["path"] = CAPTURE_PATH
        self.refuse(raw(doc, "capture"), "capture", "own output")

    def test_negative_output_sizes(self):
        for index in range(3):
            doc = capture(); doc["observation"][index]["byte_size"] = -1
            self.refuse(raw(doc, "capture"), "capture", "negative")

    def test_output_size_and_exit_types(self):
        for key in ("process_exit", "byte_size"):
            doc = capture(); target = doc if key == "process_exit" else doc["observation"][0]
            target[key] = "0"
            self.refuse(raw(doc, "capture"), "capture", "wrong value type")

    def test_writer_unknown_keys_at_every_depth(self):
        for family, doc in self.documents():
            nodes = [doc, *doc["input"]]
            if family == "capture": nodes += [doc["host"], *doc["observation"], *doc["tool"]]
            encoder = A.encode_dependencies if family == "dependencies" else A.encode_capture
            for index in range(len(nodes)):
                changed = copy.deepcopy(doc); targets = [changed, *changed["input"]]
                if family == "capture": targets += [changed["host"], *changed["observation"], *changed["tool"]]
                targets[index]["qualified"] = True
                with self.assertRaisesRegex(A.ArtifactError, "undeclared"):
                    encoder(changed, path=location(family))

    def test_writer_refuses_lossy_or_wrong_types(self):
        for value in (True, 1.5, None, [], {}):
            doc = capture(); doc["process_exit"] = value
            with self.assertRaises(A.ArtifactError): A.encode_capture(doc, path=CAPTURE_PATH)
        doc = capture(); doc["argv"] = tuple(doc["argv"])
        with self.assertRaisesRegex(A.ArtifactError, "lose or change"):
            A.encode_capture(doc, path=CAPTURE_PATH)


MUTATIONS = {
    "no-facets": None,
    "no-root-count": ('if len(forms) != 1 or forms[0][0] != family:', 'if not forms or forms[0][0] != family:'),
    "no-path": ('if not isinstance(value, str) or not is_canonical_path(value):', 'if False:'),
    "no-manifest-limit": ('if len(inputs) > MANIFEST_INPUTS:', 'if False:'),
    "no-nested-manifest": ('if item["role"] == "dependency-manifest":', 'if False:'),
    "no-byte-bound": ("if not payload or len(payload) > DOCUMENT_BYTES:", "if not payload:"),
    "no-identity": ("if len(set(values)) != len(values):", "if False:"),
    "no-manifest-edges": ('if item["path"] == path:\n            raise ArtifactError("dependencies: self reference")', 'if False:\n            raise ArtifactError("dependencies: self reference")'),
    "no-output-set": ("if len(observations) != 3 or {item[\"role\"] for item in observations} != _OUTPUT_ROLES:", "if False:"),
    "no-collector-edge": ("if doc[\"collector_input_id\"] not in inputs:", "if False:"),
}


def main():
    global A
    cli = argparse.ArgumentParser(description=__doc__)
    mode = cli.add_mutually_exclusive_group()
    mode.add_argument("--emit", choices=("dependencies", "capture"))
    mode.add_argument("--mutation", choices=tuple(MUTATIONS))
    args = cli.parse_args()
    if args.emit:
        doc = dependencies() if args.emit == "dependencies" else capture()
        sys.stdout.buffer.write(raw(doc, args.emit))
        return 0
    if args.mutation == "no-facets":
        original_schema = A._schema

        def without_patterns(family):
            constructs, operators = copy.deepcopy(original_schema(family))
            for construct in constructs.values():
                for field in construct.fields.values():
                    field.pattern = None
            return constructs, operators

        A._schema = without_patterns
    elif args.mutation:
        source = Path(A.__file__).read_text()
        old, new = MUTATIONS[args.mutation]
        if source.count(old) != 1: raise SystemExit("mutation seam drift")
        module = types.ModuleType("matched_gpr_artifacts_mutant")
        module.__file__ = A.__file__
        exec(compile(source.replace(old, new), A.__file__, "exec"), module.__dict__)
        A = module
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ArtifactTests))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

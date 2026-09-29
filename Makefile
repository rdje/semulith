# Makefile — standard commands. `make gate` = the doctrine enforcer; `make check` = Rust.
SHELL := /usr/bin/env bash

.PHONY: help gate check ci fmt clippy test book bench smoke-bench hooks bootstrap update-scaffold

help:
	@echo "make gate            - run the doctrine enforcer (scripts/check_doctrines.sh)"
	@echo "make check           - cargo fmt --check + clippy (deny warnings) + test"
	@echo "make fmt             - cargo fmt --all"
	@echo "make clippy          - cargo clippy --all-targets -- -D warnings"
	@echo "make test            - cargo test --all"
	@echo "make book            - build the mdBook (the project book and every model book)"
	@echo "make ci              - the NAMED full local suite (runs at the pre-push boundary): check + gate + bench + smoke-bench + book"
	@echo "make bench           - build the browser bench's wasm module (scripts/build_bench.sh)"
	@echo "make smoke-bench     - verify the bench engine headlessly (scripts/smoke_bench.js)"
	@echo "make hooks           - install the git hooks (core.hooksPath=.githooks)"
	@echo "make bootstrap       - first-time project bootstrap"
	@echo "make update-scaffold - pull the latest bedrock spine (set URL=<bedrock-repo>)"

gate:
	scripts/check_doctrines.sh

check:
	cargo fmt --all -- --check
	cargo clippy --all-targets --all-features -- -D warnings
	cargo test --all

fmt:
	cargo fmt --all

clippy:
	cargo clippy --all-targets --all-features -- -D warnings

test:
	cargo test --all

book:
	mdbook build docs/book
	@for b in docs/models/*/book.toml; do mdbook build "$$(dirname "$$b")" || exit 1; done

# make ci — the NAMED full local suite (PUSH-DISCIPLINE.2), run by the pre-push hook before
# any push. Membership, named not implied:
#   check        cargo fmt --check + clippy -D warnings + all tests     (CI's rust.yml)
#   gate         every doctrine, incl. the wasm build and all self-tests (CI's doctrines.yml)
#   bench        build the browser bench's wasm module
#   smoke-bench  run the bench engine headlessly over the pinned guests
#   book         build the project book and every model book
# This MATCHES the server-side workflows (check + gate) and consciously EXCEEDS them (bench,
# smoke-bench, book). The live three-way smoke (scripts/run_semulith_smoke.py) is NOT in it:
# it needs the untracked, network-acquired reference binaries under target/refs/ — the same
# not-a-commit-gate standing it already has.
ci: check gate bench smoke-bench book
	@echo "ci: all legs green (check, gate, bench, smoke-bench, book)"

bench:
	scripts/build_bench.sh

smoke-bench:
	node scripts/smoke_bench.js

hooks:
	git config core.hooksPath .githooks
	@echo "git hooks activated (core.hooksPath=.githooks)"

bootstrap:
	scripts/bootstrap.sh

update-scaffold:
	scripts/update_scaffold.sh $(URL)

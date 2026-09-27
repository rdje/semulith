;; sources.sexp — the schema for a pinned-source ledger (sources.sexp).
;;
;; `SOT-FORMAT.4`: the retired sources.toml is one document form. `sha256` is the digest of
;; the artifact as served; the (pattern …) facet keeps it a 64-hex string, and the
;; publication/revision pair is what makes a version string an identity (see the dossier's
;; own warning — a version string without its publication is not an identity).
;; scripts/check_citations.py resolves locators against the artifacts these rows pin.

(schema (id "sources"))

(construct (name sources)
  (field (name publication) (type string) (min-length 1))
  (field (name not_this_publication) (type string) (optional yes))
  (field (name revision) (type string) (min-length 1))
  (field (name base_url) (type string) (min-length 1))
  (field (name retrieved) (type string) (min-length 1))
  (field (name work_dir) (type string) (min-length 1))
  (field (name source) (type form) (head source) (repeat yes) (min 1)))

(construct (name source)
  (field (name id) (type string) (min-length 1))
  (field (name file) (type string) (min-length 1))
  (field (name title) (type string) (min-length 1))
  (field (name chapter_version) (type string) (optional yes))
  (field (name sha256) (type string) (pattern "^[0-9a-f]{64}$"))
  (field (name bytes) (type integer))
  (field (name http_status) (type integer))
  (field (name supplies) (type string) (min-length 1)))

;; state.sexp — the schema for an architectural-state document (state.sexp).
;;
;; `SOT-FORMAT.4`: the retired state.json is one document form. Identifiers stay strings;
;; `authority` is a symbol, and `software-convention` is legal ONLY here — for the ABI roles
;; the ISA chapter itself names (PROFILE-CONSISTENCY carries the same rule; docs/
;; INFORMATION_CATALOG.md §6 names the mistake). Booleans are the symbols true/false. The
;; empty hidden_state list is absence (`.3` rule): the census beside it is what earns the
;; universal claim, and PROFILE-CONSISTENCY gates that.

(schema (id "state"))

(construct (name state)
  (field (name profile_id) (type string) (min-length 1))
  (field (name xlen) (type integer))
  (field (name note) (type string) (min-length 1))
  (field (name integer_registers) (type form) (head integer_registers))
  (field (name special_registers) (type form) (head register) (repeat yes))
  (field (name hidden_state_census) (type form) (head hidden_state_census)))

(construct (name integer_registers)
  (field (name count) (type integer))
  (field (name width_bits) (type integer))
  (field (name ids) (type string) (min-length 1))
  (field (name authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory))
  (field (name source) (type string) (min-length 1))
  (field (name x0) (type form) (head x0))
  (field (name named_by_the_isa_chapter) (type form) (head named-register)
         (repeat yes) (min 1))
  (field (name reset) (type form) (head reset)))

(construct (name x0)
  (field (name hardwired_zero) (type symbol) (values true) (values false))
  (field (name authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory))
  (field (name source) (type string) (min-length 1))
  (field (name statement) (type string) (min-length 1)))

(construct (name named-register)
  (field (name reg) (type string) (min-length 1))
  (field (name role) (type string) (min-length 1))
  (field (name authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory)
         (values software-convention))
  (field (name source) (type string) (min-length 1)))

(construct (name reset)
  (field (name value) (type string) (min-length 1))
  (field (name authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory))
  (field (name source) (type string) (min-length 1))
  (field (name statement) (type string) (min-length 1)))

(construct (name register)
  (field (name id) (type string) (min-length 1))
  (field (name width_bits) (type integer))
  (field (name holds) (type string) (min-length 1))
  (field (name authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory))
  (field (name source) (type string) (min-length 1))
  (field (name reset) (type string) (min-length 1))
  (field (name reset_authority) (type symbol)
         (values architecture) (values execution-environment) (values laboratory)))

(construct (name hidden_state_census)
  (field (name question) (type string) (min-length 1))
  (field (name answer) (type string) (min-length 1))
  (field (name candidates) (type form) (head checked) (repeat yes) (min 1))
  (field (name consequence) (type string) (min-length 1)))

(construct (name checked)
  (field (name candidate) (type string) (min-length 1))
  (field (name present) (type symbol) (values true) (values false))
  (field (name why) (type string) (min-length 1)))

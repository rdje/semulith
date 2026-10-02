;; GENERATED — do not edit (OWN-03). Regenerate with `python3 scripts/gen_board.py`; drift between this document and the
;; canonical board definition is refused by the BOARD-GEN doctrine (scripts/check_board_gen.sh).
;; Canonical input: profiles/netboard-lab-v0/board.sexp (sha256 93b087cb65842cd43ce63e24853f4a7c9778a9278d3a8d6458a606f1a6122333)
;; Generator: scripts/gen_board.py (sha256 887649166b6c832f6d7d3a552fe6cba85f00dfad2a1acc1b140ccaabd58c671a)

(hardware
  (board "netboard-lab-v0")
  (version "0")
  (processor (unit "rv64i-lab-v0") (version "0") (contract "rv64i-lab-env-v0") (contract-version "0"))
  (region (name "ram0") (base "0x8000_0000") (size "0x8000_0000") (end "0x1_0000_0000") (kind ram) (executable true))
  (region (name "uart0") (base "0x1001_0000") (size "0x1000") (end "0x1001_1000") (kind mmio) (executable false) (device "uart0"))
  (region (name "eth0") (base "0x1002_0000") (size "0x100") (end "0x1002_0100") (kind mmio) (executable false) (device "eth0"))
  (wiring (device "uart0") (unit "sifive-uart-lab-v0") (kind sifive-uart) (region "uart0") (access-widths 32) (interrupt unconnected) (backend-rx recorded-input) (backend-tx host-console))
  (wiring (device "eth0") (unit "lan9118-lab-v0") (kind lan9118) (region "eth0") (access-widths 16) (access-widths 32) (interrupt unconnected) (backend-rx recorded-trace-replay) (backend-tx recording-sink))
  (serial-console (device "uart0"))
  (reset (kinds cold))
  (absence (element timers) (satisfies "OB-ENV-VIRTUAL-TIME"))
  (absence (element interrupt-controller) (satisfies "OB-ENV-EVENT-DELIVERY"))
)

auipc x1, 0                    #: the base for the handler: {new}. | RVI-RV64I §3.1.2.1
addi x1, x1, 16                #: the handler, a few rows on: {new}. | RVI-RV32I §1.1.4
csrrw x0, mtvec, x1            #: mtvec = the handler; no GPR written. | RVP-MACHINE §2.1.1.7
jal x0, 20                     #: past the handler; x0 discards the link. | RVI-RV32I §1.1.5.1
csrrs x30, mcause, x0          #: the handler reads mcause: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.15
csrrs x29, mtval, x0           #: and mtval: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.16
csrrs x28, mepc, x0            #: and mepc, the instruction's own address: {new}. | RVI-ZICSR §5.1.1; RVP-MACHINE §2.1.1.14
jalr x0, x27, 0                #: on, to where x27 says, still in M. | RVI-RV32I §1.1.5.1
addi x10, x0, 1                #: raw material for the region base. | RVI-RV32I §1.1.4
slli x10, x10, 31              #: 0x80000000: {new}. | RVI-RV64I §3.1.2.1
lui x1, 7                      #: 0x7000: {new}. | RVI-RV64I §3.1.2.1
add x1, x1, x10                #: the data cell, on a page of its own, past this program: {new}. | RVI-RV32I §1.1.4
addi x5, x0, 41                #: forty-one: {new}. | RVI-RV32I §1.1.4
sd x5, 0, x1                   #: the hart stores it. | RVI-RV64I §3.1.3
addi x6, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x6, x1, 0                   #: and its own later load sees it: {new}. | RVI-RVWMO §17.1; RVI-RV64I §3.1.3 (boundary: a hart sees its own store)
addi x7, x0, 1                 #: one: {new}. | RVI-RV32I §1.1.4
amoadd.d x8, x7, (x1)          #: no annotation: rd takes the old value: {new}. | RVI-A §12.1 (boundary: the annotations change nothing a hart sees)
amoadd.d.aq x8, x7, (x1)       #: acquire, and the same result at one hart: {new}. | RVI-A §12.1
amoadd.d.rl x8, x7, (x1)       #: release, and the same result at one hart: {new}. | RVI-A §12.1
amoadd.d.aqrl x8, x7, (x1)     #: acquire and release, and the same result at one hart: {new}. | RVI-A §12.1
addi x9, x0, 77                #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x9, x1, 0                   #: memory took all four: {new}. | RVI-RV64I §3.1.3
lr.d.aq x10, (x1)              #: an acquire LR: {new}. | RVI-A §12.1
addi x11, x0, 50               #: fifty: {new}. | RVI-RV32I §1.1.4
addi x12, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
sc.d.rl x12, x11, (x1)         #: a release SC pairs with it: {new}. | RVI-A §12.1
fence 0, 15, 15, x0, x0        #: FENCE IORW, IORW: it orders against other agents, and there are none. | RVI-RV32I §1.1.7
addi x13, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x13, x1, 0                  #: the value is still the SC's: {new}. | RVI-RV64I §3.1.3
fence 0, 3, 3, x0, x0          #: FENCE RW, RW: it orders against other agents, and there are none. | RVI-RV32I §1.1.7
addi x13, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x13, x1, 0                  #: the value is still the SC's: {new}. | RVI-RV64I §3.1.3
fence 8, 3, 3, x0, x0          #: FENCE.TSO: it orders against other agents, and there are none. | RVI-RV32I §1.1.7
addi x13, x0, 77               #: a sentinel, so the next read changes it. | RVI-RV32I §1.1.4
ld x13, x1, 0                  #: the value is still the SC's: {new}. | RVI-RV64I §3.1.3
c.nop                          #: the end of the program. | RVI-C §27.1.8

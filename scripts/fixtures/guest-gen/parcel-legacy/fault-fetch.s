# fault-fetch.s — the P2-SCALAR.3 fault guest: an instruction access fault on a jump
# TARGET, reported ON THE TARGET (D-FETCH-FAULT-REPORT — the opposite reporting point
# from misalignment).
#
# 0x40000000 is outside sail-riscv's MainMemory region (0x80000000 + 2 GiB), outside
# spike's DRAM, and no device on either — so all three models raise the same fault and
# the comparison runs cross-model. ⭐ THE FETCH SUPPLIED NO WORD: the step at the target
# is the vocabulary's word-less step (P2-SCALAR.3's extension), never a fabricated
# encoding. The laboratory run stops with Stop::FetchFault.

      lui   x1, 0x40000        # x1 = 0x40000000: outside every region either platform declares
      jalr  x0, x1, 0          # transfer to 0x40000000 (link discarded into x0)
      # step 2 is the fetch at 0x40000000 itself: it faults — trap (0x01, 0x40000000),
      # no word fetched, reported ON THE TARGET

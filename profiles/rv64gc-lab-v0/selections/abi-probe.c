/* REQ-D-ABI's fixture. A double beside an integer: under the hardware floating-point convention with ABI_FLEN=64 the double
   arrives and returns in fa0, so nothing moves. Under lp64 and lp64f it arrives in a1 and returns in a0. psABI 2.4-2.5. */
double abi_probe(long unused, double value) {
    (void)unused;
    return value;
}

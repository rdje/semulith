# My survey found plenty — how do I know it found everything?

**A non-empty result is not a complete one.** A zero at least prompts the question "is my instrument
blind?" ([[zero-hits-absence-or-blindness]]). Twenty-two results prompt nothing at all: the output
looks like work, reads like a census, and gets committed as one. The failure mode is quieter than
the zero, and it is the more common of the two.

## What happened

Surveying a 3,684-file documentation corpus for processor manuals, I enumerated by **guessing
vendor directory names**:

```
$ find zilog wdc openrisc openpower sparc -name '*.pdf'     # "the small-CPU vendors"
$ find ti -name '*.pdf'                                      # "the DSPs"
$ find arm amd intel -name '*.pdf'                           # "the big ISAs"
```

Twenty-two materials, catalogued with digests, page counts, licences and prose — a thorough-looking
record built on a list of directory names I had produced from memory.

The re-survey swept by **path shape** instead:

```
$ find . -name '*.pdf' | grep -iE '/(isa|cpu|architecture|processors|m68k|z80|65c02|dsp|mcu)/'
```

Eight more documents, including an entire architecture: **M68000**. It is filed under `nxp/m68k/`,
because NXP inherited Motorola's semiconductor business through Freescale. My sweep would have had
to know thirty years of corporate history to look there. Also missed: three ESP32 SoC manuals and
two Raspberry Pi datasheets — every board-class document in the corpus, which is to say the entire
material base for one of this project's own milestones.

## Why the first survey felt complete

Each probe returned results, and the results were *relevant*. Nothing signalled absence, because
the instrument was never asked a question it could fail. I checked `zilog/` and found a Z80 —
confirmation. I never asked "which directories did I not name?", which is the only question whose
answer contains the miss.

⭐ And the name I invented was the giveaway I ignored: I searched for a `motorola/` directory. It
does not exist. A probe naming something that is not there should be a signal, and I read it as
nothing.

## How to tell the two apart

| Survey by | Records | Fails when |
| --- | --- | --- |
| a list of names you wrote | **your expectations** about the corpus | the corpus is organised by someone else's history |
| a property of the thing | **the corpus** | the property is wrong — which is visible and arguable |

So sweep by a property, and then prove the sweep is exhaustive against a total:

```
$ find . -name '*.pdf' | wc -l                         # 196   the denominator
$ <my classifier> | wc -l                              #  37   classified
$ <everything my classifier did NOT match>             # READ THIS LIST
```

That last line is the whole technique. The residue is short enough to eyeball, and it is where
`nxp/m68k/` was hiding. A classifier you never check the complement of is a filter you are trusting
on faith.

## The rule

> Enumerate by a property of the thing, never by a list of names you wrote from memory — and read
> what your enumeration excluded before you believe it.

And when a survey is wrong, **say which method was wrong, in the record**. The catalogue now carries
a `derivation` field naming the sweep command, so the next reader can judge the method rather than
trusting the result. A census with no stated method cannot be checked; it can only be believed.

Related: [[zero-hits-absence-or-blindness]], [[a-version-string-is-not-an-identity]],
[[census-instrument-signature-gap]].

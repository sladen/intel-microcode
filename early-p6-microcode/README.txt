Early P6/Pentium Pro microcode updates;

See the Intel Pentium Pro Errata/Specification tables for the steppings;
(Intel 242689-034)
http://www.citi.umich.edu/projects/linux-scalability/pdf/24268934.pdf

('s' is for shrink.)

  0x611 /  B0 mask stepping (150 MHz)
  0x612 /  C0 mask stepping (150 MHz)

  0x616 / sA0 mask stepping (200 MHz) die-shrink/process change; equivalent to C0
  0x617 / sA1 mask stepping (200 MHz) die-shrink/process change; similiar to C0

  0x619 / sB1 mask stepping (200 MHz) die-shrink/process change; new mask/ROM


For first generation P6 (PPro) the public microcode update stepping
share the initial letter as the on-die mask, plus a number;

 * B-stepping had a lot of microcode revisions, so the public microcodes
   get up to 'b26' + 'b27'.
 * C-stepping (C0, sA0, sA1) got up to 'c5' and then 'c6' in public
 * D-stepping (sB1, aka D0) was mostly done, and only needed 'd1' and 'd2'


Half of these early microcodes have complete junk in the 48-byte
header; wrong endianness, wrong year or century; manual hex update in
the wrong byte position or moving everything off-by-one.
Dates are guessed/corrected based on likely timeline.

The processor itself never sees the 48-byte header, and so getting it
right was probably not important... P6 microcode 'updates' were
originally for interactively debugging the processor; so designed to
be semi-auto-generated + re-ciphered and fed automatically straight
into the CPU.

'b26' microcode is missing the psuedo-random noise stream at the end,
and just has zero padding!  It may also be 'bswapped'; does not
appear possible know which endianness is actually going to be
correct without successfully deciphering it; which requires either
that exact chip ... or knowledge of the algorithm + a good guess
at the keys!

For the latter; the {612,616,617}*{c5,c6} set are likely to be most
useful as the plaintext contents are anticipated to be
extremely-similar (virtually identical).

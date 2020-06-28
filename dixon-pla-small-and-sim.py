#!/usr/bin/env python

import operator

def n(number, bits = 104):
    return ((1<<bits)-1)^number

def main(instruction = None): 

    lines = open('dixon-pla-small-and-only.txt', 'r').readlines()
    assert len(lines) == 48
    assert len(lines[0].rstrip()) == 102

    binary_lines = [int(l.rstrip(), 2) for l in lines]

    # small decoder: 3 bytes => 24 bits
    xchg_ecx_eax = 0x910000
    if instruction is None:
        instruction = xchg_ecx_eax

    # is the PLA actually backwards?!
    flipped = int('{:024b}'.format(instruction)[::-1], 2)
    #flipped = instruction

    # each bit doubled up (if true, if false) => 48 bits
    x86 = flipped | 0x1000000
    x86n = x86 ^ 0xffffff | 0x1000000

    # double each bit, flipping the duplicate 
    z = zip(bin(x86)[3:], bin(x86n)[3:])

    # + recombine
    pla_input = int(''.join([x for y in z for x in y]),2)

    # pretty print for debugging
    #print hex(pla_input)
    #print ' '.join(bin(xchg_ecx_eax)[2:])
    #print bin(pla_input)[2:]

    pla_and_output = (1 << 104) - 1
    pla_and_output = 0
    #print bin(output)

    outputs = []

    active = 0x1 << (48 - 1)
    #print hex(pla_input)
    for l in binary_lines:
        #print hex(active), hex(pla_input), hex(active & pla_input), bool(active & pla_input)
        if (active & pla_input):
            #print 'active'
            outputs.append(l)
        else:
            #outputs.append(0)
            pass
            
        #print hex(pla_and_output)
        #print bin(l)
        active = active >> 1
    #print len(outputs)
    meh = n(0)
    for o in outputs:
        #print "{0:#0{1}x}".format(o, 28)
        # "AND" array is actually NOR...
        # CHECKME...
        meh = n(meh) | n(o)
    
    print "{0:#0{1}x}".format(instruction, 6+2), 'x86_instruction', '=>',
    print "{0:#0{1}x}".format(n(meh), 28), 'AND output'


if __name__=='__main__':
    for ins in (0x0f0b00, 0x0fff00, 0x0fffff, 0x66f0b0, 0x67f0b0, #Undefined Op-codes
                0x909090, 0x669000, 0x0f1f00, 0x0f1f40, 0x660f1f, 0x0f1f80, 0x0f1f84, 0x660f1f, 0x666690, # Nops
                0x900000, 0x909000, 0x909090, # Repeated Nops, should be the same
                0x404040, 0x414141, 0x424242, 0x434343, 0x444444, # Inc/Rex single byte
                0x900000, 0x910000, 0x920000, 0x930000, 0x940000, 0x950000, 0x960000, 0x970000, 0x971234, # xchg
                0xc8c8c8, 0xc80000, # enter
                0xc30000, 0xc3c3c3, # ret
                0x616161, # pushad
                0xb80500, 0xb80600, 0xb8ff00, # mov
                0x48b812, 0xb81200, 0x66b812, 0xb01200, # mov const => rax, eax, ax, al
                0x31c100, 0x33c800, # two forms of xor eax, ecx
                0xb80500, 0xb90500, 0xba0500, 0xbb0500, # mov eax, ecx, edx, ebx
                0x500000, 0x510000, 0x520000, 0x530000, # push eax ecx, edx, ebx
                0x7f0100, # jg @+01
                0xb81234, 0xb91234, 0xba1234, 0xbb1234, 0xbc1234, 0xbd1234, 0xbe1234, 0xbf1234, # mov const => reg
                0x890000, 0x890100, 0x890200, 0x890300, 0x890424, 0x894500, 0x890600, # mov reg => mem
                0x03c000, 0x03c100, # add reg, reg
                0xf7d000, 0xf7d100, # not reg
                0xf7d800, 0xf7d900, # neg reg
                0x66f7d8, 0x67f7d8, # prefix neg reg
                ):
        main(ins)

#!/usr/bin/env python

import operator

# not, using xor to stay postive avoid Python negativity
def n(number, bits = 104):
    return ((1<<bits)-1)^number

# fixed length bin(), without needing to strip '0b' prefix
def binstring(number, bits = 24):
    return ('{:0' + str(bits) + 'b}').format(number)

# iterable bitmask 1, 2, 4, 8, ...
def bitmask(start = 0x1, bits = None, shift = 1):
    i = start
    while bits is None or bits > 0:
        yield i
        i = i << shift
        if bits is not None:
            bits = bits - 1

def main(instruction = None): 

    lines = open('dixon-pla-small-and-only.txt', 'r').readlines()
    assert len(lines) == 48
    assert len(lines[0].rstrip()) == 102

    binary_lines = [int(l.rstrip(), 2) for l in lines]

    # small decoder: 3 bytes => 24 bits
    if instruction is None:
        # fallback example
        xchg_ecx_eax = 0x910000
        instruction = xchg_ecx_eax

    and_thresholds = [0] * 104
    and_buckets = [0] * 104

    # how many bits are required (AND) in column?
    for l in binary_lines:
        for j, mask in zip(xrange(104), bitmask(bits=104)):
            if l & mask:
                and_thresholds[j] += 1

    #print `and_thresholds`
        
    # how many bits were activated (AND) in each column?
    
    for i, mask in zip(xrange(0,24*2,2), bitmask(bits=24)):
        match = bool(instruction & mask)
        #print i, hex(mask), match
        line1 = binary_lines[i+0]
        line2 = binary_lines[i+1]
        for output, bit in zip(xrange(104), bitmask(bits=104)):
            if bool(line1 & bit) and match:
                and_buckets[output] += 1
            if bool(line2 & bit) and not match:
                and_buckets[output] += 1

    result = 0
    for i, mask in zip(xrange(104), bitmask(bits=104)):
        if and_buckets[i] >= (and_thresholds[i]-4):
            result |= mask

    print and_buckets

    #print `and_buckets`
    print "{0:#0{1}x}".format(instruction, 6+2), 'x86_instruction', '=>',
    print "{0:#0{1}x}".format(result, 28), '(N)AND output'
    return

    # each bit doubled up (if true, if false) => 48 bits
    not_x86 = n(instruction,24)
    x86 = instruction

    # double each bit, !bit first
    z = zip(binstring(not_x86), binstring(x86))

    # + interlace bits + convert back from binary-string to binary-number
    pla_input = int(''.join([x for y in z for x in y]),2)

    line_outputs = []
    for l, mask in zip(binary_lines, bitmask()):
        #print hex(active), hex(pla_input), hex(active & pla_input), bool(active & pla_input)
        if (mask & pla_input):
            line_outputs.append(l)
        else:
            pass

    intermediate = 0
    for wire in line_outputs:
        # "AND" array is actually NAND (or is it NOR)...
        # CHECKME...
        a = intermediate
        b = wire
        intermediate = n(a) & b
    
    valid = bool(intermediate & 0x1)
    prefix = bool(intermediate & 0x2)
    print "{0:#0{1}x}".format(instruction, 6+2), 'x86_instruction', '=>',
    print "{0:#0{1}x}".format(intermediate, 28), 'AND output',
    if valid: print '<== valid?',
    if prefix: print '<== prefix?',
    print

if __name__!='__main__':
    main(0xcccccc)

if __name__=='__main__':
    for x86 in (0xcc0000, 0xcccc00, 0xcccccc, # Debug interupt
                0x330000, 0x333300, 0x333333, # Debug interupt
                0x0f0b00, 0x0fff00, 0x0fffff, 0x66f0b0, 0x67f0b0, #Undefined Op-codes
                0x909090, 0x669000, 0x0f1f00, 0x0f1f40, 0x660f1f, 0x0f1f80, 0x0f1f84, 0x660f1f, 0x666690, # Nops
                0x900000, 0x909000, 0x909090, # Repeated Nops, should be the same
                0x404040, 0x414141, 0x424242, 0x434343, 0x444444, # Inc/Rex single byte
                0x900000, 0x910000, 0x920000, 0x930000, 0x940000, 0x950000, 0x960000, 0x970000, 0x971234, # xchg
                0xc80000, 0xc80001, # enter
                0xc30000, 0xc3c3c3, # ret; ret + padding
                0x600000, 0x606000, 0x606060, # pushad + padding
                0x610000, 0x616100, 0x616161, 0x666100, # popad
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
        main(x86)

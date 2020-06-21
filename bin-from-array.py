#!/usr/bin/env python

def main():
    raw = ''
    found = 0
    lines = open('glm-ucode/ms_rom.txt', 'r').readlines()[1:]
    for l in lines:
        fields = l.strip().split(' ')
        #print `fields`
        offset, empty, hop1, hop2, hop3, nulls = fields
        op1 = hop1.decode("hex")
        op2 = hop1.decode("hex")
        op3 = hop1.decode("hex")
        raw += op1
        raw += op2
        raw += op3
        found += 1
        if found == 1:
            print 'length:', len(raw), 'bytes;', len(8*raw), 'bits'
        

    open('microcode.bin', 'wb').write(raw)

if __name__=='__main__':
    main()

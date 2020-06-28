#!/usr/bin/env python

# Peter Bosch screenshot of working with pladecode:
# https://github.com/peterbjornx/pladecode/blob/master/readme.md
# links to:
# https://camo.githubusercontent.com/2052888407ba5d842a0fe9309ccf85c5a1544737/68747470733a2f2f686f6d652e737472772e6c656964656e756e69762e6e6c2f7e70626f7363682f706c616465635f78346c5f616e642e706e67
# image get downloaded as "6874747*6e67.png"

import glob
import PIL.Image

# xrange for floating point stepping
def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step

def main():
    screenshot = glob.glob('6874*6e67.png')[0]
    image = PIL.Image.open(screenshot)
    assert image.size == (3840, 2132)

    # screenshot, of a screenshot, of a screenshot
    # pladecode preview (fixed-width text area) within screenshot
    left, top = 1058, 1101
    width, height = 1388, 660
    textarea = image.crop((left, top, left+width, top+height))
    assert textarea.size == (width, height)

    # approximate size of text cells within text area
    # found of hand-measuring .. looks like Ubuntu Mono ;-)
    cell_width, cell_height = 132/10., 130/10.
    #print [int(d/c) for d,c in zip(textarea.size, (cell_width, cell_height))]

    # should be 4 ignored + 102*2 useful;
    # and  2 ignored + 48 useful
    cell_width = textarea.size[0] / (4. + 102 * 2 + 2)
    cell_height = textarea.size[1] / (2. + 48 + 1)
    #print cell_width, cell_height

    # might be slightly off because of integer; but we only care
    # about whether a cell is empty (' '==0), or has a character ('1')
    # in the horizontal direction, cells area double spaced
    rows = []
    for row in frange(0, textarea.size[1] - 4, cell_height):
        line = ''
        for column in frange(0, textarea.size[0], cell_width):
            tile = textarea.crop([int(x + 0.5) for x in (column, row, column + cell_width, row+cell_height )])
            # scan it in the same way as a multiple choice school exam;
            # counting the number of colours: if there's one one colour,
            # then the cell is empty
            hit = len(tile.getcolors()) != 1
            line += ('01'[hit])
        # skip noise at start + end
        useful = line[4:-3]
        # because of monospace every other cell is blank
        really_useful = useful[1::2]
        assert len(really_useful) == 102

        rows.append(really_useful)

    # first couple of rows are header, last is empty
    content = rows[2:-1]
    assert len(content) == 48
    assert len(content[0]) == 102

    # ensure we get a final newline too
    s = '\n'.join(content + [''])

    # save it somewhere
    file('dixon-pla-small-and-only.txt','w').write(s)


    # for convenience, save it in the other orientation too
    flipped = [''.join(a) for a in zip(*reversed(content))]
    assert len(flipped) == 102
    assert len(flipped[0]) == 48

    # ensure we get a final newline too
    t = '\n'.join(flipped + [''])

    # save it somewhere
    file('dixon-pla-small-and-flipped.txt', 'w').write(t)


if __name__=="__main__":
    main()

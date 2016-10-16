# Oh Sheet!

A small CSV editor with vim controls.

## Installation
1. Download the source.
2. Run `sudo python setup.py install`
3. Run the program anywhere using `ohsheet [filename]`

## Usage
Use vim keys (`h`, `j`, `k`, `l`) for movement.

Press `g` to go to a cell by its code.

Press `i` to edit a cell or `r` to replace its contents.

When editing, you can use arrow keys to move the cursor withing the cell's text.

To use formulas, begin the cell with `=` and write expressions with no whitespace. Cell references are case-insensitive.

Press `Enter` to finish editing.

Press `w` to save and `q` to quit.


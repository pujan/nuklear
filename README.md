# What is this?

This project is clone a game sokoban (sobokan).

Writing in Python 3 and curses library (module nnuklear.py).

# Create a board

Elements of witch the board consists:

* \# - wall
* o - container
* . - destroyer
* & - player (robot, bulldozer, etc. :))
*   (space) - empty area

Start to level is word `level` and next opening square bracket. Ending square bracket is close level. Word `begin`
opening structure level. Between opening brackets and the word `begin` are optional options:

* `number` - level number
* `author` - level author
* `title` - level title

For example:

```
; this is a comment
level [
; before and after `=` spaces are required
title = "anything"
author = "Łukasz A. Pelc"
number = 1
begin
######
#& o.#
######
]
```

# TODO

* write in pygame (gnuklear.py)

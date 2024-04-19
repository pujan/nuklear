# What is this?

This project is clone a game sokoban (sobokan).

Writing in Python 3 and curses library (module nnuklear.py).

# Create Virtual Env

## VirtalenvWrapper

```sh
mkvirtualenv -a $(pwd) -i flit nuklear
```

## Venv

```sh
python3 -m venv venv
source venv/bin/activate
pip install flit
```

# Instalation

```sh
flit install --deps production --only-deps
```

When Python throws excepion: `ModuleNotFoundError: No module named 'i18n'`:

```sh
pip install python-i18n
```

# Create a board (level)

Elements of witch the board consists:

* \# - wall
* o - container
* . - destroyer
* & - player (robot, bulldozer, etc. :))
*   (space) - empty area

Begin the level with a word `level` and then open the square bracket. End the level follows the closing square bracket. The word `begin` opening structure the level. Optional options can be placed between the opening square bracket and the
word `begin`:

* `number` - level number
* `author` - level author
* `title` - level title

For example:

```
; this is a comment
level [
; spaces are required before and after sign `=`
title = "anything"
author = "Łukasz A. Pelc"
number = 1
begin
######
#& o.#
######

level [
begin
###
#.#
#o#
# #
#&#
###
]
```

# Keybindings

* `arrows` - moving the player
* `r` - reload the board
* `q` - quit

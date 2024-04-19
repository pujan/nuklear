# -*- coding: utf-8 -*-

import curses
from typing import Any

# game modules
import nuklear.engine as engine
import nuklear.lang as lang
from nuklear.parser import Level


t = lang.i18n.t


def winboard(parent: Any, pair: int, win_status_height: int = 3) -> Any:
    y = int(((parent.getmaxyx()[0]) - engine.MAX_Y) / 2) - win_status_height
    x = int((parent.getmaxyx()[1] - engine.MAX_X + 2) / 2)

    if y < 0:
        y = 0

    win = curses.newwin(engine.MAX_Y + 2, engine.MAX_X + 2, y, x)
    win.bkgd(' ', curses.color_pair(pair))
    win.box()

    return win


def winstatus(parent: Any, pair: int) -> Any:
    maxy, maxx = parent.getmaxyx()
    y = maxy - 3
    x = 0
    win = curses.newwin(3, maxx, y, x)
    win.bkgd(' ', curses.color_pair(pair))
    win.box()

    return win


def question(parent, pair: int, string: str) -> bool:
    maxy, maxx = parent.getmaxyx()
    w = len(string) + 4
    h = 3
    y = int((maxy - h) / 2)
    x = int((maxx - w) / 2)
    win = parent.derwin(h, w, y, x)
    win.bkgd(' ', curses.color_pair(pair))
    win.box()
    win.addstr(1, 2, string)
    win.refresh()
    answer = None

    while True:
        key = win.getkey()

        if key in (t('nnuklear.yes_lower'), t('nnuklear.yes_upper')):
            answer = True
        elif key in (t('nnuklear.no_lower'), t('nnuklear.no_upper')):
            answer = False

        if answer is not None:
            break

    win.clear()

    return answer


def winending(parent: Any, pair: int) -> None:
    maxy, maxx = parent.getmaxyx()
    msg = t('nnuklear.end_game')
    info = t('nnuklear.exit_key')
    w = max([len(msg), len(info)]) + 4  # frame + space on left and on right - 2+2=4 :)
    h = 4
    y = int((maxy - h) / 2)
    x = int((maxx - w) / 2)
    win = parent.subwin(h, w, y, x)
    win.bkgd(' ', curses.color_pair(pair))
    win.box()
    msg_x = int((w - len(msg)) / 2)
    info_x = int((w - len(info)) / 2)
    win.addstr(1, msg_x, msg)
    win.addstr(2, info_x, info)
    win.refresh()

    while True:
        if win.getkey() == ' ':
            break


def update_status(win: Any, lvl_number: int, moves: int, title: str = '', author: str = '') -> None:
    _, maxx = win.getmaxyx()
    y = 1
    win.addstr(y, 2, '| ' + t('nnuklear.level') + f': {lvl_number:3d}')
    win.addstr(y, 14, f'| {title:^24}')
    x = maxx - 14
    win.addstr(y, x, '| ' + t('nnuklear.moves') + f': {moves:3d}')
    win.refresh()


def update_board(win: Any, lvl: Level) -> None:
    for y in range(engine.MAX_Y):
        for x in range(engine.MAX_X):
            elem = lvl.board.get(x, y)
            wx = x + 1
            wy = y + 1

            if elem == engine.Object.EMPTY:
                win.addch(wy, wx, ' ')
            elif elem == engine.Object.WALL:
                win.addch(wy, wx, '#')
            elif elem == engine.Object.CONTAINER:
                win.addch(wy, wx, 'o')
            elif elem == engine.Object.DESTROYER:
                win.addch(wy, wx, '.')
            elif elem == engine.Object.PLAYER:
                win.addch(wy, wx, '&')

    win.refresh()


def main(stdscr: Any) -> None:
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    wboard = wstaus = None

    def drawwins():
        stdscr.clear()
        stdscr.refresh()
        wboard = winboard(stdscr, 1)
        wstatus = winstatus(stdscr, 1)
        return wboard, wstatus

    wboard, wstatus = drawwins()
    wboard.refresh()
    wstatus.refresh()

    e = engine.Engine(pln_file='nuklear.pln')
    e.parsefile()
    e.start()

    def update():
        update_board(wboard, e.current_level)
        update_status(wstatus, e.current_level.number, e.moves, e.current_level.title, e.current_level.author)

    update()

    while True:
        if e.is_end():
            if e.is_game_over():
                winending(stdscr, 2)
                break

            if not e.next_level():
                continue

            e.start()
            update()

        key = stdscr.getkey()

        if key == 'KEY_UP':
            ret = e.player_move_up()
            update()
        elif key == 'KEY_DOWN':
            ret = e.player_move_down()
            update()
        elif key == 'KEY_LEFT':
            ret = e.player_move_left()
            update()
        elif key == 'KEY_RIGHT':
            ret = e.player_move_right()
            update()
        elif key == 'KEY_RESIZE':
            wboard, wstatus = drawwins()
            update()
        elif key == 'r':
            e.start()
            update()
        elif key == 'q':
            if question(stdscr, 2, t('nnuklear.exit_info')):
                break
            else:
                wboard, wstatus = drawwins()
                update()


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass

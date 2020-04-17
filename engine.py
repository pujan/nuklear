# -*- coding: utf-8 -*-
import copy
import gettext

gettext.bindtextdomain('nuklear', 'locale')
gettext.textdomain('nuklear')
_ = gettext.gettext

from parser import *

max_size = Size(MAX_X, MAX_Y)

CONFIG = {
    'player_step': 1,
    # new options
    'max_x': 40,
    'max_y': 20,
}


class Engine:
    def __init__(self, pln_file, size=max_size):
        self.size = size
        self.filename = pln_file
        self.board = None
        self.player = None
        self.levels = []
        self.current_level = None
        self.config = CONFIG.copy()
        self.moves = 0
        # index number of list self.levels
        self.current_number_level = 0

    def parsefile(self):
        parser = Parser(self.filename)
        self.levels = parser.parse()
        i = 1

        for level in self.levels:
            if level.number is None:
                level.number = i
                i += 1
            else:
                level.number = int(level.number)
                if i == level.number:
                    i += 1

        self.levels = sorted(self.levels, key=lambda x: x.number)

    def configuration(self, **options):
        invalid = [x for x in options if x not in CONFIG]

        if invalid:
            raise Exception(_('Error options') + ' ' + ', '.join(invalid))

        self.config.update(options)

    def start(self):
        if self.current_number_level >= len(self.levels):
            raise Exception(_(f'Level number error') + f': {number_level}')

        self.current_level = copy.deepcopy(self.levels[self.current_number_level])
        self.board = self.current_level.board
        player_x, player_y = self.board.search_player()
        self.player = Player(player_x, player_y)
        self.moves = 0

    def next_level(self):
        self.current_number_level += 1
        self.start()

    def _player_move(self, direction):
        # ustalamy nowa pozycje gracza
        x, y = self.player.move(direction, self.config['player_step'])

        # pobieramy co znajduje sie na nowej pozycji
        elem = self.board.get(self.player.x, self.player.y)

        if elem in (Object.WALL, Object.DESTROYER):
            # cofamy gracza
            self.player.set_position(x, y)
            return False
        elif elem == Object.CONTAINER:
            # przesuwamy pojemnik, jezeli to mozliwe
            # spawdzamy co za pojemnikiem
            tmpx, tmpy = self.player_next_position(direction)
            tmp_elem = self.board.get(tmpx, tmpy)

            if tmp_elem in (Object.WALL, Object.CONTAINER):
                self.player.set_position(x, y)
                return False
            elif tmp_elem in (Object.EMPTY, Object.DESTROYER):
                # przesuwamy pojemnik
                if tmp_elem == Object.DESTROYER:
                    self.board.set(tmpx, tmpy, Object.EMPTY)


                    self.board.decrement_cointainers()
                else:
                    self.board.set(tmpx, tmpy, Object.CONTAINER)

                self.board.set(self.player.x, self.player.y, Object.PLAYER)
                self.board.set(x, y, Object.EMPTY)
                self.moves += 1

                return True

        # mamy pusta przestrzen, wiec ustawiamy gracza na nowej pozycji, a ze starej usuwamy
        self.board.set(self.player.x, self.player.y, Object.PLAYER)

        if x != self.player.x or y != self.player.y:
            self.board.set(x, y, Object.EMPTY)
            self.moves += 1

        return True

    def player_next_position(self, direction):
        x, y = self.player.move(direction, self.config['player_step'])
        ret_x, ret_y = self.player.x, self.player.y
        self.player.set_position(x, y)
        return ret_x, ret_y

    def player_move_up(self):
        return self._player_move(Direction.NORTH)

    def player_move_down(self):
        return self._player_move(Direction.SOUTH)

    def player_move_left(self):
        return self._player_move(Direction.WEST)

    def player_move_right(self):
        return self._player_move(Direction.EAST)

    def is_end(self):
        return (self.board.containers, self.board.destroyers) == (0, 0)

    def is_game_over(self):
        return len(self.levels) == self.current_number_level


if __name__ == '__main__':
    e = Engine(pln_file='nuklear.pln')
    # e.configuration(a=1, b=2)
    e.parsefile()
    e.current_level_number = 9

    for lvl in e.levels:
        print(lvl)

    e.start()

    def the_end():
        if e.is_end():
            print('THE END')
        else:
            print('Continuing game')

    def display_level(lvl):
        for y in range(MAX_Y):
            for x in range(MAX_X):
                elem = lvl.board.get(x, y)
                if elem == Object.EMPTY:
                    print(' ', end='')
                elif elem == Object.WALL:
                    print('#', end='')
                elif elem == Object.CONTAINER:
                    print('o', end='')
                elif elem == Object.DESTROYER:
                    print('.', end='')
                elif elem == Object.PLAYER:
                    print('&', end='')
            print()

        the_end()

    print(e.current_level)
    display_level(e.current_level)
    e.player_move_up()
    display_level(e.current_level)
    e.player_move_down()
    display_level(e.current_level)
    e.player_move_left()
    e.player_move_left()
    e.player_move_left()
    display_level(e.current_level)
    e.player_move_up()
    display_level(e.current_level)
    e.player_move_down()
    e.player_move_left()
    e.player_move_left()
    display_level(e.current_level)
    e.player_move_up()
    e.player_move_up()
    e.player_move_right()
    display_level(e.current_level)
    e.player_move_right()
    display_level(e.current_level)
    e.player_move_right()
    e.player_move_right()
    e.player_move_right()
    e.player_move_right()
    e.player_move_right()
    e.player_move_right()
    e.player_move_right()
    display_level(e.current_level)
    e.player_move_up()
    e.player_move_right()
    e.player_move_down()
    display_level(e.current_level)
    e.player_move_left()
    e.player_move_down()
    e.player_move_right()
    e.player_move_right()
    e.player_move_right()
    e.player_move_right()
    e.player_move_right()
    e.player_move_right()
    display_level(e.current_level)
    e.player_move_down()
    e.player_move_right()
    display_level(e.current_level)
    e.player_move_up()
    display_level(e.current_level)
    e.player_move_left()
    e.player_move_left()
    e.player_move_left()
    e.player_move_left()
    e.player_move_left()
    e.player_move_left()
    e.player_move_left()
    e.player_move_left()
    e.player_move_left()
    display_level(e.current_level)
    e.player_move_down()
    display_level(e.current_level)
    e.player_move_left()
    e.player_move_left()
    e.player_move_left()
    e.player_move_left()
    e.player_move_left()
    e.player_move_left()
    e.player_move_left()
    display_level(e.current_level)
    e.player_move_up()
    e.player_move_up()
    e.player_move_up()
    e.player_move_up()
    e.player_move_up()
    e.player_move_up()
    display_level(e.current_level)
    e.player_move_left()
    e.player_move_up()
    e.player_move_right()
    e.player_move_right()
    e.player_move_right()
    e.player_move_right()
    e.player_move_right()
    e.player_move_right()
    e.player_move_right()
    e.player_move_right()
    e.player_move_right()
    display_level(e.current_level)
    e.player_move_up()
    e.player_move_right()
    e.player_move_down()
    e.player_move_down()
    e.player_move_down()
    e.player_move_down()
    e.player_move_left()
    e.player_move_down()
    e.player_move_right()
    e.player_move_right()
    e.player_move_right()
    e.player_move_right()
    display_level(e.current_level)
    e.player_move_up()
    e.player_move_right()
    e.player_move_down()
    display_level(e.current_level)
    e.player_move_down()
    display_level(e.current_level)

# -*- coding: utf-8 -*-
import copy
import gettext
from typing import List, Tuple

import nuklear.lang as lang
from nuklear.parser import MAX_X, MAX_Y, Board, Direction, Level, Object, Parser, Player, Size


_ = lang.i18n.t

max_size = Size(MAX_X, MAX_Y)

CONFIG = {
    'player_step': 1,
    'max_x': 40,
    'max_y': 20,
}


class Engine:
    def __init__(self, pln_file: str, size: int = max_size):
        self.size = size
        self.filename = pln_file
        self.board: Board = None
        self.player: Player = None
        self.levels: List[Level] = []
        self.current_level: Level = None
        self.config = CONFIG.copy()
        self.moves = 0
        # index number of list self.levels
        self.current_number_level = 0

    def parsefile(self) -> None:
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

    def configuration(self, **options) -> None:
        invalid = [x for x in options if x not in CONFIG]

        if invalid:
            raise Exception(_('engine.err_opt') + ' ' + ', '.join(invalid))

        self.config.update(options)

    def start(self) -> bool:
        if self.current_number_level >= len(self.levels):
            return False

        self.current_level = copy.deepcopy(self.levels[self.current_number_level])
        self.board = self.current_level.board
        player_x, player_y = self.board.search_player()
        self.player = Player(player_x, player_y)
        self.moves = 0

        return True

    def next_level(self) -> bool:
        self.current_number_level += 1
        return self.start()

    def _player_move(self, direction: Direction) -> bool:
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

    def player_next_position(self, direction: Direction) -> Tuple[int, int]:
        x, y = self.player.move(direction, self.config['player_step'])
        ret_x, ret_y = self.player.x, self.player.y
        self.player.set_position(x, y)

        return ret_x, ret_y

    def player_move_up(self) -> bool:
        return self._player_move(Direction.NORTH)

    def player_move_down(self) -> bool:
        return self._player_move(Direction.SOUTH)

    def player_move_left(self) -> bool:
        return self._player_move(Direction.WEST)

    def player_move_right(self) -> bool:
        return self._player_move(Direction.EAST)

    def is_end(self) -> bool:
        return (self.board.containers, self.board.destroyers) == (0, 0) or self.current_number_level >= len(self.levels)

    def is_game_over(self) -> bool:
        return len(self.levels) == self.current_number_level

# -*- coding: utf-8 -*-
from enum import Enum, auto, unique
from itertools import repeat
from typing import Dict, List, Tuple

import nuklear.lang as lang
from nuklear.tokenizer import tokenize_file

_ = lang.i18n.t

# FIXME: as parameters Parser, not global variable
MAX_Y = 20
MAX_X = 40

__all__ = [
    'MAX_X',
    'MAX_Y',
    'PlayerNotFoundError',
    'ContainerDestroyerNotEqualError',
    'ZeroContainerError',
    'ZeroDestroyerError',
    'Direction',
    'Object',
    'Player',
    'Board',
    'Level',
    'Parser',
    'Size']


class PlayerNotFoundError(Exception):
    pass


class ContainerDestroyerNotEqualError(Exception):
    pass


class ZeroContainerError(Exception):
    pass


class ZeroDestroyerError(Exception):
    pass


class ParserError(Exception):
    pass


class Size:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y


@unique
class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    WEST = auto()
    EAST = auto()


@unique
class Object(Enum):
    EMPTY = auto()
    WALL = auto()
    CONTAINER = auto()
    DESTROYER = auto()
    PLAYER = auto()


class Player:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def set_position(self, x: int, y: int):
        self.x = x
        self.y = y

    def move(self, direction: Direction, step: int = 1) -> Tuple:
        x, y = self.x, self.y

        if direction == Direction.NORTH:
            self.y -= step
            if self.y < 0:
                self.y = 0
        elif direction == Direction.SOUTH:
            self.y += step
            if self.y >= MAX_Y:
                self.y = MAX_Y - 1
        elif direction == Direction.WEST:
            self.x -= step
            if self.x < 0:
                self.x = 0
        elif direction == Direction.EAST:
            self.x += step
            if self.x >= MAX_X:
                self.x = MAX_X - 1

        return x, y


class Board:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows  # y
        self.cols = cols  # x
        self.containers = 0
        self.destroyers = 0
        self.reset()

    def reset(self) -> None:
        self._board = []

        for _ in range(self.rows):
            self._board.append(list(repeat(Object.EMPTY, self.cols)))

    def get(self, x: int, y: int) -> Object:
        return self._board[y][x]

    def set(self, x: int, y: int, obj: Object) -> None:
        self._board[y][x] = obj

    def from_list(self, list2d: List[List[str]]) -> None:
        for y, row in enumerate(list2d):
            for x, item in enumerate(row):
                if item == ' ':
                    self.set(x, y, Object.EMPTY)
                elif item == '#':
                    self.set(x, y, Object.WALL)
                elif item == '.':
                    self.set(x, y, Object.DESTROYER)
                elif item == 'o':
                    self.set(x, y, Object.CONTAINER)
                elif item == '&':
                    self.set(x, y, Object.PLAYER)

    def check(self) -> None:
        x, y = self.search_player()

        if x == -1 or y == -1:
            raise PlayerNotFoundError(_('parser.player_not_found'))

        self.destroyers = self.num_destroyers()

        if self.destroyers == 0:
            raise ZeroDestroyerError(_('parser.dest_not_found'))

        self.containers = self.num_containers()

        if self.containers == 0:
            raise ZeroContainerError(_('parser.cont_not_found'))

        if self.containers != self.destroyers:
            raise ContainerDestroyerNotEqualError(_('parser.not_equal'))

    def search_player(self) -> Tuple[int, int]:
        for y in range(self.rows):
            for x in range(self.cols):
                if self._board[y][x] == Object.PLAYER:
                    return (x, y)

        return -1, -1

    def num_destroyers(self) -> int:
        return len([x for y in self._board for x in y if x == Object.DESTROYER])

    def num_containers(self) -> int:
        return len([x for y in self._board for x in y if x == Object.CONTAINER])

    def decrement_cointainers(self) -> None:
        self.containers -= 1
        self.destroyers -= 1


class Level:
    def __init__(self, number: int, title: str, author: str, board: Board) -> None:
        self.number = number
        self.title = title
        self.author = author
        self.board = board

    def __str__(self) -> str:
        return f'<{self.__class__.__name__} [title="{self.title}", number={self.number}]>'

    def __repr__(self) -> str:
        return str(self)


class Parser:
    def __init__(self, pln_file: str) -> None:
        self.filename = pln_file
        self.kw_level = False
        self.kw_begin = False
        self.open_braket = False

    def parse(self) -> List[Level]:
        levels = []
        options: Dict[str, str] = {}
        board = Board(MAX_Y, MAX_X)
        board_list = []
        iterator = tokenize_file(self.filename)

        for token in iterator:
            if token.type in ('COMMENT',):
                continue
            elif token.type == 'BEGIN':
                if not self.kw_level:
                    raise ParserError(_('parser.err_token') + f' "{token.text}"')
                self.open_braket = True
            elif token.type == 'KEYWORD':
                if token.text == 'level':
                    self.kw_level = True
                    continue
                if token.text == 'begin' and self.kw_level and self.open_braket:
                    self.kw_begin = True
                else:
                    raise ParserError(_('parser.err_token') + f' "{token.text}"')
            elif token.type == 'OPTION':
                if not self.kw_level or not self.open_braket:
                    raise ParserError(_('parser.err_token') + f' "{token.text}"')
                t = next(iterator)
                if t.type != 'EQUAL':
                    raise ParserError(_(f'parser.err_token') + f' "{t.text}"')
                t = next(iterator)
                if t.type not in ('STRING', 'NUMBER'):
                    raise ParserError(_(f'parser.err_token') + f' "{t.text}"')
                options[token.text] = t.text.replace('"', '')
            elif token.type == 'LINE':
                if not all((self.kw_level, self.open_braket, self.kw_begin)):
                    raise ParserError(_(f'parser.err_token') + f' "{t.text}"')

                board_list.append(token.text)
            elif token.type == 'END':
                board.from_list(board_list)
                board.check()
                levels.append(Level(
                    int(options.get('number', '-1')),
                    options.get('title', ''),
                    options.get('author', ''),
                    board))
                self.kw_level = False
                self.kw_begin = False
                self.open_braket = False
                # number = title = author = Nones
                options = {}  # .clear()
                board_list = []  # .clear()
                board = Board(MAX_Y, MAX_X)

        return levels


if __name__ == '__main__':
    p = Parser('nuklear.pln')
    p.parse()

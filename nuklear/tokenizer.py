# -*- coding: utf-8 -*-

import re
from collections import namedtuple
from typing import Generator


Token = namedtuple('Token', ['type', 'text'])

OPTIONS = [
    'title',
    'author',
    'number']
KEYWORDS = [
    'level',
    'begin']
R_EOL = re.compile(r'[\r\n]+$')
R_LINE = re.compile(r'^[#& .o]+$')
R_NUMBER = re.compile(r'^[0-9.]+$')
T_EOL = '\n'
T_EQUAL = '='
T_COMMENT = ';'
T_BEGIN = '['
T_END = ']'
T_TERM_STR = '"'


def tokenize(line: str) -> Generator[Token, None, None]:
    tokens = iter(line.split(' '))

    for token in tokens:
        token_type = 'WORD'
        eol = R_EOL.search(token)
        if eol:
            token = token.rstrip()
        if token in KEYWORDS:
            token_type = 'KEYWORD'
        elif token in OPTIONS:
            token_type = 'OPTION'
        elif token == T_BEGIN:
            token_type = 'BEGIN'
        elif token == T_END:
            token_type = 'END'
        elif token == T_EQUAL:
            token_type = 'EQUAL'
        elif token and token[0] == T_TERM_STR:
            token_type = 'STRING'
            while True:
                if token[-1] == T_TERM_STR:
                    break
                token += ' ' + next(tokens)
                eol = R_EOL.search(token)
                if eol:
                    token = token.rstrip()

        if token_type == 'WORD' and token.replace('"', '').isdigit():
            token_type = 'NUMBER'

        yield Token(type=token_type, text=token)

        if eol:
            yield Token(type='EOL', text=eol.group())


def tokenize_file(filename: str) -> Generator[Token, None, None]:
    with open(filename) as fd:
        for line in fd:
            eol = R_EOL.search(line)
            board_line = R_LINE.match(line)

            if board_line:
                yield Token(type='LINE', text=board_line.group().rstrip())
            elif line[0] == T_COMMENT:
                yield Token(type='COMMENT', text=line.rstrip())
                if eol:
                    yield Token(type='EOL', text=eol.group())
            elif not line.rstrip():
                yield Token(type='EMPTY', text=line.rstrip())
                if eol:
                    yield Token(type='EOL', text=eol.group())
            else:
                for token in tokenize(line):
                    yield token


if __name__ == '__main__':
    for token in tokenize_file('nuklear.pln'):
        print(token)

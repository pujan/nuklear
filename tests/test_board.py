# -*- coding: utf-8 -*-
import unittest

from nuklear.parser import (Board, ContainerDestroyerNotEqualError, Object,
                            PlayerNotFoundError, ZeroContainerError,
                            ZeroDestroyerError)


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(3, 3)

    def test_attrs(self):
        board = [[Object.EMPTY,
                 Object.EMPTY,
                 Object.EMPTY],
                [Object.EMPTY,
                 Object.EMPTY,
                 Object.EMPTY],
                [Object.EMPTY,
                 Object.EMPTY,
                 Object.EMPTY]]
        self.assertEqual(self.board.rows, 3)
        self.assertEqual(self.board.cols, 3)
        self.assertEqual(self.board._board, board)

    def test_set_get(self):
        self.board.set(1, 1, Object.PLAYER)
        self.assertEqual(self.board.get(1, 1), Object.PLAYER)
        self.board.set(1, 2, Object.CONTAINER)
        self.assertEqual(self.board.get(1, 2), Object.CONTAINER)
        self.board.set(2, 2, Object.DESTROYER)
        self.assertEqual(self.board.get(2, 2), Object.DESTROYER)
        self.board.set(0, 1, Object.WALL)
        self.assertEqual(self.board.get(0, 1), Object.WALL)


    def test_check(self):
        with self.assertRaises(PlayerNotFoundError):
            self.board.check()

        self.board.set(0, 0, Object.PLAYER)

        with self.assertRaises(ZeroDestroyerError):
            self.board.check()

        self.board.set(0, 1, Object.DESTROYER)

        with self.assertRaises(ZeroContainerError):
            self.board.check()

        self.board.set(0, 2, Object.CONTAINER)
        self.board.set(1, 0, Object.DESTROYER)

        with self.assertRaises(ContainerDestroyerNotEqualError):
            self.board.check()

        self.board.set(1, 0, Object.EMPTY)

        self.board.check()

    def test_search_player(self):
        self.assertEqual(self.board.search_player(), (-1, -1))
        self.board.set(2, 2, Object.PLAYER)
        self.assertEqual(self.board.search_player(), (2, 2))

    def test_number_destroyer_container(self):
        self.assertEqual(self.board.num_containers(), 0)
        self.board.set(0, 0, Object.CONTAINER)
        self.board.set(0, 1, Object.CONTAINER)
        self.assertEqual(self.board.num_containers(), 2)

        self.assertEqual(self.board.num_destroyers(), 0)
        self.board.set(1, 0, Object.DESTROYER)
        self.board.set(1, 1, Object.DESTROYER)
        self.assertEqual(self.board.num_destroyers(), 2)

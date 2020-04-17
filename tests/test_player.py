# -*- coding: utf-8 -*-
import unittest

from parser import Player, Direction, MAX_X, MAX_Y


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(10, 12)

    def test_check_attrs(self):
        self.assertEqual(self.player.x, 10)
        self.assertEqual(self.player.y, 12)

        self.player.set_position(20, 19)

        self.assertEqual(self.player.x, 20)
        self.assertEqual(self.player.y, 19)

    def test_move_north(self):
        self.assertEqual(self.player.x, 10)
        self.assertEqual(self.player.y, 12)

        x, y = self.player.move(Direction.NORTH)
        
        self.assertEqual(self.player.x, 10)
        self.assertEqual(self.player.y, 11)
        self.assertEqual(x, 10)
        self.assertEqual(y, 12)
        
        x, y = self.player.move(Direction.NORTH, step=10)

        self.assertEqual(self.player.x, 10)
        self.assertEqual(self.player.y, 1)
        self.assertEqual(x, 10)
        self.assertEqual(y, 11)

        x, y = self.player.move(Direction.NORTH, step=10)

        self.assertEqual(self.player.x, 10)
        self.assertEqual(self.player.y, 0)
        self.assertEqual(x, 10)
        self.assertEqual(y, 1)
        
    def test_move_south(self):
        self.assertEqual(self.player.x, 10)
        self.assertEqual(self.player.y, 12)

        x, y = self.player.move(Direction.SOUTH)

        self.assertEqual(self.player.x, 10)
        self.assertEqual(self.player.y, 13)
        self.assertEqual(x, 10)
        self.assertEqual(y, 12)

        x, y = self.player.move(Direction.SOUTH, step=7)
        self.assertEqual(self.player.x, 10)
        self.assertEqual(self.player.y, 20)
        self.assertEqual(x, 10)
        self.assertEqual(y, 13)
        
        x, y = self.player.move(Direction.SOUTH, step=50)

        self.assertEqual(self.player.x, 10)
        self.assertEqual(self.player.y, 20)
        self.assertEqual(x, 10)
        self.assertEqual(y, 20)

    def test_move_west(self):
        self.assertEqual(self.player.x, 10)
        self.assertEqual(self.player.y, 12)

        x, y = self.player.move(Direction.WEST)

        self.assertEqual(self.player.x, 9)
        self.assertEqual(self.player.y, 12)
        self.assertEqual(x, 10)
        self.assertEqual(y, 12)
        
        x, y = self.player.move(Direction.WEST, step=10)
        self.assertEqual(self.player.x, 0)
        self.assertEqual(self.player.y, 12)
        self.assertEqual(x, 9)
        self.assertEqual(y, 12)

    def test_move_east(self):
        self.assertEqual(self.player.x, 10)
        self.assertEqual(self.player.y, 12)

        x, y = self.player.move(Direction.EAST)

        self.assertEqual(self.player.x, 11)
        self.assertEqual(self.player.y, 12)
        self.assertEqual(x, 10)
        self.assertEqual(y, 12)

        x, y = self.player.move(Direction.EAST, step=10)

        self.assertEqual(self.player.x, 21)
        self.assertEqual(self.player.y, 12)
        self.assertEqual(x, 11)
        self.assertEqual(y, 12)

        x, y = self.player.move(Direction.EAST, step=100)

        self.assertEqual(self.player.x, MAX_X)
        self.assertEqual(self.player.y, 12)
        self.assertEqual(x, 21)
        self.assertEqual(y, 12)


if __name__ == '__main__':
   unittest.main()


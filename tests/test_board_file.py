import unittest

from tarea1 import board_file


class BoardTests(unittest.TestCase):
    def test__is_space_available__space_available__returns_True(self):
        # Arrange
        board = board_file.Board(6)

        # Act
        result = board._is_space_available(5, 5)

        # Assert
        self.assertTrue(result)

    def test__is_space_available__space_is_not_available__returns_False(self):
        # Arrange
        board = board_file.Board(6)
        board.board[5][5] = board_file.Token(board_file.TOKEN_SYMBOLS['x'])

        # Act
        result = board._is_space_available(5, 5)

        # Assert
        self.assertFalse(result)

    def test__is_space_in_bounds__space_is_in_bounds__returns_true(self):
        # Arrange
        board = board_file.Board(3)

        # Act
        result = board._is_space_in_bounds(1, 2)

        # Assert
        self.assertTrue(result)

    def test__is_space_in_bounds__space_is_not_in_bounds__returns_true(self):
        # Arrange
        board = board_file.Board(3)

        # Act
        result = board._is_space_in_bounds(4, 4)

        # Assert
        self.assertFalse(result)


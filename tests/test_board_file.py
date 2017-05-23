import unittest

from tarea1 import board_file


# 11 tests

class BoardTests(unittest.TestCase):
    def test_is_space_available__space_available__returns_True(self):
        # Arrange
        board = board_file.Board(6)

        # Act
        result = board.is_space_available(5, 5)

        # Assert
        self.assertTrue(result)

    def test_is_space_available__space_is_not_available__returns_False(self):
        # Arrange
        board = board_file.Board(6)
        board.board[5][5] = board_file.Token(board_file.TOKEN_SYMBOLS['x'])

        # Act
        result = board.is_space_available(5, 5)

        # Assert
        self.assertFalse(result)

    def test_is_space_in_bounds__space_is_in_bounds__returns_true(self):
        # Arrange
        board = board_file.Board(3)

        # Act
        result = board.is_space_in_bounds(1, 2)

        # Assert
        self.assertTrue(result)

    def test_is_space_in_bounds__space_is_not_in_bounds__returns_true(self):
        # Arrange
        board = board_file.Board(3)

        # Act
        result = board.is_space_in_bounds(4, 4)

        # Assert
        self.assertFalse(result)

    def test_is_valid_move__is_valid__return_True(self):
        # Arrange
        board = board_file.Board(6)

        # Act
        result = board.is_valid_move(5, 5)

        # Assert
        expected = True
        self.assertEqual(result, expected)

    def test_is_valid_move__is_not_valid_bound_row__return_False(self):
        # Arrange
        board = board_file.Board(6)

        # Act
        result = board.is_valid_move(8, 3)

        # Assert
        expected = False
        self.assertEqual(result, expected)

    def test_is_valid_move__is_not_valid_bound_column__return_False(self):
        # Arrange
        board = board_file.Board(6)

        # Act
        result = board.is_valid_move(3, 8)

        # Assert
        expected = False
        self.assertEqual(result, expected)

    def test_is_valid_move__is_not_valid_not_available__return_False(self):
        # Arrange
        board = board_file.Board(6)
        board.make_move('X', 5, 5)
        # Act
        result = board.is_valid_move(5, 5)

        # Assert
        expected = False
        self.assertEqual(result, expected)


class BoardCreatorTests(unittest.TestCase):
    def test_create__length_3__returns_list_of_lists_length_4(self):
        # Arrange
        board_creator = board_file.BoardCreator()

        # Act
        result = board_creator.create(3)

        # Assert
        result = (len(result), len(result[0]))
        expected = (4, 4)
        self.assertEqual(result, expected)


class BoardReviewerTests(unittest.TestCase):
    def test_look_for_draw__empty_board__returns_False(self):
        # Arrange
        board_creator = board_file.BoardCreator()
        board = board_creator.create(4)
        board_reviewer = board_file.BoardReviewer()

        # Act
        result = board_reviewer.look_for_draw(board)

        # Assert
        expected = False
        self.assertEqual(result, expected)

    def test_look_for_draw__tied_board__returns_True(self):
        # Arrange
        board_creator = board_file.BoardCreator()
        board = board_creator.create(3)
        board[1][1].title = 'X'
        board[1][2].title = 'X'
        board[1][3].title = 'O'

        board[2][1].title = 'O'
        board[2][2].title = 'O'
        board[2][3].title = 'X'

        board[3][1].title = 'X'
        board[3][2].title = 'O'
        board[3][3].title = 'X'

        board_reviewer = board_file.BoardReviewer()

        # Act
        result = board_reviewer.look_for_draw(board)

        # Assert
        expected = True
        self.assertEqual(result, expected)

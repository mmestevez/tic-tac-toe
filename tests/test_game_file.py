import unittest

from tarea1 import game_file


class GameTests(unittest.TestCase):
    def test_is_players_turn__is_x_turn__returns_True(self):
        # Arrange
        game = game_file.Game()
        game.turn = 'X'

        # Act
        result = game.is_players_turn('X')

        # Assert
        expected = True
        self.assertEqual(expected, result)

    def test_is_players_turn__is_x_turn_try_with_o__returns_False(self):
        # Arrange
        game = game_file.Game()
        game.turn = 'X'

        # Act
        result = game.is_players_turn('O')

        # Assert
        expected = False
        self.assertEqual(expected, result)

    def test_is_players_turn__is_o_turn_try_with_o__returns_True(self):
        # Arrange
        game = game_file.Game()
        game.turn = 'O'

        # Act
        result = game.is_players_turn('O')

        # Assert
        expected = True
        self.assertEqual(expected, result)

    def test_is_players_turn__is_o_turn_try_with_x__returns_False(self):
        # Arrange
        game = game_file.Game()
        game.turn = 'O'

        # Act
        result = game.is_players_turn('X')

        # Assert
        expected = False
        self.assertEqual(expected, result)

    def test_is_players_turn__no_turn_
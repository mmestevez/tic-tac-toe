import unittest

from tarea1 import score_file


class ScoreReaderTests(unittest.TestCase):
    def test_read_scores__file_with_numbers__returns_list_of_four_elements(self):
        # Arrange
        score_reader = score_file.ScoreReader()

        # Act
        result = score_reader.read_scores()

        # Assert
        expected = [3, 1, 1, 1]
        self.assertEqual(expected, result)

    def test_read_scores__not_existing_route__returns_list_of_four_zeros(self):
        # Arrange
        score_reader = score_file.ScoreReader()
        route = 'not-existent.txt'

        # Act
        result = score_reader.read_scores(route=route)

        # Assert
        expected = [0] * 4
        self.assertEqual(expected, result)

    def test_read_scores__wrong_amount_of_numbers__returns_list_of_four_zeros(self):
        # Arrange
        score_reader = score_file.ScoreReader()
        route = 'tic-tac-toe-2.txt'

        # Act
        result = score_reader.read_scores(route=route)

        # Assert
        expected = [0] * 4
        self.assertEqual(expected, result)

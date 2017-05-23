""" Contains classes for managing every thing related to the board."""

COLUMN_SYMBOLS = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E',
                  6: 'F', 7: 'G', 8: 'H', 9: 'I',
                  'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7,
                  'H': 8, 'I': 9}
TOKEN_SYMBOLS = {'x': 'X', 'o': 'O', 'nil': ' '}


class Board(object):
    def __init__(self, board_size):
        board_creator = BoardCreator()
        self.board = board_creator.create(board_size)
        self.board_size = board_size
        """ Last token coordinate must be bigger than the
        board so brackets don't show in the empty board """
        self.last_token_coordinate = [board_size + 1, board_size + 1]
        self.board_reviewer = BoardReviewer()

    def print_board(self, board_printer):
        board_printer.print_board(self.board, self.last_token_coordinate)

    def is_valid_move(self, row, column):
        if self.is_space_in_bounds(row, column) and self.is_space_available(
                row, column):
            return True
        return False

    def make_move(self, token_title, row, column):
        self.board[row][column].set_title(token_title)
        self.last_token_coordinate = [row, column]

    def look_for_winner(self):
        return self.board_reviewer.get_winner(self.board)

    def look_for_draw(self):
        return self.board_reviewer.look_for_draw(self.board)

    def is_space_in_bounds(self, row, column):
        try:
            token = self.board[row][column]
            return True
        except IndexError:
            BoardPrinter.print_out_of_bounds_message()
            return False

    def is_space_available(self, row, column):
        try:
            token = self.board[row][column]

            if not token.is_nil_token():
                raise IOError
            return True
        except IOError:
            BoardPrinter.print_used_space_message()
            return False


class BoardReviewer(object):
    def __init__(self):
        pass

    @staticmethod
    def look_for_draw(board):
        # If the range is len(board) it takes de blank space in the corner.
        for row in range(1, len(board)):
            for token in board[row]:
                if token.is_nil_token():
                    return False
        return True

    def get_winner(self, board):
        winner = self._get_winner_on_each_row(board)
        if not winner.is_nil_token():
            return winner
        winner = self._get_winner_on_each_column(board)
        if not winner.is_nil_token():
            return winner
        winner = self._get_winner_on_diagonals(board)
        return winner

    def _get_winner_on_each_row(self, board):
        for row in range(1, len(board)):
            winner = self._get_winner_in_row(board, row)
            if not winner.is_nil_token():
                return winner
        return Token(TOKEN_SYMBOLS['nil'])

    def _get_winner_on_each_column(self, board):
        for column in range(1, len(board)):
            winner = self._get_winner_in_column(board, column)
            if not winner.is_nil_token():
                return winner
        return Token(TOKEN_SYMBOLS['nil'])

    def _get_winner_on_diagonals(self, board):
        winner = self._get_descending_diagonal_winner(board)
        if not winner.is_nil_token():
            return winner
        winner = self._get_ascending_diagonal_winner(board)
        if not winner.is_nil_token():
            return winner
        return Token(TOKEN_SYMBOLS['nil'])

    @staticmethod
    def _get_winner_in_row(board, row):
        winner = board[row][1]
        if winner.is_nil_token():
            return Token(TOKEN_SYMBOLS['nil'])
        for position in range(2, len(board)):
            if not winner.__eq__(board[row][position]):
                return Token(TOKEN_SYMBOLS['nil'])
        return winner

    @staticmethod
    def _get_winner_in_column(board, column):
        winner = board[1][column]
        if winner.is_nil_token():
            return Token(TOKEN_SYMBOLS['nil'])
        for row in range(2, len(board)):
            if not winner.__eq__(board[row][column]):
                return Token(TOKEN_SYMBOLS['nil'])
        return winner

    @staticmethod
    def _get_descending_diagonal_winner(board):
        winner = board[1][1]
        if winner.is_nil_token():
            return Token(TOKEN_SYMBOLS['nil'])
        for position in range(2, len(board)):
            if not winner.__eq__(board[position][position]):
                return Token(TOKEN_SYMBOLS['nil'])
        return winner

    @staticmethod
    def _get_ascending_diagonal_winner(board):
        winner = board[1][len(board) - 1]
        if winner.is_nil_token():
            return Token(TOKEN_SYMBOLS['nil'])
        for position in range(1, len(board)):
            token = board[position][len(board) - position]
            if not winner.__eq__(token):
                return Token(TOKEN_SYMBOLS['nil'])
        return winner


class BoardPrinter(object):
    def __init__(self):
        pass

    @staticmethod
    def print_board(board, last_coordinate):
        for row in range(len(board)):
            BoardPrinter.print_column(board, last_coordinate, row)

    @staticmethod
    def print_column(board, last_coordinate, row):
        for column in range(len(board)):
            BoardPrinter.print_token(board, column, last_coordinate, row)
        print

    @staticmethod
    def print_token(board, column, last_coordinate, row):
        if row == last_coordinate[0] and column == last_coordinate[1]:
            print '[' + board[row][column].title + ']',
        else:
            print ' ' + board[row][column].title + ' ',

    @staticmethod
    def print_used_space_message():
        print 'Used space. Please try again'

    @staticmethod
    def print_out_of_bounds_message():
        print 'Out of bounds. Please try again'


class BoardCreator(object):
    def __init__(self):
        pass

    def create(self, length):
        board = []
        for row_number in range(length + 1):
            row = self._create_row(length, row_number)
            board.append(row)
        return board

    def _create_row(self, length, row):
        row_with_tokens = []
        for position in range(length + 1):
            token = self._get_corresponding_token(position, row)
            row_with_tokens.append(token)
        return row_with_tokens

    @staticmethod
    def _get_corresponding_token(position, row):
        title_for_token = TOKEN_SYMBOLS['nil']
        if row == 0:
            if position != 0:
                title_for_token = str(position)
        else:
            if position == 0:
                title_for_token = COLUMN_SYMBOLS[row]
        return Token(title_for_token)


class Token(object):
    def __init__(self, title):
        self.title = title

    def __eq__(self, token):
        if token.title == self.title:
            return True
        return False

    def is_nil_token(self):
        nil = Token(TOKEN_SYMBOLS['nil'])
        return self.__eq__(nil)

    def set_title(self, title):
        self.title = title

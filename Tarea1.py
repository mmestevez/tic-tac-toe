import re

Column = {1: ' A ', 2: ' B ', 3: ' C ', 4: ' D ', 5: ' E ', 6: ' F ',
          7: ' G ', 8: ' H ', 9: ' I ',
          'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
          'I': 9}


class Board:
    def __init__(self, board_size):
        self.board = self.create_board(board_size)
        self.nil_element = Element('   ')
        self.board_size = board_size

    @staticmethod
    def create_board(length):
        board = []
        for row in range(length + 1):
            row_with_elements = []
            for position in range(length + 1):
                title_for_element = '   '
                if row == 0:
                    if position != 0:
                        title_for_element = ' ' + str(position) + ' '
                else:
                    if position == 0:
                        title_for_element = Column[row]
                element = Element(title_for_element)
                row_with_elements.append(element)
            board.append(row_with_elements)
        return board

    def print_board(self):
        for row in self.board:
            for element in row:
                print element.title,
            print

    def place_element(self, element, row, column):
        self.board[row][column] = element

    def check_for_winner(self):
        winner = self.check_for_winner_on_each_row()
        if not winner.is_equal_element(self.nil_element):
            return winner
        winner = self.check_for_winner_on_each_column()
        if not winner.is_equal_element(self.nil_element):
            return winner
        winner = self.check_for_winner_on_each_diagonal()
        return winner

    def check_for_winner_on_each_row(self):
        for row in range(1, len(self.board)):
            winner = self.check_for_winner_in_row(row)
            if not winner.is_equal_element(self.nil_element):
                return winner
        return self.nil_element

    def check_for_winner_on_each_column(self):
        for column in range(1, self.board_size):
            winner = self.check_for_winner_in_column(column)
            if not winner.is_equal_element(self.nil_element):
                return winner
        return self.nil_element

    def check_for_winner_on_each_diagonal(self):
        winner = self.check_winner_on_descendant_diagonal()
        if not winner.is_equal_element(self.nil_element):
            return winner
        self.check_winner_on_ascendant_diagonal()
        return winner

    def check_for_winner_in_row(self, row):
        winner = self.board[row][1]
        if winner.is_equal_element(self.nil_element):
            return self.nil_element
        for position in range(1, self.board_size):
            if not winner.is_equal_element(self.board[row][position]):
                return self.nil_element
            return winner

    def check_for_winner_in_column(self, column):
        winner = self.board[1][column]
        if winner.is_equal_element(self.nil_element):
            return self.nil_element
        for row in range(2, self.board_size):
            if not winner.is_equal_element(self.board[row][column]):
                return self.nil_element
        return winner

    def check_winner_on_descendant_diagonal(self):
        winner = self.board[1][1]
        if winner.is_equal_element(self.nil_element):
            return self.nil_element
        for position in range(2, self.board_size):
            if not winner.is_equal_element(self.board[position][position]):
                return self.nil_element
        return winner

    def check_winner_on_ascendant_diagonal(self):
        winner = self.board[1][1]
        if winner.is_equal_element(self.nil_element):
            return self.nil_element
        for position in range(2, self.board_size):
            element = self.board[self.board_size - position][position]
            if not winner.is_equal_element(element):
                return self.nil_element
        return winner

    def make_move(self, element, row, column):
        if self.board.is_space_in_bounds(row, column):
            if self.board.is_space_available(row, column):
                self.board.place_element(element, row, column)

    def is_space_available(self, row, column):
        try:
            element = self.board[row][column]
            if not element.is_equal_element(self.nil_element):
                raise IOError
            return True
        except IOError:
            print 'Used space. Please try again'
            return False

    def is_space_in_bounds(self, row, column):
        try:
            self.board[row][column]
            return True
        except IndexError:
            print 'Out of bounds. Please try again'
            return False


class Element:
    def __init__(self, title):
        self.title = title
        self.is_label = False
        self.is_the_last = False

    def is_equal_element(self, element):
        if element.title[1] == self.title[1]:
            return True
        return False


class Score:
    def __init__(self):
        self.x_winnings, self.o_winnings = self.read_score_file()

    @staticmethod
    def read_score_file():
        try:
            saved_file = open('tic-tac-toe.txt', 'r')
            if saved_file:
                x_winnings = saved_file.readline()
                o_winnings = saved_file.readline()
                saved_file.close()
        except IOError:
                x_winnings = 0
                o_winnings = 0
        return x_winnings, o_winnings

    def save_score(self):
        saved_file = file.open('saved_file', 'W')
        saved_file.write(self.x_winnings)
        saved_file.write(self.o_winnings)
        saved_file.close()

    def show_score(self):
        print 'player X has won:', self.x_winnings, 'times'
        print 'player O has won:', self.o_winnings, 'times'

    def increase_x_score(self):
        self.x_winnings += 1

    def increase_o_score(self):
        self.o_winnings += 1


class Game:
    def __init__(self):
        self.silent_mode = False
        self.consecutive_mode = False
        self.turn = 0
        self.score = Score()
        self.board = None

    def go_to_action(self):
        print 'Welcome to > tic tac toe < Write your command or help'
        while True:
            command = raw_input()
            if re.search(r'^start ', command):
                settings = command[6:]
                if re.search(r'[3-9]$', settings):
                    board_size = int(settings)
                elif re.search(
                        r'(--silent --consecutive)|(--consecutive --silent) [3-9]$',
                        settings):
                    settings = settings.split()
                    board_size = int(settings[-1])
                    silent_mode = True
                    self.consecutive_mode = True
                elif re.search(r'--(silent)|(consecutive) [3-9]$',
                               settings):
                    settings = settings.split()
                    board_size = int(settings[-1])
                    if re.search(r'(--silent)', settings[0]):
                        self.silent_mode = True
                    else:
                        self.consecutive_mode = True
                else:
                    print 'Wrong format, please try again'
                    break
                self.board = Board(board_size)
            elif re.search(r'^play ', command):
                self.play(command)

            elif re.search(r'^score', command):
                self.score.show_score()
            elif re.search(r'^help', command):
                self.show_help()
            elif re.search(r'exit', command):
                exit()
            else:
                print 'Wrong instruction, please try again'
            if not self.silent_mode:
                self.board.print_board()

    def start(self, command):
        settings = command[6:]
        if re.search(r'[3-9]$', settings):
            self.board = Board(int(settings))
        elif re.search(
                r'--(silent --consecutive)|(consecutive --silent) [3-9]$',
                settings):
            settings = settings.split()
            self.board = Board(int(settings[-1]))
            self.silent_mode = True
            self.consecutive_mode = True
        elif re.search(r'--(silent)|(consecutive) [3-9]$', settings):
            settings = settings.split()
            self.board = Board(int(settings[-1]))
            if re.search(r'(--silent)', settings[0]):
                self.silent_mode = True
            else:
                self.consecutive_mode = True
        else:
            print 'Wrong format, please try again'

    def play(self, expression):
        if re.search(r'^play [o|x] [a-i][1-9]$', expression):
            command = expression.split()
            player = command[1].upper()
            row = command[2][0]
            column = int(command[2][1])
            if self.is_players_turn(player):
                title = (' ' + player + ' ')
                element = Element(title)
                self.board.make_move(element, row, column)

                self.set_next_turn(player)

    @staticmethod
    def show_help():
        start_help = 'start[ --silent][ --consecutive] <number>\t' \
                     'start a game with size <number> form 3 to 9\n' \
                     + '\t' * 11 \
                     + '--silent mode don\'t show the board\n' \
                     + '\t' * 11 \
                     + '--consecutive is for one player mode\n'
        play_help = 'play <player> <row><column>' \
                    + '\t' * 5 \
                    + 'Make a move for <player> "o" or "x", in <row> \n' \
                    + '\t' * 11 \
                    + 'from A to the final letter on the board and ' \
                      '<column> form 1 to the board size\n'
        score_help = 'score' + '\t' * 10 \
                     + 'shows the historic score saved\n'
        exit_help = 'exit' + '\t' * 10 + 'exits the program'
        print start_help + play_help + score_help + exit_help

def is_players_turn(self, player):
    if player == self.turn:
        return True
    return False


def set_next_turn(self, player):
    if self.consecutive_mode:
        self.turn = player
    else:
        if player == 'X':
            self.turn = 'O'
        else:
            self.turn = 'X'





class Parser:
    def __init__(self):
        self.START_RE = r'^start '
        self.SILENT_RE = r'--silent '
        self.CONSECUTIVE_RE = r'--consecutive '
        self.BOARD_SIZE_RE = r'[3-9]$'
        pass

    def match_start_expression(self, expression):
        pass


if __name__ == '__main__':
    game = Game()
    game.go_to_action()

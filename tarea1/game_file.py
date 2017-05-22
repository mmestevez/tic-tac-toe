import re
from tarea1 import board_file
from tarea1 import score_file


class Game(object):
    def __init__(self):
        self.silent_mode = False
        self.consecutive_mode = False
        self.turn = 0
        self.score = self._set_score()
        self.board = board_file.Board(0)
        self.game_on = False

    def run(self, game_printer, input_reader):
        game_printer.print_welcome_message()
        while True:
            game_printer.print_legend()
            command = input_reader.get_input()

            if re.search(r'^start ', command):
                if self.game_on:
                    game_printer.print_game_on_message()
                    continue
                self.start(command, game_printer)
            elif re.search(r'^play ', command):
                if not self.game_on:
                    game_printer.print_start_new_game_message()
                self.play(command, game_printer)
            elif re.search(r'^score', command):
                score_printer = score_file.ScorePrinter()
                self.score.show(score_printer)
            elif re.search(r'^help$', command):
                self.show_help()
            elif re.search(r'exit', command):
                exit()
            else:
                game_printer.print_wrong_format_message()
            if not self.silent_mode and self.game_on:
                board_printer = board_file.BoardPrinter()
                self.board.print_board(board_printer)

    def start(self, command, game_printer):
        self.silent_mode = False
        self.consecutive_mode = False
        settings = command[6:]
        if re.search(r'^[3-9]$', settings):
            board_size = int(settings)
        elif re.search(
                r'^--(silent --consecutive)|(consecutive --silent) [3-9]$',
                settings):
            settings = settings.split()
            board_size = int(settings[-1])
            self.silent_mode = True
            self.consecutive_mode = True
        elif re.search(r'^--(silent)|(consecutive) [3-9]$', settings):
            settings = settings.split()
            board_size = int(settings[-1])
            if re.search(r'(--silent)', settings[0]):
                self.silent_mode = True
            else:
                self.consecutive_mode = True
        else:
            game_printer.print_wrong_format_message()
            game_printer.print_start_format()
            return
        self.board = board_file.Board(board_size)
        self.game_on = True
        self.turn = 0

    def play(self, expression, game_printer):
        if re.search(r'^play [o|x] [a-i][1-9]$', expression):
            command = expression.split()
            player = command[1].upper()
            row = board_file.COLUMN_SYMBOLS[command[2][0].upper()]
            column = int(command[2][1])
            if self.is_players_turn(player):
                token_title = player
                self.board.make_move(token_title, row, column)
                winner = self.board.look_for_winner()
                if not winner.is_nil_token():
                    print 'Player {0} wins! Congratulations'.format(player)
                    score_manager = score_file.ScoreManager()
                    self.score.update(player, score_manager)
                    self.set_next_turn(player)
                    self.game_on = False
                else:
                    if self.board.look_for_draw():
                        self.game_on = False
                        print 'Game over. Its a tye'
                    self.set_next_turn(token_title)
            else:
                game_printer.print_not_your_turn_message()
        else:
            game_printer.print_wrong_format_message()
            game_printer.print_play_format()

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
        if self.turn == 0:
            self.turn = player
            return True
        if self.turn == player:
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

    @staticmethod
    def _set_score():
        score_reader = score_file.ScoreReader()
        score_list = score_reader.read_scores()
        score = score_reader.create_score(score_list)
        return score


class GamePrinter(object):
    def __init__(self):
        pass

    @staticmethod
    def print_welcome_message():
        print 'Welcome to > tic tac toe < Write your command or help'

    @staticmethod
    def print_legend():
        print "tic-tac-toe >> ",

    @staticmethod
    def print_wrong_format_message():
        print 'Wrong format, please try again'

    @staticmethod
    def print_start_new_game_message():
        print 'Start a new game'

    @staticmethod
    def print_game_on_message():
        print 'You have a game on. You can\'t start a new one'

    @staticmethod
    def print_start_format():
        print 'start [--silent][--consecutive] [3..9]'

    @staticmethod
    def print_play_format():
        print 'play [x-o] [a..i][1..9]'

    @staticmethod
    def print_not_your_turn_message():
        print 'Its not your turn. Please try again'


class InputParser(object):
    pass

    def parse_command(self, command):
        if re.match(r'^start', command):
            self.parse_start_command(command)
        elif re.match(r'^play ', command):
            self.parse_play_command(command)
        elif re.match(r'(^help)|(-h$)', command):
            self.parse_help_command(command)
        elif re.match(r'^score', command):
            self.parse_exit_command()

    def parse_start_command(self, command):

        pass

    def parse_play_command(self, command):
        pass

    def parse_help_command(self, command):
        pass

    def parse_score_command(self, command):
        pass

    def parse_exit_command(self, command):
        pass


class InputReader(object):
    @staticmethod
    def get_input():
        return raw_input()

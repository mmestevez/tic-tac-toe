import re

from tarea1 import board_file
from tarea1 import score_file

COMMANDS = ['start', 'play', 'board', 'score', 'help', 'exit']


class Game(object):
    def __init__(self):
        self.is_silent_mode = False
        self.is_consecutive_mode = False
        self.turn = 0
        self.score = self._set_score()
        self.board = board_file.Board(0)
        self.is_game_on = False

    def run(self, game_printer, input_reader):
        game_printer.print_welcome_message()
        board_printer = board_file.BoardPrinter()
        while True:
            game_printer.print_legend()
            command = input_reader.get_input()
            command = command.lower()
            if re.search(r'(^help$)|(-h$)', command):
                self.help(command)
            elif re.search(r'^start ', command):
                if self.is_game_on:
                    game_printer.print_game_on_message()
                    continue
                self.start(command, game_printer)

            elif re.search(r'^play ', command):
                if not self.is_game_on:
                    game_printer.print_start_new_game_message()
                    continue
                self.play(command, game_printer)

            elif re.search(r'^board$', command):
                if self.is_game_on:
                    self.board.print_board(board_printer)
                else:
                    game_printer.print_start_new_game_message()

            elif re.search(r'^score$', command):
                score_printer = score_file.ScorePrinter()
                self.score.show(score_printer)

            elif re.search(r'exit', command):
                exit()
            else:
                game_printer.print_wrong_format_message()
            if self.is_game_on and not self.is_silent_mode:
                self.board.print_board(board_printer)

    def start(self, command, game_printer):
        self.is_silent_mode = False
        self.is_consecutive_mode = False
        settings = command[6:]
        if re.search(r'^[3-9]$', settings):
            board_size = int(settings)
        elif re.search(
                r'^--(silent --consecutive)|(consecutive --silent) [3-9]$',
                settings):
            settings = settings.split()
            board_size = int(settings[-1])
            self.is_silent_mode = True
            self.is_consecutive_mode = True
        elif re.search(r'^--(silent)|(consecutive) [3-9]$', settings):
            settings = settings.split()
            board_size = int(settings[-1])
            if re.search(r'(--silent)', settings[0]):
                self.is_silent_mode = True
            else:
                self.is_consecutive_mode = True
        else:
            game_printer.print_wrong_format_message()
            game_printer.print_start_format()
            return
        self.board = board_file.Board(board_size)
        self.is_game_on = True
        self.turn = 0

    def play(self, expression, game_printer):
        if re.search(r'^play [o|x] [a-i][1-9]$', expression):
            command = expression.split()
            player = command[1].upper()
            row = board_file.COLUMN_SYMBOLS[command[2][0].upper()]
            column = int(command[2][1])
            if self.is_players_turn(player):
                token_title = player
                if self.board.is_valid_move(row, column):
                    self.board.make_move(token_title, row, column)
                    self._set_next_turn(token_title)
                winner = self.board.look_for_winner()

                if not winner.is_nil_token():
                    game_printer.print_player_wins(winner.title)
                    score_manager = score_file.ScoreManager()
                    self.score.update(player, score_manager)
                    self._set_next_turn(board_file.TOKEN_SYMBOLS['nil'])
                    self.is_game_on = False

                else:
                    if self.board.look_for_draw():
                        self.is_game_on = False
                        game_printer.print_game_over_tye()

                    self._set_next_turn(board_file.TOKEN_SYMBOLS['nil'])
            else:
                game_printer.print_not_your_turn_message()
        else:
            game_printer.print_wrong_format_message()
            game_printer.print_play_format()

    def help(self, command):
        command = command.split()
        if command[0] in COMMANDS:
            if len(command) == 2 and command[1] == '-h':
                self.show_help(command[0])
            elif command[0] == 'help':
                self.show_help()

    @staticmethod
    def show_help(command='help'):
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
        board_help = 'board' + '\t' * 10 \
                     + 'shows the playing board.'
        score_help = 'score' + '\t' * 10 \
                     + 'shows the historic score saved\n'
        exit_help = 'exit' + '\t' * 10 + 'exits the program'
        help_help = '[command] -h' + '\t' * 8 \
                    + 'shows help for that command\n'
        if command == 'start':
            print start_help
        elif command == 'play':
            print play_help
        elif command == 'score':
            print score_help
        elif command == 'board':
            print board_help
        elif command == 'help':
            print help_help + start_help + play_help,
            print board_help + score_help + exit_help
        elif command == 'exit':
            print exit_help

    def is_players_turn(self, player):
        if self.turn == 0:
            self.turn = player
            return True
        if self.turn == player:
            return True
        return False

    def _set_next_turn(self, player):
        if self.is_consecutive_mode:
            self.turn = player
        else:
            if player == 'X':
                self.turn = 'O'
            elif player == 'O':
                self.turn = 'X'
            elif player == board_file.TOKEN_SYMBOLS['nil']:
                self.turn = 0

    @staticmethod
    def _set_score():
        score_reader = score_file.ScoreReader()
        score_list = score_reader.read_scores()
        score = score_reader.create_score(score_list)
        return score

    def set_consecutive_silent(self):
        self.set_consecutive()
        self.set_silent()

    def set_consecutive(self):
        self.is_consecutive_mode = True

    def set_silent(self):
        self.is_silent_mode = True


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

    @staticmethod
    def print_player_wins(player):
        print 'Player {0} wins! Congratulations'.format(player)

    @staticmethod
    def print_game_over_tye():
        print 'Game over. Its a tye'


class InputReader(object):
    @staticmethod
    def get_input():
        return raw_input()

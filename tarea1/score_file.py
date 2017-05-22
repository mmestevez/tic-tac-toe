from tarea1.board_file import TOKEN_SYMBOLS


class Score(object):
    def __init__(self):
        self.total_games = 0
        self.x_winnings = 0
        self.o_winnings = 0
        self.tye_games = 0

    def set_total_games(self, amount):
        self.total_games = amount

    def set_x_winnings(self, amount):
        self.x_winnings = amount

    def set_o_winnings(self, amount):
        self.o_winnings = amount

    def set_tye_games(self, amount):
        self.tye_games = amount

    def update(self, winner_title, score_manager):
        if winner_title == TOKEN_SYMBOLS['x']:
            self._increase_x_winnings()
        elif winner_title == TOKEN_SYMBOLS['o']:
            self._increase_o_winnings()
        elif winner_title == TOKEN_SYMBOLS['nil']:
            self._increase_tye_games()
        self.save_scores_in_file(score_manager)

    def _increase_x_winnings(self):
        self._increase_total_games()
        self.x_winnings += 1

    def _increase_o_winnings(self):
        self._increase_total_games()
        self.o_winnings += 1

    def _increase_tye_games(self):
        self._increase_total_games()
        self.tye_games += 1

    def _increase_total_games(self):
        self.total_games += 1

    def save_scores_in_file(self, score_manager):
        score_manager.save_scores_in_file(self._scores_to_list())

    def _scores_to_list(self):
        return [self.total_games, self.x_winnings, self.o_winnings,
                self.tye_games]

    @staticmethod
    def _scores_dict_from_list(scores_list):
        scores_dict = {'total_games': scores_list[0],
                       'x_winnings': scores_list[1],
                       'o_winnings': scores_list[2],
                       'tye_total': scores_list[3]}
        return scores_dict

    def show(self, score_printer):
        score_printer.print_score(self.total_games, self.x_winnings,
                                  self.o_winnings, self.tye_games)


class ScorePrinter(object):
    def __init__(self):
        pass

    @staticmethod
    def print_score(total_games=0, x_winnings=0, o_winnings=0, tye_games=0):
        print 'Number of games played:', total_games
        print 'Number of games X has won:', x_winnings
        print 'Number of games O has won:', o_winnings
        print 'Number of games no one won:', tye_games


class ScoreManager(object):
    def __init__(self):
        pass

    @staticmethod
    def save_scores_in_file(score_saver, scores_list):
        score_saver.save_scores(scores_list)

    @staticmethod
    def get_scores(score_reader):
        scores_list = score_reader.read_scores()
        score = score_reader.create_score(scores_list)
        return score


class ScoreReader(object):
    def __init__(self):
        pass

    @staticmethod
    def create_score(scores_list):
        score = Score()
        if scores_list[0]:
            score.set_total_games(scores_list[0])
        if scores_list[1]:
            score.set_x_winnings(scores_list[1])
        if scores_list[2]:
            score.set_o_winnings(scores_list[2])
        if scores_list[3]:
            score.set_tye_games(scores_list[3])
        return score

    @staticmethod
    def read_scores(route='tic-tac-toe.txt'):
        score_file = open(route, 'r')
        scores_list = []
        try:
            total_games = int(score_file.readline())
            scores_list.append(total_games)
            x_winnings = int(score_file.readline())
            scores_list.append(x_winnings)
            o_winnings = int(score_file.readline())
            scores_list.append(o_winnings)
            tye_games = int(score_file.readline())
            scores_list.append(tye_games)
        except ValueError:
            scores_list = [0] * 4
        return scores_list


class ScoreSaver(object):
    def __init__(self):
        pass

    @staticmethod
    def save_scores(score_values_list):
        score_file = open(ROUTE, 'w')
        for score in score_values_list:
            score_file.write(str(score) + '\n')
        score_file.close()

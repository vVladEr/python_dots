import shelve


class StatisticSaver:
    def __init__(self, file_name='game_statistic'):
        self.file_dict = shelve.open(file_name)

    def get(self, name):
        if name in self.file_dict:
            return self.file_dict[name]
        else:
            return None

    def update_player_statistic(self, player, is_won, is_draw=False):
        name = player.name
        if name not in self.file_dict:
            self.file_dict[name] = PlayerStatistic(name)
        self.file_dict[name] = self.file_dict[name].update_statistic(player.scores, is_won, is_draw)

    def __del__(self):
        self.file_dict.close()


class PlayerStatistic:
    def __init__(self, name):
        self.name = name
        self.games_count = 0
        self.victories_count = 0
        self.defeats_count = 0
        self.draws_count = 0
        self.max_score = 0

    def update_statistic(self, scores, is_won, is_draw=False):
        self.games_count += 1
        self.max_score = max(self.max_score, scores)
        if is_won:
            self.victories_count += 1
        elif is_draw:
            self.draws_count += 1
        else:
            self.defeats_count += 1
        return self

    def __str__(self):
        name = self.name
        if name != name[:10]:
            name = name[:10] + '...'
        result_lines = [name + ':', f'Total games: {self.games_count}',
                        f'Victories: {self.victories_count}', f'Defeats: {self.defeats_count}',
                        f'Max scores: {self.max_score}']
        return '\n'.join(result_lines)

import shelve


class StatisticSaver:
    def __init__(self, file_name='game_statistic'):
        self.file_dict = shelve.open(file_name)

    def get(self, name):
        if name in self.file_dict:
            return self.file_dict[name]
        else:
            return None

    def update_player_statistic(self, name, is_won, is_draw=False):
        if name not in self.file_dict:
            self.file_dict[name] = PlayerStatistic(name)
        self.file_dict[name] = self.file_dict[name].update_statistic(is_won, is_draw)

    def __del__(self):
        self.file_dict.close()


class PlayerStatistic:
    def __init__(self, name):
        self.name = name
        self.games_count = 0
        self.victories_count = 0
        self.defeats_count = 0
        self.draws_count = 0
        # self.captured_points_count = 0

    def update_statistic(self, is_won, is_draw=False):
        self.games_count += 1
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
                        f'Victories: {self.victories_count}', f'Defeats: {self.defeats_count}']
        return '\n'.join(result_lines)


if __name__ == '__main__':
    pass
    # s = StatisticSaver('ok')
    # s.update_player_statistic('r', False)
    # print(s.get('r'))

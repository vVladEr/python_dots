import shelve


class Statistic:
    def __init__(self, file_name='game_statistic'):
        self.file = shelve.open(file_name)

    def add(self, name, value):
        self.file[name] = value

    def get(self, name):
        try:
            return self.file[name]
        except KeyError:
            return None

    def __del__(self):
        self.file.close()


if __name__ == '__main__':
    s = Statistic('ok')
    print(s.get('s'))

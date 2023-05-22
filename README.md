# Dots Game (Игра "Точки")

Dots Game - это реализация игры в точки с допольнительными техническими требованиями, предоставленными в учебных целях.

## Описание

В игре "Точки" можно играть от 1 до 4 человек. В случае, если игрок 1, создается виртуальный оппонент 'Robot', выступающий в роли соперника. Игроки ходят поочереди. Если один игрок смог захватить вражеские(-ую) точки(-у), то есть замкнуть контур вокруг них, то игрок учеличивает количество очков на количество захваченных точек.
Побеждает игрок, набравший больше всех очков. 

## Запуск игры
Чтобы начать игру, запустите файл main.py. (Технические требования к игре описаны в файле 'requirements.txt')

## Уровни сложности игры с компьютером

Есть 2 уровня сложности игры против компьютера, которые можно выбрать в начале игры. 1) Базовый - компьютер ставит наугад точки; 2) Компьютер использует некоторую стратегию и тактику.

## Остановка и перезапуск игры

Для того чтобы вернуться в меню, нажмите клавишу Q, а затем появившуюся кнопку 'Back to menu' (в этом случае в статистику засчитается поражение для текущего игрока).
Если на поле закончилось место для точек, то игра заканчивается, и появляется кнопка возврата в меню.

## Тестирование

В проекте представлены тесты в папке tests, проверяющие корректную работу игровых функций.

### Проект содержит несколько классов:

#### Game

Класс Game содержит основную логику работы игры, отрисовку игры, а также управление 'Menu'.

#### Bfs

Класс Bfs содержит методы для поиска захваченных областей и точек.

#### Map

Класс Map содержит основные методы для работы с игровым полем.

#### Player
Класс Player содержит основную информацию о игроках.

#### AI_player
Класс AI_player содержит логику работы компьютера оппонента.

#### Statistic
Класс Statistic содержит логику для сохранения статистики и рекордов для игроков.
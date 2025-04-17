class Robot:
    def __init__(self, board, start_x, start_y, direction='NORTH'):
        # Инициализация доски (стена '-', пустая клетка '*', не закрашенная '#', закрашенная '+')
        self.board = [list(row) for row in board]
        self.x = start_x
        self.y = start_y
        self.direction = direction
        self.visited = set()  # Множество для отслеживания посещенных клеток
        self.moves_history = []  # Список для хранения истории ходов
        self.board_states = []  # Список для хранения состояний поля
        
        # Проверка начальной позиции
        if not (0 <= self.y < len(self.board) and 0 <= self.x < len(self.board[self.y])):
            raise ValueError("Start position out of board bounds")
        elif self.board[self.y][self.x] == '-':
            raise ValueError("Robot cannot start on a wall")
        else:
            self.visited.add((self.x, self.y))
            if self.board[self.y][self.x] == '#':
                self.board[self.y][self.x] = '+'
                self._add_move("fill", self.x, self.y)
            # Сохраняем начальное состояние
            self._save_board_state()

    def _save_board_state(self):
        """Сохраняет текущее состояние поля"""
        current_state = {
            'board': [list(row) for row in self.board],
            'x': self.x,
            'y': self.y,
            'direction': self.direction
        }
        self.board_states.append(current_state)

    def _add_move(self, action, x, y):
        """Добавляет ход в историю"""
        self.moves_history.append({
            'action': action,
            'x': x,
            'y': y,
            'direction': self.direction
        })
        # Сохраняем состояние поля после каждого хода
        self._save_board_state()

    def turn_left(self):
        directions = {'NORTH': 'WEST', 'WEST': 'SOUTH', 'SOUTH': 'EAST', 'EAST': 'NORTH'}
        self.direction = directions[self.direction]
        self._add_move("turn_left", self.x, self.y)

    def turn_right(self):
        directions = {'NORTH': 'EAST', 'EAST': 'SOUTH', 'SOUTH': 'WEST', 'WEST': 'NORTH'}
        self.direction = directions[self.direction]
        self._add_move("turn_right", self.x, self.y)

    def forward(self):
        return self._move_in_direction(self.direction)

    def down(self):
        opposite_dir = {'NORTH': 'SOUTH', 'SOUTH': 'NORTH', 'EAST': 'WEST', 'WEST': 'EAST'}[self.direction]
        return self._move_in_direction(opposite_dir)

    def left(self):
        self.turn_left()

    def right(self):
        self.turn_right()

    def _move_in_direction(self, direction):
        dx, dy = 0, 0
        if direction == 'NORTH': 
            dy = 1
        elif direction == 'EAST': 
            dx = 1
        elif direction == 'SOUTH': 
            dy = -1
        elif direction == 'WEST': 
            dx = -1
        else:
            return False
            
        new_x, new_y = self.x + dx, self.y + dy
        
        # Проверка границ и стены
        if 0 <= new_y < len(self.board) and 0 <= new_x < len(self.board[new_y]):
            if self.board[new_y][new_x] != '-':
                self.x, self.y = new_x, new_y
                self.visited.add((self.x, self.y))
                if self.board[self.y][self.x] == '#':
                    self.board[self.y][self.x] = '+'
                    self._add_move("fill", self.x, self.y)
                else:
                    self._add_move("move", self.x, self.y)
                return True
        return False

    def is_wall_forward(self):
        return self._is_wall_in_direction(self.direction)

    def is_wall_left(self):
        left_dir = {'NORTH': 'WEST', 'WEST': 'SOUTH', 'SOUTH': 'EAST', 'EAST': 'NORTH'}[self.direction]
        return self._is_wall_in_direction(left_dir)

    def is_wall_right(self):
        right_dir = {'NORTH': 'EAST', 'EAST': 'SOUTH', 'SOUTH': 'WEST', 'WEST': 'NORTH'}[self.direction]
        return self._is_wall_in_direction(right_dir)

    def is_wall_down(self):
        opposite_dir = {'NORTH': 'SOUTH', 'SOUTH': 'NORTH', 'EAST': 'WEST', 'WEST': 'EAST'}[self.direction]
        return self._is_wall_in_direction(opposite_dir)

    def _is_wall_in_direction(self, direction):
        dx, dy = 0, 0
        if direction == 'NORTH': dy = 1
        elif direction == 'EAST': dx = 1
        elif direction == 'SOUTH': dy = -1
        elif direction == 'WEST': dx = -1
        
        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_y < len(self.board) and 0 <= new_x < len(self.board[new_y]):
            return self.board[new_y][new_x] == '-'
        return True

    def print_board(self):
        # Использование цикла for для печати доски
        for y in reversed(range(len(self.board))):
            row = []
            for x in range(len(self.board[y])):
                if x == self.x and y == self.y:
                    dir_char = {'NORTH':'^', 'EAST':'>', 'SOUTH':'v', 'WEST':'<'}[self.direction]
                    row.append(dir_char)
                else:
                    row.append(self.board[y][x])
            print(' '.join(row))
        print()

    def flood_fill(self, x, y):
        """Рекурсивная заливка области."""
        if not (0 <= y < len(self.board) and 0 <= x < len(self.board[y])):
            return
        if self.board[y][x] in ('-', '+'):
            return
        self.board[y][x] = '+'
        self.flood_fill(x + 1, y)  # Вправо
        self.flood_fill(x - 1, y)  # Влево
        self.flood_fill(x, y + 1)  # Вверх
        self.flood_fill(x, y - 1)  # Вниз

    def fill_area(self):
        """Запускает заливку области с текущей позиции робота."""
        self.flood_fill(self.x, self.y)

    def _is_surrounded(self, x, y):
        # Проверка окружения клетки с использованием if-elif-else
        if y > 0 and self.board[y-1][x] == '*':
            return False
        elif y < len(self.board)-1 and self.board[y+1][x] == '*':
            return False
        elif x > 0 and self.board[y][x-1] == '*':
            return False
        elif x < len(self.board[y])-1 and self.board[y][x+1] == '*':
            return False
        return True

    def move_in_square_pattern(self, steps):
        # Использование цикла for с шагами
        for i in range(steps):
            if i % 4 == 0:
                self.forward()
            elif i % 4 == 1:
                self.right()
                self.forward()
            elif i % 4 == 2:
                self.right()
                self.forward()
            else:
                self.right()
                self.forward()
            self.print_board()

    def has_unfilled_cells(self):
        """Проверяет наличие не закрашенных клеток на поле."""
        for row in self.board:
            if '#' in row:
                return True
        return False

    def autonomous_filling(self):
        """Улучшенный алгоритм автономной заливки."""
        steps = 0
        max_steps = 50  # Увеличенный лимит шагов
        last_position = None
        stuck_counter = 0
        
        while self.has_unfilled_cells() and steps < max_steps:
            current_pos = (self.x, self.y)
            
            # Проверка на зацикливание
            if current_pos == last_position:
                stuck_counter += 1
                if stuck_counter > 4:  # Если застряли, меняем направление
                    self.turn_right()
                    stuck_counter = 0
            else:
                stuck_counter = 0
                last_position = current_pos
            
            # Основная логика движения
            if not self.is_wall_forward():
                self.forward()
            elif not self.is_wall_left():
                self.turn_left()
                self.forward()
            elif not self.is_wall_right():
                self.turn_right()
                self.forward()
            else:
                self.turn_right()
                self.turn_right()
                self.forward()
            
            steps += 1
        
            # Подсчет штрафных шагов
            penalty_steps = self._count_penalty_steps()
            total_steps = steps + penalty_steps
            
            # Вывод результатов
            print("\nРезультаты выполнения:")
            print("-" * 40)
            print(f"Количество выполненных шагов: {steps}")
            print(f"Количество штрафных шагов: {penalty_steps}")
            print(f"Общее количество шагов с учетом штрафов: {total_steps}")
            print(f"Успешность выполнения: {'Да' if steps < max_steps else 'Нет'}")
            print(f"Остались ли не закрашенные клетки: {'Да' if self.has_unfilled_cells() else 'Нет'}")
            print("-" * 40)
        
        return steps < max_steps  # Возвращаем True, если заливка успешно завершена

    def _count_penalty_steps(self):
        """Подсчитывает количество штрафных шагов за неверно закрашенные клетки"""
        penalty = 0
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == '#':  # Не закрашенная клетка
                    penalty += 1
                elif self.board[y][x] == '+' and self._is_surrounded(x, y):  # Неверно закрашенная клетка
                    penalty += 1
        return penalty

    def print_moves(self):
        """Выводит все ходы робота в читаемом формате"""
        print("\nИстория ходов робота:")
        print("-" * 40)
        for i, move in enumerate(self.moves_history, 1):
            action_text = {
                'move': 'Перемещение',
                'turn_left': 'Поворот налево',
                'turn_right': 'Поворот направо',
                'fill': 'Закрашивание клетки'
            }.get(move['action'], move['action'])
            
            print(f"{i}. {action_text} -> позиция ({move['x']}, {move['y']}), направление: {move['direction']}")
        print("-" * 40)
        print(f"Всего ходов: {len(self.moves_history)}")

    def print_board_state(self, state, move_number=None, action_text=None):
        """Выводит состояние поля"""
        if move_number is not None and action_text is not None:
            print(f"\nХод #{move_number}: {action_text}")
        print("-" * (len(state['board'][0]) * 2 + 1))
        for y in reversed(range(len(state['board']))):
            row = []
            for x in range(len(state['board'][y])):
                if x == state['x'] and y == state['y']:
                    dir_char = {'NORTH':'^', 'EAST':'>', 'SOUTH':'v', 'WEST':'<'}[state['direction']]
                    row.append(dir_char)
                else:
                    row.append(state['board'][y][x])
            print(' '.join(row))
        print("-" * (len(state['board'][0]) * 2 + 1))

    def print_moves_with_states(self):
        """Выводит все ходы робота с отображением состояния поля после каждого хода"""
        print("\nПолная история ходов робота с состояниями поля:")
        print("=" * 40)
        
        # Выводим начальное состояние
        print("\nНачальное состояние:")
        self.print_board_state(self.board_states[0])
        
        # Выводим каждый ход и состояние поля после него
        for i, (move, state) in enumerate(zip(self.moves_history, self.board_states[1:]), 1):
            action_text = {
                'move': 'Перемещение',
                'turn_left': 'Поворот налево',
                'turn_right': 'Поворот направо',
                'fill': 'Закрашивание клетки'
            }.get(move['action'], move['action'])
            
            self.print_board_state(
                state,
                i,
                f"{action_text} -> позиция ({move['x']}, {move['y']}), направление: {move['direction']}"
            )
        
        print(f"\nВсего ходов: {len(self.moves_history)}")
        print("=" * 40)

    @staticmethod
    def create_board_A():
        """Создает поле как на картинке A."""
        board = [
            ['*', '-', '#', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '-', '#', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '-', '#', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '-', '#', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '-', '#', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '-', '#', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '-', '#', '#', '#', '#', '#', '*', '*', '*'],
            ['*', '-', '-', '-', '-', '-', '-', '*', '*', '*'],
            ['*', '-', '*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '-', '*', '*', '*', '*', '*', '*', '*', '*']
        ]
        return board
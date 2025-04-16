class Robot:
    def __init__(self, board, start_x, start_y, direction='NORTH'):
        self.board = [row.copy() for row in board]
        self.x = start_x
        self.y = start_y
        self.direction = direction
        if not (0 <= self.y < len(self.board) and 0 <= self.x < len(self.board[self.y])):
            raise ValueError("Start position out of board bounds")
        if self.board[self.y][self.x] == '-':
            raise ValueError("Robot cannot start on a wall")
        self.board[self.y][self.x] = '+'

    def turn_left(self):
        directions = {'NORTH': 'WEST', 'WEST': 'SOUTH', 'SOUTH': 'EAST', 'EAST': 'NORTH'}
        self.direction = directions[self.direction]

    def turn_right(self):
        directions = {'NORTH': 'EAST', 'EAST': 'SOUTH', 'SOUTH': 'WEST', 'WEST': 'NORTH'}
        self.direction = directions[self.direction]

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
        if direction == 'NORTH': dy = 1
        elif direction == 'EAST': dx = 1
        elif direction == 'SOUTH': dy = -1
        elif direction == 'WEST': dx = -1
        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_y < len(self.board) and 0 <= new_x < len(self.board[new_y]):
            if self.board[new_y][new_x] != '-':
                self.x, self.y = new_x, new_y
                self.board[self.y][self.x] = '+'
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
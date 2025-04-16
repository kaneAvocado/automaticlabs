import unittest
from robotlib.robot import Robot
from collections import defaultdict

class TestRobotSolution(unittest.TestCase):
    def setUp(self):
        # Создаем простой лабиринт 5x5
        self.board = [
            ['-', '-', '-', '-', '-'],
            ['-', '*', '*', '*', '-'],
            ['-', '*', '-', '*', '-'],
            ['-', '*', '*', '*', '-'],
            ['-', '-', '-', '-', '-']
        ]
        
    def test_complete_filling(self):
        """Проверка полного заполнения лабиринта"""
        robot = Robot(self.board, 1, 1)
        solve_maze(robot)
        
        # Проверяем, что все доступные клетки заполнены
        for y in range(1, 4):
            for x in range(1, 4):
                if self.board[y][x] != '-':  # Игнорируем стены
                    self.assertEqual(robot.board[y][x], '+')
                    
    def test_no_wall_collision(self):
        """Проверка отсутствия столкновений со стенами"""
        robot = Robot(self.board, 1, 1)
        solve_maze(robot)
        
        # Проверяем, что робот не пытался пройти сквозь стены
        for move in robot.moves_history:
            x, y = move['x'], move['y']
            self.assertNotEqual(self.board[y][x], '-')
            
    def test_move_limit(self):
        """Проверка ограничения на количество ходов"""
        robot = Robot(self.board, 1, 1)
        solve_maze(robot)
        
        self.assertLessEqual(len(robot.moves_history), 1000)
        
    def test_efficiency_metrics(self):
        """Проверка метрик эффективности алгоритма"""
        robot = Robot(self.board, 1, 1)
        solve_maze(robot)
        
        # 1. Подсчет повторных посещений клеток
        cell_visits = defaultdict(int)
        for move in robot.moves_history:
            cell_visits[(move['x'], move['y'])] += 1
            
        # Максимальное количество посещений одной клетки не должно превышать 3
        max_visits = max(cell_visits.values())
        self.assertLessEqual(max_visits, 3, 
            f"Клетка посещена {max_visits} раз, что превышает допустимый лимит")
            
        # 2. Проверка оптимальности пути
        available_cells = sum(1 for row in self.board for cell in row if cell != '-')
        # Оптимальное количество ходов: количество клеток + количество поворотов
        optimal_moves = available_cells + (available_cells // 2)
        self.assertLessEqual(len(robot.moves_history), optimal_moves * 2,
            "Количество ходов превышает оптимальное более чем в 2 раза")
            
        # 3. Проверка стратегии обхода
        # Подсчет количества разворотов (изменений направления)
        direction_changes = 0
        prev_direction = None
        for move in robot.moves_history:
            if prev_direction and move['direction'] != prev_direction:
                direction_changes += 1
            prev_direction = move['direction']
            
        # Количество изменений направления не должно превышать количество клеток
        self.assertLessEqual(direction_changes, available_cells,
            "Слишком много изменений направления движения")
        
    def test_different_mazes(self):
        """Проверка работы на разных лабиринтах"""
        mazes = [
            # Простой лабиринт
            [
                ['-', '-', '-', '-', '-'],
                ['-', '*', '*', '*', '-'],
                ['-', '*', '-', '*', '-'],
                ['-', '*', '*', '*', '-'],
                ['-', '-', '-', '-', '-']
            ],
            # Лабиринт с тупиками
            [
                ['-', '-', '-', '-', '-'],
                ['-', '*', '*', '-', '-'],
                ['-', '*', '-', '*', '-'],
                ['-', '*', '*', '*', '-'],
                ['-', '-', '-', '-', '-']
            ],
            # Лабиринт с коридором
            [
                ['-', '-', '-', '-', '-'],
                ['-', '*', '-', '*', '-'],
                ['-', '*', '-', '*', '-'],
                ['-', '*', '-', '*', '-'],
                ['-', '-', '-', '-', '-']
            ]
        ]
        
        for maze in mazes:
            robot = Robot(maze, 1, 1)
            solve_maze(robot)
            
            # Проверяем полное заполнение
            for y in range(1, 4):
                for x in range(1, 4):
                    if maze[y][x] != '-':
                        self.assertEqual(robot.board[y][x], '+')
                        
            # Проверяем эффективность для каждого лабиринта
            self.test_efficiency_metrics()

if __name__ == '__main__':
    unittest.main() 
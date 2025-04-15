from ..robotlib.robot import Robot
import random

# def create_random_board(width, height, wall_prob=0.2):
#     """Создает случайное поле со стенами и пустыми клетками."""
#     board = []
#     for _ in range(height):
#         row = []
#         for _ in range(width):
#             if random.random() < wall_prob:
#                 row.append('-')  # Стена
#             else:
#                 row.append('#')  # Не закрашенная клетка
#         board.append(row)
#     return board

# def create_board_A():
#     """Создает поле как на картинке A."""
#     board = [
#         ['*', '-', '#', '*', '*', '*', '*', '*', '*', '*'],
#         ['*', '-', '#', '*', '*', '*', '*', '*', '*', '*'],
#         ['*', '-', '#', '*', '*', '*', '*', '*', '*', '*'],
#         ['*', '-', '#', '*', '*', '*', '*', '*', '*', '*'],
#         ['*', '-', '#', '*', '*', '*', '*', '*', '*', '*'],
#         ['*', '-', '#', '*', '*', '*', '*', '*', '*', '*'],
#         ['*', '-', '#', '#', '#', '#', '#', '*', '*', '*'],
#         ['*', '-', '-', '-', '-', '-', '-', '*', '*', '*'],
#         ['*', '-', '*', '*', '*', '*', '*', '*', '*', '*'],
#         ['*', '-', '*', '*', '*', '*', '*', '*', '*', '*']
#     ]
#     return board

def test_autonomous_filling():
    # 1. Создаем поле как на картинке A
    board = Robot.create_board_A()
    
    # 2. Устанавливаем робота в правую часть
    start_x, start_y = 6, 6
    
    # 3. Инициализируем робота
    robot = Robot(board, start_x, start_y, 'NORTH')
    print("Начальное состояние поля:")
    robot.print_board()
    
    # 4. Запускаем улучшенный алгоритм заливки
    success = robot.autonomous_filling()
    
    print("Поле после заливки:")
    robot.print_board()
    
    # 5. Выводим все ходы робота с состояниями поля
    robot.print_moves_with_states()
    
    if success:
        print("Заливка успешно завершена")
    else:
        print("Достигнут лимит шагов, заливка не завершена")
    
    # Проверяем, что все не закрашенные клетки были обработаны
    if robot.has_unfilled_cells():
        print("ВНИМАНИЕ: Остались не закрашенные клетки!")
    else:
        print("Все клетки успешно закрашены")
    
    # Возвращаем результаты теста
    return {
        'name': 'Тестовый',
        'surname': 'Пользователь',
        'steps': len(robot.moves_history)
    }

# Запуск теста
if __name__ == '__main__':
    test_autonomous_filling()
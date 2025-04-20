from robotlib.robot import Robot

def test_autonomous_filling():
    # Создаем поле
    board = Robot.create_board_A()
    
    # Создаем робота в начальной позиции (3, 1) - верхний левый угол буквы "П"
    robot = Robot(board, 3, 1, 'EAST')
    steps = 0
    
    # Шаг 1: Движемся вправо по верхней части
    for _ in range(4):
        robot.forward()  # Двигаемся вправо
        steps += 1
    
    # Шаг 2: Поворачиваем и движемся вниз
    robot.turn_right()
    steps += 1
    
    for _ in range(6):
        robot.forward()  # Двигаемся вниз
        steps += 1
    
    # Шаг 3: Поворачиваем и движемся влево
    robot.turn_right()
    steps += 1
    
    for _ in range(4):
        robot.forward()  # Двигаемся влево
        steps += 1
    
    # Шаг 4: Поворачиваем и движемся вверх
    robot.turn_right()
    steps += 1
    
    for _ in range(5):
        robot.forward()  # Двигаемся вверх
        steps += 1
    
    # Шаг 5: Теперь обходим внутреннюю часть буквы "П"
    robot.turn_right()
    robot.forward()
    robot.turn_right()
    steps += 3
    
    for _ in range(4):
        robot.forward()  # Двигаемся вниз
        steps += 1
    
    robot.turn_left()
    robot.forward()
    robot.forward()
    robot.turn_left()
    steps += 4
    
    for _ in range(4):
        robot.forward()  # Двигаемся вверх
        steps += 1
    
    # Подсчитываем штрафные шаги
    penalty_info = robot._count_penalty_steps()
    
    # Формируем результат
    result = {
        'name': 'Иван',  # Имя студента
        'surname': 'Иванов',  # Фамилия студента
        'steps': steps,  # Количество шагов
        'penalty_steps': penalty_info['penalty'],  # Штрафные шаги
        'total_steps': steps + penalty_info['penalty'],  # Общее количество шагов
        'total_target_cells': penalty_info['total_target_cells'],  # Всего клеток для закрашивания
        'unfilled_cells': penalty_info['unfilled_cells'],  # Незакрашенные клетки
        'extra_filled_cells': penalty_info['extra_filled_cells']  # Лишние закрашенные клетки
    }
    
    # Печатаем доску для визуализации результата
    robot.print_board()
    
    return result

if __name__ == '__main__':
    result = test_autonomous_filling()
    print(f"Результаты:")
    print(f"Шаги: {result['steps']}")
    print(f"Штрафные шаги: {result['penalty_steps']}")
    print(f"Всего шагов: {result['total_steps']}")
    print(f"Всего клеток для закрашивания: {result['total_target_cells']}")
    print(f"Незакрашенных клеток: {result['unfilled_cells']}")
    print(f"Лишних закрашенных клеток: {result['extra_filled_cells']}")
    print(f"Имя и фамилия: {result['name']} {result['surname']}") 
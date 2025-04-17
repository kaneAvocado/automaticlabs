from robotlib.robot import Robot

def test_autonomous_filling():
    # Создаем поле
    board = Robot.create_board_A()
    
    # Создаем робота в начальной позиции (2, 0) - верхняя точка буквы "Г"
    robot = Robot(board, 2, 0, 'SOUTH')
    steps = 0
    
    # Шаг 1: Движемся вниз по вертикальной части
    for _ in range(6):
        robot.forward()  # Двигаемся вниз
        steps += 1
    
    # Шаг 2: Поворачиваем направо для горизонтальной части
    robot.turn_right()
    steps += 1
    
    # Шаг 3: Движемся вправо по горизонтальной части
    for _ in range(4):
        robot.forward()  # Двигаемся вправо
        steps += 1
    
    # Подсчитываем штрафные шаги
    penalty_steps = robot._count_penalty_steps()
    
    # Формируем результат
    result = {
        'name': 'Иван',  # Имя студента
        'surname': 'Иванов',  # Фамилия студента
        'steps': steps,  # Количество шагов
        'penalty_steps': penalty_steps,  # Штрафные шаги
        'total_steps': steps + penalty_steps  # Общее количество шагов
    }
    
    return result

if __name__ == '__main__':
    result = test_autonomous_filling()
    print(f"Результаты:")
    print(f"Шаги: {result['steps']}")
    print(f"Штрафные шаги: {result['penalty_steps']}")
    print(f"Всего шагов: {result['total_steps']}") 
from robotlib.robot import Robot

def test_autonomous_filling():
    # Создаем поле как на картинке A
    board = Robot.create_board_A()

    
    
    # Устанавливаем робота в оптимальную позицию
    start_x, start_y = 6, 6
    
    # Инициализируем робота
    robot = Robot(board, start_x, start_y, 'NORTH')
    
    # Запускаем расширенный алгоритм заливки
    success = robot.autonomous_filling()
    
    # Выводим подробную информацию о выполнении
    print(f"Количество выполненных шагов: {len(robot.moves_history)}")
    print(f"Успешность выполнения: {'Да' if success else 'Нет'}")
    print(f"Остались ли не закрашенные клетки: {'Да' if robot.has_unfilled_cells() else 'Нет'}")
    
    # Возвращаем результаты теста
    return {
        'name': 'Сергей',
        'surname': 'Сергеев',
        'steps': len(robot.moves_history)
    }

if __name__ == '__main__':
    test_autonomous_filling() 
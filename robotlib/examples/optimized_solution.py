from robotlib.robot import Robot

def test_autonomous_filling():
    # Создаем поле как на картинке A
    board = Robot.create_board_A()
    
    # Устанавливаем робота в оптимальную позицию
    start_x, start_y = 6, 6
    
    # Инициализируем робота
    robot = Robot(board, start_x, start_y, 'NORTH')
    
    # Запускаем оптимизированный алгоритм заливки
    success = robot.autonomous_filling()
    
    # Проверяем результат
    if not success:
        print("Достигнут лимит шагов")
    elif robot.has_unfilled_cells():
        print("Остались не закрашенные клетки")
    else:
        print("Все клетки успешно закрашены")
    
    # Возвращаем результаты теста
    return {
        'name': 'Петр',
        'surname': 'Петров',
        'steps': len(robot.moves_history)
    }

if __name__ == '__main__':
    test_autonomous_filling() 
from robotlib.robot import Robot

def test_autonomous_filling():
    # Создаем поле как на картинке A
    board = Robot.create_board_A()
    
    # Устанавливаем робота в правую часть
    start_x, start_y = 6, 6
    
    # Инициализируем робота
    robot = Robot(board, start_x, start_y, 'NORTH')
    
    # Запускаем алгоритм заливки
    success = robot.autonomous_filling()
    
    # Возвращаем результаты теста
    return {
        'name': 'Иван',
        'surname': 'Иванов',
        'steps': len(robot.moves_history)
    }

if __name__ == '__main__':
    test_autonomous_filling() 
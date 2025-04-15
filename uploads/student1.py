from robotlib.robot import Robot

def test_autonomous_filling():
    """
    Тест автономного заполнения формы роботом
    """
    # Создаем экземпляр робота
    robot = Robot(
        board=[[0, 0, 0], [0, 0, 0], [0, 0, 0]],  # Пустая доска 3x3
        start_x=0,  # Начальная позиция по X
        start_y=0   # Начальная позиция по Y
    )
    
    # Запускаем робота
    robot.run()
    
    # Получаем результаты
    results = {
        "name": "Иван",
        "surname": "Иванов",
        "steps": robot.get_steps()
    }
    
    return results 
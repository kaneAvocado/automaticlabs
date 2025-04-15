from chess5x5.game.board import Board, Color, Piece, PieceType

def evaluate_position(board: Board, color: Color) -> float:
    """
    Улучшенная оценка позиции на доске 5x5.
    Учитывает материальное преимущество, позиционные факторы, безопасность фигур и мобильность.
    
    Args:
        board: Объект доски 5x5
        color: Цвет, за который оценивается позиция (WHITE или BLACK)
        
    Returns:
        float: Оценка позиции (положительное значение - преимущество, отрицательное - недостаток)
    """
    score = 0.0
    
    # Значения фигур с учетом их относительной силы
    piece_values = {
        PieceType.PAWN: 1.0,
        PieceType.ROOK: 5.0,
        PieceType.BISHOP: 3.0,
        PieceType.KING: 100.0
    }
    
    # Бонусы за позицию пешек (учитывая их продвижение)
    pawn_position_bonus = [
        [0.0, 0.0, 0.0, 0.0, 0.0],
        [0.5, 0.5, 0.5, 0.5, 0.5],
        [0.2, 0.2, 0.3, 0.2, 0.2],
        [0.1, 0.1, 0.2, 0.1, 0.1],
        [0.0, 0.0, 0.0, 0.0, 0.0]
    ]
    
    # Бонус за контроль центра (усилен в центре)
    center_bonus = [
        [0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.2, 0.3, 0.2, 0.0],
        [0.0, 0.3, 0.5, 0.3, 0.0],
        [0.0, 0.2, 0.3, 0.2, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0]
    ]
    
    # Бонусы за мобильность фигур
    mobility_bonus = {
        PieceType.PAWN: 0.1,
        PieceType.ROOK: 0.2,
        PieceType.BISHOP: 0.3,
        PieceType.KING: 0.1
    }
    
    # Подсчет материального преимущества и позиционных бонусов
    for row in range(board.size):
        for col in range(board.size):
            piece = board.get_piece(row, col)
            if piece:
                # Базовое значение фигуры
                value = piece_values[piece.type]
                
                # Множитель в зависимости от цвета
                multiplier = 1.0 if piece.color == color else -1.0
                
                # Добавляем позиционный бонус для пешек
                if piece.type == PieceType.PAWN:
                    if piece.color == Color.WHITE:
                        value += pawn_position_bonus[row][col]
                    else:
                        value += pawn_position_bonus[board.size - 1 - row][col]
                
                # Добавляем бонус за контроль центра
                if piece.color == Color.WHITE:
                    value += center_bonus[row][col]
                else:
                    value += center_bonus[board.size - 1 - row][col]
                
                # Проверяем безопасность фигуры
                if not is_piece_safe(board, row, col, piece.color):
                    value -= 0.5  # Штраф за небезопасность
                
                # Проверяем изолированность пешек
                if piece.type == PieceType.PAWN and is_pawn_isolated(board, row, col, piece.color):
                    value -= 0.3  # Штраф за изолированность
                
                # Добавляем бонус за мобильность
                value += calculate_mobility(board, row, col, piece) * mobility_bonus[piece.type]
                
                score += value * multiplier
    
    # Проверяем безопасность короля
    king_safety = evaluate_king_safety(board, color)
    score += king_safety
    
    return score

def is_piece_safe(board: Board, row: int, col: int, color: Color) -> bool:
    """
    Проверяет, находится ли фигура под атакой.
    """
    # Проверяем атаки по горизонтали и вертикали (ладьи)
    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        r, c = row + dr, col + dc
        while 0 <= r < board.size and 0 <= c < board.size:
            piece = board.get_piece(r, c)
            if piece:
                if piece.color != color and piece.type == PieceType.ROOK:
                    return False
                break
            r, c = r + dr, c + dc
    
    # Проверяем атаки по диагонали (слоны)
    for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        r, c = row + dr, col + dc
        while 0 <= r < board.size and 0 <= c < board.size:
            piece = board.get_piece(r, c)
            if piece:
                if piece.color != color and piece.type == PieceType.BISHOP:
                    return False
                break
            r, c = r + dr, c + dc
    
    return True

def is_pawn_isolated(board: Board, row: int, col: int, color: Color) -> bool:
    """
    Проверяет, является ли пешка изолированной.
    """
    # Проверяем наличие соседних пешек того же цвета
    for dr, dc in [(0, 1), (0, -1)]:
        r, c = row, col + dc
        if 0 <= c < board.size:
            piece = board.get_piece(r, c)
            if piece and piece.type == PieceType.PAWN and piece.color == color:
                return False
    
    return True

def calculate_mobility(board: Board, row: int, col: int, piece: Piece) -> int:
    """
    Вычисляет мобильность фигуры (количество доступных ходов).
    """
    mobility = 0
    
    if piece.type == PieceType.PAWN:
        # Для пешек считаем только продвижение вперед
        direction = 1 if piece.color == Color.WHITE else -1
        new_row = row + direction
        if 0 <= new_row < board.size:
            # Прямое продвижение
            if not board.get_piece(new_row, col):
                mobility += 1
            # Взятие по диагонали
            for dc in [-1, 1]:
                new_col = col + dc
                if 0 <= new_col < board.size:
                    target = board.get_piece(new_row, new_col)
                    if target and target.color != piece.color:
                        mobility += 1
    
    elif piece.type == PieceType.ROOK:
        # Для ладьи считаем ходы по горизонтали и вертикали
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            r, c = row + dr, col + dc
            while 0 <= r < board.size and 0 <= c < board.size:
                target = board.get_piece(r, c)
                if not target:
                    mobility += 1
                elif target.color != piece.color:
                    mobility += 1
                    break
                else:
                    break
                r, c = r + dr, c + dc
    
    elif piece.type == PieceType.BISHOP:
        # Для слона считаем ходы по диагонали
        for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = row + dr, col + dc
            while 0 <= r < board.size and 0 <= c < board.size:
                target = board.get_piece(r, c)
                if not target:
                    mobility += 1
                elif target.color != piece.color:
                    mobility += 1
                    break
                else:
                    break
                r, c = r + dr, c + dc
    
    elif piece.type == PieceType.KING:
        # Для короля считаем все возможные ходы
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < board.size and 0 <= new_col < board.size:
                    target = board.get_piece(new_row, new_col)
                    if not target or target.color != piece.color:
                        mobility += 1
    
    return mobility

def evaluate_king_safety(board: Board, color: Color) -> float:
    """
    Оценивает безопасность короля.
    """
    # Находим позицию короля
    king_pos = None
    for row in range(board.size):
        for col in range(board.size):
            piece = board.get_piece(row, col)
            if piece and piece.type == PieceType.KING and piece.color == color:
                king_pos = (row, col)
                break
        if king_pos:
            break
    
    if not king_pos:
        return -100.0  # Король не найден - критическая ситуация
    
    king_row, king_col = king_pos
    safety_score = 0.0
    
    # Проверяем защиту короля своими фигурами
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            new_row, new_col = king_row + dr, king_col + dc
            if 0 <= new_row < board.size and 0 <= new_col < board.size:
                piece = board.get_piece(new_row, new_col)
                if piece and piece.color == color:
                    safety_score += 0.2  # Бонус за защиту
    
    # Проверяем атаки на короля
    for row in range(board.size):
        for col in range(board.size):
            piece = board.get_piece(row, col)
            if piece and piece.color != color:
                if can_attack_square(board, row, col, king_row, king_col, piece):
                    safety_score -= 0.5  # Штраф за атаку на короля
    
    return safety_score

def can_attack_square(board: Board, from_row: int, from_col: int, to_row: int, to_col: int, piece: Piece) -> bool:
    """
    Проверяет, может ли фигура атаковать указанную клетку.
    """
    if piece.type == PieceType.PAWN:
        # Пешки атакуют по диагонали
        direction = 1 if piece.color == Color.WHITE else -1
        return abs(to_row - from_row) == 1 and abs(to_col - from_col) == 1 and to_row - from_row == direction
    
    elif piece.type == PieceType.ROOK:
        # Ладьи атакуют по горизонтали и вертикали
        return from_row == to_row or from_col == to_col
    
    elif piece.type == PieceType.BISHOP:
        # Слоны атакуют по диагонали
        return abs(to_row - from_row) == abs(to_col - from_col)
    
    elif piece.type == PieceType.KING:
        # Король атакует на одну клетку в любом направлении
        return abs(to_row - from_row) <= 1 and abs(to_col - from_col) <= 1
    
    return False 
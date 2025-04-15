from chess5x5.game.board import Board, Color, Piece, PieceType

def evaluate_position(board: Board, color: Color) -> float:
    """
    Оценивает позицию на доске для заданного цвета.
    
    Args:
        board: Объект доски 5x5
        color: Цвет, за который оценивается позиция (WHITE или BLACK)
        
    Returns:
        float: Оценка позиции (положительное значение - преимущество, отрицательное - недостаток)
    """
    score = 0.0
    
    # Значения фигур
    piece_values = {
        PieceType.PAWN: 1.0,
        PieceType.ROOK: 5.0,
        PieceType.BISHOP: 3.0,
        PieceType.KING: 100.0
    }
    
    # Бонусы за позицию пешек
    pawn_position_bonus = [
        [0.0, 0.0, 0.0, 0.0, 0.0],
        [0.5, 0.5, 0.5, 0.5, 0.5],
        [0.2, 0.2, 0.3, 0.2, 0.2],
        [0.1, 0.1, 0.2, 0.1, 0.1],
        [0.0, 0.0, 0.0, 0.0, 0.0]
    ]
    
    # Бонус за контроль центра
    center_bonus = [
        [0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.2, 0.3, 0.2, 0.0],
        [0.0, 0.3, 0.5, 0.3, 0.0],
        [0.0, 0.2, 0.3, 0.2, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0]
    ]
    
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
                
                score += value * multiplier
    
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
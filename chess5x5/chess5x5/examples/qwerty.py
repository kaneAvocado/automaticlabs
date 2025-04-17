from chess5x5.game.board import Board, Color, PieceType

def evaluate_position(board: Board, color: Color) -> float:
    """
    Базовая функция оценки позиции.
    Учитывает:
    1. Материальное преимущество
    2. Позиционное преимущество (центр, безопасность короля)
    3. Мобильность фигур
    """
    score = 0.0
    
    # Значения фигур
    piece_values = {
        PieceType.PAWN: 1.0,
        PieceType.ROOK: 5.0,
        PieceType.BISHOP: 3.0,
        PieceType.KING: 100.0
    }
    
    # Бонусы за позицию (центр)
    center_bonus = [
        [0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.2, 0.2, 0.2, 0.0],
        [0.0, 0.0, 0.0, 0.2, 0.0],
        [0.0, 0.2, 0.2, 0.2, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0]
    ]
    
    # Бонусы за безопасность короля
    king_safety_bonus = [
        [0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.1, 0.1, 0.1, 0.0],
        [0.0, 0.1, 0.2, 0.1, 0.0],
        [0.0, 0.1, 0.1, 0.1, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0]
    ]
    
    for row in range(board.size):
        for col in range(board.size):
            piece = board.get_piece(row, col)
            if piece:
                # Базовое значение фигуры
                value = piece_values[piece.type]
                
                # Множитель в зависимости от цвета
                multiplier = 1.0 if piece.color == color else -1.0
                
                # Добавляем позиционные бонусы
                if piece.color == Color.WHITE:
                    value += center_bonus[row][col]
                    if piece.type == PieceType.KING:
                        value += king_safety_bonus[row][col]
                else:
                    value += center_bonus[board.size - 1 - row][col]
                    if piece.type == PieceType.KING:
                        value += king_safety_bonus[board.size - 1 - row][col]
                
                # Учитываем мобильность (количество возможных ходов)
                legal_moves = board.get_legal_moves(row, col)
                value += len(legal_moves) * 0.1
                
                score += value * multiplier
    
    return score 
from chess5x5.game.board import Board, Color, PieceType

def evaluate_position(board: Board, color: Color) -> float:
    """
    Улучшенная базовая функция оценки позиции.
    Учитывает:
    1. Материальное преимущество
    2. Позиционное преимущество (центр, безопасность короля)
    3. Мобильность фигур
    4. Структуру пешечного строя
    5. Координацию фигур
    6. Атакующий потенциал
    """
    score = 0.0
    
    # Базовые значения фигур
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
        [0.0, 0.2, 0.3, 0.2, 0.0],
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
    
    # Бонусы за атакующий потенциал
    attack_bonus = [
        [0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.1, 0.1, 0.1, 0.0],
        [0.0, 0.1, 0.2, 0.1, 0.0],
        [0.0, 0.1, 0.1, 0.1, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0]
    ]
    
    # Подсчет материала и позиционных бонусов
    for row in range(board.size):
        for col in range(board.size):
            piece = board.get_piece(row, col)
            if piece:
                # Базовое значение фигуры
                value = piece_values[piece.type]
                
                # Множитель в зависимости от цвета
                multiplier = 1.0 if piece.color == color else -1.0
                
                # Добавляем позиционные бонусы
                if piece.color == color:
                    # Бонус за центр
                    value += center_bonus[row][col]
                    
                    # Бонус за безопасность короля
                    if piece.type == PieceType.KING:
                        value += king_safety_bonus[row][col]
                    
                    # Бонус за атакующий потенциал
                    if piece.type in [PieceType.ROOK, PieceType.BISHOP]:
                        value += attack_bonus[row][col]
                
                score += value * multiplier
    
    # Оценка мобильности (количество возможных ходов)
    mobility_score = 0.0
    for row in range(board.size):
        for col in range(board.size):
            piece = board.get_piece(row, col)
            if piece and piece.color == color:
                moves = board.get_legal_moves(row, col)
                mobility_score += len(moves) * 0.1  # Бонус за каждый возможный ход
    
    # Оценка структуры пешечного строя
    pawn_structure_score = 0.0
    for col in range(board.size):
        pawn_count = 0
        for row in range(board.size):
            piece = board.get_piece(row, col)
            if piece and piece.type == PieceType.PAWN and piece.color == color:
                pawn_count += 1
                # Штраф за сдвоенные пешки
                if pawn_count > 1:
                    pawn_structure_score -= 0.5
                # Бонус за изолированные пешки
                elif pawn_count == 1:
                    pawn_structure_score += 0.3
    
    # Оценка координации фигур
    coordination_score = 0.0
    for row in range(board.size):
        for col in range(board.size):
            piece = board.get_piece(row, col)
            if piece and piece.color == color:
                # Проверяем защиту фигур
                for r in range(max(0, row-1), min(board.size, row+2)):
                    for c in range(max(0, col-1), min(board.size, col+2)):
                        if r != row or c != col:
                            defender = board.get_piece(r, c)
                            if defender and defender.color == color:
                                coordination_score += 0.2
    
    # Оценка безопасности короля
    king_safety_score = 0.0
    if board.is_king_under_attack(color):
        king_safety_score -= 2.0  # Штраф за атаку на короля
    
    # Комбинируем все оценки
    final_score = (
        score +                    # Материальное и позиционное преимущество
        mobility_score +           # Мобильность
        pawn_structure_score +     # Структура пешечного строя
        coordination_score +       # Координация фигур
        king_safety_score         # Безопасность короля
    )
    
    return final_score 
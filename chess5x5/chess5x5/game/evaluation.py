from typing import Dict
from .board import Board, Color, Piece, PieceType

class PositionEvaluator:
    def __init__(self):
        # Базовые значения фигур
        self.piece_values: Dict[PieceType, float] = {
            PieceType.PAWN: 1.0,
            PieceType.ROOK: 5.0,
            PieceType.BISHOP: 3.0,
            PieceType.KING: 100.0
        }
        
        # Бонусы за позицию (пример для пешек)
        self.pawn_position_bonus = [
            [0.0, 0.0, 0.0, 0.0, 0.0],
            [0.5, 0.5, 0.5, 0.5, 0.5],
            [0.2, 0.2, 0.3, 0.2, 0.2],
            [0.1, 0.1, 0.2, 0.1, 0.1],
            [0.0, 0.0, 0.0, 0.0, 0.0]
        ]
        
        # Бонус за контроль центра
        self.center_bonus = [
            [0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.2, 0.3, 0.2, 0.0],
            [0.0, 0.3, 0.5, 0.3, 0.0],
            [0.0, 0.2, 0.3, 0.2, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0]
        ]
    
    def evaluate_position(self, board: Board, color: Color) -> float:
        score = 0.0
        
        for row in range(board.size):
            for col in range(board.size):
                piece = board.get_piece(row, col)
                if piece:
                    # Базовое значение фигуры
                    value = self.piece_values[piece.type]
                    
                    # Множитель в зависимости от цвета
                    multiplier = 1.0 if piece.color == color else -1.0
                    
                    # Добавляем позиционный бонус для пешек
                    if piece.type == PieceType.PAWN:
                        if piece.color == Color.WHITE:
                            value += self.pawn_position_bonus[row][col]
                        else:
                            value += self.pawn_position_bonus[board.size - 1 - row][col]
                    
                    # Добавляем бонус за контроль центра
                    if piece.color == Color.WHITE:
                        value += self.center_bonus[row][col]
                    else:
                        value += self.center_bonus[board.size - 1 - row][col]
                    
                    score += value * multiplier
        
        return score

def create_evaluation_function() -> callable:
    evaluator = PositionEvaluator()
    return lambda board, color: evaluator.evaluate_position(board, color) 
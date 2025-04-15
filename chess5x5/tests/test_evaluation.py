import unittest
from chess5x5.game.board import Board, Color, Piece, PieceType
from chess5x5.game.evaluation import PositionEvaluator

class TestEvaluation(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.evaluator = PositionEvaluator()
        
    def test_material_value(self):
        """Проверка материального преимущества"""
        # Очищаем доску
        self.board.board = [[None for _ in range(5)] for _ in range(5)]
        
        # Добавляем фигуры
        self.board.board[0][0] = Piece(PieceType.KING, Color.WHITE)
        self.board.board[0][1] = Piece(PieceType.ROOK, Color.WHITE)
        self.board.board[0][2] = Piece(PieceType.BISHOP, Color.WHITE)
        self.board.board[0][3] = Piece(PieceType.PAWN, Color.WHITE)
        
        score = self.evaluator.evaluate_position(self.board, Color.WHITE)
        expected_score = 100.0 + 5.0 + 3.0 + 1.0  # Значения фигур
        self.assertAlmostEqual(score, expected_score, delta=0.1)
        
    def test_center_control(self):
        """Проверка бонуса за контроль центра"""
        # Очищаем доску
        self.board.board = [[None for _ in range(5)] for _ in range(5)]
        
        # Размещаем фигуру в центре
        self.board.board[2][2] = Piece(PieceType.ROOK, Color.WHITE)
        score = self.evaluator.evaluate_position(self.board, Color.WHITE)
        self.assertGreater(score, 5.0)  # Базовое значение ладьи + бонус за центр
        
    def test_pawn_advancement(self):
        """Проверка бонуса за продвинутые пешки"""
        # Очищаем доску
        self.board.board = [[None for _ in range(5)] for _ in range(5)]
        
        # Размещаем пешку на 3-й горизонтали
        self.board.board[2][0] = Piece(PieceType.PAWN, Color.WHITE)
        score = self.evaluator.evaluate_position(self.board, Color.WHITE)
        self.assertGreater(score, 1.0)  # Базовая стоимость пешки + бонус за продвижение
        
    def test_king_safety(self):
        """Проверка штрафа за небезопасность короля"""
        # Очищаем доску
        self.board.board = [[None for _ in range(5)] for _ in range(5)]
        
        # Размещаем короля под атакой
        self.board.board[0][0] = Piece(PieceType.KING, Color.WHITE)
        self.board.board[0][1] = Piece(PieceType.ROOK, Color.BLACK)
        score = self.evaluator.evaluate_position(self.board, Color.WHITE)
        self.assertLess(score, 100.0)  # Стоимость короля - штраф за атаку
        
    def test_initial_position(self):
        """Проверка оценки начальной позиции"""
        score = self.evaluator.evaluate_position(self.board, Color.WHITE)
        # В начальной позиции оценка должна быть близка к 0
        self.assertAlmostEqual(score, 0.0, delta=0.1)

if __name__ == '__main__':
    unittest.main() 
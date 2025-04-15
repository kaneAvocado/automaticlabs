from typing import Tuple, List, Callable, Optional
from .board import Board, Color, Piece

class AlphaBetaAI:
    def __init__(self, evaluation_function: Callable[[Board, Color], float]):
        self.evaluation_function = evaluation_function
    
    def get_best_move(self, board: Board, color: Color, depth: int = 4) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        # Получаем все возможные ходы
        moves = self._get_all_moves(board, color)
        
        for move in moves:
            # Делаем ход
            from_pos, to_pos = move
            captured_piece = board.get_piece(*to_pos)
            board.move_piece(from_pos, to_pos)
            
            # Рекурсивно оцениваем позицию
            value = -self._alpha_beta(board, -beta, -alpha, depth - 1, Color.BLACK if color == Color.WHITE else Color.WHITE)
            
            # Отменяем ход
            board.move_piece(to_pos, from_pos)
            if captured_piece:
                board.board[to_pos[0]][to_pos[1]] = captured_piece
            
            # Обновляем лучший ход
            if value > best_value:
                best_value = value
                best_move = move
            
            # Обновляем альфа
            alpha = max(alpha, value)
        
        return best_move
    
    def _alpha_beta(self, board: Board, alpha: float, beta: float, depth: int, color: Color) -> float:
        if depth == 0 or board.is_king_captured():
            return self.evaluation_function(board, color)
        
        moves = self._get_all_moves(board, color)
        
        if color == Color.WHITE:
            value = float('-inf')
            for move in moves:
                from_pos, to_pos = move
                captured_piece = board.get_piece(*to_pos)
                board.move_piece(from_pos, to_pos)
                
                value = max(value, self._alpha_beta(board, alpha, beta, depth - 1, Color.BLACK))
                
                board.move_piece(to_pos, from_pos)
                if captured_piece:
                    board.board[to_pos[0]][to_pos[1]] = captured_piece
                
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = float('inf')
            for move in moves:
                from_pos, to_pos = move
                captured_piece = board.get_piece(*to_pos)
                board.move_piece(from_pos, to_pos)
                
                value = min(value, self._alpha_beta(board, alpha, beta, depth - 1, Color.WHITE))
                
                board.move_piece(to_pos, from_pos)
                if captured_piece:
                    board.board[to_pos[0]][to_pos[1]] = captured_piece
                
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value
    
    def _get_all_moves(self, board: Board, color: Color) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        moves = []
        for row in range(board.size):
            for col in range(board.size):
                piece = board.get_piece(row, col)
                if piece and piece.color == color:
                    legal_moves = board.get_legal_moves(row, col)
                    moves.extend([((row, col), move) for move in legal_moves])
        return moves 
from typing import List, Tuple, Optional, Callable
from .board import Board, Color, PieceType
from .ai import AlphaBetaAI
from .evaluation import create_evaluation_function

class Game:
    def __init__(self, white_eval: Callable, black_eval: Callable):
        self.board = Board()
        self.white_eval = white_eval
        self.black_eval = black_eval
        self.moves = []
        self.move_history = []
        self.current_player = Color.WHITE
    
    def make_move(self) -> bool:
        if self.board.is_king_captured():
            return False
            
        eval_func = self.white_eval if self.current_player == Color.WHITE else self.black_eval
        best_move = None
        best_score = float('-inf')
        
        # Перебираем все возможные ходы
        for row in range(self.board.size):
            for col in range(self.board.size):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == self.current_player:
                    moves = self.board.get_legal_moves(row, col)
                    for move_row, move_col in moves:
                        # Сохраняем текущее состояние
                        original_piece = self.board.get_piece(move_row, move_col)
                        self.board.move_piece((row, col), (move_row, move_col))
                        
                        # Оцениваем позицию
                        score = eval_func(self.board, self.current_player)
                        if score > best_score:
                            best_score = score
                            best_move = ((row, col), (move_row, move_col))
                            
                        # Возвращаем доску в исходное состояние
                        self.board.move_piece((move_row, move_col), (row, col))
                        if original_piece:
                            self.board.board[move_row][move_col] = original_piece
        
        if best_move:
            from_pos, to_pos = best_move
            from_piece = self.board.get_piece(*from_pos)
            to_piece = self.board.get_piece(*to_pos)
            
            # Записываем ход в лог
            move_str = f"{'W' if self.current_player == Color.WHITE else 'B'}{from_piece.type.value if from_piece else '?'}"
            self.moves.append(move_str)
            
            # Выполняем ход
            self.board.move_piece(from_pos, to_pos)
            self.move_history.append(best_move)
            self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
            return True
            
        return False
    
    def play(self) -> List[str]:
        while self.make_move():
            pass
        return self.moves
    
    def _format_move(self, move: Tuple[Tuple[int, int], Tuple[int, int]], color: Color) -> str:
        """Форматирует ход в читаемый вид"""
        from_pos, to_pos = move
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Преобразуем координаты в шахматную нотацию
        col_names = ['a', 'b', 'c', 'd', 'e']
        row_names = ['5', '4', '3', '2', '1']
        
        from_square = f"{col_names[from_col]}{row_names[from_row]}"
        to_square = f"{col_names[to_col]}{row_names[to_row]}"
        
        # Получаем тип фигуры
        piece = self.board.get_piece(from_row, from_col)
        piece_type = piece.type.value if piece else "?"
        
        return f"{color.value}{piece_type}: {from_square} -> {to_square}"
    
    def play_game(self) -> Optional[Color]:
        """
        Играет полную партию и возвращает победителя (Color.WHITE или Color.BLACK)
        или None в случае ничьей
        """
        print("\n=== Начало новой партии ===")
        move_number = 1
        
        while not self.board.is_king_captured():
            # Ход белых
            best_move = None
            best_score = float('-inf')
            
            # Перебираем все возможные ходы белых
            for row in range(self.board.size):
                for col in range(self.board.size):
                    piece = self.board.get_piece(row, col)
                    if piece and piece.color == Color.WHITE:
                        moves = self.board.get_legal_moves(row, col)
                        for move_row, move_col in moves:
                            # Сохраняем текущее состояние
                            original_piece = self.board.get_piece(move_row, move_col)
                            self.board.move_piece((row, col), (move_row, move_col))
                            
                            # Оцениваем позицию
                            score = self.white_eval(self.board, Color.WHITE)
                            if score > best_score:
                                best_score = score
                                best_move = ((row, col), (move_row, move_col))
                                
                            # Возвращаем доску в исходное состояние
                            self.board.move_piece((move_row, move_col), (row, col))
                            if original_piece:
                                self.board.board[move_row][move_col] = original_piece
            
            if not best_move:
                print(f"\nЧерные победили (белые не могут сделать ход)")
                return Color.BLACK
                
            self._make_move(best_move)
            print(f"{move_number}. {self._format_move(best_move, Color.WHITE)}")
            
            if self.board.is_king_captured():
                print(f"\nБелые победили (мат)")
                return Color.WHITE
            
            # Ход черных
            best_move = None
            best_score = float('-inf')
            
            # Перебираем все возможные ходы черных
            for row in range(self.board.size):
                for col in range(self.board.size):
                    piece = self.board.get_piece(row, col)
                    if piece and piece.color == Color.BLACK:
                        moves = self.board.get_legal_moves(row, col)
                        for move_row, move_col in moves:
                            # Сохраняем текущее состояние
                            original_piece = self.board.get_piece(move_row, move_col)
                            self.board.move_piece((row, col), (move_row, move_col))
                            
                            # Оцениваем позицию
                            score = self.black_eval(self.board, Color.BLACK)
                            if score > best_score:
                                best_score = score
                                best_move = ((row, col), (move_row, move_col))
                                
                            # Возвращаем доску в исходное состояние
                            self.board.move_piece((move_row, move_col), (row, col))
                            if original_piece:
                                self.board.board[move_row][move_col] = original_piece
            
            if not best_move:
                print(f"\nБелые победили (черные не могут сделать ход)")
                return Color.WHITE
                
            self._make_move(best_move)
            print(f"{move_number}. {self._format_move(best_move, Color.BLACK)}")
            
            move_number += 1
        
        # Определяем победителя
        for row in range(self.board.size):
            for col in range(self.board.size):
                piece = self.board.get_piece(row, col)
                if piece and piece.type == PieceType.KING:
                    winner = piece.color
                    print(f"\n{winner.value} победили (мат)")
                    return winner
        
        print("\nНичья")
        return None
    
    def _make_move(self, move: Tuple[Tuple[int, int], Tuple[int, int]]):
        from_pos, to_pos = move
        self.board.move_piece(from_pos, to_pos)
        self.move_history.append(move)
    
    def get_move_history(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        return self.move_history.copy() 
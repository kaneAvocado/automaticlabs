from enum import Enum
from typing import List, Tuple, Optional

class PieceType(Enum):
    PAWN = "P"
    ROOK = "R"
    BISHOP = "B"
    KING = "K"
    

class Color(Enum):
    WHITE = "W"
    BLACK = "B"

class Piece:
    def __init__(self, piece_type: PieceType, color: Color):
        self.type = piece_type
        self.color = color

class Board:
    def __init__(self):
        self.size = 5
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
        self._initialize_board()
    
    def _initialize_board(self):
        # Инициализация начальной позиции
        # Белые фигуры
        self.board[4][0] = Piece(PieceType.ROOK, Color.WHITE)
        self.board[4][4] = Piece(PieceType.ROOK, Color.WHITE)
        self.board[4][1] = Piece(PieceType.BISHOP, Color.WHITE)
        self.board[4][3] = Piece(PieceType.BISHOP, Color.WHITE)
        self.board[4][2] = Piece(PieceType.KING, Color.WHITE)
        for i in range(5):
            self.board[3][i] = Piece(PieceType.PAWN, Color.WHITE)
        
        # Черные фигуры
        self.board[0][0] = Piece(PieceType.ROOK, Color.BLACK)
        self.board[0][4] = Piece(PieceType.ROOK, Color.BLACK)
        self.board[0][1] = Piece(PieceType.BISHOP, Color.BLACK)
        self.board[0][3] = Piece(PieceType.BISHOP, Color.BLACK)
        self.board[0][2] = Piece(PieceType.KING, Color.BLACK)
        for i in range(5):
            self.board[1][i] = Piece(PieceType.PAWN, Color.BLACK)
    
    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.board[row][col]
        return None
    
    def move_piece(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        piece = self.board[from_row][from_col]
        
        # Проверяем превращение пешки
        if piece and piece.type == PieceType.PAWN:
            if (piece.color == Color.WHITE and to_row == 0) or \
               (piece.color == Color.BLACK and to_row == self.size - 1):
                # Превращаем пешку в ладью
                self.board[to_row][to_col] = Piece(PieceType.ROOK, piece.color)
            else:
                self.board[to_row][to_col] = piece
        else:
            self.board[to_row][to_col] = piece
            
        self.board[from_row][from_col] = None
    
    def is_king_under_attack(self, color: Color) -> bool:
        # Находим позицию короля
        king_pos = None
        for row in range(self.size):
            for col in range(self.size):
                piece = self.board[row][col]
                if piece and piece.type == PieceType.KING and piece.color == color:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False
            
        # Проверяем атаки всех фигур противника
        for row in range(self.size):
            for col in range(self.size):
                piece = self.board[row][col]
                if piece and piece.color != color:
                    moves = self.get_legal_moves(row, col)
                    if king_pos in moves:
                        return True
        return False

    def is_king_captured(self) -> bool:
        white_king = False
        black_king = False
        
        # Проверяем наличие королей
        for row in range(self.size):
            for col in range(self.size):
                piece = self.board[row][col]
                if piece and piece.type == PieceType.KING:
                    if piece.color == Color.WHITE:
                        white_king = True
                    else:
                        black_king = True
        
        # Если хотя бы один король отсутствует
        return not white_king or not black_king
    
    def get_legal_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        piece = self.get_piece(row, col)
        if not piece:
            return []
        
        moves = []
        if piece.type == PieceType.PAWN:
            direction = -1 if piece.color == Color.WHITE else 1
            # Ход вперед
            if 0 <= row + direction < self.size:
                if not self.get_piece(row + direction, col):
                    moves.append((row + direction, col))
                    # Двойной ход с начальной позиции
                    if (piece.color == Color.WHITE and row == 3) or \
                       (piece.color == Color.BLACK and row == 1):
                        if not self.get_piece(row + 2 * direction, col):
                            moves.append((row + 2 * direction, col))
                # Взятие по диагонали
                for dcol in [-1, 1]:
                    if 0 <= col + dcol < self.size:
                        target = self.get_piece(row + direction, col + dcol)
                        if target and target.color != piece.color:
                            moves.append((row + direction, col + dcol))
        
        elif piece.type == PieceType.ROOK:
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for drow, dcol in directions:
                current_row, current_col = row + drow, col + dcol
                while 0 <= current_row < self.size and 0 <= current_col < self.size:
                    target = self.get_piece(current_row, current_col)
                    if target:
                        if target.color != piece.color:
                            moves.append((current_row, current_col))
                        break
                    moves.append((current_row, current_col))
                    current_row += drow
                    current_col += dcol
        
        elif piece.type == PieceType.BISHOP:
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for drow, dcol in directions:
                current_row, current_col = row + drow, col + dcol
                while 0 <= current_row < self.size and 0 <= current_col < self.size:
                    target = self.get_piece(current_row, current_col)
                    if target:
                        if target.color != piece.color:
                            moves.append((current_row, current_col))
                        break
                    moves.append((current_row, current_col))
                    current_row += drow
                    current_col += dcol
        
        elif piece.type == PieceType.KING:
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0),
                         (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for drow, dcol in directions:
                new_row, new_col = row + drow, col + dcol
                if 0 <= new_row < self.size and 0 <= new_col < self.size:
                    target = self.get_piece(new_row, new_col)
                    if not target or target.color != piece.color:
                        moves.append((new_row, new_col))
        
        return moves 
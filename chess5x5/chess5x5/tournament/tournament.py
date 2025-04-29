from typing import List, Dict, Tuple, Callable
from ..game.game import Game
from ..game.board import Color

class Tournament:
    def __init__(self, participants: List[Tuple[str, Callable]]):
        """
        Инициализация турнира
        participants: список кортежей (имя_участника, функция_оценки)
        """
        self.participants = participants
        self.scores: Dict[str, float] = {name: 0.0 for name, _ in participants}
        self.matches_played: Dict[str, int] = {name: 0 for name, _ in participants}
    
    def play_tournament(self) -> List[Tuple[str, float]]:
        """
        Проводит круговой турнир и возвращает отсортированный список результатов
        """
        n = len(self.participants)
        total_matches = n * (n - 1)  # Каждый с каждым дважды
        current_match = 0
        
        print(f"\n=== Начало турнира ===")
        print(f"Участников: {n}")
        print(f"Всего матчей: {total_matches}")
        print("=" * 50)
        
        # Каждый участник играет с каждым дважды
        for i in range(n):
            for j in range(n):
                if i != j:
                    current_match += 1
                    print(f"\nМатч {current_match}/{total_matches}")
                    print(f"{self.participants[i][0]} (белые) vs {self.participants[j][0]} (черные)")
                    self._play_match(
                        self.participants[i][0], self.participants[i][1],
                        self.participants[j][0], self.participants[j][1],
                        Color.WHITE
                    )
        
        print("\n=== Итоги турнира ===")
        results = sorted(
            [(name, score) for name, score in self.scores.items()],
            key=lambda x: x[1],
            reverse=True
        )
        
        for i, (name, score) in enumerate(results, 1):
            print(f"{i}. {name}: {score} очков")
        
        return results
    
    def _play_match(self, player1_name: str, player1_eval: Callable,
                   player2_name: str, player2_eval: Callable,
                   first_player_color: Color):
        """
        Проводит матч между двумя участниками
        """
        game = Game(
            white_eval=player1_eval if first_player_color == Color.WHITE else player2_eval,
            black_eval=player2_eval if first_player_color == Color.WHITE else player1_eval
        )
        
        winner = game.play_game()
        
        # Обновляем статистику
        self.matches_played[player1_name] += 1
        self.matches_played[player2_name] += 1
        
        if winner is None:
            # Ничья
            self.scores[player1_name] += 0.5
            self.scores[player2_name] += 0.5
            print(f"Результат: Ничья")
        elif winner == first_player_color:
            # Победа первого игрока
            self.scores[player1_name] += 1.0
            print(f"Результат: Победа {player1_name}")
        else:
            # Победа второго игрока
            self.scores[player2_name] += 1.0
            print(f"Результат: Победа {player2_name}")
    
    def get_statistics(self) -> Dict[str, Dict[str, float]]:
        """
        Возвращает статистику турнира
        """
        return {
            name: {
                "score": score,
                "matches_played": self.matches_played[name],
                "win_rate": score / self.matches_played[name] if self.matches_played[name] > 0 else 0
            }
            for name, score in self.scores.items()
        } 
import os
import sys
import importlib.util
import traceback
from typing import List, Tuple, Dict, Any
from pathlib import Path

from .game.board import Board, Color
from .game.game import Game
from .tournament.tournament import Tournament

class DebugTournament:
    def __init__(self):
        self.examples_dir = Path(__file__).parent.parent / "examples"
        self.participants: List[Tuple[str, Any]] = []
        self.errors: List[Dict[str, str]] = []
        
    def load_evaluation_functions(self) -> None:
        """Загружает все функции оценки из директории examples"""
        print("\n=== Загрузка функций оценки ===")
        
        for file in self.examples_dir.glob("*.py"):
            if file.name.startswith("_"):
                continue
                
            try:
                # Загружаем модуль
                spec = importlib.util.spec_from_file_location(file.stem, file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Проверяем наличие функции evaluate_position
                if hasattr(module, "evaluate_position"):
                    self.participants.append((file.stem, module.evaluate_position))
                    print(f"✓ Загружена функция оценки из {file.name}")
                else:
                    self.errors.append({
                        "file": file.name,
                        "error": "Функция evaluate_position не найдена"
                    })
                    print(f"✗ Ошибка в {file.name}: функция evaluate_position не найдена")
                    
            except Exception as e:
                self.errors.append({
                    "file": file.name,
                    "error": str(e),
                    "traceback": traceback.format_exc()
                })
                print(f"✗ Ошибка при загрузке {file.name}: {str(e)}")
    
    def run_tournament(self) -> None:
        """Запускает турнир и обрабатывает ошибки"""
        if not self.participants:
            print("\nНет участников для турнира")
            return
            
        print("\n=== Запуск турнира ===")
        try:
            tournament = Tournament(self.participants)
            results = tournament.play_tournament()
            
            print("\n=== Результаты турнира ===")
            for i, (name, score) in enumerate(results, 1):
                print(f"{i}. {name}: {score} очков")
                
        except Exception as e:
            self.errors.append({
                "context": "Проведение турнира",
                "error": str(e),
                "traceback": traceback.format_exc()
            })
            print(f"\n✗ Ошибка при проведении турнира: {str(e)}")
    
    def run_tests(self) -> None:
        """Запускает тесты для каждой функции оценки"""
        print("\n=== Запуск тестов ===")
        board = Board()
        
        for name, eval_func in self.participants:
            try:
                # Проверяем базовую функциональность
                score = eval_func(board, Color.WHITE)
                if not isinstance(score, (int, float)):
                    raise ValueError(f"Функция вернула не числовой результат: {type(score)}")
                    
                # Проверяем работу с разными цветами
                score_black = eval_func(board, Color.BLACK)
                if not isinstance(score_black, (int, float)):
                    raise ValueError(f"Функция вернула не числовой результат для черных: {type(score_black)}")
                    
                print(f"✓ Тесты пройдены для {name}")
                
            except Exception as e:
                self.errors.append({
                    "participant": name,
                    "error": str(e),
                    "traceback": traceback.format_exc()
                })
                print(f"✗ Ошибка в тестах для {name}: {str(e)}")
    
    def print_errors(self) -> None:
        """Выводит все найденные ошибки"""
        if not self.errors:
            print("\n✓ Ошибок не найдено")
            return
            
        print("\n=== Найденные ошибки ===")
        for i, error in enumerate(self.errors, 1):
            print(f"\nОшибка #{i}:")
            for key, value in error.items():
                if key != "traceback":
                    print(f"{key}: {value}")
            if "traceback" in error:
                print("\nТрассировка:")
                print(error["traceback"])

def main():
    debugger = DebugTournament()
    
    # Загружаем функции оценки
    debugger.load_evaluation_functions()
    
    # Запускаем тесты
    debugger.run_tests()
    
    # Проводим турнир
    debugger.run_tournament()
    
    # Выводим ошибки
    debugger.print_errors()

if __name__ == "__main__":
    main() 
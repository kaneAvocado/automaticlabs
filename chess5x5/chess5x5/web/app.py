from flask import Flask, render_template, request, jsonify, send_file
import importlib.util
import sys
import os
import csv
import io
from datetime import datetime
from chess5x5.game.board import Board, Color
from chess5x5.tournament.tournament import Tournament

app = Flask(__name__)

# Глобальные переменные
participants = []
tournament_results = None
tournament_statistics = None

@app.route('/')
def index():
    return render_template('index.html', participants=participants)

@app.route('/upload', methods=['POST'])
def upload_evaluation():
    if 'files' not in request.files:
        return jsonify({'error': 'Файлы не загружены'}), 400
    
    files = request.files.getlist('files')
    if not files:
        return jsonify({'error': 'Файлы не выбраны'}), 400
    
    successful_uploads = 0
    errors = []
    
    for file in files:
        if file.filename == '':
            errors.append(f'Пустой файл')
            continue
        
        if not file.filename.endswith('.py'):
            errors.append(f'Файл {file.filename} должен иметь расширение .py')
            continue
        
        try:
            # Сохраняем файл временно
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(temp_path)
            
            # Загружаем модуль
            spec = importlib.util.spec_from_file_location("evaluation_module", temp_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Проверяем наличие функции evaluate_position
            if not hasattr(module, 'evaluate_position'):
                errors.append(f'Функция evaluate_position не найдена в файле {file.filename}')
                os.remove(temp_path)
                continue
            
            # Проверяем корректность функции
            test_board = Board()
            try:
                module.evaluate_position(test_board, Color.WHITE)
            except Exception as e:
                errors.append(f'Ошибка в функции evaluate_position в файле {file.filename}: {str(e)}')
                os.remove(temp_path)
                continue
            
            # Добавляем участника
            participant_name = os.path.splitext(file.filename)[0]
            participants.append((participant_name, module.evaluate_position))
            
            # Удаляем временный файл
            os.remove(temp_path)
            successful_uploads += 1
            
        except Exception as e:
            errors.append(f'Ошибка при загрузке файла {file.filename}: {str(e)}')
            continue
    
    if successful_uploads > 0:
        message = f'Успешно загружено {successful_uploads} файлов'
        if errors:
            message += f'. Ошибки: {", ".join(errors)}'
        return jsonify({'message': message})
    else:
        return jsonify({'error': 'Не удалось загрузить ни один файл. Ошибки: ' + ', '.join(errors)}), 400

@app.route('/start_tournament', methods=['POST'])
def start_tournament():
    global tournament_results, tournament_statistics
    
    if len(participants) < 2:
        return jsonify({'error': 'Недостаточно участников для турнира'}), 400
    
    try:
        tournament = Tournament(participants)
        tournament_results = tournament.play_tournament()
        tournament_statistics = tournament.get_statistics()
        
        return jsonify({
            'results': tournament_results,
            'statistics': tournament_statistics
        })
    
    except Exception as e:
        return jsonify({'error': f'Ошибка при проведении турнира: {str(e)}'}), 500

@app.route('/download_results', methods=['GET'])
def download_results():
    if not tournament_results:
        return jsonify({'error': 'Турнир еще не проведен'}), 400
    
    # Создаем CSV файл в памяти
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Записываем заголовок
    writer.writerow(['Место', 'Участник', 'Очки', 'Сыграно матчей', 'Процент побед'])
    
    # Записываем данные
    for i, (name, score) in enumerate(tournament_results, 1):
        stats = tournament_statistics[name]
        writer.writerow([
            i,
            name,
            f"{score:.1f}",
            stats['matches_played'],
            f"{stats['win_rate']*100:.1f}%"
        ])
    
    # Создаем файл для скачивания
    output.seek(0)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'tournament_results_{timestamp}.csv'
    )

if __name__ == '__main__':
    # Создаем директорию для загруженных файлов
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    app.run(debug=True) 
import os
import sys
import json
from datetime import datetime

# Добавляем путь к корневой директории проекта
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from flask import Flask, render_template, request, send_file
import pandas as pd
from robotlib.robot import Robot
import tempfile
import importlib.util

app = Flask(__name__)
# Используем абсолютный путь к папке uploads
app.config['UPLOAD_FOLDER'] = os.path.join(project_root, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['RESULTS_FILE'] = os.path.join(project_root, 'uploads', 'results.json')

# Создаем папку для загрузок, если она не существует
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Загружаем сохраненные результаты, если они есть
def load_results():
    if os.path.exists(app.config['RESULTS_FILE']):
        with open(app.config['RESULTS_FILE'], 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'uploaded_files': [], 'test_results': []}

# Сохраняем результаты в файл
def save_results(uploaded_files, test_results):
    with open(app.config['RESULTS_FILE'], 'w', encoding='utf-8') as f:
        json.dump({
            'uploaded_files': uploaded_files,
            'test_results': test_results
        }, f, ensure_ascii=False, indent=2)

# Загружаем начальные результаты
saved_results = load_results()
uploaded_files = saved_results['uploaded_files']
test_results = saved_results['test_results']

def format_file_size(size):
    """Форматирует размер файла в читаемый вид"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

@app.route('/', methods=['GET', 'POST'])
def index():
    global uploaded_files, test_results
    
    if request.method == 'POST':
        # Очищаем предыдущие результаты
        uploaded_files = []
        test_results = []
        
        # Получаем список загруженных файлов
        files = request.files.getlist('files')
        
        for file in files:
            if file.filename:
                # Сохраняем файл
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                
                # Запускаем тест для файла
                result = run_test(filepath)
                if result:
                    test_results.append(result)
                
                # Добавляем информацию о файле
                uploaded_files.append({
                    'name': file.filename,
                    'size': format_file_size(os.path.getsize(filepath)),
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'status': 'Успешно' if result else 'Ошибка'
                })
        
        # Сохраняем результаты после обработки всех файлов
        save_results(uploaded_files, test_results)
    
    return render_template('index.html', uploaded_files=uploaded_files, results=test_results)

def run_test(filepath):
    """Запускает тест для указанного файла"""
    try:
        # Импортируем модуль из загруженного файла
        import importlib.util
        spec = importlib.util.spec_from_file_location("test_module", filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Запускаем тест
        result = module.test_autonomous_filling()
        if result:
            # Добавляем имя файла к результатам
            result['filename'] = os.path.basename(filepath)
            # Добавляем информацию о штрафных шагах
            result['penalty_steps'] = result.get('penalty_steps', 0)
            result['total_steps'] = result['steps'] + result['penalty_steps']
        return result
    except Exception as e:
        print(f"Ошибка при выполнении теста: {e}")
        return None

@app.route('/download')
def download():
    """Скачивание результатов в формате CSV"""
    try:
        if not test_results:
            return "Нет результатов для скачивания", 404
            
        # Создаем CSV файл с результатами
        csv_content = "Имя,Фамилия,Шаги,Штрафные шаги,Общее количество шагов,Файл\n"
        for result in test_results:
            csv_content += f"{result['name']},{result['surname']},{result['steps']},{result['penalty_steps']},{result['total_steps']},{result['filename']}\n"
        
        # Сохраняем CSV файл
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'results.csv')
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        
        # Отправляем файл для скачивания
        return send_file(
            csv_path,
            mimetype='text/csv',
            as_attachment=True,
            download_name='results.csv'
        )
    except Exception as e:
        print(f"Ошибка при создании CSV файла: {e}")
        return "Ошибка при создании файла результатов", 500

if __name__ == '__main__':
    app.run(debug=True) 
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в PYTHONPATH
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from chess5x5.chess5x5.web.app import app

if __name__ == '__main__':
    app.run(debug=True) 
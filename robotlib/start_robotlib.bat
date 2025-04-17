@echo off
echo Установка зависимостей...
pip install -r requirements.txt

# Перейдите в корневую директорию проекта
cd D:\Programs\automaticlabs-master\automaticlabs

# Установите пакет в режиме разработки
pip install -e robotlib

# Запустите приложение
python robotlib/web/app.py

pause 
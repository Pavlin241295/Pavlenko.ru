@echo off
chcp 65001 >nul
echo ============================================
echo OCR Scanner Online - Установка
echo ============================================
echo.
echo Эта версия работает БEЗ Tesseract!
echo Используется онлайн OCR API.
echo.
echo --------------------------------------------
echo.
echo Устанавливаю зависимости...
echo.
pip install -r requirements.txt
echo.
echo ============================================
echo Готово! Запуск программы...
echo ============================================
python ocr_online.py
pause

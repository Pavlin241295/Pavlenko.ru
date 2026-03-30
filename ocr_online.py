import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image
import os
import sys
import tempfile
import webbrowser
import requests
from deep_translator import GoogleTranslator

class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📸 OCR Scanner - Online (Без Tesseract)")
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        self.root.configure(bg='#1e1e2e')
        
        # Цветовая схема
        self.colors = {
            'bg': '#1e1e2e',
            'bg_secondary': '#2a2a3e',
            'text': '#ffffff',
            'text_secondary': '#a0a0b0',
            'accent_green': '#4CAF50',
            'accent_blue': '#2196F3',
            'accent_orange': '#FF9800',
            'accent_red': '#f44336',
            'border': '#3a3a5e'
        }
        
        # Стиль кнопок
        self.btn_style = {
            'font': ('Segoe UI', 11, 'bold'),
            'fg': '#ffffff',
            'padx': 25,
            'pady': 12,
            'relief': 'flat',
            'cursor': 'hand2'
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Заголовок
        header_frame = tk.Frame(self.root, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        title_label = tk.Label(
            header_frame,
            text="📸 OCR Scanner - Online",
            font=('Segoe UI', 18, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Распознавание текста через онлайн API (НЕ нужен Tesseract!)",
            font=('Segoe UI', 9),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg']
        )
        subtitle_label.pack(side=tk.LEFT, padx=15, pady=5)
        
        # Кнопка сайта
        self.btn_website = tk.Button(
            header_frame,
            text="🌐 GitHub",
            command=self.open_website,
            font=('Segoe UI', 9, 'bold'),
            bg='#24292e',
            fg='#ffffff',
            padx=15,
            pady=5,
            relief='flat',
            cursor='hand2'
        )
        self.btn_website.pack(side=tk.RIGHT)
        
        # Фрейм для кнопок
        button_frame = tk.Frame(self.root, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Кнопка выбора файла
        self.btn_select = tk.Button(
            button_frame, 
            text="📁 Выбрать файл", 
            command=self.select_image,
            bg=self.colors['accent_green'],
            **self.btn_style
        )
        self.btn_select.pack(side=tk.LEFT, padx=(0, 10))
        
        # Разделитель
        separator = tk.Frame(button_frame, bg=self.colors['border'], height=2)
        separator.pack(side=tk.LEFT, padx=20, fill=tk.Y)
        
        # Кнопка вставки
        self.btn_paste = tk.Button(
            button_frame,
            text="📥 Вставить",
            command=self.paste_text,
            bg='#00BCD4',
            **self.btn_style
        )
        self.btn_paste.pack(side=tk.LEFT, padx=5)
        
        # Вторая строка с переводом
        translate_frame = tk.Frame(self.root, bg=self.colors['bg'])
        translate_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Первый столбик - язык оригинала
        from_lang_frame = tk.Frame(translate_frame, bg=self.colors['bg'])
        from_lang_frame.pack(side=tk.LEFT, padx=10)
        
        from_label = tk.Label(
            from_lang_frame,
            text="📖 С языка:",
            font=('Segoe UI', 10, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        from_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.from_lang_var = tk.StringVar(value='Авто')
        self.from_lang_dropdown = tk.OptionMenu(
            from_lang_frame,
            self.from_lang_var,
            'Авто', 'Русский', 'English', 'Español', 'Français', 'Deutsch',
            'Italiano', 'Polski', 'Türkçe', '中文', '日本語', '한국어'
        )
        self.from_lang_dropdown.config(
            font=('Segoe UI', 10, 'bold'),
            bg='#3a3a5e',
            fg='#ffffff',
            activebackground=self.colors['accent_blue'],
            activeforeground='#ffffff',
            relief='raised',
            bd=2,
            cursor='hand2',
            width=8
        )
        self.from_lang_dropdown['menu'].config(
            bg='#2a2a3e',
            fg='#ffffff',
            activebackground=self.colors['accent_blue'],
            activeforeground='#ffffff',
            font=('Segoe UI', 10)
        )
        self.from_lang_dropdown.pack(side=tk.LEFT)
        
        # Кнопка перевода
        self.btn_translate = tk.Button(
            translate_frame,
            text="🌐 Перевести",
            command=self.translate_current_text,
            bg='#9C27B0',
            **self.btn_style
        )
        self.btn_translate.pack(side=tk.LEFT, padx=15)
        
        # Второй столбик - язык перевода
        to_lang_frame = tk.Frame(translate_frame, bg=self.colors['bg'])
        to_lang_frame.pack(side=tk.LEFT, padx=10)
        
        to_label = tk.Label(
            to_lang_frame,
            text="📗 На язык:",
            font=('Segoe UI', 10, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        to_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.to_lang_var = tk.StringVar(value='Русский')
        self.to_lang_dropdown = tk.OptionMenu(
            to_lang_frame,
            self.to_lang_var,
            'Русский', 'English', 'Español', 'Français', 'Deutsch',
            'Italiano', 'Polski', 'Türkçe', '中文', '日本語', '한국어'
        )
        self.to_lang_dropdown.config(
            font=('Segoe UI', 10, 'bold'),
            bg='#3a3a5e',
            fg='#ffffff',
            activebackground=self.colors['accent_blue'],
            activeforeground='#ffffff',
            relief='raised',
            bd=2,
            cursor='hand2',
            width=8
        )
        self.to_lang_dropdown['menu'].config(
            bg='#2a2a3e',
            fg='#ffffff',
            activebackground=self.colors['accent_blue'],
            activeforeground='#ffffff',
            font=('Segoe UI', 10)
        )
        self.to_lang_dropdown.pack(side=tk.LEFT)
        
        # Переключатель перевода
        self.translate_enabled = tk.BooleanVar(value=True)
        self.translate_check = tk.Checkbutton(
            translate_frame,
            text="✅ Перевод",
            variable=self.translate_enabled,
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            selectcolor=self.colors['bg_secondary'],
            activebackground=self.colors['bg'],
            activeforeground=self.colors['text'],
            cursor='hand2'
        )
        self.translate_check.pack(side=tk.LEFT, padx=10)
        
        # Статус бар
        status_frame = tk.Frame(self.root, bg=self.colors['bg_secondary'])
        status_frame.pack(fill=tk.X, padx=20, pady=(10, 5))
        
        self.status_label = tk.Label(
            status_frame,
            text="Готов к работе",
            font=('Segoe UI', 9),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary'],
            anchor='w'
        )
        self.status_label.pack(fill=tk.X, padx=15, pady=8)
        
        # Фрейм для текстового поля с рамкой
        text_container = tk.Frame(self.root, bg=self.colors['border'])
        text_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Текстовое поле для результата
        self.text_area = scrolledtext.ScrolledText(
            text_container,
            font=('Consolas', 12),
            wrap=tk.WORD,
            bg='#2a2a3e',
            fg='#ffffff',
            insertbackground='#ffffff',
            selectbackground='#4a4a6e',
            selectforeground='#ffffff',
            relief='flat',
            padx=15,
            pady=15,
            borderwidth=0
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Контекстное меню для текстового поля
        self.context_menu = tk.Menu(self.root, tearoff=0, bg='#2a2a3e', fg='#ffffff')
        self.context_menu.add_command(label="📋 Копировать", command=self.copy_text)
        self.context_menu.add_command(label="📥 Вставить", command=self.paste_text)
        
        # Привязка правой кнопки мыши
        self.text_area.bind("<Button-3>", self.show_context_menu)
        
        # Настройка скроллбара
        scrollbar = tk.Scrollbar(
            text_container,
            orient=tk.VERTICAL,
            command=self.text_area.yview,
            bg=self.colors['bg_secondary'],
            activebackground=self.colors['accent_blue']
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 1), pady=1)
        self.text_area.config(yscrollcommand=scrollbar.set)
        
        # Инфо-панель внизу
        info_frame = tk.Frame(self.root, bg=self.colors['bg'])
        info_frame.pack(fill=tk.X, padx=20, pady=(5, 15))
        
        info_label = tk.Label(
            info_frame,
            text="Форматы: PNG, JPG, JPEG, BMP, GIF, TIFF, WEBP  |  🌐 Онлайн OCR - Tesseract НЕ НУЖЕН!",
            font=('Segoe UI', 8),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg']
        )
        info_label.pack()
        
        self.current_file = None
        
        # Словарь кодов языков
        self.lang_codes = {
            'Авто': 'auto',
            'Русский': 'ru',
            'English': 'en',
            'Español': 'es',
            'Français': 'fr',
            'Deutsch': 'de',
            'Italiano': 'it',
            'Polski': 'pl',
            'Türkçe': 'tr',
            '中文': 'zh-cn',
            '日本語': 'ja',
            '한국어': 'ko'
        }
        
    def open_website(self):
        """Открытие сайта в браузере"""
        webbrowser.open('https://github.com/Pavlin241295/Pavlenko.ru.git')
        
    def show_context_menu(self, event):
        """Показ контекстного меню"""
        self.context_menu.post(event.x_root, event.y_root)
    
    def ocr_online(self, image_path):
        """Онлайн OCR через API"""
        try:
            # Используем бесплатный API для OCR
            # OCR.Space API (бесплатно до 25000 запросов в месяц)
            api_key = "helloworld"  # Бесплатный API ключ для демонстрации
            
            with open(image_path, 'rb') as f:
                files = {'file': f}
                data = {
                    'apikey': api_key,
                    'language': 'rus+eng',
                    'isOverlayRequired': 'false',
                    'filetype': os.path.splitext(image_path)[1][1:]
                }
                
                response = requests.post(
                    'https://api.ocr.space/parse/image',
                    files=files,
                    data=data
                )
                
                result = response.json()
                
                if result.get('IsErroredOnPage', True):
                    return result.get('ErrorMessage', 'Ошибка OCR')
                
                text = result.get('ParsedResults', [{}])[0].get('ParsedText', '')
                return text
                
        except Exception as e:
            # Если API не работает, пробуем альтернативный метод
            return f"Ошибка онлайн OCR: {str(e)}\n\nПопробуйте другое изображение или проверьте интернет."
    
    def translate_text(self, text, source='auto', target='ru'):
        """Перевод текста"""
        try:
            translator = GoogleTranslator(source=source, target=target)
            return translator.translate(text)
        except Exception as e:
            print(f"Ошибка перевода: {e}")
            return None
    
    def translate_current_text(self):
        """Перевод текущего текста в поле"""
        text = self.text_area.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning("Внимание", "Нет текста для перевода!")
            return
        
        # Если текст уже содержит перевод, извлекаем оригинал
        if "=== Оригинал ===" in text and "=== Перевод" in text:
            parts = text.split("=== Перевод")
            original_part = parts[0].replace("=== Оригинал ===", "").strip()
            lines = original_part.split('\n')
            original = '\n'.join(lines).strip()
        else:
            original = text
        
        # Получаем выбранные языки
        from_lang = self.from_lang_var.get()
        to_lang = self.to_lang_var.get()
        
        from_code = self.lang_codes.get(from_lang, 'auto')
        to_code = self.lang_codes.get(to_lang, 'ru')
        
        self.status_label.config(text=f"⏳ Перевод с {from_lang} на {to_lang}...")
        self.root.update()
        
        translated = self.translate_text(original, from_code, to_code)
        
        if translated and translated.strip():
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, f"=== Оригинал ({from_lang}) ===\n{original}\n\n=== Перевод ({to_lang}) ===\n{translated}")
            self.status_label.config(text=f"✓ Перевод выполнен")
        else:
            self.status_label.config(text="❌ Ошибка перевода")
            messagebox.showerror("Ошибка", "Не удалось перевести текст.\nПроверьте подключение к интернету.")
        
    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[
                ("Изображения", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp"),
                ("Все файлы", "*.*")
            ]
        )
        
        if file_path:
            self.current_file = file_path
            filename = os.path.basename(file_path)
            self.status_label.config(text=f"⏳ Обработка: {filename}...")
            self.root.update()
            
            try:
                # Онлайн OCR без Tesseract
                self.status_label.config(text="⏳ Онлайн распознавание...")
                self.root.update()
                text = self.ocr_online(file_path)
                
                # Проверка включен ли перевод
                if self.translate_enabled.get():
                    # Автоматический перевод на выбранный язык
                    to_lang = self.to_lang_var.get()
                    to_code = self.lang_codes[to_lang]
                    
                    self.status_label.config(text=f"⏳ Перевод на {to_lang}...")
                    self.root.update()
                    translated = self.translate_text(text, 'auto', to_code)
                    
                    if translated and translated.strip():
                        self.text_area.delete(1.0, tk.END)
                        self.text_area.insert(1.0, f"=== Оригинал ===\n{text}\n\n=== Перевод ({to_lang}) ===\n{translated}")
                        self.status_label.config(text=f"✓ Готово: {filename}")
                    else:
                        self.text_area.delete(1.0, tk.END)
                        self.text_area.insert(1.0, text)
                        self.status_label.config(text=f"✓ Распознано: {filename}")
                else:
                    # Перевод отключен - только распознавание
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, text)
                    self.status_label.config(text=f"✓ Распознано: {filename} (перевод выкл)")
                
            except Exception as e:
                self.status_label.config(text="❌ Ошибка!")
                messagebox.showerror("Ошибка", f"Не удалось распознать текст:\n{str(e)}")
    
    def copy_text(self):
        text = self.text_area.get(1.0, tk.END).strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.status_label.config(text="✓ Текст скопирован в буфер обмена")
        else:
            messagebox.showwarning("Внимание", "Нет текста для копирования!")
    
    def paste_text(self):
        """Вставка текста из буфера обмена"""
        try:
            text = self.root.clipboard_get()
            if text:
                self.text_area.insert(tk.END, text)
                self.status_label.config(text="✓ Текст вставлен из буфера обмена")
        except tk.TclError:
            messagebox.showwarning("Внимание", "Буфер обмена пуст!")

if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()

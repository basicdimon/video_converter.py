#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Пакетный конвертер видео в MP3
Автор: basic-dimon
Описание: GUI приложение для конвертации множественных видео файлов в аудио формат MP3
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
from pathlib import Path
# moviepy будет импортироваться при необходимости

class VideoToMP3Converter:
    def __init__(self, root):
        self.root = root
        self.root.title("Пакетный конвертер видео в MP3")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Переменные
        self.video_files = []
        self.output_folder = tk.StringVar()
        self.is_converting = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Создание пользовательского интерфейса"""
        # Главный фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Пакетный конвертер видео в MP3", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Секция выбора файлов
        files_frame = ttk.LabelFrame(main_frame, text="Выбор видео файлов", padding="10")
        files_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        files_frame.columnconfigure(0, weight=1)
        
        # Кнопки для работы с файлами
        buttons_frame = ttk.Frame(files_frame)
        buttons_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(buttons_frame, text="Добавить файлы", 
                  command=self.add_files).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Очистить список", 
                  command=self.clear_files).pack(side=tk.LEFT, padx=(0, 10))
        
        # Список файлов
        list_frame = ttk.Frame(files_frame)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        self.files_listbox = tk.Listbox(list_frame, height=8)
        self.files_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Скроллбар для списка
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.files_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.files_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Секция выбора папки вывода
        output_frame = ttk.LabelFrame(main_frame, text="Папка для сохранения MP3", padding="10")
        output_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Папка:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Entry(output_frame, textvariable=self.output_folder, state="readonly").grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(output_frame, text="Выбрать", 
                  command=self.select_output_folder).grid(row=0, column=2)
        
        # Секция настроек качества
        quality_frame = ttk.LabelFrame(main_frame, text="Настройки качества", padding="10")
        quality_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(quality_frame, text="Битрейт:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.bitrate_var = tk.StringVar(value="192k")
        bitrate_combo = ttk.Combobox(quality_frame, textvariable=self.bitrate_var, 
                                   values=["128k", "192k", "256k", "320k"], state="readonly")
        bitrate_combo.grid(row=0, column=1, sticky=tk.W)
        
        # Прогресс бар
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.status_label = ttk.Label(progress_frame, text="Готов к конвертации")
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
        # Кнопки управления
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=5, column=0, columnspan=3, pady=(10, 0))
        
        self.convert_button = ttk.Button(control_frame, text="Начать конвертацию", 
                                       command=self.start_conversion)
        self.convert_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(control_frame, text="Выход", 
                  command=self.root.quit).pack(side=tk.LEFT)
        
    def add_files(self):
        """Добавление видео файлов"""
        filetypes = [
            ('Видео файлы', '*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.m4v'),
            ('MP4 файлы', '*.mp4'),
            ('AVI файлы', '*.avi'),
            ('MOV файлы', '*.mov'),
            ('Все файлы', '*.*')
        ]
        
        files = filedialog.askopenfilenames(
            title="Выберите видео файлы",
            filetypes=filetypes
        )
        
        for file in files:
            if file not in self.video_files:
                self.video_files.append(file)
                self.files_listbox.insert(tk.END, os.path.basename(file))
                
    def clear_files(self):
        """Очистка списка файлов"""
        self.video_files.clear()
        self.files_listbox.delete(0, tk.END)
        
    def select_output_folder(self):
        """Выбор папки для сохранения"""
        folder = filedialog.askdirectory(title="Выберите папку для сохранения MP3")
        if folder:
            self.output_folder.set(folder)
            
    def start_conversion(self):
        """Запуск процесса конвертации"""
        if not self.video_files:
            messagebox.showwarning("Предупреждение", "Выберите видео файлы для конвертации")
            return
            
        if not self.output_folder.get():
            messagebox.showwarning("Предупреждение", "Выберите папку для сохранения MP3")
            return
            
        if self.is_converting:
            messagebox.showinfo("Информация", "Конвертация уже выполняется")
            return
            
        # Запуск конвертации в отдельном потоке
        self.is_converting = True
        self.convert_button.configure(state="disabled")
        
        conversion_thread = threading.Thread(target=self.convert_videos)
        conversion_thread.daemon = True
        conversion_thread.start()
        
    def convert_videos(self):
        """Конвертация видео файлов"""
        # Импорт moviepy при необходимости
        try:
            from moviepy.video.io.VideoFileClip import VideoFileClip
        except ImportError as e:
            error_msg = "Ошибка импорта moviepy. Убедитесь, что библиотека установлена правильно."
            self.root.after(0, lambda: messagebox.showerror("Ошибка", error_msg))
            self.root.after(0, lambda: self.status_label.configure(text="Ошибка: moviepy не найдена"))
            self.is_converting = False
            self.root.after(0, lambda: self.convert_button.configure(state="normal"))
            return
            
        total_files = len(self.video_files)
        successful_conversions = 0
        failed_conversions = []
        
        for i, video_file in enumerate(self.video_files):
            try:
                # Обновление статуса
                filename = os.path.basename(video_file)
                self.root.after(0, lambda f=filename: self.status_label.configure(
                    text=f"Конвертация: {f}"))
                
                # Загрузка видео
                video = VideoFileClip(video_file)
                
                # Создание имени выходного файла
                output_name = Path(video_file).stem + ".mp3"
                output_path = os.path.join(self.output_folder.get(), output_name)
                
                # Конвертация в MP3
                audio = video.audio
                audio.write_audiofile(
                    output_path,
                    bitrate=self.bitrate_var.get(),
                    logger=None
                )
                
                # Освобождение ресурсов
                audio.close()
                video.close()
                
                successful_conversions += 1
                
            except Exception as e:
                failed_conversions.append(f"{filename}: {str(e)}")
                
            # Обновление прогресса
            progress = ((i + 1) / total_files) * 100
            self.root.after(0, lambda p=progress: self.progress_var.set(p))
            
        # Завершение конвертации
        self.root.after(0, self.conversion_completed, successful_conversions, failed_conversions)
        
    def conversion_completed(self, successful, failed):
        """Завершение процесса конвертации"""
        self.is_converting = False
        self.convert_button.configure(state="normal")
        self.status_label.configure(text="Конвертация завершена")
        
        # Показ результатов
        message = f"Конвертация завершена!\n\n"
        message += f"Успешно конвертировано: {successful} файлов\n"
        
        if failed:
            message += f"Ошибки: {len(failed)} файлов\n\n"
            message += "Файлы с ошибками:\n"
            for error in failed[:5]:  # Показываем только первые 5 ошибок
                message += f"• {error}\n"
            if len(failed) > 5:
                message += f"... и еще {len(failed) - 5} файлов"
                
        messagebox.showinfo("Результат конвертации", message)
        
        # Сброс прогресса
        self.progress_var.set(0)

def main():
    """Главная функция"""
    root = tk.Tk()
    app = VideoToMP3Converter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
import os
import re
import sys
import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox, ttk

POSSIBLE_PATHS = [
    os.path.expandvars(r"%LOCALAPPDATA%\Spotify\Users"),
    os.path.expandvars(r"%APPDATA%\Spotify\Users"),
    os.path.expandvars(
        r"%LOCALAPPDATA%\Packages\SpotifyAB.SpotifyMusic_zpdnekdrzrea0\LocalState\Spotify\Users"
    ),
]


def find_cache_file():
    for base_path in POSSIBLE_PATHS:
        if os.path.exists(base_path):
            for root, dirs, files in os.walk(base_path):
                for f in files:
                    if "history" in f.lower() or "play" in f.lower():
                        return os.path.join(root, f)
    return None


def extract_tracks(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        raw_tracks = re.findall(
            r"(?:spotify:track:|open\.spotify\.com\/track\/)([a-zA-Z0-9]{22})",
            content,
        )

        unique_tracks = list(dict.fromkeys(raw_tracks))
        unique_tracks.reverse()

        return [f"spotify:track:{tid}" for tid in unique_tracks]
    except Exception:
        return []


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.lang = "en"
        self.tracks = []
        self.found_count = 0

        self.title("Spotify Cache Recovery Tool")
        self.geometry("560x540")
        self.resizable(False, False)

        self.texts = {
            "en": {
                "btn_lang": "Русский",
                "status_searching": "Searching for Spotify cache...",
                "status_found": "Unique tracks found: ",
                "status_not_found": "Cache file not found! Select manually.",
                "btn_copy": "Copy URLs to Clipboard",
                "btn_manual": "Select history file manually",
                "instruction": "How to insert into Spotify:\n1. Create a new playlist in Spotify.\n2. Click 'Copy URLs to Clipboard'.\n3. Open your new playlist and press Ctrl + V.",
                "path_info": (
                    r"Default path: C:\Users\<Username>\AppData\Local\Spotify\Users\<User_ID>\list_player_play_history"
                ),
                "copied_msg": "URLs copied to clipboard!",
                "error_no_tracks": "No tracks found in the selected file.",
                "about_desc": (
                    "Created by lov3llama\n"
                    "I built this tool because my Spotify account got deleted for no reason, "
                    "so I needed a way to recover my recent play history.\n"
                    "If this tool helped you out, consider supporting!"
                ),
            },
            "ru": {
                "btn_lang": "English",
                "status_searching": "Ищем кэш Spotify...",
                "status_found": "Найдено уникальных треков: ",
                "status_not_found": "Кэш-файл не найден! Выберите вручную.",
                "btn_copy": "Скопировать URL в буфер",
                "btn_manual": "Выбрать файл истории вручную",
                "instruction": "Как вставить в Spotify:\n1. Создай новый плейлист в Spotify.\n2. Нажми 'Скопировать URL в буфер'.\n3. Открой новый плейлист и нажми Ctrl + V.",
                "path_info": (
                    r"Обычно файл лежит в: C:\Users\<Username>\AppData\Local\Spotify\Users\<User_ID>\list_player_play_history"
                ),
                "copied_msg": "URL успешно скопированы в буфер обмена!",
                "error_no_tracks": "В выбранном файле не найдено треков.",
                "about_desc": (
                    "Автор: lov3llama\n"
                    "Я создал это приложение, потому что мой аккаунт Spotify удалили без причины, "
                    "и мне нужно было вернуть недавнюю историю прослушиваний.\n"
                    "Если вам пригодилась утилита, буду рад вашей поддержке!"
                ),
            },
        }

        self.setup_ui()
        self.run_search()

    def setup_ui(self):
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", padx=15, pady=10)

        self.lbl_title = ttk.Label(
            top_frame,
            text="Spotify Cache Recover",
            font=("Segoe UI", 14, "bold"),
        )
        self.lbl_title.pack(side="left")

        self.btn_lang = ttk.Button(
            top_frame, text="Русский", command=self.toggle_lang, width=10
        )
        self.btn_lang.pack(side="right")

        ttk.Separator(self).pack(fill="x", padx=15, pady=5)

        self.lbl_status = ttk.Label(
            self, text="", font=("Segoe UI", 11), wraplength=520
        )
        self.lbl_status.pack(pady=10)

        self.btn_copy = ttk.Button(
            self,
            text="",
            command=self.copy_to_clipboard,
            state="disabled",
            width=32,
        )
        self.btn_copy.pack(pady=8)

        self.btn_manual = ttk.Button(
            self, text="", command=self.select_manual_file
        )
        self.btn_manual.pack(pady=4)

        self.lbl_instruction = ttk.Label(
            self,
            text="",
            font=("Segoe UI", 9),
            justify="left",
            foreground="gray",
        )
        self.lbl_instruction.pack(pady=8)

        ttk.Separator(self).pack(fill="x", padx=15, pady=8)

        self.lbl_about = ttk.Label(
            self,
            text="",
            font=("Segoe UI", 8),
            justify="center",
            foreground="#444444",
            wraplength=520,
        )
        self.lbl_about.pack(pady=4)

        links_frame = ttk.Frame(self)
        links_frame.pack(pady=4)

        btn_github = ttk.Button(
            links_frame,
            text="GitHub (lov3llama)",
            command=lambda: webbrowser.open("https://github.com/lov3llama"),
        )
        btn_github.pack(side="left", padx=5)

        btn_paypal = ttk.Button(
            links_frame,
            text="Donate (PayPal)",
            command=lambda: webbrowser.open("https://paypal.me/lov3llama"),
        )
        btn_paypal.pack(side="left", padx=5)

        self.lbl_path_info = ttk.Label(
            self,
            text="",
            font=("Segoe UI", 8),
            justify="center",
            foreground="#666666",
            wraplength=520,
        )
        self.lbl_path_info.pack(side="bottom", pady=8)

        self.update_texts()

    def update_texts(self):
        t = self.texts[self.lang]
        self.btn_lang.config(text=t["btn_lang"])
        self.btn_copy.config(text=t["btn_copy"])
        self.btn_manual.config(text=t["btn_manual"])
        self.lbl_instruction.config(text=t["instruction"])
        self.lbl_about.config(text=t["about_desc"])
        self.lbl_path_info.config(text=t["path_info"])

        if self.found_count > 0:
            self.lbl_status.config(
                text=f"{t['status_found']}{self.found_count}"
            )
        else:
            self.lbl_status.config(text=t["status_not_found"])

    def toggle_lang(self):
        self.lang = "ru" if self.lang == "en" else "en"
        self.update_texts()

    def run_search(self, path=None):
        t = self.texts[self.lang]
        cache_path = path or find_cache_file()

        if cache_path and os.path.exists(cache_path):
            self.tracks = extract_tracks(cache_path)
            self.found_count = len(self.tracks)

            if self.found_count > 0:
                self.lbl_status.config(
                    text=f"{t['status_found']}{self.found_count}"
                )
                self.btn_copy.config(state="normal")
            else:
                self.lbl_status.config(text=t["error_no_tracks"])
                self.btn_copy.config(state="disabled")
        else:
            self.lbl_status.config(text=t["status_not_found"])
            self.btn_copy.config(state="disabled")

    def select_manual_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Spotify history/cache file",
            filetypes=[("All files", "*.*")],
        )
        if file_path:
            self.run_search(file_path)

    def copy_to_clipboard(self):
        t = self.texts[self.lang]
        if self.tracks:
            self.clipboard_clear()
            self.clipboard_append("\n".join(self.tracks))
            messagebox.showinfo("Success", t["copied_msg"])
        else:
            messagebox.showwarning("Error", t["error_no_tracks"])


if __name__ == "__main__":
    app = App()
    app.mainloop()
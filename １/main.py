import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import csv
import os
from datetime import datetime
import random
from PIL import Image, ImageTk

PAPER_BG = "#fffaf0"
NOTE_BG = "#fffbf2"
FONT_JP = "游明朝" if os.name == "nt" else "Noto Serif JP"

DATA_FOLDER = "diary_data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

weather_options = ["晴れ", "雨", "曇り", "雪"]
activity_options = ["出社", "テレワーク", "外回り", "出張", "休日"]

omikuji_themes = [
    "今日の出来事を振り返ってみよう。",
    "今日一番嬉しかったことは何ですか？",
    "今日の感謝したことを思い出して書こう。",
    "今日はどんな小さな成功を感じたかを書いてみよう。",
    "今日の自分に贈る言葉を書いてみよう。",
    "最近ハマっていることについて書いてみよう。",
    "今日はどんな挑戦をしたか書いてみよう。",
    "今日の一番印象に残った人は誰ですか？",
]

feelings = {
    "イライラ": {"bg": "#ff6666", "font": (FONT_JP, 14, "bold")},
    "悲しい": {"bg": "#87cefa", "font": (FONT_JP, 14, "italic")},
    "楽しい": {"bg": "#ffff99", "font": ("Hiragino Kaku Gothic Pro", 14)},
}

def save_data():
    date = cal.get_date()
    weather = weather_var.get()
    activity = activity_var.get()
    satisfaction = satisfaction_scale.get()
    diary_text = diary_entry.get("1.0", tk.END).strip()

    if not weather or not activity:
        messagebox.showerror("エラー", "天気と行動を選択してください。")
        return

    def confirm_and_save():
        csv_path = os.path.join(DATA_FOLDER, "diary.csv")
        weather_index = weather_options.index(weather)
        activity_index = activity_options.index(activity)

        if os.path.exists(csv_path):
            with open(csv_path, "r", encoding="utf-8-sig") as f:
                rows = [row for row in csv.reader(f) if row[0] != date]
        else:
            rows = []

        rows.append([date, weather_index, satisfaction, activity_index])

        with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        txt_path = os.path.join(DATA_FOLDER, f"{date}.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"[おみくじ]\n{omikuji_label.cget('text')}\n\n")
            f.write("[日記]\n")
            f.write(diary_text)

        weather_var.set("")
        activity_var.set("")
        satisfaction_scale.set(50)
        diary_entry.delete("1.0", tk.END)

        messagebox.showinfo("保存完了", "日記が保存されました！")
        confirm_window.destroy()

    confirm_window = tk.Toplevel(root)
    confirm_window.title("保存内容の確認")
    confirm_window.geometry("700x700")
    confirm_window.configure(bg=PAPER_BG)

    def restore_inputs():
        weather_var.set(weather)
        activity_var.set(activity)
        satisfaction_scale.set(satisfaction)
        diary_entry.delete("1.0", tk.END)
        diary_entry.insert("1.0", diary_text)

    tk.Label(confirm_window, text=f"日付: {date}", font=(FONT_JP, 14), bg=PAPER_BG).pack(pady=10)
    tk.Label(confirm_window, text=f"天気: {weather}", font=(FONT_JP, 14), bg=PAPER_BG).pack(pady=10)
    tk.Label(confirm_window, text=f"主な行動: {activity}", font=(FONT_JP, 14), bg=PAPER_BG).pack(pady=10)
    tk.Label(confirm_window, text=f"充実度: {satisfaction}", font=(FONT_JP, 14), bg=PAPER_BG).pack(pady=10)

    tk.Label(confirm_window, text="日記内容:", font=(FONT_JP, 14), bg=PAPER_BG).pack(pady=(20, 5))
    diary_preview = tk.Text(confirm_window, width=50, height=10, font=(FONT_JP, 12), wrap="word", bg=PAPER_BG)
    diary_preview.insert("1.0", diary_text)
    diary_preview.config(state="disabled")
    diary_preview.pack(pady=10)

    btn_frame = tk.Frame(confirm_window, bg=PAPER_BG)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="戻る", font=(FONT_JP, 12), width=10, bg="#87cefa",
              command=lambda: [restore_inputs(), confirm_window.destroy()]).pack(side="left", padx=10)
    tk.Button(btn_frame, text="保存する", font=(FONT_JP, 12), width=10, bg="#90ee90",
              command=confirm_and_save).pack(side="left", padx=10)

def load_data_for_date(event=None):
    date = cal.get_date()
    txt_path = os.path.join(DATA_FOLDER, f"{date}.txt")
    csv_path = os.path.join(DATA_FOLDER, "diary.csv")

    date_label.config(text=f"今日の日付: {date}")

    if os.path.exists(txt_path):
        with open(txt_path, "r", encoding="utf-8") as f:
            content = f.read()
            diary_entry.delete("1.0", tk.END)
            diary_entry.insert("1.0", content)
    else:
        content = ""
        diary_entry.delete("1.0", tk.END)

    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
            for row in reversed(rows):
                if row[0] == date:
                    weather_var.set(weather_options[int(row[1])])
                    satisfaction_scale.set(int(row[2]))
                    activity_var.set(activity_options[int(row[3])])
                    break
            else:
                weather_var.set("")
                activity_var.set("")
                satisfaction_scale.set(50)

            if "[おみくじ]" in content and "[日記]" in content:
                omikuji_part = content.split("[日記]")[0].replace("[おみくじ]\n", "").strip()
                diary_part = content.split("[日記]")[1].strip()
                omikuji_label.config(text=omikuji_part)
                diary_entry.delete("1.0", tk.END)
                diary_entry.insert("1.0", diary_part)
            else:
                omikuji_label.config(text="おみくじ: ")
                diary_entry.delete("1.0", tk.END)
                diary_entry.insert("1.0", content)

def draw_omikuji():
    theme = random.choice(omikuji_themes)
    omikuji_label.config(text=f"おみくじ: {theme}")

def change_feeling(feeling):
    color = feelings[feeling]["bg"]
    font = feelings[feeling]["font"]

    for widget in [root, main_frame, left_frame, right_frame, feeling_button_frame]:
        widget.configure(bg=color)

    diary_entry.configure(bg=NOTE_BG, font=font)

    for label in [feeling_label, omikuji_label, date_label]:
        label.configure(font=font)

    for widget in right_frame.winfo_children():
        if isinstance(widget, tk.Label):
            widget.configure(bg=color, font=font)
            
def reset_feeling():
    for widget in [root, main_frame, left_frame, right_frame, feeling_button_frame]:
        widget.configure(bg=PAPER_BG)

    diary_entry.configure(bg=NOTE_BG, font=(FONT_JP, 16))

    for label in [feeling_label, omikuji_label, date_label]:
        label.configure(font=(FONT_JP, 16))

    for widget in right_frame.winfo_children():
        if isinstance(widget, tk.Label):
            widget.configure(bg=PAPER_BG, font=(FONT_JP, 14))


root = tk.Tk()
root.title("日記アプリ")
root.attributes('-fullscreen', True)
root.configure(bg=PAPER_BG)
root.bind("<Escape>", lambda event: root.destroy())

main_frame = tk.Frame(root, bg=PAPER_BG)
main_frame.grid(row=1, column=0, padx=40, pady=20, sticky="e")

left_frame = tk.Frame(main_frame, bg=PAPER_BG)
left_frame.grid(row=0, column=0, sticky="n", padx=40)

right_frame = tk.Frame(main_frame, bg=PAPER_BG)
right_frame.grid(row=0, column=1, sticky="n", padx=40)

calender_label = tk.Label(left_frame, text="日付を選択", font=(FONT_JP, 18), bg=PAPER_BG)
calender_label.grid(row=0, column=1)

cal = Calendar(left_frame, selectmode='day', date_pattern='yyyy_mm_dd', font=(FONT_JP, 14), background="lightblue", foreground="black", selectbackground="lightgreen")
cal.grid(row=1, column=1, pady=10)
cal.bind("<<CalendarSelected>>", load_data_for_date)

logo_path = "img/logo.png"
logo_image = Image.open(logo_path).resize((100, 100))
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(left_frame, image=logo_photo, bg=PAPER_BG)
logo_label.photo = logo_photo
logo_label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)


tk.Label(left_frame, text="天気", font=(FONT_JP, 13), bg=PAPER_BG).grid(row=2, column=1, pady=(10, 8), sticky="w")
weather_var = tk.StringVar()
weather_combo = ttk.Combobox(left_frame, textvariable=weather_var, values=weather_options, state="readonly", width=25, font=(FONT_JP, 14))
weather_combo.grid(row=3, column=1, pady=5)

tk.Label(left_frame, text="主な行動", font=(FONT_JP, 13), bg=PAPER_BG).grid(row=4, column=1, pady=(10, 8), sticky="w")
activity_var = tk.StringVar()
activity_combo = ttk.Combobox(left_frame, textvariable=activity_var, values=activity_options, state="readonly", width=25, font=(FONT_JP, 14))
activity_combo.grid(row=5, column=1, pady=5)

fullness_label = tk.Label(left_frame, text="充実度 (0-100)", font=(FONT_JP, 13), bg=PAPER_BG)
fullness_label.grid(row=6, column=1, pady=(10, 8), sticky="w")
satisfaction_scale = tk.Scale(left_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=300, sliderlength=20)
satisfaction_scale.set(50)
satisfaction_scale.grid(row=7, column=1, pady=5)

today_date = datetime.today().strftime("%Y-%m-%d")
date_label = tk.Label(right_frame, text=f"今日の日付: {today_date}", font=(FONT_JP, 16), bg=PAPER_BG)
date_label.grid(row=0, column=0, pady=(10, 5))

omikuji_button = tk.Button(right_frame, text="今日のおみくじ", font=(FONT_JP, 14), bg="#ffff99", command=draw_omikuji)
omikuji_button.grid(row=1, column=0, pady=10)

omikuji_label = tk.Label(right_frame, text="おみくじ: ", font=(FONT_JP, 14), bg=PAPER_BG)
omikuji_label.grid(row=2, column=0, pady=5)

feeling_label = tk.Label(right_frame, text="今の気分を選んでください", font=(FONT_JP, 16), bg=PAPER_BG)
feeling_label.grid(row=3, column=0, pady=(20, 5))

feeling_button_frame = tk.Frame(right_frame, bg=PAPER_BG)
feeling_button_frame.grid(row=4, column=0, pady=(5, 20))
for i, feeling in enumerate(feelings):
    btn = tk.Button(feeling_button_frame, text=feeling, font=(FONT_JP, 14), width=10,
                    command=lambda f=feeling: change_feeling(f))
    btn.grid(row=0, column=i, padx=10)
    
reset_btn = tk.Button(feeling_button_frame, text="リセット", font=(FONT_JP, 14), width=10, bg="#dddddd",
                      command=reset_feeling)
reset_btn.grid(row=0, column=len(feelings), padx=10)


tk.Label(right_frame, text="今日の日記", font=(FONT_JP, 16), bg=PAPER_BG).grid(row=5, column=0, pady=(10, 5))
diary_entry = tk.Text(right_frame, height=10, width=40, font=(FONT_JP, 16), wrap="word", bg=NOTE_BG, bd=1, relief="solid", padx=15, pady=15)
diary_entry.grid(row=6, column=0, pady=10)

button_frame = tk.Frame(right_frame, bg=PAPER_BG)
button_frame.grid(row=7, column=0, pady=10)
save_btn = tk.Button(button_frame, text="保存する", command=save_data, bg="#90ee90", font=(FONT_JP, 13), width=9, relief="flat", bd=5, activebackground="#80e080")
save_btn.grid(row=0, column=0, padx=10)
close_btn = tk.Button(button_frame, text="閉じる", command=root.destroy, bg="#f08080", font=(FONT_JP, 13), width=9, relief="flat", bd=5, activebackground="#f08080")
close_btn.grid(row=0, column=1, padx=10)

root.mainloop()

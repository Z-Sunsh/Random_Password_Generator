import tkinter as tk
from tkinter import messagebox
import random
import string
import json

# Загрузка истории
try:
    with open("passwords.json", "r", encoding="utf-8") as f:
        history = json.load(f)
except:
    history = []

def save_history():
    with open("passwords.json", "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def update_list():
    listbox.delete(0, tk.END)
    if not history:
        listbox.insert(0, "История пуста")
        return
    for i, p in enumerate(history[-10:], 1):
        listbox.insert(tk.END, f"{i}. {p['pwd']} (дл:{p['len']})")

def generate():
    length = scale.get()
    
    chars = ""
    if var_letters.get():
        chars += string.ascii_letters
    if var_digits.get():
        chars += string.digits
    if var_symbols.get():
        chars += "!@#$%&*"
    
    if not chars:
        messagebox.showerror("Ошибка", "Выберите типы символов!")
        return
    
    pwd = ""
    for _ in range(length):
        pwd += random.choice(chars)
    
    label_pwd.config(text=pwd)
    
    history.append({"pwd": pwd, "len": length})
    save_history()
    update_list()

def copy_pwd():
    pwd = label_pwd.cget("text")
    if pwd and pwd != "---":
        root.clipboard_clear()
        root.clipboard_append(pwd)
        messagebox.showinfo("Успех", "Пароль скопирован!")

def clear_history():
    if messagebox.askyesno("Очистка", "Удалить всю историю?"):
        global history
        history = []
        save_history()
        update_list()

# Окно
root = tk.Tk()
root.title("Генератор паролей")
root.geometry("450x550")

tk.Label(root, text="ГЕНЕРАТОР ПАРОЛЕЙ", font=("Arial", 14, "bold")).pack(pady=10)

# Длина
tk.Label(root, text="Длина пароля:").pack()
scale = tk.Scale(root, from_=4, to=24, orient="horizontal")
scale.set(10)
scale.pack()

# Чекбоксы
var_letters = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=False)

tk.Checkbutton(root, text="Буквы", variable=var_letters).pack(anchor="w", padx=50)
tk.Checkbutton(root, text="Цифры", variable=var_digits).pack(anchor="w", padx=50)
tk.Checkbutton(root, text="Спецсимволы (!@#$%&*)", variable=var_symbols).pack(anchor="w", padx=50)

# Кнопка
tk.Button(root, text="СГЕНЕРИРОВАТЬ", command=generate, bg="green", fg="white").pack(pady=10)

# Результат
label_pwd = tk.Label(root, text="---", font=("Courier", 12, "bold"), fg="blue")
label_pwd.pack(pady=5)

tk.Button(root, text="КОПИРОВАТЬ", command=copy_pwd, bg="orange").pack(pady=5)

# История
tk.Label(root, text="ИСТОРИЯ", font=("Arial", 10, "bold")).pack()
listbox = tk.Listbox(root, height=8, width=50)
listbox.pack(pady=5)

tk.Button(root, text="ОЧИСТИТЬ ИСТОРИЮ", command=clear_history, bg="red", fg="white").pack(pady=10)

update_list()
root.mainloop()
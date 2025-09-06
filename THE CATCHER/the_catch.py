import tkinter as tk
from tkinter import messagebox
import desktop

# this is your destop.py (renamed)

def show_main_menu():
    root = tk.Tk()
    root.title("The Catcher - Main Menu")
    root.geometry("800x600")
    root.configure(bg="white")

    tk.Label(root, text="THE CATCHER", font=("Arial", 36), bg="white").pack(pady=50)

    start_btn = tk.Button(root, text="Start", font=("Arial", 18), command=lambda: [root.destroy(), desktop.show_desktop()])
    start_btn.pack(pady=10)

    options_btn = tk.Button(root, text="Options", font=("Arial", 18), command=lambda: messagebox.showinfo("Options", "Options coming soon..."))
    options_btn.pack(pady=10)

    root.mainloop()

# Run the menu
show_main_menu()

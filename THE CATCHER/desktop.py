import tkinter as tk
from tkinter import PhotoImage, messagebox
import os
import pygame
import time

# Init pygame for sound
pygame.mixer.init()
CLICK_SOUND = os.path.join("assets", "audio", "click.wav")

# State dictionaries
open_windows = {}
taskbar_buttons = {}
PIXEL_FONT = ("Courier New", 9, "bold")

# Track minimized states
window_sizes = {}  # Store app original size
window_states = {}  # 'normal' or 'minimized'

def play_click():
    try:
        pygame.mixer.Sound(CLICK_SOUND).play()
    except:
        pass

def close_app(name):
    if name in open_windows:
        win = open_windows[name]
        if win.winfo_exists():
            animate_close(win)
            win.destroy()
        del open_windows[name]
    if name in taskbar_buttons:
        taskbar_buttons[name].destroy()
        del taskbar_buttons[name]
    if name in window_sizes:
        del window_sizes[name]
    if name in window_states:
        del window_states[name]

def toggle_window(name):
    win = open_windows.get(name)
    if not win or not win.winfo_exists():
        return

    if window_states.get(name) == 'minimized':
        window_states[name] = 'normal'
        win.deiconify()
        win.overrideredirect(True)
        w, h = window_sizes.get(name, (800, 500))
        win.geometry(f"{w}x{h}+200+150")
        win.lift()
    else:
        animate_minimize(win)
        win.withdraw()
        window_states[name] = 'minimized'

def animate_close(win):
    try:
        x, y = win.winfo_x(), win.winfo_y()
        w, h = win.winfo_width(), win.winfo_height()
        for i in range(12):
            scale = (12 - i) / 12
            new_w, new_h = int(w * scale), int(h * scale)
            win.geometry(f"{new_w}x{new_h}+{x + (w - new_w)//2}+{y + (h - new_h)//2}")
            win.update()
            time.sleep(0.01)
    except:
        pass

def animate_minimize(win):
    try:
        x, y = win.winfo_x(), win.winfo_y()
        w, h = win.winfo_width(), win.winfo_height()
        for i in range(10):
            scale = (10 - i) / 10
            new_w, new_h = int(w * scale), int(h * scale * 0.5)
            win.geometry(f"{new_w}x{new_h}+{x + (w - new_w)//2}+{y + (h - new_h)//2}")
            win.update()
            time.sleep(0.01)
    except:
        pass

def show_folder_contents(folder_frame, back_button, content_area):
    for widget in content_area.winfo_children():
        widget.destroy()
    back_button.pack(side="top", anchor="w", padx=5, pady=5)
    tk.Label(content_area, text="(empty for now)", font=PIXEL_FONT, bg="#fdf6e3").pack(pady=20)

start_menu_ref = None  # Global reference to start menu window

def show_start_menu(root):
    global start_menu_ref
    if start_menu_ref and start_menu_ref.winfo_exists():
        start_menu_ref.destroy()
        start_menu_ref = None
        return

    play_click()

    start_menu = tk.Toplevel(root)
    start_menu.geometry("150x250+0+450")
    start_menu.overrideredirect(True)
    start_menu.configure(bg="#fdf6e3")

    apps = [f"app{i}.exe" for i in range(1, 9)]

    for app in apps:
        def open_app(app_name=app):
            show_blank_app(app_name, taskbar_frame)
            start_menu.destroy()
        tk.Button(start_menu, text=app, font=PIXEL_FONT, anchor="w", bg="#ffffee",
                  command=open_app).pack(fill="x", padx=4, pady=2)

    def close_menu(event):
        if not (start_menu.winfo_x() <= event.x_root <= start_menu.winfo_x() + start_menu.winfo_width() and
                start_menu.winfo_y() <= event.y_root <= start_menu.winfo_y() + start_menu.winfo_height()):
            start_menu.destroy()
            root.unbind("<Button-1>")
            global start_menu_ref
            start_menu_ref = None

    root.bind("<Button-1>", close_menu)
    start_menu.focus_force()
    start_menu_ref = start_menu

    def close_menu(event):
        if not (start_menu.winfo_x() <= event.x_root <= start_menu.winfo_x() + start_menu.winfo_width() and
                start_menu.winfo_y() <= event.y_root <= start_menu.winfo_y() + start_menu.winfo_height()):
            start_menu.destroy()
            root.unbind("<Button-1>")
            global start_menu_ref
            start_menu_ref = None

    root.bind("<Button-1>", close_menu)
    start_menu.focus_force()
    start_menu_ref = start_menu


def show_blank_app(name, taskbar_frame):
    if name in open_windows:
        toggle_window(name)
        return

    win = tk.Toplevel()
    win.title("")
    win.overrideredirect(True)
    win.geometry("800x500+200+150")
    win.configure(bg="#000000")
    open_windows[name] = win
    window_sizes[name] = (800, 500)
    window_states[name] = 'normal'

    if name not in taskbar_buttons:
        btn = tk.Button(taskbar_frame, text=name, font=PIXEL_FONT, width=12,
                        command=lambda n=name: toggle_window(n))
        btn.pack(side="left", padx=2)
        taskbar_buttons[name] = btn

    def start_move(event):
        win.x, win.y = event.x, event.y

    def do_move(event):
        x = win.winfo_pointerx() - win.x
        y = win.winfo_pointery() - win.y
        win.geometry(f"+{x}+{y}")

    outer_frame = tk.Frame(win, bg="#000000", bd=0)
    outer_frame.pack(expand=True, fill="both", padx=1, pady=1)

    app_frame = tk.Frame(outer_frame, bg="#fdf6e3")
    app_frame.pack(expand=True, fill="both")

    titlebar = tk.Frame(app_frame, bg="#000000", height=22)
    titlebar.pack(fill="x")
    titlebar.bind("<Button-1>", start_move)
    titlebar.bind("<B1-Motion>", do_move)

    tk.Label(titlebar, text=f"  {name}", fg="white", bg="#000000", font=PIXEL_FONT).pack(side="left")

    tk.Button(titlebar, text="_", font=("Courier New", 8), bg="#333", fg="white", width=2,
              command=lambda: toggle_window(name)).pack(side="right")

    tk.Button(titlebar, text="X", font=("Courier New", 8), bg="#550000", fg="white", width=2,
              command=lambda: close_app(name)).pack(side="right")

    content = tk.Frame(app_frame, bg="#fdf6e3")
    content.pack(expand=True, fill="both")

    if name == "Notes":
        text_area = tk.Text(content, font=("Courier New", 10), bg="#ffffe0", fg="black", wrap="word")
        text_area.pack(expand=True, fill="both", padx=10, pady=10)

    elif name == "File Explorer":
        explorer_frame = tk.Frame(content, bg="#fdf6e3")
        explorer_frame.pack(fill="both", expand=True)

        back_btn = tk.Button(explorer_frame, text="← Back", font=PIXEL_FONT, bg="#ddd",
                             command=lambda: refresh_file_explorer(folder_area, back_btn))

        folder_area = tk.Frame(explorer_frame, bg="#fdf6e3")
        folder_area.pack(fill="both", expand=True)

        refresh_file_explorer(folder_area, back_btn)

    else:
        tk.Label(content, text=f"{name} - Placeholder App", font=PIXEL_FONT, bg="#fdf6e3").pack(expand=True)

def refresh_file_explorer(folder_area, back_button):
    for widget in folder_area.winfo_children():
        widget.destroy()
    back_button.pack_forget()

    folders = ["My Documents", "My Pictures"]
    for folder in folders:
        try:
            folder_icon = PhotoImage(file=os.path.join("assets", "icons", "files.png"))
        except:
            folder_icon = None

        folder_btn = tk.Button(folder_area, image=folder_icon, text=folder, compound="left",
                               font=PIXEL_FONT, anchor="w", bg="#fdf6e3", bd=0,
                               command=lambda f=folder: show_folder_contents(folder_area, back_button, folder_area))
        folder_btn.image = folder_icon
        folder_btn.pack(anchor="w", padx=20, pady=5)

# Clock and Desktop remain unchanged from here (you can leave as-is)

# ... (rest of show_desktop and other functions continue)


def update_clock(clock_label):
    now = time.strftime("%H:%M:%S")
    clock_label.config(text=now)
    clock_label.after(1000, lambda: update_clock(clock_label))

def show_desktop():
    root = tk.Tk()
    root.title("Catcher OS")
    root.attributes("-fullscreen", True)
    root.configure(bg="#f0e9d2")
    root.config(cursor="arrow")

    def on_esc(event):
        if messagebox.askyesno("Exit", "Do you want to exit the game?"):
            root.destroy()

    root.bind("<Escape>", on_esc)

    apps = [
        ("File Explorer", "file_explorer.png"),
        ("Chat App", "chat_app.png"),
        ("Notes", "notes.png"),
        ("Browser", "internet.png"),
        ("Recycle Bin", "recycle_bin.png"),
    ]

    icon_spacing = 95
    icon_x = 30
    icon_y_start = 50

    for i, (name, icon_file) in enumerate(apps):
        icon_path = os.path.join("assets", "icons", icon_file)
        try:
            icon = PhotoImage(file=icon_path).subsample(1, 1)
        except:
            icon = None

        btn = tk.Button(
            root,
            image=icon,
            text=name,
            font=PIXEL_FONT,
            compound="top",
            wraplength=100,
            bg="#f0e9d2",
            bd=0,
            fg="black",
            relief="flat",
            command=lambda n=name: [play_click(), root.after(100, lambda: show_blank_app(n, taskbar_frame))]
        )
        btn.image = icon
        btn.place(x=icon_x, y=icon_y_start + i * icon_spacing, width=90, height=85)

    taskbar = tk.Frame(root, bg="#c2b59b", height=40, highlightbackground="black", highlightthickness=1)
    taskbar.pack(side="bottom", fill="x")

    start_icon_path = os.path.join("assets", "icons", "start.png")
    try:
        start_icon = PhotoImage(file=start_icon_path).subsample(2, 2)
        def handle_start_click():
            show_start_menu(root)


        start_btn = tk.Button(
            taskbar,
            image=start_icon,
            bg="#c2b59b",
            relief="flat",
            command=handle_start_click
        )
        start_btn.image = start_icon
        start_btn.pack(side="left", padx=10)

    except:
        start_btn = tk.Button(taskbar, text="Start", font=PIXEL_FONT, command=play_click, bg="#c2b59b")
    start_btn.pack(side="left", padx=10)

    global taskbar_frame
    taskbar_frame = tk.Frame(taskbar, bg="#c2b59b")
    globals()['taskbar_frame'] = taskbar_frame
    taskbar_frame.pack(side="left", padx=10)

    clock_label = tk.Label(taskbar, font=PIXEL_FONT, fg="black", bg="#c2b59b")
    clock_label.pack(side="right", padx=10)
    update_clock(clock_label)

    def minimize_all():
        for name, win in open_windows.items():
            if win.winfo_exists():
                animate_minimize(win)
                win.withdraw()
                window_states[name] = 'minimized'

    show_btn = tk.Button(taskbar, text="▭", font=("Courier", 10, "bold"), width=3,
                         bg="#c2b59b", fg="black", relief="flat", command=minimize_all)
    show_btn.pack(side="right", padx=10)

    root.mainloop()

import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Custom Menubar with Dropdowns")
app.geometry("420x320")

FONT = ("Segoe UI", 15)

# ---------- Faux menubar ----------
bar = ctk.CTkFrame(app)
bar.pack(fill="x")

# Keep track of the currently open dropdown
app._active_menu = None


def close_active_menu():
    if app._active_menu and app._active_menu.winfo_exists():
        app._active_menu.grab_release()
        app._active_menu.destroy()
    app._active_menu = None


def open_dropdown(anchor_widget, entries, width=180):
    # Close any open dropdown first
    close_active_menu()

    # Build the popup right under the anchor
    menu = ctk.CTkToplevel(app)
    app._active_menu = menu
    menu.overrideredirect(True)
    menu.attributes("-topmost", True)

    # position under the anchor
    x = anchor_widget.winfo_rootx()
    y = anchor_widget.winfo_rooty() + anchor_widget.winfo_height()
    menu.geometry(f"+{x}+{y}")

    # container to give a subtle border/padding
    container = ctk.CTkFrame(menu, corner_radius=8)
    container.pack(padx=2, pady=2)

    def on_item_click(cmd):
        close_active_menu()
        cmd()

    # add items
    for label, cmd in entries:
        if label == "---":  # simple separator
            sep = ctk.CTkFrame(container, height=1)
            sep.pack(fill="x", padx=6, pady=(4, 4))
            continue

        btn = ctk.CTkButton(
            container,
            text=label,
            font=FONT,
            width=width,
            fg_color="transparent",
            hover_color=None,  # let theme handle hover
            corner_radius=0,
            anchor="w",
            command=lambda c=cmd: on_item_click(c),
        )
        btn.pack(fill="x", padx=6, pady=2)

    # close behavior
    def on_focus_out(_=None):
        close_active_menu()

    def on_escape(_=None):
        close_active_menu()

    menu.bind("<FocusOut>", on_focus_out)
    menu.bind("<Escape>", on_escape)
    menu.grab_set()  # capture clicks outside
    menu.focus_force()


# Example command callbacks
def do_open():
    print("Open clicked")


def do_save():
    print("Save clicked")


def do_exit():
    app.quit()


def do_cut():
    print("Cut clicked")


def do_copy():
    print("Copy clicked")


# Menubar buttons (styled & clickable)
file_btn = ctk.CTkButton(
    bar,
    text="File",
    font=("Segoe UI", 16),
    fg_color="transparent",
    command=lambda: open_dropdown(
        file_btn,
        [
            ("Open", do_open),
            ("Save", do_save),
            ("---", None),
            ("Exit", do_exit),
        ],
    ),
)
file_btn.pack(side="left", padx=(10, 6), pady=6)

edit_btn = ctk.CTkButton(
    bar,
    text="Edit",
    font=("Segoe UI", 16),
    fg_color="transparent",
    command=lambda: open_dropdown(
        edit_btn,
        [
            ("Cut", do_cut),
            ("Copy", do_copy),
        ],
    ),
)
edit_btn.pack(side="left", padx=6, pady=6)

# Demo content
label = ctk.CTkLabel(app, text="Hello with a custom dropdown menubar!", font=("Segoe UI", 14))
label.pack(pady=40)

app.mainloop()

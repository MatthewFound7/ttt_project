from typing import Callable

from customtkinter import CTkButton, CTkFrame, CTkLabel

from ttt_ui.services.colours import BG_COL, BLUE_COL, BLUE_COL_HOV


class TitleBar(CTkFrame):
    def __init__(self, master, on_stats: Callable[[], None]) -> None:
        super().__init__(master, fg_color=BG_COL, height=150, width=600)

        title_label = CTkLabel(
            self,
            text="Tic-Tac-Toe",
            font=("Helvetica", 80, "bold"),
            width=12,
            fg_color=BG_COL,
            text_color="black",
            corner_radius=10,
        )
        title_label.place(relx=0.5, rely=0.4, anchor="center")

        stats_button = CTkButton(
            self,
            fg_color=BLUE_COL,
            text_color="black",
            text="Stats",
            height=30,
            width=100,
            font=("Helvetica", 18, "bold"),
            hover_color=BLUE_COL_HOV,
            command=on_stats,
        )
        stats_button.place(relx=0, rely=1, anchor="sw")

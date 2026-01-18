from typing import Callable

from customtkinter import CTkButton, CTkFrame, CTkLabel

from ttt_ui.services.colours import RED_COL, RED_COL_HOV


class StatsView(CTkFrame):
    def __init__(self, master, on_close: Callable[[], None]) -> None:
        super().__init__(master, fg_color="white", height=600, width=600)

        self._close = CTkButton(
            self,
            fg_color=RED_COL,
            text_color="black",
            text="Close",
            height=30,
            width=100,
            font=("Helvetica", 18, "bold"),
            hover_color=RED_COL_HOV,
            command=on_close,
        )
        self._title = CTkLabel(
            self,
            text="Statistics",
            font=("Helvetica", 80, "bold"),
            width=12,
            text_color="black",
        )
        self._player_title = CTkLabel(
            self,
            text="Player wins: ",
            font=("Helvetica", 20, "bold"),
            width=12,
            text_color="black",
        )
        self._player_score = CTkLabel(
            self,
            text="",
            font=("Helvetica", 20, "bold"),
            width=12,
            text_color="black",
        )
        self._player_over_total = CTkLabel(
            self,
            text="",
            font=("Helvetica", 20, "bold"),
            width=12,
            text_color="black",
        )

    def show_stats(self, wins: int, win_percent: float) -> None:
        self.place(relx=0, rely=0)
        self._close.place(relx=0, rely=0)
        self._title.place(relx=0.5, rely=0.2, anchor="center")
        self._player_title.place(relx=0.22, rely=0.34)
        self._player_score.place(relx=0.43, rely=0.34)
        self._player_over_total.place(relx=0.5, rely=0.34)
        self._player_score.configure(text=str(wins))
        self._player_over_total.configure(text=f"({win_percent:.1%})")

    def hide_stats(self) -> None:
        """Hide stats page."""
        self.place_forget()

from typing import Callable, Optional

from customtkinter import CTkButton, CTkCanvas, CTkFrame, CTkImage, CTkLabel
from PIL import Image

from ttt_ui.services.colours import (
    BG_COL,
    BLUE_COL,
    BLUE_COL_HOV,
    GREEN_COL,
    GREEN_COL_HOV,
    LIGHT_BLUE_COL,
    LIGHT_BLUE_COL_HOVER,
    PURPLE_COL,
    PURPLE_COL_HOV,
    RED_COL,
    RED_COL_HOV,
    YELLOW_COL,
)


class SidebarView(CTkFrame):
    def __init__(
        self,
        master,
        cross_menu: CTkImage,
        circle_menu: CTkImage,
        arrow_left: CTkImage,
        on_restart: Callable[[], None],
        on_multi: Callable[[], None],
        on_easy: Callable[[], None],
        on_hard: Callable[[], None],
        on_impossible: Callable[[], None],
    ) -> None:
        super().__init__(master, fg_color="white", height=450, width=150, corner_radius=0)

        self._arrow_left = arrow_left
        self._arrow_label = CTkLabel(self, image=self._arrow_left, fg_color="white", text="")

        self._menu_cross = CTkLabel(self, image=cross_menu, fg_color="white", text="")
        self._menu_cross.place(relx=0.15, rely=0.1, anchor="center")

        self._menu_circle = CTkLabel(self, image=circle_menu, fg_color="white", text="")
        self._menu_circle.place(relx=0.15, rely=0.23, anchor="center")

        self._game_result = CTkLabel(
            self,
            text="wins!",
            font=("Helvetica", 25, "bold"),
            width=12,
            fg_color=BG_COL,
            text_color="black",
            corner_radius=0,
        )
        self._draw_result = CTkLabel(
            self,
            text="draw...",
            font=("Helvetica", 25, "bold"),
            width=12,
            fg_color=BG_COL,
            text_color="black",
            corner_radius=0,
        )
        self._result_box = CTkLabel(
            self, text="", fg_color=BG_COL, corner_radius=5, width=130, height=40
        )

        self._win_icon: Optional[CTkLabel] = None

        self._play_again = CTkButton(
            self,
            fg_color=LIGHT_BLUE_COL,
            text_color="black",
            text="Play Again?",
            height=70,
            width=131,
            font=("Helvetica", 18, "bold"),
            hover_color=LIGHT_BLUE_COL_HOVER,
            command=on_restart,
        )

        select_frame = CTkFrame(self, fg_color=BG_COL, height=140, width=131, corner_radius=5)
        select_frame.place(relx=0.45, rely=0.81, anchor="center")

        self.multi_button = CTkButton(
            select_frame,
            fg_color=BLUE_COL,
            text_color="black",
            text="Multiplayer",
            width=110,
            height=22,
            font=("Helvetica", 14, "bold"),
            hover_color=BLUE_COL_HOV,
            command=on_multi,
        )
        self.multi_button.place(relx=0.5, rely=0.16, anchor="center")

        black_line = CTkCanvas(select_frame, width=100, height=8, bg=BG_COL, highlightthickness=0)
        black_line.place(relx=0.5, rely=0.31, anchor="center")
        black_line.create_line(0, 2, 100, 2, width=3, capstyle="round", fill="black")

        self.easy_button = CTkButton(
            select_frame,
            fg_color=GREEN_COL,
            text_color="black",
            text="Easy",
            width=110,
            height=22,
            font=("Helvetica", 14, "bold"),
            hover_color=GREEN_COL_HOV,
            command=on_easy,
        )
        self.easy_button.place(relx=0.5, rely=0.44, anchor="center")

        self.hard_button = CTkButton(
            select_frame,
            fg_color=RED_COL,
            text_color="black",
            text="Hard",
            width=110,
            height=22,
            font=("Helvetica", 14, "bold"),
            hover_color=RED_COL_HOV,
            command=on_hard,
        )
        self.hard_button.place(relx=0.5, rely=0.64, anchor="center")

        self.imp_button = CTkButton(
            select_frame,
            fg_color=PURPLE_COL,
            text_color="black",
            text="Impossible",
            width=110,
            height=22,
            font=("Helvetica", 14, "bold"),
            hover_color=PURPLE_COL_HOV,
            command=on_impossible,
        )
        self.imp_button.place(relx=0.5, rely=0.84, anchor="center")

    def highlight_mode_button(self, button) -> None:
        for btn in [self.easy_button, self.hard_button, self.imp_button, self.multi_button]:
            btn.configure(border_color=YELLOW_COL, border_width=0)
        button.configure(border_color=YELLOW_COL, border_width=3)

    def move_turn_arrow(self, shape: str) -> None:
        if shape == "O":
            self._arrow_label.place(relx=0.5, rely=0.1, anchor="center")
        else:
            self._arrow_label.place(relx=0.5, rely=0.23, anchor="center")

    def hide_turn_arrow(self) -> None:
        try:
            self._arrow_label.destroy()
        except Exception:
            pass

    def reset_turn_arrow(self) -> None:
        try:
            self._arrow_label.destroy()
        except Exception:
            pass
        self._arrow_label = CTkLabel(self, image=self._arrow_left, fg_color="white", text="")
        self._arrow_label.place(relx=0.5, rely=0.1, anchor="center")

    def clear_game_results(self) -> None:
        try:
            self._result_box.place_forget()
            self._game_result.place_forget()
            self._draw_result.place_forget()
        except Exception:
            pass

        if self._win_icon is not None:
            try:
                if self._win_icon.winfo_exists():
                    self._win_icon.destroy()
            except Exception:
                pass
            self._win_icon = None

        try:
            self._play_again.place_forget()
        except Exception:
            pass

    def show_game_results(self, winner: str, icon_path: str, icon_size: tuple[int, int]) -> None:
        self._result_box.place(relx=0.45, rely=0.38, anchor="center")

        if winner == "":
            self._draw_result.lift()
            self._draw_result.place(relx=0.4, rely=0.38, anchor="center")
        else:
            pil_img = Image.open(icon_path).convert("RGBA")
            win_img = CTkImage(pil_img, size=icon_size)
            self._win_icon = CTkLabel(self, image=win_img, fg_color=BG_COL, text="")
            self._win_icon.place(relx=0.2, rely=0.38, anchor="center")

            self._game_result.lift()
            self._game_result.place(relx=0.6, rely=0.38, anchor="center")

        self._play_again.place(relx=0.02, rely=0.46)

    def enable_game_mode_selection(self) -> None:
        self.multi_button.configure(state="normal")
        self.easy_button.configure(state="normal")
        self.hard_button.configure(state="normal")
        self.imp_button.configure(state="normal")

    def disable_game_mode_selection(self) -> None:
        self.multi_button.configure(state="disabled")
        self.easy_button.configure(state="disabled")
        self.hard_button.configure(state="disabled")
        self.imp_button.configure(state="disabled")

from typing import Callable, Dict, List, Optional, Tuple

from customtkinter import CTkButton, CTkCanvas, CTkFrame, CTkImage, CTkLabel

from ttt_ui.services.colours import DEEP_RED, WHITE_HOV
from ttt_ui.services.layout import board_grid_x, board_grid_y

BoardCoord = Tuple[float, float]


class BoardView(CTkFrame):
    def __init__(self, master, on_cell_click: Callable[[float, float, CTkButton], None]) -> None:
        super().__init__(master, fg_color="white", height=450, width=450, corner_radius=0)
        self._on_cell_click = on_cell_click

        self._board_buttons: List[CTkButton] = []
        self._coord_button_map: Dict[BoardCoord, CTkButton] = {}

        self._placed_items: List[CTkLabel] = []
        self._placed_positions: List[Tuple[CTkLabel, float, float]] = []
        self._highlight_board_buttons: List[CTkButton] = []

        self._canvas = CTkCanvas(self, width=420, height=420, bg="white", highlightthickness=0)
        self._canvas.grid(column=0, row=1, padx=15, pady=15)

        self._draw_game_grid()

    @property
    def active_board_buttons(self) -> List[CTkButton]:
        return self._board_buttons

    @property
    def highlight_board_buttons(self) -> List[CTkButton]:
        return self._highlight_board_buttons

    @property
    def coord_button_map(self) -> Dict[BoardCoord, CTkButton]:
        return self._coord_button_map

    def _draw_game_grid(self) -> None:
        self._canvas.create_line(0, 140, 420, 140, width=8, capstyle="round", fill=DEEP_RED)
        self._canvas.create_line(0, 280, 420, 280, width=8, capstyle="round", fill=DEEP_RED)
        self._canvas.create_line(140, 0, 140, 420, width=8, capstyle="round", fill=DEEP_RED)
        self._canvas.create_line(280, 0, 280, 420, width=8, capstyle="round", fill=DEEP_RED)

    def create_click_grid(self) -> None:
        self._board_buttons.clear()
        self._coord_button_map.clear()

        for x_pos in board_grid_x:
            for y_pos in board_grid_y:
                btn = CTkButton(
                    self,
                    fg_color="transparent",
                    bg_color="transparent",
                    hover_color=WHITE_HOV,
                    width=120,
                    height=120,
                    text="",
                )
                btn.place(relx=x_pos, rely=y_pos, anchor="center")
                btn.configure(command=lambda e=x_pos, p=y_pos, b=btn: self._on_cell_click(e, p, b))
                self._board_buttons.append(btn)
                self._coord_button_map[(x_pos, y_pos)] = btn

    def destroy_click_grid(self) -> None:
        for btn in self._board_buttons:
            try:
                if btn.winfo_exists():
                    btn.destroy()
            except Exception:
                pass
        self._board_buttons = []
        self._coord_button_map = {}

    def set_button_active(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        for btn in self._board_buttons:
            try:
                if btn.winfo_exists():
                    btn.configure(state=state)
            except Exception:
                pass

    def remove_cell_button(self, x: float, y: float, fallback: Optional[CTkButton]) -> None:
        target = self._coord_button_map.get((x, y))
        if target and target.winfo_exists():
            target.destroy()
            return
        if fallback and fallback.winfo_exists():
            fallback.destroy()

    def render_mark(self, x: float, y: float, image: CTkImage) -> None:
        item = CTkLabel(self, image=image, fg_color="white", text="")
        item.place(relx=x, rely=y, anchor="center")
        self._placed_items.append(item)
        self._placed_positions.append((item, x, y))

    def clear_all_marks(self) -> None:
        for item in self._placed_items:
            try:
                if item.winfo_exists():
                    item.destroy()
            except Exception:
                pass
        self._placed_items = []
        self._placed_positions = []

    def button_disable_on_win(self) -> None:
        self.destroy_highlight_overlay()

        for pos in board_grid_y:
            for entry in board_grid_x:
                btn = CTkButton(
                    self,
                    fg_color="transparent",
                    bg_color="transparent",
                    hover_color=WHITE_HOV,
                    width=120,
                    height=120,
                    text="",
                    state="disabled",
                )
                btn.place(relx=entry, rely=pos, anchor="center")
                self._highlight_board_buttons.append(btn)

    def destroy_highlight_overlay(self) -> None:
        for btn in self._highlight_board_buttons:
            try:
                if btn.winfo_exists():
                    btn.destroy()
            except Exception:
                pass
        self._highlight_board_buttons = []

    def replace_marks_and_lift(self) -> None:
        for item, x, y in self._placed_positions:
            try:
                item.place(relx=x, rely=y, anchor="center")
                item.lift()
            except Exception:
                pass

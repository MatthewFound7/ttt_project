import os

from customtkinter import CTk

from ttt_ui.services.layout import CELLS

from .controllers.game_controller import GameController, MoveResult
from .services.assets import ImageAssetLoader
from .state import IconSizesSet, UIAssetsContainer
from .views.board import BoardView
from .views.sidebar import SidebarView
from .views.stats import StatsView
from .views.title_bar import TitleBar


class TicTacToeUI(CTk):
    """Main Tk application composing views and controller."""

    def __init__(self) -> None:
        super().__init__()

        self.title("Tic-Tac-Toe")
        self.geometry("600x600")
        self.resizable(False, False)
        self.config(bg="white")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._controller = GameController()

        self._assets = self._load_assets()

        self._title_bar = TitleBar(self, on_stats=self._open_stats)
        self._title_bar.grid(column=0, row=0, columnspan=2, sticky="nsew")

        self._board = BoardView(self, on_cell_click=self._handle_click)
        self._board.grid(column=0, row=1, columnspan=2, sticky="nsew")

        self._sidebar = SidebarView(
            self,
            cross_menu=self._assets.cross.menu,
            circle_menu=self._assets.circle.menu,
            arrow_left=self._assets.arrow_left,
            on_restart=self._restart_game,
            on_multi=self._multi_choice,
            on_easy=self._easy_choice,
            on_hard=self._hard_choice,
            on_impossible=self._impossible_choice,
        )
        self._sidebar.grid(column=1, row=1, columnspan=2, sticky="nsew")

        self._stats = StatsView(self, on_close=self._close_stats)

        self._game_over = False
        self._game_started = False
        self._board.create_click_grid()

        self._easy_choice()

    def _load_assets(self) -> UIAssetsContainer:
        base_dir = os.path.dirname(__file__)
        loader = ImageAssetLoader(base_dir)
        paths = loader.image_paths()

        cross_main = loader.load_file_into_ctk_image(paths.cross, (105, 105))
        circle_main = loader.load_file_into_ctk_image(paths.circle, (110, 110))
        cross_menu = loader.load_file_into_ctk_image(paths.cross, (30, 30))
        circle_menu = loader.load_file_into_ctk_image(paths.circle, (32, 32))
        arrow_left = loader.load_file_into_ctk_image(paths.arrow_left, (30, 30))

        return UIAssetsContainer(
            cross=IconSizesSet(main=cross_main, menu=cross_menu),
            circle=IconSizesSet(main=circle_main, menu=circle_menu),
            arrow_left=arrow_left,
            cross_path=paths.cross,
            circle_path=paths.circle,
            arrow_path=paths.arrow_left,
        )

    def _open_stats(self) -> None:
        wins, _games, percent = self._controller.hold_stats()
        self._stats.show_stats(wins=wins, win_percent=percent)

    def _close_stats(self) -> None:
        self._stats.hide_stats()

    def _multi_choice(self) -> None:
        self._controller.set_mode_multi()
        self._sidebar.highlight_mode_button(self._sidebar.multi_button)
        self._restart_game()

    def _easy_choice(self) -> None:
        self._controller.set_mode_easy()
        self._sidebar.highlight_mode_button(self._sidebar.easy_button)
        self._restart_game()

    def _hard_choice(self) -> None:
        self._controller.set_challenge_mode("ai-training/models/hard_agent.pkl")
        self._sidebar.highlight_mode_button(self._sidebar.hard_button)
        self._restart_game()

    def _impossible_choice(self) -> None:
        self._controller.set_challenge_mode("ai-training/models/imp_agent.pkl")
        self._sidebar.highlight_mode_button(self._sidebar.imp_button)
        self._restart_game()

    def _handle_click(self, x: float, y: float, btn) -> None:
        if self._game_over:
            return

        self._sidebar.move_turn_arrow(self._controller.current_shape())
        image = (
            self._assets.circle.main
            if self._controller.current_shape() == "O"
            else self._assets.cross.main
        )

        result = self._controller.register_click_and_move(x, y)
        if result.placed_index is None:
            return

        if not self._game_started:
            self._game_started = True
            self._sidebar.disable_game_mode_selection()

        sx, sy = CELLS[result.placed_index]
        self._board.remove_cell_button(sx, sy, fallback=btn)
        self._board.render_mark(sx, sy, image=image)

        if result.attempts == 10:
            self._sidebar.hide_turn_arrow()

        if result.game_over:
            self._end_game(result)
            return

        if self._controller.ai_should_move():
            self._board.set_button_active(False)
            self.after(1000, self._run_ai_turn)

    def _run_ai_turn(self) -> None:
        if self._game_over:
            return

        self._sidebar.move_turn_arrow(self._controller.current_shape())
        image = (
            self._assets.circle.main
            if self._controller.current_shape() == "O"
            else self._assets.cross.main
        )

        result = self._controller.register_ai_click_and_move()
        if result.placed_index is None:
            self._board.set_button_active(True)
            return

        sx, sy = CELLS[result.placed_index]
        self._board.remove_cell_button(sx, sy, fallback=None)
        self._board.render_mark(sx, sy, image=image)

        if result.attempts == 10:
            self._sidebar.hide_turn_arrow()

        if result.game_over:
            self._end_game(result)
            return

        self._board.set_button_active(True)

    def _end_game(self, result: MoveResult) -> None:
        self._game_over = True
        self._board.set_button_active(False)
        self._sidebar.hide_turn_arrow()

        self._board.button_disable_on_win()
        if result.win_line:
            for idx in result.win_line:
                self._board.highlight_board_buttons[idx].configure(fg_color="#FFE96D")

        if result.winner == "X":
            self._sidebar.show_game_results(
                winner="X", icon_path=self._assets.cross_path, icon_size=(30, 30)
            )
        elif result.winner == "O":
            self._sidebar.show_game_results(
                winner="O", icon_path=self._assets.circle_path, icon_size=(32, 32)
            )
        else:
            self._sidebar.show_game_results(winner="", icon_path="", icon_size=(0, 0))

        self._board.replace_marks_and_lift()
        self._sidebar.enable_game_mode_selection()

    def _restart_game(self) -> None:
        self._controller.reset_game_engine()
        self._game_over = False
        self._game_started = False
        self._sidebar.enable_game_mode_selection()

        self._board.destroy_highlight_overlay()
        self._board.clear_all_marks()
        self._sidebar.clear_game_results()
        self._sidebar.reset_turn_arrow()

        self._board.destroy_click_grid()
        self._board.create_click_grid()
        self._board.set_button_active(True)

from typing import Sequence

WIN_LINES: Sequence[tuple[int, int, int]] = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def has_winner(cells: Sequence[str]) -> tuple[bool, str | None]:
    for a, b, c in WIN_LINES:
        if cells[a] and cells[a] == cells[b] == cells[c]:
            return True, cells[a], (a, b, c)
    return False, None, None


def is_draw(cells: Sequence[str]) -> bool:
    return all(bool(cell) for cell in cells)

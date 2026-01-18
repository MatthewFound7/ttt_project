from dataclasses import dataclass

from customtkinter import CTkImage


@dataclass(frozen=True)
class IconSizesSet:
    """Holds main and menu-sized icons."""

    main: CTkImage
    menu: CTkImage


@dataclass(frozen=True)
class UIAssetsContainer:
    cross: IconSizesSet
    circle: IconSizesSet
    arrow_left: CTkImage
    cross_path: str
    circle_path: str
    arrow_path: str

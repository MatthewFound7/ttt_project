import os
from dataclasses import dataclass
from typing import Tuple

from customtkinter import CTkImage
from PIL import Image


@dataclass(frozen=True)
class UIAssetPaths:
    cross: str
    circle: str
    arrow_left: str


class ImageAssetLoader:
    """Loads PIL images and wraps them as CTkImage."""

    def __init__(self, base_dir: str) -> None:
        self._base_dir = base_dir

    def image_paths(self) -> UIAssetPaths:
        assets_dir = os.path.join(self._base_dir, "services/images")
        return UIAssetPaths(
            cross=os.path.join(assets_dir, "blue_cross.png"),
            circle=os.path.join(assets_dir, "orange_circle.png"),
            arrow_left=os.path.join(assets_dir, "left-arrow.png"),
        )

    def load_file_into_ctk_image(self, path: str, size: Tuple[int, int]) -> CTkImage:
        pil_img = Image.open(path).convert("RGBA")
        return CTkImage(pil_img, size=size)

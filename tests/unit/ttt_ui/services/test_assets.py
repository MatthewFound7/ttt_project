from pathlib import Path

import pytest
from PIL import Image

from tests.unit.ttt_ui.views.fakes import FakeImage
from ttt_ui.services.assets import ImageAssetLoader, UIAssetPaths


@pytest.fixture
def base_dir(tmp_path: Path) -> Path:
    assets_dir = tmp_path / "services" / "images"
    assets_dir.mkdir(parents=True)
    return tmp_path


@pytest.fixture
def populated_assets(base_dir: Path) -> UIAssetPaths:
    loader = ImageAssetLoader(str(base_dir))
    paths = loader.image_paths()

    for path in paths.__dict__.values():
        Image.new("RGBA", (16, 16)).save(path)

    return paths


def test_all_assets_load_successfully(
    base_dir: Path,
    populated_assets: UIAssetPaths,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    loader = ImageAssetLoader(str(base_dir))

    module_path = ImageAssetLoader.__module__

    monkeypatch.setattr(
        f"{module_path}.CTkImage",
        FakeImage,
    )

    for path in populated_assets.__dict__.values():
        result = loader.load_file_into_ctk_image(path, (32, 32))

        assert isinstance(result, FakeImage)
        assert result.size == (32, 32)
        assert result.image.mode == "RGBA"

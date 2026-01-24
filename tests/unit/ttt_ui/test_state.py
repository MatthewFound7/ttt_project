import pytest

import ttt_ui.state as state


class FakeImage:
    pass


@pytest.fixture
def icon_set() -> state.IconSizesSet:
    return state.IconSizesSet(main=FakeImage(), menu=FakeImage())


@pytest.fixture
def assets(icon_set: state.IconSizesSet) -> state.UIAssetsContainer:
    return state.UIAssetsContainer(
        cross=icon_set,
        circle=icon_set,
        arrow_left=FakeImage(),
        cross_path="cross.png",
        circle_path="circle.png",
        arrow_path="arrow.png",
    )


def test_ui_assets_container_stores_fields(assets: state.UIAssetsContainer) -> None:
    assert assets.cross_path == "cross.png"
    assert assets.circle_path == "circle.png"
    assert assets.arrow_path == "arrow.png"


def test_icon_sizes_set_is_frozen(icon_set: state.IconSizesSet) -> None:
    with pytest.raises(Exception):
        icon_set.main = FakeImage()


def test_ui_assets_container_is_frozen(assets: state.UIAssetsContainer) -> None:
    with pytest.raises(Exception):
        assets.cross_path = "new_path.png"

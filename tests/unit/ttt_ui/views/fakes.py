from typing import Tuple


class FakeWidget:
    placed_count = 0

    def __init__(self, *args, **kwargs) -> None:
        self.destroyed = False
        self.placed = False
        self.lifted = False
        self.exists = True
        self.state = kwargs.get("state", "normal")
        self.border_color = None
        self.border_width = None
        self.text = kwargs.get("text", "")
        self.command = kwargs.get("command")
        self.place_args = None

    def place(self, **kwargs) -> None:
        self.placed = True
        self.place_args = kwargs
        FakeWidget.placed_count += 1

    def place_forget(self) -> None:
        self.placed = False

    def destroy(self) -> None:
        self.destroyed = True
        self.exists = False

    def winfo_exists(self) -> bool:
        return self.exists

    def configure(self, **kwargs) -> None:
        if "state" in kwargs:
            self.state = kwargs["state"]
        if "border_color" in kwargs:
            self.border_color = kwargs["border_color"]
        if "border_width" in kwargs:
            self.border_width = kwargs["border_width"]
        if "text" in kwargs:
            self.text = kwargs["text"]
        if "command" in kwargs:
            self.command = kwargs["command"]

    def lift(self) -> None:
        self.lifted = True

    def grid(self, **kwargs) -> None:
        pass

    def invoke(self) -> None:
        if self.command:
            self.command()

    def create_line(self, *args, **kwargs) -> None:
        pass


class FakeCanvas(FakeWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.lines = []

    def create_line(self, *args, **kwargs) -> None:
        self.lines.append((args, kwargs))


class FakeImage:
    def __init__(self, image: object = None, size: Tuple[int, int] = None) -> None:
        self.image = image
        self.size = size

    def convert(self, mode: str) -> None:
        pass

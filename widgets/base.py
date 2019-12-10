from dataclasses import dataclass


@dataclass
class Widget:
    name: str

    def gui(self):
        """" This method should contain imgui instructions """
        pass

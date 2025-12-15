from abc import ABC, abstractmethod


class View(ABC):
    id: str
    label: str
    icon: str

    @abstractmethod
    def render(self):
        pass

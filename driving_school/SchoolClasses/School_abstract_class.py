from abc import ABC, abstractmethod


class School(ABC):

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def choice(self, numb):
        return numb

    @abstractmethod
    def action(self):
        pass

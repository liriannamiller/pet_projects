from abc import ABC


class Person(ABC):
    def __init__(self, name, birthdate, phone_number):
        self.name = name
        self.birthdate = birthdate
        self.phone_number = phone_number

from Person import Person_abstract_class as PAC
class Teacher_p(PAC.Person):
    def __init__(self, name, birthdate, phone_number, category):
        super().__init__(name, birthdate, phone_number)
        self.category = category


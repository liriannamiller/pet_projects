from Person import Person_abstract_class as PAC
class Student_p(PAC.Person):

    def __init__(self, name, birthdate, phone_number, start_date, attemps, student_status):
        super().__init__(name, birthdate, phone_number)
        self.start_date = start_date
        self.attemps = attemps
        self.student_status = student_status



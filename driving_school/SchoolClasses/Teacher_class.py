import pandas as pd
from sqlalchemy import create_engine
from SchoolClasses import School_abstract_class as SAC
from datetime import datetime
from Person import Student_person as sp
from SchoolClasses import EnumStatus as es

class Teacher(SAC.School):

    def __init__(self, connection_string='mysql://root:3306@localhost/driving_school'):
        self.connection_string = connection_string
        self.engine = create_engine(connection_string)
        self.res_query = "SELECT * FROM result"
        self.res_df = pd.read_sql(self.res_query, self.engine)
        self.student_query = "SELECT * FROM students"
        self.stud_df = pd.read_sql(self.student_query, self.engine)
        self.teacher_query = "SELECT * FROM teachers"
        self.teacher_df = pd.read_sql(self.teacher_query, self.engine)


    def display(self):
        print('=' * 30 + '\n'
              + '1 - Добавить студента' + '\n'
              + '2 - Поиск студента' + '\n'
              + '3 - История студента' + '\n'
              + '4 - Выход' + '\n'
              + ('=' * 30))


    def test_day_message(self, teacher_name, day):
        test_date = datetime.strptime(day, '%d-%m-%Y').date()
        if teacher_name not in self.teacher_df['teacher_name'].values:
            return f"Учитель с именем {teacher_name} не найден"
        else:
            return f"Уважаемый {teacher_name}, вам необходимо принять тест {test_date}."

    def teacher_notification(self, message):
        teacher_names = self.teacher_df['teacher_name'].values
        for name in teacher_names:
            print(f"Уважаемый преподаватель {name}. {message.capitalize()}")
        return '\nСообщения преподавателям доставлены!'


    def add_student(self):
        print('Введите ФИО студента:')
        name = input().title()
        print('Введите дату рождения студента в формате дд-мм-гг:')
        birthdate = datetime.strptime(input(), '%d-%m-%Y').date()
        print('Введите мобильный номер телефона:')
        number = input()
        print('Введите дату начала обучения в формате дд-мм-гг:')
        start = datetime.strptime(input(), '%d-%m-%Y').date()
        test = 0
        status = es.Status.ACTIVE.value
        s_id = len(self.stud_df['student_id']) + 1

        new_student = sp.Student_p(name, birthdate, number, start, test, status)

        new_info = pd.DataFrame({
            'student_id': [s_id],
            'student_name': [new_student.name],
            'birthdate': [new_student.birthdate],
            'phone_number': [new_student.phone_number],
            'start_date': [new_student.start_date],
            'attemps': [new_student.attemps],
            'student_status': [new_student.student_status]
        })

        new_info.to_sql('students', self.engine, if_exists='append', index=False)

        return 'Студент добавлен!'

    def search_student(self):
        print('Введите имя студента')
        student_name = input().title()
        if student_name not in self.stud_df['student_name'].values:
            return f"Студент с именем {student_name} не найден"
        else:
            pd.set_option('display.max_columns', None)
            info = self.stud_df[self.stud_df['student_name'] == student_name].index[0]
            try:
                last_test = self.res_df[self.res_df['student_name'] == student_name].index[-1]
                print(self.stud_df.loc[info, self.stud_df.columns != 'student_id'].to_string()+'\n')
                print('Данные о последнем тесте'+'\n')
                return self.res_df.loc[last_test, self.res_df.columns.isin(['attemps', 'result', 'mistakes', 'test_date'])].to_string()
            except:
                return f'Студент {student_name} еще не сдавал тесты.'

    def student_history(self):
        print('Введите имя студента')
        student_name = input().title()
        if (student_name in self.stud_df['student_name'].values) and (student_name not in self.res_df['student_name'].values):
            return f'Студент {student_name} еще не сдавал тесты.'
        elif student_name not in self.stud_df['student_name'].values:
            return f"Студент с именем {student_name} не найден"
        else:
            history = self.res_df['student_name'] == student_name
            return self.res_df.loc[history, self.res_df.columns != 'student_id'].to_string(index=False)

    def choice(self, numb):
        select_dict = {
        1: self.add_student,
        2: self.search_student,
        3: self.student_history,
        4: exit
        }

        if numb in select_dict:
            if numb == 7:
                exit()
            else:
                print(select_dict[numb]())
        else:
            print('Неправильный номер')



    def action(self):
        while True:
            self.display()
            try:
                numb = int(input())
                self.choice(numb)
            except ValueError:
                print('Неправильный номер')


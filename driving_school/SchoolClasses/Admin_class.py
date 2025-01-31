import pandas as pd
from sqlalchemy import create_engine
from SchoolClasses import School_abstract_class as SAC
from SchoolClasses import Teacher_class as tc
from SchoolClasses import Student_class as sc
from Person import Student_person as sp
from datetime import datetime
from SchoolClasses import EnumStatus as es


class Admin(SAC.School):

    def __init__(self, connection_string='mysql://root:3306@localhost/driving_school'):
        self.connection_string = connection_string
        self.engine = create_engine(connection_string)
        self.res_query = "SELECT * FROM result"
        self.res_df = pd.read_sql(self.res_query, self.engine)
        self.student_query = "SELECT * FROM students"
        self.stud_df = pd.read_sql(self.student_query, self.engine)
        self.teacher_query = "SELECT * FROM teachers"
        self.teacher_df = pd.read_sql(self.teacher_query, self.engine)
        self.teacher = tc.Teacher(connection_string)
        self.student = sc.Student(connection_string)

    def display(self):
        print('\n'+'=' * 30 + '\n'
              + '1 - Добавить студента' + '\n'
              + '2 - Поиск студента' + '\n'
              + '3 - История студента' + '\n'
              + '4 - Изменить статус студенту' + '\n'
              + '5 - Назначить дату теста' + '\n'
              + '6 - Послать уведомление' + '\n'
              + '7 - Выход' + '\n'
              + ('=' * 30)+'\n')

    def change_student_status(self):
        print('Введите ФИО студента')
        name = input()
        if name not in self.stud_df['student_name'].values:
            return f"Студент с именем {name} не найден"
        elif (name in self.stud_df['student_name'].values) and (name not in self.res_df['student_name'].values):
            print(f'Вы уверены? Студент {name} еще не сдавал тесты.' +'\n'+'\n'+'1 - Подтвердить изменение'+'\n'+'2 - Отменить')
            n = int(input())
            if n == 1:
                self.stud_df.loc[self.stud_df['student_name'] == name, 'student_status'] = es.Status.INACTIVE.value
                self.stud_df.to_sql('students', self.engine, if_exists='replace', index=False)
                return "Информация успешно обновлена!"
            elif n == 2:
                exit()
        else:
            student_results = self.res_df[self.res_df['student_name'] == name]
            last_result = student_results.iloc[-1]['result']
            if last_result == 'failed':
                print('Вы уверенны? Данный студент не сдал успешно тест.'+'\n'+'\n'+'1 - Подтвердить изменение'+'\n'+'2 - Отменить')
                n = int(input())
                if n == 1:
                    self.stud_df.loc[self.stud_df['student_name'] == name, 'student_status'] = es.Status.INACTIVE.value
                    self.stud_df.to_sql('students', self.engine, if_exists='replace', index=False)
                    return "Информация успешно обновлена!"
                elif n == 2:
                    exit()
            elif last_result == 'successful':
                self.stud_df.loc[self.stud_df['student_name'] == name, 'student_status'] = es.Status.INACTIVE.value
                self.stud_df.to_sql('students', self.engine, if_exists='replace', index=False)
                return "Информация успешно обновлена!"

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

    def test_date(self):
        print('Введите имя учителя')
        teacher_name = input().title()
        print('Введите имя студента')
        student_name = input().title()
        print('Введите дату сдачи теста в формате дд-мм-гг:')
        day = input()
        return '\n'+self.teacher.test_day_message(teacher_name, day)+'\n\n'+self.student.test_day_message(student_name, day)

    def sent_notification(self):
        print('Введите ваше уведомлени:')
        message = input()
        return self.teacher.teacher_notification(message)+'\n'+self.student.student_notification(message)

    def choice(self, numb):
        select_dict = {
            1: self.add_student,
            2: self.search_student,
            3: self.student_history,
            4: self.change_student_status,
            5: self.test_date,
            6: self.sent_notification,
            7: exit
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


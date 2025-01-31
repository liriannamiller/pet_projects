import pandas as pd
from sqlalchemy import create_engine
from SchoolClasses import School_abstract_class as SAC
import numpy as np
from datetime import datetime, timedelta


class Student(SAC.School):

    def __init__(self, connection_string='mysql://root:3306@localhost/driving_school'):
        self.connection_string = connection_string
        self.engine = create_engine(connection_string)
        self.res_query = "SELECT * FROM result"
        self.res_df = pd.read_sql(self.res_query, self.engine)
        self.student_query = "SELECT * FROM students"
        self.stud_df = pd.read_sql(self.student_query, self.engine)


    def display(self):
        print('=' * 30 + '\n'
              + '1 - Пройти тест' + '\n'
              + '2 - Показать историю' + '\n'
              + '3 - Выход' + '\n'
              + ('=' * 30))

    def test(self):
        print('Введите ваше имя')
        student_name = input().title()
        if student_name not in self.stud_df['student_name'].values:
            return f"Студент с именем {student_name} не найден."
        elif (student_name in self.stud_df['student_name'].values) and (student_name not in self.res_df['student_name'].values):
            s_id = [self.stud_df.loc[self.stud_df['student_name'] == student_name, 'student_id'].values[0]],
            random_test_date = (datetime.now() - timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d')
            random_mistakes = np.random.randint(0, 10)
            new_attempts = 1


        else:
            s_id = [self.stud_df.loc[self.stud_df['student_name'] == student_name, 'student_id'].values[0]],
            random_test_date = (datetime.now() - timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d')
            random_mistakes = np.random.randint(0, 10)
            last_index = self.res_df[self.res_df['student_name'] == student_name].index[-1]
            new_attempts = self.res_df.loc[last_index, 'attemps'] + 1

        result = 'failed' if random_mistakes > 2 else 'success'

        new_data = pd.DataFrame({
            'student_id': s_id,
            'test_date': [random_test_date],
            'mistakes': [random_mistakes],
            'result': [result],
            'student_name': [student_name],
            'attemps': [new_attempts]
        })

        for index, row in self.res_df.iterrows():
            row['attemps'] == new_data['attemps']

        new_data.to_sql('result', self.engine, if_exists='append', index=False)

        return 'Результат успешно записан'

    def student_history(self):
        print('Введите ваше имя')
        student_name = input().title()
        if student_name not in self.res_df['student_name'].values:
            return f"Студент с именем {student_name} не найден"
        else:
            history = self.res_df['student_name'] == student_name
            return self.res_df.loc[history, self.res_df.columns != 'student_id'].to_string(index=False)

    def test_day_message(self, student_name, day):
        test_date = datetime.strptime(day, '%d-%m-%Y').date()
        if student_name not in self.stud_df['student_name'].values:
            return f"Студент с именем {student_name} не найден"
        else:
            return f"Уважаемый {student_name}, вам назначен тест на {test_date}."

    def student_notification(self, message):
        student_names = self.stud_df.loc[self.stud_df['student_status'] == 'ACTIVE', 'student_name']
        for name in student_names:
            print(f"Уважаемый студент школы вождения {name}. {message.capitalize()}")
        return '\nСообщения студентам доставлены!'


    def choice(self, numb):
        select_dict = {
            1: self.test,
            2: self.student_history,
            3: exit
        }
        if numb in select_dict:
            if numb == 3:
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




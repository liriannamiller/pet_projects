import pandas as pd
from sqlalchemy import create_engine
import json
connection_string = 'mysql://root:3306@localhost/driving_school'
engine = create_engine(connection_string)

cred_query = "SELECT * FROM credantial"
cred_df = pd.read_sql(cred_query, engine)


class LoginAttempts:
    def __init__(self, file):
        self.file = file
        self.login = self.read_json_f()[0]
        self.password = self.read_json_f()[-1]

    def read_json_f(self):
        with open(self.file, 'r') as f:
            templates = json.load(f)
            login = templates.get('login')
            password = templates.get('password')
        return login, password

    def check(self):
        if self.login in cred_df['login'].values:
            cred_pass = cred_df.loc[cred_df['login'] == self.login, 'passwords'].values[0]
            if cred_pass == self.password:
                return 'Доступ разрешен'
            else:
                return 'Доступ запрещен'
        else:
            return 'Доступ запрещен'

    def job_title(self):
        if self.check() == 'Доступ разрешен':
            job = cred_df.loc[cred_df['login'] == self.login, 'job_title'].values[0]
            return job



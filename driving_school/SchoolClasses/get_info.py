from SchoolClasses import LoginAttempts as LA
from SchoolClasses import Student_class as sc
from SchoolClasses import Teacher_class as tc
from SchoolClasses import Admin_class as ac
from SchoolClasses import EnumRoles as er

def get_info(role=LA.LoginAttempts('credentinal.json').job_title()):
    if role == er.Roles.ADMIN.value:
        return ac.Admin().action()

    if role == er.Roles.STUDENT.value:
        return sc.Student().action()

    elif role == er.Roles.TEACHER.value:
        return tc.Teacher().action()



print(get_info())
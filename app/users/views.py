import graphene

from app.users.employee_views import EmployeeMutation, EmployeeQuery
from app.users.hr_advisor_views import HrAdvisorMutation, HrAdvisorQuery


class UserQuery(HrAdvisorQuery, EmployeeQuery):
    pass


class UserMutation(HrAdvisorMutation, EmployeeMutation):
    pass


user_schema = graphene.Schema(query=UserQuery, mutation=UserMutation)

import graphene

from app.users.employee_views import EmployeeMutation, EmployeeQuery
from app.users.hr_advisor_views import HrAdvisorQuery, HrAdvisorMutation


class Query(HrAdvisorQuery, EmployeeQuery, graphene.ObjectType):
    pass


class Mutation(HrAdvisorMutation, EmployeeMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

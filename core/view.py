import graphene

from app.insurance.views import InsuranceQuery, InsuranceMutation
from app.insurance_company.views import InsuranceCompanyMutation, InsuranceCompanyQuery
from app.users.employee_views import EmployeeMutation, EmployeeQuery
from app.users.hr_advisor_views import HrAdvisorQuery, HrAdvisorMutation


class Query(HrAdvisorQuery, EmployeeQuery, InsuranceCompanyQuery, InsuranceQuery, graphene.ObjectType):
    pass


class Mutation(HrAdvisorMutation, EmployeeMutation, InsuranceCompanyMutation, InsuranceMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

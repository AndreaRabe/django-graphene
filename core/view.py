import graphene
import graphql_jwt

from app.insurance.views import InsuranceQuery, InsuranceMutation
from app.insurance_company.views import InsuranceCompanyMutation, InsuranceCompanyQuery
from app.notification.views import NotificationQuery, NotificationMutation
from app.users.employee_views import EmployeeMutation, EmployeeQuery
from app.users.hr_advisor_views import HrAdvisorQuery, HrAdvisorMutation


class Query(HrAdvisorQuery, EmployeeQuery, InsuranceCompanyQuery, InsuranceQuery, NotificationQuery,
            graphene.ObjectType):
    pass


class Mutation(HrAdvisorMutation, EmployeeMutation, InsuranceCompanyMutation, InsuranceMutation, NotificationMutation,
               graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

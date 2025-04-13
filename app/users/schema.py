from graphene_django import DjangoObjectType

from app.users.models import User, HrAdvisor, Employee


class UsersType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'


class HrAdvisorType(UsersType):
    class Meta:
        model = HrAdvisor
        fields = '__all__'


class EmployeeType(UsersType):
    class Meta:
        model = Employee
        fields = '__all__'

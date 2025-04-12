from graphene_django import DjangoObjectType

from app.users.models import User, HrAdvisor, Employee


class UsersType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'


class HrAdvisorType(UsersType):
    class Meta(UsersType.Meta):
        model = HrAdvisor
        fields = UsersType.Meta.fields + '__all__'


class EmployeeType(UsersType):
    class Meta(UsersType.Meta):
        model = Employee
        fields = UsersType.Meta.fields + '__all__'

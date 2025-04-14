import graphene

from app.users.models import Employee
from app.users.schema import EmployeeType


class EmployeeQuery(graphene.ObjectType):
    all_employees = graphene.List(EmployeeType)

    def resolve_all_employees(root, info):
        return Employee.objects.all()


class CreateEmployee(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=True)
        password = graphene.String(required=True)
        job_title = graphene.String(required=True)
        job_description = graphene.String(required=True)
        contract_type = graphene.String(required=True)

    employee = graphene.Field(EmployeeType)

    def mutate(self, info, username, first_name, last_name, email, phone, password, job_title, job_description,
               contract_type):
        if Employee.objects.filter(email=email).exists():
            raise Exception('Email already registered.')
        if Employee.objects.filter(username=username).exists():
            raise Exception('Username already registered')

        employee = Employee(username=username, first_name=first_name, last_name=last_name, email=email, phone=phone,
                            job_title=job_title,
                            job_description=job_description, contract_type=contract_type, role='employee')
        employee.set_password(password)
        employee.save()

        return CreateEmployee(employee=employee)


class UpdateEmployee(graphene.Mutation):
    class Arguments:
        IM = graphene.ID(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        phone = graphene.String()
        password = graphene.String()
        job_title = graphene.String()
        job_description = graphene.String()
        contract_type = graphene.String()

    employee = graphene.Field(EmployeeType)

    def mutate(self, info, IM, first_name=None, last_name=None, email=None, phone=None, password=None,
               job_title=None,
               job_description=None, contract_type=None):
        try:
            employee = Employee.objects.get(IM=IM)
        except Employee.DoesNotExist:
            raise Exception('Employee does not exist.')

        if first_name is not None:
            employee.first_name = first_name.strip()
        if last_name is not None:
            employee.last_name = last_name.strip()
        if email is not None:
            employee.email = email.strip()
        if phone is not None:
            employee.phone = phone.strip()
        if password is not None:
            employee.set_password(password)
        if job_title is not None:
            employee.job_title = job_title.strip()
        if job_description is not None:
            employee.job_description = job_description.strip()
        if contract_type is not None:
            employee.contract_type = contract_type.strip()

        employee.save()

        return UpdateEmployee(employee=employee)


class DeleteEmployee(graphene.Mutation):
    class Arguments:
        IM = graphene.ID(required=True)

    ok = graphene.Boolean()
    employee = graphene.Field(EmployeeType)

    def mutate(self, info, IM):
        try:
            employee = Employee.objects.get(IM=IM)
        except Employee.DoesNotExist:
            raise Exception('Employee does not exist.')

        employee.delete()

        return DeleteEmployee(ok=True, employee=employee)


class EmployeeMutation(graphene.ObjectType):
    create_employee = CreateEmployee.Field()
    update_employee = UpdateEmployee.Field()
    delete_employee = DeleteEmployee.Field()

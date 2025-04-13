import graphene

from app.users.models import HrAdvisor
from app.users.schema import HrAdvisorType


class HrAdvisorQuery(graphene.ObjectType):
    all_hr_advisors = graphene.List(HrAdvisorType)

    def resolve_all_hr_advisors(root, info):
        return HrAdvisor.objects.all()


class CreateHrAdvisor(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=True)
        password = graphene.String(required=True)
        department = graphene.String(required=True)

    hr_advisor = graphene.Field(HrAdvisorType)

    def mutate(self, info, first_name, last_name, email, phone, password, department):
        if HrAdvisor.objects.filter(email=email).exists():
            raise Exception('Email already registered.')
        hr_advisor = HrAdvisor(first_name=first_name, last_name=last_name, email=email, phone=phone, role='hr',
                               department=department)
        hr_advisor.set_password(password)
        hr_advisor.save()

        return CreateHrAdvisor(hr_advisor=hr_advisor)


class UpdateHrAdvisor(graphene.Mutation):
    class Arguments:
        IM = graphene.ID(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        phone = graphene.String()
        password = graphene.String()
        department = graphene.String()

    hr_advisor = graphene.Field(HrAdvisorType)

    def mutate(self, info, IM, first_name=None, last_name=None, email=None, phone=None, password=None, department=None):
        try:
            hr_advisor = HrAdvisor.objects.get(IM=IM)
        except HrAdvisor.DoesNotExist:
            raise Exception('HrAdvisor does not exist.')

        if first_name is not None:
            hr_advisor.first_name = first_name.strip()
        if last_name is not None:
            hr_advisor.last_name = last_name.strip()
        if email is not None:
            hr_advisor.email = email.strip()
        if phone is not None:
            hr_advisor.phone = phone.strip()
        if password is not None:
            hr_advisor.set_password(password)
        if department is not None:
            hr_advisor.department = department.strip()

        hr_advisor.save()

        return UpdateHrAdvisor(hr_advisor=hr_advisor)


class DeleteHrAdvisor(graphene.Mutation):
    class Arguments:
        IM = graphene.ID(required=True)

    ok = graphene.Boolean()
    hr_advisor = graphene.Field(HrAdvisorType)

    def mutate(self, info, IM):
        try:
            hr_advisor = HrAdvisor.objects.get(IM=IM)
        except HrAdvisor.DoesNotExist:
            raise Exception('HrAdvisor does not exist.')

        hr_advisor.delete()

        return DeleteHrAdvisor(ok=True, hr_advisor=hr_advisor)


class HrAdvisorMutation(graphene.ObjectType):
    create_hr_advisor = CreateHrAdvisor.Field()
    update_hr_advisor = UpdateHrAdvisor.Field()
    delete_hr_advisor = DeleteHrAdvisor.Field()

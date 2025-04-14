import graphene

from app.insurance_company.models import InsuranceCompany
from app.insurance_company.schema import InsuranceCompanyType


class InsuranceCompanyQuery(graphene.ObjectType):
    all_companies = graphene.List(InsuranceCompanyType)

    def resolve_all_companies(root, info):
        return InsuranceCompany.objects.all()


class CreateInsuranceCompany(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        address = graphene.String(required=True)
        phone = graphene.String(required=True)
        email = graphene.String(required=True)

    insurance_company = graphene.Field(InsuranceCompanyType)

    def mutate(self, info, name, address, phone, email):
        # authorization
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be connected to perform this action")
        if user.role != "hr":
            raise Exception("You must be Hr Advisor to perform this action")

        insurance_company = InsuranceCompany(name=name, address=address, phone=phone, email=email)
        insurance_company.save()

        return CreateInsuranceCompany(insurance_company=insurance_company)


class UpdateInsuranceCompany(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        address = graphene.String()
        phone = graphene.String()
        email = graphene.String()

    insurance_company = graphene.Field(InsuranceCompanyType)

    def mutate(self, info, id, name=None, address=None, phone=None, email=None):
        # authorization
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be connected to perform this action")
        if user.role != "hr":
            raise Exception("You must be Hr Advisor to perform this action")

        try:
            insurance_company = InsuranceCompany.objects.get(id=id)
        except InsuranceCompany.DoesNotExist:
            raise Exception('Insurance company does not exist')

        if name is not None:
            insurance_company.name = name
        if address is not None:
            insurance_company.address = address
        if phone is not None:
            insurance_company.phone = phone
        if email is not None:
            insurance_company.email = email

        insurance_company.save()

        return UpdateInsuranceCompany(insurance_company=insurance_company)


class DeleteInsuranceCompany(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    insurance_company = graphene.Field(InsuranceCompanyType)

    def mutate(self, info, id):
        # authorization
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be connected to perform this action")
        if user.role != "hr":
            raise Exception("You must be Hr Advisor to perform this action")

        try:
            insurance_company = InsuranceCompany.objects.get(id=id)
        except InsuranceCompany.DoesNotExist:
            raise Exception('Insurance company does not exist')

        insurance_company.delete()

        return DeleteInsuranceCompany(ok=True, insurance_company=insurance_company)


class InsuranceCompanyMutation(graphene.ObjectType):
    create_company = CreateInsuranceCompany.Field()
    update_company = UpdateInsuranceCompany.Field()
    delete_company = DeleteInsuranceCompany.Field()

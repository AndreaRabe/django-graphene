import graphene

from app.insurance.models import Insurance
from app.insurance.schema import InsuranceType
from app.insurance_company.models import InsuranceCompany
from app.users.models import User


class InsuranceQuery(graphene.ObjectType):
    all_insurances = graphene.List(InsuranceType)

    def resolve_all_insurances(root, info):
        return Insurance.objects.all()


class CreateInsurance(graphene.Mutation):
    class Arguments:
        user = graphene.ID(required=True)
        insurance_company = graphene.ID(required=True)
        start_date = graphene.Date(required=True)
        end_date = graphene.Date(required=True)

    insurance = graphene.Field(InsuranceType)

    def mutate(self, info, user, insurance_company, start_date, end_date):
        insurance = Insurance(user=User.objects.get(pk=user),
                              insurance_company=InsuranceCompany.objects.get(pk=insurance_company),
                              start_date=start_date, end_date=end_date)
        insurance.save()

        return CreateInsurance(insurance=insurance)


class UpdateInsurance(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        start_date = graphene.Date()
        end_date = graphene.Date()

    insurance = graphene.Field(InsuranceType)

    def mutate(self, info, id, start_date=None, end_date=None):
        try:
            insurance = Insurance.objects.get(id=id)
        except Insurance.DoesNotExist:
            raise Exception('Insurance does not exist')

        if start_date is not None:
            insurance.start_date = start_date
        if end_date is not None:
            insurance.end_date = end_date

        insurance.save()

        return UpdateInsurance(insurance=insurance)


class DeleteInsurance(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    insurance = graphene.Field(InsuranceType)

    def mutate(self, info, id):
        try:
            insurance = Insurance.objects.get(id=id)
        except Insurance.DoesNotExist:
            raise Exception('Insurance does not exist')

        insurance.delete()

        return DeleteInsurance()


class InsuranceMutation(graphene.ObjectType):
    create_insurance = CreateInsurance.Field()
    update_insurance = UpdateInsurance.Field()
    delete_insurance = DeleteInsurance.Field()

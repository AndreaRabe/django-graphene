import graphene

from app.insurance.models import Insurance
from app.insurance.schema import InsuranceType
from app.insurance_company.models import InsuranceCompany
from app.notification.views import notify_user
from app.users.models import User


class InsuranceQuery(graphene.ObjectType):
    all_insurances = graphene.List(InsuranceType)

    search_employee = graphene.List(InsuranceType, IM=graphene.String(), Username=graphene.String())

    def resolve_all_insurances(root, info):
        return Insurance.objects.all()

    def resolve_search_employee(root, info, IM=None, Username=None):
        queryset = Insurance.objects.all()
        if IM:
            queryset = queryset.filter(user__IM__icontains=IM)
        if Username:
            queryset = queryset.filter(user__username__icontains=Username)
        return queryset


class CreateInsurance(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        insurance_company = graphene.ID(required=True)
        beneficiary = graphene.String(required=True)
        start_date = graphene.Date(required=True)
        end_date = graphene.Date(required=True)

    insurance = graphene.Field(InsuranceType)

    def mutate(self, info, user_id, insurance_company, beneficiary, start_date, end_date):
        # authorization
        user_details = info.context.user
        if user_details.is_anonymous:
            raise Exception("You must be connected to perform this action")
        if user_details.role != "hr":
            raise Exception("You must be Hr Advisor to perform this action")

        user_data = User.objects.get(pk=user_id)
        insurance_company_data = InsuranceCompany.objects.get(pk=insurance_company)

        insurance = Insurance(user=user_data,
                              insurance_company=insurance_company_data,
                              start_date=start_date, end_date=end_date, beneficiary=beneficiary)
        insurance.save()

        return CreateInsurance(insurance=insurance)


class UpdateInsurance(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        beneficiary = graphene.String()
        start_date = graphene.Date()
        end_date = graphene.Date()

    insurance = graphene.Field(InsuranceType)

    def mutate(self, info, id, start_date=None, beneficiary=None, end_date=None):
        # authorization
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be connected to perform this action")
        if user.role != "hr":
            raise Exception("You must be Hr Advisor to perform this action")

        try:
            insurance = Insurance.objects.get(id=id)
        except Insurance.DoesNotExist:
            raise Exception('Insurance does not exist')

        if start_date is not None:
            insurance.start_date = start_date
        if end_date is not None:
            insurance.end_date = end_date
        if beneficiary is not None:
            insurance.beneficiary = beneficiary
            notify_user(insurance.user, "Modification d'assurance", f"Bénéficiaire mis à jour : {beneficiary}")

        insurance.save()

        return UpdateInsurance(insurance=insurance)


class DeleteInsurance(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()
    insurance = graphene.Field(InsuranceType)

    def mutate(self, info, id):
        # authorization
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be connected to perform this action")
        if user.role != "hr":
            raise Exception("You must be Hr Advisor to perform this action")

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

from graphene_django import DjangoObjectType

from app.insurance_company.models import InsuranceCompany


class InsuranceCompanyType(DjangoObjectType):
    class Meta:
        model = InsuranceCompany
        fields = '__all__'

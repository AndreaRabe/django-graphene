from graphene_django import DjangoObjectType

from app.insurance.models import Insurance


class InsuranceType(DjangoObjectType):
    class Meta:
        model = Insurance
        fields = '__all__'

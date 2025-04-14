from graphene_django import DjangoObjectType

from app.notification.models import Notification


class NotificationType(DjangoObjectType):
    class Meta:
        model = Notification
        fields = '__all__'

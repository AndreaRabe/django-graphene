import uuid

from django.db import models


# Create your models here.
class Insurance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.UUIDField()
    insurance_company = models.UUIDField()
    beneficiary = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        app_label = "insurance"  # name of app in installed apps

    def __str__(self):
        return f"Assurance de : {self.user} avec la company {self.insurance_company}. Date : {self.start_date} | {self.end_date}"

import uuid

from django.db import models

from app.insurance_company.models import InsuranceCompany
from app.users.models import User


# Create your models here.
class Insurance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='insurances')
    insurance_company = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE, related_name='insurances')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Assurance de : {self.user} avec la company {self.insurance_company}. Date : {self.start_date} | {self.end_date}"

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('hr', 'Conseiller RH'),
        ('employee', 'Employé'),
    ]
    IM = models.AutoField(primary_key=True, editable=False)
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (IM: {self.IM})"


class HrAdvisor(User):
    department = models.CharField(max_length=50)

    def __str__(self):
        return f"Conseiller RH du departement : {self.department}"


class Employee(User):
    CONTRACT_TYPE_CHOICES = [
        ("CDI", "CDI"),
        ("CDD", "CDD"),
        ("Stage", "Stage"),
        ("Freelance", "Freelance"),
    ]

    job_title = models.CharField(max_length=50)
    job_description = models.TextField()
    contract_type = models.CharField(max_length=50, choices=CONTRACT_TYPE_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job_title}"

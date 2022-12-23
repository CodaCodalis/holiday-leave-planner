from django.contrib.auth.models import AbstractUser
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=30)
    head = models.ForeignKey(
        "Employee",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name[:50]


class Division(models.Model):
    name = models.CharField(max_length=30)
    department = models.ForeignKey(
        "Department",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    head = models.ForeignKey(
        "Employee",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name[:50]


class Team(models.Model):
    name = models.CharField(max_length=30)
    head = models.ForeignKey(
        "Employee",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    MIN_ATTENDANCE_CHOICES = [
        (0.0, "0%"),
        (0.25, "25%"),
        (0.33, "33%"),
        (0.5, "50%"),
        (0.66, "66%"),
        (0.75, "75%"),
        (1.0, "100%"),
    ]
    division = models.ForeignKey(
        "Division",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name[:50]


class Employee(AbstractUser):
    reg_num = models.PositiveIntegerField(null=True, blank=True)
    supervisor = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    team = models.ForeignKey(
        "Team",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    role = [
        ("HODep", "head of department"),
        ("HODiv", "head of division"),
        ("HOT", "head of team"),
        ("Emp", "employee"),
    ]

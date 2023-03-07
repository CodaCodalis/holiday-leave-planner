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
        related_name='head_team',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class MinAttendance(models.TextChoices):
        ZERO = ("0", "0%")
        QUARTER = ("25", "25%")
        THIRD = ("33", "33%")
        HALF = ("50", "50%")
        TWOTHIRD = ("66", "66%")
        THREEQUARTER = ("75", "75%")
        ALL = ("100", "100%")

    min_attendance = models.CharField(
        max_length=3,
        choices=MinAttendance.choices,
        default=100,
    )

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
        null=False,
        blank=False,
    )
    team = models.ForeignKey(
        "Team",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    class Role(models.TextChoices):
        HODEP = ("HODep", "Head of Department")
        HODIV = ("HODiv", "Head of Division")
        HOT = ("HOT", "Head of Team")
        EMP = ("Emp", "Employee")

    role = models.CharField(
        max_length=5,
        choices=Role.choices,
        default="Emp",
    )

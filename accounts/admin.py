from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import EmployeeCreationForm, EmployeeChangeForm
from .models import Employee, Team, Division, Department

admin.site.register(Team)
admin.site.register(Division)
admin.site.register(Department)


class EmployeeAdmin(UserAdmin):
    add_form = EmployeeCreationForm
    form = EmployeeChangeForm
    model = Employee
    list_display = [
        "username",
        "email",
        "reg_num",
        "supervisor",
        "team",
        "ROLE_CHOICES",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("reg_num",
                                                          "supervisor",
                                                          "team",
                                                          "ROLE_CHOICES",
                                                          )}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("first_name",
                                                                  "last_name",
                                                                  "username",
                                                                  "email",
                                                                  "reg_num",
                                                                  "supervisor",
                                                                  "team",
                                                                  "ROLE_CHOICES",
                                                                  )}),)


admin.site.register(Employee, EmployeeAdmin)

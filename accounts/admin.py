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
        "division",
        "team",
        "role",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("reg_num",
                                                          "supervisor",
                                                          "division",
                                                          "team",
                                                          "role",
                                                          )}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("first_name",
                                                                  "last_name",
                                                                  "email",
                                                                  "reg_num",
                                                                  "supervisor",
                                                                  "division",
                                                                  "team",
                                                                  "role",
                                                                  )}),)


admin.site.register(Employee, EmployeeAdmin)

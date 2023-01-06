from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Department, Division, Team, Employee
from django.urls import reverse


class SignupTests(TestCase):
    def test_signup_view_url_location(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)

    def test_signup_view_name(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_form(self):
        Employee.objects.create(username="hodep", email="a@bc.de", first_name="B", last_name="Oss", reg_num="111100", role="HODep")
        Department.objects.create(name="dep_1", head_id=1)
        Division.objects.create(name="div_1", department_id=1, head_id=1)
        Team.objects.create(name="team_1", min_attendance="0", division_id=1, head_id=1)

        response = self.client.post(
            reverse("signup"),
            {
                "username": "testuser",
                "email": "testuser@email.com",
                "first_name": "Arb",
                "last_name": "Eitstier",
                "reg_num": "111111",
                "supervisor": "1",
                "team": "1",
                "role": "Emp",
                "password1": "testpass123",
                "password2": "testpass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.all().count(), 2)
        self.assertEqual(get_user_model().objects.all()[0].username, "hodep")
        self.assertEqual(get_user_model().objects.all()[1].username, "testuser")
        self.assertEqual(get_user_model().objects.all()[1].email, "testuser@email.com")
        self.assertEqual(get_user_model().objects.all()[1].first_name, "Arb")
        self.assertEqual(get_user_model().objects.all()[1].last_name, "Eitstier")
        self.assertEqual(get_user_model().objects.all()[1].reg_num, 111111)
        self.assertEqual(get_user_model().objects.all()[1].supervisor.first_name, "B")
        self.assertEqual(get_user_model().objects.all()[1].team.name, "team_1")
        self.assertEqual(get_user_model().objects.all()[1].role, "Emp")

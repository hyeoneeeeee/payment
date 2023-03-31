from rest_framework.test import APITestCase
from django.urls import reverse
from user.models import UserModel
# Create your tests here.

# class UserSignUpLoginAPITest(APITestCase):
#     def test_signup(self):
#         url = reverse('sign_up_view')
#         user_data = {
#             "user_id":"z9x80123@gmail.com",
#             "password":"a123456789"
#         }
#         response = self.client.post(url, user_data)
#         self.assertEqual(response.status_code, 200)


# class UserLogInTest(APITestCase):

#     def setUp(self):
#         self.urls = reverse("login_view")
#         self.data = {
#             "user_id":"z9x80123@gmail.com",
#             "password":"a123456!"
#         }
#         self.user = UserModel.objects.create_user(user_id="z9x80123@gmail.com", password="a123456!")

#     def test_login(self):
#         response = self.client.post(self.urls, self.data)
#         self.assertEqual(response.status_code, 200)



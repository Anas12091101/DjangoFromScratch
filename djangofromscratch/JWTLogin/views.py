from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# Create your views here.


class CheckLogin(APIView, TemplateView):
    permission_classes = [IsAuthenticated]
    template_name = "LoginCheck/success.html"


check_login = CheckLogin.as_view()

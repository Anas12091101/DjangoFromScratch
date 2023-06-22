from django.core.mail import EmailMessage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


def send_email(user):
    email = EmailMessage(
        "Welcome to DjangoFromScratch",
        f"Hi {user.email}, Welcome to DjangoFromScratch. We hope you enjoy our product and have a good time here",
        "muhammad.anas@arbisoft.com",
        [user.email],
        reply_to=["muhammad.anas@arbisoft.com"],
    )
    email.send(fail_silently=False)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_login(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(["POST"])
def register_user(request):
    data = request.data
    try:
        user = User.objects.create_user(password=data["password"], email=data["email"])
        send_email(user)
        return Response({"Success": "User Registered"})
    except Exception as e:
        return Response({"Failed": str(e)})

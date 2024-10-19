from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User


class RegisterView(APIView):

    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        if not phone_number:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            user = User.objects.create_user(phone_number=phone_number, password=password)

        return Response({'username': user.username, 'phone_number': phone_number}, status=status.HTTP_201_CREATED)

from django.contrib.auth import logout
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.models import Officer
from attendance.permissions import IsOwner
from attendance.serializer import OfficerSerializer


class OfficerViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwner)
    queryset = Officer.objects.all()
    serializer_class = OfficerSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.dict()
        user = Officer(username=data['username'], first_name=data['first_name'], last_name=data['last_name'], phone=data['phone'],
                       email=data['email'], office_latitude=data['office_latitude'],
                       office_longitude=data['office_longitude'], office_time_entry=data['office_time_entry'])
        user.set_password(request.data['password'])
        user.save()
        serializer = self.get_serializer(user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class LogoutView(APIView):
    authentication_class = [TokenAuthentication]

    def post(self, request):
        print(request.user.username)

        # print(Token.objects.filter(user=request.user))
        request.user.auth_token.delete()
        logout(request)
        return Response({"message": "Logout Successfull"}, status=204)
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from account.models import User
from .models import Message
from rest_framework.response import Response
from .serializers import MessageSerializer

@permission_classes((IsAuthenticated,))
@authentication_classes([JWTAuthentication])
class MessageList(APIView):
    def get(self,request):
        user = request.user
        messages = Message.objects.filter(user = user)
        response = MessageSerializer(messages,many = True).data
        return Response(response)

    def post(self,request):
        message = Message.objects.get(id = request.data["id"])
        message.read = True
        return Response(status = 200,data ={"message":"success"})

    def delete(self,request):
        user = request.user
        # user = User.objects.get(id = 1)
        messages = Message.objects.filter(user = user,id__in = request.data["id"])
        for message in messages:
            message.delete()
        return Response(status=200)

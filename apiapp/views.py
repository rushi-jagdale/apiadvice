from django.shortcuts import render
from .models import CreateUser,Advisor
from .serializers import  AdvisorSerializer, UserSerializer,Registration
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.conf import settings   
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.decorators import api_view, permission_classes,authentication_classes     
from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
# Create your views here.


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@api_view(['POST'],)
def registration_view(request):
    if request.method == "POST":
        serializer = Registration(data = request.data)
        data={}
        if serializer.is_valid():

            account = serializer.save()
            data['username'] = account.username
            data['email'] = account.email
            token = Token.objects.get(user=account).key
            data['token'] = token
            data['Response'] = "Registration success "
            return Response(data)
    else:
        msg={'msg':"no request "}
        return Response(msg)

@api_view(['POST'],)
@authentication_classes([TokenAuthentication,BasicAuthentication])
@permission_classes([AllowAny])
def logout(request):
    if request.method == "POST":
       
        request.user.auth_token.delete()
        return Response(
            {
                "msg":"you are logout "
            }
        )


@api_view(['GET','POST','PATCH','DELETE','PUT'])
@authentication_classes([TokenAuthentication,BasicAuthentication])
@permission_classes([IsAuthenticated])
def book_api(request):
    if request.method == "GET":
        stu=CreateUser.objects.all()
        print((stu))
        serializer  = UserSerializer(stu,many=True)
        msg={'msg':" No data"}
        print(serializer.data)
        return Response(serializer.data)
       

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication,BasicAuthentication])
@permission_classes([IsAuthenticated])
def fav_api(request):
    if request.method == "GET":
            stu=Advisor.objects.all()
            print((stu))
            serializer  = AdvisorSerializer(stu,many=True)
            msg={'msg':" apka favourite abhi koi  nhi hai phle kuch add kro phir dekho"}
            print(serializer.data)
            return Response(serializer.data)


    if request.method == "POST":
       
        stu=CreateUser.objects.get(user_id=request.user)
        myd = stu
       
        
        iscorrectuser = request.data['khiladi'] 
       
        if iscorrectuser == str(myd.id):
            serializer = AdvisorSerializer(data=request.data)
            print(serializer)
            if serializer.is_valid(): 
                serializer.save()
                msg= {'msg':'data is inserted check in database'}
                return Response(msg)
            else:
                return Response(serializer.errors)
        else:
            msg= {'msg':'Not Allowed '}
            return Response(msg)
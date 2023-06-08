from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from Account.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, SendPasswordResetEmailSerializer, UserPasswordResetSerializer

from django.shortcuts import render

# from account.renderers import UserRenderer

from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication



## Create your views here.-----------------------------------------------------------------------------------
# NOTE ------------( Fontend এ Error Meggege আছে তা বুজানোর জন্যে  )--------------------
from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
  charset='utf-8'
  def render(self, data, accepted_media_type=None, renderer_context=None):
    response = ''
    if 'ErrorDetail' in str(data):
      response = json.dumps({'errors':data})
    else:
      response = json.dumps(data)
    
    return response
#_______________________________________________________________________________________

# NOTE ------------( Creating tokens manually )------------------------------------------
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# ________________________________________________________________________________________


# NOTE ------------------( User Registration View )--------------------------------------------
# URL = ( http://127.0.0.1:8000/register/ )
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)   ## Token Genaret
            # return Response({'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
            return Response({'token': token,'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#_________________________________________________________________________________________


# NOTE ------------------------( User Login View )---------------------------------------------
# যদি username, password এর মাধ্যমে আমরা Login কোরতে চাই তবে এই ভাবে করতে হবে।
# URL = ( http://127.0.0.1:8000/login/ )
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get('username')
            password = serializer.data.get('password')

            user = authenticate(username= username , password=password)            

            if user is not None:
                token = get_tokens_for_user(user)   ## Token Genaret
                return Response({'token': token,'msg':'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
                        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# যদি email, password এর মাধ্যমে আমরা Login কোরতে চাই তবে এই ভাবে করতে হবে।
"""
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
        
            try:
                usr = User.objects.get(email = email)
                if usr:
                    authenticate(username= usr.username , password=password)
                    # token = CustomAuthToken(usr)  # Token Genaret           
                    return Response({'token': 'token','msg':'Login Success'}, status=status.HTTP_200_OK)
                
            except User.DoesNotExist:
                return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
#________________________________________________________________________________________


# NOTE ------------------------( User Profile View )-----------------------------------------
# URL = ( http://127.0.0.1:8000/profile/ )
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
#______________________________________________________________________________________


# NOTE ------------------------( ChangePasswor View )----------------------------------
# URL = ( http://127.0.0.1:8000/change-password/ )
class UserChangePasswordView(APIView):

    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        serializer.is_valid(raise_exception=True) # password টি কে  serializaer এর ভেতর save করানো হয়েছে।
        return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
    """
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Successfully'}, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # NOTE raise_exception = True হয়ে গেলে নিচের return Response(serializer.errors) code আর exicution হয় না।
               তাই fontend developer দের বুঝতে problem হয় কোন ধরনের error হয়েছে এর জন্যে নিচের code টিকে লিখা হয়নি, 
               এটিকে উপরে if condition ছাড়া লেখা হয়েছে। তবে এখানে কোন error থাকলে তা যদি আমরা fontend এ পাঠাতে
               চাই তবে UserRenderer Class টি create করার মাধ্যমে তা বলে দিতে পারবো।
               এটিকে Class based view ভেতরে আমরা class এর নিচে এই ভাবে declare করতে পারি,
               renderer_classes = [UserRenderer]

        
    """
#______________________________________________________________________________________



# NOTE -----------------( Passord Reset Email Send With Link/OTP View )----------------
# URL = ( http://127.0.0.1:8000/reset-password-email-send/ )
class SendPasswordResetEmailView(APIView):
    
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)
#______________________________________________________________________________________



# NOTE ---( Passord Reset Email Send Link/OTP Verify and New Password Set View )-------
# IF Link verification:-
# class UserPasswordResetView(APIView):
#     renderer_classes = [UserRenderer]
#     def post(self, request, uid, token, format=None):
#         serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
#         serializer.is_valid(raise_exception=True)
#         return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
    
# IF OTP Verification:-
class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
#______________________________________________________________________________________
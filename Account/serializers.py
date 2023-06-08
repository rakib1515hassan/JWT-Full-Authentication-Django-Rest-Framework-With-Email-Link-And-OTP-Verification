# from django.contrib.sessions import serializers
from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import datetime, timedelta

from Account.models import User_OTP

# Sending Mail
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password


# NOTE ----------------------------------( Registration Serialize )------------------------------------
class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type':'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type':'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password':{'write_only':True}
        }
    # Validating Password and Confirm Password while Registration
    def validate(self, attrs): # attrs means data
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        return attrs
    # NOTE An alternative way for password validation
    """
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs
    """

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user
#______________________________________________________________________________________________________    


# NOTE --------------------------------------( Login Serialize )--------------------------------------
# If Email:-

# class UserLoginSerializer(serializers.ModelSerializer):
#   email = serializers.EmailField(max_length=255)
#   class Meta:
#     model = User
#     fields = ['email', 'password']

# If username:-
class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25)
    class Meta:
        model = User
        fields = ['username', 'password']

#_____________________________________________________________________________________________________


# NOTE ------------------------------------( Profile Serialize )--------------------------------------
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email',]
#_____________________________________________________________________________________________________



# NOTE --------------------------------( ChangePasswor Serialize )------------------------------------
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):   # attrs means data
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user') # যেই user আমরা view.py function এর context এর মাধ্যমে send করেছি তা receive করা হয়েছে
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs
#_____________________________________________________________________________________________________


# NOTE -----------------------------( Reset Passwor Email Send Serialize )---------------------------------
# For Link
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError

# For OTP
import random

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email = email)

            # Django সেশনে email স্টোর করুন
            self.context['request'].session['email'] = email

            # NOTE If You send link on your email-------------------------------------
            # uid = urlsafe_base64_encode(force_bytes(user.id))
            # print('Encoded UID', uid)

            # token = PasswordResetTokenGenerator().make_token(user)  # আমরা যদি একটি time set করে দিতে চাই, জাতে ঐ সময় পর 
            # print('Password Reset Token', token)                    # user ঐ token দিয়ে আর verify না করতে পারে। 
            #                                                         # এর জন্যে PASSWORD_RESET_TIMEOUT = 300 অর্থাত 5min set করা হয়েছে।

            # link = 'http://127.0.0.1:8000/reset-password-email-verify/'+uid+'/'+token  # যেহেতু এই link এ click কোরলে react.js or vue.js run
            # print('Password Reset Link', link)                            # কোরবে, তাই সেই localhost এর link দিতে হবে।

            # body = 'Click Following Link to Reset Your Password '+link


            # NOTE If You send OTP on your email-------------------------------------
            otp = random.randint(100000, 999999)

            #Django সেশনে টাইমআউট সেট করুন
            timeout_datetime = datetime.now() + timedelta( minutes = 5 )
            self.context['request'].session['timeout'] = timeout_datetime.timestamp()

            if User_OTP.objects.filter(user = user).exists(): # পুরাতন otp থাকলে তাকে এখনে delete করে দিবে
                User_OTP.objects.get(user = user).delete()

            otp_obj = User_OTP.objects.create(user = user, otp=otp)
            print("Your OTP = ", otp)
            print("Your Object = ", otp_obj)

            body = f"Hello {user.first_name}{user.last_name},\nYour OTP is {otp}\nThanks!"
            #-------------------------------------------------------------------------

            ## Send EMail-------------------------------------------------------------
            send_mail(
                "Reset Your Password",     # Subject
                body,                      # Body
                settings.EMAIL_HOST_USER,  # From
                [user.email],              # To
                fail_silently = False
            )
            #_________________________________________________________________________
            return attrs
        else:
            raise serializers.ValidationError('You are not a Registered User')
#_____________________________________________________________________________________________________



# NOTE -----------------------------( Reset Passwor Email Verify Serialize )---------------------------------

# NOTE IF Link Verification------------------------

# class UserPasswordResetSerializer(serializers.Serializer):
#     password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
#     password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
#     class Meta:
#         fields = ['password', 'password2']

#     def validate(self, attrs):
#         try:
#             password = attrs.get('password')
#             password2 = attrs.get('password2')

#             uid = self.context.get('uid')
#             token = self.context.get('token')

#             if password != password2:
#                 raise serializers.ValidationError("Password and Confirm Password doesn't match")
            
#             id = smart_str(urlsafe_base64_decode(uid))
#             user = User.objects.get(id=id)

#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 raise serializers.ValidationError('Token is not Valid or Expired')
#             user.set_password(password)
#             user.save()
#             return attrs
        
#         except DjangoUnicodeDecodeError as identifier:
#             PasswordResetTokenGenerator().check_token(user, token)
#             raise serializers.ValidationError('Token is not Valid or Expired')



# NOTE IF OTP Verification-----------------------

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    otp = serializers.IntegerField()
    class Meta:
        fields = ['password', 'password2', 'otp']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        otp = attrs.get('otp')
        
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        
        # যেই email and OTP_timeout আমরা serializers.py  এর SendPasswordResetEmailSerializer class থেকে Django session এর মাধ্যমে 
        # send করেছি তা receive করা হয়েছে email এবং timeout_timestamp veriable এর ভেতর।
        email = self.context['request'].session.get('email')
        timeout_timestamp = self.context['request'].session.get('timeout')

        timeout_datetime = datetime.fromtimestamp(timeout_timestamp)
        if datetime.now() > timeout_datetime:
            raise serializers.ValidationError("OTP verification time has expired")

        user_obj = User.objects.get(email = email) 
        # otp_obj = User_OTP.objects.get(user = user)

        otp_obj = User_OTP.objects.get(user = User.objects.get(email=email))

        print("---------------------------")
        print(f"Request User = {User.objects.get(email=email)}, Correct OTP = {otp_obj.otp}")
        print("---------------------------")

        
        
        if otp != otp_obj.otp:
            raise serializers.ValidationError("Your OTP doesn't match")

        user_obj.set_password(password)
        user_obj.save()
        return attrs
    
#_____________________________________________________________________________________________________





# --------------------------------( JWT Token )----------------------------------------
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super(MyTokenObtainPairSerializer, cls).get_token(user)

#         # Add custom claims
#         token['username'] = user.username
#         return token
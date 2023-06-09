# NOTE) Simple JWT can be installed with pip:-

    *) pip install djangorestframework-simplejwt

# NOTE) Project Configuration:-

    i) settings.py
        REST_FRAMEWORK = {
            ...
            'DEFAULT_AUTHENTICATION_CLASSES': (
                ...
                'rest_framework_simplejwt.authentication.JWTAuthentication',
            )
            ...
        }
        INSTALLED_APPS = [
            ...
            'rest_framework_simplejwt',
            ...
        ]

    ii) Some of Simple JWT’s behavior can be customized through settings variables in settings.py:
        from datetime import timedelta

        SIMPLE_JWT = {
            "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
            "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
            "ROTATE_REFRESH_TOKENS": False,
            "BLACKLIST_AFTER_ROTATION": False,
            "UPDATE_LAST_LOGIN": False,

            "ALGORITHM": "HS256",
            "SIGNING_KEY": settings.SECRET_KEY,
            "VERIFYING_KEY": "",
            "AUDIENCE": None,
            "ISSUER": None,
            "JSON_ENCODER": None,
            "JWK_URL": None,
            "LEEWAY": 0,

            "AUTH_HEADER_TYPES": ("Bearer",),
            "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
            "USER_ID_FIELD": "id",
            "USER_ID_CLAIM": "user_id",
            "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

            "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
            "TOKEN_TYPE_CLAIM": "token_type",
            "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

            "JTI_CLAIM": "jti",

            "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
            "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
            "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

            "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
            "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
            "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
            "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
            "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
            "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
        }

    iii) urls.py
        from rest_framework_simplejwt.views import (
            TokenObtainPairView,
            TokenRefreshView,
        )

        urlpatterns = [

            path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
            path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
            
            # For TokenVerifyView
            path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'), 
        
        ]


# NOTE) আমরা যখন api কে কোন frontend (react, vue) এ add কবি তখন একটি common error face করি তা হল CORS Policy Error,
        যা সমাধান করার জন্যে আমাদের একটি librarry install করা লাগবে 

    i) pip install django-cors-headers

    ii) INSTALLED_APPS = [
            "corsheaders",
        ]
    
    iii) Comma Middleware এর উপরে add করতে হবে

        MIDDLEWARE = [
            'corsheaders.middleware.CorsMiddleware',
            'django.middleware.common.CommonMiddleware',
        ]
    
    iv) যেহেতু এটি react.js or vue.js এ run কোরবে তাই,
        CORS_ALLOWED_ORIGINS = [
            "https://example.com",        # example এর জায়গায় your Domain বসবে।
            "https://sub.example.com",    # sub.example এর জায়গায় your Sub-Domain বসবে।
            
            "http://localhost:3000",      # react.js and vue.js এর জন্যে 
            "http://127.0.0.1:3000",
        ]


import jwt
import json
from rest_framework_jwt.settings import api_settings
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from user.models import Member

JWT_DECODE_HANDLER = api_settings.JWT_DECODE_HANDLER

def login_check(func):
    
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            #Decode - jwt.decode(access_token, SECRET_KEY, algorithm=ALGORITHM)
            payload = JWT_DECODE_HANDLER(access_token)
            user_id = Member.objects.get(uuid=payload['user_id'])
            request.user = user_id

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID TOKEN'}, status = 400)

        except Member.DoesNotExist:
            return JsonResponse({'message': 'INVALID USER'}, status = 400)

        return func(self, request, *args, **kwargs)

    return wrapper
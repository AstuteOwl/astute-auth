import datetime
import random
from VerificationEmail import VerificationEmail

from astute_auth.auth_service.request_serializers import TokenRequestSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from jwt import generate_jwt
from astute_auth import settings
from rest_framework.response import Response

from models import UserVerification


@api_view(['POST'])
@csrf_exempt
def token(request):
	data = JSONParser().parse(request)
	token_serializer = TokenRequestSerializer(data=data)

	if not token_serializer.is_valid():
		return JsonResponse(status=status.HTTP_400_BAD_REQUEST)

	email = token_serializer.validated_data['email']
	password = token_serializer.validated_data['password']

	if User.objects.filter(username=email).exists():
		user = authenticate(username=email, password=password)
		if user is None:
			return Response(status=status.HTTP_401_UNAUTHORIZED)
		else:
			if user.is_active:
				claims = {'email': email, 'permissions': list(user.get_all_permissions())}
				jwt = generate_jwt(claims, settings.HMAC_SECRET, 'HS512', datetime.timedelta(days=365))
				response_data = {'token':jwt}
				return JsonResponse(response_data, status=status.HTTP_201_CREATED)
			else:
				return Response(status=status.HTTP_202_ACCEPTED)
	else:
		user = User.objects.create_user(username=email, email=email, password=password)
		user.is_active = False
		user.save()

		rng = random.SystemRandom()
		key = rng.randint(1000000, 2000000000)
		user_verification = UserVerification(email=email, validation_key=key)
		user_verification.save()

		VerificationEmail.send(email, key)

		return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
@csrf_exempt
def ping(request):
	return Response(data="pong", status=status.HTTP_200_OK)

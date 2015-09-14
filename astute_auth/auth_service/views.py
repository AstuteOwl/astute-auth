import datetime
import random
from VerificationEmail import VerificationEmail
from astute_auth.auth_service.ProspectEmail import ProspectEmail

from astute_auth.auth_service.request_serializers import TokenRequestSerializer, VerificationRequestSerializer, \
	ProspectRequestSerializer
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

from models import UserVerification, UserClaim, Prospect


@api_view(['POST'])
@csrf_exempt
def token(request):
	data = JSONParser().parse(request)
	token_serializer = TokenRequestSerializer(data=data)

	if not token_serializer.is_valid():
		return Response(status=status.HTTP_400_BAD_REQUEST)

	email = token_serializer.validated_data['email']
	password = token_serializer.validated_data['password']

	if User.objects.filter(username=email).exists():
		user = authenticate(username=email, password=password)
		if user is None:
			return Response(status=status.HTTP_401_UNAUTHORIZED)
		else:
			if user.is_active:
				# assign claims
				claims = {}
				claim_set = UserClaim.objects.filter(email=email)
				for claim in claim_set:
					claims[claim.claim_name] = claim.claim_value
				claims['email'] = email

				# Generate the JWT
				jwt = generate_jwt(claims, settings.HMAC_SECRET, 'HS512', datetime.timedelta(days=365))
				response_data = {'token':jwt}
				return JsonResponse(response_data, status=status.HTTP_201_CREATED)
			else:
				return Response(status=status.HTTP_202_ACCEPTED)
	else:
		user = User.objects.create_user(username=email, email=email, password=password)
		user.is_active = False
		user.save()

		# Generate the verification key and email
		rng = random.SystemRandom()
		key = rng.randint(1000000, 2000000000)
		user_verification = UserVerification(email=email, validation_key=key)
		user_verification.save()

		VerificationEmail.send(email, key)

		# Store any registration claims
		if 'claims' in token_serializer.validated_data.keys():
			claims = token_serializer.validated_data['claims']
			for claim_name in claims:
				user_claim = UserClaim(email=email, claim_name=claim_name, claim_value=claims[claim_name])
				user_claim.save()

		return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
@csrf_exempt
def verify(request):
	data = JSONParser().parse(request)
	verification_key_serializer = VerificationRequestSerializer(data=data)

	if not verification_key_serializer.is_valid():
		return Response(status=status.HTTP_400_BAD_REQUEST)

	email = verification_key_serializer.validated_data['email']
	validation_key = verification_key_serializer.validated_data['validation_key']

	if UserVerification.objects.filter(email=email, validation_key=validation_key).exists():
		user_verification = UserVerification.objects.get(email=email, validation_key=validation_key)
		user = User.objects.get(username=user_verification.email)
		user.is_active = True
		user.save()
		user_verification.delete()
		return Response(status=status.HTTP_200_OK)
	else:
		return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@csrf_exempt
def prospects(request):
	data = JSONParser().parse(request)
	prospect_serializer = ProspectRequestSerializer(data=data)

	if not prospect_serializer.is_valid():
		return Response(status=status.HTTP_400_BAD_REQUEST)

	email = prospect_serializer.validated_data['email']
	if not Prospect.objects.filter(email=email).exists():
		client_ip = request.META.get('HTTP_X_FORWARDED_FOR')
		if not client_ip:
			client_ip = request.META.get('REMOTE_ADDR')
		prospect = Prospect(
			email=email, request_when=datetime.datetime.utcnow(), remote_addr=client_ip)
		prospect.save()
		ProspectEmail.send(email)

	return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@csrf_exempt
def ping(request):
	return Response(data="pong", status=status.HTTP_200_OK)

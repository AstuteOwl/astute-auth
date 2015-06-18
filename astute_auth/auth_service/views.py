import datetime

from astute_auth.auth_service.request_serializers import TokenRequestSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from jwt import generate_jwt
from astute_auth import settings


class JsonCorsResponse(Response):
	"""
	A Response that renders its content into JSON and allows all origins.
	"""

	def __init__(self, **kwargs):
		kwargs['content_type'] = 'application/json'
		kwargs['headers'] = {"Access-Control-Allow-Origin": "*"}
		super(JsonCorsResponse, self).__init__(**kwargs)


@api_view(['POST'])
@csrf_exempt
def token(request):
	data = JSONParser().parse(request)
	token_serializer = TokenRequestSerializer(data=data)

	if not token_serializer.is_valid():
		return JsonCorsResponse(status=status.HTTP_400_BAD_REQUEST)
	
	email = token_serializer.validated_data['email']
	password = token_serializer.validated_data['password']

	if User.objects.filter(username=email).exists():
		user = authenticate(username=email, password=password)
		if user is None:
			return JsonCorsResponse(status=status.HTTP_401_UNAUTHORIZED)
		else:
			claims = {'email': email, 'permissions': list(user.get_all_permissions())}
			jwt = generate_jwt(claims, settings.HMAC_SECRET, 'HS512', datetime.timedelta(days=365))
			response_data = {'token':jwt}
			return JsonCorsResponse(data=response_data, status=status.HTTP_201_CREATED)
	else:
		user = User.objects.create_user(username=email, email=email, password=password)
		# TODO: send verification email
		return JsonCorsResponse(status=status.HTTP_202_ACCEPTED)

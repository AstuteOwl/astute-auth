import datetime

from astute_auth.auth_service.request_serializers import TokenRequestSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from jwt import generate_jwt
from astute_auth import settings


class JSONResponse(HttpResponse):
	"""
    An HttpResponse that renders its content into JSON.
    """

	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

	# Access-Control-Allow-Origin


@api_view(['POST'])
@csrf_exempt
def token(request):
	data = JSONParser().parse(request)
	token_serializer = TokenRequestSerializer(data=data)

	if not token_serializer.is_valid():
		return HttpResponse(status=status.HTTP_400_BAD_REQUEST, headers={"Access-Control-Allow-Origin": "*"})
	
	email = token_serializer.validated_data['email']
	password = token_serializer.validated_data['password']

	if User.objects.filter(username=email).exists():
		user = authenticate(username=email, password=password)
		if user is None:
			return Response(status=status.HTTP_401_UNAUTHORIZED, headers={"Access-Control-Allow-Origin": "*"})
		else:
			claims = {'email': email, 'permissions': list(user.get_all_permissions())}
			token = generate_jwt(claims, settings.HMAC_SECRET, 'HS512', datetime.timedelta(days=365))
			response = {'token':token}
			return Response(response, status=status.HTTP_201_CREATED, headers={"Access-Control-Allow-Origin": "*"})
	else:
		user = User.objects.create_user(username=email, email=email, password=password)
		user.save()
		# TODO: send verification email
		return Response(status=status.HTTP_202_ACCEPTED, headers={"Access-Control-Allow-Origin": "*"})

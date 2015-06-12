import datetime
from django.http import HttpResponse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from jwt import generate_jwt, verify_jwt


class JSONResponse(HttpResponse):
	"""
    An HttpResponse that renders its content into JSON.
    """

	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

	# Access-Control-Allow-Origin


@api_view(['GET'])
def auth(request):
	"""
	Retrieve, update or delete a snippet instance.
	"""
	snippet = {"Hello": "World"}

	if request.method == 'GET':
		return Response(snippet, headers={"Access-Control-Allow-Origin": "*"})


@api_view(['GET'])
def noauth(request):
	"""
	Retrieve, update or delete a snippet instance.
	"""
	return Response(status=status.HTTP_401_UNAUTHORIZED, headers={"Access-Control-Allow-Origin": "*"})


@api_view(['POST'])
def login(request):
	if request.data['username'] == "hi" and request.data['password'] == "there":
		claims = {'roles': ['user'], 'foo': 'bar'}
		token = generate_jwt(claims, os.environ.get('HMAC_SECRET_KEY', 'default'), 'HS512', datetime.timedelta(minutes=500))
		return Response(token, headers={"Access-Control-Allow-Origin": "*"})
	else:
		return Response(status=status.HTTP_401_UNAUTHORIZED, headers={"Access-Control-Allow-Origin": "*"})

@api_view(['GET'])
def verify(request):
	token = request.query_params['token']
	header, claims = verify_jwt(token, os.environ.get('HMAC_SECRET_KEY', 'default'), ['HS512'])
	return Response(claims, headers={"Access-Control-Allow-Origin": "*"})

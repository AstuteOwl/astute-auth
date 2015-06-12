from django.http import HttpResponse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.response import Response


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
		#Access-Control-Allow-Origin


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
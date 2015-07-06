from lettuce import *
import requests

@step('the resource name "(.*)"')
def have_the_resource(step, resource):
	world.resource_name = str(resource)

@step('I call the Astute-Auth Service')
def call_the_astute_auth_service(step):
	response = requests.get("https://test-astute-auth.herokuapp.com/{}".format(world.resource_name))
	world.response = response.text

@step('the response is "(.*)"')
def check_the_response(step, expected):
	expected = str('\"{}\"'.format(expected))
	assert world.response == expected, \
		"Got {} expected {}".format(world.response, expected)


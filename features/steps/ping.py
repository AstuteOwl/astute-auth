from behave import *
import requests

#use_step_matcher(parse())

@step('the resource name "{resource}"')
def have_the_resource(context, resource):
	context.resource_name = str(resource)

@step('I call the Astute-Auth Service')
def call_the_astute_auth_service(context):
	headers = {'content-type': 'application/json'}
	response = requests.get("https://test-astute-auth.herokuapp.com/{}".format(context.resource_name), headers)
	context.response = response.text

@step('the response is "{expected}"')
def check_the_response(context, expected):
	expected = str('\"{}\"'.format(expected))
	assert context.response == expected, \
		"Got {} expected {}".format(context.response, expected)


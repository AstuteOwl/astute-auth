Feature: Ping resource
	In order to ensure the Astute-Auth service is available
	As a monitoring agent
	I want to be able to check a test resource on service to ensure it's available

	Scenario: Ping
		Given the resource name "ping"
		When I call the Astute-Auth Service
		Then the response is "pong"
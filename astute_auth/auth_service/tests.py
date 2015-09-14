import random
from astute_auth.auth_service.models import UserVerification, UserClaim
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from jwt import verify_jwt
from rest_framework.test import APITestCase
from rest_framework import status
from astute_auth import settings
import json


class TokenTestCase(APITestCase):
	email = 'myemail@domain.com'
	email_with_claims = 'myclaimsemail@foo.com'
	password = 'my_password'

	def test_no_username_or_password_400(self):
		resp = self.client.post('/token/')
		self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

	def test_new_account_no_claims(self):
		resp = self.client.post('/token/', data={'email': self.email, 'password': self.password})
		self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)
		user = User.objects.get(username=self.email)
		self.assertIsNotNone(user)
		user = authenticate(username=self.email, password=self.password)
		self.assertIsNotNone(user)
		self.assertEqual(False, user.is_active)
		user_verification = UserVerification.objects.filter(email=self.email)
		self.assertIsNotNone(user_verification)

	def test_new_account_with_claims(self):
		claims = {
			'first claim': 'first value',
			'second claim': 'second value',
		}
		resp = self.client.post(
			'/token/', data={'email': self.email_with_claims, 'password': self.password, 'claims': claims})
		self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)
		user = User.objects.get(username=self.email_with_claims)
		self.assertIsNotNone(user)
		user = authenticate(username=self.email_with_claims, password=self.password)
		self.assertIsNotNone(user)
		self.assertEqual(False, user.is_active)
		user_verification = UserVerification.objects.filter(email=self.email_with_claims)
		self.assertIsNotNone(user_verification)
		actual_claims = list(UserClaim.objects.filter(email=self.email_with_claims).order_by('claim_name'))
		self.assertEqual(len(claims), len(actual_claims))
		for actual_claim in actual_claims:
			self.assertEqual(claims[actual_claim.claim_name], actual_claim.claim_value)

	def test_existing_account_bad_password(self):
		bad_password = "bad_password"
		# create the account
		User.objects.create_user(self.email, self.email, self.password)
		# authenticate w/bad password
		resp = self.client.post('/token/', data={'email': self.email, 'password': bad_password})
		self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_existing_active_account_correct_password(self):
		# create the account
		user = User.objects.create_user(self.email, self.email, self.password)
		user.is_active = True
		user.save()
		claim = UserClaim(email=self.email, claim_name='foo', claim_value='bar')
		claim.save()
		# authenticate
		resp = self.client.post('/token/', data={'email': self.email, 'password': self.password})
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
		token = json.loads(resp.content)['token']
		header, claims = verify_jwt(token, settings.HMAC_SECRET, ['HS512'])
		self.assertEqual(claims['email'], self.email)
		self.assertEqual(claims[claim.claim_name], claim.claim_value)
		self.assertEqual(header['alg'], u'HS512')

	def test_existing_inactive_account_correct_password(self):
		# create the inactive account
		user = User.objects.create_user(self.email, self.email, self.password)
		user.is_active = False
		user.save()
		# authenticate
		resp = self.client.post('/token/', data={'email': self.email, 'password': self.password})
		self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)


class PingTestCase(APITestCase):
	def test_ping_get(self):
		resp = self.client.get('/ping')
		self.assertEqual('pong', resp.data)


class VerifyTestCase(APITestCase):
	email = "newaccount@foo.com"
	password = "password"

	def test_verification_bad_request(self):
		resp = self.client.post('/verify/', data={'email': self.email})
		self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

	def test_verification_invalid(self):
		resp = self.client.post('/verify/', data={'email': self.email, 'validation_key': 12345})
		self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

	def test_verification_valid(self):
		user = User.objects.create_user(self.email, self.email, self.password)
		user.is_active = False
		user.save()

		rng = random.SystemRandom()
		validation_key = rng.randint(1000000, 2000000000)

		user_verification = UserVerification(email=self.email, validation_key=validation_key)
		user_verification.save()
		resp = self.client.post('/verify/', data={'email': self.email, 'validation_key': validation_key})
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertFalse(UserVerification.objects.filter(email=self.email, validation_key=validation_key).exists())

		user = User.objects.get(username=self.email)
		self.assertTrue(user.is_active)


class ProspectsTestCase(APITestCase):
	email = "interested@whatever.com"

	def test_prospects_bad_request(self):
		resp = self.client.post('/prospects/')
		self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

	def test_prospects_valid(self):
		resp = self.client.post('/prospects/', data={'email': self.email})
		self.assertEqual(resp.status_code, status.HTTP_200_OK)

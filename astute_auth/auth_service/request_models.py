from django.db import models


class TokenRequest(models.Model):
	email = models.CharField(max_length=254)
	password = models.CharField(max_length=254)

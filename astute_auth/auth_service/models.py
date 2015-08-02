from django.db import models


class UserVerification(models.Model):
	email = models.EmailField(max_length=254, db_index=True)
	validation_key = models.IntegerField(db_index=True)

	class Meta:
		index_together = [
			("email", "validation_key"),
		]


class UserClaim(models.Model):
	email = models.EmailField(max_length=254, db_index=True)
	claim_name = models.CharField(max_length=50, db_index=True)
	claim_value = models.CharField(max_length=254)

	class Meta:
		index_together = [
			("email", "claim_name")
		]

from django.db import models


class UserVerification(models.Model):
	email = models.EmailField(max_length=254, db_index=True)
	validation_key = models.IntegerField(db_index=True)

	class Meta:
		index_together = [
			("email", "validation_key"),
		]
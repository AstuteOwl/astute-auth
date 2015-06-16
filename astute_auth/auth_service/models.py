from django.db import models


class User(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=254)
    role = models.CharField(max_length=25)

    class Meta:
        ordering = ('role', 'email',)

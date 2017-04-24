from django.db import models

class Url(models.Model):
    url_completa = models.CharField(max_length=100, unique=True)
    url_scheme = models.CharField(max_length=5)
    url_acortada = models.AutoField(primary_key=True)

    def __str__(self):
        return self.url_completa

from django.db import models

# Create your models here.

class Account(models.Model):
    id = models.CharField(primary_key=True,max_length=200)
    name = models.CharField(max_length=200)
    balance = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.name


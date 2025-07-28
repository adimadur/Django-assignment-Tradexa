from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    email = models.EmailField()

    class Meta:
        app_label = 'core'

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    price = models.FloatField()

    class Meta:
        app_label = 'core'

class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.IntegerField()

    class Meta:
        app_label = 'core'

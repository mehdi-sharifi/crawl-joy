from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} {self.last_name}"


class CarAd(models.Model):
    code = models.CharField(max_length=100, primary_key=True)
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=20)
    year = models.CharField(max_length=4)
    mileage = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    body_status = models.CharField(max_length=50)
    modified_date = models.DateTimeField()
    
    def __str__(self):
        return f"{self.code} {self.title}"
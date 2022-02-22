from django.db import models
from django.contrib.auth.models import User

class Host(models.Model):
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    phone = models.CharField(max_length=150, null=True)
    language = models.CharField(max_length=150, null=True)
    def __str__(self):
        return self.last_name
    objects = models.Manager()
class Region(models.Model):
    region_name = models.CharField(max_length=150, null=True)
    def __str__(self):
        return self.region_name
    objects = models.Manager()
class Country(models.Model):
    name = models.CharField(max_length=150, null=True)
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE)
    objects = models.Manager()
class Location(models.Model):
    street = models.CharField(max_length=150, null=True)
    city = models.CharField(max_length=150, null=True)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    def __str__(self):
        return self.city + ", " + self.street
    objects = models.Manager()
class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name    
    objects = models.Manager()
class Room(models.Model):
    location = models.ForeignKey(Location, null=True, on_delete= models.CASCADE)
    price = models.FloatField()
    desctiption = models.CharField(max_length=300, null=True)
    tags = models.ManyToManyField(Tag)
    def __str__(self):
        return "Price: " + str(self.price) + ", Details: " + self.desctiption
    objects = models.Manager()
class Book(models.Model):
    STATUS = (
			('Renting', 'Renting'),
			('Not Renting', 'Not Renting')
			)
    room_id = models.ForeignKey(Room, null=True, on_delete= models.CASCADE)
    host_id = models.ForeignKey(Host, null=True, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    objects = models.Manager()

    def __str__(self):
        return self.status
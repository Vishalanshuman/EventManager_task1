from django.db import models

# Create your models here.

class Event(models.Model):
    owner = models.ForeignKey('auth.user', on_delete=models.CASCADE, related_name='events')
    type = models.CharField(max_length=200)
    name = models.CharField(max_length=300)
    envent_image =models.ImageField(upload_to='event')
    tagline = models.CharField(max_length=500)
    schedule =models.DateTimeField()
    description = models.TextField()
    category = models.CharField(max_length=200)
    sub_category = models.CharField(max_length=200)
    attendees = models.ManyToManyField('auth.user')

    def __str__(self) -> str:
        return self.name



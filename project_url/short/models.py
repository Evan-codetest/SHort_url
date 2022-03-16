from django.db import models

# Create your models here.

class Shorturl(models.Model):
    short_url = models.CharField(max_length=10)
    original_url = models.URLField()
    create_date = models.DateTimeField()

    class Meta:
        ordering = ('-create_date',)

    def __str__(self):
        return self.short_url
from django.db import models
from django.utils import timezone
from user.models import CustomUser

# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=False,null=False)
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='notes')

    class Meta:
        ordering = ['last_modified']
    
    def __str__(self):
        return self.title
from django.db import models
from django.utils import timezone
from user.models import CustomUser

class Tag(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='tags')

    class Meta:
        unique_together = ('name', 'owner')

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Note(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=False,null=False)
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='notes')
    tags = models.ManyToManyField(Tag, related_name='notes', blank=True)
    shared_with = models.ManyToManyField(CustomUser, related_name='shared_notes', blank=True)
    
    class Meta:
        ordering = ['-last_modified']
    
    def __str__(self):
        return self.title
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
# Create your models here.
import uuid

class Basemodel(models.Model):
        uid=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
        # title=models.CharField(max_length=500)
        created_at=models.DateField(auto_now_add=True)
        updated_at=models.DateField(auto_now_add=True)
        
        class Meta:
            abstract=True
            
class Task(Basemodel):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="taskss")
    Title = models.CharField(max_length=100, blank=False)
    Description = models.CharField(max_length=100, blank=True)
    # Date = models.DateField( blank=False)
    
    # Completed = models.BooleanField(default=False)

    def __str__(self):
        return self.Title
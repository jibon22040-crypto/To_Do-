from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class AuthUserModel(AbstractUser):
    USER_TYPES=[
        ('user','user'),
        ('admin', 'admin'),
    ]
    full_name=models.CharField(max_length=100, null=True)
    user_types=models.CharField(max_length=100, null=True, choices=USER_TYPES)

    def __str__(self):
        return f"{self.full_name}-{self.user_types}"
    
class TaskModel(models.Model):
    STATUS_TYPES=[
        ('pending', 'Pending'),
        ('Inprogress', 'Inprogress'),
        ('Completed', 'Completed'),
    ]
    user=models.ForeignKey(AuthUserModel, max_length=100, on_delete=models.CASCADE)
    title=models.CharField(max_length=100, null=True)
    description=models.TextField(max_length=100, null=True) 
    task_image=models.ImageField(max_length=100, upload_to="PICs", null=True)
    due_date=models.DateField(null=True)
    status=models.CharField(max_length=100, null=True, choices=STATUS_TYPES)
    created_at=models.DateField(auto_now_add=True, null=True)


    def __str__(self):
        return f"{self.title}-{self.user}"
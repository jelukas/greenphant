from django.db import models
from django.contrib.auth.models import User
from elearning.models import Category


class Interest(models.Model):
    user = models.ForeignKey(User,related_name='interests')
    category = models.ForeignKey(Category,related_name='interested')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' --- ' + self.category.name
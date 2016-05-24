from django.db import models

# Create your models here.


class BuildInfo(models.Model):
    curr_build_info = models.TextField()
    is_success = models.BooleanField(default=False)

from django.db import models

# Create your models here.


class StagingBuildInfo(models.Model):
    curr_build_info = models.TextField()
    is_success = models.BooleanField(default=False)

class ProductionBuildInfo(models.Model):
    curr_build_info = models.TextField()
    is_success = models.BooleanField(default=False)

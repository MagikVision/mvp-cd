from django.db import models

# Create your models here.


class StagingBuildInfo(models.Model):
    curr_build_info = models.TextField()
    is_success = models.BooleanField(default=False)
    console_output = models.TextField()


class StagingWorkerBuildInfo(models.Model):
    curr_build_info = models.TextField()
    is_success = models.BooleanField(default=False)
    console_output = models.TextField()


class ProductionBuildInfo(models.Model):
    curr_build_info = models.TextField()
    is_success = models.BooleanField(default=False)
    console_output = models.TextField()


class ProductionWorkerBuildInfo(models.Model):
    curr_build_info = models.TextField()
    is_success = models.BooleanField(default=False)
    console_output = models.TextField()

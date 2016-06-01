from django.db import models

# Create your models here.


class ServerType(object):
    APP_SERVER = 'app_server'
    WORKER = 'celery_worker'


class BuildInfo(models.Model):
    circleci_json = models.TextField()
    branch = models.CharField(max_length=255)
    commitor = models.CharField(max_length=255)
    circleci_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class ServerBuildInfo(models.Model):
    ip = models.CharField(max_length=255)
    server_type = models.CharField(max_length=255)
    is_success = models.BooleanField(default=False)
    console_output = models.TextField()
    build_info = models.ForeignKey(BuildInfo)

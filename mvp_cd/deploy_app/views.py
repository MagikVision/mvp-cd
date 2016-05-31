from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from mvp_cd.deploy_app.models import StagingBuildInfo
from mvp_cd.deploy_app.models import ProductionBuildInfo
from mvp_cd.deploy_app.models import ProductionWorkerBuildInfo
from mvp_cd.deploy_app.models import StagingWorkerBuildInfo
import subprocess
from django.shortcuts import render_to_response
import json


# Create your views here.


@api_view(['POST'])
def deploy(request):
    if request.data['payload']['outcome'] == 'success':
        with open('deploy_config.json') as data_file:
            deploy_config = json.load(data_file)
            pem_path = deploy_config['pem_path']
            deployment_path = deploy_config['deployment_path']
        if request.data['payload']['branch'] == 'staging':
            for ip in deploy_config['staging_celery_ips']:
                deploy_celery_staging(request, ip, pem_path, deployment_path)
            for ip in deploy_config['staging_app_server_ips']:
                deploy_app_staging(request, ip, pem_path, deployment_path)
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.data['payload']['branch'] == 'production':
            for ip in deploy_config['production_celery_ips']:
                deploy_celery_production(
                    request, ip, pem_path, deployment_path)
            for ip in deploy_config['production_app_server_ips']:
                deploy_app_production(request, ip, pem_path, deployment_path)
            return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def build_info(request):
    build_info = StagingBuildInfo.objects.all().order_by('-id')
    return render_to_response(
        'build_info.html', {'build_info_item': build_info[0]})


def deploy_celery_staging(request, ip, pem_path, deployment_path):
    try:
        process_output = subprocess.check_output(
            ['bash', 'deploy_staging_celery.sh', pem_path,
             ip, deployment_path])
        process_status_staging_celery(request, process_output, 0)
    except subprocess.CalledProcessError as e:
        process_status_staging_celery(request, e.output, 1)


def deploy_celery_production(request, ip, pem_path, deployment_path):
    try:
        process_output = subprocess.check_output(
            ['bash', 'deploy_prod_celery.sh', pem_path, ip, deployment_path])
        process_status_production_celery(request, process_output, 0)
    except subprocess.CalledProcessError as e:
        process_status_production_celery(request, e.output, 1)


def deploy_app_staging(request, ip, pem_path, deployment_path):
    try:
        process_output = subprocess.check_output(
            ['bash', 'deploy_staging.sh', pem_path, ip, deployment_path])
        process_status_staging(request, process_output, 0)
    except subprocess.CalledProcessError as e:
        process_status_staging(request, e.output, 1)


def deploy_app_production(request, ip, pem_path, deployment_path):
    try:
        process_output = subprocess.check_output(
            ['bash', 'deploy_prod.sh', pem_path, ip, deployment_path])
        process_status_production(request, process_output, 0)
    except subprocess.CalledProcessError as e:
        process_status_production(request, e.output, 1)


def process_status_staging(request, process_output, process_status):
    if process_status == 0:
        build_info_item = StagingBuildInfo(
            curr_build_info=json.dumps(request.data['payload']),
            is_success='True',
            console_output=process_output)
        build_info_item.save()
    else:
        build_info_item = StagingBuildInfo(
            curr_build_info=json.dumps(request.data['payload']),
            is_success='False',
            console_output=process_output)
        build_info_item.save()


def process_status_production(request, process_output, process_status):
    if process_status == 0:
        build_info_item = ProductionBuildInfo(
            curr_build_info=json.dumps(request.data['payload']),
            is_success='True',
            console_output=process_output)
        build_info_item.save()
    else:
        build_info_item = ProductionBuildInfo(
            curr_build_info=json.dumps(request.data['payload']),
            is_success='False',
            console_output=process_output)
        build_info_item.save()


def process_status_production_celery(request, process_output, process_status):
    if process_status == 0:
        build_info_item = ProductionWorkerBuildInfo(
            curr_build_info=json.dumps(request.data['payload']),
            is_success='True',
            console_output=process_output)
        build_info_item.save()
    else:
        build_info_item = ProductionWorkerBuildInfo(
            curr_build_info=json.dumps(request.data['payload']),
            is_success='False',
            console_output=process_output)
        build_info_item.save()


def process_status_staging_celery(request, process_output, process_status):
    if process_status == 0:
        build_info_item = StagingWorkerBuildInfo(
            curr_build_info=json.dumps(request.data['payload']),
            is_success='True',
            console_output=process_output)
        build_info_item.save()
    else:
        build_info_item = StagingWorkerBuildInfo(
            curr_build_info=json.dumps(request.data['payload']),
            is_success='False',
            console_output=process_output)
        build_info_item.save()

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from mvp_cd.deploy_app.models import (BuildInfo, ServerBuildInfo, ServerType)
import subprocess
from django.shortcuts import render_to_response
import json
from django.shortcuts import get_object_or_404


# Create your views here.


@api_view(['POST'])
def deploy_view(request):
    if request.data['outcome'] == 'success':
        build_info_obj = BuildInfo(
            circleci_json=request.data,
            branch=request.data['branch'],
            commitor=request.data['author_name'],
            circleci_url=request.data['build_url'])
        build_info_obj.save()
        with open('deploy_config.json') as data_file:
            deploy_config = json.load(data_file)
            pem_path = deploy_config['pem_path']
            deployment_path = deploy_config['deployment_path']

        if request.data['branch'] == 'staging':
            for ip in deploy_config['staging_celery_ips']:
                deploy_celery_staging(
                    request, ip, pem_path, deployment_path, build_info_obj)
            for ip in deploy_config['staging_app_server_ips']:
                deploy_app_staging(
                    request, ip, pem_path, deployment_path, build_info_obj)
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.data['branch'] == 'production':
            for ip in deploy_config['production_celery_ips']:
                deploy_celery_production(
                    request, ip, pem_path, deployment_path, build_info_obj)
            for ip in deploy_config['production_app_server_ips']:
                deploy_app_production(
                    request, ip, pem_path, deployment_path, build_info_obj)
            return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def build_list_view(request):
    build_info = BuildInfo.objects.all().order_by('-id')[:10]
    return render_to_response(
        'build_list.html', {'build_list': build_info})


def build_detail_view(request, id):
    build_info = get_object_or_404(BuildInfo, id=id)
    return render_to_response(
        'build_info.html', {'build_list': build_info})


def deploy_celery_staging(
        request, ip, pem_path, deployment_path, build_info_obj):
    try:
        process_output = subprocess.check_output(
            ['bash', 'deploy_staging_celery.sh', pem_path,
             ip, deployment_path],stdin=subprocess.PIPE)
        process_status(
            request, process_output, 0, ip, ServerType.WORKER, build_info_obj)
    except subprocess.CalledProcessError as e:
        process_status(
            request, e.output, 1, ip, ServerType.WORKER, build_info_obj)


def deploy_celery_production(
        request, ip, pem_path, deployment_path, build_info_obj):
    try:
        process_output = subprocess.check_output(
            ['bash', 'deploy_prod_celery.sh', pem_path, ip, deployment_path],stdin=subprocess.PIPE)
        process_status(
            request, process_output, 0, ip, ServerType.WORKER, build_info_obj)
    except subprocess.CalledProcessError as e:
        process_status(
            request, e.output, 1, ip, ServerType.WORKER, build_info_obj)


def deploy_app_staging(request, ip, pem_path, deployment_path, build_info_obj):
    try:
        process_output = subprocess.check_output(
            ['bash', 'deploy_staging.sh', pem_path, ip, deployment_path],stdin=subprocess.PIPE)
        process_status(
            request,
            process_output, 0, ip, ServerType.APP_SERVER, build_info_obj)
    except subprocess.CalledProcessError as e:
        process_status(
            request, e.output, 1, ip, ServerType.APP_SERVER, build_info_obj)


def deploy_app_production(
        request, ip, pem_path, deployment_path, build_info_obj):
    try:
        process_output = subprocess.check_output(
            ['bash', 'deploy_prod.sh', pem_path, ip, deployment_path],stdin=subprocess.PIPE)
        process_status(
            request,
            process_output, 0, ip, ServerType.APP_SERVER, build_info_obj)
    except subprocess.CalledProcessError as e:
        process_status(
            request, e.output, 1, ip, ServerType.APP_SERVER, build_info_obj)


def process_status(
        request,
        process_output, process_status, ip, server_type, build_info_obj):
    if process_status == 0:
        build_info_item = ServerBuildInfo(
            is_success=True,
            console_output=process_output,
            ip=ip,
            server_type=server_type,
            build_info=build_info_obj)
        build_info_item.save()
    else:
        build_info_item = ServerBuildInfo(
            is_success=False,
            console_output=process_output,
            ip=ip,
            server_type=server_type,
            build_info=build_info_obj)
        build_info_item.save()

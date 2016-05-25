from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from mvp_cd.deploy_app.models import StagingBuildInfo
import subprocess
from django.shortcuts import render_to_response
import json


# Create your views here.


@api_view(['POST'])
def deploy(request):
    if request.data['payload']['outcome'] == 'success':
        if request.data['payload']['branch'] == 'staging':
            process_status = subprocess.call(
                ['bash', 'deploy.sh', request.data['payload']['branch']])
            if process_status == 0:
                build_info_item = StagingBuildInfo(
                    curr_build_info=json.dumps(request.data['payload']),
                    is_success='True')
                build_info_item.save()
            else:
                build_info_item = StagingBuildInfo(
                    curr_build_info=json.dumps(request.data['payload']),
                    is_success='False')
                build_info_item.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.data['payload']['branch'] == 'production':
            process_status = subprocess.call(
                ['bash', 'deploy_prod.sh', request.data['payload']['branch']])
            if process_status == 0:
                build_info_item = StagingBuildInfo(
                    curr_build_info=json.dumps(request.data['payload']),
                    is_success='True')
                build_info_item.save()
            else:
                build_info_item = StagingBuildInfo(
                    curr_build_info=json.dumps(request.data['payload']),
                    is_success='False')
                build_info_item.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def build_info(request):
    build_info = StagingBuildInfo.objects.all().order_by('id')
    return render_to_response(
        'build_info.html', {'build_info_item': build_info[0]})

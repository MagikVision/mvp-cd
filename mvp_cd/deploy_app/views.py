from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import subprocess
import os


# Create your views here.


@api_view(['POST'])
def deploy(request):
    print(request.data)
    if request.data['outcome'] == 'success':
        if request.data['branch'] == 'master':
            print(os.getcwd())
            subprocess.call(['bash', 'deploy.sh',request.data['branch']])
            return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)
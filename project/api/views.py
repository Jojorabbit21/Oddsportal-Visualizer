from email.policy import HTTP
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http.response import HttpResponse
import json

from .service.main import GetOddsData

@api_view(['GET', 'POST'])
def api(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        result = GetOddsData(body['url'], body['type'])
        result = json.dumps(result)
        return Response(result, status=status.HTTP_200_OK, 
                        headers={ 
                                 'Origin': 'http://127.0.0.1',
                                 },
                        content_type="application/json")
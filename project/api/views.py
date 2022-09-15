from email.policy import HTTP
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http.response import HttpResponse

@api_view(['GET', 'POST'])
def api(request):
  return HttpResponse("Hello World!");
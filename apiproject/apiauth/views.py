from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

def index(request):
    return Response(status=status.HTTP_200_OK)
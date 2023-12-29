from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import JSONParser
from rest_framework import status, generics, mixins, viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view,permission_classes, authentication_classes


# Create your views here.


@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([permissions.IsAuthenticated])
def main(request):
    HttpResponse("Hello, world. You're at the polls index.")
    return HttpResponse("Hello, world. You're at the polls index.")
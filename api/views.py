from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status, generics, mixins, viewsets, permissions

# Create your views here.


def main(request):
    return HttpResponse("Hello, world. You're at the polls index.")

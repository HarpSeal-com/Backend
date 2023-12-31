from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import JSONParser
from rest_framework import status, generics, mixins, viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view,permission_classes, authentication_classes

from .scraper import getProductLink

# Create your views here.


@api_view(['POST'])
def main(request):
    #Extract JSON data
    data = JSONParser().parse(request)
    productName = data['product']
    category = data['category']

    searchTermX = getProductLink(productName, category)
    result = searchTermX.getPublic()

    return HttpResponse(result, content_type='application/json')

@api_view(['POST'])
def apiTest(request):
    #Extract JSON data
    data = JSONParser().parse(request)
    productName = data['product']
    category = data['category']

    searchTermX = getProductLink(productName, category)
    result = searchTermX.findPage(
        {
            "Amazon": {
                "url": "https://www.amazon.co.uk/",
                "country": "UK",
                "products": "all"
            }
        }
    )

    return HttpResponse(result['Link'], content_type='application/json')




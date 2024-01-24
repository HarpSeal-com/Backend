from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import JSONParser
from rest_framework import status, generics, mixins, viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view,permission_classes, authentication_classes

from .scraper import getProductLink


@api_view(['POST'])
def main(request):
    #Extract JSON data
    data = JSONParser().parse(request)
    productName = data['product']
    category = data['category']

    searchTermX = getProductLink(productName, category)

    result = searchTermX.getPublic()
    
    return JsonResponse({
        "Link": result["Link"],
        "Retailer": result["Retailer"],
        "Price": result["Price"]
    }, 
    content_type='application/json',
    safe=False,
    status=status.HTTP_200_OK)

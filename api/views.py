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

    return JsonResponse({
        "Link": result["Link"],
        "Retailer": result["Retailer"],
        "Price": result["Price"]
    }, 
    content_type='application/json',
    safe=False,
    status=status.HTTP_200_OK)

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
                "url": f"https://www.amazon.co.uk/s?k={productName}&language=en_GB&crid=2HI29GR81T65C&linkCode=ll2&linkId=2ca4f43cbe0f08dcc779b9d74749b620&sprefix={productName}%2Caps%2C69&ref=as_li_ss_tl",
                "country": "UK",
                "products": "all"
            }
        }
    )

    return JsonResponse(result)




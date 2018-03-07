from django.http import HttpResponse

from django.shortcuts import render
from django.core import serializers

from .models import Dog, Location

# Create your views here.
def index(request):

    message = 'Hello, world!'

    return render(request, 'index.html', {
        'message': message,
    })

def search(request, zipcode):
    
    locations = Location.objects.filter(zipcode=zipcode)
    dogs = Dog.objects.filter(location__in=locations)
    #data = serializers.serialize("json", dogs)
    #return HttpResponse(data, content_type='application/json')
    return HttpResponse(list(dogs), content_type='application/json')

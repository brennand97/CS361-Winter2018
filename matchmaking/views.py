from django.http import HttpResponse

from django.shortcuts import render
from django.core import serializers

from .models import Dog, Location

def reduce_json(data):
    if isinstance(data, []):
        r_data = []
        for d in data:
            if "model" in d:
                r = d["fields"]
                for f in r:
    else:
        if "model" in data:
            data = data["fields"]
            

# Create your views here.
def index(request):

    message = 'Hello, world!'

    return render(request, 'index.html', {
        'message': message,
    })

def search(request, zipcode):
    
    location = Location.objects.get(zipcode=zipcode)
    dogs = Dog.objects.filter(location=location)
   
    data = serializers.serialize("json", dogs)
    

    return HttpResponse(data, content_type='application/json')


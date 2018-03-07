from django.http import HttpResponse

from django.shortcuts import render
from django.core import serializers

from .models import Dog, Location

# Helper Functions
def reduce_json(data):
    if isinstance(data, (list,tuple)):
        o_data = []
        for d in data:
            o_data.append(reduce_json(d))
        return o_data
    else:
        if isinstance(data, dict):
            if "model" in data:
                data = data["fields"]
            for f in data:
                data[f] = reduce_json(data[f])
        return data

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

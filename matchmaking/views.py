from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from .models import Dog, Location, PersonalityQualities, PhysicalQualities

import json

# Helper Functions
"""
This function reduces the nasty json that the Django serailizer produces
to objects that only contain the fields.

Example usage:

dogs = Dog.objects.filter(location__in=locations)
data = serializers.serialize("json", dogs)
data = json.dumps(reduce_json(json.loads(data)))

"""

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


"""
This is a helper function for reduce_json.
"""
def queryset_to_json(qs):
    return json.dumps(reduce_json(json.loads(serializers.serialize("json", qs))))


def check_for_fields(d, l):
    for e in l:
        if e not in d:
            return False
    return True

def remove_empty(d):
    return {k: v for k, v in d.items() if v is not None}

# Create your views here.
def index(request):

    message = 'Hello, world!'

    return render(request, 'index.html', {
        'message': message,
    })

def add_dog(request):
    message = 'Add New Dog'

    return render(request, 'add_dog.html',{
        'message': message,
    })

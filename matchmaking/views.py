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

"""
Send a GET request to this address with the zipcode you want the dogs from
to get all the dogs in that zipcode.
To filter the dogs send a POST request with the same zipcode and a json data
load that looks like (set fields to null if you don't want to filter on them):
{
  "dog": {
    "sex": "m",
    "age": 4,
    "breed": "Pug"
  },
  "physical": {
    "color": "Yellow",
    "height": 20.0,
    "weight": 30.0,
    "eye_color": "Blue",
    "hypoallergenic": false,
    "shedding": true
  },
  "personality": {
    "friendly": true,
    "kid_friendly": true,
    "likes_water": true,
    "likes_cars": false,
    "socialized": true,
    "rescue_animal": false
  }
}
"""
@csrf_exempt
def search(request, zipcode):

    locations = Location.objects.filter(zipcode=zipcode)

    if request.method == 'POST':

        json_data = json.loads(request.body)

        if not check_for_fields(json_data, ["physical", "personality", "dog"]):
            return HttpResponseBadRequest("Missing either the physical or personality fields.")

        physical_data = json_data["physical"]
        personality_data = json_data["personality"]
        dog_data = json_data["dog"]

        if physical_data is None or \
           personality_data is None or \
           dog_data is None:
            return HttpResponseBadRequest("One or all of the physical, personality, or dog fields is null.")

        # Check to make sure physical_data has proper fields
        if not check_for_fields(physical_data, [
                "color", "height", "weight", "eye_color",
                "hypoallergenic", "shedding"
            ]):
            return HttpResponseBadRequest("Not all fields are in physical data object.")

        # Check to make sure personality_data has proper fields
        if not check_for_fields(personality_data, [
                "friendly", "kid_friendly", "likes_water",
                "likes_cars", "socialized", "rescue_animal"
            ]):
            return HttpResponseBadRequest("Not all fields are in personality data object.")

        # Check to make sure dog_data has proper fields
        if not check_for_fields(dog_data, [
                "sex", "age", "breed"
            ]):
            return HttpResponseBadRequest("Not all fields are in dog data object.")

        physical_data = remove_empty(physical_data)
        personality_data = remove_empty(personality_data)
        dog_data = remove_empty(dog_data)

        phy_qs = PhysicalQualities.objects.filter(**physical_data)
        per_qs = PersonalityQualities.objects.filter(**personality_data)

        dogs = Dog.objects.filter(location__in=locations,
                                  physical__in=phy_qs,
                                  personality__in=per_qs,
                                  **dog_data)

    else:
        dogs = Dog.objects.filter(location__in=locations)

    data = serializers.serialize("json", dogs)
    data = json.dumps(reduce_json(json.loads(data)))

    return HttpResponse(data, content_type='application/json')

def add_dog(request):
    message = 'Add New Dog'

    return render(request, 'add_dog.html',{
        'message': message,
    })

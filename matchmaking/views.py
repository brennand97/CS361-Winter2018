from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from .models import Dog, Location, PersonalityQualities, PhysicalQualities, Shelter, UserProfile


import json

# Helper Functions

"""
This is a helper function for add_dog_to_db.  Javascript bool values were sent as strings.  Python
needs them as bools.  This converts them.
"""
def str2bool(v):
  try:
      return v.lower() in ("true", "True")
  except Exception as e:
      return False
  

def fix_bools(data):
    data["personality"]["friendly"] = str2bool(data["personality"]["friendly"])
    data["personality"]["kid_friendly"] = str2bool(data["personality"]["kid_friendly"])
    data["personality"]["likes_water"] = str2bool(data["personality"]["likes_water"])
    data["personality"]["likes_cars"] = str2bool(data["personality"]["likes_cars"])
    data["personality"]["socialized"] = str2bool(data["personality"]["socialized"])
    data["personality"]["rescue_animal"] = str2bool(data["personality"]["rescue_animal"])
    data["physical"]["hypoallergenic"] = str2bool(data["physical"]["hypoallergenic"])
    data["physical"]["shedding"] = str2bool(data["physical"]["shedding"])
    return data
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
                pk = data["pk"]
                data = data["fields"]
                data["id"] = pk
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
    "min_age": 2,
    "max_age": 4,
    "breed": "Pug"
  },
  "physical": {
    "color": "Yellow",
    "min_height": 10.0,
    "max_height": 20.0,
    "min_weight": 15.0,
    "max_weight": 30.0,
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

        try:
            json_data = json.loads(request.body.decode('utf-8'))
        except Exception:
            return HttpResponseBadRequest("Need to include a json payload with filter data.")

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
                "color", "min_height", "max_height", "min_weight", "max_weight", "eye_color",
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
                "sex", "min_age", "max_age", "breed"
            ]):
            return HttpResponseBadRequest("Not all fields are in dog data object.")


        # Remove fields with None values
        physical_data = remove_empty(physical_data)
        personality_data = remove_empty(personality_data)
        dog_data = remove_empty(dog_data)


        # Handle age
        if "max_age" in dog_data:
            max_a = dog_data["max_age"]
            del dog_data["max_age"]
            dog_data["age__lte"] = max_a

        if "min_age" in dog_data:
            min_a = dog_data["min_age"]
            del dog_data["min_age"]
            dog_data["age__gte"] = min_a


        # Handle weight
        if "max_weight" in physical_data:
            max_w = physical_data["max_weight"]
            del physical_data["max_weight"]
            physical_data["weight__lte"] = max_w

        if "min_weight" in physical_data:
            min_w = physical_data["min_weight"]
            del physical_data["min_weight"]
            physical_data["weight__gte"] = min_w


        # Handle height
        if "max_height" in physical_data:
            max_h = physical_data["max_height"]
            del physical_data["max_height"]
            physical_data["height__lte"] = max_h

        if "min_height" in physical_data:
            min_h = physical_data["min_height"]
            del physical_data["min_height"]
            physical_data["height__gte"] = min_h


        phy_qs = PhysicalQualities.objects.filter(**physical_data)
        per_qs = PersonalityQualities.objects.filter(**personality_data)

        dogs = Dog.objects.filter(location__in=locations,
                                  physical__in=phy_qs,
                                  personality__in=per_qs,
                                  **dog_data)

    else:
        dogs = Dog.objects.filter(location__in=locations)

    print("Found {} dogs.".format(len(dogs)))

    data = serializers.serialize("json", dogs)
    data = json.dumps(reduce_json(json.loads(data)))

    return HttpResponse(data, content_type='application/json')

def add_dog(request):
    message = 'Add New Dog'

    return render(request, 'add_dog.html',{
        'message': message,
    })

def view_listings(request):
    return render(request, 'view_listings.html', {})

def shelter_dogs(request, shelter):
    s = get_object_or_404(Shelter, name=shelter)

    dogs = Dog.objects.filter(has_shelter=True, shelter=s)
    dogs_json = queryset_to_json(dogs)

    return HttpResponse(dogs_json, content_type='application/json')

@csrf_exempt
def add_dog_to_db(request):
    print(request.body)
    data = json.loads(request.body.decode('utf-8'))
    data = fix_bools(data)

    #location
    l, created_l = Location.objects.get_or_create(
        city=data["dog"]["city"],
        state=data["dog"]["state"],
        zipcode=data["dog"]["zipcode"])
 
    #personality
    pers, created_pers = PersonalityQualities.objects.get_or_create(
        friendly=data["personality"]["friendly"],
        kid_friendly=data["personality"]["kid_friendly"],
        likes_water =data["personality"]["likes_water"],
        likes_cars =data["personality"]["likes_cars"],
        socialized  =data["personality"]["socialized"],
        rescue_animal = data["personality"]["rescue_animal"])

    #physical
    phys, created_phys = PhysicalQualities.objects.get_or_create(
        color=data["physical"]["color"],
        height=data["physical"]["height"],
        weight=data["physical"]["weight"],
        eye_color=data["physical"]["eye_color"],
        hypoallergenic=data["physical"]["hypoallergenic"],
        shedding=data["physical"]["shedding"]) 

    #owner
    form_user = get_object_or_404(User, username=data["user"])
    user_prof = UserProfile.objects.filter(user = form_user)

    #finally, Dog
    d = Dog(
        name = data["dog"]["name"],
        sex=data["dog"]["sex"],
        age=data["dog"]["age"],
        breed=data["dog"]["breed"],
        bio = data["dog"]["bio"],
        location = l,
        personality = pers, 
        physical = phys,
        owner = user_prof[0])
    d.save()

    success = "yes"
    status = {'success': success}

    return HttpResponse(status, content_type='application/json')


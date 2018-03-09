from django.http import HttpResponse

from django.shortcuts import render

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

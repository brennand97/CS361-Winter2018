from django.http import HttpResponse

from django.shortcuts import render

# Create your views here.
def index(request):

    message = 'Hello, world!'

    return render(request, 'index.html', {
        'message': message,
    })

def search(request):
    message = 'Add New Dog'

    return render(request, 'add-dog.html',{
        'message': message,
    })

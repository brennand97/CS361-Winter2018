from django import forms

from .models import Dog

class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = [
            "name",
            "age",
            "sex",
            "breed",
            "bio",
            "personality",
            "physical",
            "owner",
            "has_shelter",
            "shelter",
            "location"
        ]

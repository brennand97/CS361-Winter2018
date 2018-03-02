from django.db.models import Model, CASCADE, FloatField, CharField, ForeignKey, \
                             BooleanField, IntegerField, TextField, DecimalField
from django.contrib.auth.models import User

# Create your models here.

"""
Example models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
"""

class Location(Model):

    states = [
            "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
            "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
            ]

    city    = CharField(max_length=256, null=False)
    state   = CharField(max_length=2, choices=map(lambda a: (a,a), states), null=False)
    zipcode = CharField(max_length=32, null=False)


class ContactInfo(Model):

    phone_number = CharField(max_length=16, null=True)
    email        = CharField(max_length=256, null=False)
    website      = CharField(max_length=256, null=True)


class UserProfile(Model):
    """
    Django already has a built-in user calss that should be
    used.  So this UserProfile class will 'extend' that class
    by holding a relationship to a user.  This will allow
    extra data points to be added and related to a user.

    User already includes:
        * username
        * password
        * first_name
        * last_name

    """

    user         = ForeignKey(User, on_delete=CASCADE, null=False)
    location     = ForeignKey(Location, on_delete=CASCADE, null=True)
    contact_info = ForeignKey(ContactInfo, on_delete=CASCADE, null=False)


class Shelter(Model):

    name         = CharField(max_length=256, null=False)
    location     = ForeignKey(Location, on_delete=CASCADE, null=False)
    contact_info = ForeignKey(ContactInfo, on_delete=CASCADE, null=False)
    verified     = BooleanField(null=False, default=False)


class PersonalityQualities(Model):

    friendly      = BooleanField(default=False)
    kid_friendly  = BooleanField(default=False)
    likes_water   = BooleanField(default=False)
    likes_cars    = BooleanField(default=False)
    socialized    = BooleanField(default=False)
    rescue_animal = BooleanField(default=False)


class PhysicalQualities(Model):
    color          = CharField(max_length=64, null=True)
    height         = FloatField(null=True)
    weight         = FloatField(null=True)
    eye_color      = CharField(max_length=64, null=True)
    hypoallergenic = BooleanField(default=False)
    shedding       = BooleanField(default=True)


class Dog(Model):

    name        = CharField(max_length=256, null=False)
    sex         = CharField(max_length=16, null=False)
    age         = IntegerField(null=False)
    breed       = CharField(max_length=256, null=True)
    bio         = TextField(null=True)

    location    = ForeignKey(Location, on_delete=CASCADE, null=False)
    personality = ForeignKey(PersonalityQualities, on_delete=CASCADE, null=False)
    physical    = ForeignKey(PhysicalQualities, on_delete=CASCADE, null=False)


class Message(Model):

    body      = TextField(null=False)
    user_to   = ForeignKey(UserProfile,
                           on_delete=CASCADE,
                           related_name='user_to',
                           null=True)
    user_from = ForeignKey(UserProfile,
                           on_delete=CASCADE,
                           related_name='user_from',
                           null=False)


class Payment(Model):

    user_profile = ForeignKey(UserProfile, on_delete=CASCADE, null=False)
    shelter      = ForeignKey(Shelter, on_delete=CASCADE, null=False)
    amount       = DecimalField(max_digits=15, decimal_places=2)

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

    def __str__(self):
        return 'Location: {}, {} {}'.format(self.city, self.state, self.zipcode)


class ContactInfo(Model):

    phone_number = CharField(max_length=16, null=True)
    email        = CharField(max_length=256, null=False)
    website      = CharField(max_length=256, null=True)

    def __str__(self):
        return 'ContactInfo: {}; {}; {}'.format(self.phone_number, self.email, self.website)


def user_to_str(user):
    return 'User: {} {}; {}'.format(user.first_name, user.last_name, user.username)


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
    is_shelter   = BooleanField(null=False, default=False)

    def __str__(self):
        return user_to_str(self.user)


class Shelter(Model):

    name         = CharField(max_length=256, null=False)
    location     = ForeignKey(Location, on_delete=CASCADE, null=False)
    contact_info = ForeignKey(ContactInfo, on_delete=CASCADE, null=False)
    verified     = BooleanField(null=False, default=False)

    def __str__(self):
        return 'Shelter: {} (v: {})'.format(self.name, int(self.verified))


class PersonalityQualities(Model):

    friendly      = BooleanField(default=False)
    kid_friendly  = BooleanField(default=False)
    likes_water   = BooleanField(default=False)
    likes_cars    = BooleanField(default=False)
    socialized    = BooleanField(default=False)
    rescue_animal = BooleanField(default=False)

    def __str__(self):
        return 'Personality: f: {0}, kf: {1}, lw: {2}, lc: {3}, s: {4}, ra: {5}'.format(
            *list(map(lambda a: int(a), [
                self.friendly,
                self.kid_friendly,
                self.likes_water,
                self.likes_cars,
                self.socialized,
                self.rescue_animal
            ]))
        )


class PhysicalQualities(Model):
    color          = CharField(max_length=64, null=True)
    height         = FloatField(null=True)
    weight         = FloatField(null=True)
    eye_color      = CharField(max_length=64, null=True)
    hypoallergenic = BooleanField(default=False)
    shedding       = BooleanField(default=True)

    def __str__(self):
        return 'Physical: c: {}, h: {}, w: {}, ec: {}, hypo: {}, shed: {}'.format(
            self.color,
            self.height,
            self.weight,
            self.eye_color,
            int(self.hypoallergenic),
            int(self.shedding)
        )


class Dog(Model):

    MALE = "m"
    FEMALE = "f"

    name        = CharField(max_length=256, null=False)
    sex         = CharField(max_length=1, choices=(
                                    (MALE, "Male"),
                                    (FEMALE, "Female")
                                ), null=False)
    age         = IntegerField(null=False)
    breed       = CharField(max_length=256, null=True)
    bio         = TextField(null=True)

    location    = ForeignKey(Location, on_delete=CASCADE, null=False)
    personality = ForeignKey(PersonalityQualities, on_delete=CASCADE, null=False)
    physical    = ForeignKey(PhysicalQualities, on_delete=CASCADE, null=False)
    
    has_shelter = BooleanField(default=False, null=False)
    owner       = ForeignKey(UserProfile, on_delete=CASCADE, null=True)
    shelter     = ForeignKey(Shelter, on_delete=CASCADE, null=True)

    def __str__(self):
        return 'Dog: {}, {}, {}, {}'.format(self.name, self.sex, self.age, self.breed)


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

    def __str__(self):
        return 'Message: {} to {}'.format(self.user_from, self.user_to)

class Payment(Model):

    user_profile = ForeignKey(UserProfile, on_delete=CASCADE, null=False)
    shelter      = ForeignKey(Shelter, on_delete=CASCADE, null=False)
    amount       = DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return 'Payment: {} from {} to {}'.format(self.amount, self.user_profile, self.shelter)

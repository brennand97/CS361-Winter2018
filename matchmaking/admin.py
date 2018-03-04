from django.contrib import admin
from .models import Location, ContactInfo, UserProfile, Shelter, PersonalityQualities, PhysicalQualities, Dog, Message, Payment

# Register your models here.
admin.site.register(Location)
admin.site.register(ContactInfo)
admin.site.register(UserProfile)
admin.site.register(Shelter)
admin.site.register(PersonalityQualities)
admin.site.register(PhysicalQualities)
admin.site.register(Dog)
admin.site.register(Message)
admin.site.register(Payment)
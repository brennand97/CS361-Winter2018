from django.test import TestCase

from .models import Location, Dog

# Create your tests here.

class SearchTestCase(TestCase):

    fixtures=['test_data']

    def setUp(self):
        #Location.objects.create(city="Corvallis", state="OR", zipcode=97333)
        pass

    def test_can_lookup_location(self):

        location = Location.objects.get(zipcode=97333)

        self.assertEqual(location.city, "Corvallis")
        self.assertEqual(location.state, "OR")

    def test_can_detect_bad_location(self):

        with self.assertRaises(Location.DoesNotExist) :
            location = Location.objects.get(zipcode=10000)

    def test_dog_by_location_lookup(self):

        location = Location.objects.get(zipcode=97333)
        self.assertIsNotNone(location)

        dogs = Dog.objects.filter(location=location)
        self.assertIsNotNone(dogs)

    def test_bad_dog_lookup(self):

        location = Location.objects.get(zipcode=77001)
        self.assertIsNotNone(location)

        dogs = Dog.objects.filter(location=location)
        # Use the fact that empty lists evaluate as False
        self.assertFalse(dogs)

    def test_different_dog_location_lookup(self):

        location_1 = Location.objects.get(zipcode=97333)
        self.assertIsNotNone(location_1)

        location_2 = Location.objects.get(zipcode=97331)
        self.assertIsNotNone(location_2)

        dogs_1 = Dog.objects.filter(location=location_1)
        self.assertIsNotNone(dogs_1)

        dogs_2 = Dog.objects.filter(location=location_2)
        self.assertIsNotNone(dogs_2)

        self.assertNotEqual(dogs_1, dogs_2)
